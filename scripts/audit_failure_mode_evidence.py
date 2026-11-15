import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EARTH_PATH = ROOT / "data/processed/earth_candidates_contract.json"
TARGET_PATH = ROOT / "data/planetary_targets.json"
OUTPUT_PATH = ROOT / "data/processed/failure_mode_evidence_audit.json"


def load_json(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return json.loads(path.read_text())


def build_lunar_evidence(site, target):
    features = site.get("features", {})
    metadata = site.get("feature_metadata", {})
    terrain = features.get("terrain_type")

    earth_slope = features.get("slope_deg")
    lunar_slope = target["features"].get("slope_deg")

    slope_metadata = metadata.get("slope_deg", {})
    slope_status = slope_metadata.get("comparability_status")

    if (
        earth_slope is not None
        and lunar_slope is not None
        and slope_status == "approximate"
    ):
        slope = {
            "status": "quantitative_proxy",
            "earth_value": earth_slope,
            "target_value": lunar_slope,
            "absolute_difference": abs(earth_slope - lunar_slope),
            "unit": "degrees",
            "caveat": "Mean slope comparison; different spatial sampling scales."
        }
    else:
        slope = {
            "status": "unavailable",
            "reason": "Compatible slope measurements unavailable."
        }

    temperature = features.get("mean_daily_temp_range_k")

    thermal = {
        "status": "contextual_only",
        "earth_value": temperature,
        "unit": "K",
        "reason": "Earth daily temperature range exists, but no equivalent lunar measurement is available."
    } if temperature is not None else {
        "status": "unavailable",
        "reason": "Earth temperature measurement unavailable."
    }

    dust = {
        "status": "contextual_only",
        "earth_value": terrain,
        "reason": "Terrain classification provides environmental context only; no direct dust grain, cohesion, or electrostatic measurements."
    } if terrain else {
        "status": "unavailable",
        "reason": "Terrain classification unavailable."
    }

    illumination = {
        "status": "unavailable",
        "reason": "No matched solar illumination, shadow duration, or navigation measurements."
    }

    return {
        "steep_slope_traversal": slope,
        "thermal_extremes": thermal,
        "electrostatic_dust": dust,
        "illumination_shadow_navigation": illumination
    }


def main():
    earth = load_json(EARTH_PATH)
    targets = load_json(TARGET_PATH)["targets"]

    lunar_target = next(
        item for item in targets
        if item["target_id"] == "lunar_south_pole"
    )

    output = {
        "audit_version": "1.0",
        "earth_sites_evaluated": len(earth),
        "target": lunar_target["name"],
        "coverage_percent_calculated": False,
        "policy": [
            "Quantitative proxies are not proof of mission failure-mode fidelity.",
            "Contextual evidence is not counted as quantitative coverage.",
            "Unavailable evidence is never converted to zero.",
            "No validated failure-mode coverage percentage is claimed."
        ],
        "sites": []
    }

    totals = {
        "quantitative_proxy": 0,
        "contextual_only": 0,
        "unavailable": 0
    }

    for site in earth:
        evidence = build_lunar_evidence(site, lunar_target)

        for item in evidence.values():
            totals[item["status"]] += 1

        output["sites"].append({
            "site_id": site["site_id"],
            "site_name": site["site_name"],
            "failure_mode_evidence": evidence
        })

    output["evidence_item_totals"] = totals

    # Mars targets remain unscored until measurements are populated.
    output["mars_targets"] = []

    for target in targets:
        if target["planet"] != "Mars":
            continue

        output["mars_targets"].append({
            "target_id": target["target_id"],
            "target_name": target["name"],
            "numerical_scoring_eligible": False,
            "reason": "No target environmental features currently populated."
        })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")

    print("===== FAILURE-MODE EVIDENCE AUDIT =====")
    print("Earth sites:", len(earth))
    print("Target:", lunar_target["name"])
    print("\nEvidence item totals:")
    for status, count in totals.items():
        print(f"  {status}: {count}")

    print("\nMars targets:")
    for target in output["mars_targets"]:
        print(" ", target["target_name"], "-> not numerically scoreable")

    print("\nOutput:", OUTPUT_PATH.relative_to(ROOT))
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
