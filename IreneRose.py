#!/usr/bin/env python3
"""
IreneRose — Ultimate Blue Team Toolkit
Pink Edition

IMPORTANT: Authorized use only. This toolkit is intended for legitimate
defensive security testing on systems you own or have explicit written
permission to assess. Unauthorized use against systems you do not own or
control is illegal and unethical.
"""

import os
import sys
import json
import time
import re
import getpass
import subprocess
import shutil
import platform
import hashlib
from pathlib import Path
from datetime import datetime

try:
    from analysis import dga_score, extract_ips, extract_hashes
except ImportError:  # imported from another directory: look next to this file
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from analysis import dga_score, extract_ips, extract_hashes

# ── pink palette ─────────────────────────────────────────────────────────────
class P:
    BOLD   = "\033[1m"
    PINK   = "\033[95m"
    LPINK  = "\033[35m"
    ROSE   = "\033[91m"
    LROSE  = "\033[31m"
    WHITE  = "\033[97m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    GRAY   = "\033[90m"
    RESET  = "\033[0m"

C = P()

# ── large ascii logo ─────────────────────────────────────────────────────────
LOGO = rf"""{C.PINK}
  ██████  █████  ███    ██ ███████ ██   ██
 ██      ██   ██ ████   ██ ██      ██  ██
 ██      ███████ ██ ██  ██ █████   █████
 ██      ██   ██ ██  ██ ██ ██      ██  ██
  ██████ ██   ██ ██   ████ ███████ ██   ██
{C.LPINK}═══════════════════════════════════════════════════════════════
  I R E N E R O S E   —   U L T I M A T E   B L U E   T E A M
═══════════════════════════════════════════════════════════════{C.RESET}
"""

# ── categories ───────────────────────────────────────────────────────────────
CATEGORIES = [
    ("SCAN & RECON", [
        ("Iris", "Port scanner + service fingerprint"),
        ("Nova", "Nmap wrapper with pink reports"),
        ("NucleiPink", "Nuclei templates manager"),
        ("Veil", "OSINT passive recon"),
        ("SniffRose", "Live traffic sniffer"),
        ("DNSRose", "DNS exfil detector"),
    ]),
    ("DEFEND & ATTACK", [
        ("ShieldRose", "Lightweight NIDS"),
        ("GateRose", "Firewall rule auditor"),
        ("YaraRose", "YARA malware scanner"),
        ("PatchRose", "Patch checker"),
        ("KernelRose", "Kernel rootkit detector"),
        ("C2Rose", "C2 lab reference (authorized labs only)"),
    ]),
    ("AUTH & ACCESS", [
        ("AuthRose", "Auth log analyzer"),
        ("VaultRose", "Secret hasher / locker"),
        ("AccessRose", "File permission auditor"),
        ("SSHRose", "Remote SSH checker"),
    ]),
    ("SIEM & ALERTS", [
        ("LogRose", "Log analyzer"),
        ("AlertRose", "Alert dashboard"),
        ("SigmaRose", "Sigma rule converter"),
        ("VTLookupRose", "VirusTotal hash lookup"),
        ("ChainsawRose", "EVTX forensics hunter"),
    ]),
    ("FORENSIC & IR", [
        ("ForensicRose", "Disk forensics helper"),
        ("IRPlaybookRose", "Incident response playbook"),
    ]),
    ("COMPLIANCE & ASSET", [
        ("ComplianceRose", "CIS checks"),
        ("AssetRose", "Asset inventory"),
        ("ConfigRose", "Config auditor"),
        ("BackupRose", "Backup verifier"),
        ("ChecklistRose", "Hygiene checklist"),
        ("LynisRose", "Lynis wrapper"),
    ]),
    ("UTILITIES", [
        ("SelfTest", "Self-test & dependency check"),
        ("SetupRose", "Auto-install dependencies"),
        ("ExportRose", "Export alerts / reports"),
    ]),
]

MENU = []
MENU_INDEX = {}
idx = 1
for cat, items in CATEGORIES:
    for name, desc in items:
        MENU.append((str(idx), name, desc))
        MENU_INDEX[name] = str(idx)
        idx += 1

# ── helpers ──────────────────────────────────────────────────────────────────
def hr(ch="─"):
    return ch * 60

def banner(title, angry=False):
    print(f"\n{C.PINK}{LOGO}{C.RESET}")
    print(f"{C.PINK}{hr('═')}")
    print(f"  {C.BOLD}{C.WHITE}{title}{C.RESET}")
    print(f"{hr('═')}{C.RESET}\n")

def run(cmd, shell=False, timeout=120):
    try:
        proc = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.stdout.strip(), proc.stderr.strip(), proc.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 124
    except Exception as e:
        return "", str(e), 1

def which(bin_name):
    return shutil.which(bin_name)

def section(title):
    print(f"\n{C.PINK}{hr('─')}")
    print(f"  {C.BOLD}{C.WHITE}{title}{C.RESET}")
    print(f"{hr('─')}{C.RESET}")

# ── menu ─────────────────────────────────────────────────────────────────────
def show_menu():
    section("Modules")
    print(f"{C.PINK}{hr('═')}{C.RESET}")
    i = 0
    for cat, items in CATEGORIES:
        print(f"\n  {C.BOLD}{C.ROSE}══ {cat} ══{C.RESET}")
        for name, desc in items:
            print(f"    {C.CYAN}{MENU[i][0]:>2}.{C.RESET} {C.WHITE}{name:<20}{C.RESET} {desc}")
            i += 1
    print(f"\n    {C.GRAY} 0. Exit{C.RESET}")

# ── modules ──────────────────────────────────────────────────────────────────
def module_iris():
    banner("Iris — Port Scanner", angry=True)
    target = input(f"  {C.CYAN}Target:{C.RESET} ").strip()
    if not target:
        return
    nmap = which("nmap")
    if not nmap:
        print(f"  {C.YELLOW}nmap not found. Install: sudo pacman -S nmap{C.RESET}")
        return
    print(f"  {C.PINK}Scanning {target}...{C.RESET}")
    out, err, rc = run(["nmap", "-sV", "-T4", "--max-retries", "1", "--host-timeout", "30s", target], timeout=60)
    if rc == 0 and out:
        print(f"\n{out[:5000]}")
    else:
        print(f"  {C.YELLOW}rc={rc}{C.RESET}")
        if err:
            print(f"  {C.YELLOW}{err[:500]}{C.RESET}")

def module_nova():
    banner("Nova — Nmap Wrapper")
    target = input(f"  {C.CYAN}Target:{C.RESET} ").strip()
    if not target:
        return
    nmap = which("nmap")
    if not nmap:
        print(f"  {C.YELLOW}nmap not found.{C.RESET}")
        return
    print(f"  {C.PINK}Running nmap on {target}...{C.RESET}")
    out, err, rc = run(["nmap", "-p-", "--open", "-T4", target], timeout=120)
    if rc == 0 and out:
        print(f"\n{out[:5000]}")
    else:
        print(f"  {C.YELLOW}rc={rc}{C.RESET}")

def module_nucleipink():
    banner("NucleiPink — Vulnerability Scanner")
    target = input(f"  {C.CYAN}Target URL or host:{C.RESET} ").strip()
    if not target:
        return
    nuclei = which("nuclei")
    if not nuclei:
        print(f"  {C.YELLOW}nuclei not found. Install: go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest{C.RESET}")
        return
    print(f"  {C.PINK}Running nuclei on {target}...{C.RESET}")
    out, err, rc = run(["nuclei", "-u", target, "-severity", "high,critical", "-no-color"], timeout=120)
    if rc == 0 and out:
        print(f"\n{out[:5000]}")
    else:
        print(f"  {C.YELLOW}rc={rc}{C.RESET}")

def module_veil():
    banner("Veil — OSINT Passive Recon")
    target = input(f"  {C.CYAN}Domain or IP:{C.RESET} ").strip()
    if not target:
        return
    print(f"  {C.PINK}Gathering passive intel on {target}...{C.RESET}")
    if which("whois"):
        out, _, _ = run(["whois", target], timeout=15)
        if out:
            print(f"\n{C.GRAY}{out[:2000]}{C.RESET}")
    if which("dig"):
        out, _, _ = run(["dig", "+short", target], timeout=10)
        if out:
            print(f"\n{C.CYAN}DNS:{C.RESET} {out}")

def module_sniffrose():
    banner("SniffRose — Live Traffic Sniffer")
    iface = input(f"  {C.CYAN}Interface (blank for auto):{C.RESET} ").strip()
    if not iface:
        try:
            out = subprocess.check_output(["ip", "route", "get", "1.1.1.1"], text=True, timeout=5)
            tokens = out.split()
            if "dev" in tokens:
                iface = tokens[tokens.index("dev") + 1]
        except Exception:
            pass
    if not iface:
        print(f"  {C.YELLOW}No interface detected.{C.RESET}")
        return
    tshark = which("tshark")
    tcpdump = which("tcpdump")
    if tshark:
        print(f"  {C.PINK}Capturing 30 packets on {iface}...{C.RESET}")
        out, err, rc = run(["tshark", "-i", iface, "-c", "30", "-T", "fields", "-e", "ip.src", "-e", "ip.dst", "-e", "frame.len", "-E", "separator=|"], timeout=30)
        if rc == 0 and out:
            print(f"\n{out[:5000]}")
    elif tcpdump:
        print(f"  {C.PINK}Capturing 50 packets on {iface}...{C.RESET}")
        out, err, rc = run(["tcpdump", "-i", iface, "-c", "50", "-n", "-q"], timeout=30)
        if rc == 0 and out:
            print(f"\n{out[:5000]}")
    else:
        print(f"  {C.YELLOW}tshark/tcpdump not installed.{C.RESET}")

def module_dnsrose():
    banner("DNSRose — DNS Exfil Detector")
    print(f"  {C.PINK}DGA / exfil heuristic scorer (entropy+length+digit+consonant).{C.RESET}")
    print(f"  {C.GRAY}Ref: CABTA dga_detector.py (7 heuristics) simplified to stdlib-only 4.{C.RESET}")
    target = input(f"  {C.CYAN}Domain to score (blank for demo list):{C.RESET} ").strip()
    domains = [target] if target else ["google.com", "github.com", "x7f9k2qz8pl4m1x.com", "akd83ks82d9s7f23skd.com"]
    for d in domains:
        r = dga_score(d)
        col = C.RED if r["verdict"] == "LIKELY-DGA" else C.YELLOW if r["verdict"] == "SUSPICIOUS" else C.GREEN
        print(f"  {col}{r['verdict']:>13}{C.RESET} {r['domain']:<32} ent={r['entropy']} len={r['len']} score={r['score']}")
    print(f"\n  {C.YELLOW}Live tip: sudo tcpdump -i any port 53 -l | grep --line-buffered -E '.{{40,}}'{C.RESET}")

def module_shieldrose():
    banner("ShieldRose — Lightweight NIDS", angry=True)
    iface = input(f"  {C.CYAN}Interface (blank for all):{C.RESET} ").strip() or "any"
    print(f"  {C.PINK}Starting NIDS on {iface}...{C.RESET}")
    tshark = which("tshark")
    tcpdump = which("tcpdump")
    alerts = []
    if tshark:
        out, err, rc = run(["tshark", "-i", iface, "-c", "100", "-T", "fields", "-e", "ip.src", "-e", "tcp.flags", "-e", "frame.len", "-E", "separator=|"], timeout=30)
        if rc == 0 and out:
            for line in out.splitlines():
                parts = line.split("|")
                src = parts[0] if len(parts) > 0 else "?"
                flags = parts[1] if len(parts) > 1 else ""
                length = parts[2] if len(parts) > 2 else "0"
                if flags == "0x02":
                    alerts.append(("MEDIUM", src, "SYN scan"))
                elif flags == "0x12":
                    alerts.append(("LOW", src, "SYN-ACK"))
                elif flags == "0x14":
                    alerts.append(("HIGH", src, "RST scan"))
                else:
                    try:
                        if int((length or "0").strip() or 0) > 9000:
                            alerts.append(("MEDIUM", src, "Large packet"))
                    except ValueError:
                        pass
    if not alerts and tcpdump:
        out, err, rc = run(["tcpdump", "-i", iface, "-c", "50", "-n", "-q"], timeout=30)
        if rc == 0 and out:
            for line in out.splitlines():
                if "SYN" in line:
                    alerts.append(("MEDIUM", "tcpdump", "SYN packet"))
    if not alerts:
        print(f"  {C.GREEN}No suspicious traffic captured on {iface}.{C.RESET}")
    else:
        print(f"\n{C.PINK}{hr('─')}")
        print(f"  {C.BOLD}Alert summary{C.RESET}")
        for severity, ip, sig in alerts[:20]:
            col = C.RED if severity == "HIGH" else C.YELLOW if severity == "MEDIUM" else C.CYAN
            print(f"  {col}{severity}{C.RESET} {ip:<20} {sig}")

def module_gaterose():
    banner("GateRose — Firewall Rule Auditor")
    print(f"  {C.PINK}Checking firewall status...{C.RESET}")
    ufw = which("ufw")
    fw_cmd = which("firewall-cmd")
    ipt = which("iptables")
    if ufw:
        out, _, _ = run(["sudo", "ufw", "status"], timeout=10)
        print(f"\n{C.GRAY}{out[:3000]}{C.RESET}")
    elif fw_cmd:
        out, _, _ = run(["sudo", "firewall-cmd", "--list-all"], timeout=10)
        print(f"\n{C.GRAY}{out[:3000]}{C.RESET}")
    elif ipt:
        out, _, _ = run(["sudo", "iptables", "-L", "-n"], timeout=10)
        print(f"\n{C.GRAY}{out[:3000]}{C.RESET}")
    else:
        print(f"  {C.YELLOW}No firewall tool found (ufw/firewalld/iptables).{C.RESET}")

def module_yararose():
    banner("YaraRose — YARA Malware Scanner")
    target = input(f"  {C.CYAN}Path to file or directory:{C.RESET} ").strip()
    if not target:
        return
    yara_py = which("yara")
    if not yara_py:
        print(f"  {C.YELLOW}yara not found. Install: pip install yara-python{C.RESET}")
        return
    rule_dirs = [Path.home() / ".config" / "iru" / "rules", Path("/usr/share/yara/rules")]
    rule_files = []
    for d in rule_dirs:
        if d.is_file() and d.suffix in (".yar", ".yara", ".rule"):
            rule_files.append(str(d))
        elif d.is_dir():
            rule_files.extend([str(p) for p in d.glob("*.yar")])
            rule_files.extend([str(p) for p in d.glob("*.yara")])
    if not rule_files:
        print(f"  {C.YELLOW}No YARA rules found.{C.RESET}")
        print(f"  {C.GRAY}Checked: {', '.join(str(d) for d in rule_dirs)}{C.RESET}")
        return
    print(f"  {C.PINK}Scanning {target} with {rule_files[0]}...{C.RESET}")
    out, err, rc = run(["yara", "-r", rule_files[0], target], timeout=60)
    if rc == 0 and out:
        print(f"\n{out[:5000]}")
    else:
        print(f"  {C.YELLOW}No matches or scan failed.{C.RESET}")

def module_patchrose():
    banner("PatchRose — Patch Checker")
    print(f"  {C.PINK}Checking system updates...{C.RESET}")
    if which("apt"):
        out, _, rc = run(["sudo", "apt", "list", "--upgradable"], timeout=30)
        print(f"\n{C.GRAY}{out[:4000]}{C.RESET}")
    elif which("pacman"):
        out, _, rc = run(["sudo", "pacman", "-Qu"], timeout=30)
        print(f"\n{C.GRAY}{out[:4000]}{C.RESET}")
    else:
        print(f"  {C.YELLOW}No package manager detected.{C.RESET}")

def module_kernelrose():
    banner("KernelRose — Kernel Rootkit Detector")
    print(f"  {C.PINK}Checking kernel modules and syscall table...{C.RESET}")
    if which("lsmod"):
        out, _, _ = run(["lsmod"], timeout=10)
        print(f"\n{C.GRAY}{out[:3000]}{C.RESET}")
    else:
        print(f"  {C.YELLOW}lsmod not available.{C.RESET}")
    if which("ip"):
        out, _, _ = run(["ip", "link"], timeout=10)
        print(f"\n{C.GRAY}{out[:2000]}{C.RESET}")

def module_c2rose():
    banner("C2Rose — C2 Lab Reference")
    print(f"  {C.YELLOW}Scope: understand/detect C2 beacons against systems you own")
    print(f"  or are authorized to test — in an isolated lab. Not for use against")
    print(f"  anyone else's infrastructure.{C.RESET}")
    print(f"  1. Check Sliver")
    print(f"  2. Check Havoc")
    print(f"  3. Install Sliver")
    print(f"  4. Install Havoc (AUR)")
    ch = input(f"\n  {C.CYAN}Select>{C.RESET} ").strip()
    if ch == "1":
        path = which("sliver")
        print(f"  Sliver: {path or 'not found'}")
    elif ch == "2":
        paths = [which("havoc"), which("havoc-server"), which("havoc-client")]
        found = [p for p in paths if p]
        if found:
            print(f"  {C.GREEN}Havoc found:{C.RESET}")
            for p in found:
                print(f"    {p}")
        else:
            print(f"  {C.YELLOW}Havoc not found.{C.RESET}")
    elif ch == "3":
        print(f"  {C.YELLOW}Install Sliver from: https://github.com/bishopfox/sliver{C.RESET}")
    elif ch == "4":
        helper = which("yay") or which("paru")
        if helper:
            print(f"  {C.CYAN}{helper} -S --noconfirm havoc-c2-git{C.RESET}")
        else:
            print(f"  {C.YELLOW}Install yay/paru first, then: yay -S havoc-c2-git{C.RESET}")

def module_authrose():
    banner("AuthRose — Auth Log Analyzer")
    log = "/var/log/auth.log"
    if not Path(log).exists():
        log = "/var/log/secure"
    if not Path(log).exists():
        print(f"  {C.YELLOW}No auth log found at /var/log/auth.log or /var/log/secure{C.RESET}")
        return
    out, _, _ = run(["sudo", "tail", "-n", "200", log], timeout=10)
    if not out:
        print(f"  {C.YELLOW}Empty log or need sudo.{C.RESET}")
        return
    fails: dict[str, int] = {}
    accepts = 0
    for ln in out.splitlines():
        ll = ln.lower()
        if "failed" in ll or "invalid" in ll:
            for ip in extract_ips(ln):
                fails[ip] = fails.get(ip, 0) + 1
        if "accepted" in ll:
            accepts += 1
    print(f"  Accepted: {accepts}, failing IPs: {len(fails)}")
    for ip, c in sorted(fails.items(), key=lambda x: x[1], reverse=True)[:10]:
        flag = "BRUTE?" if c >= 5 else ""
        print(f"    {C.RED if c >= 5 else C.YELLOW}{c:>4}x{C.RESET} {ip} {flag}")

def module_vaultrose():
    banner("VaultRose — Secret Locker")
    name = input(f"  {C.CYAN}Secret name:{C.RESET} ").strip()
    try:
        val = getpass.getpass(f"  Secret value (hidden): ")
    except Exception:
        val = input(f"  {C.CYAN}Secret value:{C.RESET} ").strip()
    if name and val:
        enc = hashlib.sha256(val.encode()).hexdigest()[:16]
        print(f"  {C.GREEN}Hashed {name} (sha256[:16]: {enc}){C.RESET}")
        print(f"  {C.GRAY}Note: plaintext not stored — keep value in your vault.{C.RESET}")

def module_accessrose():
    banner("AccessRose — Permission Auditor")
    files = ["/etc/passwd", "/etc/shadow", "/etc/sudoers", "/root/.ssh/id_rsa"]
    for f in files:
        p = Path(f)
        if p.exists():
            try:
                perm = oct(os.stat(f).st_mode & 0o777)
                ok = perm in ("0o644", "0o600", "0o640", "0o400")
                col = C.GREEN if ok else C.RED
                print(f"  {col}{perm}{C.RESET} {f}")
            except PermissionError:
                print(f"  {C.YELLOW}[SKIP]{C.RESET} {f} — run as root")
        else:
            print(f"  {C.YELLOW}[MISS]{C.RESET} {f}")

def module_sshrose():
    banner("SSHRose — Remote SSH Checker")
    host = input(f"  {C.CYAN}Remote host:{C.RESET} ").strip()
    if not host:
        return
    if not which("ssh"):
        print(f"  {C.YELLOW}ssh not found. Install openssh.{C.RESET}")
        return
    out, err, rc = run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", host, "hostname"], timeout=15)
    if rc == 0:
        print(f"  {C.GREEN}Connected. Hostname: {out.strip()}{C.RESET}")
    else:
        print(f"  {C.YELLOW}SSH failed rc={rc}: {err[:120]}{C.RESET}")

def module_logrose():
    banner("LogRose — Log Analyzer")
    print(f"  {C.GRAY}Ref: CABTA ioc_extractor.py + btl1-field-notes 04_SIEM_Analysis common searches.{C.RESET}")
    path = input(f"  {C.CYAN}Log file path:{C.RESET} ").strip()
    if not path or not Path(path).exists():
        print(f"  {C.YELLOW}Log not found.{C.RESET}")
        return
    try:
        lines = Path(path).read_text(errors="ignore").splitlines()[-500:]
    except Exception as e:
        print(f"  {C.YELLOW}Read failed: {e}{C.RESET}")
        return
    ips: dict[str, int] = {}
    hashes: set[str] = set()
    fails = 0
    for ln in lines:
        ll = ln.lower()
        if "failed" in ll or "invalid" in ll or "denied" in ll or "error" in ll:
            fails += 1
        for ip in extract_ips(ln, skip_private=True):
            ips[ip] = ips.get(ip, 0) + 1
        for h in extract_hashes(ln):
            hashes.add(h)
    print(f"  Scanned {len(lines)} lines — fails/errors: {fails}, unique public IPs: {len(ips)}, hashes: {len(hashes)}")
    top = sorted(ips.items(), key=lambda x: x[1], reverse=True)[:10]
    for ip, c in top:
        print(f"    {C.YELLOW}{c:>4}x{C.RESET} {ip}")
    if hashes:
        print(f"  {C.CYAN}Hashes:{C.RESET} {', '.join(list(hashes)[:5])}")
    print(f"  {C.GRAY}SPL hint: index=* | stats count by src_ip | sort -count{C.RESET}")

def module_alertrose():
    banner("AlertRose — Alert Dashboard")
    exp = Path("export")
    files = sorted(exp.glob("*.json"))[-5:] if exp.exists() else []
    if not files:
        print(f"  {C.PINK}Recent alerts:{C.RESET}")
        print(f"  {C.GREEN}[OK]{C.RESET}   No critical alerts right now.")
        print(f"  {C.YELLOW}[INFO]{C.RESET} System scan completed. Run LogRose/AuthRose then ExportRose to populate.")
        return
    print(f"  {C.PINK}Last {len(files)} export(s):{C.RESET}")
    for f in files:
        try:
            data = json.loads(f.read_text())
            print(f"    {f.name}: {len(data) if isinstance(data, list) else 'obj'} entries")
        except Exception:
            print(f"    {f.name}: (unreadable)")

def module_sigmarose():
    banner("SigmaRose — Sigma Rule Converter")
    print(f"  {C.GRAY}Ref: CABTA rule_generator.py — KQL/SPL/Sigma/YARA from single IOC.{C.RESET}")
    ioc = input(f"  {C.CYAN}IOC (ip/domain/hash/url):{C.RESET} ").strip()
    if not ioc:
        print(f"  {C.YELLOW}Install sigma-cli for full convert: pip install sigma-cli{C.RESET}")
        print(f"  {C.GRAY}Usage: sigma convert -t splunk rule.yml{C.RESET}")
        return
    if re.match(r"^(?:\d+\.){3}\d+$", ioc):
        itype = "ipv4"
    elif re.match(r"^[a-fA-F0-9]{32}$|^[a-fA-F0-9]{40}$|^[a-fA-F0-9]{64}$", ioc):
        itype = "hash"
    elif ioc.startswith("http"):
        itype = "url"
    else:
        itype = "domain"
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    outdir = Path("export") / f"sigma_{ts}"
    outdir.mkdir(parents=True, exist_ok=True)
    kql = f"// KQL - Hunt {itype}: {ioc}\nDeviceNetworkEvents\n| where Timestamp > ago(30d)\n| where RemoteIP == \"{ioc}\" or RemoteUrl has \"{ioc}\"\n"
    spl = f"# SPL - Hunt {itype}: {ioc}\nindex=* earliest=-30d\n| search dest_ip=\"{ioc}\" OR url=\"*{ioc}*\" OR hash=\"{ioc}\"\n| stats count by host\n"
    sigma = f"title: Hunt {ioc}\nstatus: test\nlogsource:\n  category: network_connection\n  product: windows\nselection:\n  DestinationIp: '{ioc}'\n  Query: '*{ioc}*'\ncondition: selection\nlevel: medium\n"
    (outdir / "hunt.kql").write_text(kql)
    (outdir / "hunt.spl").write_text(spl)
    (outdir / "hunt.yml").write_text(sigma)
    print(f"  {C.GREEN}Wrote {outdir}/hunt.{{kql,spl,yml}}{C.RESET}")
    print(f"\n{C.GRAY}{sigma[:600]}{C.RESET}")

def module_vtlookuprose():
    banner("VTLookupRose — VirusTotal Lookup")
    h = input(f"  {C.CYAN}File hash (MD5/SHA1/SHA256):{C.RESET} ").strip()
    if not h:
        return
    import urllib.request
    api = os.environ.get("VT_API_KEY", "")
    print(f"  {C.GRAY}https://www.virustotal.com/gui/file/{h}{C.RESET}")
    if not api:
        print(f"  {C.YELLOW}Set VT_API_KEY for live lookup — showing link only.{C.RESET}")
        return
    try:
        req = urllib.request.Request(f"https://www.virustotal.com/api/v3/files/{h}", headers={"x-apikey": api})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            print(f"  {C.PINK}VT stats:{C.RESET} {stats}")
    except Exception as e:
        print(f"  {C.YELLOW}VT lookup failed: {e}{C.RESET}")

def module_chainsawrose():
    banner("ChainsawRose — EVTX Forensics")
    path = input(f"  {C.CYAN}EVTX file or directory:{C.RESET} ").strip()
    if not path:
        return
    chainsaw = which("chainsaw")
    if not chainsaw:
        print(f"  {C.YELLOW}chainsaw not found.{C.RESET}")
        print(f"  {C.CYAN}cargo install chainsaw{C.RESET}")
        return
    out, err, rc = run(["chainsaw", "hunt", path, "--no-color", "--quiet"], timeout=120)
    if rc == 0 and out:
        print(f"\n{out[:5000]}")
    else:
        print(f"  {C.YELLOW}rc={rc}{C.RESET}")

def module_forensicrose():
    banner("ForensicRose — Disk Forensics Helper")
    print(f"  {C.GRAY}Ref: DFIR-Toolkit (mmls, timeline, logs) + btl1 03_Digital_Forensics (Volatility).{C.RESET}")
    img = input(f"  {C.CYAN}Disk image path (blank for live-host triage):{C.RESET} ").strip()
    if img:
        if not which("mmls"):
            print(f"  {C.YELLOW}sleuthkit not installed. Install: sudo pacman -S sleuthkit / sudo apt install sleuthkit{C.RESET}")
        else:
            out, _, _ = run(["mmls", img], timeout=15)
            print(f"\n{C.GRAY}{out[:3000]}{C.RESET}")
        print(f"  {C.GRAY}Volatility hints: vol -f mem.raw windows.pslist windows.malfind windows.netscan{C.RESET}")
        return
    print(f"  {C.PINK}Live triage: timeline + bash_history + /var/log list{C.RESET}")
    for p in [Path.home() / ".bash_history", Path("/var/log/auth.log"), Path("/var/log/syslog")]:
        print(f"  {'present' if p.exists() else 'missing':>7} {p}")

def module_irplaybookrose():
    banner("IRPlaybookRose — Incident Response Playbook")
    print(f"  {C.GRAY}Ref: btl1-field-notes 06_Incident_Response (lifecycle + live response) + DFIR-Toolkit artifact list.{C.RESET}")
    print(f"  1. Preparation")
    print(f"  2. Detection & Analysis (triage)")
    print(f"  3. Containment")
    print(f"  4. Eradication")
    print(f"  5. Recovery")
    print(f"  6. Lessons Learned")
    print(f"  7. Linux live-response bundle (DFIR-style)")
    ch = input(f"\n  {C.CYAN}Select>{C.RESET} ").strip()
    plays = {
        "1": ["Scope + roles", "Preserve logs", "Comms channel", "Legal hold if needed"],
        "2": ["Identify IOCs", "Check auth.log / syslog", "List conns: ss -tunap", "List procs: ps aux --forest"],
        "3": ["Isolate host (net, not power)", "Block IPs at fw", "Snapshot / memory dump first", "Preserve evidence"],
        "4": ["Kill malicious procs", "Remove persistence (cron, systemd, autoruns)", "Patch vuln", "Rotate creds"],
        "5": ["Restore from clean backup", "Verify hashes", "Monitor 7d for re-infection", "Close case notes"],
        "6": ["Timeline", "Root cause", "Detection gap", "Update Sigma/YARA + checklist"],
    }
    if ch in plays:
        for step in plays[ch]:
            print(f"    - {step}")
    elif ch == "7":
        host = platform.node() or "host"
        outdir = Path(f"Collection_{host}")
        (outdir / "logs").mkdir(parents=True, exist_ok=True)
        for cmd, fname in [(["uptime"], "sysinfo.txt"), (["uname", "-a"], "sysinfo.txt"), (["df", "-h"], "sysinfo.txt"), (["ps", "aux", "--forest"], "process.txt"), (["ss", "-tunap"], "netstat.txt"), (["last", "-n", "20"], "users.txt")]:
            o, _, _ = run(cmd, timeout=10)
            if o:
                with open(outdir / "logs" / fname, "a") as f:
                    f.write(f"\n### {' '.join(cmd)}\n{o[:4000]}\n")
        print(f"  {C.GREEN}Wrote DFIR-lite bundle to {outdir}/logs/{C.RESET}")

def module_compliancerose():
    banner("ComplianceRose — CIS Checks")
    print(f"  {C.PINK}Running basic CIS checks...{C.RESET}")
    checks = [
        ("SSH PermitRootLogin", "/etc/ssh/sshd_config", "permitrootlogin"),
        ("PasswordAuthentication", "/etc/ssh/sshd_config", "passwordauthentication"),
    ]
    for name, path, keyword in checks:
        p = Path(path)
        if p.exists():
            txt = p.read_text(errors="ignore").lower()
            status = "found" if keyword in txt else "not found"
            col = C.GREEN if status == "found" else C.YELLOW
            print(f"  {col}{name}: {status}{C.RESET}")
        else:
            print(f"  {C.YELLOW}{name}: file not found{C.RESET}")

def module_assetrose():
    banner("AssetRose — Asset Inventory")
    print(f"  {C.PINK}Collecting host info...{C.RESET}")
    print(f"  Hostname: {C.WHITE}{platform.node()}{C.RESET}")
    print(f"  OS: {C.WHITE}{platform.system()} {platform.release()}{C.RESET}")
    print(f"  Arch: {C.WHITE}{platform.machine()}{C.RESET}")
    print(f"  Python: {C.WHITE}{platform.python_version()}{C.RESET}")
    if which("ip"):
        out, _, _ = run(["ip", "-brief", "addr"], timeout=10)
        print(f"\n{C.GRAY}{out[:3000]}{C.RESET}")

def module_configrose():
    banner("ConfigRose — Config Auditor")
    files = ["/etc/ssh/sshd_config", "/etc/sysctl.conf", "/etc/hosts.allow", "/etc/hosts.deny"]
    for f in files:
        p = Path(f)
        status = f"{C.GREEN}present{C.RESET}" if p.exists() else f"{C.YELLOW}missing{C.RESET}"
        print(f"  {status} {f}")

def module_backuprose():
    banner("BackupRose — Backup Verifier")
    path = input(f"  {C.CYAN}Backup file path:{C.RESET} ").strip()
    if not path or not Path(path).exists():
        print(f"  {C.YELLOW}File not found.{C.RESET}")
        return
    h = hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]
    print(f"  {C.GREEN}Verified {path} — SHA256: {h}{C.RESET}")

