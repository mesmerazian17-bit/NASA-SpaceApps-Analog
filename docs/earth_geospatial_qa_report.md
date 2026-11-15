# Earth Geospatial QA Report and Integration Handoff

**QA date:** 2026-11-15  
**Historical Earth extraction date:** Unavailable; the QA date is not the extraction date.
**Raw QA source:** `data/raw/teammates/earth_candidates.json`  
**Scope:** Read-only validation of the 85 raw Earth records, targeted elevation cross-checks, extraction-method review, provider/provenance audit, and comparison with the processed lunar summary.  
**Data changes:** None. No candidate values were replaced; no extraction was rerun.

> **Current integration status:** This report documents QA of the raw source JSON. The frontend authority is now [`data/processed/earth_candidates_contract.json`](../data/processed/earth_candidates_contract.json); the contract QA, coordinate interpretation, limitations, and top lunar slope matches are documented in the [geospatial handoff](geospatial_handoff.md). Do not use the raw JSON in place of the contract.

## Executive summary

- The raw JSON audited here contains 85 sites. All 85 have finite elevation, slope, raw roughness, and normalized roughness values; there are no duplicate coordinates or negative slope/roughness values.
- The recorded provider labels are **85 `opentopodata-mapzen`, 0 `open-elevation`** in the raw JSON. Of the 85 sites, 55 fall within the extraction script's stated SRTM latitude band and 30 fall outside it. The data alone cannot establish whether the in-band Mapzen values came from automatic fallback after Open-Elevation failures or an explicit `--elevation-provider opentopodata` run; the extraction logs and run arguments are unavailable.
- Seven points were checked against Open-Meteo's global Copernicus DEM GLO-90 endpoint. Absolute differences from the stored candidate elevations were 2–32 m (median 4 m). This is an independent DEM-product cross-check, not ground-truth validation or a replacement for survey control.
- The three records with zero slope and roughness were queried again at their center and four cardinal offsets from the Mapzen endpoint. For each, all five returned elevations were identical, reproducing the stored zero metrics. This confirms the API-sample result on the QA date, but not that the physical terrain is truly flat.
- Earth and lunar slope/roughness are not interchangeable measurements: Earth uses five samples at nominal 500 m offsets; the lunar raster is 5 m/pixel and roughness is a 3 x 3-pixel local elevation standard deviation.
- **Integration recommendation:** retain the input values but mark Earth terrain metrics as scale-dependent derived proxies, display the provider split and missing historical run provenance, and do not compare Earth and lunar roughness/slope numerically as if produced by the same method.

## 1. Files, authority, and provenance status

The raw validation source for this review is [earth_candidates.json](../data/raw/teammates/earth_candidates.json). It contains 85 rows. Its values were inspected directly; the processed Earth contract is the current frontend authority.

The seed CSV was supplied separately from the repository. Its 85 site IDs and coordinates were cross-checked against the processed contract and match. The extraction staging CSV is a separate input and was not independently reconciled in this handoff.

The contract builder, [build_earth_contract_reconciled.py](../scripts/build_earth_contract_reconciled.py), depends on the staging CSV at the literal path `/tmp/earth_candidates_staging.csv`. That CSV is not included in the repository. A fresh clone cannot reproduce the build without supplying the required file at the path configured in the script; no alternate input path is documented.

The following implementation and data notes were reviewed:

- [fetch_nasa_earth_data.py](../data/raw/teammates/fetch_nasa_earth_data.py) defines the Earth extraction endpoints, provider-selection logic, offsets, terrain equations, retries, and CSV output behavior.
- [schema.md](../data/schema.md) requires units, scale/method, provenance, uncertainty/quality information, and null rather than zero for missing values.
- [lunar_features.json](../data/processed/lunar_features.json) contains the processed 5 m/pixel lunar statistics and explicitly leaves the source URL and measurement date undocumented.

