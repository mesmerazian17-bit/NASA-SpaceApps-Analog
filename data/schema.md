
# Planetary Analog Campaign Architect
## Shared Data Schema — Version 1.0

### 1. Purpose

This schema defines the shared data contract between the geospatial,
scientific validation, backend scoring, and frontend teams.

All measurements must have:
- A defined unit.
- A known spatial scale or resolution where relevant.
- A source or provenance record.
- A quality or confidence indicator.
- A clear distinction between measured, derived, estimated,
  and unavailable values.

Missing values must be null, never silently replaced with zero.

---

### 2. Planetary Target Schema

Each planetary target must contain:

| Field | Type | Description |
|---|---|---|
| target_id | string | Unique target identifier |
| name | string | Target name |
| planet | string | Moon or Mars |
| lat | float | Target reference latitude |
| lon | float | Target reference longitude |
| gravity_m_s2 | float | Local planetary gravity |
| terrain_type | string | Geological classification |
| features | object | Environmental measurements |
| tolerances | object | Feature comparison tolerances |
| required_failure_modes | array | Required engineering stress tests |
| sources | array | Scientific references |

### 3. Universal Environmental Features

| Feature | Unit | Description |
|---|---|---|
| slope_deg | degrees | Surface inclination |
| roughness_rms | meters | RMS elevation deviation |
| albedo | dimensionless | Surface reflectivity |
| mean_daily_temp_range_k | Kelvin | Day-weighted climatological mean of monthly average daily maximum-minus-minimum temperature ranges (12 months) |
| aridity_index | dimensionless | Terrestrial aridity indicator |

Important:
- Roughness must specify the spatial resolution and calculation method.
- Albedo must specify wavelength range and measurement method.
- Temperature swing must specify observation period and local time.
- Aridity index is primarily a terrestrial climate indicator.
  Do not treat it as directly comparable to a Martian or lunar
  environmental measurement.
- A null value means unavailable, not zero.

### 4. Earth Candidate Schema

Each Earth candidate must contain:

| Field | Type | Description |
|---|---|---|
| site_id | string | Unique site identifier |
| name | string | Site name |
| region | string | Country or region |
| lat | float | Latitude |
| lon | float | Longitude |
| is_benchmark | boolean | Established analog site |
| terrain_type | string | Volcanic, karst, desert, etc. |
| distance_to_road_km | float | Road accessibility |
| is_protected_area | boolean/null | Protected status |
| failure_modes | array | Supported engineering stress tests |
| features | object | Environmental measurements |
| provenance | object | Data source information |

### 5. Failure Mode Taxonomy

Initial supported tags:

- electrostatic_dust
- fine_dust
- regolith_slip
- thermal_extremes
- gps_denied_navigation
- subsurface_exploration
- steep_slope_traversal
- low_visibility_navigation
- loose_material_mobility
- illumination_shadow_navigation

A failure mode must have a scientific or engineering justification.
Do not assign a tag based on visual resemblance alone.

### 6. Measurement Provenance

Every measured or derived feature should record:

- source_name
- source_url
- instrument_or_dataset
- measurement_date
- spatial_resolution_m
- method
- value_type: measured, derived, estimated, or simulated
- uncertainty
- quality_flag

### 7. Scoring Contract

The backend must return:

- normalized_distance
- similarity_score
- data_completeness
- failure_mode_coverage
- matched_failure_modes
- missing_failure_modes
- overall_score

Similarity and failure-mode coverage must remain separately
visible in the frontend.

### 8. Composite Campaign Contract

The two-site optimizer must return:

- selected_site_ids
- combined_failure_mode_coverage
- covered_failure_modes
- uncovered_failure_modes
- average_similarity
- logistics_constraints
- selection_explanation

### 9. Physics Scaling Rules

Earth, Moon, and Mars are different physical environments.

The system must explicitly account for:

- Gravity differences
- Atmospheric pressure and composition
- Thermal environment
- Solar illumination
- Dust properties
- Material behavior

Terrestrial analogs reproduce selected geological or operational
conditions, not the complete planetary environment.

### 10. Data Quality Rules

1. Never fabricate missing measurements.
2. Preserve original measurement units.
3. Record source URLs.
4. Identify estimated and simulated values.
5. Never compare incompatible measurement resolutions without
   accounting for their differences.
6. Protected-area status must be independently verified.
7. A candidate's failure-mode tags require documented justification.
8. All scoring results must be reproducible.

### 11. Output Files

data/
- earth_candidates.csv
- planetary_targets.json
- schema.md

frontend/public/data/
- scored_results.json
- mission_briefs.json

