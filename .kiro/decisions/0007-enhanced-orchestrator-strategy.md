# 7. Enhanced Orchestrator Strategy with Protocol Enforcement

**Date**: 2026-01-06
**Status**: Accepted
**Deciders**: Stratos Louvaris
**Tags**: kiro, agents, workflow, orchestration

## Context

Arete was built using Kiro CLI with AI agents for parallel development:
- **Backend Agent**: Builds FastAPI backend (resume parsing, job analysis, optimization)
- **Frontend Agent**: Builds React frontend (UI components, state management)
- **Orchestrator Agent**: Coordinates backend and frontend agents

Initial approach (Phase 1-4): Basic orchestration with informal coordination
- Result: Integration failures, API contract mismatches, wasted development time

For Phase 5 (Cover Letter Generation), we needed better coordination to avoid previous mistakes.

## Decision Drivers

* **Past failures**: Lost 3 hours in Phase 3 due to API contract mismatch
* **Efficiency**: Need parallel development without constant human intervention
* **Quality**: Ensure integration works first time (no debugging cycles)
* **Scalability**: Should work for future features beyond Phase 5
* **Learning**: Document patterns for other Kiro users

## Considered Options

### 1. Sequential Development (No Orchestrator)

```
1. Backend agent builds API
2. Wait for backend to finish
3. Frontend agent reads backend code and builds UI
```

**Pros**:
- No coordination complexity
- No integration mismatches (frontend sees actual backend code)

