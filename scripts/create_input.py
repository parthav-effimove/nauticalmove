"""Create custom voyage input JSON from the built-in test scenario."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from voyage_testing_toolkit.testing import build_voyage_input


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a voyage input JSON scenario.")
    parser.add_argument("--output", default="examples/custom_input.json", help="Output JSON path.")
    parser.add_argument("--scrubber", action="store_true", help="Set vessel.hasScrubber=true.")
    parser.add_argument("--hire-rate", type=float, help="Override hireRate.")
    parser.add_argument("--cargo-quantity", type=float, help="Override cargo.quantity and load/discharge quantities.")
    parser.add_argument("--co2-price", type=float, help="Override bunker.co2Price.")
    parser.add_argument("--no-regulatory-impact", action="store_true", help="Disable EUA and FuelEU cost impact.")
    args = parser.parse_args()

    payload = build_voyage_input()
    if args.scrubber:
        payload["vessel"]["hasScrubber"] = True
    if args.hire_rate is not None:
        payload["hireRate"] = args.hire_rate
    if args.cargo_quantity is not None:
        payload["cargo"]["quantity"] = args.cargo_quantity
        for leg in payload["sequence"]:
            if leg["operation"] in {"load", "disch", "discharging", "loading"}:
                leg["quantity"] = args.cargo_quantity
    if args.co2_price is not None:
        payload["bunker"]["co2Price"] = args.co2_price
    if args.no_regulatory_impact:
        payload["applyEuaImpact"] = False
        payload["applyFuelEuImpact"] = False

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
