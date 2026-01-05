# Product Requirements Document: Arete

## Executive Summary

Arete is an AI-powered job application optimizer for tech professionals. Users upload resumes, input job descriptions (text or URL), and receive optimized ATS-friendly resumes with real-time streaming, cover letters, and interview prep questions.

**Target:** Tech-savvy professionals (new grads to senior engineers) applying to software engineering roles.

**MVP Timeline:** 3-week hackathon delivering resume parsing, job analysis, AI optimization with SSE streaming, and document export (PDF/DOCX).

**Differentiator:** Tech-specific understanding (frameworks, GitHub profiles, technical terminology) vs. generic resume tools.

---

## Mission & Principles

**Mission:** Build an intelligent job application assistant that helps tech professionals present their best selves through ATS-optimized, tailored materials powered by AI.

**Core Principles:**
1. **Tech-First Focus** - Understand technical terminology, frameworks, career patterns
2. **Privacy-Conscious** - Transparent AI usage, simple data retention
3. **Actionable Insights** - Specific suggestions, not vague feedback
4. **ATS Compatibility** - Follow 2025 ATS best practices
5. **Real-Time Feedback** - Stream AI responses for transparency

---

## Target Users

**Primary Persona:** Tech Job Seekers
- **Who:** Software engineers, developers, data scientists, DevOps engineers
- **Levels:** New graduates to senior (5-15 years experience)
- **Tech Profile:** High comfort with web apps, expect polished UIs, understand AI capabilities

**Key Needs:**
- Quickly tailor resumes for multiple applications
- Understand ATS optimization and keyword matching
- Generate professional, non-generic cover letters
- Prepare for role-specific technical interviews
- Identify skill gaps for target roles

**Pain Points:**
- Generic advice doesn't address tech-specific needs (tech stacks, GitHub, projects)
- Manual tailoring is time-consuming (10+ applications)
- Uncertainty about ATS compatibility
- Cover letters feel templated
- Unknown interview question expectations

---

## MVP Scope

### ✅ In Scope

**Resume Management:**
- ✅ Upload PDF/DOCX/TXT files (10MB limit)
- ✅ Parse to structured data (skills, experience, education, projects)
- ✅ Store in Supabase (original files + metadata + parsed JSON)

**Job Analysis:**
- ✅ Accept text paste (primary) or URL scraping (secondary)
- ✅ Extract required/preferred skills, keywords, experience, responsibilities, seniority

**AI Optimization:**
- ✅ Generate tailored resume via SSE streaming
- ✅ Actionable suggestions (keyword density, quantifiable metrics, impact language)
- ✅ Generate cover letter and interview questions

**Export:**
- ✅ PDF (WeasyPrint) and DOCX (python-docx)
- ✅ ATS-friendly templates (single column, standard fonts)

**Tech Stack:**
- ✅ FastAPI backend, Vite + React + shadcn/ui frontend
- ✅ Supabase (database, auth, storage)
- ✅ Claude API via LiteLLM abstraction
- ✅ Docker + Docker Compose deployment

### ❌ Out of Scope (Future)

- ❌ Multiple resume versions, version control, history
- ❌ LinkedIn optimization, skill gap analyzer with learning paths
- ❌ Application tracking, job board integrations
- ❌ Team accounts, analytics dashboards, admin panels
- ❌ Payment processing, CI/CD, production cloud deployment

---

## User Stories

**1. Resume Upload & Parsing**
> As a **job seeker**, I want to **upload my resume and have it automatically parsed**, so that **I can quickly start optimization without re-entering data**.

**2. Job-Specific Optimization**
> As a **applicant**, I want to **paste a job description and receive a tailored resume**, so that **my application passes ATS screening for each role**.

**3. Real-Time Streaming**
> As a **user**, I want to **see suggestions appear in real-time**, so that **I trust the AI's process and recommendations**.

**4. Cover Letter Generation**
> As a **tech professional**, I want to **auto-generate tailored cover letters**, so that **I save time while submitting personalized materials**.

