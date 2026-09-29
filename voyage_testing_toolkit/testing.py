"""Custom test-input builder for voyage scenarios."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


def build_voyage_input(**overrides: Any) -> dict[str, Any]:
    """Create a realistic default voyage input and apply shallow top-level overrides."""

    payload = deepcopy(DEFAULT_VOYAGE_INPUT)
    for key, value in overrides.items():
        payload[key] = value
    return payload


DEFAULT_PROFILE = {
    "hsfo": {"ballast": 18, "laden": 24, "load": 3, "discharge": 3.2, "idle": 1.5, "canal": 4},
    "vlsfo": {"ballast": 17, "laden": 23, "load": 2.8, "discharge": 3, "idle": 1.4, "canal": 3.8},
    "lsmgo": {"ballast": 2, "laden": 2.5, "load": 0.8, "discharge": 0.9, "idle": 0.5, "canal": 0},
    "ae": {"ballast": 1.2, "laden": 1.4, "load": 1.8, "discharge": 2.0, "idle": 0.7},
    "aeScrubber": {"ballast": 1.4, "laden": 1.6, "load": 2.0, "discharge": 2.2, "idle": 0.8},
}

DEFAULT_VOYAGE_INPUT = {
    "vessel": {
        "name": "Demo Vessel",
        "dwt": 82000,
        "type": "bulk_carrier",
        "speedProfile": "eco",
        "hasScrubber": False,
        "ecoConsumption": DEFAULT_PROFILE,
        "fullConsumption": DEFAULT_PROFILE,
    },
    "sequence": [
        {
            "id": 1,
            "operation": "load",
            "port": "Santos",
            "portUnloc": "BRSSZ",
            "isEuEea": False,
            "distance": 0,
            "ecaDistance": 0,
            "seaTime": 0,
            "ecaTime": 0,
            "nonEcaTime": 0,
            "portDays": 2.0,
            "quantity": 50000,
            "expDa": 10000,
            "turnTimeHours": 6,
            "extraTimeHours": 0,
            "portFuelType": "vlsfo",
        },
        {
            "id": 2,
            "operation": "disch",
            "port": "Rotterdam",
            "portUnloc": "NLRTM",
            "isEuEea": True,
            "distance": 4200,
            "ecaDistance": 250,
            "seaTime": 12.5,
            "ecaTime": 0.8,
            "nonEcaTime": 11.7,
            "portDays": 3.0,
            "quantity": 50000,
            "expDa": 18000,
            "turnTimeHours": 8,
            "extraTimeHours": 4,
            "portFuelType": "lsmgo",
        },
    ],
    "cargo": {
        "rate": 32,
        "rateType": "mt",
        "quantity": 50000,
        "voyageCommission": 2.5,
        "tcCommission": 3.75,
        "demurrage": 0,
        "despatch": 0,
    },
    "bunker": {
        "hsfo": {"price": 460, "robStart": 0},
        "vlsfo": {"price": 610, "robStart": 0},
        "lsmgo": {"price": 790, "robStart": 0},
        "co2Price": 85,
        "rewardFactor": 1.0,
    },
    "hireRate": 14500,
    "netBB": 0,
    "misc": {"miscCost": 5000, "extraFees": 1200, "extraInsurance": 800, "canalCost1": 0, "canalCost2": 0},
    "extraTime": {"canal1Days": 0, "canal2Days": 0, "idlePortDays": 0.5, "atSeaDays": 0.25, "atSeaSpeedContext": "EV"},
    "applyEuaImpact": True,
    "applyFuelEuImpact": True,
}
