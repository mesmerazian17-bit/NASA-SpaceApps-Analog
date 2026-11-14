import { readFile } from "node:fs/promises";
import path from "node:path";
import type { RawSite, Site } from "./types";

/** Convert the file's "True"/"False" strings into real booleans. */
export function normalizeSite(raw: RawSite): Site {
  return {
    ...raw,
    is_benchmark: raw.is_benchmark === "True",
    is_protected_area: raw.is_protected_area === "True",
  };
}

/** Server-side loader (used by server components such as the landing page). */
export async function loadSitesFromDisk(): Promise<Site[]> {
  const file = path.join(process.cwd(), "public", "data", "earth_candidates.json");
  const text = await readFile(file, "utf8");
  const raw = JSON.parse(text) as RawSite[];
  return raw.map(normalizeSite);
}

export interface DatasetSummary {
  siteCount: number;
  benchmarkCount: number;
  terrainTypeCount: number;
  regionCount: number;
  minLat: number;
  maxLat: number;
}

/** Every number on the landing page is computed here from the JSON. */
export function summarizeSites(sites: Site[]): DatasetSummary | null {
  if (sites.length === 0) return null;
  const lats = sites.map((s) => s.lat);
  return {
    siteCount: sites.length,
    benchmarkCount: sites.filter((s) => s.is_benchmark).length,
    terrainTypeCount: new Set(sites.map((s) => s.terrain_type)).size,
    regionCount: new Set(sites.map((s) => s.region)).size,
    minLat: Math.min(...lats),
    maxLat: Math.max(...lats),
  };
}

export function formatLat(lat: number): string {
  return `${Math.abs(lat).toFixed(1)}°${lat < 0 ? "S" : "N"}`;
}
