# Mandatory Research Protocol

## CRITICAL RULE: Research Before Action

### Protocol Enforcement
**BEFORE ANY TASK EXECUTION OR AGENT DEPLOYMENT:**

1. **MANDATORY RESEARCH PHASE**
   ```
   Step 1: Read current codebase state
   Step 2: Verify implementation status  
   Step 3: Document findings
   Step 4: ONLY THEN propose next actions
   ```

2. **RESEARCH CHECKLIST** (Must complete ALL):
   - [ ] Backend implementation status verified
   - [ ] Frontend implementation status verified  
   - [ ] Integration points validated
   - [ ] Current phase completion confirmed
   - [ ] Next phase requirements identified

3. **VIOLATION PREVENTION**
   - No assumptions based on documentation alone
   - No agent deployment without current state verification
   - No "fixing" without confirming what's broken
   - No implementation without gap analysis

### Research Commands Sequence
```bash
# 1. Check directory structure
fs_read: backend/app/ and frontend/src/components/

# 2. Verify key endpoints exist
fs_read: main.py, App.tsx

# 3. Check implementation completeness
fs_read: specific feature files

# 4. Test environment status
execute_bash: docker-compose ps
```

### Reporting Template
```markdown
## Current Implementation Status

### Backend Status:
- [ ] Feature X: [COMPLETE/PARTIAL/MISSING]
- [ ] Feature Y: [COMPLETE/PARTIAL/MISSING]

### Frontend Status:  
- [ ] Component X: [COMPLETE/PARTIAL/MISSING]
- [ ] Component Y: [COMPLETE/PARTIAL/MISSING]

### Integration Status:
- [ ] End-to-end workflow: [WORKING/BROKEN/UNTESTED]

### Conclusion:
**Current Phase**: [Phase X - Status]
**Next Required**: [Specific gap or next phase]
**Action**: [Research complete - ready for next steps]
```

## Enforcement Mechanisms

### 1. Orchestrator Self-Check
Before any task, orchestrator must:
```
IF (task involves implementation OR agent deployment) {
    REQUIRE: Research phase completion
    VALIDATE: Current state documented
    CONFIRM: Gaps identified before action
}
```

### 2. Agent Deployment Gates
```
BEFORE agent deployment:
✅ Research protocol completed
✅ Current state verified  
✅ Specific gaps identified
✅ Implementation plan based on actual needs
```

### 3. Quality Gate Integration
Add to existing quality control:
- **Pre-Plan Gate**: Research must be complete
- **Plan Approval**: Must reference current state findings
- **Execution Gate**: Must address actual gaps only

## Implementation

### Immediate Changes:
1. Update enhanced-orchestrator-prompt.md to enforce this protocol
2. Add research validation to quality-control.md
3. Create research command templates
4. Integrate with existing checkpoint system

### Long-term Evolution:
1. Automated current state detection
2. Implementation gap analysis tools
3. Research completeness validation
4. Historical state tracking

---

**Status**: Active Protocol - Mandatory for All Tasks
**Violation Response**: Immediate halt and research requirement
**Success Metric**: Zero assumption-based implementation failures
