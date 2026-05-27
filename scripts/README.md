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