def module_checklistrose():
    banner("ChecklistRose — Hygiene Checklist")
    items = [
        ("Firewall enabled", which("ufw") or which("firewall-cmd") or which("iptables")),
        ("SSH key-based auth", Path("/root/.ssh/authorized_keys").exists() or Path.home().joinpath(".ssh/authorized_keys").exists()),
        ("Automatic updates", False),
        ("Fail2ban installed", which("fail2ban-client")),
        ("Antivirus installed", which("clamscan")),
    ]
    for name, ok in items:
        col = C.GREEN if ok else C.YELLOW
        status = "PASS" if ok else "WARN"
        print(f"  {col}{status}{C.RESET} {name}")

def module_lynisrose():
    banner("LynisRose — Lynis Wrapper")
    lynis = which("lynis")
    if not lynis:
        print(f"  {C.YELLOW}lynis not found. Install: sudo pacman -S lynis{C.RESET}")
        return
    print(f"  {C.PINK}Running lynis audit (quick)...{C.RESET}")
    out, _, rc = run(["sudo", "lynis", "audit", "system", "--quick"], timeout=120)
    if out:
        print(f"\n{C.GRAY}{out[:5000]}{C.RESET}")

def module_selftestrose():
    banner("SelfTest — Dependency Check")
    deps = ["nmap", "tshark", "tcpdump", "whois", "dig", "lynis", "yara", "chainsaw"]
    for dep in deps:
        ok = which(dep) is not None
        col = C.GREEN if ok else C.YELLOW
        status = "OK" if ok else "MISSING"
        print(f"  {col}{dep}: {status}{C.RESET}")
    print(f"\n  {C.GREEN}IreneRose ready.{C.RESET}")

