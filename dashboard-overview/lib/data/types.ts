/**
 * Shape of one record in public/data/earth_candidates.json.
 * Verified against the file: 85 records, no null values.
 * NOTE: the file stores booleans as the strings "True" / "False".
 */
export interface RawSite {
  site_id: string;
  name: string;
  region: string;
  lat: number;
  lon: number;
  is_benchmark: "True" | "False";
  terrain_type: string;
  distance_to_road_km: number;
  is_protected_area: "True" | "False";
  elevation_m: number;
  elevation_source: string;
  t2m_max_c: number;
  t2m_min_c: number;
  diurnal_temp_swing_k: number;
  albedo: number;
  precip_mm_day: number;
  aridity_index: number;
  slope_deg: number;
  roughness_rms_m: number;
  roughness_rms: number;
}

/** Cleaned version used by the UI: real booleans instead of strings. */
export interface Site extends Omit<RawSite, "is_benchmark" | "is_protected_area"> {
  is_benchmark: boolean;
  is_protected_area: boolean;
}
