#!/usr/bin/env python3
"""Evidenca podjetij iz Google Sheets: razčlenitev, pregled, naloge in varen načrt zapisa.

Vhod je kopija zavihka evidence, kot jo vrne konektor (get_values 'Predizbor 30'!A1:W),
shranjena v JSON datoteko ({"range": ..., "values": [[...], ...]}).

Uporaba:
  python3 -I evidenca.py razcleni POSNETEK.json            → JSON seznam podjetij (vrstica, polja, ključi)
  python3 -I evidenca.py pregled POSNETEK.json             → pregled za /podjetja
  python3 -I evidenca.py naloge POSNETEK.json              → čakajoče naloge iz stolpca »Naloga za Claude«
  python3 -I evidenca.py najdi POSNETEK.json "ime ali domena"
  python3 -I evidenca.py nacrt POSNETEK.json PREDLOG.json  → preverjen načrt zapisa (JSON + tabela)

PREDLOG.json: [{"podjetje": "GEOFOTO d.o.o.", "maticna": "...", "polja": {"ai_ocena": "=…{r}…", "stanje": "OCENJENO"}}]
V vrednostih se {r} zamenja s številko vrstice. Pravila (config/evidenca.json → lastnistvo):
  samo_uporabnik  – nikoli
  claude_ce_prazno – samo v prazno celico (različen obstoječ podatek gre med razhajanja)
  claude          – vedno
  claude_omejeno  – samo dovoljene vrednosti in samo v prazno celico
"""
import json
import os
import re
import sys
import unicodedata
import urllib.parse

MODUL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PRAVNE_OBLIKE = r"\b(d\s*\.?\s*o\s*\.?\s*o|s\s*\.?\s*p|d\s*\.?\s*d|k\s*\.?\s*d|d\s*\.?\s*n\s*\.?\s*o|z\s*\.?\s*o\s*\.?\s*o)\b\.?"


def nastavitve():
    with open(os.path.join(MODUL, "config", "evidenca.json"), encoding="utf-8") as f:
        return json.load(f)


