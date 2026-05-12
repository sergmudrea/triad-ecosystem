#!/bin/bash
# scripts/quick_start.sh

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              TRIAD ECOSYSTEM - QUICK START                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
if [[ $(echo "$PYTHON_VERSION >= 3.10" | bc) -ne 1 ]]; then
    echo "❌ Python 3.10+ required (found $PYTHON_VERSION)"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Copy example config if needed
if [ ! -f "config/evolution.yaml" ]; then
    echo "📝 Creating config from example..."
    cp config/evolution.example.yaml config/evolution.yaml
fi

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v --tb=short 2>/dev/null || echo "   ⚠️ No tests found, skipping"

# Start the ecosystem
echo ""
echo "🚀 Starting TRIAD Ecosystem..."
echo ""
python run.py "$@"
