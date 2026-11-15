import csv
import copy
import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

RAW_PATH = ROOT / "data/raw/teammates/earth_candidates.json"
STAGING_PATH = Path("/tmp/earth_candidates_staging.csv")
TEMPLATE_PATH = ROOT / "data/processed/earth_candidates_contract.json"
SCHEMA_PATH = ROOT / "data/contracts/earth_moon_feature_schema.json"

OUTPUT_PATH = (
    ROOT / "data/processed/"
    "earth_candidates_contract_reconciled_candidate.json"
)

def load_json(path):
    return json.loads(path.read_text())

def number(value, label):
    if value is None or value == "":
        raise ValueError(f"Missing numeric value: {label}")

    result = float(value)

    if not math.isfinite(result):
        raise ValueError(f"Non-finite numeric value: {label}")

    return result

raw_records = load_json(RAW_PATH)
template_records = load_json(TEMPLATE_PATH)
schema = load_json(SCHEMA_PATH)

with STAGING_PATH.open(newline="") as f:
    staging_records = list(csv.DictReader(f))

raw_by_id = {r["site_id"]: r for r in raw_records}
stage_by_id = {r["site_id"]: r for r in staging_records}
template_by_id = {r["site_id"]: r for r in template_records}

if len(raw_by_id) != 85:
    raise ValueError(f"Expected 85 unique raw sites, got {len(raw_by_id)}")

if set(raw_by_id) != set(stage_by_id):
    raise ValueError("Raw and staging site IDs do not match")

if set(raw_by_id) != set(template_by_id):
    raise ValueError("Raw and template site IDs do not match")

# Verify coordinates and climate fields again before merging.
for site_id in sorted(raw_by_id):
    raw = raw_by_id[site_id]
    stage = stage_by_id[site_id]

    for field in ("lat", "lon"):
        a = number(raw[field], f"{site_id}.{field}")
        b = number(stage[field], f"{site_id}.{field}")

        if not math.isclose(a, b, rel_tol=0, abs_tol=0.000001):
            raise ValueError(f"Coordinate mismatch: {site_id}.{field}")

    for field in ("albedo", "precip_mm_day", "aridity_index"):
        a = number(raw[field], f"{site_id}.{field}")
        b = number(stage[field], f"{site_id}.{field}")

        if not math.isclose(a, b, rel_tol=0, abs_tol=0.0001):
            raise ValueError(f"Climate mismatch: {site_id}.{field}")

    number(
        stage["mean_daily_temp_range_k"],
        f"{site_id}.mean_daily_temp_range_k"
    )

# Confirm normalized roughness is the raw value divided by
# the dataset maximum. Stop rather than silently changing its meaning.
roughness_max = max(
    number(r["roughness_rms_m"], f'{r["site_id"]}.roughness_rms_m')
    for r in raw_records
)

if roughness_max <= 0:
    raise ValueError("Invalid dataset roughness maximum")

for r in raw_records:
    raw_value = number(
        r["roughness_rms_m"],
        f'{r["site_id"]}.roughness_rms_m'
    )
    normalized = number(
        r["roughness_rms"],
        f'{r["site_id"]}.roughness_rms'
    )

    expected = raw_value / roughness_max

    if not math.isclose(
        normalized, expected, rel_tol=0, abs_tol=0.00015
    ):
        raise ValueError(
            f"Normalized roughness formula mismatch: {r['site_id']}"
        )

# Use the existing contract as the structural template.
output = []

