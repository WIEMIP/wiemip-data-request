#!/usr/bin/env python3
"""
Check the "cf_compliant_units" key of variable JSONs with UDUNITS-2.

Prints what UDUNITS resolves each unit to, so a unit that parses to the wrong
quantity (e.g. "kg C m-2", where C is read as coulombs) is visible by eye.
Exits 1 if any unit is missing, empty, or not recognized.

Needs the udunits2 command line tool (brew install udunits / apt install udunits-bin).

Usage:
    python scripts/check_cf_units.py variables/methane/fch4soil.json
    python scripts/check_cf_units.py variables/*/*.json
"""

import json
import subprocess
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)

failed = 0
for path in sys.argv[1:]:
    with open(path) as fh:
        units = (json.load(fh).get("cf_compliant_units") or "").strip()

    # udunits2 reads an empty string as "1", so catch it before calling it
    if not units:
        print(f"FAIL {path}: no cf_compliant_units")
        failed += 1
        continue

    result = subprocess.run(
        ["udunits2", "-H", units, "-W", ""],
        capture_output=True, text=True, stdin=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        print(f"FAIL {path}: {units!r} not recognized by UDUNITS")
        failed += 1
    else:
        print(f"ok   {path}: {units!r} = {result.stdout.strip()}")

print(f"\n{failed} of {len(sys.argv) - 1} failed")
sys.exit(1 if failed else 0)
