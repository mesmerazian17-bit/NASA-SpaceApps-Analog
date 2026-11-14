"use client";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend } from "recharts";
import { AlertTriangle } from "lucide-react";
import type { Site } from "@/lib/data/types";
import { AXES, humanize, radarValues } from "@/lib/data/analysis";

type Ranges = Parameters<typeof radarValues>[1];
const GRAVITY: Record<string, { body: string; g: string }> = {
  "lunar-south-pole": { body: "Moon", g: "0.16g" },
  "jezero-crater": { body: "Mars", g: "0.38g" },
  "arsia-lava-tube": { body: "Mars", g: "0.38g" },
};

export function Engineering({ primary, partner, ranges, target, targetLabel, modes }:
  { primary: Site | null; partner: Site | null; ranges: Ranges; target: string; targetLabel: string; modes: string[] }) {
  if (!primary) return <p className="p-4 text-sm text-slate">No site selected. Loosen the filters to see analysis.</p>;
  const a = radarValues(primary, ranges);
  const b = partner ? radarValues(partner, ranges) : null;
  const data = AXES.map((x) => ({ axis: x.label, primary: a[x.key], ...(b ? { partner: b[x.key] } : {}) }));
  const strong = AXES.filter((x) => a[x.key] >= 70), weak = AXES.filter((x) => a[x.key] <= 30);
  const g = GRAVITY[target];

  return (
    <div className="space-y-5 p-4 text-sm">
      <section>
        <h2 className="font-medium">Engineering risk radar</h2>
        <div className="h-60">
          <ResponsiveContainer>
            <RadarChart data={data} outerRadius="70%">
              <PolarGrid stroke="#8091A5" strokeOpacity={0.35} />
              <PolarAngleAxis dataKey="axis" tick={{ fill: "#E8EEF5", fontSize: 11 }} />
              <PolarRadiusAxis domain={[0, 100]} tick={{ fill: "#8091A5", fontSize: 9 }} />
              <Radar name={primary.name} dataKey="primary" stroke="#E7B85C" fill="#E7B85C" fillOpacity={0.25} />
              {b && <Radar name={partner!.name} dataKey="partner" stroke="#52D6E8" fill="#52D6E8" fillOpacity={0.15} />}
              <Legend wrapperStyle={{ fontSize: 11 }} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
        <p className="text-xs text-slate">Indices (0–100) derived from dataset fields, min-max normalised across all 85 sites. They rank sites against each other; they are not validated engineering scores.</p>
      </section>

      <section role="alert" className="rounded-sm border-2 border-warn bg-warn/10 p-3">
        <h2 className="flex items-center gap-2 font-medium text-warn"><AlertTriangle className="h-4 w-4" aria-hidden />Physics delta: Earth vs {targetLabel}</h2>
        <p className="mt-2 font-mono text-xs">Earth 1g · Moon ≈0.16g · Mars ≈0.38g{g ? ` (target: ${g.body} ${g.g})` : ""}</p>
        <p className="mt-2 text-xs leading-relaxed text-ink/90">Earth's atmosphere, surface pressure, temperature and radiation environment differ greatly from the Moon (near-vacuum) and Mars (thin CO₂ atmosphere). A terrestrial analog reproduces only some terrain or geology traits. It cannot reproduce gravity or atmosphere, so results must not be treated as full flight validation.</p>
      </section>

      <section>
        <h2 className="font-medium">Readiness brief</h2>
        <h3 className="mt-2 text-xs font-medium text-cyan">Data-backed findings (from earth_candidates.json)</h3>
        <ul className="mt-1 list-disc space-y-0.5 pl-5 text-xs">
          <li><span className="font-mono">{primary.site_id}</span>, {humanize(primary.terrain_type)}, {primary.region}</li>
          <li>Slope {primary.slope_deg.toFixed(1)}°, roughness {primary.roughness_rms_m.toFixed(1)} m RMS, elevation {primary.elevation_m} m</li>
          <li>Temperature {primary.t2m_min_c}° to {primary.t2m_max_c}°C (swing {primary.diurnal_temp_swing_k.toFixed(1)} K), aridity {primary.aridity_index.toFixed(2)}</li>
          <li>{primary.distance_to_road_km} km to nearest road; {primary.is_protected_area ? "inside a protected area (access permits likely)" : "not flagged as protected"}</li>
          <li>Seasonal operating window: not in dataset</li>
        </ul>
        <h3 className="mt-3 text-xs font-medium text-gold">Generated interpretation (not validated)</h3>
        <ul className="mt-1 list-disc space-y-0.5 pl-5 text-xs">
          <li>Advantages: {strong.length ? strong.map((x) => x.label.toLowerCase()).join(", ") : "no axis scores 70 or higher"}.</li>
          <li>Limitations: {weak.length ? weak.map((x) => x.label.toLowerCase()).join(", ") : "no axis scores 30 or lower"}.</li>
          <li>Uncertainties: climate values are single-point estimates; dust, illumination, geology and seasonality are not measured in the dataset.</li>
          <li>Suggested tests: {modes.length ? modes.map(humanize).join(", ") : "select failure modes to list tests"}.</li>
        </ul>
      </section>

      <section>
        <h2 className="font-medium">Hardware subsystem scores</h2>
        <p className="text-xs text-slate">Not shown. The dataset has no subsystem metrics and no documented scoring method exists yet. Scores will not be invented.</p>
      </section>
    </div>
  );
}
