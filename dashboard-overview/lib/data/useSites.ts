"use client";
import { useEffect, useState } from "react";
import type { RawSite, Site } from "./types";

export function useSites() {
  const [sites, setSites] = useState<Site[]>([]);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");
  useEffect(() => {
    fetch("/data/earth_candidates.json")
      .then((r) => { if (!r.ok) throw new Error(String(r.status)); return r.json() as Promise<RawSite[]>; })
      .then((raw) => {
        setSites(raw.map((r) => ({ ...r, is_benchmark: r.is_benchmark === "True", is_protected_area: r.is_protected_area === "True" })));
        setStatus("ready");
      })
      .catch(() => setStatus("error"));
  }, []);
  return { sites, status };
}
