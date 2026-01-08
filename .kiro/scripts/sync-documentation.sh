#!/bin/bash

# Documentation Sync Hook
# Automatically updates README.md after any implementation changes

echo "📚 Checking documentation sync..."

# Run the Python sync script
python3 .kiro/scripts/sync-readme.py

# Check if README was modified
if git diff --quiet README.md; then
    echo "✅ Documentation is in sync"
else
    echo "📝 README.md updated to reflect current implementation"
    echo "   Changes detected and synced automatically"
fi

exit 0
