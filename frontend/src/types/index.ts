export type ModuleType = 'riverwatch' | 'wetlandwatch' | 'forestguard' | 'urbanwatch';

export interface StudyArea {
  id: string;
  name: string;
  description: string;
  module_type: ModuleType;
  state: string;
  geometry: {
    type: string;
    coordinates: number[][][];
  };
  area_ha: number;
}

export interface SatelliteScene {
  id: string;
  provider: string;
  satellite: string;
  sensor: string;
  product_id: string;
  acquisition_date: string;
  cloud_cover_pct: number;
  processing_level: string;
  crs: string;
  resolution_m: number;
  footprint: any;
  download_status: string;
}

export interface AnalysisJob {
  id: string;
  module_type: ModuleType;
  study_area_id: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  progress_pct: number;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
}

export interface AnalysisResult {
  id: string;
  job_id: string;
  result_type: string;
  total_change_ha: number;
  summary_metrics: Record<string, any>;
  quality_metadata: Record<string, any>;
  created_at: string;
}

export interface Alert {
  id: string;
  module_type: ModuleType;
  study_area_id: string;
  alert_type: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  description: string;
  confidence_score: number;
  validation_status: string;
  created_at: string;
}

export interface ProviderStatus {
  id: string;
  name: string;
  type: string;
  status: string;
  endpoint: string;
  sensors?: string[];
  authenticated: boolean;
  quota: string;
}
