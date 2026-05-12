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

🔬 Reality Audit: Simulation vs. Production

    "A shadow is perfect in shape but cannot grasp. This document tells you exactly where the shadow ends and the weapon begins."

TRIAD is a research-grade evolutionary architecture prototype. It models the complete lifecycle of autonomous cyber operations—reconnaissance, exploitation, adaptation, defense, and memory optimization—in a fully simulated environment. Below is an honest breakdown of what is real and what is simulated, so contributors understand exactly where to focus hardening efforts.
Infrastructure Layer (Production-Ready)
Component	Status	Description
MetaMemory	✅ Production	AES-256 encryption via cryptography.fernet, LZ4 compression, SHA-256 deduplication, TTL expiration, Redis persistence. Rippable for any C2 framework.
ReplicationEngine	✅ Production	Async pub/sub propagation with subscriber callbacks. Distributed state sharing pattern used in real systems.
AsyncIO Concurrency	✅ Production	Full asyncio event loop, concurrent agent execution, cancellable tasks, SIGINT/SIGTERM signal handling.
Evolution Parameters	✅ Production	Dataclass-based parameter system with presets (default/aggressive/conservative/research) and dynamic adjustment.
Algorithms Layer (Academically Correct, Synthetically Fed)
Component	Algorithm	Data Reality
Novelty Search	✅ Correct	k-nearest-neighbor behavioral distance, archive maintenance, novelty-weighted fitness. Operates on simulated agent histories.
MAP-Elites	✅ Correct	Grid-based quality-diversity archive, niche competition, coverage tracking, heatmap generation. Fed synthetic fitness values.
Coevolution	✅ Correct	Black vs Blue payoff matrix, round-robin tournament evaluation. Success determined by np.random.random(), not real detection.
Decision Engine	✅ Correct	Threshold-based selection mechanics (cull/mutate/promote). Standard evolutionary algorithm pattern.
Fitness Calculator	✅ Correct	Weighted multi-metric scoring. Inputs are synthetic success/failure flags.
Simulation Layer (What Stands Between Shadow and Weapon)
Simulation Component	What It Does Now	What Real Replacement Looks Like
Sandbox.scan()	Returns hardcoded fake targets	nmap, masscan, zgrab2, or raw sockets via scapy
Sandbox.run_exploit()	random.random() < 0.7 success check	Metasploit RPC, custom exploit scripts, C2 agent deployment via pwnlib
Sandbox.simulate_attack()	await asyncio.sleep(0.2) then Success	Real sandbox execution (VM with syscall tracing, network capture)
BlueAgent._apply_patch()	await asyncio.sleep(0.5) then "patched"	Actual firewall API calls (iptables, Windows Firewall COM), GPO deployment
BlueAgent.deploy_rules()	Prints "Deployed N rules"	Sigma rule push to SIEM (Splunk/Elastic), YARA rule deployment, OSQuery config
BlackAgent.genome.exploit_ids	Strings like mutated_T1059_4837	CVE IDs, Metasploit module paths, custom binary payloads with real shellcode
Road to Production

The gap between this prototype and a real autonomous cyber platform is approximately one focused development sprint:

    Rip out the Sandbox mock layer

    Replace with real tool wrappers (Nmap, Metasploit, Impacket, CrackMapExec)

    Wire Target objects to actual network discovery output

    Replace random.random() with real exploit return codes

    Connect BlueAgent to real firewall/EDR/SIEM APIs

    Deploy against isolated lab environment with vulnerable VMs

This project knows exactly what it is and what it is not. The architecture is correct. The algorithms are genuine. The simulation is honest. Contributions that bridge any component from the Simulation column to the Production column are welcome.
📊 Complexity Metrics
Metric	Value
Total Source Files	24+
Python Classes	18
Evolution Strategies	4 (Standard, Novelty Search, MAP-Elites, Coevolution)
Agent Types	3 (Black/Red/Blue) with full lifecycle loops
Memory Operations	5 (Encrypt, Compress, Deduplicate, Index, Prune)
Concurrent Tasks	5+ per orchestrator instance
Configuration Presets	4 (Default, Aggressive, Conservative, Research)
Lines of Code	~3,000+



✍️ Author

sergmudrea
