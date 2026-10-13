import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis import (shannon_entropy, dga_score, extract_ips,
                      extract_hashes, is_private_ip)
import IreneRose


def test_entropy_orders_string_complexity():
    assert shannon_entropy("") == 0.0
    assert shannon_entropy("aaaa") < shannon_entropy("x7f9k2qz8")
    assert 0.0 <= shannon_entropy("google") <= 8.0


def test_dga_separates_legit_from_random():
    legit = dga_score("google.com")
    bad = dga_score("x7f9k2qz8pl4m1x.com")
    assert legit["verdict"] == "LIKELY-LEGIT" and legit["score"] < 30
    assert bad["score"] >= 30 and bad["verdict"] in ("SUSPICIOUS", "LIKELY-DGA")


def test_extract_ips_and_private_filter():
    text = "login from 203.0.113.7 and 10.0.0.5 hash d41d8cd98f00b204e9800998ecf8427e"
    assert "203.0.113.7" in extract_ips(text)
    assert "10.0.0.5" in extract_ips(text)
    assert "10.0.0.5" not in extract_ips(text, skip_private=True)
    assert is_private_ip("192.168.1.1") and not is_private_ip("203.0.113.7")


def test_extract_hashes_by_length():
    text = "d41d8cd98f00b204e9800998ecf8427e and notahash"
    found = extract_hashes(text)
    assert "d41d8cd98f00b204e9800998ecf8427e" in found
    assert "notahash" not in found


def test_menu_and_modules_stay_aligned():
    assert len(IreneRose.MENU) == 32 and len(IreneRose.MODULES) == 32
    assert ([n for _, n, _ in IreneRose.MENU]
            == [IreneRose.MODULES[str(i + 1)][0] for i in range(32)])
