# Mandatory Agent Gate Protocol - ACTIVE

## ENFORCEMENT MECHANISM: Tool Restrictions

**Orchestrator Capabilities:**
- ✅ READ: Can analyze current state
- ✅ RESEARCH: Can use glob/grep for investigation  
- ✅ COORDINATE: Can deploy subagents via use_subagent
- ❌ WRITE: Cannot modify files directly
- ❌ EXECUTE: Cannot run shell commands directly

## Protocol Enforcement

**Before Any Implementation:**
1. **Research Phase**: Use read/glob/grep to understand current state
2. **Plan Phase**: Analyze gaps and propose agent deployment
3. **Approval Gate**: Wait for user approval
4. **Agent Deployment**: MANDATORY use of use_subagent for all implementation
5. **Monitoring**: Track agent progress through checkpoints

**Violation Prevention:**
- **Technical**: Orchestrator lacks write/shell tools
- **Procedural**: All implementation must go through specialized agents
- **Quality**: Agents follow VSA patterns and quality standards

## Agent Deployment Requirements

**For Any Code Changes:**
```
use_subagent({
  "command": "InvokeSubagents",
  "content": {
    "subagents": [
      {
        "agent_name": "backend-agent|frontend-agent|infrastructure-agent",
        "query": "Specific implementation task",
        "relevant_context": "Current state findings and requirements"
      }
    ]
  }
})
```

**Quality Gates:**
- Agent must show @prime → @plan → @execute → @review workflow
- Plan must align with api-contracts.yaml
- Implementation must follow VSA patterns
- 30-minute checkpoints for progress monitoring

## Success Metrics

**Protocol Compliance:**
- ✅ 100% of implementations go through specialized agents
- ✅ Zero direct file modifications by orchestrator
- ✅ All changes follow quality standards
- ✅ Integration issues prevented through contract-first approach

**Status**: ACTIVE - Protocol violations now impossible
**Last Updated**: 2025-01-10T09:53:00Z
