import type { Site } from "./types";

/* ---------- Filters (only use fields that exist in the JSON) ---------- */
export interface Filters { excludeProtected: boolean; maxRoadKm: number }

export const filterSites = (sites: Site[], f: Filters) =>
  sites.filter((s) => (!f.excludeProtected || !s.is_protected_area) && s.distance_to_road_km <= f.maxRoadKm);

/* ---------- Radar axes ----------
 * Each axis is a dataset-derived index (0-100), min-max normalised across ALL
 * 85 sites. Skewed fields (roughness, road distance) use log1p first.
 * These are NOT validated engineering scores. */
export interface AxisDef { key: string; label: string; field: keyof Site; invert: boolean; log: boolean; note: string }
export const AXES: AxisDef[] = [
  { key: "slope", label: "Gentle slope", field: "slope_deg", invert: true, log: false, note: "slope_deg, lower = higher index" },
  { key: "rough", label: "Smooth surface", field: "roughness_rms_m", invert: true, log: true, note: "roughness_rms_m, lower = higher index" },
  { key: "arid", label: "Aridity", field: "aridity_index", invert: false, log: false, note: "aridity_index" },
  { key: "swing", label: "Thermal swing", field: "diurnal_temp_swing_k", invert: false, log: false, note: "diurnal_temp_swing_k, larger = closer to airless-body extremes" },
  { key: "access", label: "Accessibility", field: "distance_to_road_km", invert: true, log: true, note: "distance_to_road_km, shorter = higher index" },
];

type Ranges = Record<string, [number, number]>;
const tf = (v: number, log: boolean) => (log ? Math.log1p(v) : v);

export function computeRanges(sites: Site[]): Ranges {
  const out: Ranges = {};
  for (const a of AXES) {
    const vals = sites.map((s) => tf(Number(s[a.field]), a.log));
    out[a.key] = [Math.min(...vals), Math.max(...vals)];
  }
  return out;
}

export function radarValues(site: Site, ranges: Ranges): Record<string, number> {
  const out: Record<string, number> = {};
  for (const a of AXES) {
    const [lo, hi] = ranges[a.key];
    const n = hi === lo ? 0.5 : (tf(Number(site[a.field]), a.log) - lo) / (hi - lo);
    out[a.key] = Math.round((a.invert ? 1 - n : n) * 100);
  }
  return out;
}

/* ---------- Composite partner ----------
 * Method: choose the site (excluding the primary) that adds the most index
 * points on the axes where the primary is weak: sum of max(0, partner - primary). */
export function pickPartner(primary: Site, pool: Site[], ranges: Ranges): Site | null {
  const p = radarValues(primary, ranges);
  let best: Site | null = null, bestGain = -1;
  for (const s of pool) {
    if (s.site_id === primary.site_id) continue;
    const v = radarValues(s, ranges);
    const gain = AXES.reduce((t, a) => t + Math.max(0, v[a.key] - p[a.key]), 0);
    if (gain > bestGain) { bestGain = gain; best = s; }
  }
  return best;
}

export const humanize = (id: string) => id.replace(/_/g, " ");
