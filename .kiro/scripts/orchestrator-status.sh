#!/bin/bash

echo "🎯 Enhanced Orchestrator Strategy - ACTIVE"
echo "📋 Quality Gates: Plan Approval → Contract Validation → 30min Checkpoints"
echo ""
echo "Available Specialized Agents:"
echo "  🔧 backend-agent     - FastAPI, LLM, Supabase, Resume parsing"
echo "  🎨 frontend-agent    - React, TypeScript, shadcn/ui, Components"  
echo "  🐳 infrastructure-agent - Docker, Environment, Deployment"
echo ""
echo "Orchestration Documents Loaded:"
ls -la .kiro/orchestration/ 2>/dev/null | grep -E "\.(md|json)$" | awk '{print "  📄 " $9}' || echo "  📄 No orchestration docs found"
echo ""
echo "Contract Status:"
if [ -f "api-contracts.yaml" ]; then
    echo "  ✅ api-contracts.yaml loaded"
else
    echo "  ❌ api-contracts.yaml missing"
fi
echo ""
echo "Ready for parallel development coordination!"
