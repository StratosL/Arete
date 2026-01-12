import { useState } from 'react';
import { Download, FileText, File as FileIcon, Layout, Sparkles } from 'lucide-react';
import { exportApi } from '@/lib/api';
import { logger } from '@/lib/logger';

interface DocumentExportProps {
  resumeId: string;
}

type TemplateType = 'classic' | 'modern';

const TEMPLATES = [
  {
    id: 'classic' as TemplateType,
    name: 'ATS Classic',
    description: 'Single column, maximum ATS compatibility. Direct PDF download.',
    icon: Layout,
    color: 'gray',
  },
  {
    id: 'modern' as TemplateType,
    name: 'Modern Professional',
    description: 'Clean design with accent colors. Opens print dialog.',
    icon: Sparkles,
    color: 'blue',
  },
];

export const DocumentExport = ({ resumeId }: DocumentExportProps) => {
  const [isExporting, setIsExporting] = useState<string | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<TemplateType>('classic');

  const handleExport = async (format: 'pdf' | 'docx') => {
    setIsExporting(format);
    try {
      await exportApi.exportResume(resumeId, format, selectedTemplate);
    } catch (error) {
      logger.error('Export failed:', error);
    } finally {
      setIsExporting(null);
    }
  };

  const selectedTemplateInfo = TEMPLATES.find(t => t.id === selectedTemplate);

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          Export Optimized Resume
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Choose a template and download your ATS-optimized resume
        </p>
      </div>

      {/* Template Selection */}
      <div className="bg-secondary/50 rounded-lg border p-6">
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
          Select Template Style
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {TEMPLATES.map((template) => {
            const Icon = template.icon;
            const isSelected = selectedTemplate === template.id;
            return (
              <button
                key={template.id}
                onClick={() => setSelectedTemplate(template.id)}
                className={`flex items-start space-x-3 p-4 rounded-lg border-2 transition-all text-left ${
                  isSelected
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-950/30'
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                }`}
              >
                <div
                  className={`p-2 rounded-lg ${
                    isSelected
                      ? 'bg-blue-100 dark:bg-blue-900'
                      : 'bg-gray-100 dark:bg-gray-800'
                  }`}
                >
                  <Icon
                    className={`w-5 h-5 ${
                      isSelected
                        ? 'text-blue-600 dark:text-blue-400'
                        : 'text-gray-500 dark:text-gray-400'
                    }`}
                  />
                </div>
                <div className="flex-1">
                  <h4
                    className={`font-medium ${
                      isSelected
                        ? 'text-blue-900 dark:text-blue-100'
                        : 'text-gray-900 dark:text-gray-100'
                    }`}
                  >
                    {template.name}
                  </h4>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    {template.description}
                  </p>
                </div>
                {isSelected && (
                  <div className="w-2 h-2 rounded-full bg-blue-500 mt-2" />
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Export Format Buttons */}
      <div className="bg-secondary/50 rounded-lg border p-6">
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
          Export Format
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={() => handleExport('pdf')}
            disabled={isExporting === 'pdf'}
            className="flex items-center justify-center space-x-3 p-6 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 transition-colors disabled:opacity-50"
          >
            <FileText className="w-8 h-8 text-red-600" />
            <div className="text-left">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100">PDF Format</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {selectedTemplate === 'modern'
                  ? 'Opens print dialog for PDF save'
                  : 'ATS-friendly, direct download'}
              </p>
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
            className="flex items-center justify-center space-x-3 p-6 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-950/20 transition-colors disabled:opacity-50"
          >
            <FileIcon className="w-8 h-8 text-blue-600" />
            <div className="text-left">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100">DOCX Format</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">Editable, customizable</p>
            </div>
            {isExporting === 'docx' ? (
              <Download className="w-5 h-5 text-gray-400 animate-pulse" />
            ) : (
              <Download className="w-5 h-5 text-gray-400" />
            )}
          </button>
        </div>

        {/* Template info note */}
        {selectedTemplateInfo && (
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-4 text-center">
            Using <span className="font-medium">{selectedTemplateInfo.name}</span> template
            {selectedTemplate === 'modern' && ' - A new tab will open for printing'}
          </p>
        )}
      </div>
    </div>
  );
};