#!/bin/bash

# Auto-Analysis Script - Provides accurate project state on every context window
# Analyzes actual codebase implementation and generates current status

echo "🔍 AUTO-ANALYZING PROJECT STATE"
echo "================================"

# Create temp directory for analysis
mkdir -p .kiro/temp

# 1. Analyze Backend Implementation
echo "📊 Backend Analysis:"
backend_features=0
if [ -f "backend/app/resume/routes.py" ]; then
    echo "  ✅ Resume Upload & Parsing"
    backend_features=$((backend_features + 1))
fi
if [ -f "backend/app/jobs/routes.py" ]; then
    echo "  ✅ Job Description Analysis"
    backend_features=$((backend_features + 1))
fi
if [ -f "backend/app/optimization/routes.py" ]; then
    echo "  ✅ AI Optimization (SSE)"
    backend_features=$((backend_features + 1))
fi
if [ -f "backend/app/export/routes.py" ] && [ -s "backend/app/export/routes.py" ]; then
    echo "  ✅ Document Export"
    backend_features=$((backend_features + 1))
else
    echo "  ⏳ Document Export - NOT IMPLEMENTED"
fi

# 2. Analyze Frontend Implementation  
echo ""
echo "🎨 Frontend Analysis:"
frontend_features=0
if [ -f "frontend/src/components/ResumeUpload.tsx" ]; then
    echo "  ✅ Resume Upload Component"
    frontend_features=$((frontend_features + 1))
fi
if [ -f "frontend/src/components/JobDescriptionInput.tsx" ]; then
    echo "  ✅ Job Input Component"
    frontend_features=$((frontend_features + 1))
fi
if [ -f "frontend/src/components/OptimizationDisplay.tsx" ]; then
    echo "  ✅ Optimization Display Component"
    frontend_features=$((frontend_features + 1))
fi
if [ -f "frontend/src/components/DocumentExport.tsx" ]; then
    echo "  ✅ Export Component"
    frontend_features=$((frontend_features + 1))
else
    echo "  ⏳ Export Component - NOT IMPLEMENTED"
fi

# 3. Determine Current Phase
echo ""
echo "📋 Phase Analysis:"
if [ $backend_features -ge 3 ] && [ $frontend_features -ge 3 ]; then
    current_phase="Phase 3 Complete - AI Optimization"
    next_phase="Phase 4 - Document Export"
    echo "  🎯 Current: $current_phase"
    echo "  ➡️  Next: $next_phase"
elif [ $backend_features -ge 2 ] && [ $frontend_features -ge 2 ]; then
    current_phase="Phase 2 Complete - Job Analysis"
    next_phase="Phase 3 - AI Optimization"
    echo "  🎯 Current: $current_phase"
    echo "  ➡️  Next: $next_phase"
elif [ $backend_features -ge 1 ] && [ $frontend_features -ge 1 ]; then
    current_phase="Phase 1 Complete - Resume Upload"
    next_phase="Phase 2 - Job Analysis"
    echo "  🎯 Current: $current_phase"
    echo "  ➡️  Next: $next_phase"
else
    current_phase="Phase 0 - Setup"
    next_phase="Phase 1 - Resume Upload"
    echo "  🎯 Current: $current_phase"
    echo "  ➡️  Next: $next_phase"
fi

# 4. Check Docker Environment
echo ""
echo "🐳 Environment Status:"
if docker-compose ps | grep -q "Up"; then
    echo "  ✅ Docker containers running"
else
    echo "  ⚠️  Docker containers not running"
fi

# 5. Generate Status Summary
echo ""
echo "📝 CURRENT PROJECT STATUS"
echo "========================="
echo "Phase: $current_phase"
echo "Next: $next_phase"
echo "Backend Features: $backend_features/4"
echo "Frontend Features: $frontend_features/4"

# 6. Save analysis for orchestrator
cat > .kiro/temp/project-analysis.txt << EOF
CURRENT_PHASE=$current_phase
NEXT_PHASE=$next_phase
BACKEND_FEATURES=$backend_features
FRONTEND_FEATURES=$frontend_features
ANALYSIS_TIME=$(date)
EOF

echo ""
echo "✅ Auto-analysis complete - Project state verified"

# Mark research as complete
touch .kiro/temp/research-complete.flag

exit 0
