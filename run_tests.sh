#!/bin/bash
# scripts/run_tests.sh

set -e

echo "🧪 Running TRIAD tests..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dev dependencies if needed
pip install -q pytest pytest-asyncio pytest-cov 2>/dev/null || true

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=term --cov-report=html

echo ""
echo "✅ Tests complete. Coverage report in htmlcov/index.html"
