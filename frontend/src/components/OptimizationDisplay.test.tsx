import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { OptimizationDisplay } from './OptimizationDisplay';
import * as api from '@/lib/api';

vi.mock('@/lib/api');

describe('OptimizationDisplay', () => {
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

  it('renders optimization interface', () => {
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    expect(screen.getByText('Resume Optimization')).toBeInTheDocument();
    expect(screen.getByText('Optimization Control')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /start optimization/i })).toBeInTheDocument();
  });

  it('starts optimization process', async () => {
    const user = userEvent.setup();
    
    // Mock ReadableStream
    const mockReader = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode('data: {"step":"analyzing","progress":10,"message":"Analyzing...","suggestions":[],"completed":false}\n\n')
        })
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode('data: {"step":"complete","progress":100,"message":"Complete","suggestions":[{"section":"skills","type":"add_keyword","original":"Python","suggested":"Python, Docker","reason":"Missing Docker","impact":"high","accepted":false}],"completed":true}\n\n')
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse = {
      ok: true,
      body: { getReader: () => mockReader }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('Processing optimization...')).toBeInTheDocument();
    });
  });

  it('displays optimization suggestions', async () => {
    const user = userEvent.setup();
    
    const mockSuggestion = {
      section: 'skills',
      type: 'add_keyword',
      original: 'Python',
      suggested: 'Python, Docker',
      reason: 'Job requires Docker',
      impact: 'high',
      accepted: false
    };

    const mockReader = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode(`data: {"step":"complete","progress":100,"message":"Complete","suggestions":[${JSON.stringify(mockSuggestion)}],"completed":true}\n\n`)
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse = {
      ok: true,
      body: { getReader: () => mockReader }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('Optimization Suggestions (1)')).toBeInTheDocument();
      expect(screen.getByText('Job requires Docker')).toBeInTheDocument();
    });
  });

  it('toggles suggestion selection', async () => {
    const user = userEvent.setup();
    
    const mockSuggestion = {
      section: 'skills',
      type: 'add_keyword',
      original: 'Python',
      suggested: 'Python, Docker',
      reason: 'Job requires Docker',
      impact: 'high',
      accepted: false
    };

    const mockReader = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode(`data: {"step":"complete","progress":100,"message":"Complete","suggestions":[${JSON.stringify(mockSuggestion)}],"completed":true}\n\n`)
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse = {
      ok: true,
      body: { getReader: () => mockReader }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('Select this')).toBeInTheDocument();
    });
    
    const selectButton = screen.getByText('Select this');
    await user.click(selectButton);
    
    expect(screen.getByText('Selected')).toBeInTheDocument();
  });

  it('applies selected suggestions', async () => {
    const user = userEvent.setup();
    
    const mockSuggestion = {
      section: 'skills',
      type: 'add_keyword',
      original: 'Python',
      suggested: 'Python, Docker',
      reason: 'Job requires Docker',
      impact: 'high',
      accepted: false
    };

    const mockReader = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode(`data: {"step":"complete","progress":100,"message":"Complete","suggestions":[${JSON.stringify(mockSuggestion)}],"completed":true}\n\n`)
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse = {
      ok: true,
      body: { getReader: () => mockReader }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    vi.mocked(api.optimizationApi.saveOptimization).mockResolvedValue();
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    // Start optimization
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('Select this')).toBeInTheDocument();
    });
    
    // Select suggestion
    const selectButton = screen.getByText('Select this');
    await user.click(selectButton);
    
    // Apply suggestions
    const applyButton = screen.getByRole('button', { name: /apply selected/i });
    await user.click(applyButton);
    
    await waitFor(() => {
      expect(api.optimizationApi.saveOptimization).toHaveBeenCalled();
    });
  });

  it('handles optimization error', async () => {
    const user = userEvent.setup();
    
    vi.mocked(api.optimizationApi.startOptimization).mockRejectedValue(
      new Error('Optimization failed')
    );
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('Optimization failed')).toBeInTheDocument();
    });
  });

  it('stops optimization process', async () => {
    const user = userEvent.setup();
    
    const mockReader = {
      read: vi.fn().mockImplementation(() => new Promise(() => {})) // Never resolves
    };

    const mockResponse = {
      ok: true,
      body: { getReader: () => mockReader }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /stop/i })).toBeInTheDocument();
    });
    
    const stopButton = screen.getByRole('button', { name: /stop/i });
    await user.click(stopButton);
    
    expect(screen.getByRole('button', { name: /start optimization/i })).toBeInTheDocument();
  });

  it('shows progress updates during optimization', async () => {
    const user = userEvent.setup();
    
    const mockReader = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode('data: {"step":"analyzing","progress":25,"message":"Analyzing alignment...","suggestions":[],"completed":false}\n\n')
        })
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode('data: {"step":"keywords","progress":75,"message":"Generating keywords...","suggestions":[],"completed":false}\n\n')
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse = {
      ok: true,
      body: { getReader: () => mockReader }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('Analyzing alignment...')).toBeInTheDocument();
    });
  });

  it('handles malformed SSE data gracefully', async () => {
    const user = userEvent.setup();
    
    const mockReader = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode('data: invalid json\n\n')
        })
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode('data: {"step":"complete","progress":100,"message":"Complete","suggestions":[],"completed":true}\n\n')
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse = {
      ok: true,
      body: { getReader: () => mockReader }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    // Should continue processing despite malformed data
    await waitFor(() => {
      expect(screen.getByText('Complete')).toBeInTheDocument();
    });
  });

  it('handles HTTP error responses', async () => {
    const user = userEvent.setup();
    
    const mockResponse = {
      ok: false,
      status: 500,
      statusText: 'Internal Server Error'
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('HTTP 500: Internal Server Error')).toBeInTheDocument();
    });
  });

  it('handles missing response body', async () => {
    const user = userEvent.setup();
    
    const mockResponse = {
      ok: true,
      body: null
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('No response body')).toBeInTheDocument();
    });
  });

  it('displays different impact levels correctly', async () => {
    const user = userEvent.setup();
    
    const suggestions = [
      {
        section: 'skills',
        type: 'add_keyword',
        original: 'Python',
        suggested: 'Python, Docker',
        reason: 'High impact change',
        impact: 'high',
        accepted: false
      },
      {
        section: 'experience',
        type: 'enhance_description',
        original: 'Worked on projects',
        suggested: 'Led development of scalable projects',
        reason: 'Medium impact change',
        impact: 'medium',
        accepted: false
      },
      {
        section: 'projects',
        type: 'add_metric',
        original: 'Built web app',
        suggested: 'Built web app serving 1000+ users',
        reason: 'Low impact change',
        impact: 'low',
        accepted: false
      }
    ];

    const mockReader = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode(`data: {"step":"complete","progress":100,"message":"Complete","suggestions":${JSON.stringify(suggestions)},"completed":true}\n\n`)
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse = {
      ok: true,
      body: { getReader: () => mockReader }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('High Impact')).toBeInTheDocument();
      expect(screen.getByText('Medium Impact')).toBeInTheDocument();
      expect(screen.getByText('Low Impact')).toBeInTheDocument();
    });
  });

  it('disables apply button when no suggestions selected', async () => {
    const user = userEvent.setup();
    
    const mockSuggestion = {
      section: 'skills',
      type: 'add_keyword',
      original: 'Python',
      suggested: 'Python, Docker',
      reason: 'Job requires Docker',
      impact: 'high',
      accepted: false
    };

    const mockReader = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode(`data: {"step":"complete","progress":100,"message":"Complete","suggestions":[${JSON.stringify(mockSuggestion)}],"completed":true}\n\n`)
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse = {
      ok: true,
      body: { getReader: () => mockReader }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      const applyButton = screen.getByRole('button', { name: /apply selected/i });
      expect(applyButton).toBeDisabled();
    });
  });

  it('shows success state after saving', async () => {
    const user = userEvent.setup();
    
    const mockSuggestion = {
      section: 'skills',
      type: 'add_keyword',
      original: 'Python',
      suggested: 'Python, Docker',
      reason: 'Job requires Docker',
      impact: 'high',
      accepted: false
    };

    const mockReader = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode(`data: {"step":"complete","progress":100,"message":"Complete","suggestions":[${JSON.stringify(mockSuggestion)}],"completed":true}\n\n`)
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse = {
      ok: true,
      body: { getReader: () => mockReader }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    vi.mocked(api.optimizationApi.saveOptimization).mockResolvedValue();
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    // Start optimization
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('Select this')).toBeInTheDocument();
    });
    
    // Select suggestion
    const selectButton = screen.getByText('Select this');
    await user.click(selectButton);
    
    // Apply suggestions
    const applyButton = screen.getByRole('button', { name: /apply selected/i });
    await user.click(applyButton);
    
    await waitFor(() => {
      expect(screen.getByText('Saved!')).toBeInTheDocument();
    });
  });

  it('handles save optimization error', async () => {
    const user = userEvent.setup();
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    const mockSuggestion = {
      section: 'skills',
      type: 'add_keyword',
      original: 'Python',
      suggested: 'Python, Docker',
      reason: 'Job requires Docker',
      impact: 'high',
      accepted: false
    };

    const mockReader = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode(`data: {"step":"complete","progress":100,"message":"Complete","suggestions":[${JSON.stringify(mockSuggestion)}],"completed":true}\n\n`)
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse = {
      ok: true,
      body: { getReader: () => mockReader }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValue(mockResponse as any);
    vi.mocked(api.optimizationApi.saveOptimization).mockRejectedValue(new Error('Save failed'));
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    // Start optimization and select suggestion
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('Select this')).toBeInTheDocument();
    });
    
    const selectButton = screen.getByText('Select this');
    await user.click(selectButton);
    
    // Try to apply suggestions
    const applyButton = screen.getByRole('button', { name: /apply selected/i });
    await user.click(applyButton);
    
    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith('Failed to save optimizations:', expect.any(Error));
    });
    
    consoleSpy.mockRestore();
  });

  it('resets state when starting new optimization', async () => {
    const user = userEvent.setup();
    
    // First optimization with suggestions
    const mockSuggestion = {
      section: 'skills',
      type: 'add_keyword',
      original: 'Python',
      suggested: 'Python, Docker',
      reason: 'Job requires Docker',
      impact: 'high',
      accepted: false
    };

    const mockReader1 = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode(`data: {"step":"complete","progress":100,"message":"Complete","suggestions":[${JSON.stringify(mockSuggestion)}],"completed":true}\n\n`)
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse1 = {
      ok: true,
      body: { getReader: () => mockReader1 }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValueOnce(mockResponse1 as any);
    
    render(<OptimizationDisplay resumeData={mockResumeData} jobAnalysis={mockJobAnalysis} />);
    
    // First optimization
    const startButton = screen.getByRole('button', { name: /start optimization/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('Optimization Suggestions (1)')).toBeInTheDocument();
    });
    
    // Start second optimization
    const mockReader2 = {
      read: vi.fn()
        .mockResolvedValueOnce({
          done: false,
          value: new TextEncoder().encode('data: {"step":"analyzing","progress":50,"message":"Analyzing...","suggestions":[],"completed":false}\n\n')
        })
        .mockResolvedValueOnce({ done: true })
    };

    const mockResponse2 = {
      ok: true,
      body: { getReader: () => mockReader2 }
    };

    vi.mocked(api.optimizationApi.startOptimization).mockResolvedValueOnce(mockResponse2 as any);
    
    await user.click(startButton);
    
    // Should clear previous suggestions and show new progress
    expect(screen.queryByText('Optimization Suggestions (1)')).not.toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText('Analyzing...')).toBeInTheDocument();
    });
  });
});