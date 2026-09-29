"""Distance, sea time, port time, and cargo-state calculations."""

from __future__ import annotations

from typing import Any

from voyage_testing_toolkit.voyage.helpers import as_number, is_discharge_operation, is_load_operation, operation_name


def calculate_time_distance(sequence: list[dict[str, Any]], extra_time: dict[str, Any] | None) -> dict[str, Any]:
    total_distance = 0.0
    total_eca_distance = 0.0
    ballast_distance = 0.0
    laden_distance = 0.0
    sea_days_ballast = 0.0
    sea_days_laden = 0.0
    eca_sea_days_ballast = 0.0
    eca_sea_days_laden = 0.0
    non_eca_sea_days_ballast = 0.0
    non_eca_sea_days_laden = 0.0
    total_port_days = 0.0
    port_costs = 0.0
    base_sea_time = 0.0
    sea_margin_time = 0.0
    cargo_on_board = 0.0

    port_days_by_fuel = {
        "loading": {"hsfo": 0.0, "vlsfo": 0.0, "lsmgo": 0.0},
        "discharging": {"hsfo": 0.0, "vlsfo": 0.0, "lsmgo": 0.0},
        "idle": {"hsfo": 0.0, "vlsfo": 0.0, "lsmgo": 0.0},
        "bunkering": {"hsfo": 0.0, "vlsfo": 0.0, "lsmgo": 0.0},
    }
    totals_by_operation = {"loading": 0.0, "discharging": 0.0, "idle": 0.0, "bunkering": 0.0}
    leg_states: list[dict[str, Any]] = []

    for index, leg in enumerate(sequence):
        distance = as_number(leg.get("distance"))
        eca_distance = as_number(leg.get("ecaDistance"))
        port_days = as_number(leg.get("portDays"))
        sea_time = as_number(leg.get("seaTime"))
        eca_time = as_number(leg.get("ecaTime"))
        non_eca_time = as_number(leg.get("nonEcaTime"), sea_time - eca_time)
        quantity = max(0.0, as_number(leg.get("quantity")))
        leg_is_laden = cargo_on_board > 0

        total_distance += distance
        total_eca_distance += eca_distance
        total_port_days += port_days
        port_costs += as_number(leg.get("expDa"))
        base_sea_time += as_number(leg.get("baseSeaTime"))
        sea_margin_time += as_number(leg.get("seaMarginTime"))

        if leg_is_laden:
            laden_distance += distance
            sea_days_laden += sea_time
            eca_sea_days_laden += eca_time
            non_eca_sea_days_laden += non_eca_time
        else:
            ballast_distance += distance
            sea_days_ballast += sea_time
            eca_sea_days_ballast += eca_time
            non_eca_sea_days_ballast += non_eca_time

        leg_port_fuel = leg.get("portFuelType") or "vlsfo"
        turn_extra_days = (as_number(leg.get("turnTimeHours")) + as_number(leg.get("extraTimeHours"))) / 24
        working_days = max(0.0, port_days - turn_extra_days)
        op = operation_name(leg.get("operation"))

        if is_load_operation(op):
            totals_by_operation["loading"] += working_days
            totals_by_operation["idle"] += turn_extra_days
            port_days_by_fuel["loading"][leg_port_fuel] += working_days
            port_days_by_fuel["idle"][leg_port_fuel] += turn_extra_days
        elif is_discharge_operation(op):
            totals_by_operation["discharging"] += working_days
            totals_by_operation["idle"] += turn_extra_days
            port_days_by_fuel["discharging"][leg_port_fuel] += working_days
            port_days_by_fuel["idle"][leg_port_fuel] += turn_extra_days
        elif op == "bunkering":
            totals_by_operation["bunkering"] += port_days
            port_days_by_fuel["bunkering"][leg_port_fuel] += port_days
        elif port_days > 0:
            totals_by_operation["idle"] += port_days
            port_days_by_fuel["idle"][leg_port_fuel] += port_days

        leg_states.append(
            {
                "index": index,
                "isLaden": leg_is_laden,
                "cargoOnBoardBefore": cargo_on_board,
                "seaTime": sea_time,
                "ecaTime": eca_time,
                "nonEcaTime": non_eca_time,
                "workingDays": working_days,
                "turnExtraDays": turn_extra_days,
                "portFuelType": leg_port_fuel,
            }
        )

        if is_load_operation(op):
            cargo_on_board += quantity
        elif is_discharge_operation(op):
            cargo_on_board = max(0.0, cargo_on_board - quantity)

    extra_time = extra_time or {}
    extra_sea_days = as_number(extra_time.get("atSeaDays"))
    extra_port_days = as_number(extra_time.get("idlePortDays"))
    extra_canal_days = as_number(extra_time.get("canal1Days")) + as_number(extra_time.get("canal2Days"))
    total_sea_days = sea_days_ballast + sea_days_laden + extra_sea_days

    return {
        "totalDistance": total_distance,
        "totalEcaDistance": total_eca_distance,
        "ballastDistance": ballast_distance,
        "ladenDistance": laden_distance,
        "seaDaysBallast": sea_days_ballast,
        "seaDaysLaden": sea_days_laden,
        "ecaSeaDaysBallast": eca_sea_days_ballast,
        "ecaSeaDaysLaden": eca_sea_days_laden,
        "nonEcaSeaDaysBallast": non_eca_sea_days_ballast,
        "nonEcaSeaDaysLaden": non_eca_sea_days_laden,
        "totalSeaDays": total_sea_days,
        "totalPortDays": total_port_days,
        "extraSeaDays": extra_sea_days,
        "extraPortDays": extra_port_days,
        "extraCanalDays": extra_canal_days,
        "totalVoyageDays": total_sea_days + total_port_days + extra_port_days + extra_canal_days,
        "baseSeaTime": base_sea_time,
        "seaMarginTime": sea_margin_time,
        "portCosts": port_costs,
        "portDaysByFuel": port_days_by_fuel,
        "portOperationDays": totals_by_operation,
        "legStates": leg_states,
    }
