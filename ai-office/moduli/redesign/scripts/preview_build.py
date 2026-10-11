#!/usr/bin/env python3
"""Pripravi zaščiteno izdajo predogleda iz 05_naslovnica (ne objavi ničesar).

Uporaba:
  python3 -I preview_build.py PROJEKT [--nastavitve ../../moduli/redesign/config/nastavitve.env]

Naredi 06_predogled/izdaja/<pot>/ s kopijo naslovnice in doda:
  - <meta name="robots" content="noindex, nofollow, noarchive"> in predpono »PREDLOG PRENOVE« v <title>
  - stalen trak z oznako predloga (templates/predogled/oznaka.html)
  - .htaccess: HTTP Basic Auth + glava X-Robots-Tag (templates/predogled/.htaccess)
Geslo se ustvari enkrat in shrani v 06_predogled/.dostop (ni v gitu), hash v 06_predogled/.htpasswd.
Pot (<stranka>-<naključni niz>) ostane enaka ob vsaki ponovni izdaji, da se povezava ne spreminja.
"""
import argparse
import datetime
import html
import os
import re
import secrets
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifest import beri, pisi  # noqa: E402

MODUL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PREDLOGE = os.path.join(MODUL, "templates", "predogled")


def beri_env(pot):
    nastavitve = {}
    if os.path.exists(pot):
        with open(pot, encoding="utf-8") as f:
            for v in f:
                v = v.strip()
                if v and not v.startswith("#") and "=" in v:
                    k, val = v.split("=", 1)
                    nastavitve[k.strip()] = val.strip().strip('"').strip("'")
    return nastavitve


def apr1(geslo):
    """Hash za .htpasswd (Apache in LiteSpeed) prek openssl."""
    r = subprocess.run(["openssl", "passwd", "-apr1", "-stdin"], input=geslo, capture_output=True, text=True)
    if r.returncode:
        sys.exit("openssl ni na voljo – namesti ga ali ustvari .htpasswd ročno (htpasswd -c).")
    return r.stdout.strip()


def predloga(ime, **vrednosti):
    with open(os.path.join(PREDLOGE, ime), encoding="utf-8") as f:
        t = f.read()
    for k, v in vrednosti.items():
        t = t.replace("{" + k + "}", v)
    return t