def module_setuprose():
    banner("SetupRose — Auto Install Dependencies")
    print(f"  {C.PINK}Detecting package manager...{C.RESET}")
    helper = None
    if which("yay"):
        helper = "yay"
    elif which("paru"):
        helper = "paru"
    elif which("pacman"):
        helper = "sudo pacman"
    elif which("apt"):
        helper = "sudo apt"
    if helper:
        pkgs = ["nmap", "tshark", "tcpdump", "whois", "dnsutils", "lynis", "yara-python"]
        if helper in ("yay", "paru"):
            cmd = [helper, "-S", "--noconfirm"] + pkgs
        else:
            cmd = [*helper.split(), "install", "-y"] + pkgs
        print(f"  {C.CYAN}{' '.join(cmd)}{C.RESET}")
        confirm = input(f"  {C.CYAN}Proceed? [y/N]:{C.RESET} ").strip().lower()
        if confirm == "y":
            out, err, rc = run(cmd, timeout=300)
            if rc == 0:
                print(f"  {C.GREEN}Dependencies installed.{C.RESET}")
            else:
                print(f"  {C.YELLOW}Install failed rc={rc}{C.RESET}")
                if err:
                    print(f"  {C.YELLOW}{err[:400]}{C.RESET}")
    else:
        print(f"  {C.YELLOW}No supported package manager found.{C.RESET}")

