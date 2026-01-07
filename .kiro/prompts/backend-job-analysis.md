Using FastAPI 2024-2025 best practices and web scraping research as context, implement job description analysis endpoint for Arete.

Documentation to read: 
- READ: api-contracts.yaml (JobAnalysis schema)
- READ: .kiro/steering/tech.md (FastAPI + LiteLLM patterns)
- READ: backend/app/resume/routes.py (existing patterns)

Focus on: async/await patterns, Pydantic v2 validation, web scraping with BeautifulSoup4, LLM integration via Claude API

First, install dependencies:
```bash
cd backend && pip install beautifulsoup4 requests tenacity
```

Then create/modify these files:

1. backend/app/jobs/schemas.py with:
   - JobAnalysisRequest (job_text: str, job_url: Optional[str])
   - JobAnalysis response model matching api-contracts.yaml
   - Pydantic v2 field validators for URL validation

2. backend/app/jobs/service.py with:
   - async scrape_job_url() function with BeautifulSoup4
   - async analyze_job_description() using Claude API
   - Rate limiting and error handling with tenacity retry
   - Text cleaning and normalization

3. backend/app/jobs/routes.py with:
   - POST /jobs/analyze endpoint
   - Async request handling with proper error responses
   - Integration with LLM service from core.llm
   
   Example pattern:
   ```python
   @router.post("/analyze", response_model=JobAnalysis)
   async def analyze_job(request: JobAnalysisRequest):
       # URL scraping if provided, then LLM analysis
   ```

4. UPDATE backend/main.py:
   - Include jobs router: app.include_router(jobs.routes.router, prefix="/jobs")

Test requirements:

Unit tests (no external dependencies):
- Test job text parsing and validation
- Test URL validation and cleaning
- Expected: 5 tests passing

Integration tests (with Claude API):
- Test full job analysis workflow
- Mark with @pytest.mark.integration  
- Expected: 3 tests passing

E2E/Manual testing:
- POST /jobs/analyze with job_text: should return structured analysis
- POST /jobs/analyze with job_url: should scrape and analyze
- Invalid inputs: should return proper 422 validation errors

All linting (ruff check ., mypy app/) must pass

When everything is green, let the user know we are ready to commit

Output format:
Summary: [what was accomplished]
Files created/modified: [list]
API endpoints: [list with descriptions]
