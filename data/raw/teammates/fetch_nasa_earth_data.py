#!/usr/bin/env python3
"""Enrich data/seed_locations.csv with physical metrics -> data/earth_candidates.csv.

Sources
  * NASA POWER climatology (T2M_MAX, T2M_MIN, T2M_MAX_AVG,
    T2M_MIN_AVG, ALLSKY_SRF_ALB, PRECTOTCORR)
      -> mean_daily_temp_range_k, annual temperature extremes, albedo,
         aridity_index (0-1)
  * Open-Elevation (centre + 4 points ~500 m N/S/E/W)
      -> slope_deg, roughness_rms (0-1, min-max normalised over the dataset)

Caveats
  * Open-Elevation serves SRTM, which only covers ~56S-60N. Outside that band (all
    polar sites) or if Open-Elevation keeps failing, the script falls back to
    OpenTopoData's global 'mapzen' dataset (disable with --no-fallback). The
    'elevation_source' column records which service produced each row.
  * Aridity index = 1 - clip(annual-mean precip / 6 mm/day, 0, 1). 0 = very wet, 1 = no
    rain. Precipitation-only; it ignores PET. Adjust PRECIP_REF_MM_DAY to taste.
  * roughness_rms (raw) = RMS residual (m) of a least-squares plane fitted to the 5
    elevation samples; a 500 m-scale curvature/roughness proxy, not a fine-scale one.
  * POWER is ~0.5 deg resolution, so values are regional, not point-exact.
"""
import argparse
import logging
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[3]
SEED_CSV = ROOT / "data" / "seed_locations.csv"
OUT_CSV = ROOT / "data" / "earth_candidates.csv"

POWER_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"
POWER_PARAMS = (
    "T2M_MAX,T2M_MIN,"
    "T2M_MAX_AVG,T2M_MIN_AVG,"
    "ALLSKY_SRF_ALB,PRECTOTCORR"
)
OPEN_ELEV_URL = "https://api.open-elevation.com/api/v1/lookup"
OPENTOPO_URL = "https://api.opentopodata.org/v1/mapzen"

OFFSET_M = 500.0
M_PER_DEG_LAT = 111_320.0
PRECIP_REF_MM_DAY = 6.0
SRTM_LAT_MIN, SRTM_LAT_MAX = -56.0, 60.0
MAX_RETRIES = 4
TIMEOUT = 60
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

# NASA POWER climatology uses a representative non-leap calendar.
MONTH_DAYS = {
    "JAN": 31, "FEB": 28, "MAR": 31, "APR": 30,
    "MAY": 31, "JUN": 30, "JUL": 31, "AUG": 31,
    "SEP": 30, "OCT": 31, "NOV": 30, "DEC": 31,
}

log = logging.getLogger("fetch")
session = requests.Session()
session.headers["User-Agent"] = "nasa-space-apps-earth-analogs/1.0"


def request_json(method, url, delay, **kwargs):
    """HTTP request with exponential-backoff retries; sleeps `delay` s after every call."""
    last = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.request(method, url, timeout=TIMEOUT, **kwargs)
            if resp.status_code == 429 or resp.status_code >= 500:
                raise requests.HTTPError(f"HTTP {resp.status_code}", response=resp)
            resp.raise_for_status()
            data = resp.json()
            time.sleep(delay)
            return data
        except (requests.RequestException, ValueError) as exc:
            last = exc
            wait = 2 ** attempt
            resp_obj = getattr(exc, "response", None)
            if resp_obj is not None and resp_obj.status_code == 429:
                retry_after = resp_obj.headers.get("Retry-After", "")
                wait = max(int(retry_after) if retry_after.isdigit() else 0, 15 * attempt)
            log.warning("%s attempt %d/%d failed (%s); retrying in %ds", url, attempt, MAX_RETRIES, exc, wait)
            time.sleep(wait)
    raise RuntimeError(f"giving up on {url}: {last}")


# ---------------------------------------------------------------- NASA POWER
def _annual(series):
    """Annual value from a POWER monthly dict; POWER uses -999 as fill."""
    ann = series.get("ANN")
    if ann is not None and ann > -990:
        return float(ann)
    vals = [series[m] for m in MONTHS if m in series and series[m] > -990]
    return float(np.mean(vals)) if len(vals) >= 6 else float("nan")


