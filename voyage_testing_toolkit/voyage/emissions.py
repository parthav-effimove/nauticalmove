"""CO2, CII, EFOI, ETS, and FuelEU calculations."""

from __future__ import annotations

from typing import Any

CO2_EMISSION_FACTORS = {
    "hsfo": 3.114,
    "vlsfo": 3.151,
    "lsmgo": 3.206,
}


def calculate_co2_emissions(fuel: dict[str, float]) -> dict[str, float]:
    result = {
        fuel_name: round(fuel.get(fuel_name, 0.0) * factor, 6)
        for fuel_name, factor in CO2_EMISSION_FACTORS.items()
    }
    result["total"] = round(sum(result.values()), 6)
    return result


def calculate_efoi(total_co2: float, cargo_quantity: float, laden_distance: float) -> dict[str, float]:
    denominator = cargo_quantity * laden_distance
    return {"efoi": round((total_co2 * 1_000_000) / denominator, 6) if denominator > 0 else 0.0}


def calculate_cii_rating(total_co2: float, dwt: float, distance_travelled: float) -> dict[str, Any]:
    denominator = dwt * distance_travelled
    actual = round((total_co2 * 1_000_000) / denominator, 6) if denominator > 0 else 0.0
    if actual <= 2:
        rating = "A"
    elif actual <= 4:
        rating = "B"
    elif actual <= 6:
        rating = "C"
    elif actual <= 8:
        rating = "D"
    else:
        rating = "E"
    return {"actualCii": actual, "rating": rating}


def get_ets_phase_in_percentage() -> float:
    return 0.70


def calculate_ets_cost(chargeable_co2: float, co2_price: float) -> float:
    return round(chargeable_co2 * co2_price, 6)


def calculate_fuel_eu_penalty(eu_fuel: dict[str, float], reward_factor: float = 1.0) -> dict[str, Any]:
    # Configurable placeholder model for scenario testing. Keep rates in one place.
    penalty_rates = {"hsfo": 48.0, "vlsfo": 42.0, "lsmgo": 18.0}
    fuels: dict[str, dict[str, float]] = {}
    for fuel_name, rate in penalty_rates.items():
        quantity = eu_fuel.get(fuel_name, 0.0)
        cost = quantity * rate * reward_factor
        fuels[fuel_name] = {"quantity": round(quantity, 6), "rate": rate, "cost": round(cost, 6)}
    return {"fuels": fuels, "totalPenalty": round(sum(fuel["cost"] for fuel in fuels.values()), 6)}


def validate_emission_inputs(
    fuel: dict[str, float],
    dwt: float,
    distance: float,
    cargo_quantity: float,
    co2_price: float,
) -> dict[str, list[str]]:
    warnings: list[str] = []
    errors: list[str] = []
    if sum(fuel.values()) <= 0:
        warnings.append("Total fuel consumption is zero.")
    if dwt <= 0:
        errors.append("Vessel DWT must be greater than zero.")
    if distance <= 0:
        warnings.append("Total distance is zero.")
    if cargo_quantity <= 0:
        warnings.append("Cargo quantity is zero.")
    if co2_price < 0:
        errors.append("CO2 price cannot be negative.")
    return {"warnings": warnings, "errors": errors}
