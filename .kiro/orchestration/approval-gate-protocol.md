# Approval Gate Protocol

## MANDATORY USER APPROVAL REQUIRED

### Before ANY Action:
1. **Research & Analysis**: Complete current state verification
2. **Proposal**: Present findings and recommended next steps
3. **Wait for Approval**: STOP and wait for explicit user permission
4. **Execute Only After Approval**: No autonomous actions

### Approval Required For:
- ✅ Subagent deployment (`use_subagent`)
- ✅ Major file modifications
- ✅ Implementation planning
- ✅ Architecture changes
- ✅ Any "what's next" responses

### Response Format:
```markdown
## Current State Analysis
[Research findings]

## Recommended Next Steps
[Specific proposed actions]

## Awaiting Your Approval
Please confirm if you want me to proceed with:
1. [Action 1]
2. [Action 2]

Type "approved" or "proceed" to continue, or provide alternative instructions.
```

### Violation Prevention:
- No autonomous subagent spawning
- No implementation without explicit permission
- Always present options, never assume approval
- Wait for user response before any execution

**Status**: ACTIVE - All actions require user approval
