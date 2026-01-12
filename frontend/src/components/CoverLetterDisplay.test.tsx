import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CoverLetterDisplay } from './CoverLetterDisplay';
import * as api from '@/lib/api';

vi.mock('@/lib/api');

describe('CoverLetterDisplay', () => {
  const mockResumeData = {
    id: 'resume-123',
    personal_info: { name: 'John Doe', email: 'john@example.com' },
    experience: [{ title: 'Developer', company: 'Tech Corp', duration: '2020-2023', description: [], technologies: [] }],
    skills: { technical: ['Python'], frameworks: [], tools: [], languages: [] },
    projects: [],
    education: []
  };

  const mockJobAnalysis = {
    id: 'job-456',
    title: 'Senior Developer',
    company: 'Startup Inc',
    required_skills: ['Python'],
    preferred_skills: [],
    technologies: ['Python'],
    experience_level: 'Senior',
    key_requirements: []
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows missing data message when no resume or job data', () => {
    render(<CoverLetterDisplay />);
    
    expect(screen.getByText('Missing Data')).toBeInTheDocument();
    expect(screen.getByText(/Please complete resume upload and job analysis/)).toBeInTheDocument();
  });

  it('renders generate button when data is available', () => {
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    expect(screen.getByText('Cover Letter')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /generate cover letter/i })).toBeInTheDocument();
  });

  it('generates cover letter successfully', async () => {
    const user = userEvent.setup();
    const mockCoverLetter = 'Dear Hiring Manager,\n\nI am excited to apply for the Senior Developer position at Startup Inc.\n\nBest regards,\nJohn Doe';
    
    vi.mocked(api.optimizationApi.generateCoverLetter).mockResolvedValue({
      cover_letter: mockCoverLetter
    });
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Cover letter generated successfully/)).toBeInTheDocument();
      expect(screen.getByText(mockCoverLetter)).toBeInTheDocument();
    });
  });

  it('shows loading state during generation', async () => {
    const user = userEvent.setup();
    
    vi.mocked(api.optimizationApi.generateCoverLetter).mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({ cover_letter: 'Test letter' }), 100))
    );
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    expect(screen.getByText('Generating...')).toBeInTheDocument();
  });

  it('handles generation error', async () => {
    const user = userEvent.setup();
    
    vi.mocked(api.optimizationApi.generateCoverLetter).mockRejectedValue(
      new Error('Generation failed')
    );
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Generation failed/)).toBeInTheDocument();
    });
  });

  it('downloads cover letter', async () => {
    const user = userEvent.setup();
    const mockCoverLetter = 'Test cover letter content';
    
    // Mock URL.createObjectURL and related methods
    global.URL.createObjectURL = vi.fn(() => 'mock-url');
    global.URL.revokeObjectURL = vi.fn();
    
    // Mock document.createElement and appendChild/removeChild
    const mockLink = {
      href: '',
      download: '',
      click: vi.fn()
    };
    vi.spyOn(document, 'createElement').mockReturnValue(mockLink as any);
    vi.spyOn(document.body, 'appendChild').mockImplementation(() => mockLink as any);
    vi.spyOn(document.body, 'removeChild').mockImplementation(() => mockLink as any);
    
    vi.mocked(api.optimizationApi.generateCoverLetter).mockResolvedValue({
      cover_letter: mockCoverLetter
    });
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    // Generate cover letter first
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.getByText(mockCoverLetter)).toBeInTheDocument();
    });
    
    // Download cover letter
    const downloadButton = screen.getByRole('button', { name: /download/i });
    await user.click(downloadButton);
    
    expect(mockLink.click).toHaveBeenCalled();
    expect(mockLink.download).toContain('cover-letter');
  });

  it('regenerates cover letter', async () => {
    const user = userEvent.setup();
    const firstLetter = 'First cover letter';
    const secondLetter = 'Second cover letter';
    
    vi.mocked(api.optimizationApi.generateCoverLetter)
      .mockResolvedValueOnce({ cover_letter: firstLetter })
      .mockResolvedValueOnce({ cover_letter: secondLetter });
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    // Generate first letter
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.getByText(firstLetter)).toBeInTheDocument();
    });
    
    // Regenerate
    const regenerateButton = screen.getByRole('button', { name: /regenerate/i });
    await user.click(regenerateButton);
    
    await waitFor(() => {
      expect(screen.getByText(secondLetter)).toBeInTheDocument();
    });
  });

  it('handles API response without cover_letter field', async () => {
    const user = userEvent.setup();
    
    vi.mocked(api.optimizationApi.generateCoverLetter).mockResolvedValue({} as any);
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Invalid response: missing cover_letter field/)).toBeInTheDocument();
    });
  });

  it('handles network errors with detailed error messages', async () => {
    const user = userEvent.setup();
    
    const mockError = {
      response: {
        data: { detail: 'API rate limit exceeded' },
        status: 429
      }
    };
    
    vi.mocked(api.optimizationApi.generateCoverLetter).mockRejectedValue(mockError);
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.getByText('API rate limit exceeded')).toBeInTheDocument();
    });
  });

  it('prevents multiple simultaneous generation requests', async () => {
    const user = userEvent.setup();
    
    vi.mocked(api.optimizationApi.generateCoverLetter).mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({ cover_letter: 'Test letter' }), 200))
    );
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    
    // Click multiple times rapidly
    await user.click(generateButton);
    await user.click(generateButton);
    await user.click(generateButton);
    
    // Should only make one API call
    expect(api.optimizationApi.generateCoverLetter).toHaveBeenCalledTimes(1);
  });

  it('handles missing resume or job IDs gracefully', async () => {
    const user = userEvent.setup();
    
    const incompleteResumeData = { ...mockResumeData, id: '' };
    
    render(<CoverLetterDisplay resumeData={incompleteResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.getByText('Resume and job analysis required')).toBeInTheDocument();
    });
  });

  it('clears error state on successful generation', async () => {
    const user = userEvent.setup();
    
    // First call fails
    vi.mocked(api.optimizationApi.generateCoverLetter)
      .mockRejectedValueOnce(new Error('Generation failed'))
      .mockResolvedValueOnce({ cover_letter: 'Success letter' });
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Generation failed/)).toBeInTheDocument();
    });
    
    // Try again
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.queryByText(/Generation failed/)).not.toBeInTheDocument();
      expect(screen.getByText('Success letter')).toBeInTheDocument();
    });
  });

  it('handles download errors gracefully', async () => {
    const user = userEvent.setup();
    const mockCoverLetter = 'Test cover letter content';
    
    // Mock URL.createObjectURL to throw error
    global.URL.createObjectURL = vi.fn(() => {
      throw new Error('Blob creation failed');
    });
    
    vi.mocked(api.optimizationApi.generateCoverLetter).mockResolvedValue({
      cover_letter: mockCoverLetter
    });
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    // Generate cover letter first
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.getByText(mockCoverLetter)).toBeInTheDocument();
    });
    
    // Try to download
    const downloadButton = screen.getByRole('button', { name: /download/i });
    await user.click(downloadButton);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to download cover letter')).toBeInTheDocument();
    });
  });

  it('generates safe filenames for download', async () => {
    const user = userEvent.setup();
    const mockCoverLetter = 'Test cover letter content';
    
    // Mock URL.createObjectURL and related methods
    global.URL.createObjectURL = vi.fn(() => 'mock-url');
    global.URL.revokeObjectURL = vi.fn();
    
    const mockLink = {
      href: '',
      download: '',
      click: vi.fn()
    };
    vi.spyOn(document, 'createElement').mockReturnValue(mockLink as any);
    vi.spyOn(document.body, 'appendChild').mockImplementation(() => mockLink as any);
    vi.spyOn(document.body, 'removeChild').mockImplementation(() => mockLink as any);
    
    vi.mocked(api.optimizationApi.generateCoverLetter).mockResolvedValue({
      cover_letter: mockCoverLetter
    });
    
    const jobAnalysisWithSpecialChars = {
      ...mockJobAnalysis,
      company: 'Tech & Co.',
      title: 'Senior Developer/Engineer'
    };
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={jobAnalysisWithSpecialChars} />);
    
    // Generate and download
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.getByText(mockCoverLetter)).toBeInTheDocument();
    });
    
    const downloadButton = screen.getByRole('button', { name: /download/i });
    await user.click(downloadButton);
    
    expect(mockLink.download).toBe('cover-letter-Tech---Co--Senior-Developer-Engineer.txt');
  });

  it('shows proper loading states during regeneration', async () => {
    const user = userEvent.setup();
    const firstLetter = 'First cover letter';
    const secondLetter = 'Second cover letter';
    
    vi.mocked(api.optimizationApi.generateCoverLetter)
      .mockResolvedValueOnce({ cover_letter: firstLetter })
      .mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({ cover_letter: secondLetter }), 100))
      );
    
    render(<CoverLetterDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    // Generate first letter
    const generateButton = screen.getByRole('button', { name: /generate cover letter/i });
    await user.click(generateButton);
    
    await waitFor(() => {
      expect(screen.getByText(firstLetter)).toBeInTheDocument();
    });
    
    // Start regeneration
    const regenerateButton = screen.getByRole('button', { name: /regenerate/i });
    await user.click(regenerateButton);
    
    // Check loading state
    expect(screen.getByText('Regenerating...')).toBeInTheDocument();
    expect(regenerateButton).toBeDisabled();
    
    await waitFor(() => {
      expect(screen.getByText(secondLetter)).toBeInTheDocument();
      expect(screen.queryByText('Regenerating...')).not.toBeInTheDocument();
    });
  });
});