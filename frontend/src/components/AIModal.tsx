import React from 'react';
import { Globe, ShieldAlert, CheckSquare, X, Copy, FileText, CheckCircle2 } from 'lucide-react';

interface AIModalProps {
  isOpen: boolean;
  onClose: () => void;
  report: any;
  areaName: string;
}

export const AIModal: React.FC<AIModalProps> = ({
  isOpen,
  onClose,
  report,
  areaName
}) => {
  if (!isOpen || !report) return null;

  const getRiskBadge = (level: string) => {
    switch (level) {
      case 'CRITICAL':
        return 'bg-red-50 text-red-800 border-red-300';
      case 'HIGH':
        return 'bg-amber-50 text-amber-800 border-amber-300';
      case 'MEDIUM':
        return 'bg-sky-50 text-sky-800 border-sky-300';
      default:
        return 'bg-emerald-50 text-emerald-800 border-emerald-300';
    }
  };

  const handleCopy = () => {
    const text = `TERRAWATCH 360 - ECOLOGICAL INTELLIGENCE BRIEFING\nTarget: ${areaName}\nRisk Assessment: ${report.regulatory_risk_level}\n\nEXECUTIVE SUMMARY:\n${report.executive_summary}\n\nPLAUSIBLE PHYSICAL & ANTHROPOGENIC DRIVERS:\n${(report.plausible_drivers || []).join('\n')}\n\nACTIONABLE GROUND VERIFICATION PROTOCOL:\n${(report.field_inspection_checklist || []).join('\n')}`;
    navigator.clipboard.writeText(text);
    alert("Research Intelligence Briefing copied to clipboard!");
  };

  return (
    <div className="fixed inset-0 z-[2000] flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-2xl bg-white border border-slate-200 rounded-3xl shadow-2xl overflow-hidden max-h-[90vh] flex flex-col">
        
        {/* Top Header */}
        <div className="px-6 py-4 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-600 flex items-center justify-center text-white shadow-sm">
              <Globe className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-sm font-bold text-slate-900 font-sans tracking-tight">
                  ECOLOGICAL RESEARCH AI ANALYST
                </h3>
                <span className="px-2 py-0.5 text-[10px] font-semibold bg-emerald-100 text-emerald-800 rounded-full">
                  Scientific Synthesis
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-sans">
                Multi-Spectral Satellite Assessment &bull; {areaName}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-1.5">
            <button
              onClick={handleCopy}
              className="p-2 text-slate-500 hover:text-emerald-700 hover:bg-slate-100 rounded-xl transition"
              title="Copy Briefing"
            >
              <Copy className="w-4 h-4" />
            </button>
            <button
              onClick={onClose}
              className="p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-xl transition"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Scrollable Content */}
        <div className="p-6 space-y-4 overflow-y-auto text-xs leading-relaxed font-sans">
          
          {/* Metadata Card */}
          <div className="flex items-center justify-between bg-slate-50 p-3.5 rounded-2xl border border-slate-200">
            <div>
              <span className="text-[10px] font-bold text-slate-600 uppercase block">Inference Source</span>
              <span className="text-xs font-semibold text-slate-800">{report.source || "TerraWatch Scientific Engine"}</span>
            </div>
            <div className="text-right">
              <span className="text-[10px] font-bold text-slate-600 uppercase block">Ecological Vulnerability</span>
              <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${getRiskBadge(report.regulatory_risk_level)}`}>
                {report.regulatory_risk_level} RISK
              </span>
            </div>
          </div>

          {/* Executive Summary */}
          <div className="space-y-1.5">
            <h4 className="text-[11px] font-bold text-slate-900 uppercase tracking-wider flex items-center space-x-1.5">
              <FileText className="w-3.5 h-3.5 text-emerald-600" />
              <span>EXECUTIVE RESEARCH BRIEFING</span>
            </h4>
            <p className="text-slate-700 bg-slate-50 p-4 rounded-2xl border border-slate-200 leading-relaxed font-sans text-xs">
              {report.executive_summary}
            </p>
          </div>

          {/* Plausible Drivers */}
          {report.plausible_drivers && (
            <div className="space-y-1.5">
              <h4 className="text-[11px] font-bold text-amber-800 uppercase tracking-wider flex items-center space-x-1.5">
                <ShieldAlert className="w-3.5 h-3.5 text-amber-600" />
                <span>PLAUSIBLE PHYSICAL & ANTHROPOGENIC DRIVERS</span>
              </h4>
              <ul className="bg-amber-50/50 p-3.5 rounded-2xl border border-amber-200/80 space-y-1.5">
                {report.plausible_drivers.map((driver: string, idx: number) => (
                  <li key={idx} className="flex items-start space-x-2 text-slate-700">
                    <span className="text-amber-600 font-bold">&bull;</span>
                    <span>{driver}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Field Inspection Protocol */}
          {report.field_inspection_checklist && (
            <div className="space-y-1.5">
              <h4 className="text-[11px] font-bold text-emerald-900 uppercase tracking-wider flex items-center space-x-1.5">
                <CheckSquare className="w-3.5 h-3.5 text-emerald-600" />
                <span>GROUND VERIFICATION & CONSERVATION AUDIT PROTOCOL (CPCB/MoEFCC)</span>
              </h4>
              <div className="bg-emerald-50/50 p-3.5 rounded-2xl border border-emerald-200/80 space-y-2">
                {report.field_inspection_checklist.map((item: string, idx: number) => (
                  <div key={idx} className="flex items-start space-x-2.5">
                    <span className="w-4 h-4 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[10px] font-bold shrink-0 mt-0.5">
                      {idx + 1}
                    </span>
                    <span className="text-slate-800 text-[11px] leading-snug">{item}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Legal / Statutory Compliance Note */}
          <div className="bg-slate-50 border border-slate-200 p-3 rounded-2xl text-[10px] text-slate-600 font-sans leading-normal">
            {report.statutory_compliance_note}
          </div>

        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-100 bg-slate-50 flex items-center justify-between">
          <span className="text-[10px] text-slate-500">
            TerraWatch 360 &bull; Open Scientific Environmental Evidence
          </span>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-semibold transition shadow-sm"
          >
            Close Briefing
          </button>
        </div>

      </div>
    </div>
  );
};
