"""Bottom-up EU-covered fuel and ETS detail calculations."""

from __future__ import annotations

from typing import Any

from voyage_testing_toolkit.voyage.emissions import CO2_EMISSION_FACTORS, calculate_ets_cost, get_ets_phase_in_percentage
from voyage_testing_toolkit.voyage.helpers import as_number, is_cargo_operation, is_discharge_operation, is_load_operation


def calculate_eu_coverage(
    sequence: list[dict[str, Any]],
    vessel: dict[str, Any],
    bunker: dict[str, Any],
    time_data: dict[str, Any],
) -> dict[str, Any]:
    has_scrubber = vessel.get("hasScrubber") is True
    profile = vessel.get("ecoConsumption") if vessel.get("speedProfile") == "eco" else vessel.get("fullConsumption")
    profile = profile or {}
    reward_factor = as_number(bunker.get("rewardFactor"), 1.0)
    phase = get_ets_phase_in_percentage()

    cargo_indexes = [i for i, leg in enumerate(sequence) if is_cargo_operation(leg.get("operation"))]
    bracket_origin: list[bool | None] = [None] * len(sequence)
    bracket_dest: list[bool | None] = [None] * len(sequence)
    cargo_on_board = 0.0
    for i, leg in enumerate(sequence):
        if cargo_on_board > 0:
            origins = [idx for idx in cargo_indexes if idx < i]
            dests = [idx for idx in cargo_indexes if idx >= i]
            if origins and dests and origins[-1] != dests[0]:
                bracket_origin[i] = _is_eu(sequence[origins[-1]])
                bracket_dest[i] = _is_eu(sequence[dests[0]])
        qty = max(0.0, as_number(leg.get("quantity")))
        if is_load_operation(leg.get("operation")):
            cargo_on_board += qty
        elif is_discharge_operation(leg.get("operation")):
            cargo_on_board = max(0.0, cargo_on_board - qty)

    eu_fuel = {"hsfo": 0.0, "vlsfo": 0.0, "lsmgo": 0.0}
    details: list[dict[str, Any]] = []
    weighted_factor = 0.0
    total_segment_sea_time = 0.0

    for i, leg in enumerate(sequence):
        factor = _coverage_factor(bracket_origin[i], bracket_dest[i])
        state = time_data["legStates"][i]
        sea_time = state["seaTime"]
        total_segment_sea_time += sea_time
        weighted_factor += sea_time * factor

        leg_fuel = _leg_fuel(leg, state, profile, has_scrubber, reward_factor)
        chargeable = {fuel: amount * factor for fuel, amount in leg_fuel.items()}
        for fuel, amount in chargeable.items():
            eu_fuel[fuel] += amount

        chargeable_co2 = sum(chargeable[fuel] * CO2_EMISSION_FACTORS[fuel] for fuel in eu_fuel)
        details.append(
            {
                "legIndex": i,
                "originIsEu": bracket_origin[i],
                "destIsEu": bracket_dest[i],
                "coveragePct": factor * 100,
                "coverageLabel": _coverage_label(bracket_origin[i], bracket_dest[i], factor),
                "chargeableHsfo": chargeable["hsfo"],
                "chargeableVlsfo": chargeable["vlsfo"],
                "chargeableLsmgo": chargeable["lsmgo"],
                "chargeableCo2": chargeable_co2,
            }
        )

    avg_factor = weighted_factor / total_segment_sea_time if total_segment_sea_time > 0 else 0.0
    if time_data["extraSeaDays"] > 0 and avg_factor > 0:
        if has_scrubber:
            eu_fuel["hsfo"] += time_data["extraSeaDays"] * _rate(profile, "hsfo", "laden") * reward_factor * avg_factor
        else:
            eu_fuel["vlsfo"] += time_data["extraSeaDays"] * _rate(profile, "vlsfo", "laden") * reward_factor * avg_factor
        ae = profile.get("aeScrubber") if has_scrubber and profile.get("aeScrubber") else profile.get("ae", {})
        eu_fuel["lsmgo"] += time_data["extraSeaDays"] * as_number(ae.get("laden")) * reward_factor * avg_factor

    eu_co2 = sum(eu_fuel[fuel] * CO2_EMISSION_FACTORS[fuel] for fuel in eu_fuel)
    chargeable_co2 = eu_co2 * phase
    ets_cost = calculate_ets_cost(chargeable_co2, as_number(bunker.get("co2Price")))

    return {
        "euCoveredFuel": eu_fuel,
        "etsLegDetails": details,
        "etsResult": {
            "phaseInPercentage": phase,
            "chargeableCo2": chargeable_co2,
            "etsCost": ets_cost,
            "legBreakdown": details,
        },
    }


