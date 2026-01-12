import axios from 'axios';
import { ResumeUploadResponse, JobAnalysisRequest, JobAnalysis, OptimizationRequest } from '@/types';
import { logger } from './logger';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const resumeApi = {
  uploadResume: async (file: File, githubUrl?: string): Promise<ResumeUploadResponse> => {
    logger.debug('API: Starting resume upload', { 
      fileName: file.name, 
      fileSize: file.size, 
      fileType: file.type,
      githubUrl: githubUrl || 'none'
    });

    const formData = new FormData();
    formData.append('file', file);
    if (githubUrl) {
      formData.append('github_url', githubUrl);
    }

    try {
      const response = await apiClient.post<ResumeUploadResponse>('/resume/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      logger.debug('API: Upload response received', {
        status: response.status,
        statusText: response.statusText,
        data: response.data
      });

      // Validate response structure
      if (!response.data) {
        throw new Error('API returned empty response data');
      }

      if (!response.data.data && response.data.status !== 'success') {
        throw new Error(`API returned error: ${response.data.message || 'Unknown error'}`);
      }

      return response.data;
    } catch (error: any) {
      logger.error('API: Upload failed', {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        responseData: error.response?.data,
        requestConfig: {
          url: error.config?.url,
          method: error.config?.method,
          headers: error.config?.headers
        }
      });
      
      // Re-throw with enhanced error information
      throw error;
    }
  },
};

export const jobsApi = {
  analyzeJob: async (data: JobAnalysisRequest): Promise<JobAnalysis> => {
    const response = await apiClient.post<JobAnalysis>('/jobs/analyze', data);
    return response.data;
  },
};

export const optimizationApi = {
  startOptimization: async (data: OptimizationRequest): Promise<Response> => {
    const response = await fetch(`${API_BASE_URL}/optimize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        resume_id: data.resume_id,
        job_id: data.job_id,
      }),
    });
    return response;
  },

  generateCoverLetter: async (resumeId: string, jobId: string): Promise<{ cover_letter: string }> => {
    logger.debug('generateCoverLetter API called with:', { resumeId, jobId });
    
    try {
      const response = await apiClient.post('/optimize/cover-letter', {
        resume_id: resumeId,
        job_id: jobId,
      });
      
      logger.debug('generateCoverLetter API response:', response);
      
      if (!response.data) {
        throw new Error('No data in response');
      }
      
      return response.data;
    } catch (error) {
      logger.error('generateCoverLetter API error:', error);
      throw error;
    }
  },

  saveOptimization: async (resumeId: string, suggestions: any[], resumeData: any): Promise<void> => {
    // Apply accepted suggestions to create optimized resume data
    const acceptedSuggestions = suggestions.filter(s => s.accepted);
    const optimizedData = JSON.parse(JSON.stringify(resumeData)); // Deep clone
    
    // Apply each accepted suggestion to the resume data
    for (const suggestion of acceptedSuggestions) {
      if (suggestion.section === 'skills' && suggestion.type === 'add_keyword') {
        // Add new skill
        if (!optimizedData.skills) optimizedData.skills = { technical: [] };
        if (!optimizedData.skills.technical) optimizedData.skills.technical = [];
        if (!optimizedData.skills.technical.includes(suggestion.suggested)) {
          optimizedData.skills.technical.push(suggestion.suggested);
        }
      } else if (suggestion.section === 'experience') {
        // Update experience descriptions
        if (optimizedData.experience) {
          for (const exp of optimizedData.experience) {
            if (exp.description) {
              exp.description = exp.description.map((desc: string) =>
                desc === suggestion.original ? suggestion.suggested : desc
              );
            }
          }
        }
      } else if (suggestion.section === 'projects') {
        // Update project descriptions
        if (optimizedData.projects) {
          for (const proj of optimizedData.projects) {
            if (proj.description === suggestion.original) {
              proj.description = suggestion.suggested;
            }
          }
        }
      }
    }
    
    await apiClient.post('/optimize/save', {
      resume_id: resumeId,
      optimized_data: optimizedData
    });
  },
};

export interface TemplateInfo {
  id: string;
  name: string;
  description: string;
  preview_image: string | null;
}

export const exportApi = {
  getTemplates: async (): Promise<TemplateInfo[]> => {
    const response = await apiClient.get<TemplateInfo[]>('/export/templates');
    return response.data;
  },

  exportResume: async (
    resumeId: string,
    format: 'pdf' | 'docx',
    template: 'classic' | 'modern' = 'classic'
  ): Promise<void> => {
    const response = await apiClient.post(
      `/export/${format}`,
      { resume_id: resumeId, template },
      { responseType: 'blob' }
    );

    // Check content type to determine how to handle the response
    const contentType = response.headers['content-type'] || '';

    if (contentType.includes('text/html')) {
      // Modern template returns HTML - open in new tab for browser print
      const htmlBlob = new Blob([response.data], { type: 'text/html' });
      const url = window.URL.createObjectURL(htmlBlob);
      const printWindow = window.open(url, '_blank');

      if (printWindow) {
        printWindow.onload = () => {
          // Add a small delay to ensure styles are loaded
          setTimeout(() => {
            printWindow.print();
          }, 500);
        };
      }

      // Clean up after a delay
      setTimeout(() => {
        window.URL.revokeObjectURL(url);
      }, 60000);
    } else {
      // Classic template returns direct PDF/DOCX - download
      const mimeType = format === 'pdf'
        ? 'application/pdf'
        : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';

      const blob = new Blob([response.data], { type: mimeType });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `resume.${format}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    }
  },
};

export default apiClient;
