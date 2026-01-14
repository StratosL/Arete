# Architecture Documentation

Complete technical architecture and design documentation for Arete.

## Table of Contents

- [System Overview](#system-overview)
- [Vertical Slice Architecture](#vertical-slice-architecture)
- [Directory Structure](#directory-structure)
- [Processing Pipelines](#processing-pipelines)
- [Data Flow](#data-flow)
- [Key Components](#key-components)
- [Tech Stack Details](#tech-stack-details)
- [Code Quality & Standards](#code-quality--standards)
- [Performance Optimizations](#performance-optimizations)
- [Enhanced Orchestrator Strategy](#enhanced-orchestrator-strategy)

---

## System Overview

Arete is a full-stack AI-powered resume optimizer built using modern web technologies and AI capabilities.

### High-Level Architecture

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
│  ├── /optimization (LLM streaming)      │
│  ├── /export     (PDF/DOCX)             │
│  └── /github     (profile analysis)     │
│  Core: config, database, llm, logging   │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
   ┌────▼─────┐    ┌─────▼──────┐
   │ Supabase │    │   Claude   │
   └──────────┘    └────────────┘
```

### Key Design Principles

1. **Vertical Slice Architecture** - Features organized by capability, not technical layer
2. **Async-First** - FastAPI with async/await for concurrent operations
3. **Streaming Responses** - SSE for real-time AI feedback
4. **Provider Abstraction** - LiteLLM wraps AI providers for flexibility
5. **Type Safety** - Full type annotations with MyPy strict mode

---

## Vertical Slice Architecture

### What is VSA?

Vertical Slice Architecture organizes code by **feature** rather than technical layer (MVC). Each feature slice contains all layers: routes, services, schemas, and business logic.

### Benefits

- **Feature Independence** - Changes to one feature don't affect others
- **Easy to Understand** - All code for a feature is in one place
- **Parallel Development** - Multiple developers can work on different slices
- **AI-Friendly** - Clear context boundaries for AI-assisted development
- **Easy Testing** - Each slice can be tested independently

### Slice Structure

Each feature slice follows this pattern:

```
feature_name/
├── routes.py       # HTTP endpoints (FastAPI routers)
├── service.py      # Business logic
├── schemas.py      # Pydantic models (request/response)
└── [optional files for specific needs]
```

### Core vs. Slices

- **Core** (`backend/app/core/`) - Universal infrastructure (config, database, LLM)
- **Slices** (`backend/app/{feature}/`) - Self-contained features

---

## Directory Structure

### Complete Project Layout

```
arete/
├── backend/
│   ├── app/
│   │   ├── core/                    # Universal infrastructure
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # Pydantic settings
│   │   │   ├── database.py         # Supabase client
│   │   │   └── llm.py              # LiteLLM wrapper
│   │   │
│   │   ├── resume/                  # Feature slice: Resume processing
│   │   │   ├── __init__.py
│   │   │   ├── routes.py           # POST /resume/upload
│   │   │   ├── service.py          # Business logic
│   │   │   ├── parser.py           # PDF/DOCX → Markdown → JSON
│   │   │   └── schemas.py          # ResumeData, ParsedResume models
│   │   │
│   │   ├── jobs/                    # Feature slice: Job analysis
│   │   │   ├── __init__.py
│   │   │   ├── routes.py           # POST /jobs/analyze
│   │   │   ├── service.py          # Analysis logic
│   │   │   └── schemas.py          # JobAnalysis models
│   │   │
│   │   ├── optimization/            # Feature slice: AI optimization
│   │   │   ├── __init__.py
│   │   │   ├── routes.py           # GET /optimize (SSE), POST /optimize/save
│   │   │   ├── service.py          # LLM integration
│   │   │   └── schemas.py          # Optimization models
│   │   │
│   │   ├── export/                  # Feature slice: Document export
│   │   │   ├── __init__.py
│   │   │   ├── routes.py           # POST /export/{format}
│   │   │   ├── service.py          # PDF/DOCX generation
│   │   │   ├── schemas.py          # Export models
│   │   │   └── templates/          # CSS templates
│   │   │       ├── README.md
│   │   │       └── modern.css
│   │   │
│   │   └── github/                  # Feature slice: GitHub analysis
│   │       ├── __init__.py
│   │       ├── routes.py           # POST /github/analyze
│   │       ├── service.py          # GitHub API integration
│   │       └── schemas.py          # GitHub models
│   │
│   ├── tests/
│   │   ├── conftest.py             # Pytest fixtures
│   │   ├── unit/                   # Unit tests
│   │   └── integration/            # Integration tests
│   │
│   ├── main.py                     # FastAPI app entry point
│   ├── Dockerfile
│   ├── pyproject.toml              # Dependencies + tool config
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                 # shadcn/ui components
│   │   │   ├── ResumeUpload.tsx
│   │   │   ├── ResumeDisplay.tsx
│   │   │   ├── JobDescriptionInput.tsx
│   │   │   ├── JobAnalysisDisplay.tsx
│   │   │   ├── OptimizationDisplay.tsx
│   │   │   ├── DocumentExport.tsx
│   │   │   ├── GitHubAnalysis.tsx
│   │   │   ├── CoverLetterDisplay.tsx
│   │   │   ├── theme-provider.tsx
│   │   │   └── mode-toggle.tsx
│   │   ├── lib/
│   │   │   ├── api.ts              # API client
│   │   │   ├── logger.ts           # Frontend logging
│   │   │   └── utils.ts            # Utilities
│   │   ├── hooks/
│   │   │   └── useSSE.ts           # SSE streaming hook
│   │   ├── types/
│   │   │   └── index.ts            # TypeScript interfaces
│   │   ├── App.tsx                 # Main app component
│   │   └── main.tsx                # Entry point
│   │
│   ├── tests/                      # Vitest tests
│   ├── package.json
│   ├── vite.config.ts
│   ├── vitest.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── .kiro/
│   ├── steering/                   # Project context documents
│   │   ├── product.md
│   │   ├── tech.md
│   │   └── structure.md
│   ├── orchestration/              # Enhanced Orchestrator Strategy
│   ├── prompts/                    # Kiro CLI prompts
│   ├── agents/                     # Specialized agent prompts
│   └── decisions/                  # Architecture Decision Records
│
├── supabase/
│   └── migrations/                 # Database schema migrations
│       ├── 001_initial_schema.sql
│       ├── 002_disable_rls_for_mvp.sql
│       └── 003_add_optimized_data_column.sql
│
├── scripts/
│   ├── setup/                      # Setup scripts
│   ├── validation/                 # Validation scripts
│   └── testing/                    # Test utilities
│
├── docs/                           # Documentation
│   ├── INSTALLATION.md
│   ├── API_KEYS.md
│   ├── ARCHITECTURE.md (this file)
│   └── TROUBLESHOOTING.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── PRD.md
└── LICENSE
```

---

## Processing Pipelines

### Resume Processing Pipeline

Complete flow from file upload to structured data:

```
┌──────────────┐
│ File Upload  │  User uploads PDF/DOCX/TXT (max 10MB)
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Stage 1: Extraction  │  pdfplumber / python-docx
│ File → Markdown      │  Extract raw text, preserve structure
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Stage 2: Parsing     │  Claude API via LiteLLM
│ Markdown → JSON      │  Extract: personal_info, experience,
│                      │  skills, education, projects
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Storage              │  Supabase Storage (original file)
│                      │  Supabase DB (metadata + parsed JSON)
└──────────────────────┘
```

**Key Files:**
- `backend/app/resume/routes.py:712` - Upload endpoint
- `backend/app/resume/parser.py` - Two-stage parsing logic
- `backend/app/resume/schemas.py` - Data models

### Job Analysis Pipeline

Extract structured requirements from job descriptions:

```
┌────────────────┐
│ Input (Text)   │  User pastes job description
│ or URL         │  or provides job posting URL
└────┬───────────┘
     │
     ▼
┌────────────────┐
│ Web Scraping   │  If URL: BeautifulSoup4 extracts content
│ (Optional)     │  Cleans HTML, extracts text
└────┬───────────┘
     │
     ▼
┌────────────────┐
│ Text Cleaning  │  Normalize whitespace, remove artifacts
└────┬───────────┘
     │
     ▼
┌────────────────┐
│ AI Analysis    │  Claude API extracts:
│                │  - Required/preferred skills
│                │  - Experience level
│                │  - Key responsibilities
│                │  - Keywords for ATS
└────┬───────────┘
     │
     ▼
┌────────────────┐
│ Structured     │  Return JobAnalysis JSON
│ Output         │
└────────────────┘
```

**Key Files:**
- `backend/app/jobs/routes.py` - Analysis endpoint
- `backend/app/jobs/service.py` - Scraping + analysis logic
- `backend/app/jobs/schemas.py` - JobAnalysis models

### AI Optimization Pipeline

Real-time resume optimization with SSE streaming:

```
┌──────────────────┐
│ Resume + Job     │  User provides resume_id + job_id
│ Analysis         │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Resume-Job       │  Analyze alignment:
│ Matching         │  - Missing keywords
│                  │  - Experience gaps
│                  │  - Skill matches
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ AI Optimization  │  Claude API generates:
│ (SSE Streaming)  │  - Keyword suggestions
│                  │  - Experience improvements
│                  │  - Impact metrics
│                  │  - ATS optimization tips
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ User Review      │  User accepts/rejects suggestions
│ & Application    │  Apply selected optimizations
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Persistence      │  Save optimized data to database
│                  │  for export
└──────────────────┘
```

**Key Files:**
- `backend/app/optimization/routes.py` - SSE streaming endpoint
- `backend/app/optimization/service.py` - Optimization logic
- `frontend/src/components/OptimizationDisplay.tsx` - Real-time UI

### Document Export Pipeline

Generate professional PDF/DOCX documents:

```
┌──────────────────┐
│ Template         │  User selects template:
│ Selection        │  - ATS Classic (max compatibility)
│                  │  - Modern Professional (clean design)
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Data Retrieval   │  Fetch optimized resume data
│                  │  (fallback to original if not optimized)
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Smart Ordering   │  Projects: Resume-sourced first,
│                  │  GitHub projects grouped at end
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Skills           │  Categorize 300+ skills:
│ Processing       │  - Languages, Frontend, Backend
│                  │  - Database, DevOps, Cloud, Tools
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ PDF Generation   │  ReportLab (Classic) or
│ or DOCX          │  HTML/CSS → PDF (Modern)
│                  │  python-docx for DOCX
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ File Delivery    │  Browser download with proper
│                  │  MIME types and filenames
└──────────────────┘
```

**Key Files:**
- `backend/app/export/routes.py` - Export endpoints
- `backend/app/export/service.py` - PDF/DOCX generation
- `backend/app/export/templates/modern.css` - Modern template styles
- `frontend/src/components/DocumentExport.tsx` - Export UI

---

## Data Flow

### Complete User Workflow

```
1. Upload Resume (with optional GitHub URL)
   │
   ├──> Resume Parsing (Stage 1: Text Extraction)
   │
   ├──> Resume Parsing (Stage 2: Structured Data via AI)
   │
   └──> Optional: GitHub Analysis (profile + impact metrics)
        │
        ▼
2. Input Job Description (text or URL)
   │
   └──> Job Analysis (AI extracts requirements)
        │
        ▼
3. AI Optimization (Real-time SSE streaming)
   │
   ├──> Generate optimization suggestions
   │
   └──> User reviews and applies suggestions
        │
        ▼
4. Cover Letter Generation (optional)
   │
   └──> AI creates personalized cover letter
        │
        ▼
5. Template Selection
   │
   ├──> ATS Classic (maximum compatibility)
   │
   └──> Modern Professional (clean design)
        │
        ▼
6. Document Export
   │
   ├──> PDF (ReportLab or HTML→PDF)
   │
   └──> DOCX (python-docx)
```

---

## Key Components

### Backend: FastAPI Application

**Entry Point**: `backend/main.py`

```python
app = FastAPI(
    title="Arete API",
    description="AI-powered resume optimizer",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(CORSMiddleware, ...)

# Include feature routers
app.include_router(resume_router)
app.include_router(jobs_router)
app.include_router(optimization_router)
app.include_router(export_router)
app.include_router(github_router)
```

### Core Infrastructure

**Config**: `backend/app/core/config.py`
- Pydantic settings with environment variables
- Type-safe configuration

**Database**: `backend/app/core/database.py`
- Supabase client initialization
- Connection pooling

**LLM Wrapper**: `backend/app/core/llm.py`
- LiteLLM abstraction for Claude API
- Easy to add other providers (OpenAI, Gemini)

### Frontend: React Application

**Entry Point**: `frontend/src/main.tsx`

```typescript
import { App } from './App'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>
)
```

**API Client**: `frontend/src/lib/api.ts`
- Axios-based HTTP client
- Centralized error handling
- Type-safe requests/responses

**SSE Hook**: `frontend/src/hooks/useSSE.ts`
- Custom React hook for Server-Sent Events
- Used for real-time optimization streaming

---

## Tech Stack Details

### Backend Technologies

| Technology | Version | Purpose | Documentation |
|------------|---------|---------|---------------|
| FastAPI | 0.115+ | Async web framework | [docs](https://fastapi.tiangolo.com/) |
| Python | 3.12+ | Runtime | [docs](https://docs.python.org/3/) |
| LiteLLM | 1.56+ | Multi-provider LLM abstraction | [docs](https://docs.litellm.ai/) |
| pdfplumber | 0.11+ | PDF text extraction | [docs](https://github.com/jsvine/pdfplumber) |
| python-docx | 1.1+ | DOCX read/write | [docs](https://python-docx.readthedocs.io/) |
| ReportLab | Latest | PDF generation | [docs](https://www.reportlab.com/docs/) |
| BeautifulSoup4 | 4.12+ | HTML parsing/scraping | [docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) |
| Supabase | 2.11+ | Database + Auth + Storage | [docs](https://supabase.com/docs) |

### Frontend Technologies

| Technology | Version | Purpose | Documentation |
|------------|---------|---------|---------------|
| React | 18+ | UI framework | [docs](https://react.dev/) |
| TypeScript | 5+ | Type safety | [docs](https://www.typescriptlang.org/docs/) |
| Vite | 5+ | Build tool | [docs](https://vitejs.dev/) |
| shadcn/ui | Latest | UI components | [docs](https://ui.shadcn.com/) |
| Tailwind CSS | 3+ | Styling | [docs](https://tailwindcss.com/docs) |
| Axios | 1.7+ | HTTP client | [docs](https://axios-http.com/docs/intro) |
| React Hook Form | 7+ | Form validation | [docs](https://react-hook-form.com/) |
| Zod | 3+ | Schema validation | [docs](https://zod.dev/) |

### Testing Technologies

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| pytest | Backend unit/integration tests | [docs](https://docs.pytest.org/) |
| pytest-asyncio | Async test support | [docs](https://pytest-asyncio.readthedocs.io/) |
| Vitest | Frontend unit tests | [docs](https://vitest.dev/) |
| React Testing Library | Component tests | [docs](https://testing-library.com/react) |
| Playwright | E2E tests | [docs](https://playwright.dev/) |

---

## Code Quality & Standards

### Python Standards

**Linting & Formatting**: Ruff

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM", "TCH", "PTH", "ERA", "PL", "RUF"]
```

**Type Checking**: MyPy (strict mode)

```toml
[tool.mypy]
python_version = "3.12"
strict = true
```

**Testing**: pytest with 80%+ coverage target

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
addopts = ["--cov=app", "--cov-fail-under=80"]
```

### TypeScript Standards

**Linting**: ESLint with TypeScript plugin

**Formatting**: Prettier (via Vite)

**Type Checking**: TypeScript strict mode

### Code Organization

**Naming Conventions**:
- **Python**: `snake_case` for functions/variables, `PascalCase` for classes
- **TypeScript**: `camelCase` for variables/functions, `PascalCase` for components
- **Files**: Match content (e.g., `ResumeUpload.tsx`, `resume_parser.py`)

**Documentation**:
- Python: Docstrings for all public functions
- TypeScript: JSDoc for complex functions
- README files in key directories

---

## Performance Optimizations

### Async Operations

- FastAPI with `async/await` for concurrent requests
- Async file I/O with `aiofiles`
- Concurrent LLM calls where possible

### Streaming Responses

- SSE (Server-Sent Events) for real-time AI feedback
- Reduces perceived latency vs. waiting for complete response
- Better user experience with progress indicators

### Resource Management

**File Size Limits**:
- Resume uploads: 10MB maximum
- Prevents memory exhaustion

**Processing Timeouts**:
- Resume parsing: 2 minutes max
- AI optimization: 2 minutes max
- Prevents hung requests

**Caching**:
- Parsed resume data stored in database
- Avoid re-parsing on subsequent requests

### Production Validated Performance

All operations meet target timeframes:
- Resume parsing: <30 seconds
- Job analysis: <30 seconds
- AI optimization: <60 seconds (with streaming)
- Document export: <10 seconds

---

## Enhanced Orchestrator Strategy

### Overview

Arete uses an Enhanced Orchestrator Strategy for AI-assisted development, enabling efficient parallel development and zero integration issues.

### Key Principles

1. **Parallel Development**
   - Backend, Frontend, Infrastructure agents work simultaneously
   - Independent feature slices enable parallel workflows

2. **Contract-First Development**
   - API specifications defined upfront (`api-contracts.yaml`)
   - Prevents integration failures
   - Clear interfaces between components

3. **Quality Control**
   - Plan approval before implementation
   - 30-minute checkpoints during development
   - Code review before merging

4. **Research-Backed Approach**
   - Mandatory research protocol
   - Architecture decision records (.kiro/decisions/)
   - 95%+ success rate

### Agent Types

Located in `.kiro/agents/`:
- **backend-agent**: Python/FastAPI development
- **frontend-agent**: React/TypeScript development
- **infrastructure-agent**: Docker/deployment
- **testing-agent**: Test suite development
- **docs-commit-agent**: Documentation updates

### Workflow Integration

The Kiro CLI provides custom prompts for development:

```bash
kiro @prime          # Load project context
kiro @plan-feature   # Plan implementation
kiro @execute        # Systematic execution
kiro @code-review    # Quality checks
```

See `.kiro/prompts/` for complete workflow automation.

---

## Database Schema

### Supabase Tables

**resumes** - Stores resume metadata and parsed data
```sql
CREATE TABLE resumes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id),
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    parsed_data JSONB,
    optimized_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**jobs** - Stores job analysis data
```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id),
    job_description TEXT NOT NULL,
    job_url TEXT,
    analysis_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Storage Buckets

- **resumes** - Original resume files (PDF/DOCX/TXT)
- **exports** - Generated PDF/DOCX documents

---

## API Reference

For interactive API documentation, run the application and visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Further Reading

- **Product Requirements**: See [PRD.md](../PRD.md)
- **Installation Guide**: See [INSTALLATION.md](INSTALLATION.md)
- **API Keys Setup**: See [API_KEYS.md](API_KEYS.md)
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Kiro CLI Guide**: See [kiro-guide.md](kiro-guide.md)
