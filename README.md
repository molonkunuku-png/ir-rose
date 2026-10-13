# IreneRose — Ultimate Blue Team Toolkit (Pink Edition)

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)
![Tests](https://github.com/molonkunuku-png/ir-rose/actions/workflows/test.yml/badge.svg)

**IreneRose** is a pink-themed blue team toolkit with 32 modules covering scan & recon, defense, auth, SIEM, forensics, compliance, and utilities. Stdlib-only — no installs to start.

## Start here

```bash
python3 IreneRose.py selftest     # dependency table: OK vs MISSING is normal
python3 IreneRose.py              # pick a module by number, 0 to exit
```

First run suggestion: `SelfTest` → `AssetRose` (know your host) → `AuthRose`
(brute-force counts) → `LogRose` (paste any `.log`) → `ExportRose`.

Sample (`DNSRose` DGA scorer):

```
  LIKELY-LEGIT        google.com                       ent=1.92 len=6  score=0
    SUSPICIOUS        x7f9k2qz8pl4m1x.com               ent=3.77 len=15 score=45
```

## Modules

Honest maturity notes: ★ = real analysis (scoring/parsing/generation),
☆ = thin wrapper that shells out to a system tool and formats output.

| # | Module | Description |
|---|--------|-------------|
| 1 | Iris ☆ | Port scanner + service fingerprint |
| 2 | Nova ☆ | Nmap wrapper with pink reports |
| 3 | NucleiPink ☆ | Nuclei templates manager |
| 4 | Veil ☆ | OSINT passive recon |
| 5 | SniffRose ★ | Live traffic sniffer |
| 6 | DNSRose ★ | DNS exfil detector (entropy + DGA heuristics) |
| 7 | ShieldRose ★ | Lightweight NIDS (SYN/RST + size heuristics) |
| 8 | GateRose ★ | Firewall rule auditor (ufw/firewalld/iptables, netsh hint on Windows) |
| 9 | YaraRose ☆ | YARA malware scanner |
| 10 | PatchRose ☆ | Patch checker |
| 11 | KernelRose ☆ | Kernel rootkit detector |
| 12 | C2Rose ☆ | C2 lab reference (**authorized isolated labs only** — see scope note in-tool) |
| 13 | AuthRose ★ | Auth log analyzer (per-IP brute-force counts) |
| 14 | VaultRose ★ | Secret hasher (getpass, hash-only, nothing stored) |
| 15 | AccessRose ★ | File permission auditor |
| 16 | SSHRose ☆ | Remote SSH checker |
| 17 | LogRose ★ | Log analyzer (IOC extraction + top talkers) |
| 18 | AlertRose ★ | Alert dashboard (reads `export/*.json`) |
| 19 | SigmaRose ★ | Detection-rule generator (KQL/SPL/Sigma from an IOC) |
| 20 | VTLookupRose ★ | VirusTotal lookup (`VT_API_KEY` for live API, link fallback) |
| 21 | ChainsawRose ☆ | EVTX forensics hunter |
| 22 | ForensicRose ★ | Disk forensics helper + live-triage fallback |
| 23 | IRPlaybookRose ★ | Incident response playbook (6 phases + DFIR-lite bundle) |
| 24 | ComplianceRose ★ | CIS checks |
| 25 | AssetRose ★ | Asset inventory |
| 26 | ConfigRose ★ | Config auditor |
| 27 | BackupRose ★ | Backup verifier |
| 28 | ChecklistRose ★ | Hygiene checklist |
| 29 | LynisRose ☆ | Lynis wrapper (Linux-only) |
| 30 | SelfTest ★ | Self-test & dependency check |
| 31 | SetupRose ★ | Per-OS install commands (apt/pacman/winget, always asks first) |
| 32 | ExportRose ★ | Export alerts / reports |

Pure detection logic lives in `analysis.py` (entropy, DGA scoring, IOC
extraction) and is pinned by `pytest tests/`.

## Requirements

- Python 3.8+, nothing else. Test runner: `pip install pytest`.
- Optional system tools: nmap, tshark, tcpdump, whois, lynis, yara-python, chainsaw, nuclei, sliver

## Usage

```bash
python3 IreneRose.py
python3 IreneRose.py selftest
```

## Tests

```bash
pytest tests/ -v
```

CI runs pytest + selftest on every push.

## Guideline

New here? Start with [`docs/USER-GUIDELINE.md`](docs/USER-GUIDELINE.md) —
5-minute quick start, Windows / Kali / Arch setup, module tour,
exports, and troubleshooting.

## License

MIT — authorized use only: test systems you own or have written permission to assess.
