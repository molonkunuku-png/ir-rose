# IreneRose — User Guideline

**IreneRose — Ultimate Blue Team Toolkit (Pink Edition)**
Authorized use only. Use on systems you own or have explicit written permission to assess.

## 1. What this is

Single-file Python CLI (`IreneRose.py`, 32 modules) for defensive checks:
scan & recon, firewall/NIDS, auth/log review, SIEM helpers, forensics triage,
compliance, and report export. Stdlib-only — no `pip install` required to start.

## 2. Quick start (5 minutes)

```bash
git clone https://github.com/molonkunuku-png/ir-rose.git
cd ir-rose
python3 IreneRose.py selftest
python3 IreneRose.py
```

`selftest` prints OK/MISSING per tool. MISSING is fine — that module will
print what to install when you open it.

Menu: type a number, `0` to exit. Every module ends with
`Press Enter to continue...`.

## 3. Per-OS setup

### Kali / Debian / Ubuntu (full support)

```bash
sudo apt update && sudo apt install -y nmap tshark tcpdump whois dnsutils lynis yara nuclei
python3 IreneRose.py selftest
```

Use `sudo` for SniffRose / ShieldRose / GateRose / AuthRose.

### Arch (full support)

```bash
sudo pacman -S nmap tshark tcpdump whois dnsutils lynis yara-python
# optional AUR: yay -S nuclei chainsaw
python3 IreneRose.py selftest
```

### Windows (partial — works, some modules degrade gracefully)

1. Install Python 3.10+ (tick “Add to PATH”).
2. Install Npcap (required for Nmap/tshark), then:
```powershell
winget install -e --id Nmap.Nmap
winget install -e --id Wireshark.Wireshark
```
3. Run as Administrator for network/firewall modules.
```powershell
python IreneRose.py selftest
```

Expected on Windows: `tcpdump/lsmod/lynis/ufw` show MISSING.
That is normal — use the printed hint (e.g. `netsh advfirewall show
allprofiles` instead of GateRose Linux path, EVTX + chainsaw instead of
`/var/log/auth.log`).

## 4. Module guide (what to try first)

| Group | Start with | What it does |
|---|---|---|
| SCAN & RECON | Iris, Veil | Iris = `nmap -sV` on a target you own; Veil = `whois` + `dig` passive info |
| DEFEND | GateRose, PatchRose | Firewall status; pending OS updates |
| AUTH & ACCESS | AuthRose, AccessRose | Brute-force counts per IP; file-perm check |
| SIEM & ALERTS | LogRose, SigmaRose | Paste a log path → top IPs + IOCs; type an IOC → KQL/SPL/Sigma files in `export/` |
| FORENSIC & IR | IRPlaybookRose (7), ForensicRose | 6-phase checklist + DFIR-lite bundle to `Collection_<host>/logs/` |
| COMPLIANCE | ChecklistRose, AssetRose | Hygiene PASS/WARN; host inventory |
| UTILITIES | SelfTest, SetupRose, ExportRose | Dependency table; per-OS install commands; CSV/JSON export |

Good first run: `SelfTest` → `Iris` (your own host) → `AuthRose` →
`LogRose` (any `.log`) → `ExportRose`.

## 5. Exports and artifacts

- `export/irerose_alerts_<ts>.csv/json` from ExportRose
- `export/sigma_<ts>/hunt.{kql,spl,yml}` from SigmaRose
- `Collection_<host>/logs/` from IRPlaybookRose option 7

Attach these when asking for help.

## 6. Troubleshooting

- `nmap not found` → install per section 3, re-run `selftest`.
- `Empty log or need sudo` (AuthRose) → `sudo python3 IreneRose.py` on Linux/Kali.
- `tshark/tcpdump not installed` → install Wireshark/Npcap; on Windows use tshark path.
- `No YARA rules found` → put `.yar` files in `~/.config/iru/rules/` or `/usr/share/yara/rules/`.
- `VT_API_KEY` not set → VTLookupRose shows link only. Set it for live lookup:
  `export VT_API_KEY='...'`.
- Menu numbers look wrong → update to latest `main` (fixed 30→32 mismatch in Oct 2026).

## 7. Rules

- Only scan/analyze hosts, domains, logs you own or are authorized to test.
- Never paste tokens/PATs into chat, issues, or exports. If exposed, revoke on GitHub immediately.
- `C2Rose` is a launcher reference only — do not use against anyone else.

## 8. Getting help

Open an issue with: OS (`Windows 11` / `Kali 2026.x` / `Arch`), `python3 --version`,
`selftest` output, module name + exact error, and (if relevant) the `export/` file.
