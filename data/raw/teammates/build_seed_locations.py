#!/usr/bin/env python3
"""Build data/seed_locations.csv: 85 terrestrial Moon/Mars analog candidate sites.

Categories (site_id prefix):
  BM  5 classic NASA validation benchmarks   (is_benchmark=True)
 SEA 20 Indonesian / Southeast Asian micro-analogs
  GL 30 global arid / volcanic / impact sites
  PL 30 polar / permafrost / subsurface sites

NOTE: lat/lon are representative points for each feature (summit, crater centre,
valley floor, cave entrance region), accurate to roughly 1-3 km. distance_to_road_km
and is_protected_area are analyst estimates from general knowledge of each site; refine
them against OpenStreetMap (roads) and WDPA/Protected Planet (protected areas) before
using them for quantitative site-selection scoring.
"""
import csv
from pathlib import Path

# (name, region, lat, lon, terrain_type, distance_to_road_km, is_protected_area)
BENCHMARKS = [
    ("Atacama Desert (Yungay)", "Chile", -24.10, -70.00, "hyperarid_desert", 20.0, False),
    ("Haughton Impact Crater, Devon Island", "Nunavut, Canada", 75.38, -89.68, "impact_crater_polar_desert", 350.0, False),
    ("Mauna Kea Summit", "Hawaii, USA", 19.82, -155.47, "volcanic_cinder_summit", 0.5, True),
    ("Stefansh\u00e9llir Lava Cave (Hallmundarhraun)", "Iceland", 64.77, -20.87, "lava_tube_basaltic", 2.0, True),
    ("Mojave Desert (Amboy Crater)", "California, USA", 34.56, -115.78, "volcanic_cinder_cone_desert", 1.5, True),
]

SEA = [
    ("Mount Tambora Caldera", "Sumbawa, Indonesia", -8.25, 118.00, "caldera_floor", 8.0, True),
    ("Mount Tambora Pyroclastic Slopes", "Sumbawa, Indonesia", -8.33, 118.00, "pyroclastic_slope", 3.0, True),
    ("Mount Bromo Sea of Sand", "East Java, Indonesia", -7.96, 112.95, "volcanic_sand_plain", 1.0, True),
    ("Kawah Ijen Crater", "East Java, Indonesia", -8.06, 114.24, "acidic_crater_lake_solfatara", 3.0, True),
    ("Mount Rinjani Caldera (Segara Anak)", "Lombok, Indonesia", -8.41, 116.46, "caldera_lake", 10.0, True),
    ("Gunung Sewu Karst Caves (Jomblang)", "Yogyakarta, Indonesia", -8.00, 110.65, "tropical_karst_cave", 1.0, False),
    ("Merapi Pyroclastic Plains (Gendol)", "Central Java, Indonesia", -7.60, 110.47, "pyroclastic_flow_plain", 2.0, True),
    ("Anak Krakatau", "Sunda Strait, Indonesia", -6.10, 105.42, "young_volcanic_island", 40.0, True),
    ("Mount Semeru Pyroclastic Flows", "East Java, Indonesia", -8.15, 112.93, "pyroclastic_flow_plain", 4.0, True),
    ("Dieng Plateau Craters (Sikidang)", "Central Java, Indonesia", -7.21, 109.91, "fumarolic_volcanic_plateau", 0.3, False),
    ("Mount Sinabung", "North Sumatra, Indonesia", 3.17, 98.39, "stratovolcano_lava_dome", 3.0, False),
    ("Toba Caldera (Samosir)", "North Sumatra, Indonesia", 2.68, 98.88, "supervolcano_caldera", 1.0, False),
    ("Kelud Crater", "East Java, Indonesia", -7.93, 112.31, "crater_lake_volcano", 2.0, False),
    ("Kelimutu Crater Lakes", "Flores, Indonesia", -8.77, 121.82, "tricolor_crater_lakes", 1.0, True),
    ("Taal Volcano Island", "Luzon, Philippines", 14.00, 120.99, "maar_crater_island", 6.0, True),
    ("Mayon Volcano", "Luzon, Philippines", 13.26, 123.69, "stratovolcano_pyroclastic", 3.0, True),
    ("Mount Pinatubo Caldera", "Luzon, Philippines", 15.14, 120.35, "caldera_lahar_deposits", 10.0, True),
    ("Son Doong Cave", "Quang Binh, Vietnam", 17.45, 106.29, "giant_karst_cave", 15.0, True),
    ("Deer Cave, Gunung Mulu", "Sarawak, Malaysia", 4.03, 114.81, "tropical_karst_cave", 3.0, True),
    ("Batur Caldera", "Bali, Indonesia", -8.24, 115.38, "caldera_lava_field", 0.5, False),
]

