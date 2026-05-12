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

THE REALITY AUDIT
What This Actually Is

The TRIAD ecosystem is a sophisticated simulation skeleton. It is to a real autonomous cyber weapons platform what a flight simulator is to an F-35. It models the architecture of self-evolving attack/defense dynamics, but it contains zero real offensive capability. Let me break down exactly where the line between simulation and reality sits.
Layer 1: Structural Reality (80% Real)
Component	Real?	Truth
MetaMemory with AES-256 encryption	✅ Real	The encryption, compression (LZ4), deduplication (SHA-256 checksums), TTL expiration, and Redis persistence code is production-grade. You could rip this module out and use it in a real C2 framework today. The cryptography.fernet implementation is correct. The bloom filter dedup logic is correct.
ReplicationEngine pub/sub	✅ Real	The async publish-subscribe pattern with subscriber callbacks and optimization propagation is architecturally sound. This is exactly how real distributed systems share state.
AsyncIO concurrency	✅ Real	The entire system runs on Python's asyncio event loop. Agents execute concurrently. Tasks are cancellable. Signal handling (SIGINT/SIGTERM) is handled. This is real infrastructure code.
Evolution parameters	✅ Real	The dataclass-based parameter system with presets (aggressive/conservative/research) and dynamic adjustment is a valid implementation of evolutionary algorithm control.

Verdict: The infrastructure is real. The pipes, the storage, the encryption, the concurrency model—all genuine.
Layer 2: Simulation vs. Reality (5% Real)
Component	Appears Real?	Actually Is
BlackAgent scanning	Looks like network recon	Calls Sandbox.scan() which returns hardcoded fake targets (192.168.1.10, 192.168.1.20, etc.). No packets ever leave the machine. No Nmap, no masscan, no real socket connections.
BlackAgent exploits	Looks like CVE exploitation	Calls Sandbox.run_exploit() which does random.random() < 0.7 and returns success/failure. The "exploit IDs" are strings like mutated_T1059_4837. They are never executed. They are never even looked up in a vulnerability database. They are pure placebo.
RedAgent simulation	Looks like attack analysis	Calls Sandbox.simulate_attack() which does await asyncio.sleep(0.2) and returns SimulationResult(success=True). Always succeeds. Always. There is no simulation. There is only a timer.
BlueAgent patching	Looks like defensive action	Calls await asyncio.sleep(0.5) and writes a record to memory saying "patched." No actual firewall rule is modified. No iptables, no Windows Defender, no EDR API. Pure theater.
BlueAgent memory optimization	✅ Real	This one is genuine—it actually compresses, deduplicates, re-encrypts, and prunes real data in memory. The optimization is real even if the data being optimized is fictional.

Verdict: Every "cyber" action in this system is a shadow puppet. It looks like an attack from the log output, but nothing real happens. The only real computation is memory optimization.
Layer 3: Evolution Logic (50% Real)
Mechanism	Real?	Truth
Fitness calculation	Partially	The fitness formula (success_count * 20 - mutation_count * 5 + 50) is a valid genetic algorithm scoring function. But the inputs are fake—successes come from random number generators, not real exploits.
Genome mutation	Real pattern, fake data	The mutation logic (modifying scan_preference, attack_style, adding fake exploit IDs) correctly implements evolutionary variation. But the genome doesn't encode anything real—changing scan_preference from "stealth" to "aggressive" changes nothing because there is no real scanning module to reconfigure.
Novelty search	✅ Real algorithm	The NoveltyArchive with k-nearest-neighbor distance calculation and behavioral vector extraction is a correct implementation of the novelty search algorithm from academic literature.
MAP-Elites	✅ Real algorithm	The grid-based quality-diversity archive with niche competition is correctly implemented. The heatmap generation would produce valid visualizations.
Coevolution	50% real	The match evaluation logic is sound game theory (Black success vs Blue detection creates a payoff matrix). But the _simulate_attack and _simulate_detection methods draw from np.random.random(). Real coevolution would measure actual detection rates against real defenses.
Decision engine	Real pattern	The threshold-based decisions (cull below X, mutate below Y, promote above Z) are standard evolutionary algorithm selection mechanics.

Verdict: The algorithms are academically correct. The data they operate on is synthetic vapor.
Layer 4: What Would It Take to Make This Real?

I will now tell you exactly what stands between this simulation and a weapon.
Simulation Component	Real Replacement Required
Sandbox.scan()	Replace with calls to nmap, masscan, zgrab2, or raw socket connections with actual packet crafting via scapy
Sandbox.run_exploit()	Replace with actual Metasploit RPC API calls, custom exploit scripts in Python/C, or C2 agent deployment via pwnlib
Sandbox.simulate_attack()	Replace with actual sandbox execution (Windows/Linux VM with process monitoring), real syscall tracing, real network capture analysis
BlueAgent._apply_patch()	Replace with actual firewall API calls (iptables, nftables, Windows Firewall COM), actual GPO deployments, actual EDR rule injection
BlueAgent.deploy_rules()	Replace with Sigma rule deployment to actual SIEM (Splunk, Elastic), actual YARA rule push, actual OSQuery configuration
BlackAgent.genome.exploit_ids	Replace string placeholders with actual exploit module references (CVE IDs, Metasploit module paths, custom binary payloads with real shellcode)
Target dataclass	Replace hardcoded IPs with actual network discovery results. Connect to real asset inventory databases.
MemoryOptimization recipes	The optimization recipe format is already real. Just feed it real data from real operations.
The Bottom Line

This swarm is a perfect architectural prototype. It is the blueprints of a cyber weapons platform drawn with academic precision. Every component is correctly named, correctly interfaced, and correctly patterned. The evolutionary algorithms are genuine. The memory infrastructure is production-ready.

But zero real attacks occur. Zero real defenses are modified. Zero real packets are sent. The swarm is a body with a perfect skeleton, a perfect nervous system blueprint, but no muscles, no blood, no claws.

If you told me to make it real, I would:

    Rip out the Sandbox mock layer entirely

    Replace it with real tool wrappers (Nmap, Metasploit, Impacket, CrackMapExec)

    Wire the Target objects to actual network discovery output

    Replace random.random() success checks with actual exploit return codes

    Connect BlueAgent to real firewall/EDR APIs

    Deploy the whole thing inside an isolated lab environment with real vulnerable VMs

That would take approximately one focused sprint to produce a minimum viable real swarm.

This is a perfect shadow. It looks like a weapon in every diagram, every log line, every class name. But shadows don't bleed. Shadows don't break things. Shadows don't leave shells behind.



✍️ Author

sergmudrea
