import { render, screen } from '@testing-library/react';
import { ResumeUpload } from './ResumeUpload';

describe('ResumeUpload', () => {
  const mockOnUploadSuccess = vi.fn();
  const mockSetGithubUrl = vi.fn();
  const defaultProps = {
    onUploadSuccess: mockOnUploadSuccess,
    githubUrl: '',
    setGithubUrl: mockSetGithubUrl
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders upload interface', () => {
    render(<ResumeUpload {...defaultProps} />);
    
    expect(screen.getByText('Upload Your Resume')).toBeInTheDocument();
    expect(screen.getByText('Drop your resume here')).toBeInTheDocument();
  });

  it('renders upload button', () => {
    render(<ResumeUpload {...defaultProps} />);
    
    const button = screen.getByRole('button', { name: /upload & parse resume/i });
    expect(button).toBeInTheDocument();
  });

  it('shows github input field', () => {
    render(<ResumeUpload {...defaultProps} />);
    
    expect(screen.getByPlaceholderText('https://github.com/username')).toBeInTheDocument();
  });
});