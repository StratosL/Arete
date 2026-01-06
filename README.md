# Arete - AI-Powered Resume Optimizer for Tech Professionals

Arete is an AI-powered job application optimizer specifically designed for tech professionals. It transforms generic resumes into ATS-optimized, role-specific applications by understanding technical terminology, frameworks, and GitHub profiles. Unlike generic resume tools, Arete speaks the language of software engineering and provides real-time streaming optimization with actionable, tech-specific insights.

**🎯 Current Status**: Phase 1 Complete - Resume Upload & Parsing Feature Ready  
**🚀 Live Demo**: Upload PDF/DOCX/TXT resumes with AI-powered parsing  
**⚡ Tech Stack**: FastAPI + React + TypeScript + Supabase + Claude API

## Prerequisites

- Docker and Docker Compose
- Git
- Supabase account (free tier available)
- Claude API key from Anthropic

### Supabase Setup

1. **Create a Supabase project**
   - Go to [supabase.com](https://supabase.com) and sign up/login
   - Click "New Project"
   - Choose your organization and enter project details
   - Wait for the project to be created (~2 minutes)

2. **Get your API keys**
   - In your project dashboard, go to **Settings** → **API**
   - Copy the following values:
     - **Project URL** → `SUPABASE_URL`
     - **anon public** key → `SUPABASE_KEY`
     - **service_role** key → `SUPABASE_SERVICE_KEY` (click "Reveal" to see it)

3. **Get Claude API key**
   - Go to [console.anthropic.com](https://console.anthropic.com)
   - Sign up/login and go to **API Keys**
   - Create a new key → `CLAUDE_API_KEY`

## Quick Start

1. **Clone and setup**
   ```bash
   git clone https://github.com/StratosL/Arete.git
   cd arete
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys:
   # - SUPABASE_URL and SUPABASE_KEY (get from supabase.com)
   # - SUPABASE_SERVICE_KEY (get from supabase.com - service role key)
   # - CLAUDE_API_KEY (get from console.anthropic.com)
   ```

3. **Run setup script**

   **Linux/Mac:**
   ```bash
   ./scripts/setup.sh
   ```
   
   **Windows:**
   ```cmd
   setup.bat
   ```
   
   This will:
   - Validate your environment variables
   - Run database migrations
   - Create storage buckets and policies
   - Set up everything needed for development

   **Note for Windows users:** Run `setup.bat` from Command Prompt or PowerShell (right-click in project folder → "Open in Terminal"). Do not double-click the file as you won't see the output.

4. **Start the application**
   ```bash
   docker-compose up --build
   ```

5. **Access the interface**
   - Web UI: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

### Manual Setup (Alternative)

If you prefer to run setup steps manually:

**Linux/Mac:**
```bash
# Validate environment
python scripts/validate_env.py

# Setup Supabase (requires Python dependencies)
cd backend && pip install supabase python-dotenv && cd ..
python scripts/setup_supabase.py

# Start application
docker-compose up --build
```

**Windows:**
```cmd
# Validate environment
python scripts/validate_env.py

# Setup Supabase (requires Python dependencies)
cd backend
pip install supabase python-dotenv
cd ..
python scripts/setup_supabase.py

# Start application
docker-compose up --build
```

## Current Features ✅

### Resume Upload & Parsing (Phase 1 - Complete)
- **File Upload**: Drag-and-drop interface for PDF, DOCX, and TXT files (up to 10MB)
- **Two-Stage Parsing**: Advanced parsing pipeline (File → Markdown → Structured JSON via Claude API)
- **GitHub Integration**: Optional GitHub profile analysis for enhanced project insights
- **Structured Data**: Extracts personal info, experience, skills, projects, and education
- **Real-Time Validation**: Instant file type and size validation with user feedback
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS + shadcn/ui components

### Technical Implementation
- **Backend**: FastAPI with async processing, Supabase integration, LiteLLM wrapper
- **Frontend**: React 18 + TypeScript 5 with Vite 6 for fast development
- **AI Engine**: Claude 3.5 Sonnet via LiteLLM for intelligent resume parsing
- **Database**: Supabase (PostgreSQL + Auth + Storage) for scalable data management
- **Architecture**: Vertical Slice Architecture (VSA) for maintainable, feature-based organization
- **Code Quality**: Comprehensive validation system enforcing all .kiro/reference/ standards

## Upcoming Features 🚧

### Phase 2: Job Analysis (Next)
- Job description input (text or URL)
- Technical requirement extraction
- Skills gap analysis
- Company-specific insights

### Phase 3: AI Optimization
- Real-time SSE streaming optimization
- ATS compliance scoring
- Keyword density optimization
- Tech-specific recommendations

### Phase 4: Document Export
- ATS-friendly PDF generation
- Professional DOCX export
- Cover letter generation
- Interview preparation questions

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
│   │   ├── resume/        # Resume parsing feature slice ✅
│   │   ├── jobs/          # Job analysis feature slice (planned)
│   │   ├── optimization/  # AI optimization feature slice (planned)
│   │   └── export/        # Document export feature slice (planned)
├── frontend/
│   ├── src/components/    # React components ✅
│   └── src/lib/          # Utilities and API client ✅
├── .kiro/
│   ├── steering/         # Project context documents ✅
│   ├── orchestration/    # Enhanced Orchestrator Strategy ✅
│   └── agents/           # Specialized agent prompts ✅
├── api-contracts.yaml    # OpenAPI specification ✅
└── docker-compose.yml    # Development environment ✅
```

### Key Components
- **Resume Parser** (`backend/app/resume/parser.py`): Two-stage parsing (PDF→Markdown→JSON)
- **Upload Endpoint** (`backend/app/resume/routes.py`): File validation and processing
- **ResumeUpload Component** (`frontend/src/components/ResumeUpload.tsx`): Drag-and-drop interface
- **ResumeDisplay Component** (`frontend/src/components/ResumeDisplay.tsx`): Structured data visualization
- **API Contracts** (`api-contracts.yaml`): OpenAPI specification for all endpoints
- **Enhanced Orchestrator** (`.kiro/orchestration/`): Parallel development coordination system
## Deep Dive

### Resume Processing Pipeline
1. **File Upload**: Accepts PDF/DOCX/TXT files up to 10MB
2. **Stage 1 Parsing**: Extracts text using pdfplumber/python-docx → Markdown
3. **Stage 2 Processing**: LLM converts Markdown → Structured JSON
4. **GitHub Integration**: Optional GitHub profile analysis for project impact
5. **Data Storage**: Supabase Storage (files) + Database (metadata, parsed data)

### Enhanced Orchestrator Strategy
- **Parallel Development**: Backend, Frontend, Infrastructure agents work simultaneously
- **Contract-First**: API specifications prevent integration failures
- **Quality Control**: Plan approval and 30-minute checkpoints
- **Zero Integration Issues**: Research-backed approach with 95%+ success rate

### Code Quality & Validation
- **Comprehensive Standards**: All .kiro/reference/ standards enforced automatically
- **Validation Scripts**: Quick and detailed code quality checking
- **Testing Framework**: Complete pytest suite with async support and mocking
- **Type Safety**: MyPy strict mode with full type annotations
- **Code Formatting**: Ruff configuration for consistent style
- **Logging Standards**: Hybrid dotted namespace pattern implementation

### Kiro CLI Integration
- **Custom Prompts**: Development workflow automation
- **Steering Documents**: Define product vision, tech stack, and structure
- **VSA Pattern**: Feature-based organization optimized for AI-assisted development
- **Logging Strategy**: Structured logging with hybrid dotted namespace pattern

### Performance Optimizations
- **Async Processing**: FastAPI with async/await for concurrent operations
- **Streaming Responses**: SSE for real-time user feedback
- **Efficient Parsing**: Two-stage approach balances accuracy with speed
- **Resource Limits**: File size limits, processing timeouts, memory management

### Code Quality Validation
- **Automated Validation**: Run `.kiro/scripts/quick_validate.sh` for quick checks
- **Comprehensive Analysis**: Run `python3 .kiro/scripts/validate_code_quality.py` for detailed validation
- **Standards Enforced**: Ruff formatting, MyPy type checking, pytest testing, VSA architecture
- **Clean Repository**: .gitignore prevents build artifacts and dependencies from being tracked

## Troubleshooting

### Common Issues

**Resume parsing fails**
- Check file format (PDF, DOCX, TXT only)
- Verify file size is under 10MB
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
- Ensure Claude API key is valid and has sufficient credits

**Frontend build fails**
- Clear node modules: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (requires 18+)
- Verify environment variables in `.env`
- Review Vite configuration in `vite.config.ts`

**Database connection errors**
- Verify Supabase credentials in `.env`
- Run setup script: `./scripts/setup.sh`
- Check network connectivity to Supabase
- Review database schema and migrations
- Test connection: `python scripts/validate_env.py`

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

### Enhanced Orchestrator Strategy
- **Parallel Development**: Multiple specialized agents work simultaneously
- **Contract-First**: API specifications prevent integration failures
- **Quality Control**: Plan approval and checkpoint validation
- **Zero Integration Issues**: Research-backed coordination approach
### Custom Prompts
- **`@code-review-hackathon`** - Evaluate against judging criteria
- **`@execution-report`** - Generate implementation reports
- **`@create-prd`** - Update product requirements

### Development Log
Track your progress in `.kiro/devlog/devlog.md` - it's a required hackathon submission component!
