import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { GitHubAnalysis } from './GitHubAnalysis';

describe('GitHubAnalysis', () => {
  const mockOnAddBulletPoint = vi.fn();
  const mockGithubUrl = 'https://github.com/testuser';

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders analyze button when no metrics loaded', () => {
    render(<GitHubAnalysis githubUrl={mockGithubUrl} onAddBulletPoint={mockOnAddBulletPoint} />);
    
    expect(screen.getByText('GitHub Analysis')).toBeInTheDocument();
    expect(screen.getByText('Analyze testuser')).toBeInTheDocument();
  });

  it('shows loading state during analysis', async () => {
    const user = userEvent.setup();
    render(<GitHubAnalysis githubUrl={mockGithubUrl} onAddBulletPoint={mockOnAddBulletPoint} />);
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    expect(screen.getByText('Analyzing GitHub profile...')).toBeInTheDocument();
  });

  it('displays metrics after analysis', async () => {
    const user = userEvent.setup();
    render(<GitHubAnalysis githubUrl={mockGithubUrl} onAddBulletPoint={mockOnAddBulletPoint} />);
    
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText('GitHub Metrics')).toBeInTheDocument();
      expect(screen.getByText('Top Projects')).toBeInTheDocument();
      expect(screen.getByText('AI-Generated Resume Bullets')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('handles bullet point addition', async () => {
    const user = userEvent.setup();
    render(<GitHubAnalysis githubUrl={mockGithubUrl} onAddBulletPoint={mockOnAddBulletPoint} />);
    
    // Trigger analysis first
    const analyzeButton = screen.getByRole('button', { name: /analyze testuser/i });
    await user.click(analyzeButton);
    
    // Wait for analysis to complete and find add buttons
    await waitFor(() => {
      const addButtons = screen.getAllByText('Add');
      expect(addButtons.length).toBeGreaterThan(0);
    }, { timeout: 3000 });
    
    const addButtons = screen.getAllByText('Add');
    await user.click(addButtons[0]);
    
    expect(mockOnAddBulletPoint).toHaveBeenCalledTimes(1);
    expect(screen.getByText('Added')).toBeInTheDocument();
  });

  it('returns null when no github url provided', () => {
    const { container } = render(<GitHubAnalysis githubUrl="" onAddBulletPoint={mockOnAddBulletPoint} />);
    expect(container.firstChild).toBeNull();
  });
});