# Warming-Induced Emissions Model Intercomparison Project Variable Request

Variable request for the Warming-Induced Emissions Model Intercomparison Project (WIEMIP).
WIE variables have been sourced from multiple MIPs: ISIMIP, TRENDY, FireMIP, WrPMIP, and CMIP7. 
The Airtable variable request is [here](https://airtable.com/appA36ibPzVolnROx/shrBXdfrFKttz3YxO) and is constructed by 
parsing the .json files in `variables/`. The `WIEMIP_variable_request_20260527.xlsx` was pulled directly from the Google
Sheet previously used to manage the WIEMIP variable request. 

# WIEMIP Variable Request details
WIEMIP will accept results that use either TRENDY or CMIP7 compound name to reduce programming load on modeling groups.
See fields `Variable name` and `CMIP7 Compound Name` in the [Airtable](https://airtable.com/appA36ibPzVolnROx/shrBXdfrFKttz3YxO).
If a variable is present that does not have a `CMIP7 Branded Variable Name`, then it does not exist in CMIP7 and 
a `CMIP7 Compound Name` has been created specifically for WIEMIP. See, for example, the variable 
`Vegtype level Carbon in Vegetation`.

First priority variables are in the first tab of the Airtable spreadsheet and the corresponding child directory in
`variables/`. 

When your model is unable to report a variable (either because it doesn't align with the definition in the variable
request or if it would be too much work), please report in the README uploaded with your model's results.


# Questions? Raise an issue.
Please raise an issue with any questions, comments, or suggestions for variable changes. 


# WIEMIP naming convention

```
<MODEL_NAME>_<gcm_pattern_short_name>_<experiment_short_name>_<variable_name>_<frequency>_<spatial_resolution_short_name>.nc
```

If you're using the CMIP7 compound name (instead of the TRENDY variable name) the naming convention is:

```
<MODEL_NAME>_<gcm_pattern_short_name>_<experiment_short_name>_<CMIP7_compound_name>_<spatial_resolution_short_name>.nc
```

The tables below contain the short names to use for GCM pattern, frequencies, and spatial resolutions.

### GCM pattern names

| Long name | Short name |
|-----------|------------|
| UKESM1-0-LL | `ukesm` |
| GFDL-ESM4 | `gfdl` |
| IPSL-CM6A-LR | `ipsl` |

See Table 2 for the experiment short names. The frequency field follows CMIP conventions:

### Frequencies

| Frequency | Short name |
|-----------|------------|
| Year | `yr` |
| Month | `mon` |
| Day | `day` |
| 6-hourly | `6hr` |
| Fixed | `fx` |

### Spatial resolutions

| Resolution                    | Short name |
|-------------------------------|------------|
| 0.5°                          | `05`       |
| 1°                            | `1`        |
| custom resolution (e.g., T63) | per-model  |

Please add a note in the README if you're using a non 0.5° or 1° grid.

### Factorial simulations

Factorial simulations for the 1pctCO2 simulations will exclude certain processes. To indicate the exclusion of a process from your model, use the following naming convention:

```
<MODEL_NAME>_<gcm_pattern_short_name>_<experiment_short_name>_<variable_name>_<frequency>_noProcess_<spatial_resolution_short_name>.nc
```
Note: For organizational purposes modeling groups can upload simulation results under subdirectories, where the subdirectories are named:
```
<MODEL_NAME>_<gcm_pattern_short_name>_<experiment_short_name>/
```

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

