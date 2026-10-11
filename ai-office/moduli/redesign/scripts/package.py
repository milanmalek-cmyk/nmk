#!/usr/bin/env python3
"""Sestavi ZIP za ChatGPT iz projekta in ga preveri.

Uporaba:
  python3 -I package.py PROJEKT_MAPA

Vsebina ZIP-a (<stranka>-chatgpt/):
  00_POZIV-ZA-CHATGPT.md   ← 03_paket-chatgpt/chatgpt-poziv.md
  01_STRUKTURA.md          ← 02_vsebina/struktura.md
  02_BESEDILA.md           ← 02_vsebina/besedila.md
  03_SMERNICE.md           ← 03_paket-chatgpt/smernice.md
  04_BARVE-IN-LOGOTIP.md   ← 03_paket-chatgpt/barve.md
  05_EVIDENCA-SLIK.md      ← 03_paket-chatgpt/EVIDENCA.md
  slike/…                  ← 03_paket-chatgpt/slike/
  referenca/…              ← 01_analiza/posnetki/obstojeca-*.jpg (trenutno stanje, če obstaja)
ZIP se zapiše v PROJEKT_MAPA/<stranka>-chatgpt.zip (v git ne gre).
"""
import glob
import hashlib
import json
import os
import sys
import zipfile

DOKUMENTI = [
    ("00_POZIV-ZA-CHATGPT.md", "03_paket-chatgpt/chatgpt-poziv.md"),
    ("01_STRUKTURA.md", "02_vsebina/struktura.md"),
    ("02_BESEDILA.md", "02_vsebina/besedila.md"),
    ("03_SMERNICE.md", "03_paket-chatgpt/smernice.md"),
    ("04_BARVE-IN-LOGOTIP.md", "03_paket-chatgpt/barve.md"),
    ("05_EVIDENCA-SLIK.md", "03_paket-chatgpt/EVIDENCA.md"),
]


def sha(pot):
    with open(pot, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    projekt = sys.argv[1].rstrip("/")
    with open(os.path.join(projekt, "projekt.json"), encoding="utf-8") as f:
        slug = json.load(f)["stranka"]["slug"]
    koren = f"{slug}-chatgpt"

    vsebina, manjka = [], []
    for ime, vir in DOKUMENTI:
        pot = os.path.join(projekt, vir)
        if os.path.exists(pot):
            vsebina.append((pot, f"{koren}/{ime}"))
        else:
            manjka.append(vir)
    slike = os.path.join(projekt, "03_paket-chatgpt", "slike")
    for pot in sorted(glob.glob(os.path.join(slike, "**", "*"), recursive=True)):
        if os.path.isfile(pot):
            vsebina.append((pot, f"{koren}/slike/{os.path.relpath(pot, slike)}"))
    for pot in sorted(glob.glob(os.path.join(projekt, "01_analiza", "posnetki", "obstojeca-*.jpg"))):
        vsebina.append((pot, f"{koren}/referenca/{os.path.basename(pot)}"))
    if manjka:
        sys.exit("Paket ni popoln, manjka: " + ", ".join(manjka))
    if not any("/slike/" in arc for _, arc in vsebina):
        sys.exit("V 03_paket-chatgpt/slike ni slik – najprej zaženi fetch_assets.py")

    izhod = os.path.join(projekt, f"{koren}.zip")
    with zipfile.ZipFile(izhod, "w", zipfile.ZIP_DEFLATED) as z:
        for pot, arc in vsebina:
            z.write(pot, arc)   # zapiše tudi izvirni čas spremembe datoteke

    with zipfile.ZipFile(izhod) as z:   # preverjanje: vsaka datoteka enaka viru
        for pot, arc in vsebina:
            if hashlib.sha256(z.read(arc)).hexdigest() != sha(pot):
                sys.exit(f"Preverjanje ni uspelo: {arc}")
    st_slik = sum("/slike/" in arc for _, arc in vsebina)
    print(f"{izhod}  ({os.path.getsize(izhod) / 1e6:.1f} MB, {len(vsebina)} datotek, od tega {st_slik} slik) – preverjeno")


if __name__ == "__main__":
    main()
