import React, { useState, useEffect } from 'react';
import { 
  Play, 
  Download, 
  MapPin, 
  Calendar, 
  AlertTriangle, 
  CheckCircle2, 
  FileSpreadsheet,
  Sparkles,
  Compass,
  Globe,
  Leaf,
  Layers,
  ArrowRight
} from 'lucide-react';
import { Navbar } from './components/Navbar';
import { ModuleCard } from './components/ModuleCard';
import { SplitSlider } from './components/SplitSlider';
import { MapCanvas } from './maps/MapCanvas';
import { AIModal } from './components/AIModal';
import { api } from './services/api';
import { StudyArea, AnalysisJob, AnalysisResult, Alert, ProviderStatus, ModuleType } from './types';

export const App: React.FC = () => {
  const [activeModule, setActiveModule] = useState<ModuleType | 'overview'>('overview');
  const [studyAreas, setStudyAreas] = useState<StudyArea[]>([]);
  const [selectedArea, setSelectedArea] = useState<StudyArea | null>(null);
  const [providers, setProviders] = useState<ProviderStatus[]>([]);
  const [offlineMode, setOfflineMode] = useState<boolean>(true);
  const [currentJob, setCurrentJob] = useState<AnalysisJob | null>(null);
  const [currentResult, setCurrentResult] = useState<AnalysisResult | null>(null);
  const [changeVector, setChangeVector] = useState<any>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'map' | 'slider'>('map');

  // AI Analysis State
  const [aiReport, setAiReport] = useState<any>(null);
  const [isAiModalOpen, setIsAiModalOpen] = useState(false);
  const [isGeneratingAi, setIsGeneratingAi] = useState(false);
  const [inspectedPoint, setInspectedPoint] = useState<any>(null);

  // Load initial data
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [areasData, provData, alertsData] = await Promise.all([
          api.getStudyAreas(),
          api.getProvidersStatus(),
          api.getAlerts()
        ]);
        setStudyAreas(areasData);
        if (areasData.length > 0) {
          setSelectedArea(areasData[0]);
        }
        setProviders(provData.providers || []);
        setAlerts(alertsData);
      } catch (err) {
        console.error("Failed to fetch initial data:", err);
      }
    };
    loadInitialData();
  }, []);

  const handleSelectModule = (mod: ModuleType | 'overview') => {
    setActiveModule(mod);
    setCurrentResult(null);
    setChangeVector(null);
    setCurrentJob(null);
    if (mod !== 'overview') {
      const match = studyAreas.find(a => a.module_type === mod);
      if (match) setSelectedArea(match);
      setTimeout(() => {
        const workspaceEl = document.getElementById('operational-workspace');
        if (workspaceEl) {
          workspaceEl.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    }
  };

  // Run change analysis
  const handleRunAnalysis = async () => {
    if (!selectedArea) return;
    setIsRunning(true);
    try {
      const job = await api.runJob({
        module_type: selectedArea.module_type,
        study_area_id: selectedArea.id
      });
      setCurrentJob(job);

      const pollInterval = setInterval(async () => {
        try {
          const updatedJob = await api.getJob(job.id);
          setCurrentJob(updatedJob);
          if (updatedJob.status === 'COMPLETED' || updatedJob.status === 'FAILED') {
            clearInterval(pollInterval);
            setIsRunning(false);
            if (updatedJob.status === 'COMPLETED') {
              const [resData, vecData, newAlerts] = await Promise.all([
                api.getResult(job.id),
                api.getResultVector(job.id),
                api.getAlerts(selectedArea.module_type)
              ]);
              setCurrentResult(resData);
              setChangeVector(vecData);
              setAlerts(newAlerts);
              // Switch automatically to Before/After Temporal Slider to reveal the results
              setActiveTab('slider');
            }
          }
        } catch (e) {
          clearInterval(pollInterval);
          setIsRunning(false);
        }
      }, 1000);
    } catch (err) {
      console.error("Error executing job:", err);
      setIsRunning(false);
    }
  };

  // Trigger AI Analysis for either the study area or inspected point
  const handleTriggerAI = async (customPoint?: any) => {
    setIsGeneratingAi(true);
    try {
      const targetName = customPoint 
        ? `${customPoint.location?.suburb || customPoint.location?.district}, ${customPoint.location?.state}`
        : (selectedArea?.name || "Selected Indian Zone");
      
      const lat = customPoint?.coordinates?.latitude || 28.53;
      const lon = customPoint?.coordinates?.longitude || 77.29;
      const changeHa = currentResult?.total_change_ha || 18.4;
      const metrics = customPoint?.spectral_indices || currentResult?.summary_metrics || {};

      const report = await api.runAIAnalysis({
        module_type: selectedArea?.module_type || "riverwatch",
        area_name: targetName,
        latitude: lat,
        longitude: lon,
        spectral_metrics: metrics,
        total_change_ha: changeHa
      });

      setAiReport(report);
      setIsAiModalOpen(true);
    } catch (err) {
      console.error("AI Analysis failed:", err);
      alert("AI analysis could not complete. Please verify backend connection.");
    } finally {
      setIsGeneratingAi(false);
    }
  };

  const filteredAreas = activeModule === 'overview' 
    ? studyAreas 
    : studyAreas.filter(a => a.module_type === activeModule);

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-[#0F172A] flex flex-col font-sans selection:bg-emerald-500 selection:text-white">
      
      {/* AI Modal Drawer */}
      <AIModal 
        isOpen={isAiModalOpen}
        onClose={() => setIsAiModalOpen(false)}
        report={aiReport}
        areaName={selectedArea?.name || "Selected Region"}
      />

      {/* Top Navigation */}
      <Navbar 
        activeModule={activeModule}
        onSelectModule={handleSelectModule}
        providers={providers}
        offlineMode={offlineMode}
        onToggleOffline={() => setOfflineMode(!offlineMode)}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 space-y-6">
        
        {/* Landing Hero (Only in Overview mode) */}
        {activeModule === 'overview' && (
          <div className="relative rounded-3xl bg-white border border-slate-200/90 p-8 overflow-hidden shadow-sm">
            <div className="relative z-10 max-w-3xl space-y-3.5">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-800">
                <Leaf className="w-3.5 h-3.5 text-emerald-600" />
                <span>ENVIRONMENTAL INTELLIGENCE & CONSERVATION RESEARCH</span>
                <span className="w-1 h-1 rounded-full bg-emerald-400"></span>
                <span>INDIA OBSERVATORY</span>
              </div>
              <h1 className="text-3xl md:text-5xl font-black tracking-tight text-slate-900 font-sans leading-tight">
                Seeing Earth's Changes. <br/>
                <span className="text-emerald-600">
                  Protecting Tomorrow.
                </span>
              </h1>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed max-w-2xl font-sans">
                An open-access Earth Observation research platform providing spatial evidence for India's dynamic river systems, fragile wetlands, protected forest canopies, and peri-urban landscapes.
              </p>
            </div>
          </div>
        )}

        {/* 4 Pillars Grid (In Overview) */}
        {activeModule === 'overview' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <ModuleCard 
              id="riverwatch"
              title="RiverWatch"
              tagline="River Channel & Sediment Intelligence"
              description="Monitors dynamic river channel shifts, exposed sediment dynamics, and bank retreat along major Indian river corridors."
              accentColor="text-sky-700"
              borderColor="border-sky-200"
              badgeBg="bg-sky-50"
              badgeText="text-sky-800"
              keyMetricLabel="Corridor Focus"
              keyMetricValue="Yamuna / Delhi Reach"
              studyAreasCount={studyAreas.filter(a => a.module_type === 'riverwatch').length}
              onOpen={handleSelectModule}
            />
            <ModuleCard 
              id="wetlandwatch"
              title="WetlandWatch"
              tagline="Lakes & Waterbody Conservation"
              description="Evaluates seasonal water persistence, surface water shrinkage, and buffer preservation across declared Ramsar wetlands."
              accentColor="text-teal-700"
              borderColor="border-teal-200"
              badgeBg="bg-teal-50"
              badgeText="text-teal-800"
              keyMetricLabel="Ramsar Site"
              keyMetricValue="Deepor Beel (Assam)"
              studyAreasCount={studyAreas.filter(a => a.module_type === 'wetlandwatch').length}
              onOpen={handleSelectModule}
            />
            <ModuleCard 
              id="forestguard"
              title="ForestGuard"
              tagline="Canopy & Fragmentation Monitoring"
              description="Tracks spectral canopy disturbances, vegetation health metrics, and patch connectivity across protected Indian bio-reserves."
              accentColor="text-emerald-700"
              borderColor="border-emerald-200"
              badgeBg="bg-emerald-50"
              badgeText="text-emerald-800"
              keyMetricLabel="Ecological Focus"
              keyMetricValue="Western Ghats (Silent Valley)"
              studyAreasCount={studyAreas.filter(a => a.module_type === 'forestguard').length}
              onOpen={handleSelectModule}
            />
            <ModuleCard 
              id="urbanwatch"
              title="UrbanWatch"
              tagline="Impervious Sprawl & Buffer Analytics"
              description="Quantifies rapid built-up surface expansion and analyzes spatial encroachment trajectories toward agricultural and wetland buffers."
              accentColor="text-amber-700"
              borderColor="border-amber-200"
              badgeBg="bg-amber-50"
              badgeText="text-amber-800"
              keyMetricLabel="Peri-Urban Zone"
              keyMetricValue="Bengaluru Growth Corridor"
              studyAreasCount={studyAreas.filter(a => a.module_type === 'urbanwatch').length}
              onOpen={handleSelectModule}
            />
          </div>
        )}

        {/* Operational Workspace Grid */}
        <div id="operational-workspace" className="grid grid-cols-1 lg:grid-cols-12 gap-6 scroll-mt-20">
          
          {/* Left Column: Study Area Selection & Trigger (4 Cols) */}
          <div className="lg:col-span-4 space-y-4">
            
            {/* Study Area Control Box */}
            <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-4 shadow-sm">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-xs tracking-wider text-slate-900 flex items-center space-x-2">
                  <MapPin className="w-4 h-4 text-emerald-600" />
                  <span>TARGET STUDY AREA (AOI)</span>
                </h3>
                <span className="text-[10px] font-semibold bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded-full border border-emerald-200">
                  UTM Projected
                </span>
              </div>

              {/* Study Area Dropdown */}
              <div>
                <label className="text-xs text-slate-500 block mb-1.5 font-medium">Pre-Calibrated Benchmark Site</label>
                <select 
                  value={selectedArea?.id || ''}
                  onChange={(e) => {
                    const match = studyAreas.find(a => a.id === e.target.value);
                    if (match) {
                      setSelectedArea(match);
                      setCurrentResult(null);
                      setChangeVector(null);
                    }
                  }}
                  className="w-full bg-slate-50 border border-slate-200 focus:border-emerald-500 rounded-xl px-3 py-2.5 text-xs font-medium text-slate-800 focus:outline-none"
                >
                  {filteredAreas.map((area) => (
                    <option key={area.id} value={area.id}>
                      {area.name} ({area.state})
                    </option>
                  ))}
                </select>
              </div>

              {/* Area Metadata Card */}
              {selectedArea && (
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-2 text-xs">
                  <p className="text-slate-600 text-[11px] leading-relaxed">
                    {selectedArea.description}
                  </p>
                  <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-200 text-[11px]">
                    <div>
                      <span className="text-slate-500 block">Total Area:</span>
                      <strong className="text-slate-900">{selectedArea.area_ha.toLocaleString()} ha</strong>
                    </div>
                    <div>
                      <span className="text-slate-500 block">Jurisdiction:</span>
                      <strong className="text-slate-900 truncate block">{selectedArea.state}</strong>
                    </div>
                  </div>
                </div>
              )}

              {/* Observation Temporal Range */}
              <div className="space-y-2 pt-2 border-t border-slate-100">
                <div className="flex items-center justify-between text-xs text-slate-500">
                  <span className="flex items-center space-x-1.5">
                    <Calendar className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Observation Window</span>
                  </span>
                  <span className="text-emerald-700 font-semibold text-[10px]">Cloud &lt; 5%</span>
                </div>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                    <span className="text-[10px] text-slate-500 block font-medium">T1 Baseline</span>
                    <strong className="text-slate-800">2023-03-10</strong>
                  </div>
                  <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                    <span className="text-[10px] text-slate-500 block font-medium">T2 Current</span>
                    <strong className="text-emerald-700">2024-03-15</strong>
                  </div>
                </div>
              </div>

              {/* Execution Trigger */}
              <button
                onClick={handleRunAnalysis}
                disabled={isRunning}
                className={`w-full py-3 px-4 rounded-xl font-semibold text-xs flex items-center justify-center space-x-2 transition shadow-sm ${
                  isRunning 
                    ? 'bg-slate-200 text-slate-500 cursor-not-allowed'
                    : 'bg-emerald-600 hover:bg-emerald-700 text-white active:scale-98'
                }`}
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>{isRunning ? 'CALCULATING CHANGE INDICES...' : 'RUN CHANGE ASSESSMENT'}</span>
              </button>

              {/* Progress bar */}
              {isRunning && currentJob && (
                <div className="space-y-1">
                  <div className="flex justify-between text-[11px] font-medium text-slate-500">
                    <span>Processing Sentinel-2 surface reflectance...</span>
                    <span>{currentJob.progress_pct}%</span>
                  </div>
                  <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                    <div 
                      className="bg-emerald-600 h-full transition-all duration-300"
                      style={{ width: `${currentJob.progress_pct}%` }}
                    />
                  </div>
                </div>
              )}
            </div>

            {/* Clicked Point HUD Summary */}
            {inspectedPoint && (
              <div className="bg-white border border-emerald-300 rounded-2xl p-4 space-y-3 shadow-md animate-fadeIn">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-emerald-800 flex items-center space-x-1.5">
                    <Compass className="w-3.5 h-3.5 text-emerald-600" />
                    <span>INSPECTED COORDINATES</span>
                  </span>
                  <span className="text-[10px] font-semibold bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded-full border border-emerald-200">
                    {inspectedPoint.spatial_reference?.utm_zone}
                  </span>
                </div>

                <div className="text-xs">
                  <p className="font-bold text-slate-900 truncate">
                    {inspectedPoint.location?.suburb || inspectedPoint.location?.district}, {inspectedPoint.location?.state}
                  </p>
                  <p className="text-[10px] text-slate-500 font-mono mt-0.5">
                    {inspectedPoint.coordinates?.latitude}°N, {inspectedPoint.coordinates?.longitude}°E
                  </p>
                </div>

                <button
                  onClick={() => handleTriggerAI(inspectedPoint)}
                  disabled={isGeneratingAi}
                  className="w-full py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-300 rounded-xl text-xs font-semibold flex items-center justify-center space-x-1.5 transition"
                >
                  <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
                  <span>{isGeneratingAi ? 'Synthesizing...' : 'Run Ecological AI on this Point'}</span>
                </button>
              </div>
            )}

            {/* Results Summary Box with AI Synthesis Button */}
            {currentResult && (
              <div className="bg-white border border-slate-200 rounded-2xl p-5 space-y-3.5 shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-emerald-700 uppercase tracking-wider flex items-center space-x-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span>Assessment Completed</span>
                  </span>
                  <span className="text-[10px] font-semibold text-slate-500">
                    UTM Projected
                  </span>
                </div>

                <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 space-y-1">
                  <span className="text-[10px] text-slate-500 block uppercase font-bold tracking-wider">Quantified Surface Delta</span>
                  <div className="flex items-baseline space-x-2">
                    <span className="text-3xl font-black text-slate-900">
                      {currentResult.total_change_ha}
                    </span>
                    <span className="text-xs text-slate-600 font-bold">hectares</span>
                  </div>
                </div>

                <div className="text-xs text-slate-700 space-y-1.5 leading-relaxed bg-amber-50/70 border border-amber-200 p-3 rounded-xl">
                  <span className="font-bold text-amber-900 text-[10px] block uppercase tracking-wider">
                    SCIENTIFIC EVALUATION NOTE:
                  </span>
                  <p className="text-[11px] text-slate-800">
                    {currentResult.summary_metrics?.cautious_assessment}
                  </p>
                </div>

                {/* AI Analysis Trigger Button */}
                <button
                  onClick={() => handleTriggerAI()}
                  disabled={isGeneratingAi}
                  className="w-full py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-xl text-xs font-semibold flex items-center justify-center space-x-2 shadow-sm transition active:scale-98"
                >
                  <Sparkles className="w-4 h-4 text-yellow-300" />
                  <span>{isGeneratingAi ? 'Synthesizing Environmental Data...' : '✨ RUN ECOLOGICAL AI SYNTHESIS'}</span>
                </button>

                <div className="flex space-x-2 pt-1">
                  <button 
                    onClick={() => {
                      if (!changeVector) return;
                      const blob = new Blob([JSON.stringify(changeVector, null, 2)], { type: 'application/json' });
                      const url = URL.createObjectURL(blob);
                      const a = document.createElement('a');
                      a.href = url;
                      a.download = `terrawatch_${selectedArea?.id}_change_vectors.geojson`;
                      a.click();
                      URL.revokeObjectURL(url);
                    }}
                    className="flex-1 py-2 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl text-[11px] font-semibold text-slate-700 flex items-center justify-center space-x-1 transition"
                  >
                    <Download className="w-3.5 h-3.5 text-slate-600" />
                    <span>GeoJSON</span>
                  </button>
                  <button 
                    onClick={() => {
                      if (!currentResult) return;
                      const rows = [
                        ["Parameter", "Value"],
                        ["Study Area", selectedArea?.name || ""],
                        ["State", selectedArea?.state || ""],
                        ["Module", currentResult.result_type],
                        ["Total Change (ha)", currentResult.total_change_ha.toString()],
                        ["Cloud Cover T1 (%)", currentResult.quality_metadata?.cloud_cover_t1_pct?.toString() || ""],
                        ["Cloud Cover T2 (%)", currentResult.quality_metadata?.cloud_cover_t2_pct?.toString() || ""],
                        ["Projection CRS", currentResult.quality_metadata?.projection_crs || ""],
                        ["Pixel Resolution (m)", currentResult.quality_metadata?.pixel_resolution_m?.toString() || ""],
                        ["Assessment", `"${currentResult.summary_metrics?.cautious_assessment || ''}"`]
                      ];
                      const csvContent = rows.map(e => e.join(",")).join("\n");
                      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                      const url = URL.createObjectURL(blob);
                      const a = document.createElement('a');
                      a.href = url;
                      a.download = `terrawatch_${selectedArea?.id}_summary_report.csv`;
                      a.click();
                      URL.revokeObjectURL(url);
                    }}
                    className="flex-1 py-2 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl text-[11px] font-semibold text-emerald-800 flex items-center justify-center space-x-1 transition"
                  >
                    <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-600" />
                    <span>CSV Report</span>
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Right Column: Interactive Map Canvas & Split Screen Slider (8 Cols) */}
          <div className="lg:col-span-8 space-y-4">
            
            {/* Viewport Mode Switcher */}
            <div className="bg-white border border-slate-200 p-2 rounded-2xl flex items-center justify-between shadow-sm">
              <div className="flex items-center space-x-1.5">
                <button
                  onClick={() => setActiveTab('map')}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition ${
                    activeTab === 'map'
                      ? 'bg-emerald-50 text-emerald-800 border border-emerald-200 shadow-sm'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  Interactive Map Canvas
                </button>
                <button
                  onClick={() => setActiveTab('slider')}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition ${
                    activeTab === 'slider'
                      ? 'bg-emerald-50 text-emerald-800 border border-emerald-200 shadow-sm'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  Before/After Temporal Slider
                </button>
              </div>

              <div className="text-xs text-slate-500 font-medium hidden sm:flex items-center space-x-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                <span>Click any point across India to analyze</span>
              </div>
            </div>

            {/* Viewport Content */}
            {activeTab === 'map' ? (
              <MapCanvas 
                selectedArea={selectedArea}
                changeGeoJSON={changeVector}
                onPointInspect={(data) => setInspectedPoint(data)}
              />
            ) : (
              <SplitSlider 
                selectedArea={selectedArea}
                currentResult={currentResult}
                changeGeoJSON={changeVector}
                beforeDate="2023-03-10"
                afterDate="2024-03-15"
                beforeLabel="T1 Baseline Scene (Pre-monsoon Sentinel-2)"
                afterLabel="T2 Recent Observation (Detected Change Mask)"
              />
            )}

            {/* Environmental Alerts Feed */}
            <div className="bg-white border border-slate-200 rounded-2xl p-4.5 space-y-3 shadow-sm">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-bold text-slate-900 flex items-center space-x-1.5">
                  <AlertTriangle className="w-4 h-4 text-amber-600" />
                  <span>OBSERVATORY ALERTS (GROUND VERIFICATION PENDING)</span>
                </h4>
                <span className="text-[10px] font-semibold text-slate-500">
                  {alerts.length} Flagged Observations
                </span>
              </div>

              <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                {alerts.map((alert) => (
                  <div 
                    key={alert.id}
                    className="bg-slate-50 border border-slate-200 p-3 rounded-xl flex items-start justify-between space-x-3 text-xs hover:border-slate-300 transition"
                  >
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold ${
                          alert.severity === 'HIGH' 
                            ? 'bg-red-50 text-red-800 border border-red-200'
                            : 'bg-amber-50 text-amber-800 border border-amber-200'
                        }`}>
                          {alert.alert_type}
                        </span>
                        <span className="text-[10px] text-slate-500">
                          Confidence: {(alert.confidence_score * 100).toFixed(0)}%
                        </span>
                      </div>
                      <p className="text-slate-700 mt-1.5 text-[11px] leading-relaxed font-sans">
                        {alert.description}
                      </p>
                    </div>

                    <span className="text-[9px] font-semibold bg-white text-slate-600 border border-slate-200 px-2.5 py-1 rounded-lg whitespace-nowrap shadow-xs">
                      {alert.validation_status}
                    </span>
                  </div>
                ))}
              </div>
            </div>

          </div>

        </div>

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-5 px-6 text-center text-xs text-slate-500">
        <div className="flex items-center justify-center space-x-2">
          <Globe className="w-3.5 h-3.5 text-emerald-600" />
          <span className="font-semibold text-slate-800">TerraWatch 360</span>
          <span>&bull;</span>
          <span>National Environmental Intelligence & Conservation Observatory</span>
        </div>
        <p className="text-[10px] text-slate-400 mt-1">Open-Access Geospatial Decision Support Architecture &bull; Compliant with Indian Environmental Standards</p>
      </footer>
    </div>
  );
};

export default App;
