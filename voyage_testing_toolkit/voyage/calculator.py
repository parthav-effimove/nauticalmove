"""Top-level orchestration for modular voyage calculations."""

from __future__ import annotations

from typing import Any

from voyage_testing_toolkit.voyage.consumption import calculate_consumption
from voyage_testing_toolkit.voyage.emissions import (
    calculate_cii_rating,
    calculate_co2_emissions,
    calculate_efoi,
    calculate_fuel_eu_penalty,
    validate_emission_inputs,
)
from voyage_testing_toolkit.voyage.ets import calculate_eu_coverage
from voyage_testing_toolkit.voyage.finance import calculate_finance
from voyage_testing_toolkit.voyage.helpers import as_number
from voyage_testing_toolkit.voyage.time_distance import calculate_time_distance


def calculate_voyage(payload: dict[str, Any]) -> dict[str, Any]:
    vessel = payload["vessel"]
    sequence = payload["sequence"]
    cargo = payload["cargo"]
    bunker = payload["bunker"]
    hire_rate = as_number(payload.get("hireRate"))
    misc = payload.get("misc") or {}
    extra_time = payload.get("extraTime") or {}

    time_data = calculate_time_distance(sequence, extra_time)
    consumption_data = calculate_consumption(vessel, bunker, time_data)
    fuel = consumption_data["fuelConsumption"]

    co2_by_fuel = calculate_co2_emissions(fuel)
    non_eca_co2 = calculate_co2_emissions(consumption_data["nonEcaFuel"])["total"]
    eca_co2 = calculate_co2_emissions(consumption_data["ecaFuel"])["total"]
    total_co2 = co2_by_fuel["total"]
    total_sea_days = time_data["totalSeaDays"]
    co2_ballast = total_co2 * (time_data["seaDaysBallast"] / total_sea_days) if total_sea_days > 0 else 0.0
    co2_laden = total_co2 * (time_data["seaDaysLaden"] / total_sea_days) if total_sea_days > 0 else 0.0
    efoi = calculate_efoi(total_co2, as_number(cargo.get("quantity")), time_data["ladenDistance"])["efoi"]
    cii_result = calculate_cii_rating(
        total_co2,
        as_number(vessel.get("dwt")),
        time_data["totalDistance"] + time_data["totalEcaDistance"],
    )

    eu = calculate_eu_coverage(sequence, vessel, bunker, time_data)
    eu["etsResult"]["totalCo2"] = total_co2
    eu["etsResult"]["etsVoyageCoverage"] = _weighted_coverage(total_co2, eu["etsLegDetails"])

    fuel_eu_result = calculate_fuel_eu_penalty(eu["euCoveredFuel"], as_number(bunker.get("rewardFactor"), 1.0))
    eua_cost = eu["etsResult"]["etsCost"]
    regulatory_cost = 0.0
    if payload.get("applyEuaImpact"):
        regulatory_cost += eua_cost
    if payload.get("applyFuelEuImpact"):
        regulatory_cost += fuel_eu_result["totalPenalty"]

    finance = calculate_finance(
        cargo,
        bunker,
        hire_rate,
        misc,
        time_data["totalVoyageDays"],
        time_data["portCosts"],
        fuel,
        as_number(payload.get("netBB")),
        regulatory_cost,
    )

    validation = validate_emission_inputs(
        fuel,
        as_number(vessel.get("dwt")),
        time_data["totalDistance"] + time_data["totalEcaDistance"],
        as_number(cargo.get("quantity")),
        as_number(bunker.get("co2Price")),
    )

    return _round_nested(
        {
            **_select_public_time_fields(time_data),
            "hsfoConsumption": fuel["hsfo"],
            "vlsfoConsumption": fuel["vlsfo"],
            "lsmgoConsumption": fuel["lsmgo"],
            "consumptionBreakdown": consumption_data["breakdown"],
            "nonEcaFuel": consumption_data["nonEcaFuel"],
            "ecaFuel": consumption_data["ecaFuel"],
            "nonEcaCo2": non_eca_co2,
            "ecaCo2": eca_co2,
            "nonEcaDistance": time_data["totalDistance"],
            "finance": finance,
            "totalCo2": total_co2,
            "co2Laden": co2_laden,
            "co2Ballast": co2_ballast,
            "co2ByFuel": co2_by_fuel,
            "efoi": efoi,
            "afrCii": cii_result["actualCii"],
            "ciiRating": cii_result["rating"],
            "ciiResult": cii_result,
            "etsResult": eu["etsResult"],
            "etsCost": eu["etsResult"]["etsCost"],
            "chargeableCo2": eu["etsResult"]["chargeableCo2"],
            "etsVoyageCoverage": eu["etsResult"]["etsVoyageCoverage"],
            "etsPhaseIn": eu["etsResult"]["phaseInPercentage"],
            "etsLegDetails": eu["etsLegDetails"],
            "emissionWarnings": validation["warnings"],
            "emissionErrors": validation["errors"],
            "ladenDistance": time_data["ladenDistance"],
            "euCoveredFuel": eu["euCoveredFuel"],
            "totalCo2Cost": total_co2 * as_number(bunker.get("co2Price")),
            "euaCo2Cost": eua_cost,
            "euaFreightImpact": eua_cost / as_number(cargo.get("quantity")) if as_number(cargo.get("quantity")) > 0 else 0.0,
            "fuelEuResult": fuel_eu_result,
            "fuelEuTotalPenalty": fuel_eu_result["totalPenalty"],
            "fuelEuFreightImpact": fuel_eu_result["totalPenalty"] / as_number(cargo.get("quantity")) if as_number(cargo.get("quantity")) > 0 else 0.0,
        }
    )


def _select_public_time_fields(time_data: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "totalDistance",
        "totalEcaDistance",
        "seaDaysBallast",
        "seaDaysLaden",
        "totalSeaDays",
        "totalPortDays",
        "extraSeaDays",
        "extraPortDays",
        "extraCanalDays",
        "totalVoyageDays",
        "baseSeaTime",
        "seaMarginTime",
        "portCosts",
    ]
    return {key: time_data[key] for key in keys}


def _weighted_coverage(total_co2: float, details: list[dict[str, Any]]) -> float:
    if total_co2 <= 0:
        return 0.0
    # Details store chargeable CO2 before phase-in only by leg factor; this is informational.
    covered = sum(detail["chargeableCo2"] for detail in details)
    return min(1.0, covered / total_co2)


def _round_nested(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 6)
    if isinstance(value, list):
        return [_round_nested(item) for item in value]
    if isinstance(value, dict):
        return {key: _round_nested(item) for key, item in value.items()}
    return value
