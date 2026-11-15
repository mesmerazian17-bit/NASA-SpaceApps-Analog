# Data Provenance & Schema Verification — Earth Geospatial Dataset

## 1. Canonical Dataset Registry

| File | Dimensions | Columns | Integrity & Reconciliation Status |
| :--- | :--- | :--- | :--- |
| `seed_locations.csv` | 85 rows × 9 cols | `site_id`, `name`, `region`, `lat`, `lon`, `is_benchmark`, `terrain_type`, `distance_to_road_km`, `is_protected_area` | Canonical base table (`0` missing values; `85` unique `site_id` and `name` entries). |
| `earth_candidates.csv` | 85 rows × 20 cols | All 9 `seed_locations.csv` columns + 11 enriched physical/metadata columns | Canonical enriched table (`0` missing values; base 9 columns match `seed_locations.csv` identically). |

---

## 2. Column Schema, Units & Observed Ranges

### A. Base Site Catalog Columns (`seed_locations.csv` & `earth_candidates.csv`)

| Column | Data Type | Units / Format | Observed Values / Range in CSV | Provenance & Definition in CSV |
| :--- | :--- | :--- | :--- | :--- |
| `site_id` | String | Prefix + 2-digit index | `BM-01`..`BM-05` (5), `SEA-01`..`SEA-20` (20), `GL-01`..`GL-30` (30), `PL-01`..`PL-30` (30) | Primary key across both CSV files. |
| `name` | String | Text | 85 unique site names | Feature/location identifier. |
| `region` | String | Text | Country / administrative region | Geographic jurisdiction string. |
| `lat` | Float | Decimal degrees | `-77.83` to `81.80` (2 decimal places) | Site latitude coordinate. |
| `lon` | Float | Decimal degrees | `-156.77` to `167.15` (2 decimal places) | Site longitude coordinate. |
| `is_benchmark` | Boolean | `True` / `False` | `True` (5 rows: `BM-01`..`BM-05`), `False` (80 rows) | Binary benchmark flag matching the `BM-` prefix. |
| `terrain_type` | String | Categorical snake_case | 72 distinct classes (e.g., `hyperarid_desert`, `caldera_floor`, `polar_desert_valley`) | Geomorphological class label. |
| `distance_to_road_km` | Float | Kilometers (`km`) | `0.1` to `800.0` (mean `55.71`, 1 decimal place) | Site accessibility distance recorded in `seed_locations.csv`. |
| `is_protected_area` | Boolean | `True` / `False` | `True` (51 rows), `False` (34 rows) | Protection status flag recorded in `seed_locations.csv`. |

### B. Enriched Elevation & Terrain Columns (`earth_candidates.csv`)

| Column | Data Type | Units / Format | Observed Values / Range in CSV | Provenance & Calculation Method |
| :--- | :--- | :--- | :--- | :--- |
| `elevation_source` | String | Provider label | `opentopodata-mapzen` (all 85 rows) | Explicit source tag recorded per row in `earth_candidates.csv`. |
| `elevation_m` | Float | Meters (`m`) | `-112.0` to `5006.0` (mean `1060.28`, 1 decimal place) | Elevation value reported by `opentopodata-mapzen` at `(lat, lon)`. |
| `slope_deg` | Float | Degrees (`°`) | `0.0000` to `29.9549` (mean `5.0201`, up to 4 decimal places) | Terrain slope angle in degrees recorded in `earth_candidates.csv`. |
| `roughness_rms_m` | Float | Meters (`m`) | `0.0000` to `96.4066` (mean `13.9479`, up to 4 decimal places) | Unnormalized root-mean-square terrain roughness in meters. |
| `roughness_rms` | Float | Dimensionless (`0–1`) | `0.0000` to `1.0000` (mean `0.1447`, up to 4 decimal places) | Exact dataset-wide min-max normalization verified directly from `roughness_rms_m`: `(roughness_rms_m - 0.0) / (96.4066 - 0.0)`. |

### C. Enriched Climate & Surface Columns (`earth_candidates.csv`)

