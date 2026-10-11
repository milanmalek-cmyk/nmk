#!/usr/bin/env python3
"""Prenos izbranih originalnih slik in samodejna evidenca.

Uporaba:
  python3 -I fetch_assets.py PROJEKT/03_paket-chatgpt [--ua brskalnik] [--brez-omrezja]

Vhod:  izbor.tsv v podani mapi, stolpci:  url <TAB> mapa <TAB> uporaba
Izhod: slike/<mapa>/<izvirno ime>, slike.json (meritve + SHA-256) in EVIDENCA.md (tabela).

Pravila: datoteka se prenese bajt-za-bajt in se nikoli ne spreminja (brez obrezovanja,
pretvorbe ali stiskanja). Če že obstaja in je enako velika kot na strežniku, se ne prenaša
znova. Z --brez-omrezja se samo preverijo in popišejo lokalne datoteke.
"""
import argparse
import email.utils
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skupno import odpri  # noqa: E402


def velikost_na_strezniku(url, ua):
    with odpri(url, ua, bajti=1) as r:
        cr = r.headers.get("Content-Range", "")
        return int(cr.split("/")[-1]) if "/" in cr else int(r.headers.get("Content-Length", -1))


def prenesi(url, cilj, ua):
    with odpri(url, ua, timeout=60) as r:
        telo = r.read()
        pricakovano = r.headers.get("Content-Length")
        spremenjeno = r.headers.get("Last-Modified")
    if pricakovano and int(pricakovano) != len(telo):
        raise OSError(f"nepopoln prenos ({len(telo)} od {pricakovano} B)")
    os.makedirs(os.path.dirname(cilj), exist_ok=True)
    with open(cilj, "wb") as f:
        f.write(telo)
    if spremenjeno:   # ohrani izvirni datum datoteke
        t = email.utils.parsedate_to_datetime(spremenjeno).timestamp()
        os.utime(cilj, (t, t))


def meritev(pot):
    from PIL import Image
    try:
        with Image.open(pot) as im:
            w, h = im.size
            prosojna = im.mode in ("RGBA", "LA") or "transparency" in im.info
    except OSError:
        w = h = None
        prosojna = False
    with open(pot, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    return {"sirina": w, "visina": h, "prosojna": prosojna, "bajti": os.path.getsize(pot), "sha256": sha}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paket")
    ap.add_argument("--ua", default="modul", choices=["modul", "brskalnik"])
    ap.add_argument("--brez-omrezja", action="store_true")
    a = ap.parse_args()

    izbor = []
    with open(os.path.join(a.paket, "izbor.tsv"), encoding="utf-8") as f:
        for v in f:
            if v.strip() and not v.startswith(("#", "url\t")):
                url, mapa, uporaba = (v.rstrip("\n").split("\t") + ["", ""])[:3]
                izbor.append((url.strip(), mapa.strip(), uporaba.strip()))

    zapisi, napake = [], 0
    stevci = {"preneseno": 0, "ponovno": 0}
    for url, mapa, uporaba in izbor:
        ime = os.path.basename(urllib.parse.unquote(urllib.parse.urlsplit(url).path))
        rel = os.path.join("slike", mapa, ime)
        cilj = os.path.join(a.paket, rel)
        try:
            if os.path.exists(cilj) and (a.brez_omrezja or
                                         velikost_na_strezniku(url, a.ua) == os.path.getsize(cilj)):
                stanje = "ponovno uporabljeno"
                stevci["ponovno"] += 1
            elif a.brez_omrezja:
                raise OSError("datoteke ni in prenos je izklopljen")
            else:
                prenesi(url, cilj, a.ua)
                stanje = "preneseno"
                stevci["preneseno"] += 1
        except (OSError, urllib.error.URLError) as e:
            print(f"  NAPAKA {url}: {e}", file=sys.stderr)
            napake += 1
            continue
        zapisi.append({"datoteka": rel, "url": url, "mapa": mapa, "uporaba": uporaba, "stanje": stanje, **meritev(cilj)})

    with open(os.path.join(a.paket, "slike.json"), "w", encoding="utf-8") as f:
        json.dump(zapisi, f, ensure_ascii=False, indent=1)

    with open(os.path.join(a.paket, "EVIDENCA.md"), "w", encoding="utf-8") as f:
        f.write("# Evidenca slik\n\nVse datoteke so originali s strežnika naročnika, nespremenjene in z izvirnimi imeni "
                "(preverjeno z velikostjo in SHA-256). Izdelkov, embalaže, etiket in logotipov ne spreminjaj.\n\n"
                "| # | Datoteka | Izvorni URL | Velikost (px) | Predlagana uporaba |\n|---|---|---|---|---|\n")
        for i, z in enumerate(zapisi, 1):
            dim = f"{z['sirina']}×{z['visina']}" if z["sirina"] else "–"
            if z["prosojna"]:
                dim += ", prosojen PNG"
            f.write(f"| {i} | `{z['datoteka']}` | {z['url']} | {dim} | {z['uporaba']} |\n")

    print(f"Slik: {len(zapisi)}  preneseno: {stevci['preneseno']}  ponovno uporabljeno: {stevci['ponovno']}"
          f"  napak: {napake}")
    sys.exit(1 if napake else 0)


if __name__ == "__main__":
    main()
