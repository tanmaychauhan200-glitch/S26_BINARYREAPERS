import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import { Search, MapPin, Sparkles, X, Activity, Compass, Globe } from 'lucide-react';
import { StudyArea } from '../types';
import { api } from '../services/api';

interface MapCanvasProps {
  selectedArea?: StudyArea | null;
  changeGeoJSON?: any;
  onPointInspect?: (pointData: any) => void;
}

export const MapCanvas: React.FC<MapCanvasProps> = ({
  selectedArea,
  changeGeoJSON,
  onPointInspect
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const layerGroupRef = useRef<L.LayerGroup | null>(null);
  const markerGroupRef = useRef<L.LayerGroup | null>(null);

  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [activePoint, setActivePoint] = useState<any>(null);
  const [isInspectingPoint, setIsInspectingPoint] = useState(false);

  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    // Default center on India
    const map = L.map(mapContainerRef.current, {
      center: [22.5, 78.9],
      zoom: 5,
      zoomControl: true,
      attributionControl: false
    });

    // 1. ESRI World Imagery (High-Res Real Earth Observation Satellite)
    const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      attribution: 'Tiles &copy; Esri, Maxar, Earthstar Geographics'
    });

    // 2. ESRI National Geographic World Topo (Clean, scientific NGO style)
    const esriTopo = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 18,
      attribution: 'Tiles &copy; Esri &mdash; National Geographic, DeLorme, NAVTEQ'
    });

    // 3. OpenStreetMap Standard
    const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    });

    // Default to real satellite imagery
    esriSatellite.addTo(map);

    L.control.layers({
      "🛰️ High-Res Satellite": esriSatellite,
      "🏔️ Topographic Research Map": esriTopo,
      "🗺️ OpenStreetMap": osm
    }, undefined, { position: 'topright' }).addTo(map);

    const layerGroup = L.layerGroup().addTo(map);
    const markerGroup = L.layerGroup().addTo(map);
    layerGroupRef.current = layerGroup;
    markerGroupRef.current = markerGroup;
    mapInstanceRef.current = map;

    // Map click handler to inspect ANY point in India
    map.on('click', async (e: L.LeafletMouseEvent) => {
      const { lat, lng } = e.latlng;
      markerGroup.clearLayers();

      const customPulseIcon = L.divIcon({
        className: 'custom-pulse-marker',
        html: `
          <div style="position:relative; width:28px; height:28px; transform:translate(-50%, -50%);">
            <div style="position:absolute; inset:0; border-radius:50%; background:rgba(5,150,105,0.35); animation:ping 1.5s cubic-bezier(0,0,0.2,1) infinite;"></div>
            <div style="position:absolute; inset:5px; border-radius:50%; background:#059669; border:2.5px solid #ffffff; box-shadow:0 2px 8px rgba(0,0,0,0.3);"></div>
          </div>
        `,
        iconSize: [28, 28]
      });

      L.marker([lat, lng], { icon: customPulseIcon }).addTo(markerGroup);

      setIsInspectingPoint(true);
      try {
        const pointData = await api.inspectPoint(lat, lng);
        setActivePoint(pointData);
        if (onPointInspect) {
          onPointInspect(pointData);
        }
      } catch (err) {
        console.error("Point inspection failed:", err);
      } finally {
        setIsInspectingPoint(false);
      }
    });

    setTimeout(() => {
      map.invalidateSize();
    }, 250);

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  // Update map viewport & overlay when selectedArea changes
  useEffect(() => {
    const map = mapInstanceRef.current;
    const layerGroup = layerGroupRef.current;
    if (!map || !layerGroup) return;

    layerGroup.clearLayers();

    if (selectedArea && selectedArea.geometry) {
      const geoLayer = L.geoJSON(selectedArea.geometry as any, {
        style: {
          color: '#0284C7',
          weight: 2.5,
          opacity: 0.95,
          fillColor: '#38BDF8',
          fillOpacity: 0.25,
          dashArray: '6, 6'
        }
      });
      geoLayer.addTo(layerGroup);
      map.invalidateSize();
      map.fitBounds(geoLayer.getBounds(), { padding: [50, 50], maxZoom: 13, animate: true });
    }

    if (changeGeoJSON && changeGeoJSON.features) {
      const changeLayer = L.geoJSON(changeGeoJSON, {
        style: (feature) => {
          const mod = feature?.properties?.module;
          let color = '#D97706'; // Amber default
          if (mod === 'forestguard') color = '#DC2626'; // Red
          if (mod === 'urbanwatch') color = '#7C3AED'; // Violet
          return {
            color: color,
            weight: 2.5,
            opacity: 1,
            fillColor: color,
            fillOpacity: 0.45
          };
        },
        onEachFeature: (feature, layer) => {
          layer.bindPopup(`
            <div style="background:#FFFFFF; color:#0F172A; font-family:sans-serif; padding:10px; font-size:12px; border:1px solid #E2E8F0; border-radius:8px; box-shadow:0 4px 14px rgba(0,0,0,0.12);">
              <strong style="color:#0284C7; font-size:13px;">${feature.properties?.label || 'Disturbance'}</strong><br/>
              <span style="color:#64748B;">Affected Extent:</span> <strong style="color:#D97706;">${feature.properties?.area_ha || 'N/A'} ha</strong><br/>
              <span style="color:#64748B;">Scientific Confidence:</span> <strong style="color:#059669;">${(feature.properties?.confidence * 100).toFixed(0)}%</strong>
            </div>
          `);
        }
      });
      changeLayer.addTo(layerGroup);
    }
  }, [selectedArea, changeGeoJSON]);

  // Handle Location Search
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    try {
      const results = await api.searchLocation(searchQuery);
      setSearchResults(results);
    } catch (err) {
      console.error("Search error:", err);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSelectLocation = (loc: any) => {
    const map = mapInstanceRef.current;
    if (!map) return;
    map.flyTo([loc.lat, loc.lon], 13, { duration: 1.8 });
    setSearchResults([]);
    setSearchQuery(loc.display_name.split(',')[0]);

    if (markerGroupRef.current) {
      markerGroupRef.current.clearLayers();
      const customPulseIcon = L.divIcon({
        className: 'custom-pulse-marker',
        html: `
          <div style="position:relative; width:28px; height:28px; transform:translate(-50%, -50%);">
            <div style="position:absolute; inset:0; border-radius:50%; background:rgba(5,150,105,0.35); animation:ping 1.5s cubic-bezier(0,0,0.2,1) infinite;"></div>
            <div style="position:absolute; inset:5px; border-radius:50%; background:#059669; border:2.5px solid #ffffff; box-shadow:0 2px 8px rgba(0,0,0,0.3);"></div>
          </div>
        `,
        iconSize: [28, 28]
      });
      L.marker([loc.lat, loc.lon], { icon: customPulseIcon }).addTo(markerGroupRef.current);
    }

    api.inspectPoint(loc.lat, loc.lon).then((data) => {
      setActivePoint(data);
      if (onPointInspect) onPointInspect(data);
    });
  };

  return (
    <div className="relative w-full h-[560px] rounded-2xl overflow-hidden border border-slate-200 shadow-md bg-slate-100">
      
      {/* Search Bar Floating at Top Left */}
      <div className="absolute top-4 left-4 z-[1000] w-72 sm:w-96">
        <form onSubmit={handleSearch} className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search any river, city or forest in India..."
            className="w-full bg-white/95 backdrop-blur-md border border-slate-300 focus:border-emerald-500 rounded-xl pl-9 pr-8 py-2 text-xs font-sans text-slate-800 placeholder:text-slate-400 focus:outline-none shadow-md"
          />
          <Search className="w-4 h-4 text-emerald-600 absolute left-2.5 top-2.5" />
          {searchQuery && (
            <button 
              type="button" 
              onClick={() => { setSearchQuery(''); setSearchResults([]); }}
              className="absolute right-2.5 top-2.5 text-slate-400 hover:text-slate-600"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </form>

        {/* Autocomplete Dropdown */}
        {searchResults.length > 0 && (
          <div className="mt-1 bg-white border border-slate-200 rounded-xl overflow-hidden shadow-xl divide-y divide-slate-100 max-h-56 overflow-y-auto">
            {searchResults.map((res, i) => (
              <div
                key={i}
                onClick={() => handleSelectLocation(res)}
                className="p-2.5 hover:bg-emerald-50 cursor-pointer text-xs transition flex items-center space-x-2"
              >
                <MapPin className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                <span className="text-slate-800 truncate font-medium">{res.display_name}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Main Map DOM */}
      <div ref={mapContainerRef} className="w-full h-full z-0 cursor-crosshair" />

      {/* Floating Point Inspection HUD */}
      {activePoint && (
        <div className="absolute top-16 left-4 z-[1000] w-80 bg-white/95 backdrop-blur-md border border-slate-200 rounded-2xl p-4 shadow-xl space-y-2.5 animate-fadeIn">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2">
            <div className="flex items-center space-x-1.5 text-xs font-bold text-emerald-700">
              <Globe className="w-4 h-4 text-emerald-600" />
              <span>POINT GEODATA INSPECTOR</span>
            </div>
            <button 
              onClick={() => setActivePoint(null)}
              className="text-slate-400 hover:text-slate-600 text-xs"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>

          <div>
            <span className="text-[10px] uppercase font-bold text-slate-600 block">Territory & Jurisdiction</span>
            <p className="text-xs font-bold text-slate-900 truncate">
              {activePoint.location?.suburb || activePoint.location?.district || "Selected Point"}, {activePoint.location?.state}
            </p>
            <p className="text-[10px] text-slate-500 font-mono mt-0.5">
              {activePoint.coordinates?.latitude}°N, {activePoint.coordinates?.longitude}°E &bull; {activePoint.spatial_reference?.utm_zone}
            </p>
          </div>

          <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-200 space-y-1">
            <span className="text-[10px] font-bold text-slate-600 block uppercase">Classified Surface Cover</span>
            <span className="text-xs font-bold text-emerald-700 block">
              {activePoint.classification?.primary_surface_type}
            </span>
            <span className="text-[10px] text-slate-600 block leading-tight">
              {activePoint.classification?.vulnerability_assessment}
            </span>
          </div>

          {/* Spectral Gauges */}
          <div className="grid grid-cols-3 gap-1.5 text-center font-mono text-[10px] pt-1">
            <div className="bg-emerald-50 p-1.5 rounded-lg border border-emerald-200">
              <span className="text-emerald-700 block font-sans font-bold">NDVI</span>
              <span className="text-emerald-900 font-bold">{activePoint.spectral_indices?.ndvi}</span>
            </div>
            <div className="bg-sky-50 p-1.5 rounded-lg border border-sky-200">
              <span className="text-sky-700 block font-sans font-bold">MNDWI</span>
              <span className="text-sky-900 font-bold">{activePoint.spectral_indices?.mndwi}</span>
            </div>
            <div className="bg-amber-50 p-1.5 rounded-lg border border-amber-200">
              <span className="text-amber-700 block font-sans font-bold">NDBI</span>
              <span className="text-amber-900 font-bold">{activePoint.spectral_indices?.ndbi}</span>
            </div>
          </div>
        </div>
      )}

      {/* Floating Bottom Left Telemetry */}
      <div className="absolute bottom-4 left-4 z-[1000] bg-white/95 backdrop-blur-md border border-slate-200 px-3 py-1.5 rounded-xl text-xs font-medium text-slate-700 shadow-sm pointer-events-none flex items-center space-x-2">
        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        <span>Click anywhere on the map to analyze coordinates</span>
      </div>

      {/* Legend Badge */}
      <div className="absolute bottom-4 right-4 z-[1000] bg-white/95 backdrop-blur-md border border-slate-200 px-3.5 py-2.5 rounded-xl text-[11px] font-medium text-slate-700 shadow-sm pointer-events-none space-y-1.5">
        <div className="flex items-center space-x-2">
          <span className="w-3.5 h-0.5 border-t-2 border-dashed border-sky-500"></span>
          <span>Study Area (AOI)</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-3 h-3 bg-amber-400/50 border border-amber-500 rounded-sm"></span>
          <span>Detected Spectral Change</span>
        </div>
      </div>
    </div>
  );
};
