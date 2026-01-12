"""
Unit tests for GitHub service
"""
import json
from unittest.mock import patch, Mock
import pytest
import requests

from app.github.service import GitHubService
from app.github.schemas import GitHubAnalysisResponse


class TestGitHubService:
    """Test GitHubService methods"""

    def setup_method(self):
        """Setup test fixtures"""
        self.service = GitHubService()

    def test_fetch_user_data_success(self):
        """Test successful user data fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "login": "testuser",
            "public_repos": 25,
            "followers": 100,
            "following": 50
        }

        with patch('requests.get', return_value=mock_response):
            result = self.service._fetch_user_data("testuser")
            
            assert result["login"] == "testuser"
            assert result["public_repos"] == 25
            assert result["followers"] == 100

    def test_fetch_user_data_not_found(self):
        """Test user not found error"""
        mock_response = Mock()
        mock_response.status_code = 404

        with patch('requests.get', return_value=mock_response):
            with pytest.raises(ValueError, match="GitHub user 'invalid' not found"):
                self.service._fetch_user_data("invalid")

    def test_fetch_user_repositories_success(self):
        """Test successful repository fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            [
                {
                    "name": "test-repo",
                    "stargazers_count": 10,
                    "forks_count": 5,
                    "language": "Python",
                    "updated_at": "2023-01-01T00:00:00Z"
                }
            ],
            []  # Empty response to stop pagination
        ]

        with patch('requests.get') as mock_get:
            mock_get.return_value = mock_response
            result = self.service._fetch_user_repositories("testuser")
            
            assert len(result) == 1
            assert result[0]["name"] == "test-repo"
            assert result[0]["stargazers_count"] == 10

    def test_calculate_impact_metrics(self):
        """Test impact metrics calculation"""
        user_data = {
            "public_repos": 25,
            "followers": 100,
            "following": 50
        }
        repos_data = [
            {"stargazers_count": 10, "forks_count": 5},
            {"stargazers_count": 20, "forks_count": 3},
            {"stargazers_count": 0, "forks_count": 1}
        ]

        result = self.service._calculate_impact_metrics(user_data, repos_data)
        
        assert result.total_stars == 30
        assert result.total_forks == 9
        assert result.total_repos == 3
        assert result.public_repos == 25
        assert result.followers == 100

    @pytest.mark.asyncio
    async def test_extract_tech_stack(self):
        """Test tech stack extraction"""
        repos_data = [
            {"language": "Python"},
            {"language": "JavaScript"},
            {"language": "Python"},  # Duplicate
            {"language": None}  # No language
        ]

        mock_response = json.dumps({
            "frameworks": ["Django", "React"],
            "tools": ["Docker", "Git"]
        })

        with patch('app.github.service.get_llm_response', return_value=mock_response):
            result = await self.service._extract_tech_stack(repos_data)
            
            assert "Python" in result.primary_languages
            assert "JavaScript" in result.primary_languages
            assert "Django" in result.frameworks
            assert "React" in result.frameworks

    @pytest.mark.asyncio
    async def test_categorize_technologies_success(self):
        """Test technology categorization"""
        languages = ["Python", "JavaScript", "Go"]
        
        mock_response = json.dumps({
            "frameworks": ["Django", "React", "Gin"],
            "tools": ["Docker", "Webpack", "Git"]
        })

        with patch('app.github.service.get_llm_response', return_value=mock_response):
            result = await self.service._categorize_technologies(languages)
            
            assert "Django" in result["frameworks"]
            assert "Docker" in result["tools"]

    @pytest.mark.asyncio
    async def test_categorize_technologies_json_error(self):
        """Test categorization with JSON parse error"""
        languages = ["Python"]
        
        with patch('app.github.service.get_llm_response', return_value="Invalid JSON"):
            result = await self.service._categorize_technologies(languages)
            
            assert result == {"frameworks": [], "tools": []}

    def test_get_top_repositories(self):
        """Test top repositories selection"""
        repos_data = [
            {
                "name": "high-stars",
                "stargazers_count": 100,
                "forks_count": 20,
                "fork": False,
                "language": "Python",
                "html_url": "https://github.com/user/high-stars",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-12-01T00:00:00Z",
                "size": 1000,
                "description": "Popular repo"
            },
            {
                "name": "low-stars",
                "stargazers_count": 5,
                "forks_count": 1,
                "fork": False,
                "language": "JavaScript",
                "html_url": "https://github.com/user/low-stars",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-12-01T00:00:00Z",
                "size": 500,
                "description": "Less popular repo"
            },
            {
                "name": "forked-repo",
                "stargazers_count": 50,
                "forks_count": 10,
                "fork": True,  # This should be filtered out
                "language": "Python",
                "html_url": "https://github.com/user/forked-repo",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-12-01T00:00:00Z",
                "size": 800,
                "description": "Forked repo"
            }
        ]

        result = self.service._get_top_repositories(repos_data)
        
        # Should exclude forks and sort by stars
        assert len(result) == 2
        assert result[0].name == "high-stars"
        assert result[0].stars == 100
        assert result[1].name == "low-stars"

    @pytest.mark.asyncio
    async def test_generate_project_highlights(self):
        """Test project highlights generation"""
        from app.github.schemas import Repository
        
        repositories = [
            Repository(
                name="awesome-project",
                description="An awesome project",
                stars=50,
                forks=10,
                language="Python",
                languages={},
                url="https://github.com/user/awesome-project",
                created_at="2023-01-01T00:00:00Z",
                updated_at="2023-12-01T00:00:00Z",
                size=1000
            )
        ]

        result = await self.service._generate_project_highlights(repositories)
        
        assert len(result) == 1
        assert result[0].name == "awesome-project"
        assert result[0].impact_metric == "50 stars, 10 forks"
        assert "Python" in result[0].tech_stack

    def test_format_impact_metric(self):
        """Test impact metric formatting"""
        from app.github.schemas import Repository
        
        # Test with both stars and forks
        repo1 = Repository(
            name="test", description="", stars=10, forks=5, language="Python",
            languages={}, url="", created_at="", updated_at="", size=0
        )
        assert self.service._format_impact_metric(repo1) == "10 stars, 5 forks"
        
        # Test with only stars
        repo2 = Repository(
            name="test", description="", stars=10, forks=0, language="Python",
            languages={}, url="", created_at="", updated_at="", size=0
        )
        assert self.service._format_impact_metric(repo2) == "10 stars"
        
        # Test with no stars or forks
        repo3 = Repository(
            name="test", description="", stars=0, forks=0, language="Python",
            languages={}, url="", created_at="", updated_at="", size=0
        )
        assert self.service._format_impact_metric(repo3) == "Active development"

    @pytest.mark.asyncio
    async def test_generate_resume_bullet_points(self):
        """Test resume bullet points generation"""
        from app.github.schemas import ImpactMetrics, TechStack, ProjectHighlight
        
        username = "testuser"
        metrics = ImpactMetrics(
            total_stars=100, total_forks=50, total_repos=25, public_repos=25,
            followers=200, following=100, contributions_last_year=500
        )
        tech_stack = TechStack(
            primary_languages=["Python", "JavaScript"],
            frameworks=["Django", "React"],
            tools=["Docker", "Git"]
        )
        highlights = [
            ProjectHighlight(
                name="awesome-project", description="Great project",
                impact_metric="50 stars", tech_stack=["Python"], url=""
            )
        ]

        mock_response = json.dumps([
            "Developed 25 open source projects using Python and JavaScript",
            "Achieved 100 stars across GitHub repositories",
            "Built projects with Django and React frameworks"
        ])

        with patch('app.github.service.get_llm_response', return_value=mock_response):
            result = await self.service._generate_resume_bullet_points(
                username, metrics, tech_stack, highlights
            )
            
            assert len(result) == 3
            assert "25 open source projects" in result[0]
            assert "100 stars" in result[1]

    @pytest.mark.asyncio
    async def test_generate_resume_bullet_points_fallback(self):
        """Test resume bullet points with JSON parse error"""
        from app.github.schemas import ImpactMetrics, TechStack, ProjectHighlight
        
        username = "testuser"
        metrics = ImpactMetrics(
            total_stars=50, total_forks=25, total_repos=10, public_repos=10,
            followers=100, following=50, contributions_last_year=300
        )
        tech_stack = TechStack(
            primary_languages=["Python"], frameworks=["Django"], tools=["Git"]
        )
        highlights = []

        with patch('app.github.service.get_llm_response', return_value="Invalid JSON"):
            result = await self.service._generate_resume_bullet_points(
                username, metrics, tech_stack, highlights
            )
            
            # Should return fallback bullet points
            assert len(result) == 3
            assert "10 open source projects" in result[0]
            assert "50 stars" in result[1]

    @pytest.mark.asyncio
    async def test_analyze_github_profile_success(self):
        """Test complete GitHub profile analysis"""
        from app.github.schemas import ImpactMetrics, TechStack
        
        username = "testuser"
        
        # Create proper mock objects
        mock_metrics = ImpactMetrics(
            total_stars=100, total_forks=50, total_repos=25, public_repos=25,
            followers=200, following=100, contributions_last_year=500
        )
        mock_tech_stack = TechStack(
            primary_languages=["Python", "JavaScript"],
            frameworks=["Django", "React"],
            tools=["Docker", "Git"]
        )
        
        # Mock all the service methods
        with patch.object(self.service, '_fetch_user_data') as mock_user, \
             patch.object(self.service, '_fetch_user_repositories') as mock_repos, \
             patch.object(self.service, '_calculate_impact_metrics') as mock_calc_metrics, \
             patch.object(self.service, '_extract_tech_stack') as mock_tech, \
             patch.object(self.service, '_get_top_repositories') as mock_top_repos, \
             patch.object(self.service, '_generate_project_highlights') as mock_highlights, \
             patch.object(self.service, '_generate_resume_bullet_points') as mock_bullets:
            
            # Setup mock returns
            mock_user.return_value = {"login": username}
            mock_repos.return_value = []
            mock_calc_metrics.return_value = mock_metrics
            mock_tech.return_value = mock_tech_stack
            mock_top_repos.return_value = []
            mock_highlights.return_value = []
            mock_bullets.return_value = ["Test bullet point"]
            
            result = await self.service.analyze_github_profile(username)
            
            assert isinstance(result, GitHubAnalysisResponse)
            assert result.username == username
            assert result.profile_url == f"https://github.com/{username}"

    def test_fetch_user_repositories_api_error(self):
        """Test repository fetch with API error"""
        mock_response = Mock()
        mock_response.status_code = 403  # Rate limited or forbidden

        with patch('requests.get', return_value=mock_response):
            result = self.service._fetch_user_repositories("testuser")
            assert result == []

    def test_fetch_user_repositories_pagination_limit(self):
        """Test repository fetch respects 100 repo limit"""
        # Create 150 repos to test limit
        repos_page_1 = [{"name": f"repo-{i}"} for i in range(100)]
        repos_page_2 = [{"name": f"repo-{i}"} for i in range(100, 150)]
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [repos_page_1, repos_page_2]

        with patch('requests.get', return_value=mock_response):
            result = self.service._fetch_user_repositories("testuser")
            # Should stop at 100 repos
            assert len(result) == 100

    def test_calculate_impact_metrics_missing_data(self):
        """Test impact metrics with missing data"""
        user_data = {}  # Missing all fields
        repos_data = [
            {},  # Missing stargazers_count and forks_count
            {"stargazers_count": 5}  # Missing forks_count
        ]

        result = self.service._calculate_impact_metrics(user_data, repos_data)
        
        assert result.total_stars == 5
        assert result.total_forks == 0
        assert result.total_repos == 2
        assert result.public_repos == 0
        assert result.followers == 0

    @pytest.mark.asyncio
    async def test_extract_tech_stack_no_languages(self):
        """Test tech stack extraction with no languages"""
        repos_data = [
            {"language": None},
            {"language": None}
        ]

        mock_response = json.dumps({"frameworks": [], "tools": []})

        with patch('app.github.service.get_llm_response', return_value=mock_response):
            result = await self.service._extract_tech_stack(repos_data)
            
            assert result.primary_languages == []
            assert result.frameworks == []
            assert result.tools == []

    @pytest.mark.asyncio
    async def test_extract_tech_stack_llm_error(self):
        """Test tech stack extraction with LLM error"""
        repos_data = [{"language": "Python"}]

        with patch('app.github.service.get_llm_response', side_effect=Exception("LLM error")):
            # LLM exceptions should propagate up
            with pytest.raises(Exception, match="LLM error"):
                await self.service._extract_tech_stack(repos_data)

    def test_get_top_repositories_all_forks(self):
        """Test top repositories when all are forks"""
        repos_data = [
            {
                "name": "forked-repo-1",
                "stargazers_count": 100,
                "fork": True,
                "html_url": "https://github.com/user/forked-repo-1",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-12-01T00:00:00Z",
                "size": 1000
            },
            {
                "name": "forked-repo-2", 
                "stargazers_count": 50,
                "fork": True,
                "html_url": "https://github.com/user/forked-repo-2",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-12-01T00:00:00Z",
                "size": 500
            }
        ]

        result = self.service._get_top_repositories(repos_data)
        assert len(result) == 0  # All forks should be filtered out

    def test_get_top_repositories_recent_activity_bonus(self):
        """Test repository scoring with recent activity bonus"""
        from datetime import datetime, timezone
        recent_date = datetime.now(timezone.utc).isoformat()
        old_date = "2020-01-01T00:00:00Z"
        
        repos_data = [
            {
                "name": "recent-repo",
                "stargazers_count": 10,  # Same stars as old repo
                "forks_count": 1,
                "fork": False,
                "language": "Python",
                "html_url": "https://github.com/user/recent-repo",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": recent_date,  # Very recent
                "size": 500,
                "description": "Recently updated"
            },
            {
                "name": "old-repo",
                "stargazers_count": 10,  # Same stars as recent repo
                "forks_count": 2,
                "fork": False,
                "language": "JavaScript",
                "html_url": "https://github.com/user/old-repo",
                "created_at": "2020-01-01T00:00:00Z",
                "updated_at": old_date,  # Very old
                "size": 1000,
                "description": "Old repo"
            }
        ]

        result = self.service._get_top_repositories(repos_data)
        
        # Recent repo should rank higher due to recency bonus
        assert len(result) == 2
        assert result[0].name == "recent-repo"

    def test_format_impact_metric_only_forks(self):
        """Test impact metric formatting with only forks"""
        from app.github.schemas import Repository
        
        repo = Repository(
            name="test", description="", stars=0, forks=5, language="Python",
            languages={}, url="", created_at="", updated_at="", size=0
        )
        assert self.service._format_impact_metric(repo) == "5 forks"

    @pytest.mark.asyncio
    async def test_generate_project_highlights_no_description(self):
        """Test project highlights with missing descriptions"""
        from app.github.schemas import Repository
        
        repositories = [
            Repository(
                name="no-desc-project",
                description=None,  # No description
                stars=0,
                forks=0,
                language=None,  # No language
                languages={},
                url="https://github.com/user/no-desc-project",
                created_at="2023-01-01T00:00:00Z",
                updated_at="2023-12-01T00:00:00Z",
                size=100
            )
        ]

        result = await self.service._generate_project_highlights(repositories)
        
        assert len(result) == 1
        assert result[0].name == "no-desc-project"
        assert result[0].description == "Open source project"  # Default description
        assert result[0].impact_metric == "Active development"  # No stars/forks
        assert result[0].tech_stack == []  # No language

    @pytest.mark.asyncio
    async def test_generate_resume_bullet_points_llm_exception(self):
        """Test resume bullet points with LLM exception"""
        from app.github.schemas import ImpactMetrics, TechStack, ProjectHighlight
        
        username = "testuser"
        metrics = ImpactMetrics(
            total_stars=10, total_forks=5, total_repos=3, public_repos=3,
            followers=50, following=25, contributions_last_year=100
        )
        tech_stack = TechStack(
            primary_languages=["Python", "Go"], frameworks=["Flask"], tools=["Docker"]
        )
        highlights = []

        # LLM exceptions should propagate up
        with patch('app.github.service.get_llm_response', side_effect=Exception("API error")):
            with pytest.raises(Exception, match="API error"):
                await self.service._generate_resume_bullet_points(
                    username, metrics, tech_stack, highlights
                )

    @pytest.mark.asyncio
    async def test_analyze_github_profile_api_error_propagation(self):
        """Test that API errors in analyze_github_profile are properly propagated"""
        username = "nonexistent"
        
        with patch.object(self.service, '_fetch_user_data', side_effect=ValueError("GitHub user 'nonexistent' not found")):
            with pytest.raises(ValueError, match="GitHub user 'nonexistent' not found"):
                await self.service.analyze_github_profile(username)

    def test_fetch_user_data_network_error(self):
        """Test user data fetch with network error"""
        with patch('requests.get', side_effect=requests.RequestException("Network error")):
            with pytest.raises(requests.RequestException):
                self.service._fetch_user_data("testuser")

    def test_fetch_user_repositories_empty_response(self):
        """Test repository fetch with empty response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        with patch('requests.get', return_value=mock_response):
            result = self.service._fetch_user_repositories("testuser")
            assert result == []