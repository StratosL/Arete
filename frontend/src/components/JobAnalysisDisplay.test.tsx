import { render, screen } from '@testing-library/react';
import { JobAnalysisDisplay } from './JobAnalysisDisplay';
import { JobAnalysis } from '@/types';

const mockJobAnalysis: JobAnalysis = {
  id: 'job-123',
  title: 'Senior Software Engineer',
  company: 'Tech Corp',
  required_skills: ['Python', 'React', 'PostgreSQL'],
  preferred_skills: ['Docker', 'AWS', 'TypeScript'],
  technologies: ['Python', 'React', 'PostgreSQL', 'Docker'],
  experience_level: 'Senior',
  key_requirements: [
    '5+ years of software development experience',
    'Experience with modern web frameworks',
    'Strong problem-solving skills'
  ]
};

describe('JobAnalysisDisplay', () => {
  it('renders job overview correctly', () => {
    render(<JobAnalysisDisplay jobAnalysis={mockJobAnalysis} />);
    
    expect(screen.getByText('Job Analysis Results')).toBeInTheDocument();
    expect(screen.getByText('Job Overview')).toBeInTheDocument();
    expect(screen.getByText('Senior Software Engineer')).toBeInTheDocument();
    expect(screen.getByText('Tech Corp')).toBeInTheDocument();
    expect(screen.getByText('Senior')).toBeInTheDocument();
  });

  it('displays required skills with proper styling', () => {
    render(<JobAnalysisDisplay jobAnalysis={mockJobAnalysis} />);
    
    expect(screen.getByText('Required Skills')).toBeInTheDocument();
    expect(screen.getByText('Python')).toBeInTheDocument();
    expect(screen.getByText('React')).toBeInTheDocument();
    expect(screen.getByText('PostgreSQL')).toBeInTheDocument();
  });

  it('displays preferred skills section', () => {
    render(<JobAnalysisDisplay jobAnalysis={mockJobAnalysis} />);
    
    expect(screen.getByText('Preferred Skills')).toBeInTheDocument();
    expect(screen.getByText('Docker')).toBeInTheDocument();
    expect(screen.getByText('AWS')).toBeInTheDocument();
    expect(screen.getByText('TypeScript')).toBeInTheDocument();
  });

  it('displays technologies section', () => {
    render(<JobAnalysisDisplay jobAnalysis={mockJobAnalysis} />);
    
    expect(screen.getByText('Technologies')).toBeInTheDocument();
    // Technologies should include both required and preferred
    expect(screen.getAllByText('Python')).toHaveLength(2); // In required and technologies
    expect(screen.getAllByText('Docker')).toHaveLength(2); // In preferred and technologies
  });

  it('displays key requirements as a list', () => {
    render(<JobAnalysisDisplay jobAnalysis={mockJobAnalysis} />);
    
    expect(screen.getByText('Key Requirements')).toBeInTheDocument();
    expect(screen.getByText('5+ years of software development experience')).toBeInTheDocument();
    expect(screen.getByText('Experience with modern web frameworks')).toBeInTheDocument();
    expect(screen.getByText('Strong problem-solving skills')).toBeInTheDocument();
  });

  it('handles empty arrays gracefully', () => {
    const emptyJobAnalysis: JobAnalysis = {
      id: 'job-456',
      title: 'Junior Developer',
      company: 'Startup Inc',
      required_skills: [],
      preferred_skills: [],
      technologies: [],
      experience_level: 'Junior',
      key_requirements: []
    };

    render(<JobAnalysisDisplay jobAnalysis={emptyJobAnalysis} />);
    
    expect(screen.getByText('Junior Developer')).toBeInTheDocument();
    expect(screen.getByText('Startup Inc')).toBeInTheDocument();
    expect(screen.getByText('Junior')).toBeInTheDocument();
    
    // Sections should still be present even if empty
    expect(screen.getByText('Required Skills')).toBeInTheDocument();
    expect(screen.getByText('Preferred Skills')).toBeInTheDocument();
    expect(screen.getByText('Technologies')).toBeInTheDocument();
    expect(screen.getByText('Key Requirements')).toBeInTheDocument();
  });

  it('renders proper icons for each section', () => {
    render(<JobAnalysisDisplay jobAnalysis={mockJobAnalysis} />);
    
    // Check that icons are rendered (they should be in the DOM)
    const briefcaseIcons = document.querySelectorAll('[data-lucide="briefcase"]');
    const targetIcons = document.querySelectorAll('[data-lucide="target"]');
    const trendingUpIcons = document.querySelectorAll('[data-lucide="trending-up"]');
    const codeIcons = document.querySelectorAll('[data-lucide="code"]');
    const checkCircleIcons = document.querySelectorAll('[data-lucide="check-circle"]');
    
    expect(briefcaseIcons.length).toBeGreaterThan(0);
    expect(targetIcons.length).toBeGreaterThan(0);
    expect(trendingUpIcons.length).toBeGreaterThan(0);
    expect(codeIcons.length).toBeGreaterThan(0);
    expect(checkCircleIcons.length).toBeGreaterThan(0);
  });

  it('handles long job titles and company names', () => {
    const longJobAnalysis: JobAnalysis = {
      id: 'job-789',
      title: 'Senior Full-Stack Software Engineer with DevOps Experience',
      company: 'Very Long Company Name Technologies International LLC',
      required_skills: ['JavaScript'],
      preferred_skills: ['Node.js'],
      technologies: ['JavaScript'],
      experience_level: 'Senior',
      key_requirements: ['Very long requirement that spans multiple lines and contains detailed information about the position']
    };

    render(<JobAnalysisDisplay jobAnalysis={longJobAnalysis} />);
    
    expect(screen.getByText('Senior Full-Stack Software Engineer with DevOps Experience')).toBeInTheDocument();
    expect(screen.getByText('Very Long Company Name Technologies International LLC')).toBeInTheDocument();
    expect(screen.getByText(/Very long requirement that spans multiple lines/)).toBeInTheDocument();
  });

  it('displays skills with different categories correctly', () => {
    const skillsJobAnalysis: JobAnalysis = {
      id: 'job-skills',
      title: 'Full Stack Developer',
      company: 'Web Agency',
      required_skills: ['HTML', 'CSS', 'JavaScript'],
      preferred_skills: ['Vue.js', 'Nuxt.js', 'Tailwind CSS'],
      technologies: ['HTML', 'CSS', 'JavaScript', 'Vue.js', 'Git'],
      experience_level: 'Mid-level',
      key_requirements: ['Frontend development experience', 'Backend API integration']
    };

    render(<JobAnalysisDisplay jobAnalysis={skillsJobAnalysis} />);
    
    // Check required skills
    expect(screen.getByText('HTML')).toBeInTheDocument();
    expect(screen.getByText('CSS')).toBeInTheDocument();
    expect(screen.getByText('JavaScript')).toBeInTheDocument();
    
    // Check preferred skills
    expect(screen.getByText('Vue.js')).toBeInTheDocument();
    expect(screen.getByText('Nuxt.js')).toBeInTheDocument();
    expect(screen.getByText('Tailwind CSS')).toBeInTheDocument();
    
    // Check technologies (should include Git which is not in required/preferred)
    expect(screen.getByText('Git')).toBeInTheDocument();
  });
});