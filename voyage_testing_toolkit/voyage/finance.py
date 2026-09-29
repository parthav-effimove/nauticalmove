"""Freight, cost, hire, and profitability calculations."""

from __future__ import annotations

from typing import Any

from voyage_testing_toolkit.voyage.helpers import as_number


def calculate_finance(
    cargo: dict[str, Any],
    bunker: dict[str, Any],
    hire_rate: float,
    misc: dict[str, Any] | None,
    total_voyage_days: float,
    port_costs: float,
    fuel_consumption: dict[str, float],
    net_bb: float = 0.0,
    regulatory_cost: float = 0.0,
) -> dict[str, float]:
    misc = misc or {}
    quantity = as_number(cargo.get("quantity"))
    gross_freight = as_number(cargo.get("rate")) if cargo.get("rateType") == "lumpsum" else as_number(cargo.get("rate")) * quantity
    voyage_commission = gross_freight * (as_number(cargo.get("voyageCommission")) / 100)
    net_freight = gross_freight - voyage_commission

    hsfo_cost = fuel_consumption.get("hsfo", 0.0) * as_number((bunker.get("hsfo") or {}).get("price"))
    vlsfo_cost = fuel_consumption.get("vlsfo", 0.0) * as_number((bunker.get("vlsfo") or {}).get("price"))
    lsmgo_cost = fuel_consumption.get("lsmgo", 0.0) * as_number((bunker.get("lsmgo") or {}).get("price"))
    total_bunker_cost = hsfo_cost + vlsfo_cost + lsmgo_cost

    misc_costs = as_number(misc.get("miscCost")) + as_number(misc.get("extraFees")) + as_number(misc.get("extraInsurance"))
    canal_costs = as_number(misc.get("canalCost1")) + as_number(misc.get("canalCost2"))
    base_voyage_costs = total_bunker_cost + port_costs + misc_costs + canal_costs
    total_voyage_costs = base_voyage_costs + regulatory_cost

    hire_cost = hire_rate * total_voyage_days + max(0.0, net_bb)
    voyage_result = net_freight - total_voyage_costs + as_number(cargo.get("demurrage")) - as_number(cargo.get("despatch"))
    p_and_l = voyage_result - hire_cost
    tc_commission_pct = as_number(cargo.get("tcCommission")) / 100
    ntce = (net_freight - total_voyage_costs) / total_voyage_days if total_voyage_days > 0 else 0.0
    gtce = ntce / (1 - tc_commission_pct) if tc_commission_pct < 1 else 0.0
    voyage_cost_incl_hire = total_voyage_costs + hire_cost
    voyage_commission_pct = as_number(cargo.get("voyageCommission")) / 100
    base_rate_per_mt = voyage_cost_incl_hire / quantity if quantity > 0 else 0.0
    gross_rate = base_rate_per_mt / (1 - voyage_commission_pct) if voyage_commission_pct < 1 else 0.0

    return {
        "grossFreight": gross_freight,
        "voyageCommission": voyage_commission,
        "netFreight": net_freight,
        "hsfoCost": hsfo_cost,
        "vlsfoCost": vlsfo_cost,
        "lsmgoCost": lsmgo_cost,
        "totalBunkerCost": total_bunker_cost,
        "miscCosts": misc_costs,
        "canalCosts": canal_costs,
        "totalVoyageCosts": total_voyage_costs,
        "hireCost": hire_cost,
        "voyageCostInclHire": voyage_cost_incl_hire,
        "voyageCostExclHire": total_voyage_costs,
        "grossProfit": voyage_result,
        "netProfit": voyage_result,
        "pAndL": p_and_l,
        "ntce": ntce,
        "gtce": gtce,
        "tce": gtce,
        "grossRate": gross_rate,
    }