def mean_daily_temp_range(max_avg, min_avg):
    """
    Calculate the day-weighted mean of 12 monthly average daily
    maximum-minus-minimum temperature ranges.

    Return NaN if any month is missing or contains a POWER fill value.
    """
    weighted_sum = 0.0
    total_days = 0

    for month in MONTHS:
        raw_max = max_avg.get(month)
        raw_min = min_avg.get(month)

        if raw_max is None or raw_min is None:
            return float("nan")

        try:
            tmax = float(raw_max)
            tmin = float(raw_min)
        except (TypeError, ValueError):
            return float("nan")

        if (
            not math.isfinite(tmax)
            or not math.isfinite(tmin)
            or tmax <= -990
            or tmin <= -990
        ):
            return float("nan")

        days = MONTH_DAYS[month]
        monthly_range = tmax - tmin

        if monthly_range < 0:
            return float("nan")

        weighted_sum += monthly_range * days
        total_days += days

    if total_days != sum(MONTH_DAYS.values()):
        return float("nan")

    return weighted_sum / total_days


def fetch_power(lat, lon, delay):
    params = {"parameters": POWER_PARAMS, "community": "SB", "longitude": lon,
              "latitude": lat, "format": "JSON"}
    data = request_json("GET", POWER_URL, delay, params=params)
    p = data["properties"]["parameter"]
    tmax, tmin = _annual(p["T2M_MAX"]), _annual(p["T2M_MIN"])
    daily_range = mean_daily_temp_range(
        p["T2M_MAX_AVG"],
        p["T2M_MIN_AVG"],
    )
    albedo, precip = _annual(p["ALLSKY_SRF_ALB"]), _annual(p["PRECTOTCORR"])
    return {
        "t2m_max_c": tmax,
        "t2m_min_c": tmin,
        "mean_daily_temp_range_k": daily_range,
        "albedo": albedo,
        "precip_mm_day": precip,
        "aridity_index": 1.0 - min(max(precip / PRECIP_REF_MM_DAY, 0.0), 1.0) if not math.isnan(precip) else float("nan"),
    }


# ----------------------------------------------------------------- Elevation
def sample_points(lat, lon):
    """Centre, N, S, E, W with metre offsets (x east, y north)."""
    dlat = OFFSET_M / M_PER_DEG_LAT
    dlon = OFFSET_M / (M_PER_DEG_LAT * max(math.cos(math.radians(lat)), 1e-6))
    pts = [(lat, lon), (lat + dlat, lon), (lat - dlat, lon), (lat, lon + dlon), (lat, lon - dlon)]
    return [p if abs(p[0]) <= 90 else (max(min(p[0], 90), -90), p[1]) for p in pts]


def elevations_open_elevation(points, delay):
    body = {"locations": [{"latitude": a, "longitude": b} for a, b in points]}
    data = request_json("POST", OPEN_ELEV_URL, delay, json=body)
    z = [r["elevation"] for r in data["results"]]
    if len(z) != 5 or any(v is None for v in z):
        raise RuntimeError("incomplete Open-Elevation response")
    return z


def elevations_opentopo(points, delay):
    locs = "|".join(f"{a:.6f},{b:.6f}" for a, b in points)
    data = request_json("GET", OPENTOPO_URL, max(delay, 1.1), params={"locations": locs})
    z = [r["elevation"] for r in data["results"]]
    if len(z) != 5 or any(v is None for v in z):
        raise RuntimeError("incomplete OpenTopoData response")
    return z


def terrain_metrics(z):
    """z = [centre, N, S, E, W] elevations (m) at +/-OFFSET_M."""
    c, n, s, e, w = z
    dzdx = (e - w) / (2 * OFFSET_M)
    dzdy = (n - s) / (2 * OFFSET_M)
    slope = math.degrees(math.atan(math.hypot(dzdx, dzdy)))
    xy = np.array([[0, 0], [0, OFFSET_M], [0, -OFFSET_M], [OFFSET_M, 0], [-OFFSET_M, 0]], float)
    A = np.column_stack([np.ones(5), xy])
    coef, *_ = np.linalg.lstsq(A, np.array(z, float), rcond=None)
    rms = float(np.sqrt(np.mean((np.array(z, float) - A @ coef) ** 2)))
    return {"elevation_m": c, "slope_deg": slope, "roughness_rms_m": rms}


