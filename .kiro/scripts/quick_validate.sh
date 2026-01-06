#!/bin/bash
# Quick validation script for development workflow
# Runs essential checks from .kiro/reference/ standards

echo "🔍 Running Arete Code Quality Checks..."
echo ""

# Backend validation
echo "📦 Backend Validation:"
cd backend

# Python syntax check
echo -n "  • Python syntax: "
if python3 -m py_compile main.py app/core/*.py app/resume/*.py 2>/dev/null; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi

# Type checking (if mypy available)
echo -n "  • Type checking: "
if command -v mypy >/dev/null 2>&1; then
    if mypy --config-file pyproject.toml . 2>/dev/null; then
        echo "✅ PASS"
    else
        echo "❌ FAIL"
    fi
else
    echo "⏭️  SKIP (mypy not installed)"
fi

# Test execution
echo -n "  • Test suite: "
if python3 -m pytest tests/ -v --tb=short 2>/dev/null; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi

cd ..

# Frontend validation
echo ""
echo "🎨 Frontend Validation:"
cd frontend

# TypeScript compilation
echo -n "  • TypeScript: "
if npx tsc --noEmit 2>/dev/null; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi

# ESLint check
echo -n "  • ESLint: "
if npm run lint 2>/dev/null; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi

# Build test
echo -n "  • Build: "
if npm run build 2>/dev/null; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi

cd ..

echo ""
echo "🎉 Validation complete! Run 'python3 .kiro/scripts/validate_code_quality.py' for detailed analysis."
