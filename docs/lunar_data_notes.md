
# Lunar Baseline: Connecting Ridge

## Dataset Source
NASA GSFC - Planetary Geodesy and Geophysics Data Archive
Instrument: Lunar Orbiter Laser Altimeter (LOLA)
Target: Artemis III Connecting Ridge
Site: Site01
Resolution: 5 metres per pixel

## Downloaded Datasets

| Dataset | Filename | Purpose |
|---|---|---|
| Elevation | surf.tif | Surface elevation |
| Slope | slp.tif | Terrain inclination |
| Slope uncertainty | slperr.tif | Slope measurement uncertainty |
| Elevation uncertainty | toterr.tif | Elevation measurement uncertainty |
| Observation count | ldec.tif | Data coverage quality |

## Observed Raster Metadata

Dimensions: 3200 x 3200
Data type: float32
Pixel resolution: 5 x 5 metres
NoData: NaN

Projection: Polar Stereographic
Reported CRS identifier: EPSG:9122

## Elevation Raster

Recorded metadata range:
- Minimum: -523.183
- Maximum: 1959.496

## Slope Raster

Recorded metadata range:
- Minimum: 0
- Maximum: 64.5882

## Processing Plan

1. Verify all raster metadata.
2. Check valid pixel coverage.
3. Calculate elevation statistics.
4. Calculate slope statistics.
5. Calculate local terrain roughness.
6. Evaluate measurement uncertainty.
7. Export processed measurements to JSON.

## Scientific Precautions

- Preserve original NASA datasets.
- Exclude NoData pixels from calculations.
- Verify units before interpreting measurements.
- Document roughness window size.
- Preserve source resolution and provenance.
- Do not treat metadata ranges as statistical summaries.