The Earth candidate JSON has provider labels and values but no per-site source URL, extraction timestamp, raw five-point elevations, uncertainty, quality flag, or run identifier. The source code contains API endpoint URLs, but it does not persist the retrieval date or response payloads in the output.

## 2. Independent elevation cross-check

### Method and source

On 2026-11-15, the seven listed coordinates were queried together using the [Open-Meteo Elevation API](https://open-meteo.com/en/docs/elevation-api). Its documentation identifies the elevation product as the global Copernicus DEM 2021 release GLO-90 at 90 m resolution; the underlying product citation is [Copernicus DEM DOI 10.5270/ESA-c5d3d65](https://doi.org/10.5270/ESA-c5d3d65). The [batch request](https://api.open-meteo.com/v1/elevation?latitude=19.82,34.56,-20.13,35.03,36.23,33.07,-24.10&longitude=-155.47,-115.78,-67.49,-111.02,-116.77,91.93,-70.00) returned, in order, 4169, 203, 3654, 1627, -85, 5008, and 1007 m.

Absolute difference is `abs(independent elevation - stored elevation)`. The displayed percentage is `absolute difference / abs(stored elevation) * 100`, rounded to four decimal places. Elevation is referenced to a vertical datum, not a ratio-scale quantity; the percentages are diagnostic only. This is particularly important for the below-sea-level Badwater value, for which a percentage is not a physically meaningful accuracy measure.

| Site ID | Site | Coordinates (lat, lon) | Stored elevation (m) | Copernicus GLO-90 (m) | Absolute difference (m) | Difference (%) |
|---|---|---:|---:|---:|---:|---:|
| BM-03 | Mauna Kea Summit | 19.82, -155.47 | 4141 | 4169 | 28 | 0.6762 |
| BM-05 | Mojave Desert (Amboy Crater) | 34.56, -115.78 | 206 | 203 | 3 | 1.4563 |
| GL-08 | Salar de Uyuni | -20.13, -67.49 | 3658 | 3654 | 4 | 0.1093 |
| GL-12 | Barringer (Meteor) Crater | 35.03, -111.02 | 1595 | 1627 | 32 | 2.0063 |
| GL-29 | Badwater Basin, Death Valley | 36.23, -116.77 | -81 | -85 | 4 | 4.9383* |
| PL-26 | Tanggula Permafrost, Tibetan Plateau | 33.07, 91.93 | 5006 | 5008 | 2 | 0.0400 |
| BM-01 | Atacama Desert (Yungay) | -24.10, -70.00 | 1011 | 1007 | 4 | 0.3956 |

`*` Arithmetic result only; not meaningful as a ratio to a sea-level-referenced elevation.

**Interpretation and limitations:** These values are close in this small sample, but seven point comparisons do not establish accuracy for all 85 sites. Copernicus GLO-90 is a 90 m DEM, so it smooths or misses smaller terrain features. The candidate locations are representative points, documented by the seed builder as approximately 1–3 km accurate, which can exceed the nominal 500 m sample offset. Vertical-datum compatibility is not recorded in the Earth JSON. Mapzen is itself a global mosaic of open DEM sources; shared source inputs between DEM products have not been ruled out. Do not silently substitute these cross-check values for the active measurements.

## 3. Slope and roughness QA across all 85 sites

| Check | Result |
|---|---|
| Row count | 85 |
| Missing, non-numeric, or non-finite elevation / slope / raw roughness / normalized roughness | 0 for each field |
| Duplicate `(lat, lon)` pairs | 0 |
| Negative slope, raw roughness, or normalized roughness | 0 |
| Slope range | 0 to 29.9549 degrees |
| Raw roughness range | 0 to 96.4066 m |
| Normalized roughness range | 0 to 1 |
| Negative elevations | 5; these are below-sea-level values, not negative terrain metrics |

The normalized roughness values exactly match the rounded four-decimal dataset min-max transform `(roughness_rms_m - 0) / (96.4066 - 0)` for all 85 rows. It is dimensionless and depends on this particular dataset's minimum and maximum; it is not an absolute physical roughness measure and will change if the dataset is extended or recalculated.

### Outlier screening

For review only, Tukey 1.5-IQR screening flags the following high values. Quartiles are the medians of the lower and upper halves after excluding the overall median. An IQR flag is not an error determination; the named volcanic and rugged sites are plausible candidates for high relief, and the five-point metric cannot characterize their detailed landforms.

- **Slope:** SEA-16 Mayon Volcano (29.9549 degrees), SEA-20 Batur Caldera (18.3963 degrees), PL-25 Beerenberg (17.1854 degrees).
- **Raw roughness:** SEA-11 Mount Sinabung (96.4066 m), SEA-05 Mount Rinjani Caldera (93.7531 m), SEA-18 Son Doong Cave (89.4748 m), SEA-13 Kelud Crater (84.5074 m), PL-01 Bockfjorden Volcanic Complex (53.6749 m), SEA-20 Batur Caldera (46.8615 m).

The same six sites are high outliers in normalized roughness because that field is a linear transform of raw roughness. The 0–30 degree slope and 0–96 m roughness ranges are not intrinsically impossible for the stated terrain proxy. No physical upper-limit specification exists in the schema, so an automatic rejection threshold would be unjustified.

### Three zero-slope / zero-roughness records

The source API was queried again on 2026-11-15 for each center and the same four cardinal positions calculated by the extraction code. OpenTopoData identified the returned dataset as `mapzen`; all five values were equal for each site:

| Site ID | Site | Five returned elevations (m) | Stored slope | Stored roughness |
|---|---|---:|---:|---:|
| SEA-12 | Toba Caldera (Samosir) | 900, 900, 900, 900, 900 | 0 degrees | 0 m |
| GL-19 | Askja Caldera | 1052, 1052, 1052, 1052, 1052 | 0 degrees | 0 m |
| PL-13 | Pingualuit Crater | 543, 543, 543, 543, 543 | 0 degrees | 0 m |

This reproduces zero slope and zero plane-residual roughness from the returned Mapzen samples. It does **not** prove the ground is perfectly flat: source raster resolution, source-data interpolation, integer output, and DEM smoothing can suppress local variation. The point response is a current re-query and not a preserved response from the historical extraction.

### Five-point method and offset math

The reviewed code samples center, north, south, east, and west. It computes:

- `dlat = 500 / 111320` degrees;
- `dlon = 500 / (111320 * cos(latitude))` degrees, with a small lower bound on cosine;
- `dz/dx = (east - west) / 1000 m`, `dz/dy = (north - south) / 1000 m`;
- `slope = degrees(atan(sqrt((dz/dx)^2 + (dz/dy)^2)))`;
- raw roughness as the RMS residual of a least-squares plane fitted to the five elevations and nominal local x/y positions.

The trigonometric cosine correction is appropriate for approximating east-west distance on a sphere. It is not a geodesic calculation on the WGS84 ellipsoid: using the WGS84 local curvature radii, the script's nominal 500 m cardinal offsets are approximately 496.66–501.65 m across these sites (up to about 3.34 m difference). This small approximation is consistent with the stated approximate scale; the slope denominator still uses exactly 1000 m.

The method measures a broad, sparse 500 m-scale gradient and plane departure, not fine-scale slope or surface texture. It is sensitive to DEM resolution, vertical rounding, interpolation, coordinate error, and whether cardinal points cross a ridge, crater wall, drainage, or material boundary. Five points cannot detect terrain variation between samples or describe directionally complex terrain robustly. `roughness_rms_m` is a five-sample plane-fit residual and is not the same statistic as local raster elevation standard deviation.

## 4. Provider and provenance audit

### Verified counts and selection logic

| Audit item | Result |
|---|---:|
| Stored Open-Elevation labels | 0 |
| Stored OpenTopoData Mapzen labels | 85 |
| Sites inside script's stated SRTM latitude band `[-56, 60]` | 55 |
| Sites outside that latitude band | 30 |

The 55/30 row is a latitude-eligibility count, not the observed provider split. In the script's default `auto` mode, in-band sites first try Open-Elevation; exceptions are logged and can fall back to Mapzen. Out-of-band sites go directly to Mapzen. An explicit `--elevation-provider opentopodata` also skips Open-Elevation. Thus the raw file's **85/0 Mapzen/Open-Elevation labels are verified**, but the cause of the 55 in-band Mapzen labels is unresolved without command-line arguments and extraction logs.

### Sources, limits, and missing provenance

- The code uses OpenTopoData's `https://api.opentopodata.org/v1/mapzen` endpoint. Its [Mapzen dataset documentation](https://www.opentopodata.org/datasets/mapzen/) describes a global 1-arc-second product (about 30 m at the equator), with some areas interpolated from lower-resolution sources; the public service documents its Mapzen data as version 1.1 downloaded in May 2020. The [API documentation](https://www.opentopodata.org/api/) says the default interpolation is bilinear and that integer raster outputs are rounded to the nearest integer. This is consistent with the integer elevations in the file but does not independently prove how the original run was executed.
- The 1-arc-second figure is the nominal Mapzen product resolution, not a verified effective resolution for each site. Effective per-site resolution is unknown and has not been independently verified; the raw records and contract do not identify it.
- The code's Open-Elevation endpoint is `https://api.open-elevation.com/api/v1/lookup`. Its current [service documentation](https://open-elevation.com/) describes SRTM-derived options and usage limits; the extraction code does not pin a dataset selector or save a response's dataset identifier. The historical resolution and service state at extraction time are therefore unknown. Current service limits should not be used to infer historical behavior.
- Climate fields are requested from the [NASA POWER climatology point API](https://power.larc.nasa.gov/api/temporal/climatology/point) for `T2M_MAX`, `T2M_MIN`, `ALLSKY_SRF_ALB`, and `PRECTOTCORR`. The extraction script notes POWER's roughly 0.5-degree spatial scale; these are regional climate estimates, not site-scale terrain measurements.
- The JSON records do not include extraction date, individual source URL, source dataset/version, raw five-point elevations, vertical datum, uncertainty, quality flag, or request/error log. The code's retry and logging behavior is not a substitute for a persisted run manifest.

The raw-source provider count is **85 Mapzen / 0 Open-Elevation recorded**, with the route ambiguity stated. Do not label it "55 Open-Elevation / 30 Mapzen" based only on the latitude rule.

## 5. Earth–Moon comparability

The processed lunar file identifies 5 m/pixel rasters. Its `slope_deg` summary is the mean of a raster slope product (12.5977 degrees); `roughness_rms` is the mean local elevation standard deviation over a 3 x 3 pixel window at 5 m/pixel (approximately a 15 m neighborhood), in metres (0.9262 m). Its provenance identifies NASA LOLA but has no source URL or measurement date.

Earth slope is derived from cardinal elevation differences spanning approximately 1 km between opposite samples. Earth roughness is a plane-fit residual at the five 500 m-offset samples. These measurements differ in:

1. **Spatial scale:** approximately 500 m Earth offset radius versus 5 m lunar pixel spacing and a roughly 15 m lunar roughness window.
2. **Estimator:** finite differences and five-point plane residual versus a raster slope product and local standard deviation.
3. **Input grid/source:** Mapzen/other Earth DEM mosaics versus the lunar LOLA-derived raster products.
4. **Coverage and aggregation:** one sparse Earth site stencil versus summary statistics across millions of lunar pixels.

Equal units do not establish equal measurement meaning. Do not use the dataset-normalized Earth `roughness_rms` (0–1) against lunar roughness in metres. If a quantitative comparison is required, derive both products from elevation data using a declared common spatial support, projection, resolution, slope algorithm, roughness statistic, NoData policy, and aggregation (for example, calculate both over matched 500 m windows from suitable DEMs). Otherwise present the values separately with their scale/method labels and treat them as qualitative context only. A 5 m lunar grid alone does not guarantee 5 m independent measurement accuracy.

## 6. Reproducibility

Run from the project root in PowerShell. These commands read the raw JSON and query only the listed APIs; they do not write candidate data.

```powershell
@'
import json, collections, math
d = json.load(open(r'data\raw\teammates\earth_candidates.json', encoding='utf-8'))
print('rows', len(d))
print('providers', collections.Counter(r.get('elevation_source') for r in d))
print('finite', {
    k: sum(
        isinstance(r.get(k), (int, float)) and math.isfinite(r[k])
        for r in d
    )
    for k in ('elevation_m', 'slope_deg', 'roughness_rms_m', 'roughness_rms')
})
print('duplicate_coordinates', len(d) - len({(r['lat'], r['lon']) for r in d}))
'@ | python -
```

Independent DEM cross-check used:

```powershell
$uri = 'https://api.open-meteo.com/v1/elevation?latitude=19.82,34.56,-20.13,35.03,36.23,33.07,-24.10&longitude=-155.47,-115.78,-67.49,-111.02,-116.77,91.93,-70.00'
(Invoke-RestMethod -Uri $uri).elevation
```

The three zero-site sample re-query used the Mapzen endpoint with the 15 center/cardinal coordinates and six-decimal rounding used by the extraction script:

```powershell
$uri = 'https://api.opentopodata.org/v1/mapzen?locations=2.680000,98.880000%7C2.684492,98.880000%7C2.675508,98.880000%7C2.680000,98.884496%7C2.680000,98.875504%7C65.030000,-16.750000%7C65.034492,-16.750000%7C65.025508,-16.750000%7C65.030000,-16.739360%7C65.030000,-16.760640%7C61.280000,-73.670000%7C61.284492,-73.670000%7C61.275508,-73.670000%7C61.280000,-73.660653%7C61.280000,-73.679347'
(Invoke-RestMethod -Uri $uri).results | Select-Object dataset,elevation,location
```

Do **not** run `fetch_nasa_earth_data.py` as a QA step: its default behavior makes external requests and writes `data/earth_candidates.csv`.

## 7. Unresolved issues and integration handoff

1. **Historical run evidence:** obtain extraction date, command-line options, logs, and raw elevation responses to establish why the 55 in-band sites are tagged Mapzen.
2. **Source version and vertical datum:** persist provider dataset/version, request URL/parameters, dataset-reported resolution, and vertical datum for every site. Confirm datum compatibility before interpreting DEM differences as error.
3. **Zero terrain metrics:** the current Mapzen service reproduces each zero from five identical integer samples, but a finer local DEM or survey source is needed to determine whether flatness is real or an artifact of source resolution/coverage.
4. **Scale and uncertainty:** include method, nominal offset/window, source resolution, uncertainty or a clear unavailable flag, and quality flag for slope and roughness in the integration data contract.
5. **Normalization:** keep raw roughness in metres for physical comparisons; expose the current dataset-wide normalized value only as a ranking aid and document that it is version-dependent.
6. **Lunar provenance:** add the NASA/LOLA product URL, product/version, measurement or processing date, slope algorithm, and source uncertainty/quality interpretation to the lunar handoff.
7. **Site metadata:** coordinate accuracy, road distance, and protected-area status are not validated by this terrain QA; the seed builder describes the coordinates as approximate and access/protection values as estimates.

**Integration recommendation:** use the processed Earth contract as the frontend input. Preserve the raw-source QA evidence and annotate the verified provider distribution as 85/0 Mapzen/Open-Elevation, with the route ambiguity stated. Present the seven independent DEM checks as cross-validation evidence with their stated limitations, not as ground-truth certification. Keep Earth and lunar slope/roughness comparisons scale-aware and non-equivalent until a matched-scale analysis is performed.
