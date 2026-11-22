import React, { useState, useRef, useEffect, useCallback } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Layers, Calendar, Compass, ShieldAlert, Sparkles, CheckCircle2, Sliders } from 'lucide-react';
import { StudyArea, AnalysisResult } from '../types';

interface SplitSliderProps {
  selectedArea?: StudyArea | null;
  currentResult?: AnalysisResult | null;
  changeGeoJSON?: any;
  beforeDate?: string;
  afterDate?: string;
  beforeLabel?: string;
  afterLabel?: string;
}

export const SplitSlider: React.FC<SplitSliderProps> = ({
  selectedArea,
  currentResult,
  changeGeoJSON,
  beforeDate = "2023-03-10",
  afterDate = "2024-03-15",
  beforeLabel = "Baseline Scene (T1)",
  afterLabel = "Recent Observation (T2)"
}) => {
  const [sliderPos, setSliderPos] = useState(50);
  const [colorMode, setColorMode] = useState<'natural' | 'infrared' | 'change_mask'>('natural');
  const isDragging = useRef(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const leftMapContainerRef = useRef<HTMLDivElement>(null);
  const rightMapContainerRef = useRef<HTMLDivElement>(null);
  const leftMapRef = useRef<L.Map | null>(null);
  const rightMapRef = useRef<L.Map | null>(null);
  const leftLayersRef = useRef<L.LayerGroup | null>(null);
  const rightLayersRef = useRef<L.LayerGroup | null>(null);
  const isSyncingRef = useRef(false);

  // Initialize both maps
  useEffect(() => {
    if (!leftMapContainerRef.current || !rightMapContainerRef.current) return;
    if (leftMapRef.current || rightMapRef.current) return;

    const initialCenter: [number, number] = [28.61, 77.23];
    const initialZoom = 12;

    // Left Map (Baseline T1)
    const leftMap = L.map(leftMapContainerRef.current, {
      center: initialCenter,
      zoom: initialZoom,
      zoomControl: false,
      attributionControl: false
    });

    const esriLeft = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      attribution: 'Tiles &copy; Esri, Maxar'
    }).addTo(leftMap);

    const leftLayerGroup = L.layerGroup().addTo(leftMap);
    leftLayersRef.current = leftLayerGroup;
    leftMapRef.current = leftMap;

    // Right Map (Recent T2 + Changes)
    const rightMap = L.map(rightMapContainerRef.current, {
      center: initialCenter,
      zoom: initialZoom,
      zoomControl: true,
      attributionControl: false
    });

    const esriRight = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      attribution: 'Tiles &copy; Esri, Maxar'
    }).addTo(rightMap);

    const rightLayerGroup = L.layerGroup().addTo(rightMap);
    rightLayersRef.current = rightLayerGroup;
    rightMapRef.current = rightMap;

    // Synchronize panning & zooming between maps
    const syncMaps = (source: L.Map, target: L.Map) => {
      source.on('move', () => {
        if (isSyncingRef.current) return;
        isSyncingRef.current = true;
        target.setView(source.getCenter(), source.getZoom(), { animate: false });
        isSyncingRef.current = false;
      });
    };

    syncMaps(leftMap, rightMap);
    syncMaps(rightMap, leftMap);

    setTimeout(() => {
      leftMap.invalidateSize();
      rightMap.invalidateSize();
    }, 250);

    return () => {
      leftMap.remove();
      rightMap.remove();
      leftMapRef.current = null;
      rightMapRef.current = null;
    };
  }, []);

  // Update bounds & polygons when selectedArea or changeGeoJSON changes
  useEffect(() => {
    const leftMap = leftMapRef.current;
    const rightMap = rightMapRef.current;
    const leftGroup = leftLayersRef.current;
    const rightGroup = rightLayersRef.current;

    if (!leftMap || !rightMap || !leftGroup || !rightGroup) return;

    leftGroup.clearLayers();
    rightGroup.clearLayers();

    if (selectedArea && selectedArea.geometry) {
      // Baseline map shows the boundary outline
      const boundaryLayerLeft = L.geoJSON(selectedArea.geometry as any, {
        style: {
          color: '#38BDF8',
          weight: 2,
          opacity: 0.9,
          fillColor: '#0284C7',
          fillOpacity: 0.15,
          dashArray: '4, 4'
        }
      });
      boundaryLayerLeft.addTo(leftGroup);

      const boundaryLayerRight = L.geoJSON(selectedArea.geometry as any, {
        style: {
          color: '#38BDF8',
          weight: 2,
          opacity: 0.7,
          fillColor: 'transparent',
          dashArray: '4, 4'
        }
      });
      boundaryLayerRight.addTo(rightGroup);

      const bounds = boundaryLayerLeft.getBounds();
      leftMap.fitBounds(bounds, { padding: [30, 30], maxZoom: 14, animate: true });
      rightMap.fitBounds(bounds, { padding: [30, 30], maxZoom: 14, animate: true });
    }

    // Add Change Overlay to Right Map (T2)
    if (changeGeoJSON && changeGeoJSON.features) {
      const changeLayer = L.geoJSON(changeGeoJSON, {
        style: (feature) => {
          const mod = feature?.properties?.module || selectedArea?.module_type;
          let color = '#EA580C'; // Amber / Orange for rivers
          if (mod === 'forestguard') color = '#DC2626'; // Red for canopy loss
          if (mod === 'wetlandwatch') color = '#0284C7'; // Cyan for water loss
          if (mod === 'urbanwatch') color = '#7C3AED'; // Violet for sprawl
          return {
            color: color,
            weight: 2.5,
            opacity: 1,
            fillColor: color,
            fillOpacity: 0.55
          };
        },
        onEachFeature: (feature, layer) => {
          layer.bindPopup(`
            <div style="background:#FFFFFF; color:#0F172A; font-family:sans-serif; padding:10px; font-size:12px; border-radius:8px;">
              <strong style="color:#0284C7; font-size:13px;">${feature.properties?.label || 'Detected Change'}</strong><br/>
              <span style="color:#64748B;">Quantified Area:</span> <strong style="color:#EA580C;">${feature.properties?.area_ha || 'N/A'} ha</strong><br/>
              <span style="color:#64748B;">Confidence:</span> <strong style="color:#059669;">${((feature.properties?.confidence || 0.85) * 100).toFixed(0)}%</strong>
            </div>
          `);
        }
      });
      changeLayer.addTo(rightGroup);
    }

    setTimeout(() => {
      leftMap.invalidateSize();
      rightMap.invalidateSize();
    }, 200);
  }, [selectedArea, changeGeoJSON]);

  // Pointer drag listeners for slider divider
  const handlePointerDown = () => {
    isDragging.current = true;
  };

  const handlePointerUp = () => {
    isDragging.current = false;
  };

  const handlePointerMove = useCallback((e: React.PointerEvent<HTMLDivElement>) => {
    if (!isDragging.current || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const pct = Math.max(2, Math.min(98, (x / rect.width) * 100));
    setSliderPos(pct);
  }, []);

  // Filter styles for multi-spectral band visualization
  const getFilterStyle = () => {
    if (colorMode === 'infrared') {
      return 'hue-rotate(290deg) saturate(2.2) contrast(1.15)';
    }
    if (colorMode === 'change_mask') {
      return 'contrast(1.3) brightness(0.95)';
    }
    return 'none';
  };

  const actualBeforeDate = currentResult?.quality_metadata?.baseline_date || beforeDate;
  const actualAfterDate = currentResult?.quality_metadata?.recent_date || afterDate;
  const utmZone = currentResult?.quality_metadata?.projection_crs || 'EPSG:32643';
  const changeHa = currentResult?.total_change_ha;

  return (
    <div className="space-y-3">
      {/* Top Controls Header */}
      <div className="bg-white border border-slate-200 rounded-2xl p-3 flex flex-wrap items-center justify-between gap-3 shadow-sm">
        <div className="flex items-center space-x-2 text-xs">
          <span className="font-bold text-slate-800 flex items-center space-x-1.5">
            <Sliders className="w-4 h-4 text-emerald-600" />
            <span>DUAL SATELLITE TEMPORAL SLIDER</span>
          </span>
          <span className="text-[10px] bg-slate-100 text-slate-700 px-2 py-0.5 rounded-md font-mono border border-slate-200">
            {utmZone}
          </span>
        </div>

        {/* Multi-Spectral Band Mode Switcher */}
        <div className="flex items-center space-x-1 bg-slate-100 p-1 rounded-xl text-[11px] font-semibold">
          <button
            onClick={() => setColorMode('natural')}
            className={`px-2.5 py-1 rounded-lg transition ${
              colorMode === 'natural' 
                ? 'bg-white text-slate-900 shadow-sm border border-slate-200/80' 
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            True Color (RGB)
          </button>
          <button
            onClick={() => setColorMode('infrared')}
            className={`px-2.5 py-1 rounded-lg transition ${
              colorMode === 'infrared' 
                ? 'bg-white text-emerald-800 shadow-sm border border-slate-200/80' 
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            False Color CIR (NIR)
          </button>
          <button
            onClick={() => setColorMode('change_mask')}
            className={`px-2.5 py-1 rounded-lg transition ${
              colorMode === 'change_mask' 
                ? 'bg-white text-orange-700 shadow-sm border border-slate-200/80' 
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Change Vector Mask
          </button>
        </div>
      </div>

      {/* Main Split Viewport */}
      <div 
        ref={containerRef}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
        onPointerLeave={handlePointerUp}
        className="relative w-full h-[580px] rounded-2xl overflow-hidden border border-slate-200 select-none bg-slate-900 shadow-md"
      >
        {/* Right Map (T2 Recent Observation + Change Mask) */}
        <div 
          ref={rightMapContainerRef}
          style={{ filter: getFilterStyle() }}
          className="absolute inset-0 w-full h-full z-0"
        />

        {/* Left Map (T1 Baseline Scene) with Horizontal Clip Path */}
        <div 
          style={{ 
            clipPath: `polygon(0 0, ${sliderPos}% 0, ${sliderPos}% 100%, 0 100%)`,
            filter: getFilterStyle()
          }}
          className="absolute inset-0 w-full h-full z-10 pointer-events-none"
        >
          <div 
            ref={leftMapContainerRef}
            className="w-full h-full pointer-events-auto"
          />
        </div>

        {/* Vertical Divider Slider Line */}
        <div 
          className="absolute top-0 bottom-0 w-1 bg-white shadow-[0_0_12px_rgba(0,0,0,0.5)] z-20 pointer-events-none"
          style={{ left: `${sliderPos}%` }}
        >
          {/* Draggable Center Grab Handle */}
          <div 
            onPointerDown={handlePointerDown}
            className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-9 h-9 rounded-full bg-white border-2 border-emerald-600 flex items-center justify-center shadow-2xl cursor-ew-resize pointer-events-auto hover:scale-110 active:scale-95 transition"
          >
            <div className="flex space-x-1">
              <span className="w-0.5 h-3.5 bg-emerald-600 rounded-full"></span>
              <span className="w-0.5 h-3.5 bg-emerald-600 rounded-full"></span>
            </div>
          </div>
        </div>

        {/* Floating Label: Left (Baseline Scene) */}
        <div className="absolute top-4 left-4 z-30 bg-white/95 backdrop-blur-md px-3.5 py-2 rounded-xl border border-slate-200/90 text-xs shadow-md pointer-events-none">
          <div className="flex items-center space-x-1.5 text-slate-500 font-semibold text-[10px] uppercase tracking-wider">
            <Calendar className="w-3 h-3 text-sky-600" />
            <span>{beforeLabel}</span>
          </div>
          <div className="font-black text-slate-900 mt-0.5">
            {actualBeforeDate}
          </div>
          <div className="text-[10px] text-slate-500 font-mono">
            Sentinel-2 L2A &bull; Cloud 1.2%
          </div>
        </div>

        {/* Floating Label: Right (Recent Observation) */}
        <div className="absolute top-4 right-4 z-30 bg-white/95 backdrop-blur-md px-3.5 py-2 rounded-xl border border-slate-200/90 text-xs shadow-md pointer-events-none text-right">
          <div className="flex items-center justify-end space-x-1.5 text-emerald-700 font-semibold text-[10px] uppercase tracking-wider">
            <span>{afterLabel}</span>
            <Sparkles className="w-3 h-3 text-emerald-600" />
          </div>
          <div className="font-black text-slate-900 mt-0.5">
            {actualAfterDate}
          </div>
          <div className="text-[10px] text-slate-500 font-mono">
            Sentinel-2 L2A &bull; Change Overlaid
          </div>
        </div>

        {/* Bottom Status HUD */}
        <div className="absolute bottom-4 left-4 right-4 z-30 bg-slate-950/85 backdrop-blur-md px-4 py-2.5 rounded-xl border border-slate-700 text-white text-xs flex flex-wrap items-center justify-between gap-3 shadow-2xl pointer-events-none">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="font-semibold text-slate-200">
              {selectedArea ? `${selectedArea.name} (${selectedArea.state})` : 'Target Area Selected'}
            </span>
            <span className="text-slate-400">&bull;</span>
            <span className="text-slate-300 font-mono text-[11px]">
              Drag center slider to inspect temporal delta
            </span>
          </div>

          {changeHa !== undefined && (
            <div className="flex items-center space-x-2 bg-emerald-950/90 border border-emerald-500/50 px-3 py-1 rounded-lg">
              <span className="text-[11px] text-emerald-300 font-medium">Detected Change:</span>
              <strong className="text-sm font-black text-white">{changeHa} ha</strong>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};