def crka(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def kljuc_ime(ime):
    s = unicodedata.normalize("NFKD", ime or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(PRAVNE_OBLIKE, " ", s)
    s = re.sub(r",.*$", "", s)                       # »Š NAILS, Špela Šega s.p.« → »s nails«
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def kljuc_domena(url):
    if not url or "." not in url:
        return ""
    n = urllib.parse.urlsplit(url if "://" in url else "https://" + url).netloc.lower()
    return n[4:] if n.startswith("www.") else n


def preberi(pot):
    with open(pot, encoding="utf-8") as f:
        podatki = json.load(f)
    vrstice = podatki["values"] if isinstance(podatki, dict) else podatki
    m = re.search(r"![A-Z]+(\d+)", podatki.get("range", "") if isinstance(podatki, dict) else "")
    prva = int(m.group(1)) if m else 1
    if prva != 1:
        sys.exit("Posnetek mora vključevati glavo (obseg od vrstice 1, npr. 'Predizbor 30'!A1:W).")
    return vrstice


def razcleni(vrstice, n=None):
    n = n or nastavitve()
    glava = vrstice[0]
    stolpci, manjka = {}, []
    for vloga, zacetek in n["stolpci"].items():
        idx = next((i for i, g in enumerate(glava) if g.strip().lower().startswith(zacetek.lower())), None)
        if idx is None:
            manjka.append(f"{vloga} ({zacetek})")
        else:
            stolpci[vloga] = idx
    if "podjetje" not in stolpci:
        sys.exit("V glavi ni stolpca »Podjetje«.")
    podjetja = []
    for i, v in enumerate(vrstice[1:], start=2):
        if not v or not str(v[stolpci["podjetje"]] if len(v) > stolpci["podjetje"] else "").strip():
            continue
        polja = {vl: (v[ix].strip() if ix < len(v) and isinstance(v[ix], str) else (v[ix] if ix < len(v) else ""))
                 for vl, ix in stolpci.items()}
        podjetja.append({
            "vrstica": i,
            "polja": polja,
            "kljuci": {"ime": kljuc_ime(polja["podjetje"]),
                       "domena": kljuc_domena(polja.get("spletna_stran") or polja.get("vir_strani", "")),
                       "maticna": re.sub(r"\D", "", str(polja.get("maticna", "")))},
        })
    return {"stolpci": {vl: crka(ix) for vl, ix in stolpci.items()}, "_idx": stolpci,
            "manjkajo_stolpci": manjka, "podjetja": podjetja, "dvojniki": dvojniki(podjetja)}


def dvojniki(podjetja):
    skupine = []
    for vrsta in ("maticna", "domena", "ime"):
        po = {}
        for p in podjetja:
            k = p["kljuci"][vrsta]
            if k:
                po.setdefault(k, []).append(p)
        for k, ps in po.items():
            if len(ps) > 1:
                skupine.append({"po": vrsta, "kljuc": k,
                                "podjetja": [f"{p['polja']['podjetje']} (vrstica {p['vrstica']})" for p in ps]})
    return skupine


def stevilo(v):
    """»1,288,896 €« → 1288896.0, »12.8%« → 0.128; None, če ni število."""
    if isinstance(v, (int, float)):
        return float(v)
    t = str(v).strip().replace("€", "").replace(" ", "").replace("\u00a0", "")
    odstotek = t.endswith("%")
    t = t.rstrip("%").replace(",", "")
    try:
        x = float(t)
    except ValueError:
        return None
    return x / 100 if odstotek else x


def enako(staro, novo):
    a, b = stevilo(staro), stevilo(novo)
    if a is not None and b is not None:
        return abs(a - b) <= max(1.0, abs(a) * 0.001) if abs(a) >= 1 else abs(a - b) < 0.001
    return str(staro).strip() == str(novo).strip()


def caka(p):
    """Ali naloga v stolpcu »Naloga za Claude« še ni opravljena."""
    naloga, stanje, faza = p["polja"].get("naloga", ""), p["polja"].get("stanje", ""), p["polja"].get("prodajna_faza", "")
    if naloga == "OCENI":
        return stanje in ("", "NAPAKA")
    if naloga == "ZA ANALIZO":
        return stanje in ("", "OCENJENO", "NAPAKA", "V TEKU")
    if naloga == "PRIPRAVI PONUDBO":
        return faza == ""
    return False


def ukaz_pregled(r):
    ps = r["podjetja"]
    def stej(vloga):
        c = {}
        for p in ps:
            c[p["polja"].get(vloga) or "(prazno)"] = c.get(p["polja"].get(vloga) or "(prazno)", 0) + 1
        return ", ".join(f"{k}: {v}" for k, v in sorted(c.items(), key=lambda x: -x[1]))
    print(f"Podjetij: {len(ps)}")
    print(f"Status: {stej('status')}")
    print(f"Stanje priprave: {stej('stanje')}")
    print(f"Prodajna faza: {stej('prodajna_faza')}")
    cakajo = [p for p in ps if caka(p)]
    print(f"\nČakajoče naloge ({len(cakajo)}):")
    for p in cakajo:
        print(f"  vrstica {p['vrstica']:>3}  {p['polja']['naloga']:<17} {p['polja']['podjetje']}"
              f"{'  ⚠ V TEKU (morda prekinjeno)' if p['polja'].get('stanje') == 'V TEKU' else ''}")
    brez = [p for p in ps if not (p["polja"].get("prihodki") and p["polja"].get("dobicek"))]
    brez_strani = [p for p in ps if not p["kljuci"]["domena"]]
    print(f"\nBrez financ: {len(brez)} · brez spletne strani: {len(brez_strani)} · brez matične: "
          f"{sum(1 for p in ps if not p['kljuci']['maticna'])}")
    ocenjeni = sorted((p for p in ps if str(p["polja"].get("ai_ocena", "")).strip()),
                      key=lambda p: -float(str(p["polja"]["ai_ocena"]).replace(",", ".") or 0))
    if ocenjeni:
        print("\nNajvišje AI ocene:")
        for p in ocenjeni[:5]:
            print(f"  {p['polja']['ai_ocena']:>4}  {p['polja']['podjetje']}  ({p['polja'].get('status', '')})")
    if r["dvojniki"]:
        print("\nMožni dvojniki:")
        for d in r["dvojniki"]:
            print(f"  po {d['po']} »{d['kljuc']}«: " + "; ".join(d["podjetja"]))
    if r["manjkajo_stolpci"]:
        print("\n⚠ Manjkajoči stolpci: " + ", ".join(r["manjkajo_stolpci"]))


def najdi(r, poizvedba=None, maticna=None, domena=None):
    ps = r["podjetja"]
    if maticna:
        z = [p for p in ps if p["kljuci"]["maticna"] == re.sub(r"\D", "", maticna)]
        if z:
            return z
    if domena:
        z = [p for p in ps if p["kljuci"]["domena"] and p["kljuci"]["domena"] == kljuc_domena(domena)]
        if z:
            return z
    if poizvedba:
        k = kljuc_ime(poizvedba)
        z = [p for p in ps if p["kljuci"]["ime"] == k]
        if not z:
            z = [p for p in ps if k and (k in p["kljuci"]["ime"] or (p["kljuci"]["domena"] and k in p["kljuci"]["domena"]))]
        return z
    return []


def ukaz_nacrt(r, predlogi, n):
    last = n["lastnistvo"]
    dovoljene = n["vrednosti"]
    zavihek = n["zavihki"]["evidenca"]
    nacrt, zavrnjeno, razhajanja = [], [], []
    for pr in predlogi:
        z = najdi(r, pr.get("podjetje"), pr.get("maticna"), pr.get("domena"))
        if len(z) != 1:
            zavrnjeno.append({"podjetje": pr.get("podjetje"), "razlog": "ni najdeno" if not z else
                              "več zadetkov: " + ", ".join(f"{p['polja']['podjetje']} (vrstica {p['vrstica']})" for p in z)})
            continue
        p = z[0]
        vr = p["vrstica"]
        celice = {}
        for vloga, nova in pr["polja"].items():
            if vloga not in r["_idx"]:
                zavrnjeno.append({"podjetje": p["polja"]["podjetje"], "polje": vloga, "razlog": "stolpca ni"})
                continue
            if isinstance(nova, str):
                nova = nova.replace("{r}", str(vr))
            staro = p["polja"].get(vloga, "")
            prazno = str(staro).strip() == ""
            razlog = None
            if vloga in last["samo_uporabnik"]:
                razlog = "vaš stolpec – Claude vanj ne piše"
            elif vloga in last["claude_ce_prazno"] and not prazno:
                if enako(staro, nova):
                    continue   # podatek je že vpisan
                razlog = "celica ni prazna – ne prepisujem"
                razhajanja.append({"podjetje": p["polja"]["podjetje"], "polje": vloga, "v_evidenci": staro, "najdeno": nova})
            elif vloga in last["claude_omejeno"]:
                if nova not in last["claude_omejeno"][vloga]:
                    razlog = f"Claude sme vpisati samo: {', '.join(last['claude_omejeno'][vloga])}"
                elif not prazno:
                    razlog = "celica ni prazna – faze ne spreminjam"
            elif vloga not in last["claude"] and vloga not in last["claude_ce_prazno"]:
                razlog = "stolpec nima določenega lastništva"
            if not razlog and vloga in dovoljene and nova not in dovoljene[vloga]:
                razlog = f"neveljavna vrednost (dovoljeno: {', '.join(dovoljene[vloga])})"
            if razlog:
                zavrnjeno.append({"podjetje": p["polja"]["podjetje"], "polje": vloga, "razlog": razlog})
                continue
            if str(staro) != str(nova):
                celice[r["_idx"][vloga]] = (vloga, staro, nova)
        if celice:
            od, do = min(celice), max(celice)
            vrednosti = [celice[i][2] if i in celice else None for i in range(od, do + 1)]
            nacrt.append({"podjetje": p["polja"]["podjetje"], "vrstica": vr,
                          "range": f"'{zavihek}'!{crka(od)}{vr}:{crka(do)}{vr}", "values": [vrednosti],
                          "spremembe": [{"celica": f"{crka(i)}{vr}", "vloga": v, "staro": s, "novo": nv}
                                        for i, (v, s, nv) in sorted(celice.items())]})
    return {"nacrt": nacrt, "zavrnjeno": zavrnjeno, "razhajanja": razhajanja}


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    ukaz, posnetek = sys.argv[1], sys.argv[2]
    n = nastavitve()
    r = razcleni(preberi(posnetek), n)
    if ukaz == "razcleni":
        print(json.dumps({k: v for k, v in r.items() if k != "_idx"}, ensure_ascii=False, indent=1))
    elif ukaz == "pregled":
        ukaz_pregled(r)
    elif ukaz == "naloge":
        print(json.dumps([{"vrstica": p["vrstica"], "podjetje": p["polja"]["podjetje"], "naloga": p["polja"]["naloga"],
                           "stanje": p["polja"].get("stanje", ""), "spletna_stran": p["polja"].get("spletna_stran", "")}
                          for p in r["podjetja"] if caka(p)], ensure_ascii=False, indent=1))
    elif ukaz == "najdi":
        z = najdi(r, sys.argv[3])
        print(json.dumps([{"vrstica": p["vrstica"], **p["polja"]} for p in z], ensure_ascii=False, indent=1))
        sys.exit(0 if len(z) == 1 else 1)
    elif ukaz == "nacrt":
        with open(sys.argv[3], encoding="utf-8") as f:
            izid = ukaz_nacrt(r, json.load(f), n)
        print(json.dumps(izid, ensure_ascii=False, indent=1))
        print("\n| Celica | Polje | Zdaj | Novo |\n|---|---|---|---|", file=sys.stderr)
        for z in izid["nacrt"]:
            for s in z["spremembe"]:
                print(f"| {s['celica']} | {s['vloga']} | {s['staro'] or '–'} | {s['novo']} |", file=sys.stderr)
        for z in izid["zavrnjeno"]:
            print(f"ZAVRNJENO: {z}", file=sys.stderr)
        for z in izid["razhajanja"]:
            print(f"RAZHAJANJE: {z}", file=sys.stderr)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
