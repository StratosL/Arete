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
  soft_skills: string[];
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
  degree?: string;
  institution?: string;
  graduation_year?: string;
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
  accepted?: boolean;
}

export interface KeywordMatchScore {
  matched: number;
  total: number;
  percentage: number;
  matched_keywords: string[];
  missing_keywords: string[];
}

export interface SectionScore {
  name: string;
  present: boolean;
  score: number;
}

export interface ATSScore {
  overall_score: number;
  keyword_match: KeywordMatchScore;
  section_completeness: number;
  sections: SectionScore[];
  recommendations: string[];
}

export interface InterviewQuestion {
  category: string;
  question: string;
  tips: string;
}

export interface OptimizationProgress {
  step: string;
  progress: number;
  message: string;
  suggestions: OptimizationSuggestion[];
  completed: boolean;
  ats_score?: ATSScore;
  interview_questions?: InterviewQuestion[];
}