# Planetary Analog Campaign Architect

**An exploratory decision-support prototype for identifying terrestrial analog sites for lunar and planetary exploration campaigns.**

## Overview

Planetary Analog Campaign Architect evaluates terrestrial locations as potential analog environments for planetary exploration. It combines Earth environmental datasets with lunar terrain measurements to identify candidate sites and explore two-site campaign configurations.

The current prototype focuses on the lunar south-polar region, using NASA Lunar Orbiter Laser Altimeter (LOLA) terrain products for the Artemis III Connecting Ridge target.

The system currently provides:
- A structured dataset of 85 terrestrial candidate sites.
- Lunar terrain feature extraction and provenance documentation.
- Slope-based Earth-to-lunar candidate ranking.
- Evidence classification for selected mission failure modes.
- Exploratory two-site campaign shortlisting based on slope similarity and terrain-class diversity.

This is a research prototype. Its rankings are preliminary and should not be interpreted as validated mission-site recommendations or quantified mission-risk coverage.

## Current Results

| Metric | Current result |
|---|---:|
| Earth candidate sites | 85 |
| Earth sites ranked against lunar slope | 85 |
| Different-terrain site pairs evaluated | 3,565 |
| Two-site campaign candidates retained | 20 |
| Automated tests | 4 passed |
| Automated test subtests | 85 passed |

### Leading single-site slope matches

1. Pinacate Volcanic Field, Mexico — GL-06; slope difference: 0.2382°
2. Mount Sinabung, Indonesia — SEA-11; slope difference: 0.5470°
3. Pamir Plateau (Murghab) — GL-01; slope difference: 0.8200°

### Leading two-site candidate

- Pinacate Volcanic Field, Mexico — GL-06
- Mount Sinabung, Indonesia — SEA-11
- Mean slope difference from the lunar target: 0.3926°

These are exploratory slope-similarity results, not overall analog-suitability scores. The two-site system currently uses different terrain labels as a diversity heuristic. Complementary failure-mode coverage has not been established, and no validated risk-coverage percentage is claimed.

### Evidence limitations

- Earth slope sampling uses an approximately 1 km five-point stencil, while the lunar terrain raster has 5 m spatial resolution.
- Earth and lunar roughness are calculated using different methods and are not directly comparable.
- Temperature, albedo, and precipitation do not have equivalent lunar measurements in this prototype.
- Jezero Crater and Arsia Mons are not numerically scoreable with the currently populated target features.

## Project Structure

```text
.
├── data/
│   ├── contracts/
│   │   ├── earth_moon_feature_schema.json
│   │   └── earth_moon_feature_example.json
│   ├── processed/
│   │   ├── earth_candidates_contract.json
│   │   ├── lunar_features.json
│   │   ├── lunar_slope_rankings.json
│   │   ├── failure_mode_evidence_audit.json
│   │   └── two_site_campaign_candidates.json
│   └── ...
├── docs/
│   └── lunar_data_notes.md
├── scripts/
│   ├── score_lunar_analogs.py
│   ├── audit_failure_mode_evidence.py
│   └── build_two_site_campaign.py
├── tests/
├── frontend/
├── requirements.txt
└── README.md
```

## Setup

Python 3.12 is recommended.

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install project dependencies:

```bash
python -m pip install -r requirements.txt
```

Install the test runner:

```bash
python -m pip install pytest
```

## Reproducing the Current Analysis

Run the following commands from the repository root.

### 1. Rank Earth sites by lunar slope similarity

```bash
python scripts/score_lunar_analogs.py
```

Output:

```text
data/processed/lunar_slope_rankings.json
```

The current ranking compares the mean Earth site slope with the mean lunar target slope using absolute difference in degrees.

### 2. Audit failure-mode evidence

```bash
python scripts/audit_failure_mode_evidence.py
```

Output:

```text
data/processed/failure_mode_evidence_audit.json
```

Evidence is classified as:
- `quantitative_proxy`
- `contextual_only`
- `unavailable`

These classifications describe available evidence, not demonstrated failure-mode equivalence.

### 3. Generate two-site campaign candidates

```bash
python scripts/build_two_site_campaign.py
```

Output:

```text
data/processed/two_site_campaign_candidates.json
```

The current shortlist requires different terrain labels and ranks pairs by mean slope difference, with the worst individual slope difference used as a tie-breaker.

### 4. Run automated tests

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
```

The environment variable prevents unrelated system-installed pytest plugins from being loaded.

## Data Sources

### Lunar terrain

The lunar terrain analysis uses NASA Lunar Orbiter Laser Altimeter (LOLA) 5-meter-per-pixel south-polar terrain products.

- NASA LOLA 5m/pixel products: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/
- NASA Planetary Geology Data products: https://pgda.gsfc.nasa.gov/products/78

The lunar feature dataset includes elevation, slope, local roughness, and associated uncertainty information where available.

See `docs/lunar_data_notes.md` for additional processing and interpretation notes.

### Earth environmental data

Earth candidate records are derived from the project's Earth geospatial data workflow, including terrain elevation measurements and NASA POWER environmental data.

See `data/SOURCES.md` and the data provenance metadata for source details and processing context.

## Methodology and Scientific Limitations

The prototype intentionally separates numerical comparisons from contextual evidence.

### Slope

Earth and lunar slopes are compared in degrees. However, the Earth terrain sampling method and spatial scale differ from the lunar 5-meter raster. The resulting ranking is therefore approximate.

### Roughness

Earth roughness is calculated using a five-point plane-fit residual over an approximately 1-kilometer baseline. Lunar roughness is calculated as local elevation standard deviation over a 3×3 neighborhood at 5-meter resolution.

These measurements are not directly comparable and are excluded from the current numerical ranking.

### Temperature and albedo

Earth daily temperature range and albedo are retained as environmental information. Equivalent lunar measurements suitable for the current comparison are not available in the prototype.

### Precipitation and dryness

The Earth precipitation-derived dryness value is a precipitation-only proxy. It is not the standard UNEP aridity index and should not be interpreted as a direct lunar environmental equivalent.

### Failure-mode evidence

Terrain classification and Earth temperature measurements can provide contextual information, but they do not establish equivalent lunar dust behavior, thermal conditions, or illumination and shadow-navigation hazards.

### Two-site campaigns

Different terrain labels do not prove complementary mission-risk coverage. The current system does not calculate a validated risk-coverage percentage or establish a 95% coverage claim.

### Mars targets

Jezero Crater and Arsia Mons are represented as target concepts, but their current environmental feature records are insufficient for numerical matching. They are not included in numerical scoring.

## Development Status

The current backend includes:
- Earth candidate data contract and validation.
- Lunar terrain feature processing.
- Slope-based analog ranking.
- Failure-mode evidence classification.
- Exploratory two-site campaign candidate generation.
- Automated tests.

Frontend integration, end-to-end application demonstration, and further scientific validation remain separate development tasks.

## Disclaimer

This project is an exploratory research and decision-support prototype. Its outputs are not operational mission recommendations, verified analog equivalence assessments, or validated estimates of mission-risk reduction.

All rankings should be interpreted alongside their stated measurement, scale, provenance, and comparability limitations.