def module_exportrose():
    banner("ExportRose — Report Exporter")
    print(f"  1. Export sample CSV")
    print(f"  2. Export sample JSON")
    ch = input(f"\n  {C.CYAN}Select>{C.RESET} ").strip()
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    if ch == "1":
        out = Path("export") / f"irerose_alerts_{ts}.csv"
        out.parent.mkdir(exist_ok=True)
        out.write_text("timestamp,severity,module,details\n")
        print(f"  {C.GREEN}Saved {out}{C.RESET}")
    elif ch == "2":
        out = Path("export") / f"irerose_alerts_{ts}.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text("[]")
        print(f"  {C.GREEN}Saved {out}{C.RESET}")

# ── module map ───────────────────────────────────────────────────────────────
MODULES = {
    "1": ("Iris", module_iris),
    "2": ("Nova", module_nova),
    "3": ("NucleiPink", module_nucleipink),
    "4": ("Veil", module_veil),
    "5": ("SniffRose", module_sniffrose),
    "6": ("DNSRose", module_dnsrose),
    "7": ("ShieldRose", module_shieldrose),
    "8": ("GateRose", module_gaterose),
    "9": ("YaraRose", module_yararose),
    "10": ("PatchRose", module_patchrose),
    "11": ("KernelRose", module_kernelrose),
    "12": ("C2Rose", module_c2rose),
    "13": ("AuthRose", module_authrose),
    "14": ("VaultRose", module_vaultrose),
    "15": ("AccessRose", module_accessrose),
    "16": ("SSHRose", module_sshrose),
    "17": ("LogRose", module_logrose),
    "18": ("AlertRose", module_alertrose),
    "19": ("SigmaRose", module_sigmarose),
    "20": ("VTLookupRose", module_vtlookuprose),
    "21": ("ChainsawRose", module_chainsawrose),
    "22": ("ForensicRose", module_forensicrose),
    "23": ("IRPlaybookRose", module_irplaybookrose),
    "24": ("ComplianceRose", module_compliancerose),
    "25": ("AssetRose", module_assetrose),
    "26": ("ConfigRose", module_configrose),
    "27": ("BackupRose", module_backuprose),
    "28": ("ChecklistRose", module_checklistrose),
    "29": ("LynisRose", module_lynisrose),
    "30": ("SelfTest", module_selftestrose),
    "31": ("SetupRose", module_setuprose),
    "32": ("ExportRose", module_exportrose),
}

# ── main ─────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        module_selftestrose()
        return
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print(LOGO)
        show_menu()
        ch = input(f"\n  {C.CYAN}Select module>{C.RESET} ").strip()
        if ch == "0":
            print(f"\n  {C.PINK}Bye! Stay safe, stay pink.{C.RESET}\n")
            break
        mod = MODULES.get(ch)
        if mod:
            name, func = mod
            func()
            input(f"\n  {C.GRAY}Press Enter to continue...{C.RESET}")
        else:
            print(f"  {C.YELLOW}Invalid selection.{C.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