def fetch_terrain(lat, lon, delay, allow_fallback, provider="auto"):
    pts = sample_points(lat, lon)
    source, z = None, None
    if provider == "opentopodata":
        return {**terrain_metrics(elevations_opentopo(pts, delay)), "elevation_source": "opentopodata-mapzen"}
    if SRTM_LAT_MIN <= lat <= SRTM_LAT_MAX:
        try:
            z, source = elevations_open_elevation(pts, delay), "open-elevation"
        except Exception as exc:
            log.warning("Open-Elevation failed for (%s, %s): %s", lat, lon, exc)
    else:
        log.info("(%s, %s) is outside SRTM coverage", lat, lon)
    if z is None and allow_fallback:
        z, source = elevations_opentopo(pts, delay), "opentopodata-mapzen"
    if z is None:
        raise RuntimeError("no elevation source available")
    out = terrain_metrics(z)
    out["elevation_source"] = source
    return out


# ---------------------------------------------------------------------- main
def minmax(s):
    lo, hi = s.min(), s.max()
    return (s - lo) / (hi - lo) if pd.notna(lo) and hi > lo else s * 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, default=SEED_CSV)
    ap.add_argument("--output", type=Path, default=OUT_CSV)
    ap.add_argument("--delay", type=float, default=0.5, help="seconds to sleep after each API call")
    ap.add_argument("--limit", type=int, default=None, help="only process the first N rows (testing)")
    ap.add_argument("--no-fallback", action="store_true", help="never use OpenTopoData")
    ap.add_argument("--elevation-provider", choices=["auto", "opentopodata"], default="auto",
                    help="auto = Open-Elevation first (SRTM latitudes) then OpenTopoData; "
                         "opentopodata = skip Open-Elevation entirely (use if it keeps returning 429)")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    seed = pd.read_csv(args.input)
    if args.limit:
        seed = seed.head(args.limit)

    extras = []
    for i, row in enumerate(seed.itertuples(index=False), 1):
        log.info("[%d/%d] %s %s (%.4f, %.4f)", i, len(seed), row.site_id, row.name, row.lat, row.lon)
        rec = {}
        try:
            rec.update(fetch_power(row.lat, row.lon, args.delay))
        except Exception as exc:
            log.error("POWER failed for %s: %s", row.site_id, exc)
        try:
            rec.update(fetch_terrain(row.lat, row.lon, args.delay, not args.no_fallback, args.elevation_provider))
        except Exception as exc:
            log.error("Elevation failed for %s: %s", row.site_id, exc)
        extras.append(rec)

    df = pd.concat([seed.reset_index(drop=True), pd.DataFrame(extras)], axis=1)
    for col in ["t2m_max_c", "t2m_min_c", "mean_daily_temp_range_k",
                "albedo", "precip_mm_day", "aridity_index", "elevation_m",
                "slope_deg", "roughness_rms_m", "elevation_source"]:
        if col not in df:
            df[col] = np.nan
    df["roughness_rms"] = minmax(df["roughness_rms_m"])

    order = ["site_id", "name", "region", "lat", "lon", "is_benchmark", "terrain_type",
             "distance_to_road_km", "is_protected_area", "elevation_m", "elevation_source",
             "t2m_max_c", "t2m_min_c", "mean_daily_temp_range_k",
             "albedo", "precip_mm_day",
             "aridity_index", "slope_deg", "roughness_rms_m", "roughness_rms"]
    df = df[order].round(4)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    missing = df[
        ["mean_daily_temp_range_k", "albedo", "aridity_index", "slope_deg"]
    ].isna().any(axis=1).sum()
    log.info("Saved %d rows to %s (%d rows have at least one missing metric)", len(df), args.output, missing)


if __name__ == "__main__":
    main()