**Cons**:
- **Slow** (can't work in parallel)
- **Underutilizes agents** (one sits idle while other works)
- **Estimated time**: 8 hours for Phase 5 (vs 4 hours with parallel)

### 2. Basic Orchestrator (Phase 1-4 Approach)

```
Orchestrator: "Backend agent, build cover letter API"
Orchestrator: "Frontend agent, build cover letter UI"

[Both work simultaneously with informal coordination]
```

**Pros**:
- Faster than sequential (parallel development)
- Simple orchestration logic

**Cons**:
- **Integration failures** (API contracts don't match)
- **Rework required** (3-hour debugging session in Phase 3)
- **No enforcement** (agents can deviate from plan)
- **Communication gaps** (backend changes schema, frontend doesn't know)

### 3. Contract-First Development (Manual Contract Writing)

```
1. Human writes API contract (OpenAPI spec)
2. Backend agent implements contract
3. Frontend agent implements against contract
```

**Pros**:
- Guaranteed integration (both follow same contract)
- Clear specification

**Cons**:
- **Requires human intervention** (defeats purpose of AI agents)
- **Slower** (human bottleneck)
- **Still possible for agents to deviate** (no enforcement)

### 4. Enhanced Orchestrator with Protocol Enforcement

```
Orchestrator creates shared API contract:
1. Define endpoints, schemas, error codes (BEFORE implementation)
2. Backend agent: "You MUST implement this exact contract"
3. Frontend agent: "You MUST use this exact contract"
4. Checkpoints: Verify both agents followed contract
5. Human approval only once (at contract design phase)
```

**Pros**:
- **Parallel development** with guaranteed integration
- **Contract enforcement** (agents can't deviate)
- **Single approval point** (human reviews contract, not implementation)
- **Quality gates** (checkpoints ensure compliance)
- **Reusable pattern** (works for all future features)

**Cons**:
- More complex orchestrator logic
- Requires orchestrator to design good contracts
- Checkpoints add some overhead (but save time on debugging)

## Decision Outcome

Chosen option: **Enhanced Orchestrator with Protocol Enforcement**

### Justification

For Phase 5 (Cover Letter Generation):

1. **Time Savings**:
   ```
   Without enforcement (Phase 3 experience):
   - Development: 4 hours
   - Integration debugging: 3 hours
   - Total: 7 hours

   With enforcement (Phase 5 actual):
   - Contract design: 0.5 hours
   - Development: 4 hours (parallel)
   - Integration: 0 hours (worked first time!)
   - Total: 4.5 hours

   Saved: 2.5 hours (36% time reduction)
   ```

2. **Zero Integration Issues**:
   - Contract defined upfront
   - Both agents enforced to follow contract
   - First integration attempt: **Success** (no debugging needed)

3. **Better Quality**:
   - Consistent error handling (all endpoints return same error format)
   - Consistent validation (all inputs validated against schemas)
   - Consistent response structure (all success responses follow pattern)

4. **Reusable Pattern**:
   - Can apply to Phase 6, 7, 8 (future features)
   - Other Kiro users can adopt this pattern
   - Documented in devlog for reference

### Implementation

**Step 1: Orchestrator Designs API Contract**

```markdown
# .kiro/contracts/cover-letter-api.md

## POST /api/cover-letters/generate

**Request**:
```json
{
  "resume_id": "uuid",
  "job_id": "uuid",
  "tone": "professional" | "casual" | "enthusiastic",
  "length": "short" | "medium" | "long"
}
```

**Response (200 OK)**:
```json
{
  "id": "uuid",
  "content": "Dear Hiring Manager...",
  "created_at": "2026-01-06T10:00:00Z"
}
```

**Response (400 Bad Request)**:
```json
{
  "error": {
    "code": "INVALID_TONE",
    "message": "Tone must be professional, casual, or enthusiastic"
  }
}
```

## GET /api/cover-letters/stream/{id}

**Response**: SSE stream
- Event type: `progress` | `chunk` | `complete` | `error`
- See SSE streaming spec in ADR-0005
```

**Step 2: Orchestrator Enforces Contract**

```markdown
# Orchestrator → Backend Agent

You MUST implement the cover letter API with this EXACT contract:
[Include full contract from .kiro/contracts/cover-letter-api.md]

CRITICAL REQUIREMENTS:
1. Request/response schemas must match exactly
2. Error codes must use specified format
3. SSE streaming must follow ADR-0005 pattern
4. Add integration tests validating contract compliance

Do NOT deviate from this contract. If you think the contract needs changes, STOP and ask the orchestrator.
```

```markdown
# Orchestrator → Frontend Agent

You MUST build the cover letter UI using this EXACT contract:
[Include full contract from .kiro/contracts/cover-letter-api.md]

CRITICAL REQUIREMENTS:
1. API calls must match request schemas exactly
2. Handle all error codes specified in contract
3. Use SSE streaming as specified in ADR-0005
4. Add TypeScript types matching the contract

Do NOT make assumptions. Use the contract as source of truth.
```

**Step 3: Quality Gates (Checkpoints)**

```markdown
# Orchestrator Verification Checklist

Backend Agent Checkpoint:
- [ ] All endpoints implemented from contract
- [ ] Request/response schemas match contract
- [ ] Error codes match contract
- [ ] Integration tests cover all contract scenarios
- [ ] No extra endpoints added (contract is complete)

Frontend Agent Checkpoint:
- [ ] All contract endpoints have corresponding API calls
- [ ] TypeScript types match contract schemas
- [ ] Error handling covers all contract error codes
- [ ] SSE streaming implementation matches ADR-0005
- [ ] No hardcoded assumptions (all from contract)

Integration Checkpoint:
- [ ] Frontend can call backend successfully
- [ ] All validation errors handled correctly
- [ ] SSE streaming works end-to-end
- [ ] No contract violations detected
```

**Step 4: Pre-Approved Tools (Efficiency Boost)**

```markdown
# .kiro/orchestrator-config.md

## Pre-Approved Tools for Backend Agent
- Read/Write in backend/app/cover_letters/
- Run pytest for testing
- Read from .kiro/contracts/
- Install Python packages (reportlab, litellm, etc.)

## Pre-Approved Tools for Frontend Agent
- Read/Write in frontend/src/features/cover-letter/
- Run npm scripts (dev, build, test)
- Read from .kiro/contracts/
- Install npm packages

NO APPROVAL NEEDED for these tools (reduces interruptions by 50%)
```

### Consequences

**Good**:
- ✅ **Zero integration failures** in Phase 5 (vs 3 hours debugging in Phase 3)
- ✅ **36% time savings** (4.5 hours vs 7 hours)
- ✅ **Better code quality** (consistent patterns across backend/frontend)
- ✅ **Single human approval point** (review contract, not implementation)
- ✅ **50% fewer interruptions** (pre-approved tools)
- ✅ **Reusable pattern** (documented for future phases)

**Bad**:
- ⚠️ **Orchestrator complexity increased** (more upfront design work)
- ⚠️ **Rigid contracts** (hard to change mid-development, but this is actually good)
- ⚠️ **Learning curve** (orchestrator needs to understand contract design)

**Neutral**:
- Checkpoints add ~15 minutes overhead (but save hours on debugging)
- Contract files need maintenance (but serve as living documentation)
- Requires orchestrator to think through integration before coding (good practice)

## Validation

Success criteria:

✅ **Criterion 1**: Zero integration failures on first attempt
- Result: **Phase 5 integrated successfully on first try** (vs 3 failures in Phase 3)

✅ **Criterion 2**: Time savings >20%
- Result: **36% time savings** (4.5 hours vs 7 hours)

✅ **Criterion 3**: Reduced human interruptions
- Result: **50% fewer approval requests** (pre-approved tools)

✅ **Criterion 4**: Consistent code quality
- Result: **All endpoints follow same patterns** (error handling, validation, responses)

✅ **Criterion 5**: Reusable pattern
- Result: **Documented in devlog, can apply to Phase 6+**

## Lessons Learned

**What Worked**:
1. **Contract-first design**: Spending 30 minutes on contract saved 3 hours debugging
2. **Explicit enforcement**: Telling agents "You MUST follow this contract" worked better than "please try to align"
3. **Pre-approved tools**: Listing allowed tools upfront reduced interruptions dramatically
4. **Quality gates**: Checkpoints caught deviations early (before integration)

**What Didn't Work Initially**:
1. **Informal coordination**: "Backend and frontend, please coordinate" led to mismatches
2. **Implicit contracts**: Assuming agents would infer API structure from context failed
3. **Post-integration validation**: Finding issues AFTER integration was too late

**Improvements for Next Time**:
1. **Contract templates**: Create reusable contract templates for common patterns (CRUD, streaming, file upload)
2. **Automated contract validation**: Script to verify backend/frontend match contract
3. **Contract versioning**: Track contract changes (v1, v2) as features evolve

## Related Decisions

* [0001-vertical-slice-architecture.md] - Each feature slice has its own contract
* [0005-sse-streaming-vs-websockets.md] - SSE streaming patterns referenced in contracts
* [0002-litellm-abstraction.md] - LLM abstraction allows easy contract changes

## References

* **Implementation**: See `.kiro/devlog/devlog.md` (Phase 5 section)
* **Contract Example**: `.kiro/contracts/cover-letter-api.md`
* **Orchestrator Prompts**: `.kiro/prompts/enhanced-orchestrator.md`
* **Lessons Learned**: `.kiro/devlog/devlog.md` (Protocol Enforcement Lessons)
* **Pre-Approved Tools**: `.kiro/orchestrator-config.md`

## Future Applications

This pattern should be used for:
- **Phase 6**: Job matching feature (backend + frontend + contract)
- **Phase 7**: Resume templates (backend + frontend + contract)
- **Phase 8**: Analytics dashboard (backend + frontend + contract)

**Template for Future Contracts**:
```markdown
# Contract: [Feature Name]

## Endpoints
- POST /api/[feature]/create
- GET /api/[feature]/{id}
- PUT /api/[feature]/{id}
- DELETE /api/[feature]/{id}

## Schemas
[Define request/response schemas]

## Error Codes
[Define all error scenarios]

## Streaming (if applicable)
[Reference ADR-0005 SSE pattern]
```
