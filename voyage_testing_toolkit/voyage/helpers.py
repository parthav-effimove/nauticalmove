"""Small helpers for dict-based voyage calculations."""

from __future__ import annotations

from numbers import Real
from typing import Any


def as_number(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, bool) or not isinstance(value, Real):
        return default
    return float(value)


def operation_name(value: Any) -> str:
    return str(value or "").strip().lower()


def is_load_operation(value: Any) -> bool:
    return operation_name(value) in {"load", "loading"}


def is_discharge_operation(value: Any) -> bool:
    return operation_name(value) in {"disch", "discharging", "discharge"}


def is_cargo_operation(value: Any) -> bool:
    return is_load_operation(value) or is_discharge_operation(value)


def fuel_names() -> tuple[str, str, str]:
    return ("hsfo", "vlsfo", "lsmgo")
