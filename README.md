# Warming-Induced Emissions Data Request

Variable request for the Wetland and Inundation Extent Model Intercomparison Project (WIEMIP), aligned with CMIP7 CMOR table definitions.

## Contents

| Path | Description                                                    |
|------|----------------------------------------------------------------|
| `WIEMIP_variable_request_20260527.xlsx` | Spreadsheet pulled from Google sheets on May 27th, 2026        |  
| `variables/` | One subdirectory per working group, one JSON file per variable |
| `scripts/sync_airtable.py` | Syncs the variable JSONs to an Airtable base                   |

### `variables/` layout

```
variables/
  first_priority/   # 98 variables
  fire/             # 22 variables
  permafrost/       # 25 variables
  soil_n2o/         #  8 variables
  methane/          #  4 variables
  mitigation/       # 13 variables
```

Each JSON file is named after the variable (e.g. `variables/first_priority/gpp.json`).

## Airtable sync

The GitHub Actions workflow (`.github/workflows/sync-airtable.yml`) runs `scripts/sync_airtable.py` on every push to `main` that modifies any `variables/**/*.json`, or on manual dispatch.

### Secrets required

| Secret | Description |
|--------|-------------|
| `AIRTABLE_TOKEN` | Personal access token (`pat...`) |
| `AIRTABLE_WORKSPACE_ID` | Target workspace (`wsp...`) |
| `AIRTABLE_BASE_ID` | Existing base ID (`app...`) — leave empty on first run to auto-create |

### Running locally

```bash
cp .env.example .env
# Fill in your Airtable credentials in .env
python scripts/sync_airtable.py
```
