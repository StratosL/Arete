import React, { useState } from 'react';
import { ResumeUpload } from './components/ResumeUpload';
import { ResumeDisplay } from './components/ResumeDisplay';
import { ResumeData } from './types';
import './App.css';

function App() {
  const [resumeData, setResumeData] = useState<ResumeData | null>(null);

  const handleUploadSuccess = (data: ResumeData) => {
    setResumeData(data);
  };

  const handleReset = () => {
    setResumeData(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Arete</h1>
              <p className="text-sm text-gray-600">AI-Powered Resume Optimizer for Tech Professionals</p>
            </div>
            {resumeData && (
              <button
                onClick={handleReset}
                className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
              >
                Upload New Resume
              </button>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!resumeData ? (
          <ResumeUpload onUploadSuccess={handleUploadSuccess} />
        ) : (
          <ResumeDisplay resumeData={resumeData} />
        )}
      </main>

      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            Arete - Transforming resumes with AI for tech professionals
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
