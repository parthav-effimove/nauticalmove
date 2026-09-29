"""Public JSON processing entry point for voyage calculations."""

from __future__ import annotations

from typing import Any

from voyage_testing_toolkit.voyage.calculator import calculate_voyage
from voyage_testing_toolkit.voyage.validation import ProcessingError, validate_payload


def process_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate a JSON-compatible voyage payload and return JSON output."""

    validate_payload(payload)
    return calculate_voyage(payload)
