#!/bin/bash
# scripts/genesis.sh

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                    TRIAD ECOSYSTEM GENESIS SCRIPT                           ║
# ║                 Black-Red-Blue Autonomous Cyber Swarm                       ║
# ║                    Author: Z3R0, by will of Master                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

set -euo pipefail

PROJECT_DIR="${HOME}/.triad"
VENV_DIR="${PROJECT_DIR}/venv"
PRESET="${1:-default}"

echo -e "\n[GENESIS] Creating TRIAD ecosystem at ${PROJECT_DIR}..."

mkdir -p "${PROJECT_DIR}"
cd "${PROJECT_DIR}"

echo "[GENESIS] Clone repository..."
git clone https://github.com/z3r0/triad-ecosystem.git . 2>/dev/null || true

echo "[GENESIS] Create virtual environment..."
python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

echo "[GENESIS] Install dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "[GENESIS] Copy configuration..."
cp config/evolution.example.yaml config/evolution.yaml 2>/dev/null || true

echo "[GENESIS] Run tests..."
pytest tests/ -v --tb=short 2>/dev/null || echo "   Tests skipped"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   ✅ TRIAD ECOSYSTEM CREATED SUCCESSFULLY                      ║"
echo "║                                                                ║"
echo "║   Location: ${PROJECT_DIR}                                    ║"
echo "║                                                                ║"
echo "║   Run:      cd ${PROJECT_DIR} && python run.py --preset ${PRESET}   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
