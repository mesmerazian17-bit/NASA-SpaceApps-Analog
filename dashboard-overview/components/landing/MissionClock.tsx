"use client";

import { useEffect, useState } from "react";

/** Live UTC clock. Renders after mount to avoid a server/client mismatch. */
export function MissionClock() {
  const [now, setNow] = useState<Date | null>(null);

  useEffect(() => {
    setNow(new Date());
    const id = window.setInterval(() => setNow(new Date()), 1000);
    return () => window.clearInterval(id);
  }, []);

  const date = now ? now.toISOString().slice(0, 10) : "----------";
  const time = now ? now.toISOString().slice(11, 19) : "--:--:--";

  return (
    <div className="text-right font-mono text-xs text-slate" aria-label="Current UTC time">
      <div>{date}</div>
      <div className="mt-1 text-sm text-ink">{time} UTC</div>
    </div>
  );
}