for site_id in sorted(raw_by_id):
    raw = raw_by_id[site_id]
    stage = stage_by_id[site_id]
    record = copy.deepcopy(template_by_id[site_id])

    record["site_name"] = raw["name"]
    record["planet"] = "Earth"

    record["location"] = {
        "latitude_deg": number(raw["lat"], f"{site_id}.lat"),
        "longitude_deg": number(raw["lon"], f"{site_id}.lon"),
        "elevation_m": number(
            raw["elevation_m"], f"{site_id}.elevation_m"
        ),
    }

    record["features"] = {
        "terrain_type": raw["terrain_type"],
        "slope_deg": number(raw["slope_deg"], f"{site_id}.slope_deg"),
        "roughness_rms_m": number(
            raw["roughness_rms_m"], f"{site_id}.roughness_rms_m"
        ),
        "roughness_normalized": number(
            raw["roughness_rms"], f"{site_id}.roughness_rms"
        ),
        "albedo": number(raw["albedo"], f"{site_id}.albedo"),
        "mean_daily_temp_range_k": number(
            stage["mean_daily_temp_range_k"],
            f"{site_id}.mean_daily_temp_range_k"
        ),
        "precip_mm_day": number(
            raw["precip_mm_day"], f"{site_id}.precip_mm_day"
        ),
        "precipitation_dryness_proxy": number(
            raw["aridity_index"], f"{site_id}.aridity_index"
        ),
    }

    metadata = record["feature_metadata"]

    metadata["terrain_type"].update({
        "source": "Earth candidate site classification",
        "method": "Categorical terrain classification",
    })

    metadata["slope_deg"].update({
        "source": "OpenTopography API, Mapzen elevation dataset",
        "method": (
            "Five-point center/cardinal elevation stencil; "
            "nominal 500 m offsets"
        ),
        "sampling_scale_m": 1000,
        "comparability_status": "approximate",
    })

    metadata["roughness_rms_m"].update({
        "source": "OpenTopography API, Mapzen elevation dataset",
        "method": (
            "RMS residual from plane fit to five-point "
            "center/cardinal elevation stencil"
        ),
        "sampling_scale_m": 1000,
        "comparability_status": "requires_review",
    })

    metadata["roughness_normalized"].update({
        "source": "Derived from active Earth candidate dataset",
        "method": (
            "roughness_rms_m divided by dataset maximum "
            f"({roughness_max:.4f} m); dataset-dependent normalization"
        ),
        "sampling_scale_m": 1000,
        "comparability_status": "requires_review",
    })

    metadata["albedo"].update({
        "source": "NASA POWER",
        "method": "Source dataset value; original extraction details limited",
        "comparability_status": "unavailable",
    })

    metadata["mean_daily_temp_range_k"].update({
        "source": "NASA POWER",
        "method": (
            "Day-weighted mean of monthly average daily maximum "
            "minus average daily minimum temperature"
        ),
        "comparability_status": "unavailable",
    })

    metadata["precip_mm_day"].update({
        "source": "NASA POWER",
        "method": "Source dataset precipitation value",
        "comparability_status": "unavailable",
    })

    metadata["precipitation_dryness_proxy"].update({
        "source": "Derived from NASA POWER precipitation",
        "method": (
            "Precipitation-only dryness proxy; not UNEP P/PET "
            "or a full climatic aridity index"
        ),
        "comparability_status": "requires_review",
    })

    record["quality"] = {
        "missing_features": [],
        "uncertainty_available": False,
        "quality_notes": [
            "85 Earth candidate records reconciled by site ID and coordinates.",
            "Terrain and elevation fields use the QA-reviewed active JSON.",
            "Corrected mean daily temperature range uses the aligned staging CSV.",
            "Active elevation provider labels are opentopodata-mapzen.",
            "Seven independent DEM cross-checks are comparisons, not ground truth.",
            "Earth slope stencil is approximately 1 km, unlike the 5 m lunar raster.",
            "Earth roughness method differs from lunar local elevation standard deviation.",
            "Normalized roughness is dataset-dependent and not a physical unit.",
            "Climate fields have regional spatial limitations and no equivalent lunar measurements.",
            "Road distance and protected-area estimates are not included as validated measurements.",
        ],
    }

    record["provenance"] = {
        "dataset_version": "earth-reconciled-2026-11-15-v1",
        "source_references": [
            "https://www.opentopodata.org/",
            "https://www.opentopodata.org/datasets/",
            "https://power.larc.nasa.gov/",
        ],
    }

    output.append(record)

# Validate every record against the actual schema.
validator = Draft202012Validator(schema)
errors = []

for index, record in enumerate(output):
    for error in validator.iter_errors(record):
        errors.append(
            f"{record.get('site_id')} "
            f"{'/'.join(map(str, error.absolute_path))}: {error.message}"
        )

if errors:
    print("SCHEMA VALIDATION FAILED")
    for error in errors[:30]:
        print("-", error)
    raise SystemExit(1)

if len(output) != 85:
    raise SystemExit(f"Unexpected output count: {len(output)}")

# Verify the first record's terrain values came from active JSON.
first = next(r for r in output if r["site_id"] == "BM-01")
source = raw_by_id["BM-01"]

assert first["location"]["elevation_m"] == float(source["elevation_m"])
assert first["features"]["slope_deg"] == float(source["slope_deg"])
assert first["features"]["roughness_rms_m"] == float(source["roughness_rms_m"])

OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")

providers = {}
for r in raw_records:
    provider = r.get("elevation_source", "unknown")
    providers[provider] = providers.get(provider, 0) + 1

print("===== RECONCILED CANDIDATE BUILD =====")
print("Records:", len(output))
print("Schema errors:", len(errors))
print("Provider counts:", providers)
print("Roughness normalization maximum:", roughness_max)
print("Output:", OUTPUT_PATH)
print("\n===== BM-01 RECONCILED VALUES =====")
print(json.dumps(first, indent=2))
print("\nPASS: candidate written; original contract unchanged.")