**5. Interview Prep**
> As a **candidate**, I want to **receive role-specific mock questions**, so that **I can prepare for technical and behavioral interviews**.

**6. Document Export**
> As a **applicant**, I want to **download ATS-friendly PDF/DOCX**, so that **I can immediately submit applications with confidence**.

---

## Architecture

### Vertical Slice Architecture (VSA)

Organizing by feature (not technical layer) for:
- Feature independence and isolation
- AI-assisted development (clear context boundaries)
- Parallel development capability
- Easy feature addition without touching existing code

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

### Directory Structure

```
techresumeai/
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
│   │   │   ├── ResumeUpload.tsx
│   │   │   ├── JobDescriptionInput.tsx
│   │   │   ├── OptimizationDisplay.tsx
│   │   │   └── DocumentExport.tsx
│   │   ├── lib/
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
└── README.md
```

### Key Design Patterns

1. **Vertical Slice** - Self-contained features with routes, services, schemas
2. **Service Layer** - Business logic isolated from HTTP handling
3. **Provider Abstraction** - LiteLLM wraps Claude, easy to add OpenAI/Gemini
4. **Two-Stage Parsing** - PDF/DOCX → Markdown → JSON (via LLM)
5. **SSE Streaming** - Real-time AI responses without WebSocket complexity

---

## Feature Specifications

### 1. Resume Upload & Parsing

**Pipeline:**
```python
# Step 1: File → Markdown
pdfplumber (PDF) / python-docx (DOCX) → markdown text

# Step 2: Markdown → Structured JSON (via Claude)
LLM extracts: personal_info, summary, work_experience, education, skills, projects
```

**Storage:** Supabase Storage (original files) + Supabase DB (metadata, markdown, JSON)

---

### 2. Job Description Analysis

**Input:** Text paste (primary) or URL scraping (BeautifulSoup - best effort)

**Output:**
```json
{
  "required_skills": ["Python", "Django", ...],
  "preferred_skills": [...],
  "experience_requirements": ["5+ years"],
  "key_responsibilities": [...],
  "keywords": [...],
  "seniority_level": "senior"
}
```

---

### 3. AI Optimization (SSE Streaming)

**Endpoint:**
```python
@router.post("/optimize/stream")
async def optimize_resume_stream(...):
    async def generate():
        async for chunk in service.optimize_streaming(...):
            yield f"data: {json.dumps(chunk)}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

**Frontend:**
```typescript
const eventSource = new EventSource('/api/optimize/stream');
eventSource.onmessage = (event) => {
  const chunk = JSON.parse(event.data);
  updateOptimizedContent(chunk);
};
```

**Prompt:** Optimize resume for job requirements, use action verbs, add metrics, incorporate keywords naturally, maintain ATS formatting, preserve factual accuracy.

---

### 4. Interview Prep Generator

**Output:** 10 questions (5 technical, 3 behavioral, 2 system design for senior roles)
```json
{
  "type": "technical",
  "question": "...",
  "why_asked": "...",
  "tips": "..."
}
```

---

### 5. Document Export

**PDF:** WeasyPrint (Markdown → HTML → PDF with ATS CSS)
**DOCX:** python-docx (structured data → formatted DOCX)

**ATS Template:**
- A4/Letter, 1.5cm margins
- Helvetica/Arial, 11pt
- Single column, no tables
- Standard headings (bold, 13pt)

---

## Technology Stack

### Backend
| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | FastAPI 0.115+ | Async web framework |
| Runtime | Python 3.12+ | Modern features |
| LLM | LiteLLM 1.56+ | Multi-provider abstraction |
| PDF Parse | pdfplumber | Text extraction |
| PDF Gen | WeasyPrint 53+ | HTML→PDF |
| DOCX | python-docx 1.1+ | Read/write DOCX |
| Scraping | BeautifulSoup4 4.12+ | HTML parsing |
| Database | Supabase 2.11+ | PostgreSQL + Auth + Storage |

**Key Dependencies:**
```
fastapi, uvicorn, pydantic, pydantic-settings
litellm, pdfplumber, python-docx, markdown, weasyprint
beautifulsoup4, httpx, markdownify, supabase
python-multipart, python-dotenv
```

### Frontend
| Component | Technology |
|-----------|------------|
| Framework | React 18+, Vite 6+ |
| Language | TypeScript 5+ |
| UI | shadcn/ui, Tailwind CSS 3+ |
| HTTP | Axios 1.7+ |
| Forms | React Hook Form 7+ |

### Infrastructure
- **Database:** Supabase PostgreSQL
- **Storage:** Supabase Storage
- **Auth:** Supabase Auth (email/password)
- **LLM:** Anthropic Claude API (claude-3.5-sonnet)
- **Deploy:** Docker + Docker Compose

---

## Security & Configuration

### Authentication
- Supabase Auth with email/password
- JWT tokens for API authentication
- Backend validates tokens via Supabase client

### Environment Variables
```bash
# Application
APP_NAME=TechResumeAI
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

