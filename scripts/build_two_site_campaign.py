import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EARTH_PATH = ROOT / "data/processed/earth_candidates_contract.json"
RANKING_PATH = ROOT / "data/processed/lunar_slope_rankings.json"
OUTPUT_PATH = ROOT / "data/processed/two_site_campaign_candidates.json"


def read_json(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return json.loads(path.read_text())


def main():
    earth = read_json(EARTH_PATH)
    ranking_data = read_json(RANKING_PATH)

    rankings = {
        item["site_id"]: item
        for item in ranking_data["rankings"]
    }

    candidates = []

    for site in earth:
        site_id = site["site_id"]

        if site_id not in rankings:
            continue

        terrain = site.get("features", {}).get("terrain_type")

        candidates.append({
            "site_id": site_id,
            "site_name": site["site_name"],
            "terrain_type": terrain,
            "slope_deg": rankings[site_id]["earth_slope_deg"],
            "slope_difference_deg": rankings[site_id][
                "absolute_slope_difference_deg"
            ],
            "region": site.get("provenance", {}).get("region")
        })

    pairs = []

    for first, second in combinations(candidates, 2):
        # Different terrain categories are required for this shortlist.
        if not first["terrain_type"] or not second["terrain_type"]:
            continue

        if first["terrain_type"] == second["terrain_type"]:
            continue

        mean_slope_difference = (
            first["slope_difference_deg"]
            + second["slope_difference_deg"]
        ) / 2

        pairs.append({
            "sites": [first, second],
            "terrain_categories_differ": True,
            "mean_slope_difference_deg": mean_slope_difference,
            "worst_site_slope_difference_deg": max(
                first["slope_difference_deg"],
                second["slope_difference_deg"]
            ),
            "failure_mode_complementarity": "not_established",
            "validated_risk_coverage_percent": None
        })

    # Prefer pairs where both sites are close slope matches.
    pairs.sort(
        key=lambda pair: (
            pair["mean_slope_difference_deg"],
            pair["worst_site_slope_difference_deg"]
        )
    )

    for rank, pair in enumerate(pairs, start=1):
        pair["rank"] = rank

    result = {
        "engine_version": "0.1",
        "target": ranking_data["target"],
        "candidate_sites": len(candidates),
        "different_terrain_pairs_evaluated": len(pairs),
        "selection_method": [
            "Both sites must have different terrain categories.",
            "Pairs are ranked by mean absolute slope difference.",
            "Worst individual slope difference breaks ties."
        ],
        "interpretation": [
            "This is an exploratory two-site shortlist.",
            "Different terrain categories do not prove different failure-mode coverage.",
            "No validated risk coverage percentage is calculated.",
            "Slope comparison retains the Earth-versus-lunar scale limitation."
        ],
        "campaign_candidates": pairs[:20]
    }

    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")

    print("===== TWO-SITE CAMPAIGN SHORTLIST =====")
    print("Candidate sites:", len(candidates))
    print("Different-terrain pairs evaluated:", len(pairs))
    print("Pairs saved:", len(result["campaign_candidates"]))

    for pair in result["campaign_candidates"][:10]:
        first, second = pair["sites"]
        print(
            f'\n#{pair["rank"]}: '
            f'{first["site_id"]} + {second["site_id"]}'
        )
        print("  Site 1:", first["site_name"])
        print("  Site 2:", second["site_name"])
        print(
            "  Mean slope difference:",
            round(pair["mean_slope_difference_deg"], 4),
            "degrees"
        )
        print(
            "  Terrain categories:",
            first["terrain_type"],
            "|",
            second["terrain_type"]
        )
        print("  Risk complementarity: NOT ESTABLISHED")

    print("\nOutput:", OUTPUT_PATH.relative_to(ROOT))
    print("RESULT:", "PASS" if pairs else "FAIL")


if __name__ == "__main__":
    main()
