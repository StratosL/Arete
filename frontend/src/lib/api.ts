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

  saveOptimization: async (resumeId: string, suggestions: any[]): Promise<void> => {
    await apiClient.post('/optimize/save', {
      resume_id: resumeId,
      suggestions: suggestions.filter(s => s.accepted)
    });
  },
};

export const exportApi = {
  exportResume: async (resumeId: string, format: 'pdf' | 'docx'): Promise<void> => {
    const response = await apiClient.post(`/export/${format}`, 
      { resume_id: resumeId },
      { responseType: 'blob' }
    );
    
    const blob = new Blob([response.data], {
      type: format === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    });
    
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `resume.${format}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  },
};

export default apiClient;
