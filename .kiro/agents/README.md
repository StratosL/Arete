# Kiro Agent Configuration Guide

## Overview

This directory contains three specialized Kiro CLI agents optimized for the Arete project. Each agent has been enhanced with:

- **Structured XML tags** for better parsing and clarity
- **Concrete code examples** showing good patterns vs anti-patterns
- **Chain-of-thought guidance** for complex problem-solving
- **Enhanced context** through auto-loaded resources
- **Error prevention patterns** to reduce common mistakes
- **Project-specific knowledge** integration

## Available Agents

### 1. Backend Agent (`backend-agent`)
**Specialization**: FastAPI + Python 3.12 + Supabase + LiteLLM + Claude API

**Use for**:
- Creating new API endpoints
- Implementing database operations with Supabase
- Integrating with Claude API via LiteLLM
- Adding async/await patterns
- Implementing VSA (Vertical Slice Architecture) features

**Auto-loaded context**:
- API contracts (api-contracts.yaml)
- All steering and reference documents
- Core backend modules
- Resume feature slice (as example)
- Project configuration files

### 2. Frontend Agent (`frontend-agent`)
**Specialization**: React 18 + TypeScript 5 + Vite 6 + shadcn/ui + Tailwind CSS

**Use for**:
- Building React components
- Implementing SSE streaming for real-time updates
- Adding form validation with React Hook Form + Zod
- Ensuring WCAG 2.1 accessibility compliance
- Creating responsive designs

**Auto-loaded context**:
- API contracts (api-contracts.yaml)
- Existing components and patterns
- TypeScript types and interfaces
- Frontend configuration files
- Steering documents

### 3. Infrastructure Agent (`infrastructure-agent`)
**Specialization**: Docker + Docker Compose + DevOps + Cross-platform deployment

**Use for**:
- Creating/optimizing Dockerfiles
- Configuring docker-compose.yml
- Managing environment variables
- Troubleshooting containerization issues
- Ensuring cross-platform compatibility

**Auto-loaded context**:
- Docker configuration files
- Environment templates
- Setup scripts (Linux, Mac, Windows)
- Steering documents

## Usage

### Quick Start

1. **Swap to an agent in Kiro CLI**:
   ```bash
   kiro-cli
   > /agent swap
   # Select the agent you want (backend-agent, frontend-agent, infrastructure-agent)
   ```

2. **Or start with a specific agent**:
   ```bash
   kiro-cli --agent backend-agent
   ```

### Recommended Workflow

Each agent follows the same mandatory workflow:

1. **`@prime`** - Load Arete project context
2. **`@plan-feature`** - Create detailed implementation plan
3. **`@execute`** - Implement systematically with validation
4. **`@code-review`** - Review code quality and fix issues

### Example Session

```bash
$ kiro-cli --agent backend-agent

[backend-agent] > @prime

# Agent loads all context automatically

[backend-agent] > I need to add a job analysis endpoint that accepts text or URL and extracts required skills

# Agent will:
# 1. Review API contracts
# 2. Check existing patterns
# 3. Create implementation plan
# 4. Ask for approval
# 5. Implement following VSA pattern
# 6. Add proper logging, error handling, type hints
# 7. Review against standards
```

## What's Different from Before

### Before (Old Prompts)
- ❌ Plain text sections
- ❌ No concrete examples
- ❌ Vague instructions
- ❌ No auto-loaded context
- ❌ Manual tool approval for every operation

### After (Enhanced Prompts)
- ✅ Structured XML tags for clarity
- ✅ Concrete code examples (good vs bad)
- ✅ Chain-of-thought problem-solving guidance
- ✅ Auto-loaded project context via resources field
- ✅ Pre-approved read/search tools (fewer interruptions)
- ✅ Git status auto-loaded on agent spawn
- ✅ Project-specific anti-patterns to avoid
- ✅ Success criteria checklists

## Key Features

### 1. Structured Tags
All prompts use XML tags for organization:
- `<role>`, `<mission>`, `<workflow>`
- `<project_context>`, `<specialization>`
- `<constraints>`, `<anti_patterns>`, `<success_criteria>`

This improves Claude's parsing and understanding.

### 2. Concrete Examples
Each agent includes working code examples:
- Backend: FastAPI endpoints, service patterns, logging
- Frontend: React components, API integration, SSE streaming
- Infrastructure: Dockerfiles, docker-compose, troubleshooting

### 3. Auto-Loaded Resources
The JSON configs use Kiro's `resources` field to automatically load:
- API contracts
- Steering documents
- Reference standards
- Existing code patterns
- Configuration files

No more manual context loading!

### 4. Pre-Approved Tools
Common tools are pre-approved to reduce interruptions:
- `read` - Read any file
- `glob` - Search for files by pattern
- `grep` - Search code content

Writing and shell commands still require approval for safety.

### 5. Dynamic Context via Hooks
On agent spawn, each agent automatically runs:
- `git status --porcelain` - See uncommitted changes
- `git branch --show-current` - Know current branch
- Service-specific checks (e.g., `docker-compose ps` for infrastructure)

### 6. Error Prevention
Each agent includes:
- Common anti-patterns to avoid
- Troubleshooting guides
- Error recovery procedures
- Success criteria checklists

## Tool Permissions

### Backend Agent
**Allowed without approval**: read, glob, grep
**Requires approval**: write (to backend files only), shell (Python tools, git)

### Frontend Agent
**Allowed without approval**: read, glob, grep
**Requires approval**: write (to frontend files only), shell (npm commands, git)

### Infrastructure Agent
**Allowed without approval**: read, glob, grep, shell (Docker/git commands)
**Requires approval**: write (to config files only)

## Tips for Best Results

1. **Be specific in your requests** - The agents have deep context, so you can be detailed
2. **Trust the workflow** - Let agents go through @prime → @plan → @execute → @review
3. **Review plans before implementation** - Agents will show you the plan first
4. **Provide feedback** - If an agent misses something, tell it directly
5. **Use the right agent** - Don't use backend agent for frontend tasks (it's constrained)

## Measuring Improvements

Track these metrics to see the impact:

| Metric | Expected Improvement |
|--------|---------------------|
| Errors per task | -40% |
| Context-switching | -50% |
| Time to completion | -25% |
| Code review issues | -30% |
| VSA pattern adherence | >95% |

## Troubleshooting

### Agent doesn't see my changes
The agent loads context on spawn. If you made changes after starting, you can:
```bash
> @prime  # Reload project context
```

### Agent asks for approval too often
Check if the tool is in `allowedTools` in the JSON config. You can add more tools if needed.

### Agent doesn't follow the pattern
Make sure you're using the workflow:
```bash
> @plan-feature [describe what you want]
# Review the plan
> @execute
```

### Agent modifies wrong files
Each agent has constraints. Backend won't touch frontend, etc. If this happens, check the agent you're using.

## Customization

You can modify the JSON configs to:
- Add more auto-loaded resources
- Change tool permissions
- Add more hooks
- Adjust which files can be written

See the [Kiro CLI documentation](https://kiro.dev/docs/cli/custom-agents/) for all options.

## Feedback

If you notice patterns that could be improved or common errors the agents make:
1. Note the specific issue
2. Update the relevant prompt with anti-patterns or examples
3. Test and iterate

These prompts are living documents that improve with use!
