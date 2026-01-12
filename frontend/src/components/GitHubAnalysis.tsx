import { useState } from 'react';
import { Github, Star, GitFork, Code, TrendingUp, Plus, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { logger } from '@/lib/logger';

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
  metrics: GitHubMetrics | null;
  setMetrics: (metrics: GitHubMetrics | null) => void;
}

export const GitHubAnalysis = ({ githubUrl, onAddBulletPoint, metrics, setMetrics }: GitHubAnalysisProps) => {
  logger.debug('GitHubAnalysis rendered with:', { githubUrl });
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [addedBullets, setAddedBullets] = useState<Set<string>>(new Set());

  const analyzeGitHub = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const username = githubUrl.split('/').pop() || 'user';
      const response = await fetch('http://localhost:8000/github/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username })
      });
      
      if (!response.ok) throw new Error('GitHub analysis failed');
      
      const data = await response.json();
      
      const metrics: GitHubMetrics = {
        username: data.username,
        totalRepos: data.impact_metrics.total_repos,
        totalStars: data.impact_metrics.total_stars,
        totalCommits: data.impact_metrics.contributions_last_year,
        topLanguages: data.tech_stack.primary_languages,
        topRepos: data.top_repositories.map((repo: any) => ({
          name: repo.name,
          description: repo.description || 'No description',
          stars: repo.stars,
          forks: repo.forks,
          language: repo.language || 'Unknown',
          url: repo.url
        })),
        suggestedBullets: data.resume_bullet_points
      };
      
      setMetrics(metrics);
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
                      <p style={{ color: '#BCBAB3' }}>{bullet}</p>
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