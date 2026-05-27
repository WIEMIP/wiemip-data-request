# Warming-Induced Emissions Model Intercomparison Project Data Request

Variable request for the Warming-Induced Emissions Model Intercomparison Project (WIEMIP).
WIE variables have been sourced from multiple MIPs: ISIMIP, TRENDY, FireMIP, WrPMIP, and CMIP7. 
The Airtable variable request is [here](https://airtable.com/appA36ibPzVolnROx/shrBXdfrFKttz3YxO).

Please raise an issue with any questions, comments, or suggestions for variable changes. When your model is unable to
report a variable (either because it doesn't align with the definition in the variable request or if it would be too much
work), please report in the README uploaded with your model's results.

## Contents

| Path | Description                                               |
|------|-----------------------------------------------------------|
| `WIEMIP_variable_request_20260527.xlsx` | Spreadsheet pulled from Google sheets on May 27th, 2026   |  
| `variables/` | One subdirectory per category, one JSON file per variable |
| `scripts/sync_airtable.py` | Syncs the variable JSONs to an Airtable base              |

### `variables/` layout

```
variables/
  first_priority/ 
  fire/
  permafrost/
  soil_n2o/
  methane/
  mitigation/
```

Each JSON file is named after the variable (e.g. `variables/first_priority/gpp.json`).

