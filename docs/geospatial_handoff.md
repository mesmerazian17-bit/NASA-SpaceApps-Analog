# Geospatial Handoff

## Status and source of truth

The frontend integration source is [`data/processed/earth_candidates_contract.json`](../data/processed/earth_candidates_contract.json). Do not substitute the raw teammate JSON or the seed CSV for this contract. The companion [`data/processed/earth_candidates_map.geojson`](../data/processed/earth_candidates_map.geojson) is a derived, map-ready export; it does not replace or modify the contract.

This handoff is based on read-only inspection. Neither the Earth extraction pipeline nor the contract builder was run.

## QA summary

- The contract contains **85 records**, **85 unique site IDs**, and **85 unique coordinate pairs**.
- Every record has a finite latitude, longitude, elevation, slope, and raw roughness value. Coordinates are within latitude/longitude ranges.
- Field ranges: latitude `-77.83` to `81.8` degrees; longitude `-156.77` to `167.15` degrees; elevation `-112` to `5006` m; slope `0` to `29.9549` degrees; raw roughness `0` to `96.4066` m.
- The normalized roughness and all other listed feature values are present and finite in all 85 records.
- The separate supplied seed CSV has 85 unique site IDs; its ID set and coordinates match the contract.
- The raw Earth JSON records `opentopodata-mapzen` for all 85 sites. This agrees with the contract's quality notes.

These are structural and value-presence checks, not ground-truth validation.

## Coordinates and map interpretation

The contract stores geographic latitude and longitude as decimal degrees. It does not declare a geodetic datum or EPSG identifier. For the GeoJSON export, coordinates follow the RFC 7946 convention: **WGS 84 longitude, latitude** in that order. A frontend should therefore read a contract point as `[longitude_deg, latitude_deg]` when constructing a GeoJSON position; do not reverse the axes.

Elevation is retained as an `elevation_m` property, not as the optional third coordinate. The contract does not record a vertical datum, so treating elevation as a GeoJSON height would imply a reference that is not documented. The WGS 84 GeoJSON convention is an integration convention, not a verified datum assertion about the original site coordinates.

## Data sources and extraction

### Earth candidates

- Site IDs, names, locations, and terrain classifications originate in the project seed-location list. The supplied seed CSV was checked against the contract for IDs and coordinates only.
- Earth elevation, slope, and roughness are attributed in the contract to the OpenTopoData API's Mapzen elevation dataset. The extraction code calls `https://api.opentopodata.org/v1/mapzen`. The raw records label all 85 elevations as `opentopodata-mapzen`.
- Climate inputs are attributed to NASA POWER climatology, queried by the extraction code at `https://power.larc.nasa.gov/api/temporal/climatology/point`. The script requests `T2M_MAX`, `T2M_MIN`, `T2M_MAX_AVG`, `T2M_MIN_AVG`, `ALLSKY_SRF_ALB`, and `PRECTOTCORR`. It describes POWER as roughly 0.5-degree resolution, so these are regional gridded values rather than site-scale observations.
- The Earth source references recorded in the contract include `https://www.opentopodata.org/`, `https://www.opentopodata.org/datasets/`, and `https://power.larc.nasa.gov/`.
- [`scripts/build_earth_contract_reconciled.py`](../scripts/build_earth_contract_reconciled.py) documents the reconciliation and schema-validation process. It writes a separate candidate output; it was not run for this handoff.

The contract does not record a per-site source raster resolution. Although the public Mapzen dataset documentation describes a nominal global 1-arc-second product, that does not establish the effective input resolution or accuracy at each candidate location. Do not populate the contract's null `spatial_resolution_m` fields with an assumed value.

### Lunar reference

The lunar summary identifies NASA LOLA gridded products for Artemis III Connecting Ridge, Site01, at 5 m/pixel. Its provenance points to `https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/`. The raster grid is 3200 by 3200 pixels. The summary records no measurement date; exact acquisition/product metadata have not been independently verified.

## Terrain methodology

### Earth

The extraction code samples a center point and four cardinal points nominally 500 m north, south, east, and west. It approximates the degree offsets using 111,320 m per degree of latitude and a cosine correction for longitude. The nominal opposite-point separation is about 1 km.

- **Elevation (`location.elevation_m`)** is the center sample returned by the elevation service.
- **Slope (`features.slope_deg`)** is derived from central east-west and north-south elevation differences, divided by a nominal 1,000 m, then converted from gradient magnitude to degrees.
- **Raw roughness (`features.roughness_rms_m`)** is the RMS elevation residual after fitting a plane to the five samples. It is a sparse, roughly 1 km-scale terrain proxy, not fine-scale surface texture.
- **Normalized roughness (`features.roughness_normalized`)** is the raw roughness divided by the active dataset maximum (96.4066 m). It is dimensionless, dataset-dependent, and not a physical roughness measurement.

