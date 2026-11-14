/**
 * Central place for every image used by the site.
 * To swap an image: replace the file in /public/images and keep the name,
 * or change the path here. Nothing else in the code needs to change.
 *
 * All images are AI-generated illustrations (OpenArt). They are visual
 * atmosphere only; never a source of coordinates or measurements.
 */
export const ASSETS = {
  heroBackground: "/images/mission-background.png",
  lunarSouthPole: "/images/lunar-south-pole.png",
  marsLandscape: "/images/mars-landscape.png",
  arsiaLavaTube: "/images/arsia-lava-tube.png",
} as const;

export const TARGETS = [
  {
    id: "lunar-south-pole",
    name: "Lunar South Pole",
    body: "Moon",
    image: ASSETS.lunarSouthPole,
    alt: "Illustration of long shadows across the cratered lunar south pole",
  },
  {
    id: "jezero-crater",
    name: "Jezero Crater",
    body: "Mars",
    image: ASSETS.marsLandscape,
    alt: "Illustration of a rust-colored Martian crater plain",
  },
  {
    id: "arsia-lava-tube",
    name: "Arsia Lava Tube",
    body: "Mars",
    image: ASSETS.arsiaLavaTube,
    alt: "Illustration of a collapsed skylight opening into a Martian lava tube",
  },
] as const;
