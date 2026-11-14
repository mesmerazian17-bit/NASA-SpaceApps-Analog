import type { DatasetSummary } from "@/lib/data/loadSites";
import { formatLat } from "@/lib/data/loadSites";

/**
 * Small readout of what is actually in earth_candidates.json.
 * Every value is computed from the file. If the file cannot be read,
 * we say so instead of showing placeholder numbers.
 */
export function DatasetReadout({ summary }: { summary: DatasetSummary | null }) {
  if (!summary) {
    return (
      <div role="status" className="w-full max-w-sm rounded border border-warn/50 bg-panel/90 p-4 text-sm lg:w-80">
        <p className="font-medium text-warn">Dataset unavailable</p>
        <p className="mt-1 text-slate">
          Could not read <span className="font-mono">public/data/earth_candidates.json</span>. Check that the
          file exists and is valid JSON.
        </p>
      </div>
    );
  }

  const rows: [string, string][] = [
    ["Candidate sites", String(summary.siteCount)],
    ["Benchmark sites", String(summary.benchmarkCount)],
    ["Terrain types", String(summary.terrainTypeCount)],
    ["Regions", String(summary.regionCount)],
    ["Latitude span", `${formatLat(summary.minLat)} to ${formatLat(summary.maxLat)}`],
  ];

  return (
    <aside aria-label="Dataset summary" className="w-full max-w-sm rounded border border-slate/25 bg-panel/85 p-4 backdrop-blur-sm lg:w-80">
      <p className="text-sm font-medium text-ink">Loaded dataset</p>
      <dl className="mt-3 divide-y divide-slate/15">
        {rows.map(([label, value]) => (
          <div key={label} className="flex items-baseline justify-between py-1.5">
            <dt className="text-sm text-slate">{label}</dt>
            <dd className="font-mono text-sm text-ink">{value}</dd>
          </div>
        ))}
      </dl>
      <p className="mt-3 font-mono text-[11px] text-slate">source: earth_candidates.json</p>
    </aside>
  );
}