def oznaci_html(h, trak, naziv):
    meta = '<meta name="robots" content="noindex, nofollow, noarchive">'
    if 'name="robots"' not in h:
        # za <meta charset>, ki mora ostati čisto na začetku <head>
        vzorec = r"(<meta\s+charset[^>]*>)" if re.search(r"<meta\s+charset", h, re.I) else r"(<head\b[^>]*>)"
        h = re.sub(vzorec, lambda m: m.group(1) + "\n" + meta, h, count=1, flags=re.I)
    h = re.sub(r"<title>(.*?)</title>",
               lambda m: f"<title>PREDLOG PRENOVE – {m.group(1)}</title>" if "PREDLOG" not in m.group(1) else m.group(0),
               h, count=1, flags=re.I | re.S)
    if "data-predlog-prenove" not in h:
        h = re.sub(r"(<body\b[^>]*>)", lambda m: m.group(1) + "\n" + trak, h, count=1, flags=re.I)
    for preveri, opis in ((meta, "noindex"), ("data-predlog-prenove", "oznaka")):
        if preveri not in h:
            sys.exit(f"Ne morem vstaviti: {opis} ({naziv}) – manjka <head> ali <body>?")
    return h


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projekt")
    ap.add_argument("--nastavitve", default=os.path.join(MODUL, "config", "nastavitve.env"))
    a = ap.parse_args()

    n = beri_env(a.nastavitve)
    m = beri(a.projekt)
    vir = os.path.join(a.projekt, "05_naslovnica")
    if not os.path.exists(os.path.join(vir, "index.html")):
        sys.exit("V 05_naslovnica ni index.html – predogled lahko pripravim šele po gradnji (F6).")

    pot = m["predogled"].get("pot") or f"{m['stranka']['slug']}-{secrets.token_hex(4)}"
    baza = n.get("PREVIEW_BASE_URL", "https://predlogi.example.com").rstrip("/")
    url = f"{baza}/{pot}/"
    dir_pred = os.path.join(a.projekt, "06_predogled")
    izdaja = os.path.join(dir_pred, "izdaja", pot)

    dostop = os.path.join(dir_pred, ".dostop")
    if os.path.exists(dostop):
        uporabnik, geslo = open(dostop, encoding="utf-8").read().split("\n")[0].split(":", 1)
    else:
        uporabnik, geslo = m["stranka"]["slug"], secrets.token_urlsafe(9)
        with open(dostop, "w", encoding="utf-8") as f:
            f.write(f"{uporabnik}:{geslo}\n")
        os.chmod(dostop, 0o600)
    with open(os.path.join(dir_pred, ".htpasswd"), "w", encoding="utf-8") as f:
        f.write(f"{uporabnik}:{apr1(geslo)}\n")

    if os.path.exists(izdaja):
        shutil.rmtree(izdaja)
    shutil.copytree(vir, izdaja, ignore=shutil.ignore_patterns(".*", "*.md"))
    datum = datetime.date.today().strftime("%d. %m. %Y")
    trak = predloga("oznaka.html", AGENCIJA=html.escape(n.get("AGENCIJA", "Multimedija")),
                    STRANKA=html.escape(m["stranka"]["naziv"]), DATUM=datum)
    strani = []
    for dp, _, fs in os.walk(izdaja):
        for ime in fs:
            if ime.endswith(".html"):
                p = os.path.join(dp, ime)
                with open(p, encoding="utf-8") as f:
                    h = oznaci_html(f.read(), trak, ime)
                with open(p, "w", encoding="utf-8") as f:
                    f.write(h)
                strani.append(os.path.relpath(p, izdaja))
    htpasswd = n.get("PREVIEW_HTPASSWD_DIR", "/POT/DO/ZASCITENE/MAPE").rstrip("/") + f"/{pot}.htpasswd"
    with open(os.path.join(izdaja, ".htaccess"), "w", encoding="utf-8") as f:
        f.write(predloga(".htaccess", HTPASSWD=htpasswd, REALM=f"Predlog prenove – {m['stranka']['naziv']}"))

    m["predogled"].update({"pot": pot, "url": url, "pripravljeno": datetime.datetime.now().isoformat(timespec="seconds")})
    pisi(a.projekt, m)

    datoteke = sorted(os.path.relpath(os.path.join(dp, x), izdaja) for dp, _, fs in os.walk(izdaja) for x in fs)
    velikost = sum(os.path.getsize(os.path.join(izdaja, x)) for x in datoteke)
    with open(os.path.join(dir_pred, "povzetek.md"), "w", encoding="utf-8") as f:
        f.write(f"# Predogled – {m['stranka']['naziv']}\n\n"
                f"- **URL:** {url}\n- **Uporabnik:** {uporabnik} (geslo v `06_predogled/.dostop`, ni v gitu)\n"
                f"- **Zaščita:** HTTP Basic Auth, `.htpasswd` → `{htpasswd}`\n"
                f"- **Indeksiranje:** meta robots noindex + glava X-Robots-Tag v `.htaccess`\n"
                f"- **Oznaka:** trak »PREDLOG PRENOVE« na {len(strani)} HTML straneh\n"
                f"- **Datoteke:** {len(datoteke)} ({velikost / 1e6:.1f} MB)\n\n"
                + "\n".join(f"  - `{x}`" for x in datoteke) + "\n\n"
                "Objava: `deploy_preview.sh PROJEKT` (suhi zagon), prava objava samo z `--potrjeno` po odobritvi V2.\n")
    print(f"Izdaja: {izdaja}\nURL: {url}\nUporabnik: {uporabnik}  geslo: {geslo}\n"
          f"Datotek: {len(datoteke)} ({velikost / 1e6:.1f} MB) – povzetek v 06_predogled/povzetek.md")


if __name__ == "__main__":
    main()
