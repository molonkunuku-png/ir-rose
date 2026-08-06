# IreneRose — Ultimate Blue Team Toolkit (Pink Edition)

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)

**IreneRose** is a pink-themed blue team toolkit with 32 modules covering scan & recon, defense, auth, SIEM, forensics, compliance, and utilities.

## Modules

| # | Module | Description |
|---|--------|-------------|
| 1 | Iris | Port scanner + service fingerprint |
| 2 | Nova | Nmap wrapper with pink reports |
| 3 | NucleiPink | Nuclei templates manager |
| 4 | Veil | OSINT passive recon |
| 5 | SniffRose | Live traffic sniffer |
| 6 | DNSRose | DNS exfil detector |
| 7 | ShieldRose | Lightweight NIDS |
| 8 | GateRose | Firewall rule auditor |
| 9 | YaraRose | YARA malware scanner |
| 10 | PatchRose | Patch checker |
| 11 | KernelRose | Kernel rootkit detector |
| 12 | C2Rose | C2 framework launcher |
| 13 | AuthRose | Auth log analyzer |
| 14 | VaultRose | Secret hasher / locker |
| 15 | AccessRose | File permission auditor |
| 16 | SSHRose | Remote SSH checker |
| 17 | LogRose | Log analyzer |
| 18 | AlertRose | Alert dashboard |
| 19 | SigmaRose | Sigma rule converter |
| 20 | VTLookupRose | VirusTotal hash lookup |
| 21 | ChainsawRose | EVTX forensics hunter |
| 22 | ForensicRose | Disk forensics helper |
| 23 | IRPlaybookRose | Incident response playbook |
| 24 | ComplianceRose | CIS checks |
| 25 | AssetRose | Asset inventory |
| 26 | ConfigRose | Config auditor |
| 27 | BackupRose | Backup verifier |
| 28 | ChecklistRose | Hygiene checklist |
| 29 | LynisRose | Lynis wrapper |
| 30 | SelfTest | Self-test & dependency check |
| 31 | SetupRose | Auto-install dependencies |
| 32 | ExportRose | Export alerts / reports |

## Requirements

- Python 3.8+
- Optional: nmap, tshark, tcpdump, whois, lynis, yara-python, chainsaw, nuclei, sliver

## Usage

```bash
python3 IreneRose.py
python3 IreneRose.py selftest
```

## License

MIT
