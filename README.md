# DDoS Simulation — Multi-Vector Attack & Defense Demo

A real-time demonstration of DDoS attacks and mitigation strategies in Python.

## Quick Start

### Prerequisites
```bash
pip install flask scapy
```

### Run the Demo (3 Terminals)

**Terminal 1 — Victim Server:**
```bash
python3 victim_server.py
```

**Terminal 2 — Mitigation Firewall:**
```bash
python3 mitigation.py
```
Then **press Enter** to activate defense when the attack starts.

**Terminal 3 — Attacker:**
```bash
python3 omni_attacker.py
```

### What You'll See

1. **Defense OFF:** Browser hangs trying to reach http://localhost:8080 (server stalled)
2. **Press Enter:** Firewall activates
3. **Defense ON:** Browser loads instantly (attack blocked)

## What's Happening

### Three Attack Vectors
- **Volumetric UDP Flood** (50 threads) — Bandwidth exhaustion
- **SYN Flood** (10 threads) — TCP handshake exhaustion  
- **Slowloris** (500 threads) — HTTP thread starvation

### Three Defense Layers
- Connection purge (evict malicious streams)
- Timeout detection (block incomplete requests)
- Header validation (verify complete HTTP)
- User-Agent check (block raw socket bots)

## Files

- `victim_server.py` — Single-threaded Flask server (intentionally vulnerable)
- `omni_attacker.py` — Multi-vector DDoS attacker
- `mitigation.py` — Reverse proxy firewall with toggleable defense

## How It Works

The firewall sits between attacker and victim:
- **Defense OFF:** Blindly forwards all traffic → server stalls
- **Defense ON:** Validates requests + blocks malicious ones → server responsive

## Key Insight

Real DDoS defense isn't about stopping attackers—it's about making sure **zero malicious packets reach the victim**. This simulation shows exactly how.

---

**Educational use only.** For Cairo University Computer Networks course.