| Column | Data Type | Units / Format | Observed Values / Range in CSV | Provenance & Calculation Method |
| :--- | :--- | :--- | :--- | :--- |
| `t2m_max_c` | Float | Degrees Celsius (`°C`) | `-8.59` to `48.47` (mean `27.62`, 2 decimal places) | Upper temperature metric recorded in `earth_candidates.csv`. |
| `t2m_min_c` | Float | Degrees Celsius (`°C`) | `-60.44` to `23.39` (mean `-12.24`, 2 decimal places) | Lower temperature metric recorded in `earth_candidates.csv`. |
| `diurnal_temp_swing_k` | Float | Kelvin (`K`) | `8.13` to `89.87` (mean `39.86`, 2 decimal places) | Exact algebraic difference verified across all 85 rows: `t2m_max_c - t2m_min_c`. |
| `albedo` | Float | Dimensionless (`0–1`) | `0.03` to `0.78` (mean `0.27`, 2 decimal places) | Surface albedo recorded in `earth_candidates.csv`. |
| `precip_mm_day` | Float | `mm/day` | `0.01` to `9.50` (mean `2.39`, 2 decimal places) | Daily precipitation rate recorded in `earth_candidates.csv`. |
| `aridity_index` | Float | Dimensionless (`0–1`) | `0.0000` to `0.9983` (mean `0.6314`, up to 4 decimal places) | Exact deterministic transform verified across all 85 rows: `1 - clip(precip_mm_day / 6.0, 0.0, 1.0)`. |

---

## 3. Data Anomalies & Flags Observable in the CSVs

1. **`diurnal_temp_swing_k` Equals `t2m_max_c - t2m_min_c` (Extreme Multi-Tens-of-Kelvin Swings):**
   * Across all 85 rows, `diurnal_temp_swing_k` is strictly equal to `t2m_max_c - t2m_min_c`, producing values exceeding `60 K` in 12 rows and reaching `89.87 K` at `PL-14` (*Batagaika Megaslump*: `t2m_max_c = 31.52°C`, `t2m_min_c = -58.35°C`) and `72.98 K` at `PL-13` (*Pingualuit Crater*: `23.89°C` to `-49.09°C`).
2. **Exact Zero Slope and Zero Roughness on Three Caldera/Crater Sites:**
   * Three rows have both `slope_deg = 0.0` and `roughness_rms_m = 0.0` (`roughness_rms = 0.0`):
     * `SEA-12` (*Toba Caldera (Samosir)*, `2.68, 98.88`, `elevation_m = 900.0`)
     * `GL-19` (*Askja Caldera*, `65.03, -16.75`, `elevation_m = 1052.0`)
     * `PL-13` (*Pingualuit Crater*, `61.28, -73.67`, `elevation_m = 543.0`)
3. **Identical Climate Values Shared Across Nearby Site Pairs/Triplets:**
   * Two groups of distinct sites share identical values across all six climate columns (`t2m_max_c`, `t2m_min_c`, `diurnal_temp_swing_k`, `albedo`, `precip_mm_day`, `aridity_index`):
     * `BM-02` (`75.38, -89.68`) and `PL-07` (`75.38, -89.27`) — both Devon Island, sharing `16.81°C`, `-48.55°C`, `65.36 K`, `albedo = 0.46`, `precip_mm_day = 0.85`, `aridity_index = 0.8583`.
     * `PL-03` (`-77.52, 161.80`), `PL-06` (`-77.33, 162.00`), and `PL-15` (`-77.38, 161.93`) — all McMurdo Dry Valleys, sharing `-3.79°C`, `-52.01°C`, `48.22 K`, `albedo = 0.56`, `precip_mm_day = 0.22`, `aridity_index = 0.9633`.
4. **Saturated `aridity_index = 0.0` Where `precip_mm_day >= 6.0`:**
   * Because `aridity_index` is clipped at `0.0` once `precip_mm_day` reaches `6.0 mm/day`, wet sites with differing precipitation rates collapse to the same floor value of `0.0000` (e.g., `PL-08` at `6.30 mm/day` and `SEA-10` / `SEA-18` / `SEA-19` up to `9.50 mm/day`).
5. **Non-Polar Latitudes Under the `PL-` ID Prefix:**
   * Three sites with a `PL-` prefix have latitudes below `60°`: `PL-08` (*Kazumura Lava Tube, Hawaii, USA*, `lat = 19.49`), `PL-26` (*Tanggula Permafrost, Tibetan Plateau*, `lat = 33.07`), and `PL-28` (*Mutnovsky Volcano, Kamchatka, Russia*, `lat = 52.45`).
6. **Below-Sea-Level Elevations (`elevation_m < 0`):**
   * Five rows contain negative `elevation_m` values: `GL-07` (`-91.0 m`), `GL-29` (`-81.0 m`), `GL-30` (`-25.0 m`), `PL-10` (`-58.0 m`), and `PL-18` (`-112.0 m`).