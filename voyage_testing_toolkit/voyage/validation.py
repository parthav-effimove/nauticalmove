"""Validation for voyage JSON input."""

from __future__ import annotations

from typing import Any


class ProcessingError(ValueError):
    """Raised when input data cannot be processed."""


def validate_payload(payload: dict[str, Any]) -> None:
    if not isinstance(payload, dict):
        raise ProcessingError("Input JSON must be an object.")

    required = ("vessel", "sequence", "cargo", "bunker", "hireRate")
    missing = [field for field in required if field not in payload]
    if missing:
        raise ProcessingError(f"Missing required field(s): {', '.join(missing)}.")

    if not isinstance(payload["sequence"], list):
        raise ProcessingError("'sequence' must be a list.")
    if not payload["sequence"]:
        raise ProcessingError("'sequence' must contain at least one voyage row.")

    for field in ("vessel", "cargo", "bunker"):
        if not isinstance(payload[field], dict):
            raise ProcessingError(f"'{field}' must be an object.")

    _require_number(payload["cargo"], "quantity", "cargo")
    _require_number(payload, "hireRate", "root")

    for index, leg in enumerate(payload["sequence"]):
        if not isinstance(leg, dict):
            raise ProcessingError(f"sequence[{index}] must be an object.")
        for field in ("distance", "ecaDistance", "portDays", "quantity", "expDa"):
            _require_optional_number(leg, field, f"sequence[{index}]")


def _require_number(data: dict[str, Any], field: str, label: str) -> None:
    if field not in data or isinstance(data[field], bool) or not isinstance(data[field], (int, float)):
        raise ProcessingError(f"'{label}.{field}' must be numeric.")


def _require_optional_number(data: dict[str, Any], field: str, label: str) -> None:
    if field in data and data[field] is not None and (
        isinstance(data[field], bool) or not isinstance(data[field], (int, float))
    ):
        raise ProcessingError(f"'{label}.{field}' must be numeric when provided.")
