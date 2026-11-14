"use client";
import dynamic from "next/dynamic";
import Image from "next/image";
import { useMemo, useState } from "react";
import { ChevronUp, ChevronDown } from "lucide-react";
import { useSites } from "@/lib/data/useSites";
import { AXES, computeRanges, filterSites, pickPartner } from "@/lib/data/analysis";
import { TARGETS } from "@/lib/config/assets";
import { Controls, PLANET_TARGETS, type ControlState } from "./Controls";
import { Engineering } from "./Engineering";

const MapView = dynamic(() => import("./MapView"), { ssr: false, loading: () => <p className="p-4 text-slate">Loading map…</p> });

export function Dashboard() {
  const { sites, status } = useSites();
  const [c, setC] = useState<ControlState>({ target: "lunar-south-pole", modes: [], composite: false, excludeProtected: false, maxRoadKm: 800, selectedId: "BM-01" });
  const [drawer, setDrawer] = useState(false);
  const set = (p: Partial<ControlState>) => setC((s) => ({ ...s, ...p }));

  const ranges = useMemo(() => (sites.length ? computeRanges(sites) : null), [sites]);
  const maxRoadLimit = useMemo(() => Math.max(0, ...sites.map((s) => s.distance_to_road_km)), [sites]);
  const filtered = useMemo(() => filterSites(sites, c), [sites, c]);
  const primary = filtered.find((s) => s.site_id === c.selectedId) ?? filtered[0] ?? null;
  const partner = useMemo(() => (c.composite && primary && ranges ? pickPartner(primary, filtered, ranges) : null), [c.composite, primary, filtered, ranges]);
  const target = PLANET_TARGETS.find((t) => t.id === c.target)!;
  const targetImg = TARGETS.find((t) => t.id === c.target)!;

  if (status === "loading") return <p role="status" className="grid h-screen place-items-center text-slate">Loading dataset…</p>;
  if (status === "error" || !ranges) return <p role="alert" className="grid h-screen place-items-center text-critical">Could not load /data/earth_candidates.json.</p>;

  return (
    <div className="flex min-h-screen flex-col bg-space text-ink lg:h-screen">
      <header className="flex items-center justify-between border-b border-slate/20 bg-navy px-4 py-2">
        <h1 className="text-sm font-semibold">Planetary Analog <span className="font-normal text-slate">Mission Control System</span></h1>
        <span className="hidden font-mono text-xs text-slate sm:block">Independent project · not a NASA product</span>
      </header>
      <div className="grid flex-1 grid-cols-1 overflow-hidden lg:grid-cols-[280px_1fr_380px]">
        <aside aria-label="Mission controls" className="overflow-y-auto border-r border-slate/20 bg-panel">
          <Controls state={{ ...c, selectedId: primary?.site_id ?? "" }} set={set} sites={filtered} total={sites.length} maxRoadLimit={maxRoadLimit} partner={partner} />
        </aside>

        <main className="relative flex min-h-[70vh] flex-col lg:min-h-0">
          <div className="relative flex-1">
            {filtered.length === 0 && <p role="status" className="absolute inset-x-0 top-4 z-[1000] mx-auto w-fit rounded-sm bg-panel px-3 py-2 text-sm text-warn">No sites match the current filters.</p>}
            <MapView sites={filtered} primary={primary} partner={partner} onSelect={(id) => set({ selectedId: id })} />
            {primary && (
              <div className="absolute bottom-3 left-3 z-[1000] max-w-xs rounded-sm border border-slate/30 bg-panel/95 p-3 text-xs">
                <p className="font-medium">{primary.name}</p>
                <p className="font-mono text-slate">{primary.lat.toFixed(2)}, {primary.lon.toFixed(2)} · {primary.site_id}</p>
                <p className="mt-1 text-slate">Seasonal window: not in dataset</p>
              </div>)}
          </div>
          <section className="border-t border-slate/20 bg-panel">
            <button onClick={() => setDrawer(!drawer)} aria-expanded={drawer} className="flex w-full items-center justify-between px-4 py-2 text-sm">
              Imagery comparison {drawer ? <ChevronDown className="h-4 w-4" aria-hidden /> : <ChevronUp className="h-4 w-4" aria-hidden />}
            </button>
            {drawer && primary && (
              <div className="grid h-56 grid-cols-2 gap-px bg-slate/20">
                <div className="relative"><MapView sites={[primary]} primary={primary} partner={null} satellite />
                  <span className="absolute left-2 top-2 z-[1000] rounded-sm bg-space/80 px-2 py-0.5 text-xs">Earth satellite: {primary.name}</span></div>
                <div className="relative bg-navy">
                  <Image src={targetImg.image} alt={targetImg.alt} fill sizes="40vw" className="object-cover" />
                  <span className="absolute left-2 top-2 rounded-sm bg-space/80 px-2 py-0.5 text-xs">{target.label}: illustrative AI image, not orbital data</span></div>
              </div>)}
          </section>
        </main>

        <aside aria-label="Engineering analysis" className="overflow-y-auto border-l border-slate/20 bg-panel">
          <Engineering primary={primary} partner={partner} ranges={ranges} target={c.target} targetLabel={target.label} modes={c.modes} />
        </aside>
      </div>
    </div>
  );
}
