# Voyage Testing Toolkit

Python toolkit for voyage calculation testing. It accepts voyage input as JSON, returns JSON output, and keeps each calculation area in its own module.

## Setup

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

## Run

```powershell
python scripts\process_data.py examples\input.json
```

You can also pass JSON directly:

```powershell
python scripts\process_data.py "{""vessel"":{...},""sequence"":[...],""cargo"":{...},""bunker"":{...},""hireRate"":14500}"
```

## Test

```powershell
python -m pytest
```

## Modules

- `voyage_testing_toolkit.voyage.time_distance`: distances, ballast/laden state, port days
- `voyage_testing_toolkit.voyage.consumption`: HSFO/VLSFO/LSMGO consumption
- `voyage_testing_toolkit.voyage.emissions`: CO2, CII, EFOI, FuelEU helpers
- `voyage_testing_toolkit.voyage.ets`: EU-covered fuel and ETS chargeable CO2
- `voyage_testing_toolkit.voyage.finance`: freight, costs, hire, TCE, P&L

Use `voyage_testing_toolkit.testing.build_voyage_input()` in tests to create custom scenario input quickly.

## Create Custom Input

```powershell
python scripts\create_input.py --output examples\custom_input.json --scrubber --hire-rate 16000 --co2-price 90
python scripts\process_data.py examples\custom_input.json
```

# nauticalmove
