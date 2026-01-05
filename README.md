# Arete - AI-Powered Resume Optimizer for Tech Professionals

Arete is an AI-powered job application optimizer specifically designed for tech professionals. It transforms generic resumes into ATS-optimized, role-specific applications by understanding technical terminology, frameworks, and GitHub profiles. Unlike generic resume tools, Arete speaks the language of software engineering and provides real-time streaming optimization with actionable, tech-specific insights.

## Prerequisites

- Python 3.12+
- Node.js 18+ (for frontend)
- Docker and Docker Compose
- Git
- Kiro CLI installed and authenticated

## Quick Start

1. **Clone and setup**
   ```bash
   git clone https://github.com/username/arete
   cd arete
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys:
   # - SUPABASE_URL and SUPABASE_KEY
   # - CLAUDE_API_KEY
   ```

3. **Run the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the interface**
   - Web UI: http://localhost:3000
   - API: http://localhost:8000/docs

## Architecture & Codebase Overview

### System Architecture
- **Backend**: FastAPI with async processing and SSE streaming
- **Frontend**: React with TypeScript and shadcn/ui components
- **AI Engine**: Claude API via LiteLLM abstraction
- **Database**: Supabase (PostgreSQL + Auth + Storage)
- **Document Processing**: pdfplumber, python-docx, WeasyPrint
- **Architecture Pattern**: Vertical Slice Architecture (VSA)

### Directory Structure
```
arete/
├── backend/
│   ├── app/
│   │   ├── core/          # Universal infrastructure
│   │   ├── resume/        # Resume parsing feature slice
│   │   ├── jobs/          # Job analysis feature slice
│   │   ├── optimization/  # AI optimization feature slice
│   │   ├── interview/     # Interview prep feature slice
│   │   └── export/        # Document export feature slice
├── frontend/
│   ├── src/components/    # React components
│   └── src/lib/          # Utilities and API client
├── .kiro/
│   ├── steering/         # Project context documents
│   ├── prompts/          # Custom Kiro commands
│   └── devlog/           # Development log
└── docker-compose.yml
```

### Key Components
- **Resume Parser** (`backend/app/resume/parser.py`): Two-stage parsing (PDF→Markdown→JSON)
- **Job Analyzer** (`backend/app/jobs/scraper.py`): URL scraping and requirement extraction
- **AI Optimizer** (`backend/app/optimization/service.py`): SSE streaming optimization
- **Document Exporter** (`backend/app/export/service.py`): ATS-compliant PDF/DOCX generation
- **Custom Kiro Prompts** (`.kiro/prompts/`): Development workflow automation

## Deep Dive

### Resume Processing Pipeline
1. **File Upload**: Accepts PDF/DOCX/TXT files up to 10MB
2. **Stage 1 Parsing**: Extracts text using pdfplumber/python-docx → Markdown
3. **Stage 2 Processing**: LLM converts Markdown → Structured JSON
4. **GitHub Integration**: Optional GitHub profile analysis for project impact
5. **Data Storage**: Supabase Storage (files) + Database (metadata, parsed data)

### AI Optimization Process
1. **Job Analysis**: Extracts requirements from job descriptions or URLs
2. **Real-Time Streaming**: SSE provides live optimization feedback
3. **Tech-Aware Processing**: Understands frameworks, technical terminology
4. **Content Generation**: Tailored resume, cover letter, interview questions
5. **ATS Compliance**: Ensures compatibility with applicant tracking systems

### Kiro CLI Integration
- **Custom Prompts**: `@prime`, `@plan-feature`, `@execute`, `@code-review`
- **Steering Documents**: Define product vision, tech stack, and structure
- **Development Workflow**: VSA pattern optimized for AI-assisted development
- **Logging Strategy**: Structured logging with hybrid dotted namespace pattern

### Performance Optimizations
- **Async Processing**: FastAPI with async/await for concurrent operations
- **Streaming Responses**: SSE for real-time user feedback
- **Efficient Parsing**: Two-stage approach balances accuracy with speed
- **Resource Limits**: File size limits, processing timeouts, memory management

## Troubleshooting

### Common Issues

**Resume parsing fails**
- Check file format (PDF, DOCX, TXT only)
- Verify file size is under 10MB
- Review logs: `docker-compose logs backend`
- Test with different file: some PDFs have complex layouts

**AI optimization is slow**
- Check Claude API key and rate limits
- Monitor token usage in logs
- Verify Supabase connection: `docker-compose ps`
- Consider using smaller model for testing

**Job URL scraping not working**
- Verify URL is accessible (not behind login)
- Check supported job sites (LinkedIn, Indeed, etc.)
- Use text paste as fallback option
- Review scraping logs for specific errors

**Export PDF/DOCX fails**
- Ensure WeasyPrint dependencies are installed
- Check template files in `backend/app/export/templates/`
- Verify font availability for PDF generation
- Test with minimal resume data first

**Frontend build fails**
- Clear node modules: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (requires 18+)
- Verify environment variables in `.env`
- Review Vite configuration in `vite.config.ts`

**Database connection errors**
- Verify Supabase credentials in `.env`
- Check network connectivity to Supabase
- Review database schema and migrations
- Test connection with Supabase client directly

### Getting Help
- Check application logs: `docker-compose logs -f`
- Review API documentation: http://localhost:8000/docs
- Consult Kiro CLI documentation: `kiro-cli --help`
- Check development log: `.kiro/devlog/devlog.md`
- Open an issue on GitHub with error details and logs

## Development with Kiro CLI

This project is optimized for AI-assisted development using Kiro CLI:

### Core Workflow
1. **`@prime`** - Load project context and understand codebase
2. **`@plan-feature`** - Create detailed implementation plans
3. **`@execute`** - Implement features systematically
4. **`@code-review`** - Review code quality and identify issues

### Hackathon-Specific Commands
- **`@code-review-hackathon`** - Evaluate against judging criteria
- **`@execution-report`** - Generate implementation reports
- **`@create-prd`** - Update product requirements

### Development Log
Track your progress in `.kiro/devlog/devlog.md` - it's a required hackathon submission component!