def _leg_fuel(
    leg: dict[str, Any],
    state: dict[str, Any],
    profile: dict[str, Any],
    has_scrubber: bool,
    reward_factor: float,
) -> dict[str, float]:
    fuel = {"hsfo": 0.0, "vlsfo": 0.0, "lsmgo": 0.0}
    if has_scrubber:
        fuel["hsfo"] += state["nonEcaTime"] * _rate(profile, "hsfo", "laden" if state["isLaden"] else "ballast") * reward_factor
    else:
        fuel["vlsfo"] += state["nonEcaTime"] * _rate(profile, "vlsfo", "laden" if state["isLaden"] else "ballast") * reward_factor
    fuel["lsmgo"] += state["ecaTime"] * _rate(profile, "lsmgo", "laden" if state["isLaden"] else "ballast") * reward_factor

    ae = profile.get("aeScrubber") if has_scrubber and profile.get("aeScrubber") else profile.get("ae", {})
    fuel["lsmgo"] += state["seaTime"] * as_number(ae.get("laden" if state["isLaden"] else "ballast")) * reward_factor

    port_fuel = state["portFuelType"]
    operation = leg.get("operation")
    if is_load_operation(operation):
        fuel[port_fuel] += state["workingDays"] * _rate(profile, port_fuel, "load")
        fuel["lsmgo"] += state["workingDays"] * as_number(ae.get("load"))
    elif is_discharge_operation(operation):
        fuel[port_fuel] += state["workingDays"] * _rate(profile, port_fuel, "discharge")
        fuel["lsmgo"] += state["workingDays"] * as_number(ae.get("discharge"))
    elif as_number(leg.get("portDays")) > 0:
        fuel[port_fuel] += as_number(leg.get("portDays")) * _rate(profile, port_fuel, "idle")
        fuel["lsmgo"] += as_number(leg.get("portDays")) * as_number(ae.get("idle"))

    fuel[port_fuel] += state["turnExtraDays"] * _rate(profile, port_fuel, "idle")
    fuel["lsmgo"] += state["turnExtraDays"] * as_number(ae.get("idle"))
    return fuel


def _coverage_factor(origin: bool | None, dest: bool | None) -> float:
    if origin is None or dest is None:
        return 0.0
    if origin and dest:
        return 1.0
    if origin or dest:
        return 0.5
    return 0.0


def _coverage_label(origin: bool | None, dest: bool | None, factor: float) -> str:
    if origin is None or dest is None:
        return "No cargo bracket: 0%"
    if factor == 1:
        return "Cargo(EU) -> Cargo(EU): 100%"
    if factor == 0.5:
        return "Cargo(EU) -> Cargo(Non-EU): 50%" if origin else "Cargo(Non-EU) -> Cargo(EU): 50%"
    return "Cargo(Non-EU) -> Cargo(Non-EU): 0%"


def _is_eu(leg: dict[str, Any]) -> bool:
    return leg.get("isEuEea") is True


def _rate(profile: dict[str, Any], fuel: str, mode: str) -> float:
    return as_number((profile.get(fuel) or {}).get(mode))
