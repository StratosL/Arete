#!/bin/bash

echo "🔍 GitHub Integration Diagnostic Tool"
echo "======================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python3."
    exit 1
fi

# Install required packages if not available
echo "📦 Installing diagnostic dependencies..."
pip3 install requests > /dev/null 2>&1

# Run the diagnostic script
echo "🚀 Running diagnostic tests..."
python3 debug_github_integration.py

echo ""
echo "💡 Quick Fixes:"
echo "   - Backend not running: docker-compose up"
echo "   - Frontend not running: cd frontend && npm run dev"
echo "   - Check browser console at http://localhost:3000"
echo ""
echo "📋 Next Steps:"
echo "   1. Fix any failed tests above"
echo "   2. Test manually in browser"
echo "   3. Check browser console for errors"