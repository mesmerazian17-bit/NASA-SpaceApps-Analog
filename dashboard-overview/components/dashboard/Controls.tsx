"use client";
import type { Site } from "@/lib/data/types";
import { humanize } from "@/lib/data/analysis";

export const PLANET_TARGETS = [
  { id: "lunar-south-pole", label: "Lunar South Pole", body: "Moon" },
  { id: "jezero-crater", label: "Jezero Crater", body: "Mars" },
  { id: "arsia-lava-tube", label: "Arsia Lava Tube", body: "Mars" },
] as const;
export const FAILURE_MODES = [
  { id: "electrostatic_dust", label: "Electrostatic dust" },
  { id: "low_angle_shadow_navigation", label: "Low-angle shadow navigation" },
  { id: "gps_denied_subsurface_slam", label: "GPS-denied subsurface SLAM" },
  { id: "subsurface_core_drilling", label: "Subsurface core drilling" },
] as const;

export interface ControlState {
  target: string; modes: string[]; composite: boolean; excludeProtected: boolean; maxRoadKm: number; selectedId: string;
}
interface Props {
  state: ControlState; set: (p: Partial<ControlState>) => void;
  sites: Site[]; total: number; maxRoadLimit: number; partner: Site | null;
}

const label = "mb-1.5 block text-xs font-medium text-slate";
const field = "w-full rounded-sm border border-slate/30 bg-navy px-2 py-1.5 text-sm text-ink";

export function Controls({ state, set, sites, total, maxRoadLimit, partner }: Props) {
  const toggleMode = (id: string) =>
    set({ modes: state.modes.includes(id) ? state.modes.filter((m) => m !== id) : [...state.modes, id] });
  return (
    <div className="space-y-5 p-4">
      <div><label className={label} htmlFor="t">Planetary target</label>
        <select id="t" className={field} value={state.target} onChange={(e) => set({ target: e.target.value })}>
          {PLANET_TARGETS.map((t) => <option key={t.id} value={t.id}>{t.label}</option>)}
        </select></div>

      <div><label className={label} htmlFor="s">Primary analog site ({sites.length} of {total} shown)</label>
        <select id="s" className={field} value={state.selectedId} onChange={(e) => set({ selectedId: e.target.value })}>
          {sites.map((s) => <option key={s.site_id} value={s.site_id}>{s.site_id} · {s.name}</option>)}
        </select></div>

      <fieldset><legend className={label}>Failure modes to test</legend>
        {FAILURE_MODES.map((m) => (
          <label key={m.id} className="flex items-center gap-2 py-1 text-sm">
            <input type="checkbox" checked={state.modes.includes(m.id)} onChange={() => toggleMode(m.id)} className="accent-[#52D6E8]" />
            {m.label}
          </label>))}
        <p className="mt-1 text-xs text-slate">The dataset has no failure-mode fields, so these do not change site scores. They shape the suggested test list only.</p>
      </fieldset>

      <div><label className="flex items-center gap-2 text-sm">
        <input type="checkbox" checked={state.composite} onChange={(e) => set({ composite: e.target.checked })} className="accent-[#52D6E8]" />
        Composite two-site campaign</label>
        {state.composite && (
          <p className="mt-2 rounded-sm bg-navy p-2 text-xs text-slate">
            <span className="text-gold">Primary:</span> {sites.find((s) => s.site_id === state.selectedId)?.name ?? "none"}<br />
            <span className="text-cyan">Partner:</span> {partner?.name ?? "none available"}
          </p>)}
      </div>

      <div className="space-y-3 border-t border-slate/20 pt-4">
        <p className="text-xs font-medium text-slate">Operational filters</p>
        <label className="flex items-center gap-2 text-sm">
          <input type="checkbox" checked={state.excludeProtected} onChange={(e) => set({ excludeProtected: e.target.checked })} className="accent-[#52D6E8]" />
          Exclude protected national parks</label>
        <div><label className={label} htmlFor="r">Max road distance: <span className="font-mono text-ink">{state.maxRoadKm} km</span></label>
          <input id="r" type="range" min={0} max={maxRoadLimit} step={5} value={state.maxRoadKm}
            onChange={(e) => set({ maxRoadKm: Number(e.target.value) })} className="w-full accent-[#52D6E8]" /></div>
      </div>

      <ul className="space-y-1 border-t border-slate/20 pt-4 text-xs text-slate">
        <li><span className="text-gold">●</span> Primary site</li><li><span className="text-cyan">●</span> Composite partner</li>
        <li><span className="text-slate">●</span> Benchmark site (is_benchmark flag)</li><li><span className="text-ink">●</span> Other candidate</li>
      </ul>
    </div>
  );
}
