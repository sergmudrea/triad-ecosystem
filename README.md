# 🧬 TRIAD: Autonomous Cyber Evolution Ecosystem

> **Black | Red (Supervisor) | Blue**  
> *Three roles. One memory. Infinite adaptation.*

[![CI/CD](https://github.com/sergmudrea/triad-ecosystem/actions/workflows/ci.yml/badge.svg)](https://github.com/sergmudrea/triad-ecosystem/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Research](https://img.shields.io/badge/Purpose-Research-yellow.svg)]()

---

## 📖 About

**TRIAD** is a research concept for a **closed-loop, self-evolving system** where three autonomous agents (Black, Red, Blue) interact, compete, adapt, and optimize a shared memory pool indefinitely.

- **Black** — Eternal predator. Scans, attacks, mutates on failure.
- **Red** — Evolution supervisor. Defines parameters, measures fitness, enforces decisions.
- **Blue** — Immune system. Patches, optimizes memory, replicates improvements.

> ⚠️ **IMPORTANT**: Runs ONLY in isolated sandboxes. No real network access.

---

## 🚀 Quick Start (One Command)

```bash
# Download and run the genesis script
curl -O https://raw.githubusercontent.com/sergmudrea/triad-ecosystem/main/scripts/genesis.sh
chmod +x genesis.sh
./genesis.sh

Or manually:
bash

git clone https://github.com/sergmudrea/triad-ecosystem.git
cd triad-ecosystem
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config/evolution.example.yaml config/evolution.yaml
python run.py --preset default

📁 Project Structure
text

triad-ecosystem/
├── .github/workflows/ci.yml    # CI/CD pipeline
├── src/
│   ├── agents/                 # Black, Red, Blue agents
│   ├── core/                   # Meta-memory, replication
│   ├── evolution/              # Parameters, fitness, decisions
│   ├── simulation/             # Sandbox, targets
│   └── visualization/          # Web dashboard
├── config/                     # YAML configurations
├── tests/                      # Unit tests
├── scripts/                    # genesis.sh, quick_start.sh
├── docker/                     # Dockerfile, docker-compose
├── docs/                       # ARCHITECTURE.md
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── pyproject.toml
├── run.py
├── .gitignore
├── LICENSE
└── README.md

⚙️ Configuration

Edit config/evolution.yaml:
yaml

mutation_rate_max: 50.0   # Increase for faster evolution
population_min: 5
population_max: 20

Presets
bash

python run.py --preset aggressive   # Fast evolution
python run.py --preset conservative # Stable
python run.py --preset research     # Exploratory

📊 Dashboard
bash

python run.py --dashboard
# Open http://localhost:8765

🐳 Docker
bash

docker build -t triad -f docker/Dockerfile .
docker run --network none triad

🧪 Testing
bash

pytest tests/ -v

⚠️ Disclaimer

FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY.
This system runs in COMPLETELY ISOLATED environments. Not a hacking tool.
📄 License

MIT — See LICENSE
✍️ Author

sergmudrea
