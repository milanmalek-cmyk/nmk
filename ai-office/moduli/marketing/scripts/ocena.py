#!/usr/bin/env python3
"""Ocena potencialne stranke 0–100 po merilih (config/merila.json).

Uporaba:
  python3 -I ocena.py OCENA.json            → JSON: točke po skupinah, skupaj, popolnost, status, vrstica za »AI ocene«
  python3 -I ocena.py OCENA.json --md       → tabela za poročilo

OCENA.json (izpolni agent; vsaka dodeljena točka ima dokaz in vir):
{"podjetje": "GEOFOTO d.o.o.", "maticna": "…", "datum": "2026-10-11",
 "merila": {"prihodki_v_razponu": {"tocke": 10, "dokaz": "1.288.896 € (2025)", "vir": "https://…"},
            "seo_geo": {"tocke": null, "manjka": "…"}},
 "izlocitve": [], "cenovna_skupina": "B 2.500–4.000 €", "obrazlozitev": "…", "porocilo": "https://…"}
Manjkajoče merilo ali "tocke": null = brez točk in ocena je DELNA (podatkov ne izmišljamo).
"""
import json
import os
import sys

MODUL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def izracun(o, merila):
    skupine, napake, manjka, viri = {}, [], [], []
    for sk, sdef in merila["skupine"].items():
        vsota, najvec = 0, 0
        for kl, mdef in sdef["merila"].items():
            najvec += mdef["tocke"]
            m = o.get("merila", {}).get(kl)
            if not m or m.get("tocke") is None:
                manjka.append(f"{mdef['opis']}" + (f" – {m['manjka']}" if m and m.get("manjka") else ""))
                continue
            t = m["tocke"]
            if not isinstance(t, (int, float)) or t < 0 or t > mdef["tocke"]:
                napake.append(f"{kl}: {t} ni med 0 in {mdef['tocke']}")
                continue
            if t > 0 and not (m.get("dokaz") and m.get("vir")):
                napake.append(f"{kl}: točke brez dokaza ali vira")
            if m.get("vir") and m["vir"] not in viri:
                viri.append(m["vir"])
            vsota += t
        skupine[sk] = {"ime": sdef["ime"], "tocke": vsota, "najvec": najvec}
    skupaj = sum(s["tocke"] for s in skupine.values())
    izl = [merila["izlocitve"][k] for k in o.get("izlocitve", []) if k in merila["izlocitve"]]
    neznane = [k for k in o.get("izlocitve", []) if k not in merila["izlocitve"]]
    if neznane:
        napake.append("neznane izločitve: " + ", ".join(neznane))
    p = merila["pragovi"]
    status = izl[0] if izl else ("PREDNOSTNO" if skupaj >= p["PREDNOSTNO"] else "PREVERI" if skupaj >= p["PREVERI"] else p["spodaj"])
    return {"podjetje": o["podjetje"], "skupine": skupine, "skupaj": skupaj,
            "popolnost": "DELNA" if manjka else "POLNA", "predlagan_status": status,
            "izlocitve": izl, "manjka": manjka, "viri": viri, "napake": napake}


def vrstica_ai_ocene(o, r):
    """Vrstica za zavihek »AI ocene« (stolpci A–O); Skupaj je formula, {r} = številka vrstice."""
    s = r["skupine"]
    return [o["podjetje"], ("'" + o["maticna"]) if o.get("maticna") else "", o.get("datum", ""),
            s["finance"]["tocke"], s["spletna_stran"]["tocke"], s["potencial"]["tocke"],
            "=SUM(D{r}:F{r})", r["popolnost"], r["predlagan_status"], o.get("cenovna_skupina", ""),
            o.get("obrazlozitev", ""), "\n".join(r["viri"]), "; ".join(r["manjka"]),
            o.get("razhajanja", ""), o.get("porocilo", "")]


def tabela(o, r, merila):
    vr = [f"| Merilo | Točke | Dokaz | Vir |", "|---|---|---|---|"]
    for sk, sdef in merila["skupine"].items():
        vr.append(f"| **{sdef['ime']}** | **{r['skupine'][sk]['tocke']} / {r['skupine'][sk]['najvec']}** | | |")
        for kl, mdef in sdef["merila"].items():
            m = o.get("merila", {}).get(kl) or {}
            t = "–" if m.get("tocke") is None else m["tocke"]
            vr.append(f"| {mdef['opis']} | {t} / {mdef['tocke']} | {m.get('dokaz') or m.get('manjka') or 'ni podatka'} "
                      f"| {m.get('vir', '')} |")
    vr.append(f"| **Skupaj** | **{r['skupaj']} / 100** ({r['popolnost'].lower()}) | predlagan status: "
              f"**{r['predlagan_status']}** | |")
    return "\n".join(vr)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    with open(os.path.join(MODUL, "config", "merila.json"), encoding="utf-8") as f:
        merila = json.load(f)
    with open(sys.argv[1], encoding="utf-8") as f:
        o = json.load(f)
    r = izracun(o, merila)
    if "--md" in sys.argv:
        print(tabela(o, r, merila))
    else:
        print(json.dumps({**r, "vrstica_ai_ocene": vrstica_ai_ocene(o, r)}, ensure_ascii=False, indent=1))
    if r["napake"]:
        print("NAPAKE: " + "; ".join(r["napake"]), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