### Pydantic Settings
```python
class Settings(BaseSettings):
    supabase_url: str
    claude_api_key: str
    max_file_size_mb: int = 10
    # ...
    class Config:
        env_file = ".env"
```

### Security Scope
**✅ In:** Basic auth, JWT validation, file type/size limits, HTTPS, input sanitization
**❌ Out:** OAuth, MFA, rate limiting, advanced CORS, password requirements, email verification

---

## API Specification

**Authentication:** `Authorization: Bearer <supabase_jwt_token>`

### Endpoints

**1. Resume Upload**
```http
POST /api/resume/upload (multipart/form-data)
→ {resume_id, filename, status, created_at}
```

**2. Get Resume**
```http
GET /api/resume/{resume_id}
→ {resume_id, status, parsed_data: {personal_info, summary, work_experience, education, skills, projects}}
```

**3. Analyze Job**
```http
POST /api/jobs/analyze {text, url?}
→ {job_id, analysis: {required_skills, preferred_skills, keywords, seniority_level, ...}}
```

**4. Optimize (SSE)**
```http
POST /api/optimize/stream {resume_id, job_id}
→ SSE stream: data: {type, section, content, improvements}
```

**5. Cover Letter**
```http
POST /api/optimize/cover-letter {resume_id, job_id}
→ {cover_letter, generated_at}
```

**6. Interview Questions**
```http
POST /api/interview/generate {resume_id, job_id}
→ {questions: [{type, question, why_asked, tips}, ...]}
```

**7. Export PDF**
```http
POST /api/export/pdf {resume_id}
→ application/pdf (file download)
```

**8. Export DOCX**
```http
POST /api/export/docx {resume_id}
→ application/vnd.openxmlformats... (file download)
```

---

## Success Criteria

### MVP Success
**User can:**
1. Upload resume, see parsed data in <30 seconds
2. Input job description, receive tailored resume + cover letter + questions
3. See real-time streaming optimization
4. Download ATS-compliant PDF/DOCX
5. Complete workflow in <5 minutes

### Functional Requirements
- ✅ Upload PDF/DOCX/TXT, parse with >85% accuracy
- ✅ Job analysis (text/URL) with >80% accuracy
- ✅ Optimization completes in <60s with streaming updates
- ✅ No hallucinations (factual accuracy maintained)
- ✅ Exported PDFs pass ATS checkers
- ✅ All features work in Docker

### Quality Indicators
- ✅ Parsing captures all major sections
- ✅ Suggestions are specific and actionable
- ✅ Cover letters mention company/role/requirements
- ✅ Interview questions are role-appropriate
- ✅ Professional document formatting
- ✅ No data loss

### UX Requirements
- ✅ Intuitive UI, no tutorial needed
- ✅ Clear error messages
- ✅ Progress indicators
- ✅ Responsive design (desktop/tablet)
- ✅ Fast loads (<2s)

