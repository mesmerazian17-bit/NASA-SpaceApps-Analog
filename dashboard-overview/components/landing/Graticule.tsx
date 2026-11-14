/** Faint coordinate grid and crosshair. Purely decorative, static, no JS. */
export function Graticule() {
  return (
    <svg aria-hidden className="pointer-events-none absolute inset-0 -z-[5] h-full w-full opacity-[0.18]" preserveAspectRatio="none">
      <defs>
        <pattern id="grid" width="120" height="120" patternUnits="userSpaceOnUse">
          <path d="M120 0H0V120" fill="none" stroke="#52D6E8" strokeWidth="0.6" />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#grid)" />
    </svg>
  );
}