GLOBAL = [
    ("Pamir Plateau (Murghab)", "Tajikistan", 38.17, 73.96, "high_altitude_cold_desert", 1.0, False),
    ("Lut Desert (Shahdad Kaluts)", "Iran", 30.45, 57.75, "hyperarid_yardang_field", 8.0, True),
    ("Erta Ale Lava Lake", "Afar, Ethiopia", 13.60, 40.67, "basaltic_shield_lava_lake", 90.0, False),
    ("Namib Gravel Plains", "Namibia", -23.50, 15.20, "gravel_plain_desert", 3.0, True),
    ("Puna de Atacama (Salar de Antofalla)", "Argentina", -25.60, -67.65, "high_altitude_salar_volcanic", 25.0, False),
    ("Pinacate Volcanic Field", "Sonora, Mexico", 31.77, -113.50, "volcanic_field_maar_craters", 8.0, True),
    ("Dallol Hydrothermal Field", "Afar, Ethiopia", 14.24, 40.30, "hydrothermal_salt_plain", 40.0, False),
    ("Salar de Uyuni", "Bolivia", -20.13, -67.49, "salt_flat", 5.0, False),
    ("Trou au Natron, Tibesti", "Chad", 20.97, 16.55, "volcanic_caldera_desert", 120.0, False),
    ("Aorounga Impact Structure", "Chad", 19.10, 19.25, "eroded_impact_structure", 200.0, False),
    ("Wolfe Creek Crater", "Western Australia", -19.17, 127.80, "impact_crater_desert", 1.0, True),
    ("Barringer (Meteor) Crater", "Arizona, USA", 35.03, -111.02, "simple_impact_crater", 0.3, False),
    ("Ries Crater", "Bavaria, Germany", 48.88, 10.57, "complex_impact_crater", 0.5, False),
    ("Lonar Crater", "Maharashtra, India", 19.98, 76.51, "basaltic_impact_crater_lake", 0.5, True),
    ("Gosses Bluff (Tnorala)", "Northern Territory, Australia", -23.82, 132.30, "complex_impact_structure", 2.0, True),
    ("Vredefort Dome", "South Africa", -27.00, 27.50, "impact_structure_dome", 1.0, True),
    ("Wadi Rum", "Jordan", 29.58, 35.42, "sandstone_desert_canyon", 3.0, True),
    ("White Desert", "Egypt", 27.30, 28.17, "chalk_yardang_desert", 2.0, True),
    ("Askja Caldera", "Iceland", 65.03, -16.75, "caldera_basaltic_desert", 3.0, True),
    ("Kau Desert", "Hawaii, USA", 19.30, -155.35, "volcanic_ash_desert", 5.0, True),
    ("Richat Structure", "Mauritania", 21.12, -11.40, "eroded_dome_sahara", 20.0, False),
    ("Taklamakan Desert", "Xinjiang, China", 38.90, 83.50, "dune_sea_desert", 5.0, False),
    ("Gurvan Saikhan, Gobi", "Mongolia", 43.50, 102.30, "cold_desert_mountains", 30.0, True),
    ("Rio Tinto Acid River", "Andalusia, Spain", 37.72, -6.55, "acidic_iron_sulfate_terrain", 0.5, False),
    ("Mount Etna Summit", "Sicily, Italy", 37.75, 14.99, "basaltic_stratovolcano", 4.0, True),
    ("Timanfaya Volcanic Field", "Lanzarote, Spain", 29.00, -13.75, "basaltic_lava_field", 1.0, True),
    ("Atakor Volcanic Massif, Hoggar", "Algeria", 23.30, 5.55, "volcanic_massif_desert", 30.0, True),
    ("Ubehebe Crater", "California, USA", 36.31, -117.45, "maar_crater_desert", 0.5, True),
    ("Badwater Basin, Death Valley", "California, USA", 36.23, -116.77, "salt_flat_basin", 0.1, True),
    ("Flaming Mountains, Turpan", "Xinjiang, China", 42.88, 89.55, "red_sandstone_badlands", 2.0, False),
]

