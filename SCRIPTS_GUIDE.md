# Arete Scripts Guide

> A comprehensive guide to all scripts in the Arete project, their purposes, and organization rationale.

---

## Table of Contents

1. [Organization Philosophy](#organization-philosophy)
2. [Directory Structure](#directory-structure)
3. [Scripts by Category](#scripts-by-category)
   - [Setup Scripts](#1-setup-scripts)
   - [Database Scripts](#2-database-scripts)
   - [Validation Scripts](#3-validation-scripts)
   - [Testing Scripts](#4-testing-scripts)
   - [Development Workflow Scripts](#5-development-workflow-scripts-kiro)
4. [Quick Reference](#quick-reference)
5. [Running the Scripts](#running-the-scripts)

---

## Organization Philosophy

Our scripts are organized following the **separation of concerns** principle:

| Category | Purpose | When to Use |
|----------|---------|-------------|
| **Setup** | Initialize the application environment | Once, during initial setup |
| **Database** | Manage database schema and configuration | When modifying database |
| **Validation** | Verify system health and production readiness | Before demos, after changes |
| **Testing** | Debug specific features and manual testing | During development, troubleshooting |
| **Kiro Workflow** | AI-assisted development automation | During development workflow |

This structure demonstrates:
- **Clean code hygiene** - Related files grouped logically
- **Self-documenting organization** - Folder names explain purpose
- **Scalability** - Easy to add new scripts to appropriate categories
- **Demo-readiness** - Judges can quickly find and understand each script

---

## Directory Structure

```
arete/
├── scripts/
│   ├── setup/                    # One-time initialization
│   │   ├── setup.sh
│   │   ├── setup_supabase.py
│   │   └── validate_env.py
│   │
│   ├── database/                 # Database management
│   │   ├── disable_rls.py
│   │   ├── add_optimized_data_column.py
│   │   └── verify_schema.py
│   │
│   ├── validation/               # System health & readiness
│   │   ├── system_validation.py
│   │   ├── frontend_validation.py
│   │   ├── test_optimization_persistence.py
│   │   └── validate_wsl2.py
│   │
│   └── testing/                  # Manual testing & debugging
│       ├── github/               # GitHub feature testing
│       │   ├── debug_github_integration.py
│       │   ├── test_github_integration.py
│       │   ├── test_github_live.py
│       │   ├── quick_github_check.py
│       │   ├── run_github_diagnostic.sh
│       │   ├── run_github_tests.sh
│       │   └── test_frontend_github.html
│       │
│       ├── features/             # Other feature tests
│       │   └── test_cover_letter.py
│       │
│       └── fixtures/             # Test data files
│           ├── test_sample_resume.txt
│           └── test_resume_github.txt
│
└── .kiro/scripts/                # AI-assisted workflow automation
    ├── quick_validate.sh
    ├── validate_code_quality.py
    ├── check-devlog-update.sh
    ├── validate-research.sh
    ├── sync-documentation.sh
    ├── sync-readme.py
    ├── orchestrator-status.sh
    └── auto-analyze-project.sh
```

---

## Scripts by Category

### 1. Setup Scripts
**Location:** `scripts/setup/`

Scripts run once during initial project setup.

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup.sh` | Main setup script - orchestrates all initialization steps | `./scripts/setup/setup.sh` |
| `setup_supabase.py` | Creates Supabase storage buckets and policies (cannot be done via migrations) | `python scripts/setup/setup_supabase.py` |
| `validate_env.py` | Validates all required environment variables are set correctly | `python scripts/setup/validate_env.py` |

**When to run:** After cloning the repository, before first `docker-compose up`

---

### 2. Database Scripts
**Location:** `scripts/database/`

Scripts for database schema management and configuration.

| Script | Purpose | Usage |
|--------|---------|-------|
| `verify_schema.py` | Verifies database schema matches expected structure | `python scripts/database/verify_schema.py` |
| `disable_rls.py` | Disables Row Level Security for MVP development (simplifies auth) | `python scripts/database/disable_rls.py` |
| `add_optimized_data_column.py` | Migration script to add optimized_data column for storing AI suggestions | `python scripts/database/add_optimized_data_column.py` |

**When to run:** When database schema changes are needed or to verify integrity

---

### 3. Validation Scripts
**Location:** `scripts/validation/`

Scripts that verify system health and production readiness.

| Script | Purpose | Usage |
|--------|---------|-------|
| `system_validation.py` | **Comprehensive MVP validation** - Tests ALL 10 critical features end-to-end | `python scripts/validation/system_validation.py` |
| `frontend_validation.py` | Tests frontend-backend integration using Selenium | `python scripts/validation/frontend_validation.py` |
| `test_optimization_persistence.py` | Verifies AI optimization suggestions persist correctly to database | `python scripts/validation/test_optimization_persistence.py` |
| `validate_wsl2.py` | Validates WSL2 environment configuration (Windows users) | `python scripts/validation/validate_wsl2.py` |

#### Highlight: System Validation Script

The `system_validation.py` script is our **primary demo validation tool**. It tests:

1. Backend Health - FastAPI server accessibility
2. Resume Upload - File upload and parsing
3. Resume Parsing Quality - Extraction accuracy
4. GitHub Integration - Profile analysis API
5. Job Analysis (Text) - Text-based job analysis
6. Job Analysis (URL) - URL scraping functionality
7. AI Optimization - SSE streaming optimization
8. Cover Letter Generation - AI-generated cover letters
9. PDF Export - Document generation
10. DOCX Export - Document generation

**Output:** Generates `validation_report.json` with detailed results

```bash
# Run before any demo
python scripts/validation/system_validation.py

# Expected output:
# ✅ 10/10 tests passed - System validation PASSED - Ready for demo!
```

---

### 4. Testing Scripts
**Location:** `scripts/testing/`

Scripts for manual testing, debugging, and development verification.

#### 4.1 GitHub Integration Testing
**Location:** `scripts/testing/github/`

Comprehensive testing suite for the GitHub Contribution Analyzer feature.

| Script | Purpose | Usage |
|--------|---------|-------|
| `debug_github_integration.py` | **Main diagnostic tool** - Tests backend API, frontend components, resume upload with GitHub, provides curl commands | `python scripts/testing/github/debug_github_integration.py` |
| `test_github_integration.py` | Tests GitHub service imports and API endpoint | `python scripts/testing/github/test_github_integration.py` |
| `test_github_live.py` | Quick live test of GitHub API endpoint | `python scripts/testing/github/test_github_live.py` |
| `quick_github_check.py` | Minimal/fastest GitHub API check | `python scripts/testing/github/quick_github_check.py` |
| `run_github_diagnostic.sh` | Shell wrapper that runs the diagnostic tool | `./scripts/testing/github/run_github_diagnostic.sh` |
| `run_github_tests.sh` | Runs the complete GitHub test suite | `./scripts/testing/github/run_github_tests.sh` |
| `test_frontend_github.html` | Browser-based GitHub API test page | Open in browser |

**Why so many GitHub scripts?** The GitHub Contribution Analyzer was a key feature requiring thorough testing. These scripts demonstrate our testing methodology:
- Quick checks for rapid iteration
- Comprehensive diagnostics for troubleshooting
- Browser-based testing for frontend validation
- Shell wrappers for CI/CD integration

#### 4.2 Feature Tests
**Location:** `scripts/testing/features/`

| Script | Purpose | Usage |
|--------|---------|-------|
| `test_cover_letter.py` | Tests the cover letter generation endpoint | `python scripts/testing/features/test_cover_letter.py` |

#### 4.3 Test Fixtures
**Location:** `scripts/testing/fixtures/`

Sample data files used across multiple tests.

| File | Purpose |
|------|---------|
| `test_sample_resume.txt` | Comprehensive sample resume with all sections (experience, skills, projects, education) |
| `test_resume_github.txt` | Minimal sample resume for quick tests |

---

### 5. Development Workflow Scripts (Kiro)
**Location:** `.kiro/scripts/`

Scripts that integrate with Kiro CLI for AI-assisted development workflow.

| Script | Purpose | Usage |
|--------|---------|-------|
| `quick_validate.sh` | Quick code quality checks (syntax, types, tests) | `./.kiro/scripts/quick_validate.sh` |
| `validate_code_quality.py` | Detailed code quality analysis against all standards | `python .kiro/scripts/validate_code_quality.py` |
| `check-devlog-update.sh` | Checks if devlog needs updating | `./.kiro/scripts/check-devlog-update.sh` |
| `validate-research.sh` | Validates research documents are complete | `./.kiro/scripts/validate-research.sh` |
| `sync-documentation.sh` | Synchronizes documentation across the project | `./.kiro/scripts/sync-documentation.sh` |
| `sync-readme.py` | Syncs README with current project state | `python .kiro/scripts/sync-readme.py` |
| `orchestrator-status.sh` | Shows status of AI agent orchestration | `./.kiro/scripts/orchestrator-status.sh` |
| `auto-analyze-project.sh` | Automatically analyzes project structure | `./.kiro/scripts/auto-analyze-project.sh` |

**Why separate from `scripts/`?** These are development-time tools specific to the Kiro CLI workflow, not application operations. They support:
- Code quality enforcement
- Documentation synchronization
- AI-assisted development patterns
- Multi-agent orchestration

---

## Quick Reference

### For Hackathon Judges

**To verify the system works:**
```bash
python scripts/validation/system_validation.py
```

**To understand GitHub feature testing:**
```bash
python scripts/testing/github/debug_github_integration.py
```

**To check code quality:**
```bash
python .kiro/scripts/validate_code_quality.py
```

### For Developers

| Task | Command |
|------|---------|
| Initial setup | `./scripts/setup/setup.sh` |
| Validate environment | `python scripts/setup/validate_env.py` |
| Full system test | `python scripts/validation/system_validation.py` |
| Quick code check | `./.kiro/scripts/quick_validate.sh` |
| Debug GitHub | `python scripts/testing/github/debug_github_integration.py` |

---

## Running the Scripts

### Prerequisites

Most scripts require:
- Python 3.12+
- Backend running (`docker-compose up`)
- Required packages (`pip install requests`)

### From Project Root

All scripts are designed to be run from the project root directory:

```bash
# Correct
python scripts/validation/system_validation.py

# Incorrect (don't cd into scripts folder)
cd scripts/validation && python system_validation.py
```

### Windows Users

Use `python` instead of `python3`:
```cmd
python scripts\validation\system_validation.py
```

For shell scripts, use Git Bash or WSL:
```bash
./scripts/setup/setup.sh
```

---

## Summary

| Directory | Count | Purpose |
|-----------|-------|---------|
| `scripts/setup/` | 3 | Initial project setup |
| `scripts/database/` | 3 | Database management |
| `scripts/validation/` | 4 | System health verification |
| `scripts/testing/github/` | 7 | GitHub feature testing |
| `scripts/testing/features/` | 1 | Other feature tests |
| `scripts/testing/fixtures/` | 2 | Test data files |
| `.kiro/scripts/` | 8 | Development workflow |
| **Total** | **28** | |

This organization reflects our commitment to **clean code practices**, **thorough testing**, and **maintainable project structure**.

---

*Last updated: January 2025*
*Arete - AI-Powered Resume Optimizer for Tech Professionals*
