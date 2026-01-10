import { useState } from 'react';
import { ResumeData, JobAnalysis } from '@/types';
import { optimizationApi } from '@/lib/api';
import { FileText, Download, Loader2, CheckCircle, AlertCircle } from 'lucide-react';

interface CoverLetterDisplayProps {
  resumeData?: ResumeData;
  jobAnalysis?: JobAnalysis;
}

export const CoverLetterDisplay = ({ resumeData, jobAnalysis }: CoverLetterDisplayProps) => {
  const [coverLetter, setCoverLetter] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string>('');

  if (!resumeData || !jobAnalysis) {
    return (
      <div className="w-full max-w-4xl mx-auto p-6">
        <div className="p-6 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div className="flex items-center gap-2 mb-2">
            <AlertCircle className="h-5 w-5 text-yellow-600" />
            <h3 className="text-lg font-semibold text-yellow-800">Missing Data</h3>
          </div>
          <p className="text-yellow-700">
            Please complete resume upload and job analysis before generating a cover letter.
          </p>
        </div>
      </div>
    );
  }

  const generateCoverLetter = async () => {
    if (!resumeData?.id || !jobAnalysis?.id) {
      setError('Resume and job analysis required');
      return;
    }

    setIsGenerating(true);
    setError('');

    try {
      const response = await optimizationApi.generateCoverLetter(resumeData.id, jobAnalysis.id);
      
      if (!response?.cover_letter) {
        throw new Error('Invalid response: missing cover_letter field');
      }
      
      setCoverLetter(response.cover_letter);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to generate cover letter. Please try again.';
      setError(errorMessage);
    } finally {
      setIsGenerating(false);
    }
  };

  const downloadCoverLetter = () => {
    if (!coverLetter) {
      return;
    }

    try {
      const blob = new Blob([coverLetter], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      
      // Safe filename generation
      const safeCompany = (jobAnalysis?.company || 'company').replace(/[^a-zA-Z0-9]/g, '-');
      const safeTitle = (jobAnalysis?.title || 'position').replace(/[^a-zA-Z0-9]/g, '-');
      a.download = `cover-letter-${safeCompany}-${safeTitle}.txt`;
      
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to download cover letter');
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Cover Letter</h2>
        <p className="text-gray-600">AI-generated cover letter for {jobAnalysis.title} at {jobAnalysis.company}</p>
      </div>

      <div className="bg-secondary/50 rounded-lg border p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <FileText className="h-5 w-5 text-blue-600" />
            <h3 className="text-lg font-semibold">Cover Letter Generation</h3>
          </div>
          
          {!coverLetter && (
            <button
              onClick={generateCoverLetter}
              disabled={isGenerating}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              {isGenerating ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <FileText className="h-4 w-4" />
              )}
              {isGenerating ? 'Generating...' : 'Generate Cover Letter'}
            </button>
          )}
        </div>

        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg mb-4">
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        {coverLetter ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-green-600">
                <CheckCircle className="h-4 w-4" />
                <span className="text-sm font-medium">Cover letter generated successfully</span>
              </div>
              
              <div className="flex gap-2">
                <button
                  onClick={generateCoverLetter}
                  disabled={isGenerating}
                  className="flex items-center gap-2 px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 transition-colors"
                >
                  {isGenerating ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : null}
                  {isGenerating ? 'Regenerating...' : 'Regenerate'}
                </button>
                <button
                  onClick={downloadCoverLetter}
                  className="flex items-center gap-2 px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                >
                  <Download className="h-4 w-4" />
                  Download
                </button>
              </div>
            </div>

            <div className="p-4 bg-white border rounded-lg">
              <div className="whitespace-pre-wrap text-sm leading-relaxed text-gray-800">
                {coverLetter}
              </div>
            </div>
          </div>
        ) : !isGenerating ? (
          <div className="p-8 text-center text-gray-500 border-2 border-dashed border-gray-300 rounded-lg">
            <FileText className="h-12 w-12 mx-auto mb-4 text-gray-400" />
            <p className="text-lg font-medium mb-2">No cover letter generated yet</p>
            <p className="text-sm">Click "Generate Cover Letter" to create a personalized cover letter for this position.</p>
          </div>
        ) : null}
      </div>
    </div>
  );
};
