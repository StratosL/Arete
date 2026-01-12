import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { GitHubAnalysis } from './GitHubAnalysis';

// Mock fetch globally
global.fetch = vi.fn();

describe('GitHubAnalysis', () => {
  const mockOnAddBulletPoint = vi.fn();
  const mockSetMetrics = vi.fn();
  const mockGithubUrl = 'https://github.com/testuser';

  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch.mockClear();
  });

  it('renders analyze button when no metrics loaded', () => {
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    
    expect(screen.getByText('GitHub Analysis')).toBeInTheDocument();
    expect(screen.getByText('Analyze testuser')).toBeInTheDocument();
  });

  it('shows loading state during analysis', async () => {
    const user = userEvent.setup();
    
    // Mock a delayed response
    global.fetch.mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: () => Promise.resolve({
          username: 'testuser',
          impact_metrics: { total_repos: 10, total_stars: 50, contributions_last_year: 100 },
          tech_stack: { primary_languages: ['Python'], frameworks: ['Django'], tools: ['Git'] },
          top_repositories: [],
          resume_bullet_points: ['Test bullet point']
        })
      }), 100))
    );
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    expect(screen.getByText('Analyzing GitHub profile...')).toBeInTheDocument();
  });

  it('displays metrics after successful analysis', async () => {
    const user = userEvent.setup();
    
    global.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        username: 'testuser',
        impact_metrics: { 
          total_repos: 25, 
          total_stars: 100, 
          total_forks: 50,
          public_repos: 25,
          followers: 200,
          following: 100,
          contributions_last_year: 500 
        },
        tech_stack: { 
          primary_languages: ['Python', 'JavaScript'], 
          frameworks: ['Django', 'React'], 
          tools: ['Docker', 'Git'] 
        },
        top_repositories: [
          {
            name: 'awesome-project',
            description: 'Great project',
            stars: 50,
            forks: 10,
            language: 'Python',
            url: 'https://github.com/testuser/awesome-project'
          }
        ],
        resume_bullet_points: [
          'Developed 25 open source projects using Python and JavaScript',
          'Achieved 100 stars across GitHub repositories'
        ]
      })
    });
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    await waitFor(() => {
      expect(mockSetMetrics).toHaveBeenCalledWith(expect.objectContaining({
        username: 'testuser',
        totalRepos: 25,
        totalStars: 100
      }));
    });
  });

  it('handles bullet point addition', async () => {
    const user = userEvent.setup();
    const mockMetrics = {
      username: 'testuser',
      totalRepos: 10,
      totalStars: 50,
      totalCommits: 100,
      topLanguages: ['Python'],
      topRepos: [],
      suggestedBullets: ['Test bullet point', 'Another bullet point']
    };
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={mockMetrics}
        setMetrics={mockSetMetrics}
      />
    );
    
    const addButtons = screen.getAllByText('Add');
    await user.click(addButtons[0]);
    
    expect(mockOnAddBulletPoint).toHaveBeenCalledWith('Test bullet point');
    expect(screen.getByText('Added')).toBeInTheDocument();
  });

  it('handles API error gracefully', async () => {
    const user = userEvent.setup();
    
    global.fetch.mockRejectedValue(new Error('Network error'));
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Failed to analyze GitHub profile/)).toBeInTheDocument();
    });
  });

  it('returns null when no github url provided', () => {
    const { container } = render(
      <GitHubAnalysis 
        githubUrl="" 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    expect(container.firstChild).toBeNull();
  });

  it('displays GitHub metrics correctly', () => {
    const mockMetrics = {
      username: 'testuser',
      totalRepos: 25,
      totalStars: 100,
      totalCommits: 500,
      topLanguages: ['Python', 'JavaScript'],
      topRepos: [
        {
          name: 'project1',
          description: 'First project',
          stars: 50,
          forks: 10,
          language: 'Python',
          url: 'https://github.com/testuser/project1'
        }
      ],
      suggestedBullets: ['Bullet 1', 'Bullet 2']
    };
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={mockMetrics}
        setMetrics={mockSetMetrics}
      />
    );
    
    expect(screen.getByText('25')).toBeInTheDocument(); // Repositories
    expect(screen.getByText('100')).toBeInTheDocument(); // Stars
    expect(screen.getByText('500')).toBeInTheDocument(); // Commits
    expect(screen.getByText('project1')).toBeInTheDocument();
  });

  it('handles HTTP error responses', async () => {
    const user = userEvent.setup();
    
    global.fetch.mockResolvedValue({
      ok: false,
      status: 404,
      statusText: 'Not Found'
    });
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Failed to analyze GitHub profile/)).toBeInTheDocument();
    });
  });

  it('handles malformed API response', async () => {
    const user = userEvent.setup();
    
    global.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ invalid: 'response' })
    });
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    await waitFor(() => {
      expect(mockSetMetrics).toHaveBeenCalledWith(expect.objectContaining({
        username: undefined,
        totalRepos: undefined,
        totalStars: undefined
      }));
    });
  });

  it('handles empty repositories array', async () => {
    const user = userEvent.setup();
    
    global.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        username: 'testuser',
        impact_metrics: { total_repos: 0, total_stars: 0, contributions_last_year: 0 },
        tech_stack: { primary_languages: [], frameworks: [], tools: [] },
        top_repositories: [],
        resume_bullet_points: []
      })
    });
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    await waitFor(() => {
      expect(mockSetMetrics).toHaveBeenCalledWith(expect.objectContaining({
        totalRepos: 0,
        totalStars: 0,
        topRepos: [],
        suggestedBullets: []
      }));
    });
  });

  it('prevents multiple simultaneous analysis requests', async () => {
    const user = userEvent.setup();
    
    global.fetch.mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: () => Promise.resolve({
          username: 'testuser',
          impact_metrics: { total_repos: 10, total_stars: 50, contributions_last_year: 100 },
          tech_stack: { primary_languages: ['Python'], frameworks: [], tools: [] },
          top_repositories: [],
          resume_bullet_points: []
        })
      }), 200))
    );
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    
    // Click multiple times rapidly
    await user.click(analyzeButton);
    await user.click(analyzeButton);
    await user.click(analyzeButton);
    
    // Should only make one API call
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });

  it('handles repositories with missing fields', async () => {
    const user = userEvent.setup();
    
    global.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        username: 'testuser',
        impact_metrics: { total_repos: 1, total_stars: 5, contributions_last_year: 50 },
        tech_stack: { primary_languages: ['Python'], frameworks: [], tools: [] },
        top_repositories: [
          {
            name: 'incomplete-repo',
            // Missing description, language, etc.
            stars: 5,
            forks: 1,
            url: 'https://github.com/testuser/incomplete-repo'
          }
        ],
        resume_bullet_points: ['Test bullet']
      })
    });
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText('incomplete-repo')).toBeInTheDocument();
      expect(screen.getByText('No description')).toBeInTheDocument();
      expect(screen.getByText('Unknown')).toBeInTheDocument(); // Default language
    });
  });

  it('shows try again button after error', async () => {
    const user = userEvent.setup();
    
    global.fetch.mockRejectedValueOnce(new Error('Network error'));
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Failed to analyze GitHub profile/)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument();
    });
  });

  it('clears error state on successful retry', async () => {
    const user = userEvent.setup();
    
    // First call fails
    global.fetch.mockRejectedValueOnce(new Error('Network error'));
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={null}
        setMetrics={mockSetMetrics}
      />
    );
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Failed to analyze GitHub profile/)).toBeInTheDocument();
    });
    
    // Second call succeeds
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        username: 'testuser',
        impact_metrics: { total_repos: 10, total_stars: 50, contributions_last_year: 100 },
        tech_stack: { primary_languages: ['Python'], frameworks: [], tools: [] },
        top_repositories: [],
        resume_bullet_points: ['Success bullet']
      })
    });
    
    const tryAgainButton = screen.getByRole('button', { name: /try again/i });
    await user.click(tryAgainButton);
    
    await waitFor(() => {
      expect(screen.queryByText(/Failed to analyze GitHub profile/)).not.toBeInTheDocument();
      expect(screen.getByText('GitHub Metrics')).toBeInTheDocument();
    });
  });

  it('handles multiple bullet point additions correctly', async () => {
    const user = userEvent.setup();
    const mockMetrics = {
      username: 'testuser',
      totalRepos: 10,
      totalStars: 50,
      totalCommits: 100,
      topLanguages: ['Python'],
      topRepos: [],
      suggestedBullets: ['First bullet', 'Second bullet', 'Third bullet']
    };
    
    render(
      <GitHubAnalysis 
        githubUrl={mockGithubUrl} 
        onAddBulletPoint={mockOnAddBulletPoint}
        metrics={mockMetrics}
        setMetrics={mockSetMetrics}
      />
    );
    
    const addButtons = screen.getAllByText('Add');
    
    // Add first bullet
    await user.click(addButtons[0]);
    expect(mockOnAddBulletPoint).toHaveBeenCalledWith('First bullet');
    
    // Add third bullet
    await user.click(addButtons[2]);
    expect(mockOnAddBulletPoint).toHaveBeenCalledWith('Third bullet');
    
    expect(mockOnAddBulletPoint).toHaveBeenCalledTimes(2);
    
    // Check that buttons show "Added" state
    expect(screen.getAllByText('Added')).toHaveLength(2);
    expect(screen.getAllByText('Add')).toHaveLength(1);
  });
});