import Image from "next/image";
import { ASSETS, TARGETS } from "@/lib/config/assets";
import type { DatasetSummary } from "@/lib/data/loadSites";
import { EnterButton } from "./EnterButton";
import { MissionClock } from "./MissionClock";
import { DatasetReadout } from "./DatasetReadout";
import { Graticule } from "./Graticule";

export function Landing({ summary }: { summary: DatasetSummary | null }) {
  return (
    <main className="relative isolate min-h-screen overflow-hidden bg-space">
      {/* Layer 1: gradient fallback so the page looks right even if an image is missing */}
      <div
        aria-hidden
        className="absolute inset-0 -z-30"
        style={{
          background:
            "radial-gradient(120% 80% at 70% 100%, #2a1f1a 0%, #101A29 45%, #080D16 100%)",
        }}
      />
      {/* Layer 2: hero image with slow drift */}
      <Image
        src={ASSETS.heroBackground}
        alt=""
        fill
        priority
        sizes="100vw"
        className="hero-drift -z-20 object-cover"
      />
      {/* Layer 3: readability scrims */}
      <div
        aria-hidden
        className="absolute inset-0 -z-10"
        style={{
          background:
            "linear-gradient(90deg, rgba(8,13,22,.92) 0%, rgba(8,13,22,.62) 42%, rgba(8,13,22,.15) 100%), linear-gradient(0deg, rgba(8,13,22,.95) 0%, rgba(8,13,22,0) 38%)",
        }}
      />
      <Graticule />

      <div className="mx-auto flex min-h-screen max-w-[1400px] flex-col px-6 py-6 md:px-10">
        {/* Top bar */}
        <header className="flex items-start justify-between gap-4">
          <div>
            <p className="font-mono text-xs text-slate">PLANETARY ANALOG PROJECT</p>
            <p className="mt-1 max-w-xs text-xs leading-relaxed text-slate">
              Independent scientific project. Not a NASA product and not endorsed by NASA.
            </p>
          </div>
          <MissionClock />
        </header>

        {/* Main content */}
        <div className="flex flex-1 flex-col justify-end gap-10 pb-8 pt-16 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <h1 className="reveal font-semibold leading-[0.92] tracking-tight text-ink text-[clamp(3rem,9vw,7.5rem)]">
              PLANETARY
              <br />
              ANALOG
            </h1>
            <p className="reveal reveal-2 mt-5 font-mono text-sm tracking-[0.28em] text-cyan md:text-base">
              MISSION CONTROL SYSTEM
            </p>
            <p className="reveal reveal-3 mt-6 max-w-xl text-base leading-relaxed text-ink/85 md:text-lg">
              Find places on Earth that resemble the Moon and Mars, compare them side by side, and see
              where each one falls short. Built to help plan field tests for lunar and Martian exploration.
            </p>
            <div className="reveal reveal-3 mt-8">
              <EnterButton />
            </div>
          </div>

          <DatasetReadout summary={summary} />
        </div>

        {/* Targets */}
        <section aria-labelledby="targets-heading" className="pb-4">
          <h2 id="targets-heading" className="mb-3 text-sm font-medium text-slate">
            Planetary targets
          </h2>
          <ul className="grid gap-3 sm:grid-cols-3">
            {TARGETS.map((t) => (
              <li key={t.id} className="group relative h-24 overflow-hidden rounded border border-slate/25 bg-panel md:h-28">
                <Image
                  src={t.image}
                  alt={t.alt}
                  fill
                  sizes="(min-width: 640px) 33vw, 100vw"
                  className="object-cover opacity-70 transition-opacity duration-300 group-hover:opacity-100"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-space/90 via-space/20 to-transparent" />
                <div className="absolute bottom-2 left-3 right-3 flex items-end justify-between">
                  <span className="text-sm font-medium text-ink">{t.name}</span>
                  <span className="font-mono text-xs text-slate">{t.body}</span>
                </div>
              </li>
            ))}
          </ul>
          <p className="mt-3 text-xs text-slate">
            Background and target images are AI-generated illustrations made with OpenArt. They are not
            real imagery and are not used for any measurement.
          </p>
        </section>
      </div>
    </main>
  );
}
