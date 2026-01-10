# 1. Use Vertical Slice Architecture (VSA)

**Date**: 2026-01-05
**Status**: Accepted
**Deciders**: Stratos Louvaris
**Tags**: architecture, structure, patterns

## Context

We need to organize the Arete codebase for a 3-week hackathon with potential for AI-assisted development (Kiro CLI). Traditional layered architecture (controllers/, services/, models/) would require changes across multiple directories for each feature.

## Decision Drivers

* Need rapid feature development (hackathon timeframe)
* Want AI agents to work on features in parallel (backend-agent, frontend-agent)
* Reduce merge conflicts between simultaneous changes
* Make it easy to add new features without touching existing code
* Enable feature-based testing (test resume parsing independently from job analysis)

## Considered Options

### 1. Layered Architecture (Traditional)

```
backend/
├── controllers/    # All HTTP handlers
├── services/       # All business logic
├── repositories/   # All data access
└── models/        # All data structures
```

**Pros**:
- Familiar to most developers
- Clear separation of concerns by technical layer
- Standard in many frameworks

**Cons**:
- Changes require touching multiple directories
- Hard to work on features in parallel
- Everything depends on everything
- Difficult for AI agents (need to coordinate across layers)

### 2. Feature Modules (Angular-style)

```
backend/
├── resume-module/
│   ├── resume.controller.ts
│   ├── resume.service.ts
│   └── resume.module.ts
```

**Pros**:
- Features grouped together
- Better than pure layers

**Cons**:
- Still requires module imports/exports
- Complex dependency injection
- Overkill for FastAPI (Python, not NestJS)

### 3. Vertical Slice Architecture (VSA)

```
backend/app/
├── resume/          # Complete resume feature
│   ├── routes.py    # HTTP + validation
│   ├── service.py   # Business logic
│   ├── schemas.py   # Pydantic models
│   └── parser.py    # Feature-specific utilities
├── jobs/            # Complete job analysis feature
│   ├── routes.py
│   ├── service.py
│   └── schemas.py
```

**Pros**:
- Each feature is completely independent
- Can develop features in parallel (no conflicts)
- Easy to add new features (copy a slice structure)
- Perfect for AI agents (each owns a slice)
- Easy to test (slice-by-slice)
- Can delete features without breaking others

**Cons**:
- Some code duplication (each slice might have similar logic)
- Less "pure" separation of concerns
- Developers unfamiliar with pattern need explanation

## Decision Outcome

Chosen option: **Vertical Slice Architecture (VSA)**

### Justification

For Arete's hackathon context:

1. **Parallel AI Development**: Backend-agent can work on `/resume` while frontend-agent works on components, with zero conflicts

2. **Speed**: Added cover letter feature in 2 hours by copying optimization/ structure

3. **Independence**: If resume parsing breaks, job analysis still works

4. **Testing**: Can test each feature slice independently

5. **Clarity**: New developers (or AI agents) see everything related to "resume" in one place

### Implementation

```python
# backend/app/resume/routes.py
from fastapi import APIRouter
from .service import resume_service
from .schemas import ResumeResponse

router = APIRouter(prefix="/resume", tags=["resume"])

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(file: UploadFile):
    # Everything resume-related in this directory
    result = await resume_service.process(file)
    return result
```

Each slice is a mini-application:
- Routes (HTTP interface)
- Service (business logic)
- Schemas (data validation)
- Utilities (feature-specific helpers)

### Consequences

**Good**:
- ✅ Added 4 feature slices in 2 weeks (resume, jobs, optimization, export)
- ✅ Zero merge conflicts between backend-agent and frontend-agent
- ✅ Cover letter feature added by copying optimization/ (2 hours vs estimated 6 hours)
- ✅ Each slice independently testable

**Bad**:
- ⚠️ Some duplicated code (validation logic similar across slices)
- ⚠️ Core utilities (database, LLM) still in core/ (hybrid approach)

**Neutral**:
- Learning curve for developers unfamiliar with VSA
- Documentation needed to explain the pattern

## Validation

Success criteria:

✅ **Criterion 1**: Can add new feature without modifying existing slices
- Result: Added export/ feature, zero changes to resume/ or jobs/

✅ **Criterion 2**: AI agents can work in parallel without conflicts
- Result: Backend-agent and frontend-agent worked simultaneously, no conflicts

✅ **Criterion 3**: Features are independently testable
- Result: pytest backend/app/resume/ runs only resume tests

✅ **Criterion 4**: New developers understand structure in <10 minutes
- Result: README architecture section explains it clearly

## Related Decisions

* [0007-enhanced-orchestrator-strategy.md] - Parallel development enabled by VSA
* [0002-litellm-abstraction.md] - LLM abstraction sits in core/ (shared across slices)

## References

* [VSA Pattern Guide](.kiro/reference/vsa-patterns.md)
* [Jimmy Bogard - Vertical Slice Architecture](https://www.youtube.com/watch?v=SUiWfhAhgQw)
