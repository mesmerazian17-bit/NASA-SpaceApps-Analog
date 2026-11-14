"use client";
import "leaflet/dist/leaflet.css";
import { useEffect } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from "react-leaflet";
import type { Site } from "@/lib/data/types";

const DARK = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";
const SAT = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}";

function FlyTo({ site, zoom }: { site: Site | null; zoom: number }) {
  const map = useMap();
  useEffect(() => { if (site) map.flyTo([site.lat, site.lon], zoom, { duration: 1.4 }); }, [site, zoom, map]);
  return null;
}

interface Props { sites: Site[]; primary: Site | null; partner: Site | null; onSelect?: (id: string) => void; satellite?: boolean }

export default function MapView({ sites, primary, partner, onSelect, satellite }: Props) {
  const colorOf = (s: Site) =>
    s.site_id === primary?.site_id ? "#E7B85C" : s.site_id === partner?.site_id ? "#52D6E8" : s.is_benchmark ? "#8091A5" : "#E8EEF5";
  const shown = satellite ? (primary ? [primary] : []) : sites;
  return (
    <MapContainer center={[20, 0]} zoom={2} minZoom={2} worldCopyJump className="h-full w-full bg-space">
      <TileLayer url={satellite ? SAT : DARK}
        attribution={satellite ? "Imagery © Esri, Maxar, Earthstar Geographics" : "© OpenStreetMap, © CARTO"} />
      {shown.map((s) => {
        const sel = s.site_id === primary?.site_id || s.site_id === partner?.site_id;
        return (
          <CircleMarker key={s.site_id} center={[s.lat, s.lon]} radius={sel ? 9 : 5}
            pathOptions={{ color: colorOf(s), fillColor: colorOf(s), fillOpacity: sel ? 0.9 : 0.55, weight: sel ? 3 : 1 }}
            eventHandlers={{ click: () => onSelect?.(s.site_id) }}>
            <Popup>
              <b>{s.name}</b><br />{s.region}<br />
              <span style={{ fontFamily: "monospace" }}>{s.lat.toFixed(2)}, {s.lon.toFixed(2)} · {s.site_id}</span>
            </Popup>
          </CircleMarker>
        );
      })}
      <FlyTo site={primary} zoom={satellite ? 12 : 5} />
    </MapContainer>
  );
}
