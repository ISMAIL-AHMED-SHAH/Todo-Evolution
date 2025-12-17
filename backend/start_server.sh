#!/bin/bash
# Startup script for FastAPI server with cache clearing

echo "=== Starting FastAPI Server ===" echo ""

# Clear Python bytecode cache
echo "Clearing Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
find . -name "*.pyo" -delete 2>/dev/null
echo "Cache cleared"

# Set environment variables to disable bytecode writing
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Start server
echo ""
echo "Starting Uvicorn server..."
python -B -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
