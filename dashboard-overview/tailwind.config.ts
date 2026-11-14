import type { Config } from "tailwindcss";

// Palette comes straight from the website brief (section 2).
const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        space: "#080D16",
        navy: "#101A29",
        panel: "#121E2D",
        cyan: { DEFAULT: "#52D6E8" },
        gold: "#E7B85C",
        slate: { DEFAULT: "#8091A5" },
        ink: "#E8EEF5",
        warn: "#F2A65A",
        critical: "#E66A6A",
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
