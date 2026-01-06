import React from 'react';
import { ResumeData } from '@/types';
import { User, Briefcase, Code, FolderOpen, GraduationCap } from 'lucide-react';

interface ResumeDisplayProps {
  resumeData: ResumeData;
}

export const ResumeDisplay: React.FC<ResumeDisplayProps> = ({ resumeData }) => {
  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-8">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Parsed Resume Data</h2>
        <p className="text-gray-600">Review the extracted information from your resume</p>
      </div>

      {/* Personal Info */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <User className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">Personal Information</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-500">Name</p>
            <p className="font-medium">{resumeData.personal_info.name}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Email</p>
            <p className="font-medium">{resumeData.personal_info.email}</p>
          </div>
          {resumeData.personal_info.phone && (
            <div>
              <p className="text-sm text-gray-500">Phone</p>
              <p className="font-medium">{resumeData.personal_info.phone}</p>
            </div>
          )}
          {resumeData.personal_info.location && (
            <div>
              <p className="text-sm text-gray-500">Location</p>
              <p className="font-medium">{resumeData.personal_info.location}</p>
            </div>
          )}
        </div>
      </div>

      {/* Experience */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Briefcase className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">Experience</h3>
        </div>
        <div className="space-y-6">
          {resumeData.experience.map((exp, index) => (
            <div key={index} className="border-l-2 border-blue-200 pl-4">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-2">
                <h4 className="font-semibold text-gray-900">{exp.title}</h4>
                <span className="text-sm text-gray-500">{exp.duration}</span>
              </div>
              <p className="text-blue-600 font-medium mb-2">{exp.company}</p>
              <ul className="list-disc list-inside space-y-1 mb-3">
                {exp.description.map((desc, i) => (
                  <li key={i} className="text-sm text-gray-600">{desc}</li>
                ))}
              </ul>
              <div className="flex flex-wrap gap-2">
                {exp.technologies.map((tech, i) => (
                  <span key={i} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Skills */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Code className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">Skills</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Technical Skills</h4>
            <div className="flex flex-wrap gap-2">
              {resumeData.skills.technical.map((skill, i) => (
                <span key={i} className="px-2 py-1 bg-blue-100 text-blue-700 text-sm rounded">
                  {skill}
                </span>
              ))}
            </div>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Frameworks</h4>
            <div className="flex flex-wrap gap-2">
              {resumeData.skills.frameworks.map((framework, i) => (
                <span key={i} className="px-2 py-1 bg-green-100 text-green-700 text-sm rounded">
                  {framework}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Projects */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <FolderOpen className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">Projects</h3>
        </div>
        <div className="space-y-4">
          {resumeData.projects.map((project, index) => (
            <div key={index} className="border border-gray-100 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-2">{project.name}</h4>
              <p className="text-gray-600 mb-3">{project.description}</p>
              <div className="flex flex-wrap gap-2 mb-3">
                {project.technologies.map((tech, i) => (
                  <span key={i} className="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded">
                    {tech}
                  </span>
                ))}
              </div>
              {project.impact_metrics.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-1">Impact:</p>
                  <ul className="list-disc list-inside">
                    {project.impact_metrics.map((metric, i) => (
                      <li key={i} className="text-sm text-gray-600">{metric}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Education */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <GraduationCap className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">Education</h3>
        </div>
        <div className="space-y-4">
          {resumeData.education.map((edu, index) => (
            <div key={index} className="flex flex-col md:flex-row md:items-center md:justify-between">
              <div>
                <h4 className="font-semibold text-gray-900">{edu.degree}</h4>
                <p className="text-blue-600">{edu.institution}</p>
              </div>
              <div className="text-right">
                <p className="text-gray-500">{edu.graduation_year}</p>
                {edu.gpa && <p className="text-sm text-gray-500">GPA: {edu.gpa}</p>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
