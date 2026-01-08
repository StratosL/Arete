#!/bin/bash

# Orchestrator status display with devlog automation
# Shows current project status and devlog update notifications

echo "🎯 Enhanced Orchestrator Strategy - ACTIVE"
echo "📋 Quality Gates: Plan Approval → Contract Validation → 30min Checkpoints"
echo ""
echo "Available Specialized Agents:"
echo "  🔧 backend-agent     - FastAPI, LLM, Supabase, Resume parsing"
echo "  🎨 frontend-agent    - React, TypeScript, shadcn/ui, Components"
echo "  🐳 infrastructure-agent - Docker, Environment, Deployment"
echo ""
echo "Orchestration Documents Loaded:"
echo "  📄 control-dashboard.md"
echo "  📄 quality-control.md"
echo ""
echo "Contract Status:"
echo "  ✅ api-contracts.yaml loaded"
echo ""

# Check for devlog update marker
if [ -f ".kiro/.devlog-update-needed" ]; then
    echo "📝 DEVLOG UPDATE NEEDED"
    echo "   Use @update-devlog to document recent changes"
    echo ""
fi

echo "Ready for parallel development coordination!"
echo ""
