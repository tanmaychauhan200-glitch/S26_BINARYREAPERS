import axios from 'axios';
import { StudyArea, SatelliteScene, AnalysisJob, AnalysisResult, Alert, ProviderStatus, ModuleType } from '../types';

const API_BASE = '/api/v1';

export const api = {
  async getHealth() {
    const res = await axios.get(`${API_BASE}/health`);
    return res.data;
  },

  async getStudyAreas(module?: ModuleType): Promise<StudyArea[]> {
    const params = module ? { module_type: module } : {};
    const res = await axios.get<StudyArea[]>(`${API_BASE}/study-areas`, { params });
    return res.data;
  },

  async getProvidersStatus(): Promise<{ providers: ProviderStatus[] }> {
    const res = await axios.get(`${API_BASE}/providers/status`);
    return res.data;
  },

  async getScenes(): Promise<SatelliteScene[]> {
    const res = await axios.get<SatelliteScene[]>(`${API_BASE}/providers/scenes`);
    return res.data;
  },

  async runJob(payload: { module_type: ModuleType; study_area_id: string; parameters?: any }): Promise<AnalysisJob> {
    const res = await axios.post<AnalysisJob>(`${API_BASE}/jobs/run`, payload);
    return res.data;
  },

  async getJob(jobId: string): Promise<AnalysisJob> {
    const res = await axios.get<AnalysisJob>(`${API_BASE}/jobs/${jobId}`);
    return res.data;
  },

  async getResult(jobId: string): Promise<AnalysisResult> {
    const res = await axios.get<AnalysisResult>(`${API_BASE}/results/${jobId}`);
    return res.data;
  },

  async getResultVector(jobId: string): Promise<any> {
    const res = await axios.get(`${API_BASE}/results/${jobId}/vector`);
    return res.data;
  },

  async getAlerts(module?: ModuleType): Promise<Alert[]> {
    const params = module ? { module_type: module } : {};
    const res = await axios.get<Alert[]>(`${API_BASE}/alerts`, { params });
    return res.data;
  },

  async inspectPoint(latitude: number, longitude: number): Promise<any> {
    const res = await axios.post(`${API_BASE}/analysis/point-inspect`, { latitude, longitude });
    return res.data;
  },

  async runAIAnalysis(payload: {
    module_type: string;
    area_name: string;
    latitude: number;
    longitude: number;
    spectral_metrics?: any;
    total_change_ha: number;
  }): Promise<any> {
    const res = await axios.post(`${API_BASE}/analysis/ai-analyze`, payload);
    return res.data;
  },

  async searchLocation(query: string): Promise<any[]> {
    const res = await axios.get(`${API_BASE}/analysis/search-location`, { params: { q: query } });
    return res.data;
  }
};
