import pytest

from voyage_testing_toolkit.processor import ProcessingError, process_payload
from voyage_testing_toolkit.testing import build_voyage_input
from voyage_testing_toolkit.voyage.consumption import calculate_consumption
from voyage_testing_toolkit.voyage.time_distance import calculate_time_distance


def test_process_payload_returns_voyage_json_output():
    payload = build_voyage_input()

    result = process_payload(payload)

    assert result["totalDistance"] == 4200
    assert result["totalEcaDistance"] == 250
    assert result["ladenDistance"] == 4200
    assert result["hsfoConsumption"] == 0
    assert result["vlsfoConsumption"] > 0
    assert result["lsmgoConsumption"] > 0
    assert result["totalBunkerCost"] > 0
    assert result["totalCo2"] > 0
    assert result["etsCost"] > 0
    assert result["fuelEuTotalPenalty"] > 0
    assert result["pAndL"] < result["grossFreight"]


def test_custom_input_builder_can_create_scrubber_scenario():
    payload = build_voyage_input()
    payload["vessel"]["hasScrubber"] = True

    result = process_payload(payload)

    assert result["hsfoConsumption"] > 0
    assert result["vlsfoConsumption"] > 0  # port load row still selects VLSFO
    assert result["euCoveredFuel"]["hsfo"] >= 0


def test_individual_time_and_consumption_modules_are_testable():
    payload = build_voyage_input()

    time_data = calculate_time_distance(payload["sequence"], payload["extraTime"])
    consumption = calculate_consumption(payload["vessel"], payload["bunker"], time_data)

    assert time_data["totalVoyageDays"] == 18.25
    assert time_data["portOperationDays"]["loading"] == 1.75
    assert consumption["fuelConsumption"]["vlsfo"] > 250


def test_regulatory_flags_change_total_voyage_costs():
    without_regulatory = build_voyage_input(applyEuaImpact=False, applyFuelEuImpact=False)
    with_regulatory = build_voyage_input(applyEuaImpact=True, applyFuelEuImpact=True)

    base_result = process_payload(without_regulatory)
    adjusted_result = process_payload(with_regulatory)

    assert adjusted_result["totalVoyageCosts"] > base_result["totalVoyageCosts"]


def test_process_payload_rejects_invalid_voyage_payload():
    with pytest.raises(ProcessingError, match="Missing required"):
        process_payload({"records": []})
