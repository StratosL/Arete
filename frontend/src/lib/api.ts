import axios from 'axios';
import { ResumeUploadResponse, JobAnalysisRequest, JobAnalysis, OptimizationRequest } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const resumeApi = {
  uploadResume: async (file: File, githubUrl?: string): Promise<ResumeUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    if (githubUrl) {
      formData.append('github_url', githubUrl);
    }

    const response = await apiClient.post<ResumeUploadResponse>('/resume/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },
};

export const jobsApi = {
  analyzeJob: async (data: JobAnalysisRequest): Promise<JobAnalysis> => {
    const response = await apiClient.post<JobAnalysis>('/jobs/analyze', data);
    return response.data;
  },
};

export const optimizationApi = {
  getOptimizationUrl: (data: OptimizationRequest): string => {
    const params = new URLSearchParams({
      resume_id: data.resume_id,
      job_id: data.job_id,
    });
    return `${API_BASE_URL}/optimize?${params.toString()}`;
  },
  
  getOptimizationPayload: (data: OptimizationRequest) => {
    return {
      resume_id: data.resume_id,
      job_id: data.job_id,
    };
  },
};

export default apiClient;