---

## Implementation Phases

### Phase 1: Foundation & Parsing (Week 1, 5-6 days)
**Deliverables:**
- ✅ VSA project structure (core/, resume/, jobs/)
- ✅ Docker Compose setup
- ✅ Supabase auth (register, login, logout)
- ✅ LiteLLM wrapper with Claude
- ✅ Resume upload, PDF/DOCX parsing → markdown → JSON
- ✅ Frontend: file upload + resume display

**Validation:** Upload test resume, verify parsed sections

---

### Phase 2: Job Analysis & Optimization (Week 2, 6-7 days)
**Deliverables:**
- ✅ Job input component (text + URL)
- ✅ Web scraping with BeautifulSoup
- ✅ Job analysis endpoint
- ✅ SSE streaming optimization
- ✅ Frontend SSE consumer with real-time display
- ✅ Cover letter + interview question generation

**Validation:** Scrape 3 job sites, verify streaming quality

---

### Phase 3: Export & Polish (Week 3, 5-6 days)
**Deliverables:**
- ✅ PDF export (WeasyPrint + ATS template)
- ✅ DOCX export (python-docx)
- ✅ UI polish (shadcn/ui components)
- ✅ Error handling, loading states
- ✅ Responsive design
- ✅ README, basic testing
- ✅ Demo preparation

**Validation:** End-to-end workflow 5x, test PDFs with ATS checkers

---

### Phase 4: Buffer & Presentation (Final 2-3 days)
**Deliverables:**
- ✅ Bug fixes
- ✅ Performance optimization
- ✅ Demo script, screenshots/video
- ✅ Deploy to VPS (optional)

**Validation:** Demo runs 3x successfully

---

## Future Enhancements

**Features:**
- Skill gap analyzer with learning paths (freeCodeCamp, LeetCode)
- LinkedIn profile optimization
- Application tracking (jobs applied, status, follow-ups)
- Resume version management (save/compare versions)
- Salary negotiation suggestions, company research

**Technical:**
- Multi-provider LLM (OpenAI, Gemini) with A/B testing
- Caching, background jobs (Celery), CDN
- Structured logging with correlation IDs, Sentry error tracking
- CI/CD pipeline, AWS/GCP deployment, auto-scaling

---

## Risks & Mitigations

### 1. LLM API Rate Limits/Costs
**Mitigation:** Request queuing, usage limits, caching, use smaller models (haiku) where appropriate

### 2. Resume Parsing Accuracy
**Mitigation:** Manual editing of parsed data, allow markdown upload (bypass parsing), show confidence scores, collect failure feedback

### 3. Job URL Scraping Reliability
**Mitigation:** Text paste is primary (URL is optional), clear error messages → fallback to paste, support common job boards first

### 4. Hackathon Time Constraints
**Mitigation:** Ruthless prioritization (parsing, optimization, export are must-haves; interview questions are nice-to-have), use pre-built components (shadcn/ui), daily progress checks, cut features early if behind

### 5. ATS Compatibility
**Mitigation:** Use proven templates (single column, standard fonts), test with ATS checkers (Jobscan, Resume Worded), follow 2025 best practices, provide PDF + DOCX

---

## Appendix

### References
- **VSA Guide:** `.agents/reference/vsa-patterns.md`
- **Inspiration:** [Resume Matcher](https://github.com/srbhr/Resume-Matcher), [OpenResume](https://github.com/xitanggg/open-resume), [Resume Optimizer AI](https://github.com/naveennk045/Resume-Optimizer)

### Documentation
- [FastAPI](https://fastapi.tiangolo.com/)
- [Supabase Python](https://supabase.com/docs/reference/python/introduction)
- [LiteLLM](https://docs.litellm.ai/docs/)
- [Claude API](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/)
- [shadcn/ui](https://ui.shadcn.com/)

---

**Version:** 1.0
**Last Updated:** 2025-01-05