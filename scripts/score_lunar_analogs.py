import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EARTH_PATH = ROOT / "data/processed/earth_candidates_contract.json"
LUNAR_PATH = ROOT / "data/processed/lunar_features.json"
OUTPUT_PATH = ROOT / "data/processed/lunar_slope_rankings.json"


def load_json(path):
    if not path.exists():
        raise FileNotFoundError(f"Required file missing: {path}")
    return json.loads(path.read_text())


def main():
    earth = load_json(EARTH_PATH)
    lunar = load_json(LUNAR_PATH)

    target_slope = lunar["features"]["slope_deg"]["mean"]

    if not isinstance(target_slope, (int, float)):
        raise ValueError("Lunar target slope is unavailable.")

    rankings = []
    excluded = []

    for site in earth:
        features = site.get("features", {})
        metadata = site.get("feature_metadata", {})
        location = site.get("location", {})

        slope = features.get("slope_deg")
        slope_metadata = metadata.get("slope_deg", {})
        status = slope_metadata.get("comparability_status")

        if slope is None:
            excluded.append({
                "site_id": site.get("site_id"),
                "reason": "Missing Earth slope"
            })
            continue

        if status != "approximate":
            excluded.append({
                "site_id": site.get("site_id"),
                "reason": f"Unexpected comparability status: {status}"
            })
            continue

        difference = abs(float(slope) - target_slope)

        rankings.append({
            "site_id": site["site_id"],
            "site_name": site["site_name"],
            "planet": site["planet"],
            "latitude_deg": location.get("latitude_deg"),
            "longitude_deg": location.get("longitude_deg"),
            "earth_slope_deg": float(slope),
            "target_slope_deg": target_slope,
            "absolute_slope_difference_deg": difference,
            "terrain_similarity_status": "approximate",
            "score_type": "slope_difference_only"
        })

    rankings.sort(
        key=lambda item: item["absolute_slope_difference_deg"]
    )

    for rank, item in enumerate(rankings, start=1):
        item["rank"] = rank

    result = {
        "engine_version": "0.1",
        "target": lunar["target"],
        "target_id": lunar["target_id"],
        "earth_sites_received": len(earth),
        "earth_sites_scored": len(rankings),
        "earth_sites_excluded": len(excluded),
        "method": {
            "name": "Absolute mean slope difference",
            "formula": "abs(earth_slope_deg - lunar_slope_deg)",
            "lower_difference_is_better": True
        },
        "comparison_limitations": [
            "Earth terrain sampling scale differs from lunar 5 m raster.",
            "Slope is the only feature used for numerical ranking.",
            "Earth and lunar roughness methods are incompatible.",
            "Albedo and temperature comparisons are unavailable.",
            "Precipitation dryness proxy is not lunar aridity.",
            "This ranking is not a validated overall analog score."
        ],
        "excluded_sites": excluded,
        "rankings": rankings
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")

    print("===== LUNAR ANALOG SCORING ENGINE =====")
    print("Engine version:", result["engine_version"])
    print("Target:", result["target"])
    print("Target slope:", round(target_slope, 4), "degrees")
    print("Earth records received:", len(earth))
    print("Sites scored:", len(rankings))
    print("Sites excluded:", len(excluded))

    print("\nTOP 10 CANDIDATES")
    for item in rankings[:10]:
        print(
            f'{item["rank"]:>2}. '
            f'{item["site_id"]} | '
            f'{item["site_name"]} | '
            f'difference: '
            f'{item["absolute_slope_difference_deg"]:.4f} degrees'
        )

    print("\nOutput:", OUTPUT_PATH.relative_to(ROOT))
    print("RESULT:", "PASS" if rankings else "FAIL")


if __name__ == "__main__":
    main()
