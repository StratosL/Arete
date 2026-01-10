import { useState } from 'react';
import { ResumeData, JobAnalysis, OptimizationProgress, OptimizationSuggestion } from '@/types';
import { optimizationApi } from '@/lib/api';
import { Zap, CheckCircle, AlertCircle, Loader2, Play, Square, Lightbulb, TrendingUp, Save } from 'lucide-react';

interface OptimizationDisplayProps {
  resumeData: ResumeData;
  jobAnalysis: JobAnalysis;
}

export const OptimizationDisplay = ({ resumeData, jobAnalysis }: OptimizationDisplayProps) => {
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [allSuggestions, setAllSuggestions] = useState<OptimizationSuggestion[]>([]);
  const [currentProgress, setCurrentProgress] = useState<OptimizationProgress | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startOptimization = async () => {
    setIsOptimizing(true);
    setAllSuggestions([]);
    setCurrentProgress(null);
    setError(null);

    try {
      const response = await optimizationApi.startOptimization({
        resume_id: resumeData.id,
        job_id: jobAnalysis.id,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              setCurrentProgress(data);
              if (data.suggestions?.length > 0) {
                setAllSuggestions(data.suggestions);
              }
              if (data.completed) {
                setIsOptimizing(false);
                return;
              }
            } catch (err) {
              console.error('Failed to parse SSE data:', err);
            }
          }
        }
      }
    } catch (err: any) {
      setError(err.message || 'Optimization failed');
      setIsOptimizing(false);
    }
  };

  const stopOptimization = () => {
    setIsOptimizing(false);
  };

  const toggleSuggestion = (index: number) => {
    setAllSuggestions(prev => prev.map((s, i) =>
      i === index ? { ...s, accepted: !s.accepted } : s
    ));
  };

  const applySuggestions = async () => {
    setIsSaving(true);
    try {
      await optimizationApi.saveOptimization(resumeData.id, allSuggestions, resumeData);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (error) {
      console.error('Failed to save optimizations:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'border-red-500 bg-red-50';
      case 'medium': return 'border-yellow-500 bg-yellow-50';
      case 'low': return 'border-green-500 bg-green-50';
      default: return 'border-blue-500 bg-blue-50';
    }
  };

  const getImpactIcon = (impact: string) => {
    switch (impact) {
      case 'high': return <TrendingUp className="w-4 h-4 text-red-600" />;
      case 'medium': return <Lightbulb className="w-4 h-4 text-yellow-600" />;
      case 'low': return <CheckCircle className="w-4 h-4 text-green-600" />;
      default: return <Lightbulb className="w-4 h-4 text-blue-600" />;
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Resume Optimization</h2>
        <p className="text-gray-600">AI-powered optimization for {jobAnalysis.title} at {jobAnalysis.company}</p>
      </div>

      {/* Control Panel */}
      <div className="bg-secondary/50 rounded-lg border p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Zap className="w-5 h-5 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900">Optimization Control</h3>
          </div>

          {!isOptimizing ? (
            <button
              onClick={startOptimization}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              <Play className="w-4 h-4" />
              <span>Start Optimization</span>
            </button>
          ) : (
            <button
              onClick={stopOptimization}
              className="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
            >
              <Square className="w-4 h-4" />
              <span>Stop</span>
            </button>
          )}
        </div>

        {/* Progress Bar */}
        {isOptimizing && currentProgress && (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">{currentProgress.message}</span>
              <span className="text-gray-600">{currentProgress.progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${currentProgress.progress}%` }}
              />
            </div>
          </div>
        )}

        {/* Connection Status */}
        <div className="flex items-center space-x-2 mt-4">
          {isOptimizing ? (
            <>
              <Loader2 className="w-4 h-4 text-green-500 animate-spin" />
              <span className="text-sm text-green-600">Processing optimization...</span>
            </>
          ) : error ? (
            <>
              <AlertCircle className="w-4 h-4 text-red-500" />
              <span className="text-sm text-red-600">{error}</span>
            </>
          ) : (
            <>
              <CheckCircle className="w-4 h-4 text-gray-400" />
              <span className="text-sm text-gray-500">Ready to optimize</span>
            </>
          )}
        </div>
      </div>

      {/* Optimization Suggestions */}
      {allSuggestions.length > 0 && (
        <div className="bg-secondary/50 rounded-lg border p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">
              Optimization Suggestions ({allSuggestions.length})
            </h3>
            <button
              onClick={applySuggestions}
              disabled={isSaving || !allSuggestions.some(s => s.accepted)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md font-medium transition-colors ${isSaving || !allSuggestions.some(s => s.accepted)
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : saveSuccess
                    ? 'bg-green-600 text-white'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
            >
              <Save className="w-4 h-4" />
              <span>
                {isSaving ? 'Saving...' : saveSuccess ? 'Saved!' : 'Apply Selected'}
              </span>
            </button>
          </div>
          <div className="space-y-4">
            {allSuggestions.map((suggestion, index) => (
              <div key={index} className={`border-l-4 p-4 rounded-r-lg ${getImpactColor(suggestion.impact)}`}>
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    {getImpactIcon(suggestion.impact)}
                    <span className="text-sm font-medium text-gray-700 capitalize">
                      {suggestion.section} - {suggestion.type.replace('_', ' ')}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-gray-500 capitalize">
                      {suggestion.impact} Impact
                    </span>
                    <button
                      onClick={() => toggleSuggestion(index)}
                      className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${suggestion.accepted
                          ? 'bg-green-600 text-white hover:bg-green-700'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                        }`}
                    >
                      {suggestion.accepted ? 'Selected' : 'Select this'}
                    </button>
                  </div>
                </div>

                <div className="space-y-2">
                  <p className="text-sm text-gray-600">{suggestion.reason}</p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="font-medium text-gray-700">Original:</span>
                      <p className="text-gray-600 bg-gray-100 p-2 rounded mt-1">{suggestion.original}</p>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Suggested:</span>
                      <p className="text-gray-600 bg-white p-2 rounded border mt-1">{suggestion.suggested}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};