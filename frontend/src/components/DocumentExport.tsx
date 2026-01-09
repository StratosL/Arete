import { useState } from 'react';
import { Download, FileText, File as FileIcon } from 'lucide-react';
import { exportApi } from '@/lib/api';

interface DocumentExportProps {
  resumeId: string;
}

export const DocumentExport = ({ resumeId }: DocumentExportProps) => {
  const [isExporting, setIsExporting] = useState<string | null>(null);

  const handleExport = async (format: 'pdf' | 'docx') => {
    setIsExporting(format);
    try {
      await exportApi.exportResume(resumeId, format);
    } catch (error) {
      console.error('Export failed:', error);
    } finally {
      setIsExporting(null);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Export Optimized Resume</h2>
        <p className="text-gray-600">Download your ATS-optimized resume in professional formats</p>
      </div>

      <div className="bg-secondary/50 rounded-lg border p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={() => handleExport('pdf')}
            disabled={isExporting === 'pdf'}
            className="flex items-center justify-center space-x-3 p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-red-400 hover:bg-red-50 transition-colors disabled:opacity-50"
          >
            <FileText className="w-8 h-8 text-red-600" />
            <div className="text-left">
              <h3 className="font-semibold text-gray-900">PDF Format</h3>
              <p className="text-sm text-gray-600">ATS-friendly, widely accepted</p>
            </div>
            {isExporting === 'pdf' ? (
              <Download className="w-5 h-5 text-gray-400 animate-pulse" />
            ) : (
              <Download className="w-5 h-5 text-gray-400" />
            )}
          </button>

          <button
            onClick={() => handleExport('docx')}
            disabled={isExporting === 'docx'}
            className="flex items-center justify-center space-x-3 p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-colors disabled:opacity-50"
          >
            <FileIcon className="w-8 h-8 text-blue-600" />
            <div className="text-left">
              <h3 className="font-semibold text-gray-900">DOCX Format</h3>
              <p className="text-sm text-gray-600">Editable, customizable</p>
            </div>
            {isExporting === 'docx' ? (
              <Download className="w-5 h-5 text-gray-400 animate-pulse" />
            ) : (
              <Download className="w-5 h-5 text-gray-400" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};