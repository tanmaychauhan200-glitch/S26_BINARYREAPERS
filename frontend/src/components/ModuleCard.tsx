import React from 'react';
import { Waves, Droplet, Trees, Building2, ArrowRight } from 'lucide-react';
import { ModuleType } from '../types';

interface ModuleCardProps {
  id: ModuleType;
  title: string;
  tagline: string;
  description: string;
  accentColor: string;
  borderColor: string;
  badgeBg: string;
  badgeText: string;
  keyMetricLabel: string;
  keyMetricValue: string;
  studyAreasCount: number;
  onOpen: (id: ModuleType) => void;
}

export const ModuleCard: React.FC<ModuleCardProps> = ({
  id,
  title,
  tagline,
  description,
  accentColor,
  keyMetricLabel,
  keyMetricValue,
  studyAreasCount,
  onOpen
}) => {
  const getIcon = () => {
    switch (id) {
      case 'riverwatch':
        return (
          <div className="p-2.5 rounded-xl bg-sky-50 text-sky-700 border border-sky-200">
            <Waves className="w-5 h-5" />
          </div>
        );
      case 'wetlandwatch':
        return (
          <div className="p-2.5 rounded-xl bg-teal-50 text-teal-700 border border-teal-200">
            <Droplet className="w-5 h-5" />
          </div>
        );
      case 'forestguard':
        return (
          <div className="p-2.5 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200">
            <Trees className="w-5 h-5" />
          </div>
        );
      case 'urbanwatch':
        return (
          <div className="p-2.5 rounded-xl bg-amber-50 text-amber-700 border border-amber-200">
            <Building2 className="w-5 h-5" />
          </div>
        );
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5 hover:shadow-md hover:border-slate-300 transition duration-200 flex flex-col justify-between shadow-sm">
      {/* Top Section */}
      <div>
        <div className="flex items-center justify-between mb-3.5">
          {getIcon()}
          <span className="text-[11px] font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
            {studyAreasCount} Active Sites
          </span>
        </div>

        <h3 className="text-base font-bold text-slate-900 tracking-tight font-sans">
          {title}
        </h3>
        <p className={`text-xs font-semibold mb-2 ${accentColor}`}>
          {tagline}
        </p>
        <p className="text-xs text-slate-600 line-clamp-3 leading-relaxed font-sans">
          {description}
        </p>
      </div>

      {/* Metric & Action CTA */}
      <div className="mt-5 pt-3.5 border-t border-slate-100 flex items-center justify-between">
        <div>
          <span className="text-[10px] uppercase font-bold tracking-wider text-slate-600 block">
            {keyMetricLabel}
          </span>
          <span className="text-xs font-bold text-slate-800">
            {keyMetricValue}
          </span>
        </div>

        <button
          onClick={() => onOpen(id)}
          className="flex items-center space-x-1 text-xs font-bold text-emerald-600 hover:text-emerald-700 transition"
        >
          <span>Explore</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
