"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight } from "lucide-react";

/** Plays a short iris transition, then opens the dashboard. */
export function EnterButton() {
  const router = useRouter();
  const [leaving, setLeaving] = useState(false);

  function handleEnter() {
    if (leaving) return;
    setLeaving(true);
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.setTimeout(() => router.push("/mission-control"), reduce ? 0 : 650);
  }

  return (
    <>
      <button
        type="button"
        onClick={handleEnter}
        disabled={leaving}
        className="group inline-flex items-center gap-3 rounded-sm bg-gold px-6 py-3.5 text-sm font-semibold tracking-wide text-space transition-colors hover:bg-[#f0c874] disabled:opacity-80"
      >
        ENTER MISSION CONTROL
        <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" aria-hidden />
      </button>
      {leaving && (
        <div aria-hidden className="iris fixed inset-0 z-50 bg-space">
          <div className="absolute inset-x-0 bottom-[15%] text-center font-mono text-xs tracking-[0.3em] text-cyan">
            ESTABLISHING LINK
          </div>
        </div>
      )}
    </>
  );
}
