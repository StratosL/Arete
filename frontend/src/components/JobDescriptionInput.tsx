import { useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { FileText, Link, Briefcase } from 'lucide-react';
import { jobsApi } from '@/lib/api';
import { JobAnalysis, JobAnalysisRequest } from '@/types';

const jobAnalysisSchema = z.object({
  job_text: z.string().optional(),
  job_url: z.string().url().optional().or(z.literal('')),
}).refine(
  (data) => data.job_text || data.job_url,
  { message: "Either job text or URL is required" }
).refine(
  (data) => !data.job_text || data.job_text.length >= 50,
  { message: "Job description must be at least 50 characters", path: ["job_text"] }
);

type JobAnalysisForm = z.infer<typeof jobAnalysisSchema>;

interface JobDescriptionInputProps {
  // eslint-disable-next-line no-unused-vars
  onAnalysisSuccess: (jobAnalysis: JobAnalysis) => void;
}

export const JobDescriptionInput = ({ onAnalysisSuccess }: JobDescriptionInputProps) => {
  const [activeTab, setActiveTab] = useState<'text' | 'url'>('text');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { control, handleSubmit, formState: { errors }, reset, setValue } = useForm<JobAnalysisForm>({
    resolver: zodResolver(jobAnalysisSchema),
    defaultValues: {
      job_text: '',
      job_url: '',
    },
  });

  // Clear the inactive field when switching tabs
  const handleTabChange = (tab: 'text' | 'url') => {
    setActiveTab(tab);
    if (tab === 'text') {
      setValue('job_url', '');
    } else {
      setValue('job_text', '');
    }
  };

  const onSubmit = async (data: JobAnalysisForm) => {
    console.log('Form submitted with data:', data);
    console.log('Active tab:', activeTab);
    
    setIsAnalyzing(true);
    setError(null);

    try {
      const requestData: JobAnalysisRequest = activeTab === 'text' 
        ? { job_text: data.job_text }
        : { job_url: data.job_url };

      console.log('Sending request:', requestData);
      const response = await jobsApi.analyzeJob(requestData);
      
      onAnalysisSuccess(response);
      reset();
    } catch (err: any) {
      console.error('Analysis error:', err);
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Job Description Analysis</h2>
        <p className="text-gray-600">Enter a job description to analyze requirements and skills</p>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
        <button
          type="button"
          onClick={() => handleTabChange('text')}
          className={`flex-1 flex items-center justify-center space-x-2 py-2 px-4 rounded-md font-medium transition-colors ${
            activeTab === 'text'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Paste Text</span>
        </button>
        <button
          type="button"
          onClick={() => handleTabChange('url')}
          className={`flex-1 flex items-center justify-center space-x-2 py-2 px-4 rounded-md font-medium transition-colors ${
            activeTab === 'url'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <Link className="w-4 h-4" />
          <span>Job URL</span>
        </button>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Text Input Tab */}
        {activeTab === 'text' && (
          <div className="space-y-2">
            <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
              <Briefcase className="w-4 h-4" />
              <span>Job Description</span>
            </label>
            <Controller
              name="job_text"
              control={control}
              render={({ field }) => (
                <textarea
                  {...field}
                  placeholder="Paste the job description here..."
                  rows={8}
                  className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical ${
                    errors.job_text ? 'border-red-300' : 'border-gray-300'
                  }`}
                  data-invalid={!!errors.job_text}
                />
              )}
            />
            {errors.job_text && (
              <p className="text-sm text-red-600">{errors.job_text.message}</p>
            )}
            <p className="text-xs text-gray-500">
              Minimum 50 characters required for analysis
            </p>
          </div>
        )}

        {/* URL Input Tab */}
        {activeTab === 'url' && (
          <div className="space-y-2">
            <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
              <Link className="w-4 h-4" />
              <span>Job Posting URL</span>
            </label>
            <Controller
              name="job_url"
              control={control}
              render={({ field }) => (
                <input
                  {...field}
                  type="url"
                  placeholder="https://company.com/jobs/position"
                  className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.job_url ? 'border-red-300' : 'border-gray-300'
                  }`}
                  data-invalid={!!errors.job_url}
                />
              )}
            />
            {errors.job_url && (
              <p className="text-sm text-red-600">{errors.job_url.message}</p>
            )}
            <p className="text-xs text-gray-500">
              We'll scrape and analyze the job posting automatically
            </p>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="button"
          onClick={() => {
            console.log('BUTTON CLICKED - TEST');
            
            // Get current form values
            const formData = control._formValues;
            console.log('Current form values:', JSON.stringify(formData, null, 2));
            console.log('Form errors:', JSON.stringify(errors, null, 2));
            console.log('Active tab:', activeTab);
            
            // Try to trigger validation manually
            handleSubmit(
              (data) => {
                console.log('Form validation PASSED, data:', JSON.stringify(data, null, 2));
                onSubmit(data);
              },
              (errors) => {
                console.log('Form validation FAILED, errors:', JSON.stringify(errors, null, 2));
              }
            )();
          }}
          disabled={isAnalyzing}
          className={`w-full py-3 px-4 rounded-md font-medium transition-colors ${
            isAnalyzing
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          {isAnalyzing ? 'Analyzing Job...' : 'Analyze Job Description'}
        </button>
      </form>
    </div>
  );
};