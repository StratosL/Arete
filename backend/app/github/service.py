import json
from datetime import datetime

import requests

from app.core.llm import get_llm_response
from app.github.schemas import GitHubAnalysisResponse
from app.github.schemas import ImpactMetrics
from app.github.schemas import ProjectHighlight
from app.github.schemas import Repository
from app.github.schemas import TechStack


class GitHubService:
    """GitHub API integration and analysis service"""

    def __init__(self):
        self.base_url = "https://api.github.com"

    async def analyze_github_profile(self, username: str) -> GitHubAnalysisResponse:
        """Analyze GitHub profile and generate resume-ready insights"""
        
        # Fetch user data
        user_data = self._fetch_user_data(username)
        repos_data = self._fetch_user_repositories(username)
        
        # Calculate metrics
        impact_metrics = self._calculate_impact_metrics(user_data, repos_data)
        tech_stack = await self._extract_tech_stack(repos_data)
        top_repos = self._get_top_repositories(repos_data)
        
        # Generate insights
        project_highlights = await self._generate_project_highlights(top_repos)
        bullet_points = await self._generate_resume_bullet_points(
            username, impact_metrics, tech_stack, project_highlights
        )
        
        return GitHubAnalysisResponse(
            username=username,
            profile_url=f"https://github.com/{username}",
            impact_metrics=impact_metrics,
            tech_stack=tech_stack,
            top_repositories=top_repos,
            project_highlights=project_highlights,
            resume_bullet_points=bullet_points
        )

    def _fetch_user_data(self, username: str) -> dict:
        """Fetch user profile data from GitHub API"""
        response = requests.get(f"{self.base_url}/users/{username}")
        if response.status_code != 200:
            raise ValueError(f"GitHub user '{username}' not found")
        return response.json()

    def _fetch_user_repositories(self, username: str) -> list[dict]:
        """Fetch user repositories from GitHub API"""
        repos = []
        page = 1
        
        while len(repos) < 100:  # Limit to 100 repos for performance
            response = requests.get(
                f"{self.base_url}/users/{username}/repos",
                params={"page": page, "per_page": 100, "sort": "updated"}
            )
            if response.status_code != 200:
                break
                
            page_repos = response.json()
            if not page_repos:
                break
                
            repos.extend(page_repos)
            page += 1
            
        return repos

    def _calculate_impact_metrics(self, user_data: dict, repos_data: list[dict]) -> ImpactMetrics:
        """Calculate GitHub impact metrics"""
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
        total_forks = sum(repo.get("forks_count", 0) for repo in repos_data)
        
        return ImpactMetrics(
            total_stars=total_stars,
            total_forks=total_forks,
            total_repos=len(repos_data),
            public_repos=user_data.get("public_repos", 0),
            followers=user_data.get("followers", 0),
            following=user_data.get("following", 0),
            contributions_last_year=0  # GitHub API doesn't provide this easily
        )

    async def _extract_tech_stack(self, repos_data: list[dict]) -> TechStack:
        """Extract tech stack from repository languages"""
        # Collect all languages
        language_counts = {}
        for repo in repos_data:
            if repo.get("language"):
                lang = repo["language"]
                language_counts[lang] = language_counts.get(lang, 0) + 1

        # Get top languages
        top_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        primary_languages = [lang for lang, _ in top_languages]

        # Use LLM to categorize into frameworks and tools
        tech_analysis = await self._categorize_technologies(primary_languages)
        
        return TechStack(
            primary_languages=primary_languages[:5],
            frameworks=tech_analysis.get("frameworks", []),
            tools=tech_analysis.get("tools", [])
        )

    async def _categorize_technologies(self, languages: list[str]) -> dict:
        """Use LLM to categorize languages into frameworks and tools"""
        prompt = f"""
        Analyze these programming languages and categorize related frameworks and tools:
        Languages: {', '.join(languages)}
        
        Return JSON with frameworks and tools commonly used with these languages:
        {{
            "frameworks": ["React", "Django", "Express.js"],
            "tools": ["Docker", "Git", "AWS"]
        }}
        
        Focus on popular, resume-relevant technologies.
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = await get_llm_response(messages)
        
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            return {"frameworks": [], "tools": []}

    def _get_top_repositories(self, repos_data: list[dict]) -> list[Repository]:
        """Get top repositories by stars and activity"""
        # Filter out forks and sort by stars + recent activity
        own_repos = [repo for repo in repos_data if not repo.get("fork", False)]
        
        # Score repos by stars + recent activity
        def repo_score(repo):
            stars = repo.get("stargazers_count", 0)
            updated = datetime.fromisoformat(repo["updated_at"].replace("Z", "+00:00"))
            days_old = (datetime.now().astimezone() - updated).days
            recency_bonus = max(0, 365 - days_old) / 365  # Bonus for recent activity
            return stars + recency_bonus
        
        top_repos = sorted(own_repos, key=repo_score, reverse=True)[:5]
        
        return [
            Repository(
                name=repo["name"],
                description=repo.get("description"),
                stars=repo.get("stargazers_count", 0),
                forks=repo.get("forks_count", 0),
                language=repo.get("language"),
                languages={},  # Would need separate API call for detailed languages
                url=repo["html_url"],
                created_at=repo["created_at"],
                updated_at=repo["updated_at"],
                size=repo.get("size", 0)
            )
            for repo in top_repos
        ]

    async def _generate_project_highlights(self, repositories: list[Repository]) -> list[ProjectHighlight]:
        """Generate project highlights for resume"""
        highlights = []
        
        for repo in repositories[:3]:  # Top 3 projects
            impact_metric = self._format_impact_metric(repo)
            tech_stack = [repo.language] if repo.language else []
            
            highlights.append(ProjectHighlight(
                name=repo.name,
                description=repo.description or "Open source project",
                impact_metric=impact_metric,
                tech_stack=tech_stack,
                url=repo.url
            ))
        
        return highlights

    def _format_impact_metric(self, repo: Repository) -> str:
        """Format impact metric for resume"""
        if repo.stars > 0 and repo.forks > 0:
            return f"{repo.stars} stars, {repo.forks} forks"
        elif repo.stars > 0:
            return f"{repo.stars} stars"
        elif repo.forks > 0:
            return f"{repo.forks} forks"
        else:
            return "Active development"

    async def _generate_resume_bullet_points(
        self, 
        username: str, 
        metrics: ImpactMetrics, 
        tech_stack: TechStack, 
        highlights: list[ProjectHighlight]
    ) -> list[str]:
        """Generate resume-ready bullet points"""
        
        prompt = f"""
        Generate 3-5 professional resume bullet points for a software engineer based on their GitHub profile:
        
        Username: {username}
        Total Stars: {metrics.total_stars}
        Total Repositories: {metrics.total_repos}
        Followers: {metrics.followers}
        
        Primary Languages: {', '.join(tech_stack.primary_languages)}
        Frameworks: {', '.join(tech_stack.frameworks)}
        
        Top Projects:
        {chr(10).join([f"- {h.name}: {h.description} ({h.impact_metric})" for h in highlights])}
        
        Create bullet points that:
        - Start with action verbs
        - Include specific technologies
        - Mention quantifiable impact (stars, forks, repos)
        - Sound professional for a resume
        
        Return as JSON array: ["bullet point 1", "bullet point 2", ...]
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = await get_llm_response(messages)
        
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            # Fallback bullet points
            return [
                f"Developed {metrics.total_repos} open source projects using {', '.join(tech_stack.primary_languages[:3])}",
                f"Achieved {metrics.total_stars} stars across GitHub repositories demonstrating code quality",
                f"Built projects with {', '.join(tech_stack.frameworks[:2])} frameworks and modern development practices"
            ]


# Global service instance
github_service = GitHubService()