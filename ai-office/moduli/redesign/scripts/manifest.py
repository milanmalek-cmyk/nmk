#!/usr/bin/env python3
"""Manifest projekta (projekt.json): ustvarjanje, stanje faz in odobritve.

Uporaba:
  python3 -I manifest.py init URL --stranka bio-sad --naziv "BIO-SAD d.o.o." [--projekt naslovnica-2026-10]
  python3 -I manifest.py najdi URL
  python3 -I manifest.py stanje PROJEKT
  python3 -I manifest.py faza PROJEKT F3 zakljuceno [--izhod 02_vsebina/besedila.md ...] [--opomba "..."]
  python3 -I manifest.py odobri PROJEKT V1 --kdo "Milan Malek" [--opomba "..."]

Vrata potrditve: V1 (dizajn v ChatGPT) pred F6, V2 (objava predogleda) pred objavo v F7,
V3 (pošiljanje stranki) pred kakršnimkoli pošiljanjem v F8. Odobritev vpiše samo
uporabnik ali agent po izrecni potrditvi uporabnika v pogovoru.
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.parse

KOREN = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PROJEKTI = os.path.join(KOREN, "projekti")
FAZE = [("F0", "Inventar"), ("F1", "Pregled strani"), ("F2", "Raziskava"), ("F3", "Vsebina"),
        ("F4", "Vizualni materiali"), ("F5", "Paket za ChatGPT"), ("F6", "Gradnja"),
        ("F7", "Predogled"), ("F8", "Prodaja")]
VRATA = {"V1": ("F6", "dizajn potrjen v ChatGPT"),
         "V2": ("F7", "objava predogleda"),
         "V3": ("F8", "pošiljanje stranki")}
STANJA = ("caka", "v_teku", "zakljuceno", "blokirano")
MAPE = ["01_analiza/posnetki", "02_vsebina", "03_paket-chatgpt/slike", "04_dizajn",
        "05_naslovnica/img", "06_predogled", "07_prodaja"]


def zdaj():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def domena(url):
    n = urllib.parse.urlsplit(url if "://" in url else "https://" + url).netloc.lower()
    return n[4:] if n.startswith("www.") else n


def beri(projekt):
    with open(os.path.join(projekt, "projekt.json"), encoding="utf-8") as f:
        return json.load(f)


def pisi(projekt, m):
    m["posodobljeno"] = zdaj()
    pot = os.path.join(projekt, "projekt.json")
    with open(pot + ".tmp", "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(pot + ".tmp", pot)


def vsi_projekti():
    for dp, _, fs in os.walk(PROJEKTI):
        if "projekt.json" in fs:
            yield dp


def ukaz_najdi(a):
    d = domena(a.url)
    najdeni = [p for p in vsi_projekti() if domena(beri(p)["stranka"]["url"]) == d]
    for p in najdeni:
        print(os.path.relpath(p, KOREN))
    if not najdeni:
        print(f"Ni projekta za {d}.", file=sys.stderr)
        sys.exit(1)


def ukaz_init(a):
    if not re.fullmatch(r"[a-z0-9-]+", a.stranka):
        sys.exit("--stranka: samo male črke, številke in vezaji (npr. bio-sad)")
    ime = a.projekt or "naslovnica-" + datetime.date.today().strftime("%Y-%m")
    projekt = os.path.join(PROJEKTI, a.stranka, ime)
    if os.path.exists(os.path.join(projekt, "projekt.json")):
        print(f"Projekt že obstaja: {os.path.relpath(projekt, KOREN)}")
        return
    for m in MAPE:
        os.makedirs(os.path.join(projekt, m), exist_ok=True)
    pisi(projekt, {
        "verzija_sheme": 1,
        "id": f"{a.stranka}/{ime}",
        "modul": "redesign",
        "stranka": {"slug": a.stranka, "naziv": a.naziv or a.stranka, "url": a.url, "crm_id": None},
        "ustvarjeno": zdaj(),
        "faze": [{"id": i, "ime": n, "stanje": "caka", "posodobljeno": None, "izhodi": [], "opomba": ""}
                 for i, n in FAZE],
        "odobritve": [],
        "predogled": {"pot": None, "url": None, "objavljeno": None},
    })
    print(f"Ustvarjen projekt: {os.path.relpath(projekt, KOREN)}")


def odobreno(m, vrata):
    return any(o["vrata"] == vrata for o in m["odobritve"])


def ukaz_faza(a):
    m = beri(a.projekt)
    if a.faza == "F6" and a.stanje in ("v_teku", "zakljuceno") and not odobreno(m, "V1"):
        sys.exit("F6 se lahko začne šele po odobritvi V1 (dizajn potrjen v ChatGPT).")
    if a.faza == "F7" and a.stanje == "zakljuceno" and not odobreno(m, "V2"):
        sys.exit("F7 je zaključena šele z objavo, ta pa zahteva odobritev V2.")
    f = next((f for f in m["faze"] if f["id"] == a.faza), None)
    if not f:
        sys.exit(f"Neznana faza {a.faza}")
    f["stanje"], f["posodobljeno"] = a.stanje, zdaj()
    f["izhodi"] = sorted(set(f["izhodi"]) | set(a.izhod or []))
    if a.opomba is not None:
        f["opomba"] = a.opomba
    pisi(a.projekt, m)
    print(f"{a.faza} {f['ime']}: {a.stanje}")


def ukaz_odobri(a):
    m = beri(a.projekt)
    m["odobritve"].append({"vrata": a.vrata, "opis": VRATA[a.vrata][1], "kdo": a.kdo,
                           "cas": zdaj(), "opomba": a.opomba or ""})
    pisi(a.projekt, m)
    print(f"Zapisana odobritev {a.vrata} ({VRATA[a.vrata][1]}) – {a.kdo}")


def ukaz_stanje(a):
    m = beri(a.projekt)
    ikone = {"caka": "⬜", "v_teku": "🔄", "zakljuceno": "✅", "blokirano": "⛔"}
    print(f"{m['stranka']['naziv']} – {m['id']}  ({m['stranka']['url']})")
    for f in m["faze"]:
        vrata = [v for v, (fz, _) in VRATA.items() if fz == f["id"]]
        oznaka = "".join(f"  [{v}: {'odobreno' if odobreno(m, v) else 'čaka potrditev'}]" for v in vrata)
        print(f"  {ikone.get(f['stanje'], '?')} {f['id']} {f['ime']:<20}{oznaka}  {f['opomba']}")
    if m["predogled"].get("url"):
        print(f"  Predogled: {m['predogled']['url']}  objavljeno: {m['predogled'].get('objavljeno') or 'ne'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="ukaz", required=True)
    p = sub.add_parser("init")
    p.add_argument("url")
    p.add_argument("--stranka", required=True)
    p.add_argument("--naziv")
    p.add_argument("--projekt")
    p = sub.add_parser("najdi")
    p.add_argument("url")
    p = sub.add_parser("stanje")
    p.add_argument("projekt")
    p = sub.add_parser("faza")
    p.add_argument("projekt")
    p.add_argument("faza", choices=[i for i, _ in FAZE])
    p.add_argument("stanje", choices=STANJA)
    p.add_argument("--izhod", nargs="*")
    p.add_argument("--opomba")
    p = sub.add_parser("odobri")
    p.add_argument("projekt")
    p.add_argument("vrata", choices=list(VRATA))
    p.add_argument("--kdo", required=True)
    p.add_argument("--opomba")
    a = ap.parse_args()
    {"init": ukaz_init, "najdi": ukaz_najdi, "stanje": ukaz_stanje,
     "faza": ukaz_faza, "odobri": ukaz_odobri}[a.ukaz](a)


if __name__ == "__main__":
    main()
