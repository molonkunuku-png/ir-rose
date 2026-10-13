#!/usr/bin/env python3
"""
analysis.py — pure, testable detection helpers for IreneRose.

Stdlib only. No subprocess, no input(), no printing: every function is a
pure function so `pytest tests/` can pin the detection behavior without
touching the network or the filesystem.
"""
import math
import re
from collections import Counter

IP_RE = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b"
)
HASH_RE = re.compile(r"\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b|\b[a-fA-F0-9]{64}\b")


def shannon_entropy(s: str) -> float:
    # Adapted pattern from CABTA entropy_analyzer.py — stdlib only
    if not s:
        return 0.0
    counts = Counter(s)
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def dga_score(domain: str) -> dict:
    # Simplified 4-heuristic version of CABTA dga_detector.py:
    # entropy + length + digit-ratio + consonant-ratio
    sld = domain.lower().strip().rstrip(".").split(".")[0]
    ent = shannon_entropy(sld)
    length = len(sld)
    digits = sum(ch.isdigit() for ch in sld) / max(1, length)
    vowels = set("aeiou")
    cons = sum(ch.isalpha() and ch not in vowels for ch in sld) / max(1, length)
    score = 0
    if ent > 3.8:
        score += 30
    elif ent > 3.2:
        score += 15
    if length > 18:
        score += 25
    elif length > 12:
        score += 10
    if digits > 0.3:
        score += 20
    if cons > 0.7 and length > 8:
        score += 15
    verdict = "LIKELY-DGA" if score >= 50 else "SUSPICIOUS" if score >= 30 else "LIKELY-LEGIT"
    return {"domain": domain, "sld": sld, "entropy": round(ent, 2),
            "len": length, "score": score, "verdict": verdict}


def is_private_ip(ip: str) -> bool:
    return (ip.startswith("10.") or ip.startswith("192.168.")
            or ip.startswith("127.") or ip.startswith("169.254."))


def extract_ips(text: str, skip_private: bool = False) -> list:
    ips = IP_RE.findall(text)
    if skip_private:
        ips = [ip for ip in ips if not is_private_ip(ip)]
    return ips


def extract_hashes(text: str) -> list:
    return HASH_RE.findall(text)
