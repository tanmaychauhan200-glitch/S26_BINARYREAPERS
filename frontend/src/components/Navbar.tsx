import React from 'react';
import { Globe, ShieldCheck, Database, Leaf } from 'lucide-react';
import { ModuleType, ProviderStatus } from '../types';

interface NavbarProps {
  activeModule: ModuleType | 'overview';
  onSelectModule: (m: ModuleType | 'overview') => void;
  providers: ProviderStatus[];
  offlineMode: boolean;
  onToggleOffline: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeModule,
  onSelectModule,
  providers,
  offlineMode,
  onToggleOffline
}) => {
  return (
    <header className="bg-white/95 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50 px-6 py-3 shadow-sm">
      <div className="flex items-center justify-between max-w-7xl mx-auto">
        
        {/* Brand & Logo */}
        <div 
          className="flex items-center space-x-3 cursor-pointer group"
          onClick={() => onSelectModule('overview')}
        >
          <div className="w-10 h-10 rounded-xl bg-emerald-600 flex items-center justify-center text-white shadow-md shadow-emerald-600/20 group-hover:bg-emerald-700 transition">
            <Globe className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold tracking-tight text-lg text-slate-900 font-sans">
                TerraWatch <span className="text-emerald-600">360</span>
              </span>
              <span className="px-2 py-0.5 text-[10px] font-medium bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-full">
                Research Observatory
              </span>
            </div>
            <p className="text-[11px] text-slate-500 font-sans">
              National Satellite Environmental Intelligence & Conservation Platform
            </p>
          </div>
        </div>

        {/* Module Switcher Buttons */}
        <nav className="hidden md:flex items-center space-x-1 bg-slate-100 p-1 rounded-xl border border-slate-200">
          <button
            onClick={() => onSelectModule('overview')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeModule === 'overview'
                ? 'bg-white text-slate-900 shadow-sm border border-slate-200'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Observatory Overview
          </button>
          <button
            onClick={() => onSelectModule('riverwatch')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center space-x-1.5 ${
              activeModule === 'riverwatch'
                ? 'bg-sky-50 text-sky-800 border border-sky-300 shadow-sm'
                : 'text-slate-600 hover:text-sky-700'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-sky-500"></span>
            <span>RiverWatch</span>
          </button>
          <button
            onClick={() => onSelectModule('wetlandwatch')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center space-x-1.5 ${
              activeModule === 'wetlandwatch'
                ? 'bg-teal-50 text-teal-800 border border-teal-300 shadow-sm'
                : 'text-slate-600 hover:text-teal-700'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-teal-500"></span>
            <span>WetlandWatch</span>
          </button>
          <button
            onClick={() => onSelectModule('forestguard')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center space-x-1.5 ${
              activeModule === 'forestguard'
                ? 'bg-emerald-50 text-emerald-800 border border-emerald-300 shadow-sm'
                : 'text-slate-600 hover:text-emerald-700'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>ForestGuard</span>
          </button>
          <button
            onClick={() => onSelectModule('urbanwatch')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center space-x-1.5 ${
              activeModule === 'urbanwatch'
                ? 'bg-amber-50 text-amber-800 border border-amber-300 shadow-sm'
                : 'text-slate-600 hover:text-amber-700'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-amber-500"></span>
            <span>UrbanWatch</span>
          </button>
        </nav>

        {/* Provider Status Pill & Offline Toggle */}
        <div className="flex items-center space-x-3">
          <div className="hidden lg:flex items-center space-x-2 text-xs bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-200">
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-600"></span>
            </span>
            <span className="text-slate-700 font-medium text-[11px]">Sentinel-2 L2A &bull; Active</span>
          </div>

          <button
            onClick={onToggleOffline}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-medium border transition ${
              offlineMode
                ? 'bg-emerald-50 text-emerald-800 border-emerald-200 hover:bg-emerald-100'
                : 'bg-sky-50 text-sky-800 border-sky-200 hover:bg-sky-100'
            }`}
          >
            <Database className="w-3.5 h-3.5 text-emerald-600" />
            <span>{offlineMode ? 'Local Benchmark' : 'Live STAC'}</span>
          </button>
        </div>

      </div>
    </header>
  );
};
