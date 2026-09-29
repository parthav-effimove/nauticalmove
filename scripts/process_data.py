"""Command-line JSON processor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from voyage_testing_toolkit.processor import ProcessingError, process_payload


def _read_json_input(value: str) -> dict:
    path = Path(value)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(value)


def main() -> int:
    parser = argparse.ArgumentParser(description="Process voyage JSON and print calculated output.")
    parser.add_argument(
        "input",
        help="Path to a JSON file or a raw JSON string.",
    )
    args = parser.parse_args()

    try:
        payload = _read_json_input(args.input)
        result = process_payload(payload)
    except (json.JSONDecodeError, ProcessingError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
