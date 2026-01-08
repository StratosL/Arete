#!/bin/bash

# Automated devlog update trigger script
# Detects significant changes and triggers devlog update

set -e

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Not in a git repository. Skipping devlog update."
    exit 0
fi

# Get recent changes (last 2 hours)
RECENT_COMMITS=$(git log --since="2 hours ago" --oneline | wc -l)
MODIFIED_FILES=$(git status --porcelain | wc -l)

# Define thresholds for significant changes
COMMIT_THRESHOLD=1
FILE_THRESHOLD=3

# Check if changes are significant enough
if [ "$RECENT_COMMITS" -ge "$COMMIT_THRESHOLD" ] || [ "$MODIFIED_FILES" -ge "$FILE_THRESHOLD" ]; then
    echo "🔄 Significant changes detected. Triggering devlog update..."
    echo "   Recent commits: $RECENT_COMMITS"
    echo "   Modified files: $MODIFIED_FILES"
    
    # Create marker file to indicate devlog update needed
    touch .kiro/.devlog-update-needed
    
    echo "✅ Devlog update marker created. Use @update-devlog to update."
else
    echo "ℹ️  No significant changes detected. Skipping devlog update."
fi
