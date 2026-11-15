import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PROCESSED = DATA / "processed"
FRONTEND = ROOT / "frontend"

app = FastAPI(
    title="Orbitra API",
    description="Backend data service for the Planetary Analog Explorer",
    version="1.0.0",
)


def load_json(path: Path):
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Required data file not found: {path.name}",
        )

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON in {path.name}: {exc}",
        )


@app.get("/")
def frontend():
    index = FRONTEND / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(index)


@app.get("/api/health")
def health():
    required_files = [
        PROCESSED / "earth_candidates_contract.json",
        PROCESSED / "lunar_features.json",
        PROCESSED / "lunar_slope_rankings.json",
        PROCESSED / "two_site_campaign_candidates.json",
        PROCESSED / "failure_mode_evidence_audit.json",
        DATA / "planetary_targets.json",
    ]

    return {
        "status": "ok",
        "service": "Orbitra API",
        "data_files": {
            path.name: path.exists()
            for path in required_files
        },
    }


@app.get("/api/sites")
def get_sites():
    return load_json(PROCESSED / "earth_candidates_contract.json")


@app.get("/api/sites/{site_id}")
def get_site(site_id: str):
    for site in get_sites():
        if site["site_id"] == site_id:
            return site
    raise HTTPException(status_code=404, detail="Site not found")


@app.get("/api/map")
def get_map():
    features = []

    for site in get_sites():
        location = site["location"]
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    location["longitude_deg"],
                    location["latitude_deg"],
                ],
            },
            "properties": {
                "site_id": site["site_id"],
                "site_name": site["site_name"],
                "planet": site["planet"],
                **site["features"],
            },
        })

    return {"type": "FeatureCollection", "features": features}


@app.get("/api/lunar-reference")
def get_lunar_reference():
    return load_json(PROCESSED / "lunar_features.json")


@app.get("/api/rankings")
def get_rankings():
    return load_json(PROCESSED / "lunar_slope_rankings.json")


@app.get("/api/campaigns")
def get_campaigns():
    return load_json(PROCESSED / "two_site_campaign_candidates.json")


@app.get("/api/failure-evidence")
def get_failure_evidence():
    return load_json(PROCESSED / "failure_mode_evidence_audit.json")


@app.get("/api/targets")
def get_targets():
    return load_json(DATA / "planetary_targets.json")
