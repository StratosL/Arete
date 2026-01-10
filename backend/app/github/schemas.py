from pydantic import BaseModel


class GitHubAnalyzeRequest(BaseModel):
    username: str


class Repository(BaseModel):
    name: str
    description: str | None
    stars: int
    forks: int
    language: str | None
    languages: dict[str, int]
    url: str
    created_at: str
    updated_at: str
    size: int


class ImpactMetrics(BaseModel):
    total_stars: int
    total_forks: int
    total_repos: int
    public_repos: int
    followers: int
    following: int
    contributions_last_year: int


class TechStack(BaseModel):
    primary_languages: list[str]
    frameworks: list[str]
    tools: list[str]


class ProjectHighlight(BaseModel):
    name: str
    description: str
    impact_metric: str
    tech_stack: list[str]
    url: str


class GitHubAnalysisResponse(BaseModel):
    username: str
    profile_url: str
    impact_metrics: ImpactMetrics
    tech_stack: TechStack
    top_repositories: list[Repository]
    project_highlights: list[ProjectHighlight]
    resume_bullet_points: list[str]