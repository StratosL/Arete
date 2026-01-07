import { JobAnalysis } from '@/types';
import { Briefcase, Target, Code, TrendingUp, CheckCircle } from 'lucide-react';

interface JobAnalysisDisplayProps {
  jobAnalysis: JobAnalysis;
}

export const JobAnalysisDisplay = ({ jobAnalysis }: JobAnalysisDisplayProps) => {
  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-8">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Job Analysis Results</h2>
        <p className="text-gray-600">AI-powered analysis of job requirements and skills</p>
      </div>

      {/* Job Overview */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Briefcase className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">Job Overview</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-500">Position</p>
            <p className="font-medium text-lg">{jobAnalysis.title}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Company</p>
            <p className="font-medium text-lg">{jobAnalysis.company}</p>
          </div>
          <div className="md:col-span-2">
            <p className="text-sm text-gray-500">Experience Level</p>
            <p className="font-medium">{jobAnalysis.experience_level}</p>
          </div>
        </div>
      </div>

      {/* Required Skills */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Target className="w-5 h-5 text-red-600" />
          <h3 className="text-lg font-semibold text-gray-900">Required Skills</h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {jobAnalysis.required_skills.map((skill, i) => (
            <span key={i} className="px-3 py-1 bg-red-100 text-red-700 text-sm rounded-full font-medium">
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Preferred Skills */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <TrendingUp className="w-5 h-5 text-green-600" />
          <h3 className="text-lg font-semibold text-gray-900">Preferred Skills</h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {jobAnalysis.preferred_skills.map((skill, i) => (
            <span key={i} className="px-3 py-1 bg-green-100 text-green-700 text-sm rounded-full">
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Technologies */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Code className="w-5 h-5 text-purple-600" />
          <h3 className="text-lg font-semibold text-gray-900">Technologies</h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {jobAnalysis.technologies.map((tech, i) => (
            <span key={i} className="px-3 py-1 bg-purple-100 text-purple-700 text-sm rounded-full">
              {tech}
            </span>
          ))}
        </div>
      </div>

      {/* Key Requirements */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <CheckCircle className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">Key Requirements</h3>
        </div>
        <ul className="space-y-2">
          {jobAnalysis.key_requirements.map((req, i) => (
            <li key={i} className="flex items-start space-x-2">
              <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
              <span className="text-gray-700">{req}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};