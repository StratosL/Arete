# Project Structure

## Directory Layout
**Vertical Slice Architecture (VSA)** - Organized by feature rather than technical layer:

```
arete/
├── backend/
│   ├── app/
│   │   ├── core/                    # Universal infrastructure
│   │   │   ├── config.py           # Pydantic settings
│   │   │   ├── database.py         # Supabase client
│   │   │   ├── llm.py              # LiteLLM wrapper
│   │   │   ├── logging.py          # Structured logging
│   │   │   └── middleware.py       # Request logging
│   │   │
│   │   ├── resume/                  # Feature slice
│   │   │   ├── routes.py           # POST /resume/upload
│   │   │   ├── service.py          # Business logic
│   │   │   ├── parser.py           # PDF/DOCX → Markdown → JSON
│   │   │   └── schemas.py          # Pydantic models
│   │   │
│   │   ├── jobs/                    # Feature slice
│   │   │   ├── routes.py           # POST /jobs/analyze
│   │   │   ├── service.py          # Analysis logic
│   │   │   ├── scraper.py          # URL scraping
│   │   │   └── schemas.py
│   │   │
│   │   ├── optimization/            # Feature slice
│   │   │   ├── routes.py           # POST /optimize (SSE)
│   │   │   ├── service.py          # LLM integration
│   │   │   ├── prompts.py          # Prompt templates
│   │   │   └── schemas.py
│   │   │
│   │   ├── interview/               # Feature slice
│   │   │   ├── routes.py
│   │   │   ├── service.py
│   │   │   └── schemas.py
│   │   │
│   │   └── export/                  # Feature slice
│   │       ├── routes.py
│   │       ├── service.py
│   │       ├── templates/          # Resume templates
│   │       │   └── modern-ats.css
│   │       └── schemas.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                 # shadcn/ui components
│   │   │   ├── ResumeUpload.tsx
│   │   │   ├── JobDescriptionInput.tsx
│   │   │   ├── OptimizationDisplay.tsx
│   │   │   └── DocumentExport.tsx
│   │   ├── lib/
│   │   │   ├── utils.ts
│   │   │   └── api.ts
│   │   ├── hooks/
│   │   │   └── useSSE.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── .kiro/
│   ├── steering/
│   │   ├── product.md
│   │   ├── tech.md
│   │   └── structure.md
│   └── prompts/
│       ├── quickstart.md
│       ├── prime.md
│       ├── plan-feature.md
│       ├── execute.md
│       └── code-review.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── DEVLOG.md
└── PRD.md
```

## File Naming Conventions
**Backend (Python):**
- **Files:** snake_case.py (e.g., `resume_parser.py`)
- **Classes:** PascalCase (e.g., `ResumeParser`)
- **Functions/Variables:** snake_case (e.g., `parse_resume`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `MAX_FILE_SIZE`)

**Frontend (TypeScript/React):**
- **Components:** PascalCase.tsx (e.g., `ResumeUpload.tsx`)
- **Hooks:** camelCase starting with 'use' (e.g., `useSSE.ts`)
- **Utilities:** camelCase.ts (e.g., `apiClient.ts`)
- **Types:** PascalCase interfaces (e.g., `ResumeData`)

**General:**
- **Directories:** kebab-case or snake_case
- **Config files:** lowercase with extensions (e.g., `docker-compose.yml`)
- **Documentation:** UPPERCASE.md for important files (e.g., `README.md`)

## Module Organization
**Vertical Slice Pattern:**
- Each feature slice contains all layers (routes, service, schemas)
- Self-contained functionality with minimal cross-slice dependencies
- Core module provides shared infrastructure (database, LLM, config)
- Clear separation between business logic (service) and HTTP handling (routes)

**Frontend Component Structure:**
- **UI Components:** Reusable shadcn/ui components in `/components/ui/`
- **Feature Components:** Page-specific components in `/components/`
- **Hooks:** Custom React hooks in `/hooks/`
- **Types:** TypeScript interfaces and types in `/types/`
- **Utils:** Helper functions and API clients in `/lib/`

## Configuration Files
**Backend Configuration:**
- **`app/core/config.py`:** Pydantic settings with environment variables
- **`app/core/logging.py`:** Structured logging with hybrid dotted namespace pattern
- **`requirements.txt`:** Python dependencies
- **`Dockerfile`:** Container configuration
- **`.env`:** Environment variables (not committed)

**Frontend Configuration:**
- **`vite.config.ts`:** Vite build configuration
- **`tailwind.config.js`:** Tailwind CSS configuration
- **`package.json`:** Node.js dependencies and scripts
- **`tsconfig.json`:** TypeScript configuration

**Infrastructure:**
- **`docker-compose.yml`:** Multi-container orchestration
- **`.env.example`:** Template for environment variables

## Documentation Structure
**Project Documentation:**
- **`README.md`:** Project overview, setup instructions, usage
- **`DEVLOG.md`:** Development timeline, decisions, challenges
- **`PRD.md`:** Product Requirements Document
- **`.kiro/steering/`:** Kiro CLI project context documents

**Code Documentation:**
- **Backend:** Docstrings for all public functions and classes
- **Frontend:** JSDoc comments for complex functions
- **API:** OpenAPI/Swagger documentation via FastAPI

## Asset Organization
**Frontend Assets:**
- **`public/`:** Static assets (favicon, images, manifest)
- **`src/assets/`:** Bundled assets (if needed)
- **Styling:** Tailwind CSS classes, shadcn/ui components

**Backend Assets:**
- **`app/export/templates/`:** Resume templates (CSS, HTML)
- **Static files served via FastAPI StaticFiles (if needed)**

## Build Artifacts
**Backend:**
- **`__pycache__/`:** Python bytecode (ignored)
- **`.pytest_cache/`:** Test cache (ignored)
- **Docker images:** Built via Dockerfile

**Frontend:**
- **`dist/`:** Vite build output (ignored)
- **`node_modules/`:** Dependencies (ignored)
- **Docker images:** Built via Dockerfile

## Environment-Specific Files
**Development:**
- **`.env`:** Local environment variables
- **`docker-compose.yml`:** Local development stack

**Production (Future):**
- **`.env.production`:** Production environment variables
- **`docker-compose.prod.yml`:** Production configuration
- **CI/CD configs:** GitHub Actions, deployment scripts

**Environment Variables:**
```bash
# Application
APP_NAME=Arete
DEBUG=true  # false in production

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# LLM
LLM_PROVIDER=claude
CLAUDE_API_KEY=sk-ant-your-key

# Limits
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES=pdf,docx,txt
```
