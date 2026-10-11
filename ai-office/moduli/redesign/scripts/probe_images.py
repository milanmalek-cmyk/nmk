#!/usr/bin/env python3
"""Popis vseh slik iz pages.json z dimenzijami – brez prenosa celih datotek (HTTP Range).

Uporaba:
  python3 -I probe_images.py 01_analiza/pages.json 01_analiza/slike.tsv [--zamik 0.1] [--prejsnji STAR.tsv]

Stolpci: url, sirina, visina, format, bajti, spremenjeno, st_strani, izvor, alt, primer_strani
Slike, ki vrnejo napako (npr. napačno razrešena relativna pot), se ne zapišejo.
Z --prejsnji se že izmerjene slike (isti URL ne glede na www.) ne merijo znova.
"""
import argparse
import json
import os
import struct
import sys
import time
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skupno import odpri  # noqa: E402


def dimenzije(b):
    """(širina, višina, format) iz prvih bajtov datoteke."""
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return (*struct.unpack(">II", b[16:24]), "png")
    if b[:6] in (b"GIF87a", b"GIF89a"):
        return (*struct.unpack("<HH", b[6:10]), "gif")
    if b[:2] == b"\xff\xd8":
        i = 2
        while i < len(b) - 9:
            if b[i] != 0xFF:
                i += 1
                continue
            m = b[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", b[i + 5:i + 9])
                return w, h, "jpg"
            if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
                i += 2
                continue
            i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
        return None, None, "jpg"
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        if b[12:16] == b"VP8X":
            return (int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1, "webp")
        if b[12:16] == b"VP8 ":
            w, h = struct.unpack("<HH", b[26:30])
            return w & 0x3FFF, h & 0x3FFF, "webp"
        return None, None, "webp"
    if b.lstrip()[:5] in (b"<?xml", b"<svg ") or b"<svg" in b[:500]:
        return None, None, "svg"
    if b[:4] == b"\x00\x00\x01\x00":
        return None, None, "ico"
    return None, None, "?"


def brez_www(url):
    return url.replace("://www.", "://", 1)


def preberi_glavo(url, nacin):
    with odpri(url, nacin, bajti=131072) as r:
        b = r.read(131072)
        cr = r.headers.get("Content-Range", "")
        velikost = cr.split("/")[-1] if "/" in cr else r.headers.get("Content-Length", "")
        return b, velikost, r.headers.get("Last-Modified", "")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages_json")
    ap.add_argument("izhod_tsv")
    ap.add_argument("--zamik", type=float, default=0.1)
    ap.add_argument("--prejsnji", help="prejšnji slike.tsv za ponovno rabo meritev")
    a = ap.parse_args()

    znano = {}
    if a.prejsnji and os.path.exists(a.prejsnji):
        with open(a.prejsnji, encoding="utf-8") as f:
            next(f)
            for v in f:
                c = v.rstrip("\n").split("\t")
                znano[brez_www(c[0])] = c[1:6]

    with open(a.pages_json, encoding="utf-8") as f:
        podatki = json.load(f)
    nacin = podatki.get("ua", "modul")
    slike = {}
    for stran in podatki["strani"]:
        for s in stran["slike"]:
            z = slike.setdefault(s["url"], {"strani": [], "izvor": set(), "alt": ""})
            z["strani"].append(stran["url"])
            z["izvor"].update(s["izvor"])
            z["alt"] = z["alt"] or s.get("alt", "")

    vrstice, napake, ponovno = [], 0, 0
    for url, z in sorted(slike.items()):
        if brez_www(url) in znano:
            meritev = znano[brez_www(url)]
            ponovno += 1
        else:
            try:
                b, velikost, spremenjeno = preberi_glavo(url, nacin)
            except (urllib.error.URLError, TimeoutError, ValueError):
                napake += 1
                continue
            w, h, fmt = dimenzije(b)
            meritev = [w or "", h or "", fmt, velikost, spremenjeno]
            time.sleep(a.zamik)
        vrstice.append([url, *meritev, len(set(z["strani"])),
                        ",".join(sorted(z["izvor"])), z["alt"].replace("\t", " "), z["strani"][0]])

    with open(a.izhod_tsv, "w", encoding="utf-8") as f:
        f.write("url\tsirina\tvisina\tformat\tbajti\tspremenjeno\tst_strani\tizvor\talt\tprimer_strani\n")
        for v in vrstice:
            f.write("\t".join(map(str, v)) + "\n")
    print(f"Slik: {len(vrstice)}  ponovno uporabljenih meritev: {ponovno}  nedosegljivih: {napake}"
          f"  → {a.izhod_tsv}", file=sys.stderr)


if __name__ == "__main__":
    main()
