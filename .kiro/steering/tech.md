# Technical Architecture

## Technology Stack
**Backend:**
- **Framework:** FastAPI 0.115+ (async web framework)
- **Runtime:** Python 3.12+ (modern features)
- **LLM Integration:** LiteLLM 1.56+ (multi-provider abstraction for Claude API)
- **Document Processing:** pdfplumber (PDF parsing), python-docx (DOCX read/write)
- **PDF Generation:** WeasyPrint 53+ (HTML→PDF conversion)
- **Web Scraping:** BeautifulSoup4 4.12+ (job posting URL scraping)
- **Database:** Supabase 2.11+ (PostgreSQL + Auth + Storage)

**Frontend:**
- **Framework:** React 18+ with Vite 6+ (fast development)
- **Language:** TypeScript 5+ (type safety)
- **UI Components:** shadcn/ui + Tailwind CSS 3+ (modern, accessible design)
- **HTTP Client:** Axios 1.7+ (API communication)
- **Forms:** React Hook Form 7+ (form validation)

**Infrastructure:**
- **Database:** Supabase PostgreSQL (managed database)
- **Storage:** Supabase Storage (file uploads)
- **Authentication:** Supabase Auth (email/password)
- **LLM Provider:** Anthropic Claude API (claude-3.5-sonnet)
- **Logging:** Structured logging with hybrid dotted namespace pattern
- **Deployment:** Docker + Docker Compose (containerized deployment)

## Architecture Overview
**Vertical Slice Architecture (VSA)** - Organized by feature rather than technical layer:

```
┌─────────────────────────────────────────┐
│   React Frontend (Vite + shadcn/ui)     │
│  - File upload, job input (text/URL)    │
│  - SSE streaming display, downloads     │
└────────────────┬────────────────────────┘
                 │ HTTP / SSE
┌────────────────▼────────────────────────┐
│         FastAPI Backend                 │
│  Feature Slices:                        │
│  ├── /resume     (upload, parse)        │
│  ├── /jobs       (analyze, scrape)      │
│  ├── /optimize   (LLM streaming)        │
│  ├── /interview  (questions)            │
│  └── /export     (PDF/DOCX)             │
│  Core: config, database, llm, logging   │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
   ┌────▼─────┐    ┌─────▼──────┐
   │ Supabase │    │   Claude   │
   └──────────┘    └────────────┘
```

**Key Components:**
- **Resume Processing:** Two-stage parsing (PDF/DOCX → Markdown → JSON via LLM)
- **Job Analysis:** Text extraction and requirement parsing
- **AI Optimization:** SSE streaming for real-time feedback
- **Document Export:** ATS-compliant PDF/DOCX generation
- **Observability:** Structured logging with correlation tracking

## Development Environment
**Required Tools:**
- Python 3.12+
- Node.js 18+ with npm/yarn
- Docker & Docker Compose
- Git

**Setup Commands:**
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install

# Full stack with Docker
docker-compose up --build
```

**Environment Variables:**
```bash
# Application
APP_NAME=Arete
DEBUG=false

# Supabase
SUPABASE_URL=https://...
SUPABASE_KEY=...
SUPABASE_SERVICE_KEY=...

# LLM
LLM_PROVIDER=claude
CLAUDE_API_KEY=sk-ant-...

# Limits
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES=pdf,docx,txt
```

## Code Standards
**Python (Backend):**
- **Style:** Black formatter, isort for imports
- **Type Hints:** Full type annotations with mypy checking
- **Naming:** snake_case for functions/variables, PascalCase for classes
- **Documentation:** Docstrings for all public functions
- **Error Handling:** Structured exceptions with proper HTTP status codes

**TypeScript (Frontend):**
- **Style:** Prettier formatter, ESLint for linting
- **Naming:** camelCase for variables/functions, PascalCase for components
- **Components:** Functional components with hooks
- **Props:** Interface definitions for all component props
- **State Management:** React hooks (useState, useEffect, useContext)

**General:**
- **Commits:** Conventional commits (feat:, fix:, docs:, etc.)
- **Branches:** feature/*, bugfix/*, hotfix/*
- **Code Review:** All changes via pull requests

## Testing Strategy
**Backend Testing:**
- **Framework:** pytest with async support
- **Coverage:** >80% code coverage target
- **Types:** Unit tests for services, integration tests for API endpoints
- **Mocking:** Mock external APIs (Claude, Supabase) for reliable tests

**Frontend Testing:**
- **Framework:** Vitest + React Testing Library
- **Types:** Component tests, integration tests for user flows
- **Coverage:** Focus on critical user paths

**End-to-End:**
- **Manual Testing:** Full workflow validation
- **Test Data:** Sample resumes and job descriptions
- **ATS Validation:** Test exported PDFs with ATS checkers

## Deployment Process
**Development:**
```bash
docker-compose up --build
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

**Production (Optional):**
- **Container Registry:** Docker Hub or AWS ECR
- **Hosting:** VPS with Docker Compose or cloud platforms
- **Environment:** Production environment variables
- **Monitoring:** Basic logging and error tracking

## Performance Requirements
**Response Times:**
- File upload: <5 seconds for 10MB files
- Resume parsing: <30 seconds
- Job analysis: <10 seconds
- AI optimization: <60 seconds with streaming
- Document export: <10 seconds

**Scalability:**
- Support 10+ concurrent users
- Handle 100+ resumes per day
- Graceful degradation under load

**Resource Limits:**
- File size: 10MB maximum
- Processing timeout: 2 minutes
- Memory usage: <512MB per request

## Security Considerations
**Authentication & Authorization:**
- Supabase JWT tokens for API access
- Token validation on all protected endpoints
- User data isolation (users only see their own data)

**Data Protection:**
- File uploads stored securely in Supabase Storage
- No sensitive data in logs
- Input sanitization for all user inputs
- HTTPS in production

**API Security:**
- Rate limiting (basic implementation)
- File type validation (PDF, DOCX, TXT only)
- File size limits (10MB maximum)
- CORS configuration for frontend domain

**Privacy:**
- Clear data retention policy
- User can delete their data
- No sharing of resume content
- Transparent AI usage disclosure
