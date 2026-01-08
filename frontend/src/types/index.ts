export interface PersonalInfo {
  name: string;
  email: string;
  phone?: string;
  location?: string;
  github?: string;
  linkedin?: string;
}

export interface Experience {
  title: string;
  company: string;
  duration: string;
  description: string[];
  technologies: string[];
}

export interface Skills {
  technical: string[];
  frameworks: string[];
  tools: string[];
  languages: string[];
}

export interface Project {
  name: string;
  description: string;
  technologies: string[];
  github_url?: string;
  impact_metrics: string[];
}

export interface Education {
  degree: string;
  institution: string;
  graduation_year: string;
  gpa?: string;
}

export interface ResumeData {
  id: string;
  personal_info: PersonalInfo;
  experience: Experience[];
  skills: Skills;
  projects: Project[];
  education: Education[];
}

export interface ResumeUploadResponse {
  id: string;
  status: string;
  message: string;
  data?: ResumeData;
}

export interface JobAnalysisRequest {
  job_text?: string;
  job_url?: string;
}

export interface JobAnalysis {
  id: string;
  title: string;
  company: string;
  required_skills: string[];
  preferred_skills: string[];
  technologies: string[];
  experience_level: string;
  key_requirements: string[];
}

export interface JobAnalysisResponse {
  id: string;
  status: string;
  message: string;
  data?: JobAnalysis;
}

export interface OptimizationRequest {
  resume_id: string;
  job_id: string;
}

export interface OptimizationSuggestion {
  section: string;
  type: string;
  original: string;
  suggested: string;
  reason: string;
  impact: string;
}

export interface OptimizationProgress {
  step: string;
  progress: number;
  message: string;
  suggestions: OptimizationSuggestion[];
  completed: boolean;
}
