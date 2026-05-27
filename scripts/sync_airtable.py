#!/usr/bin/env python3
"""
Sync the WIEMIP variable request JSON to Airtable.

Reads per-variable JSON files from the variables/ directory tree and syncs
each subdirectory to its own Airtable table inside a single base.

On first run (no AIRTABLE_BASE_ID set), creates a new base with one table
per sheet.  On subsequent runs, clears and re-populates every table.

Environment variables (via .env or GitHub Actions secrets):
    AIRTABLE_TOKEN         – Personal access token (pat...)
    AIRTABLE_WORKSPACE_ID  – Target workspace (wsp...)
    AIRTABLE_BASE_ID       – (optional) Existing base ID; written to .env
                             after first creation.

Usage:
    python scripts/sync_airtable.py

No external dependencies beyond the Python standard library.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VARIABLES_DIR = REPO_ROOT / "variables"
ENV_PATH = REPO_ROOT / ".env"

API_BASE = "https://api.airtable.com/v0"
BATCH_SIZE = 10  # Airtable max records per request

# Field name -> Airtable field type (used when creating tables)
FIELD_TYPES = {
    "Variable": "singleLineText",
    "Unit": "singleLineText",
    "Comment": "multilineText",
    "Variable name": "singleLineText",
    "CMOR dimensions": "singleLineText",
    "Calendar": "singleLineText",
    "missing value": "singleLineText",
    "Frequency": "singleLineText",
    "CMIP7 Compound Name": "singleLineText",
    "CMIP7 Branded Variable Name": "singleLineText",
    "CMIP7 Frequency": "singleLineText",
    "CF Standard Name": "singleLineText",
    "CMIP7 Description": "multilineText",
    "CMIP7 Title": "singleLineText",
}

# Extra fields that appear only in some sheets
EXTRA_FIELD_TYPES = {
    "Note": "singleLineText",
}


def load_dotenv():
    """Minimal .env loader."""
    if ENV_PATH.exists():
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, val = line.partition("=")
                    key = key.strip()
                    val = val.strip()
                    if not os.environ.get(key):
                        os.environ[key] = val


def save_base_id(base_id: str):
    """Update AIRTABLE_BASE_ID in the .env file."""
    lines = []
    found = False
    if ENV_PATH.exists():
        with open(ENV_PATH) as f:
            lines = f.readlines()
    new_lines = []
    for line in lines:
        if line.strip().startswith("AIRTABLE_BASE_ID"):
            new_lines.append(f"AIRTABLE_BASE_ID={base_id}\n")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"AIRTABLE_BASE_ID={base_id}\n")
    with open(ENV_PATH, "w") as f:
        f.writelines(new_lines)


def get_token() -> str:
    token = os.environ.get("AIRTABLE_TOKEN", "")
    if not token:
        sys.exit("AIRTABLE_TOKEN not set. See .env.example.")
    return token


def api_request(method: str, url: str, data: dict | None = None) -> dict:
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {get_token()}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode()
        sys.exit(f"Airtable API error ({e.code} {method} {url}):\n{body_text}")


def fields_for_sheet(sheet_name: str, rows: list[dict]) -> list[dict]:
    """Build the Airtable field definitions for a sheet."""
    fields = [{"name": n, "type": t} for n, t in FIELD_TYPES.items()]
    seen = set(FIELD_TYPES.keys())
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                ftype = EXTRA_FIELD_TYPES.get(key, "singleLineText")
                fields.append({"name": key, "type": ftype})
    return fields


def create_base(workspace_id: str, sheets: dict) -> str:
    """Create a new base with one table per sheet."""
    tables = []
    for sheet_name, rows in sheets.items():
        tables.append({
            "name": sheet_name,
            "fields": fields_for_sheet(sheet_name, rows),
        })
    payload = {
        "name": "WIEMIP Variable Request",
        "workspaceId": workspace_id,
        "tables": tables,
    }
    result = api_request("POST", f"{API_BASE}/meta/bases", payload)
    base_id = result["id"]
    print(f"  Created base: {base_id}")
    return base_id


def list_records(base_id: str, table_name: str) -> list[str]:
    record_ids = []
    encoded = urllib.parse.quote(table_name, safe="")
    offset = None
    while True:
        url = f"{API_BASE}/{base_id}/{encoded}"
        if offset:
            url += f"?offset={urllib.parse.quote(offset)}"
        data = api_request("GET", url)
        for rec in data.get("records", []):
            record_ids.append(rec["id"])
        offset = data.get("offset")
        if not offset:
            break
    return record_ids


def delete_records(base_id: str, table_name: str, record_ids: list[str]):
    encoded = urllib.parse.quote(table_name, safe="")
    for i in range(0, len(record_ids), BATCH_SIZE):
        batch = record_ids[i : i + BATCH_SIZE]
        params = "&".join(f"records[]={urllib.parse.quote(rid)}" for rid in batch)
        url = f"{API_BASE}/{base_id}/{encoded}?{params}"
        api_request("DELETE", url)
        time.sleep(0.25)


def create_records(base_id: str, table_name: str, rows: list[dict]):
    encoded = urllib.parse.quote(table_name, safe="")
    url = f"{API_BASE}/{base_id}/{encoded}"
    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i : i + BATCH_SIZE]
        records = []
        for row in batch:
            fields = {k: v for k, v in row.items() if v}
            records.append({"fields": fields})
        api_request("POST", url, {"records": records})
        time.sleep(0.25)


# Directory name -> Airtable table name
DIR_TO_TABLE = {
    "first_priority": "First priority",
    "fire": "Fire",
    "permafrost": "Permafrost",
    "soil_n2o": "Soil N2O",
    "methane": "Methane",
    "mitigation": "Mitigation",
}


def read_variables_dir(variables_dir: Path) -> dict[str, list[dict]]:
    """Read per-variable JSONs from the directory structure."""
    sheets: dict[str, list[dict]] = {}
    for dirname, table_name in DIR_TO_TABLE.items():
        d = variables_dir / dirname
        if not d.is_dir():
            continue
        rows = []
        for f in sorted(d.glob("*.json")):
            with open(f) as fh:
                rows.append(json.load(fh))
        sheets[table_name] = rows
    return sheets



def main():
    load_dotenv()

    workspace_id = os.environ.get("AIRTABLE_WORKSPACE_ID", "")
    base_id = os.environ.get("AIRTABLE_BASE_ID", "")

    print(f"Reading {VARIABLES_DIR} ...")
    sheets = read_variables_dir(VARIABLES_DIR)
    for name, rows in sheets.items():
        print(f"  {name}: {len(rows)} rows")

    if not base_id:
        if not workspace_id:
            sys.exit("AIRTABLE_WORKSPACE_ID not set. See .env.example.")
        print("No AIRTABLE_BASE_ID set — creating new base ...")
        base_id = create_base(workspace_id, sheets)
        save_base_id(base_id)
        os.environ["AIRTABLE_BASE_ID"] = base_id
    else:
        print(f"Using existing base: {base_id}")
        for name in sheets:
            print(f"  Clearing {name} ...")
            existing = list_records(base_id, name)
            if existing:
                delete_records(base_id, name, existing)
                print(f"    Deleted {len(existing)} records.")

    for name, rows in sheets.items():
        print(f"Uploading {name} ({len(rows)} rows) ...")
        create_records(base_id, name, rows)

    print("Done.")


if __name__ == "__main__":
    main()
