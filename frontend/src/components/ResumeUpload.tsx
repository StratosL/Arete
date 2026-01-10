import { useState, useCallback } from 'react';
import { Upload, FileText, Github } from 'lucide-react';
import { resumeApi } from '@/lib/api';
import { ResumeData } from '@/types';
import { GitHubAnalysis } from './GitHubAnalysis';

interface ResumeUploadProps {
  // eslint-disable-next-line no-unused-vars
  onUploadSuccess: (resumeData: ResumeData) => void;
}

export const ResumeUpload = ({ onUploadSuccess }: ResumeUploadProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [githubUrl, setGithubUrl] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploadedResume, setUploadedResume] = useState<ResumeData | null>(null);
  const [githubBullets, setGithubBullets] = useState<string[]>([]);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      setFile(files[0]);
      setError(null);
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      setFile(files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      const response = await resumeApi.uploadResume(file, githubUrl || undefined);

      if (response.status === 'success' && response.data) {
        setUploadedResume(response.data);
        onUploadSuccess(response.data);
      } else {
        setError(response.message || 'Upload failed');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleAddBulletPoint = (bullet: string) => {
    setGithubBullets(prev => [...prev, bullet]);
    // In a real implementation, you would update the resume data
    // and potentially call an API to save the updated resume
  };

  return (
    <div className="space-y-6">
      <div className="w-full max-w-2xl mx-auto p-6 space-y-6">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload Your Resume</h2>
          <p className="text-gray-600 dark:text-[hsl(var(--h2-foreground))]">Upload your resume to get started with AI-powered optimization</p>
        </div>

        {/* File Drop Zone */}
        <div
          className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${dragActive
            ? 'border-blue-400 bg-blue-50'
            : file
              ? 'border-green-400 bg-green-50'
              : 'border-gray-300 hover:border-gray-400'
            }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleFileSelect}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />

          <div className="space-y-4">
            {file ? (
              <div className="flex items-center justify-center space-x-2 text-green-600">
                <FileText className="w-8 h-8" />
                <span className="font-medium">{file.name}</span>
              </div>
            ) : (
              <div className="space-y-2">
                <Upload className="w-12 h-12 mx-auto text-gray-400" />
                <div>
                  <p className="text-lg font-medium text-gray-900 dark:text-[hsl(var(--h2-foreground))]">Drop your resume here</p>
                  <p className="text-sm text-gray-500">or click to browse</p>
                </div>
              </div>
            )}

            <p className="text-xs text-gray-500">
              Supports PDF, DOCX, and TXT files (max 10MB)
            </p>
          </div>
        </div>

        {/* GitHub URL Input */}
        <div className="space-y-2">
          <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 dark:text-[hsl(var(--h2-foreground))]">
            <Github className="w-4 h-4" />
            <span>GitHub Profile (Optional)</span>
          </label>
          <input
            type="url"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            placeholder="https://github.com/username"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p className="text-xs text-gray-500 dark:text-[hsl(var(--h2-foreground))]">
            Include your GitHub profile for enhanced project analysis
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          disabled={!file || isUploading}
          className={`w-full py-3 px-4 rounded-md font-medium transition-colors ${!file || isUploading
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
        >
          {isUploading ? 'Processing Resume...' : 'Upload & Parse Resume'}
        </button>
      </div>

      {/* GitHub Analysis Section */}
      {uploadedResume && githubUrl && (
        <GitHubAnalysis 
          githubUrl={githubUrl} 
          onAddBulletPoint={handleAddBulletPoint}
        />
      )}
    </div>
  );
};
