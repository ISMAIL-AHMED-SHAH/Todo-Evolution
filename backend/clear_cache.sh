#!/bin/bash
# Clear Python bytecode cache
# Run this if you experience stale import issues after schema changes

echo "Clearing Python bytecode cache..."

# Remove __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Remove .pyc files
find . -type f -name "*.pyc" -delete 2>/dev/null

# Remove .pyo files
find . -type f -name "*.pyo" -delete 2>/dev/null

echo "Cache cleared successfully!"
echo ""
echo "You can now restart your FastAPI server."
