import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { App } from '@/App';
import * as api from '@/lib/api';

vi.mock('@/lib/api');

describe('Cross-Component Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('validates complete data flow between components', async () => {
    const user = userEvent.setup();
    
    // Mock successful API responses
    vi.mocked(api.resumeApi.uploadResume).mockResolvedValue({
      id: 'resume-123',
      status: 'success',
      message: 'Success',
      data: {
        id: 'resume-123',
        personal_info: { name: 'John Doe', email: 'john@example.com' },
        experience: [{ title: 'Developer', company: 'Tech Corp', duration: '2020-2023', description: [], technologies: [] }],
        skills: { technical: ['Python'], frameworks: [], tools: [], languages: [] },
        projects: [],
        education: []
      }
    });

    vi.mocked(api.jobsApi.analyzeJob).mockResolvedValue({
      id: 'job-456',
      title: 'Senior Developer',
      company: 'Startup Inc',
      required_skills: ['Python'],
      preferred_skills: [],
      technologies: ['Python'],
      experience_level: 'Senior',
      key_requirements: []
    });

    render(<App />);

    // 1. Upload resume
    const file = new File(['test'], 'resume.pdf', { type: 'application/pdf' });
    const fileInput = screen.getByLabelText(/upload/i);
    await user.upload(fileInput, file);
    
    const uploadButton = screen.getByRole('button', { name: /upload.*parse/i });
    await user.click(uploadButton);

    // Wait for resume data to appear
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });

    // 2. Analyze job
    const jobTextarea = screen.getByPlaceholderText(/paste.*job description/i);
    await user.type(jobTextarea, 'Senior Developer position requiring Python and 5+ years experience');
    
    const analyzeButton = screen.getByRole('button', { name: /analyze job/i });
    await user.click(analyzeButton);

    // Wait for job analysis to appear
    await waitFor(() => {
      expect(screen.getByText('Senior Developer')).toBeInTheDocument();
    });

    // 3. Verify data is available for optimization
    expect(screen.getByText('Python')).toBeInTheDocument(); // From both resume and job
    expect(screen.getByText('Startup Inc')).toBeInTheDocument();

    // Verify APIs were called with correct data
    expect(api.resumeApi.uploadResume).toHaveBeenCalledWith(file, undefined);
    expect(api.jobsApi.analyzeJob).toHaveBeenCalledWith({
      job_text: 'Senior Developer position requiring Python and 5+ years experience'
    });
  });

  it('handles state synchronization between components', async () => {
    const user = userEvent.setup();
    
    // Mock resume upload
    vi.mocked(api.resumeApi.uploadResume).mockResolvedValue({
      id: 'resume-123',
      status: 'success', 
      message: 'Success',
      data: {
        id: 'resume-123',
        personal_info: { name: 'Jane Smith', email: 'jane@example.com' },
        experience: [],
        skills: { technical: ['JavaScript'], frameworks: [], tools: [], languages: [] },
        projects: [],
        education: []
      }
    });

    render(<App />);

    // Upload resume
    const file = new File(['test'], 'resume.pdf', { type: 'application/pdf' });
    const fileInput = screen.getByLabelText(/upload/i);
    await user.upload(fileInput, file);
    
    await user.click(screen.getByRole('button', { name: /upload.*parse/i }));

    // Verify state is shared across components
    await waitFor(() => {
      expect(screen.getByText('Jane Smith')).toBeInTheDocument();
      expect(screen.getByText('JavaScript')).toBeInTheDocument();
    });

    // Verify resume data is available for other workflows
    expect(screen.getByText(/job description analysis/i)).toBeInTheDocument();
  });

  it('validates error propagation between components', async () => {
    const user = userEvent.setup();
    
    // Mock API error
    vi.mocked(api.resumeApi.uploadResume).mockRejectedValue(
      new Error('Upload failed')
    );

    render(<App />);

    const file = new File(['test'], 'resume.pdf', { type: 'application/pdf' });
    const fileInput = screen.getByLabelText(/upload/i);
    await user.upload(fileInput, file);
    
    await user.click(screen.getByRole('button', { name: /upload.*parse/i }));

    // Verify error is displayed and doesn't break other components
    await waitFor(() => {
      expect(screen.getByText(/upload failed/i)).toBeInTheDocument();
    });

    // Verify other components are still functional
    expect(screen.getByText(/job description analysis/i)).toBeInTheDocument();
  });
});