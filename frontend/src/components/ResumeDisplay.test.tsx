import { render, screen } from '@testing-library/react';
import { ResumeDisplay } from './ResumeDisplay';
import { ResumeData } from '@/types';

const mockResumeData: ResumeData = {
  id: '123',
  personal_info: {
    name: 'John Doe',
    email: 'john@example.com',
    phone: '+1234567890',
    location: 'San Francisco, CA',
    github: 'https://github.com/johndoe',
    linkedin: 'https://linkedin.com/in/johndoe'
  },
  experience: [
    {
      title: 'Senior Software Engineer',
      company: 'Tech Corp',
      duration: '2020-2023',
      description: ['Built scalable web applications', 'Led team of 5 developers'],
      technologies: ['Python', 'React', 'PostgreSQL']
    }
  ],
  skills: {
    technical: ['Python', 'JavaScript'],
    frameworks: ['React', 'FastAPI'],
    tools: ['Git', 'Docker'],
    languages: ['English', 'Spanish']
  },
  projects: [
    {
      name: 'E-commerce Platform',
      description: 'Built full-stack e-commerce solution',
      technologies: ['Python', 'React'],
      github_url: 'https://github.com/johndoe/ecommerce',
      impact_metrics: ['Increased sales by 30%']
    }
  ],
  education: [
    {
      degree: 'Bachelor of Science in Computer Science',
      institution: 'Stanford University',
      graduation_year: '2018',
      gpa: '3.8'
    }
  ]
};

describe('ResumeDisplay', () => {
  it('renders personal information', () => {
    render(<ResumeDisplay resumeData={mockResumeData} />);
    
    expect(screen.getByText('Personal Information')).toBeInTheDocument();
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('renders experience section', () => {
    render(<ResumeDisplay resumeData={mockResumeData} />);
    
    expect(screen.getByText('Experience')).toBeInTheDocument();
    expect(screen.getByText('Senior Software Engineer')).toBeInTheDocument();
    expect(screen.getByText('Tech Corp')).toBeInTheDocument();
  });

  it('renders skills section', () => {
    render(<ResumeDisplay resumeData={mockResumeData} />);
    
    expect(screen.getByText('Skills')).toBeInTheDocument();
    expect(screen.getByText('Technical Skills')).toBeInTheDocument();
    expect(screen.getByText('Frameworks')).toBeInTheDocument();
  });

  it('renders projects section', () => {
    render(<ResumeDisplay resumeData={mockResumeData} />);
    
    expect(screen.getByText('Projects')).toBeInTheDocument();
    expect(screen.getByText('E-commerce Platform')).toBeInTheDocument();
  });

  it('renders education section', () => {
    render(<ResumeDisplay resumeData={mockResumeData} />);
    
    expect(screen.getByText('Education')).toBeInTheDocument();
    expect(screen.getByText('Bachelor of Science in Computer Science')).toBeInTheDocument();
  });
});