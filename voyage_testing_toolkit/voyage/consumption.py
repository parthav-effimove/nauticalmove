"""Fuel consumption calculations."""

from __future__ import annotations

from typing import Any

from voyage_testing_toolkit.voyage.helpers import as_number


def calculate_consumption(vessel: dict[str, Any], bunker: dict[str, Any], time_data: dict[str, Any]) -> dict[str, Any]:
    has_scrubber = vessel.get("hasScrubber") is True
    profile_name = "ecoConsumption" if vessel.get("speedProfile") == "eco" else "fullConsumption"
    profile = vessel.get(profile_name) or vessel.get("consumptionProfile") or {}
    reward_factor = as_number(bunker.get("rewardFactor"), 1.0)

    def rate(fuel: str, mode: str) -> float:
        return as_number((profile.get(fuel) or {}).get(mode))

    hsfo_sea = 0.0
    vlsfo_sea = 0.0
    if has_scrubber:
        hsfo_sea = (
            time_data["nonEcaSeaDaysBallast"] * rate("hsfo", "ballast")
            + time_data["nonEcaSeaDaysLaden"] * rate("hsfo", "laden")
            + time_data["extraSeaDays"] * rate("hsfo", "laden")
        ) * reward_factor
    else:
        vlsfo_sea = (
            time_data["nonEcaSeaDaysBallast"] * rate("vlsfo", "ballast")
            + time_data["nonEcaSeaDaysLaden"] * rate("vlsfo", "laden")
            + time_data["extraSeaDays"] * rate("vlsfo", "laden")
        ) * reward_factor

    lsmgo_eca_sea = (
        time_data["ecaSeaDaysBallast"] * rate("lsmgo", "ballast")
        + time_data["ecaSeaDaysLaden"] * rate("lsmgo", "laden")
    ) * reward_factor

    port_by_fuel = time_data["portDaysByFuel"]
    hsfo_port = _port_consumption(port_by_fuel, profile, "hsfo")
    vlsfo_port = _port_consumption(port_by_fuel, profile, "vlsfo")
    lsmgo_port = _port_consumption(port_by_fuel, profile, "lsmgo")

    extra_port_fuel = "hsfo" if has_scrubber else "vlsfo"
    if extra_port_fuel == "hsfo":
        hsfo_port += time_data["extraPortDays"] * rate("hsfo", "idle")
    else:
        vlsfo_port += time_data["extraPortDays"] * rate("vlsfo", "idle")

    hsfo_canal = time_data["extraCanalDays"] * rate("hsfo", "canal") if has_scrubber else 0.0
    vlsfo_canal = time_data["extraCanalDays"] * rate("vlsfo", "canal") if not has_scrubber else 0.0

    ae_profile = profile.get("aeScrubber") if has_scrubber and profile.get("aeScrubber") else profile.get("ae", {})
    ae_sea = (
        (time_data["nonEcaSeaDaysBallast"] + time_data["ecaSeaDaysBallast"]) * as_number(ae_profile.get("ballast"))
        + (time_data["nonEcaSeaDaysLaden"] + time_data["ecaSeaDaysLaden"]) * as_number(ae_profile.get("laden"))
        + time_data["extraSeaDays"] * as_number(ae_profile.get("laden"))
    ) * reward_factor
    op_days = time_data["portOperationDays"]
    ae_port = (
        op_days["loading"] * as_number(ae_profile.get("load"))
        + op_days["discharging"] * as_number(ae_profile.get("discharge"))
        + (op_days["idle"] + op_days["bunkering"] + time_data["extraPortDays"]) * as_number(ae_profile.get("idle"))
    )

    hsfo = hsfo_sea + hsfo_port + hsfo_canal
    vlsfo = vlsfo_sea + vlsfo_port + vlsfo_canal
    lsmgo = lsmgo_eca_sea + lsmgo_port + ae_sea + ae_port

    non_eca_fuel = {"hsfo": hsfo_sea, "vlsfo": vlsfo_sea, "lsmgo": 0.0}
    non_eca_fuel["total"] = sum(non_eca_fuel.values())
    eca_fuel = {"hsfo": 0.0, "vlsfo": 0.0, "lsmgo": lsmgo_eca_sea, "total": lsmgo_eca_sea}

    return {
        "fuelConsumption": {"hsfo": hsfo, "vlsfo": vlsfo, "lsmgo": lsmgo},
        "nonEcaFuel": non_eca_fuel,
        "ecaFuel": eca_fuel,
        "breakdown": {
            "sea": {"hsfo": hsfo_sea, "vlsfo": vlsfo_sea, "lsmgo": lsmgo_eca_sea},
            "port": {"hsfo": hsfo_port, "vlsfo": vlsfo_port, "lsmgo": lsmgo_port},
            "canal": {"hsfo": hsfo_canal, "vlsfo": vlsfo_canal, "lsmgo": 0.0},
            "auxiliaryEngine": {"lsmgoSea": ae_sea, "lsmgoPort": ae_port},
        },
    }


def _port_consumption(port_by_fuel: dict[str, dict[str, float]], profile: dict[str, Any], fuel: str) -> float:
    fuel_profile = profile.get(fuel) or {}
    return (
        port_by_fuel["loading"][fuel] * as_number(fuel_profile.get("load"))
        + port_by_fuel["discharging"][fuel] * as_number(fuel_profile.get("discharge"))
        + (port_by_fuel["idle"][fuel] + port_by_fuel["bunkering"][fuel]) * as_number(fuel_profile.get("idle"))
    )
