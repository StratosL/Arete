# Arete - AI-Powered Resume Optimizer for Tech Professionals

<div align="center">
  <img src="assets/arete-logo.jpg" alt="Arete Logo" width="400">
</div>

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/StratosL/Arete?style=social)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![Test Coverage](https://img.shields.io/badge/coverage-94.4%25-brightgreen.svg)
![Build Status](https://img.shields.io/badge/build-passing-success.svg)

**Transform generic Tech resumes into ATS-optimized, role-specific applications**

![Arete Resume Demo](assets/arete_30sec.gif)

[🚀 Quick Start](#-quick-start) • [📚 Documentation](#-documentation) • [🎯 Features](#-key-features) • [🗺️ Roadmap](#️-roadmap)

</div>

---

## 🎯 Overview

Arete is an AI-powered job application optimizer specifically designed for tech professionals. Unlike generic resume tools, Arete understands technical terminology, frameworks, and GitHub profiles, transforming resumes into ATS-optimized applications with real-time streaming optimization and actionable insights.

**What makes Arete different:**
- **Tech-Specific Intelligence**: Understands React vs Angular, AWS vs GCP, and technical project impact
- **GitHub Integration**: Quantifies open-source contributions and project metrics
- **Real-Time Streaming**: Watch AI optimization happen live via SSE
- **Kiro CLI Integration**: AI-assisted development with Vertical Slice Architecture
- **Production Ready**: 100% system validation, 94.4% test coverage, 144 tests passing

---

## ⚡ Key Features

- **Smart Resume Parsing** - Two-stage AI parsing (PDF/DOCX/TXT → Markdown → JSON) with GitHub profile integration
- **Job Description Analysis** - Text input or URL scraping to extract technical requirements and keywords
- **Real-Time AI Optimization** - SSE streaming shows live optimization with actionable, tech-specific suggestions
- **GitHub Contribution Analysis** - Quantify impact with stars, forks, repositories, and generate resume bullet points
- **Cover Letter Generation** - Personalized cover letters mentioning specific company, role, and technologies
- **Interview Prep** - AI-generated technical, behavioral, and system design questions based on role
- **ATS-Compatible Export** - Professional PDF (ReportLab) and DOCX with template selection and smart skills categorization
- **Comprehensive Skill Deduplication** - 300+ skills auto-categorized (Languages, Frontend, Backend, DevOps, Cloud, Tools)

---

## 📊 Status & Metrics

- **Production Ready** - 100% system validation success rate (14/14 backend endpoints, all frontend components)
- **High Test Coverage** - 94.4% coverage with 144 tests (100% pass rate)
- **Complete Workflow** - Upload → Parse → Analyze → Optimize → Generate Cover Letter → Export
- **Performance Validated** - All operations complete within target timeframes
- **Tech Stack** - FastAPI + React + TypeScript + Supabase + Claude API + ReportLab

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Installation Guide |
|-------------|---------|-------------------|
| Python | 3.12+ | [python.org](https://www.python.org/downloads/) |
| Docker | 20.10+ | [Install Docker](docs/INSTALLATION.md#docker-installation) |
| Docker Compose | 2.0+ | Included with Docker Desktop |
| Git | 2.30+ | [git-scm.com](https://git-scm.com/downloads) |

**API Keys Required:**
- [Supabase](https://supabase.com) (free tier) - Database & Storage
- [Anthropic](https://console.anthropic.com) (pay-as-you-go, ~$0.02-0.09/resume) - Claude API

<details>
<summary><strong>📦 Detailed Setup Guides</strong></summary>

- **Docker Installation**: [Windows / Linux / macOS guides](docs/INSTALLATION.md)
- **API Keys Configuration**: [Step-by-step Supabase & Anthropic setup](docs/API_KEYS.md)

</details>

### Setup (3 Steps)

```bash
# 1. Clone and configure
git clone https://github.com/StratosL/Arete.git
cd arete
cp .env.example .env
# Edit .env with your API keys - see docs/API_KEYS.md for detailed instructions

# 2. Run setup script
./scripts/setup/setup.sh  # Linux/Mac
setup.bat                  # Windows

# 3. Start application
docker-compose up --build
```

**Access the Application:**
- 🌐 **Web UI**: http://localhost:3000
- 📡 **API Docs**: http://localhost:8000/docs

### Quick Test

```bash
# Verify backend health
curl http://localhost:8000/health

# Test resume upload
curl -F "file=@test_resume.txt" http://localhost:8000/api/resume/upload
```

---

## 🏗️ Architecture

**Tech Stack:**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend Framework** | FastAPI 0.115+ | Async API with SSE streaming |
| **Frontend Framework** | React 18 + Vite 5 + TypeScript 5 | Modern, fast development |
| **UI Components** | shadcn/ui + Tailwind CSS | Accessible, consistent design |
| **Database** | Supabase PostgreSQL | Managed DB + Auth + Storage |
| **AI Engine** | Claude 3.5 Sonnet (via LiteLLM) | Resume parsing + optimization |
| **Document Processing** | pdfplumber, python-docx | Parse resumes |
| **PDF Generation** | ReportLab | ATS-compliant exports |
| **Testing** | pytest, Vitest, Playwright | 94.4% coverage |

**Architecture Pattern:** Vertical Slice Architecture (VSA).

- **[Rasmus Widing](https://rasmuswiding.com)** - Huge thanks for VSA!

Features organized by capability, not technical layer. Each slice (resume, jobs, optimization, export, github) contains routes, services, and schemas.

```
Frontend (React) → FastAPI Backend → Supabase + Claude API
                    ├── /resume        (upload, parse)
                    ├── /jobs          (analyze, scrape)
                    ├── /optimization  (AI streaming)
                    ├── /export        (PDF/DOCX)
                    └── /github        (profile analysis)
```

<details>
<summary><strong>📐 Architecture Deep Dive</strong></summary>

For complete technical documentation including:
- Complete directory structure
- Processing pipelines (Resume, Job Analysis, Optimization, Export)
- Data flow diagrams
- VSA pattern explanation
- Performance optimizations
- Enhanced Orchestrator Strategy

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

</details>

---

## 🔧 Development

### Kiro CLI Integration

Arete is optimized for AI-assisted development using **Kiro CLI** (AWS coding tool from **Dynamous Community**):

```bash
kiro @prime          # Load project context
kiro @plan-feature   # Create implementation plans
kiro @execute        # Systematic execution
kiro @code-review    # Quality checks
```

**Benefits:**
- Vertical Slice Architecture ideal for parallel AI-assisted development
- Enhanced Orchestrator Strategy enables zero integration issues
- Contract-first approach with API specifications
- Research-backed development with 95%+ success rate

Learn more: [docs/kiro-guide.md](docs/kiro-guide.md) | [.kiro/orchestration/](.kiro/orchestration/)

### Running Tests

```bash
# Backend tests (pytest)
cd backend && pytest

# Frontend tests (Vitest)
cd frontend && npm test

# E2E tests (Playwright)
npm run test:e2e

# Coverage report
pytest --cov=app --cov-report=html
```

### Code Quality

- **Ruff** - Linting and formatting (Python)
- **MyPy** - Strict type checking
- **ESLint + Prettier** - TypeScript/React standards
- **100% Validation Score** - 8/8 code quality standards enforced

```bash
# Run quality checks
cd backend && ruff check . && mypy app/
cd frontend && npm run lint
```

---

## 📚 Documentation

| Resource | Description |
|----------|-------------|
| **[Installation Guide](docs/INSTALLATION.md)** | Detailed Docker setup for Windows / Linux / macOS |
| **[API Keys Setup](docs/API_KEYS.md)** | Step-by-step Supabase & Anthropic configuration with screenshots |
| **[Architecture](docs/ARCHITECTURE.md)** | VSA patterns, pipelines, tech stack, design decisions |
| **[API Reference](http://localhost:8000/docs)** | Interactive OpenAPI documentation (requires running app) |
| **[Troubleshooting](docs/TROUBLESHOOTING.md)** | Common issues, debug commands, error solutions |
| **[PRD](PRD.md)** | Product Requirements Document |
| **[Kiro CLI Guide](docs/kiro-guide.md)** | AI-assisted development workflow |

---

## 🐛 Common Issues

<details>
<summary><strong>Resume parsing fails or returns empty data</strong></summary>

**Solutions:**
- Verify file format (PDF, DOCX, TXT only) and size (<10MB)
- Check Claude API key is valid: `python scripts/setup/validate_env.py`
- Review backend logs: `docker-compose logs backend`
- Try simpler file format (convert to TXT)
- Ensure sufficient Claude API credits

</details>

<details>
<summary><strong>Job analysis not working</strong></summary>

**Solutions:**
- Ensure job description is at least 50 characters
- For URL input, verify job posting is publicly accessible
- Check browser console for validation errors (F12)
- Try "Text Input" mode instead of URL
- Refresh page if form appears unresponsive

</details>

<details>
<summary><strong>Frontend build fails or shows blank page</strong></summary>

**Solutions:**
- Check Node.js version: `node --version` (requires 18+)
- Clear cache: `rm -rf node_modules && npm install`
- Verify environment variables in `.env`
- Check browser console for errors (F12)
- Restart Docker containers: `docker-compose restart`

</details>

<details>
<summary><strong>Database connection errors</strong></summary>

**Solutions:**
- Verify Supabase credentials in `.env`
- Run setup script: `./scripts/setup/setup.sh`
- Test connection: `python scripts/setup/validate_env.py`
- Check network connectivity to Supabase
- Review database logs in Supabase dashboard

</details>

**For more issues and solutions:** See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 🗺️ Roadmap

### ✅ MVP Complete - All 7 Phases Implemented

- **Phase 1:** Resume Upload & Parsing with GitHub integration
- **Phase 2:** Job Description Analysis with URL scraping
- **Phase 3:** AI Optimization with real-time SSE streaming
- **Phase 4:** Document Export with PDF and DOCX generation
- **Phase 5:** Cover Letter Generation with personalized content
- **Phase 6:** GitHub Contribution Analyzer with impact metrics
- **Phase 7:** Comprehensive Test Suite (144 tests, 100% pass rate)

### 🔜 Future Enhancements

- [ ] **Multi-Provider LLM Support** - Add OpenAI, Google Gemini, local models
- [ ] **Skill Gap Analyzer** - Identify missing skills with learning path recommendations
- [ ] **LinkedIn Profile Optimization** - AI-powered LinkedIn content suggestions
- [ ] **Application Tracking** - Dashboard to track job applications and status
- [ ] **Resume Version Management** - Save and compare multiple resume versions
- [ ] **Salary Negotiation Insights** - Market data and negotiation strategies
- [ ] **Company Research Integration** - Auto-fetch company culture and tech stack info

---

## 📊 Why Choose Arete?

### Arete vs. Generic Resume Tools

| Feature | Arete | Generic Tools |
|---------|-------|---------------|
| **Tech-Specific Intelligence** | ✅ Understands frameworks, languages, tech stacks | ❌ Generic keyword matching |
| **GitHub Integration** | ✅ Profile analysis with impact metrics | ❌ No code contribution analysis |
| **Real-Time Streaming** | ✅ Watch AI optimization live via SSE | ❌ Batch processing only |
| **Framework-Aware** | ✅ Knows React vs Angular, AWS vs GCP | ❌ Treats all keywords equally |
| **Technical Project Impact** | ✅ Quantifies stars, forks, repositories | ❌ No project metrics |
| **Kiro CLI Integration** | ✅ AI-assisted development workflow | ❌ Standard development only |
| **VSA Architecture** | ✅ Feature-based, AI-friendly structure | ❌ Traditional MVC layers |
| **ATS Compatibility Scoring** | ✅ Actionable ATS optimization tips | ⚠️ Basic formatting checks |
| **Vertical Slice Architecture** | ✅ Clean, maintainable codebase | ❌ Not applicable |

**Bottom Line:** Arete is built **by a developer, for developers**, with deep understanding of technical career progression, project impact, and engineering terminology.

---

## 🙏 Acknowledgments

### Project Information

**Arete** is a solo hackathon project created by **Stratos Louvaris**.

**Built with:**
- **[Kiro CLI](https://kiro.dev)** - AWS coding tool for AI-assisted development
- **[Dynamous Community](https://dynamous.ai)** - AI development community

**Powered by:**
- [Anthropic Claude API](https://www.anthropic.com/) - Advanced AI capabilities
- [Supabase](https://supabase.com) - Backend infrastructure
- [shadcn/ui](https://ui.shadcn.com/) - Beautiful UI components
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - Frontend framework

### Development Approach

This project demonstrates the power of AI-assisted development using **Vertical Slice Architecture** and the **Enhanced Orchestrator Strategy**, enabling rapid development while maintaining production-quality code standards.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**TL;DR:** Arete is free, open, and hackable. Fork it, extend it, use it commercially - just provide proper attribution.

---

## 🤝 Contributing

Contributions are welcome! This project is currently a solo effort, but community involvement is encouraged.

**Ways to contribute:**
- 🐛 Report bugs via [GitHub Issues](https://github.com/StratosL/Arete/issues)
- 💡 Suggest features via [GitHub Discussions](https://github.com/StratosL/Arete/discussions)
- 🔧 Submit pull requests (see contribution guidelines)
- 📖 Improve documentation
- ⭐ Star the repo if you find it useful!

---

<div align="center">

**Made with Love by Stratos Louvaris**

**Built with Kiro CLI for Dynamous Community Hackthon**

[GitHub](https://github.com/StratosL/Arete) • [Documentation](docs/) • [Report Issue](https://github.com/StratosL/Arete/issues)

</div>
