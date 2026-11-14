import { Landing } from "@/components/landing/Landing";
import { loadSitesFromDisk, summarizeSites } from "@/lib/data/loadSites";

// Server component: reads the JSON on the server and passes plain numbers down.
export default async function HomePage() {
  let summary = null;
  try {
    summary = summarizeSites(await loadSitesFromDisk());
  } catch (err) {
    console.error("Could not read earth_candidates.json", err);
  }
  return <Landing summary={summary} />;
}