POLAR = [
    ("Bockfjorden Volcanic Complex (Sverrefjellet)", "Svalbard, Norway", 79.40, 13.50, "polar_basaltic_volcano", 100.0, True),
    ("Adventdalen Permafrost", "Svalbard, Norway", 78.19, 16.05, "continuous_permafrost_valley", 0.5, False),
    ("Wright Valley, McMurdo Dry Valleys", "Antarctica", -77.52, 161.80, "polar_desert_valley", 100.0, True),
    ("Taylor Valley, McMurdo Dry Valleys", "Antarctica", -77.62, 163.00, "polar_desert_valley", 90.0, True),
    ("Beacon Valley Buried Ice", "Antarctica", -77.83, 160.65, "buried_glacier_ice_polar_desert", 110.0, True),
    ("Victoria Valley, McMurdo Dry Valleys", "Antarctica", -77.33, 162.00, "polar_desert_dunes", 120.0, True),
    ("Haughton Crater Eastern Rim, Devon Island", "Nunavut, Canada", 75.38, -89.27, "impact_crater_rim_polar_desert", 340.0, False),
    ("Kazumura Lava Tube", "Hawaii, USA", 19.49, -155.08, "lava_tube_basaltic", 1.0, False),
    ("Mount Erebus Ice Caves", "Antarctica", -77.53, 167.15, "volcanic_fumarolic_ice_caves", 40.0, True),
    ("Disko Island Basalts (Qeqertarsuaq)", "Greenland", 69.25, -53.50, "arctic_flood_basalt", 10.0, False),
    ("Expedition Fiord, Axel Heiberg Island", "Nunavut, Canada", 79.38, -90.75, "polar_gypsum_cold_springs", 500.0, False),
    ("Lake Hazen Region", "Nunavut, Canada", 81.80, -71.30, "high_arctic_polar_desert", 650.0, True),
    ("Pingualuit Crater", "Quebec, Canada", 61.28, -73.67, "arctic_impact_crater_lake", 130.0, True),
    ("Batagaika Megaslump", "Yakutia, Russia", 67.58, 134.77, "thermokarst_ice_rich_permafrost", 8.0, False),
    ("Lake Vida", "Antarctica", -77.38, 161.93, "hypersaline_ice_sealed_lake", 110.0, True),
    ("Blood Falls, Taylor Glacier", "Antarctica", -77.72, 162.27, "subglacial_brine_outflow", 85.0, True),
    ("Mount Melbourne", "Antarctica", -74.35, 164.70, "polar_stratovolcano_fumaroles", 300.0, True),
    ("Deception Island Caldera", "Antarctica", -62.97, -60.65, "flooded_caldera_pyroclastic", 800.0, True),
    ("Utqia\u0121vik Permafrost", "Alaska, USA", 71.29, -156.77, "arctic_coastal_polygon_ground", 1.0, False),
    ("CRREL Permafrost Tunnel", "Alaska, USA", 64.95, -147.62, "subsurface_permafrost_tunnel", 0.5, False),
    ("Tuktoyaktuk Pingos", "NWT, Canada", 69.45, -133.00, "pingo_ground_ice", 2.0, True),
    ("Kverkfj\u00f6ll Ice Caves", "Iceland", 64.65, -16.72, "geothermal_subglacial_caves", 5.0, True),
    ("Holuhraun Lava Field", "Iceland", 64.85, -16.80, "recent_basaltic_lava_field", 6.0, True),
    ("Surtsey", "Iceland", 63.30, -20.60, "young_volcanic_island", 20.0, True),
    ("Beerenberg, Jan Mayen", "Norway", 71.08, -8.17, "arctic_volcano_glaciated", 10.0, True),
    ("Tanggula Permafrost, Tibetan Plateau", "Tibet, China", 33.07, 91.93, "alpine_permafrost_plateau", 1.0, False),
    ("Ny-\u00c5lesund / Br\u00f8gger Peninsula", "Svalbard, Norway", 78.92, 11.93, "high_arctic_periglacial", 0.5, True),
    ("Mutnovsky Volcano", "Kamchatka, Russia", 52.45, 158.20, "fumarolic_volcano_glacier", 12.0, True),
    ("Schirmacher Oasis", "Antarctica", -70.75, 11.65, "polar_oasis_periglacial", 0.5, False),
    ("Lake Untersee", "Antarctica", -71.35, 13.45, "perennially_ice_covered_lake", 80.0, False),
]

HEADER = ["site_id", "name", "region", "lat", "lon", "is_benchmark",
          "terrain_type", "distance_to_road_km", "is_protected_area"]


def build_rows():
    rows = []
    for prefix, sites, bench in (("BM", BENCHMARKS, True), ("SEA", SEA, False),
                                 ("GL", GLOBAL, False), ("PL", POLAR, False)):
        for i, (name, region, lat, lon, terrain, road, prot) in enumerate(sites, 1):
            rows.append({
                "site_id": f"{prefix}-{i:02d}", "name": name, "region": region,
                "lat": round(lat, 4), "lon": round(lon, 4), "is_benchmark": bench,
                "terrain_type": terrain, "distance_to_road_km": road,
                "is_protected_area": prot,
            })
    return rows


def validate(rows):
    assert len(BENCHMARKS) == 5 and len(SEA) == 20 and len(GLOBAL) == 30 and len(POLAR) == 30, "category counts"
    assert len(rows) == 85, f"expected 85 rows, got {len(rows)}"
    assert len({r["site_id"] for r in rows}) == 85, "duplicate site_id"
    assert len({r["name"] for r in rows}) == 85, "duplicate name"
    for r in rows:
        assert -90 <= r["lat"] <= 90 and -180 <= r["lon"] <= 180, f"bad coords: {r['site_id']}"
        assert r["distance_to_road_km"] >= 0


def main():
    rows = build_rows()
    validate(rows)
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
    out = PROJECT_ROOT / "data" / "seed_locations.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} sites to {out}")


if __name__ == "__main__":
    main()