The contract does not preserve the five raw elevations, per-site retrieval responses, or Earth DEM resolution. The stencil is sensitive to source DEM resolution/interpolation and can miss terrain between its five samples.

### Moon

The lunar slope values are from a 5 m/pixel slope raster. The current ranking uses the lunar raster's mean slope, `12.597745895385742` degrees. Lunar roughness is calculated as the local standard deviation of elevation in a 3 by 3 pixel window (about a 15 m neighborhood), with at least five valid neighbors. The reported roughness summary has 10,239,996 valid pixels.

Earth and lunar slope/roughness are **not directly comparable measurements**. Earth slope uses a sparse approximately 1 km stencil, whereas the lunar values summarize a 5 m raster. Earth roughness is a five-sample plane-fit residual; lunar roughness is a local raster elevation standard deviation. Do not describe the roughness values as method-equivalent or compare them as if they were measured at the same scale.

## Field interpretation

| Contract field | Interpretation |
|---|---|
| Latitude/longitude | Seed-site representative coordinates in decimal degrees. The seed builder describes these points as accurate to roughly 1–3 km; that accuracy has not been independently validated, and no geodetic datum is specified. |
| Elevation | Elevation-service center sample from a DEM product; modeled terrain value, not a surveyed ground measurement. Vertical datum is not recorded. |
| Slope | Derived five-point terrain proxy, in degrees, at approximately 1 km stencil scale. |
| `roughness_rms_m` | Derived five-point plane-fit residual, in metres; scale- and source-dependent proxy. |
| `roughness_normalized` | Dataset-relative transformation of raw roughness; useful only as a dataset-specific ranking aid. |
| `terrain_type` | Categorical site classification, not a numeric measurement. |
| `albedo` | NASA POWER gridded source value; original extraction detail and wavelength/method are not specified in the contract. Treat as a regional estimate. |
| `precip_mm_day` | NASA POWER gridded climatology value; regional estimate, not a site-gauge observation. |
| `mean_daily_temp_range_k` | Derived day-weighted mean of monthly average daily maximum-minus-minimum temperatures, as documented by the builder. |
| `precipitation_dryness_proxy` | Precipitation-only derived proxy: `1 - clip(precip_mm_day / 6, 0, 1)`. It is **not** the UNEP P/PET aridity index and does not include potential evapotranspiration. |

## Top lunar slope matches

The ranking output reports 85 sites scored and zero excluded, using only the absolute difference between each Earth site's slope and the lunar mean slope. The following top-three IDs and coordinates were cross-checked against the authoritative Earth contract:

| Rank | Site ID | Site | Contract coordinates (latitude, longitude) | Slope difference |
|---:|---|---|---|---:|
| 1 | GL-06 | Pinacate Volcanic Field | `31.77, -113.5` | `0.238154` degrees |
| 2 | SEA-11 | Mount Sinabung | `3.17, 98.39` | `0.546954` degrees |
| 3 | GL-01 | Pamir Plateau (Murghab) | `38.17, 73.96` | `0.820046` degrees |

These are **slope-only approximate matches**, not overall analog scores. They do not establish matched roughness, access, logistics, solar illumination, or failure-mode complementarity.

## Provenance and uncertainty gaps

- Earth retrieval dates, raw API responses, per-site retrieval parameters/dataset versions, effective raster resolutions, and elevation vertical datum are not recorded. The contract does carry general source references.
- Contract feature metadata lists uncertainty as unavailable (`null`); this means unknown, not zero uncertainty.
- The coordinate datum is not specified. The seed builder's approximate 1–3 km representative-point accuracy is not an independent positional validation.
- NASA POWER climate fields are regional at the extractor's documented approximate grid scale. Their exact climatology period is not recorded in the contract.
- Lunar measurement date is null, and exact product acquisition metadata are not independently verified. The 5 m pixel size is raster spacing, not a claim of 5 m measurement accuracy.
- Road-distance and protected-area estimates from the seed data are not included as validated measurements in this contract. No access or logistics validation is implied.
- No claim is made for 95% risk coverage.

## Frontend handoff

The **85-site dataset is ready for frontend consumption** from the processed contract: required coordinates and terrain fields are present and finite, and the GeoJSON export uses standard longitude/latitude coordinate order. Preserve the field units and method notes, label Earth–Moon comparisons as scale-dependent, and present unavailable provenance/uncertainty as unavailable rather than filling it with defaults.
