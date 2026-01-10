import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { JobDescriptionInput } from './JobDescriptionInput';
import * as api from '@/lib/api';

vi.mock('@/lib/api');

describe('JobDescriptionInput', () => {
  const mockOnAnalysisSuccess = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders with text tab active by default', () => {
    render(<JobDescriptionInput onAnalysisSuccess={mockOnAnalysisSuccess} />);
    
    expect(screen.getByText('Job Description Analysis')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Paste the job description here...')).toBeInTheDocument();
  });

  it('switches between text and URL tabs', async () => {
    const user = userEvent.setup();
    render(<JobDescriptionInput onAnalysisSuccess={mockOnAnalysisSuccess} />);
    
    await user.click(screen.getByRole('button', { name: /job url/i }));
    
    expect(screen.getByPlaceholderText('https://company.com/jobs/position')).toBeInTheDocument();
    expect(screen.queryByPlaceholderText('Paste the job description here...')).not.toBeInTheDocument();
  });

  it('shows analyze button', () => {
    render(<JobDescriptionInput onAnalysisSuccess={mockOnAnalysisSuccess} />);
    
    expect(screen.getByRole('button', { name: /analyze job description/i })).toBeInTheDocument();
  });

  it('shows minimum character requirement', () => {
    render(<JobDescriptionInput onAnalysisSuccess={mockOnAnalysisSuccess} />);
    
    expect(screen.getByText(/minimum 50 characters/i)).toBeInTheDocument();
  });
});