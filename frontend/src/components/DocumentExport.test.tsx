import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { DocumentExport } from './DocumentExport';
import * as api from '@/lib/api';

vi.mock('@/lib/api');

describe('DocumentExport', () => {
  const mockResumeId = 'resume-123';

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders export interface', () => {
    render(<DocumentExport resumeId={mockResumeId} />);
    
    expect(screen.getByText('Export Optimized Resume')).toBeInTheDocument();
    expect(screen.getByText('PDF Format')).toBeInTheDocument();
    expect(screen.getByText('DOCX Format')).toBeInTheDocument();
  });

  it('handles PDF export', async () => {
    const user = userEvent.setup();
    vi.mocked(api.exportApi.exportResume).mockResolvedValue(undefined);
    
    render(<DocumentExport resumeId={mockResumeId} />);
    
    const pdfButton = screen.getByRole('button', { name: /pdf format/i });
    await user.click(pdfButton);
    
    await waitFor(() => {
      expect(api.exportApi.exportResume).toHaveBeenCalledWith(mockResumeId, 'pdf');
    });
  });

  it('handles DOCX export', async () => {
    const user = userEvent.setup();
    vi.mocked(api.exportApi.exportResume).mockResolvedValue(undefined);
    
    render(<DocumentExport resumeId={mockResumeId} />);
    
    const docxButton = screen.getByRole('button', { name: /docx format/i });
    await user.click(docxButton);
    
    await waitFor(() => {
      expect(api.exportApi.exportResume).toHaveBeenCalledWith(mockResumeId, 'docx');
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

  it('handles export error', async () => {
    const user = userEvent.setup();
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.mocked(api.exportApi.exportResume).mockRejectedValue(new Error('Export failed'));
    
    render(<DocumentExport resumeId={mockResumeId} />);
    
    const pdfButton = screen.getByRole('button', { name: /pdf format/i });
    await user.click(pdfButton);
    
    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith('Export failed:', expect.any(Error));
    });
    
    consoleSpy.mockRestore();
  });
});