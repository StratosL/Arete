import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { DocumentExport } from './DocumentExport';
import * as api from '@/lib/api';

vi.mock('@/lib/api');
vi.mock('@/lib/logger', () => ({
  logger: {
    debug: vi.fn(),
    info: vi.fn(),
    warn: vi.fn(),
    error: vi.fn(),
  }
}));

describe('DocumentExport', () => {
  const mockResumeId = 'resume-123';

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders export interface with template selection', () => {
    render(<DocumentExport resumeId={mockResumeId} />);

    expect(screen.getByText('Export Optimized Resume')).toBeInTheDocument();
    expect(screen.getByText('Select Template Style')).toBeInTheDocument();
    // Use getAllByText since template name appears in both selector and "Using..." note
    expect(screen.getAllByText('ATS Classic').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('Modern Professional')).toBeInTheDocument();
    expect(screen.getByText('PDF Format')).toBeInTheDocument();
    expect(screen.getByText('DOCX Format')).toBeInTheDocument();
  });

  it('handles PDF export with classic template by default', async () => {
    const user = userEvent.setup();
    vi.mocked(api.exportApi.exportResume).mockResolvedValue(undefined);

    render(<DocumentExport resumeId={mockResumeId} />);

    const pdfButton = screen.getByRole('button', { name: /pdf format/i });
    await user.click(pdfButton);

    await waitFor(() => {
      expect(api.exportApi.exportResume).toHaveBeenCalledWith(mockResumeId, 'pdf', 'classic');
    });
  });

  it('handles PDF export with modern template when selected', async () => {
    const user = userEvent.setup();
    vi.mocked(api.exportApi.exportResume).mockResolvedValue(undefined);

    render(<DocumentExport resumeId={mockResumeId} />);

    // Select modern template
    const modernButton = screen.getByText('Modern Professional');
    await user.click(modernButton);

    const pdfButton = screen.getByRole('button', { name: /pdf format/i });
    await user.click(pdfButton);

    await waitFor(() => {
      expect(api.exportApi.exportResume).toHaveBeenCalledWith(mockResumeId, 'pdf', 'modern');
    });
  });

  it('handles DOCX export with classic template', async () => {
    const user = userEvent.setup();
    vi.mocked(api.exportApi.exportResume).mockResolvedValue(undefined);

    render(<DocumentExport resumeId={mockResumeId} />);

    const docxButton = screen.getByRole('button', { name: /docx format/i });
    await user.click(docxButton);

    await waitFor(() => {
      expect(api.exportApi.exportResume).toHaveBeenCalledWith(mockResumeId, 'docx', 'classic');
    });
  });

  it('shows loading state during export', async () => {
    const user = userEvent.setup();
    vi.mocked(api.exportApi.exportResume).mockImplementation(() =>
      new Promise(resolve => setTimeout(resolve, 100))
    );

    render(<DocumentExport resumeId={mockResumeId} />);

    const pdfButton = screen.getByRole('button', { name: /pdf format/i });
    await user.click(pdfButton);

    expect(pdfButton).toBeDisabled();
  });

  it('handles export error gracefully', async () => {
    const user = userEvent.setup();
    vi.mocked(api.exportApi.exportResume).mockRejectedValue(new Error('Export failed'));

    render(<DocumentExport resumeId={mockResumeId} />);

    const pdfButton = screen.getByRole('button', { name: /pdf format/i });
    await user.click(pdfButton);

    // Button should be re-enabled after error
    await waitFor(() => {
      expect(pdfButton).not.toBeDisabled();
    });
  });
});