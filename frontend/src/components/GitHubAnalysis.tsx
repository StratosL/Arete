import { useState } from 'react';
import { Github, Star, GitFork, Code, TrendingUp, Plus, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface GitHubRepo {
  name: string;
  description: string;
  stars: number;
  forks: number;
  language: string;
  url: string;
}

interface GitHubMetrics {
  username: string;
  totalRepos: number;
  totalStars: number;
  totalCommits: number;
  topLanguages: string[];
  topRepos: GitHubRepo[];
  suggestedBullets: string[];
}

interface GitHubAnalysisProps {
  githubUrl: string;
  onAddBulletPoint: (bullet: string) => void;
}

export const GitHubAnalysis = ({ githubUrl, onAddBulletPoint }: GitHubAnalysisProps) => {
  const [metrics, setMetrics] = useState<GitHubMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [addedBullets, setAddedBullets] = useState<Set<string>>(new Set());

  const analyzeGitHub = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      // Mock data for now - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const mockMetrics: GitHubMetrics = {
        username: githubUrl.split('/').pop() || 'user',
        totalRepos: 24,
        totalStars: 156,
        totalCommits: 1247,
        topLanguages: ['TypeScript', 'Python', 'JavaScript', 'Go'],
        topRepos: [
          {
            name: 'ai-resume-optimizer',
            description: 'Full-stack resume optimization platform with AI',
            stars: 89,
            forks: 12,
            language: 'TypeScript',
            url: `${githubUrl}/ai-resume-optimizer`
          },
          {
            name: 'microservices-api',
            description: 'Scalable microservices architecture with Docker',
            stars: 45,
            forks: 8,
            language: 'Python',
            url: `${githubUrl}/microservices-api`
          },
          {
            name: 'react-dashboard',
            description: 'Modern dashboard with real-time analytics',
            stars: 22,
            forks: 5,
            language: 'JavaScript',
            url: `${githubUrl}/react-dashboard`
          }
        ],
        suggestedBullets: [
          'Developed 24+ open-source projects with 156 GitHub stars, demonstrating strong community engagement',
          'Built AI-powered resume optimization platform using TypeScript and Python, achieving 89 GitHub stars',
          'Architected scalable microservices infrastructure with Docker, contributing to 45-star repository',
          'Created modern React dashboard with real-time analytics, showcasing frontend expertise',
          'Maintained consistent development velocity with 1,247+ commits across multiple programming languages'
        ]
      };
      
      setMetrics(mockMetrics);
    } catch (err) {
      setError('Failed to analyze GitHub profile. Please check the URL and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddBullet = (bullet: string) => {
    onAddBulletPoint(bullet);
    setAddedBullets(prev => new Set([...prev, bullet]));
  };

  if (!githubUrl) return null;

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">GitHub Analysis</h2>
        <p className="text-gray-600">AI-powered insights from your GitHub profile</p>
      </div>

      {!metrics && !isLoading && (
        <Card>
          <CardContent className="p-6 text-center">
            <Github className="h-12 w-12 mx-auto mb-4 text-gray-400" />
            <p className="text-lg font-medium mb-2">Analyze GitHub Profile</p>
            <p className="text-gray-600 mb-4">Get AI-generated resume bullet points from your GitHub activity</p>
            <Button onClick={analyzeGitHub} className="flex items-center gap-2">
              <Github className="h-4 w-4" />
              Analyze {githubUrl.split('/').pop()}
            </Button>
          </CardContent>
        </Card>
      )}

      {isLoading && (
        <Card>
          <CardContent className="p-6 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Analyzing GitHub profile...</p>
          </CardContent>
        </Card>
      )}

      {error && (
        <Card>
          <CardContent className="p-6 text-center">
            <p className="text-red-600">{error}</p>
            <Button onClick={analyzeGitHub} variant="outline" className="mt-4">
              Try Again
            </Button>
          </CardContent>
        </Card>
      )}

      {metrics && (
        <div className="space-y-6">
          {/* GitHub Metrics */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Github className="h-5 w-5" />
                GitHub Metrics
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{metrics.totalRepos}</div>
                  <div className="text-sm text-gray-600">Repositories</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-600">{metrics.totalStars}</div>
                  <div className="text-sm text-gray-600">Stars</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{metrics.totalCommits}</div>
                  <div className="text-sm text-gray-600">Commits</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">{metrics.topLanguages.length}</div>
                  <div className="text-sm text-gray-600">Languages</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Top Projects */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code className="h-5 w-5" />
                Top Projects
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {metrics.topRepos.map((repo, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-900">{repo.name}</h4>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <div className="flex items-center gap-1">
                          <Star className="h-4 w-4" />
                          {repo.stars}
                        </div>
                        <div className="flex items-center gap-1">
                          <GitFork className="h-4 w-4" />
                          {repo.forks}
                        </div>
                      </div>
                    </div>
                    <p className="text-gray-600 mb-2">{repo.description}</p>
                    <span className="inline-block px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                      {repo.language}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Suggested Resume Bullets */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                AI-Generated Resume Bullets
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {metrics.suggestedBullets.map((bullet, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 border rounded-lg">
                    <div className="flex-1">
                      <p className="text-gray-800">{bullet}</p>
                    </div>
                    <Button
                      size="sm"
                      variant={addedBullets.has(bullet) ? "secondary" : "default"}
                      onClick={() => handleAddBullet(bullet)}
                      disabled={addedBullets.has(bullet)}
                      className="flex items-center gap-1"
                    >
                      {addedBullets.has(bullet) ? (
                        <>
                          <CheckCircle className="h-4 w-4" />
                          Added
                        </>
                      ) : (
                        <>
                          <Plus className="h-4 w-4" />
                          Add
                        </>
                      )}
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};