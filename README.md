# WIEMIP Data Request

Variable request for the Wetland and Inundation Extent Model Intercomparison Project (WIEMIP), aligned with CMIP7 CMOR table definitions.

## Contents

| File | Description |
|------|-------------|
| `WIEMIP_variable_request.xlsx` | Source-of-truth spreadsheet (one tab per working group) |
| `WIEMIP_variable_request.json` | Machine-readable JSON (one key per sheet, array of row objects) |
| `scripts/sync_airtable.py` | Syncs the JSON to an Airtable base |

## Airtable sync

The GitHub Actions workflow (`.github/workflows/sync-airtable.yml`) runs `scripts/sync_airtable.py` on every push to `main` that modifies the JSON, or on manual dispatch.

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
