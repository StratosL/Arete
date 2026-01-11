import { useState } from 'react';
import { ResumeUpload } from './components/ResumeUpload';
import { ResumeDisplay } from './components/ResumeDisplay';
import { JobDescriptionInput } from './components/JobDescriptionInput';
import { JobAnalysisDisplay } from './components/JobAnalysisDisplay';
import { OptimizationDisplay } from './components/OptimizationDisplay';
import { CoverLetterDisplay } from './components/CoverLetterDisplay';
import { DocumentExport } from './components/DocumentExport';
import { GitHubAnalysis } from './components/GitHubAnalysis';
import { ErrorBoundary } from './components/ErrorBoundary';
import { ThemeProvider } from "./components/theme-provider"
import { ModeToggle } from "./components/mode-toggle"
import { Button } from "./components/ui/button"
import { ResumeData, JobAnalysis } from './types';
import './App.css';

interface GitHubMetrics {
  username: string;
  totalRepos: number;
  totalStars: number;
  totalCommits: number;
  topLanguages: string[];
  topRepos: Array<{
    name: string;
    description: string;
    stars: number;
    forks: number;
    language: string;
    url: string;
  }>;
  suggestedBullets: string[];
}

function App() {
  const [resumeData, setResumeData] = useState<ResumeData | null>(null);
  const [jobAnalysis, setJobAnalysis] = useState<JobAnalysis | null>(null);
  const [githubUrl, setGithubUrl] = useState('');
  const [githubMetrics, setGithubMetrics] = useState<GitHubMetrics | null>(null);

  const handleUploadSuccess = (data: ResumeData) => {
    setResumeData(data);
  };

  const handleJobAnalysisSuccess = (analysis: JobAnalysis) => {
    setJobAnalysis(analysis);
  };

  const handleAddBulletPoint = (bullet: string) => {
    if (resumeData) {
      const updatedResume = { ...resumeData };
      
      // Find or create GitHub experience entry
      let githubExp = updatedResume.experience.find(exp => 
        exp.title.toLowerCase().includes('github') || exp.company.toLowerCase().includes('github')
      );
      
      if (!githubExp) {
        githubExp = {
          title: 'Open Source Contributions',
          company: 'GitHub Projects',
          duration: 'Ongoing',
          description: [],
          technologies: []
        };
        updatedResume.experience.unshift(githubExp);
      }
      
      // Add bullet if not already present
      if (!githubExp.description.includes(bullet)) {
        githubExp.description.push(bullet);
        setResumeData(updatedResume);
      }
    }
  };

  const handleReset = () => {
    setResumeData(null);
    setJobAnalysis(null);
    setGithubUrl('');
    setGithubMetrics(null);
  };

  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <div className="min-h-screen bg-background font-sans text-foreground">
        <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div className="flex flex-col">
              <h1 className="text-2xl font-serif font-medium tracking-tight text-foreground">Arete</h1>
              <p className="text-xs text-muted-foreground hidden sm:block">AI-Powered Resume Optimizer</p>
            </div>
            <div className="flex items-center gap-4">
              {resumeData && (
                <Button
                  onClick={handleReset}
                  variant="outline"
                  size="sm"
                >
                  Start Over
                </Button>
              )}
              <ModeToggle />
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
          {!resumeData ? (
            <ResumeUpload onUploadSuccess={handleUploadSuccess} githubUrl={githubUrl} setGithubUrl={setGithubUrl} />
          ) : !jobAnalysis ? (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <ResumeDisplay resumeData={resumeData} />
              {githubUrl && (
                <div className="border-t pt-8">
                  <ErrorBoundary>
                    <GitHubAnalysis 
                      githubUrl={githubUrl} 
                      onAddBulletPoint={handleAddBulletPoint}
                      metrics={githubMetrics}
                      setMetrics={setGithubMetrics}
                    />
                  </ErrorBoundary>
                </div>
              )}
              <div className="border-t pt-8">
                <JobDescriptionInput onAnalysisSuccess={handleJobAnalysisSuccess} />
              </div>
            </div>
          ) : (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <ResumeDisplay resumeData={resumeData} />
              {githubUrl && (
                <div className="border-t pt-8">
                  <ErrorBoundary>
                    <GitHubAnalysis 
                      githubUrl={githubUrl} 
                      onAddBulletPoint={handleAddBulletPoint}
                      metrics={githubMetrics}
                      setMetrics={setGithubMetrics}
                    />
                  </ErrorBoundary>
                </div>
              )}
              <div className="border-t pt-8">
                <JobAnalysisDisplay jobAnalysis={jobAnalysis} />
              </div>
              <div className="border-t pt-8">
                <OptimizationDisplay resumeData={resumeData} jobAnalysis={jobAnalysis} />
              </div>
              <div className="border-t pt-8">
                <ErrorBoundary>
                  <CoverLetterDisplay resumeData={resumeData} jobAnalysis={jobAnalysis} />
                </ErrorBoundary>
              </div>
              <div className="border-t pt-8">
                <DocumentExport resumeId={resumeData.id} />
              </div>
            </div>
          )}
        </main>

        <footer className="border-t py-6 md:py-0 mt-8">
          <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row mx-auto px-4">
            <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
              Arete - Transforming resumes with AI for tech professionals
            </p>
          </div>
        </footer>
      </div>
    </ThemeProvider>
  );
}

export default App;
