#!/usr/bin/env python3
"""Barve in pisave obstoječe strani (iz CSS) ter prevladujoče barve logotipa.

Uporaba:
  python3 -I brand.py URL_NASLOVNICE 01_analiza/brand.json [--logo pot/logotip.png] [--ua brskalnik]

Iz CSS datotek naslovnice (brez knjižnic, kot so Bootstrap, Font Awesome, animate)
prešteje barve skupaj s selektorji, kjer se pojavijo, in pobere pisave
(Google Fonts povezave in font-family). Logotip samo bere, nikoli ne spreminja.
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skupno import odpri  # noqa: E402

KNJIZNICE = re.compile(r"(bootstrap|font-?awesome|animate|owl\.|flickity|lightbox|nivo|hover\.css|uikit|"
                       r"slick|swiper|jquery|normalize|reset\.css|fontello|icons?\.css|/media/jui/)", re.I)
BARVA = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b|rgba?\([^)]*\)")


def preberi(url, ua):
    with odpri(url, ua) as r:
        return r.read().decode("utf-8", "replace")


def hex6(b):
    b = b.lower()
    if b.startswith("#") and len(b) == 4:
        return "#" + "".join(c * 2 for c in b[1:])
    if b.startswith("rgb"):
        n = [x.strip() for x in b[b.find("(") + 1:-1].split(",")]
        if len(n) == 4 and float(n[3]) < 0.5:
            return None   # skoraj prosojne barve niso del palete
        try:
            return "#%02x%02x%02x" % tuple(int(float(x)) for x in n[:3])
        except ValueError:
            return None
    return b


def barve_iz_css(css, vir, stevec, konteksti):
    css = re.sub(r"(?s)/\*.*?\*/|@(?:import|charset)[^;]*;", "", css)
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel = re.sub(r"\s+", " ", m.group(1)).strip()[:80]
        for b in BARVA.findall(m.group(2)):
            h = hex6(b)
            if h:
                stevec[h] += 1
                if len(konteksti[h]) < 4:
                    konteksti[h].append(f"{sel}  ({vir})")


def barve_logotipa(pot, n=6):
    from PIL import Image
    with Image.open(pot) as im:
        im = im.convert("RGBA")
        c = Counter(px[:3] for px in im.get_flattened_data() if px[3] == 255)
    skupaj = sum(c.values()) or 1
    return [{"hex": "#%02x%02x%02x" % k, "delez": round(v / skupaj, 3)} for k, v in c.most_common(n)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("izhod")
    ap.add_argument("--logo")
    ap.add_argument("--ua", default="modul", choices=["modul", "brskalnik"])
    a = ap.parse_args()

    h = preberi(a.url, a.ua)
    gost = urllib.parse.urlsplit(a.url).netloc.replace("www.", "")
    css_url, preskoceno = [], []
    for tag in re.findall(r"(?is)<link\b[^>]*>", h):
        if not re.search(r'''rel\s*=\s*["']?stylesheet''', tag, re.I):
            continue
        m = re.search(r'''href\s*=\s*["']([^"']+)''', tag, re.I)
        if not m:
            continue
        u = urllib.parse.urljoin(a.url, m.group(1).replace("&amp;", "&"))
        if gost not in urllib.parse.urlsplit(u).netloc:
            continue
        (preskoceno if KNJIZNICE.search(u) else css_url).append(u)

    stevec, konteksti = Counter(), defaultdict(list)
    for u in css_url:
        try:
            barve_iz_css(preberi(u, a.ua), os.path.basename(urllib.parse.urlsplit(u).path), stevec, konteksti)
        except OSError as e:
            print(f"  ne morem prebrati {u}: {e}", file=sys.stderr)
    for i, blok in enumerate(re.findall(r"(?is)<style\b[^>]*>(.*?)</style>", h)):
        barve_iz_css(blok, f"inline-{i + 1}", stevec, konteksti)
    for i, st in enumerate(re.findall(r'''style\s*=\s*["']([^"']*)["']''', h)):
        barve_iz_css("x{" + st + "}", "style-atribut", stevec, konteksti)

    google = sorted({urllib.parse.unquote(f).replace("+", " ")
                     for q in re.findall(r"fonts\.googleapis\.com/css2?\?([^\"' >]+)", h)
                     for f in re.findall(r"family=([^:&|]+)", q.replace("&amp;", "&"))})
    druzine = Counter()
    for u in css_url:
        try:
            for f in re.findall(r"font-family\s*:\s*([^;}]+)", preberi(u, a.ua)):
                druzine[f.split(",")[0].strip().strip("'\"")] += 1
        except OSError:
            pass

    izid = {
        "url": a.url,
        "css": css_url, "css_preskoceno_knjiznice": preskoceno,
        "barve": [{"hex": k, "st": v, "kje": konteksti[k]} for k, v in stevec.most_common(30)],
        "pisave_google": google,
        "pisave_css": [{"ime": k, "st": v} for k, v in druzine.most_common(10)],
        "logotip": {"pot": a.logo, "barve": barve_logotipa(a.logo)} if a.logo else None,
    }
    with open(a.izhod, "w", encoding="utf-8") as f:
        json.dump(izid, f, ensure_ascii=False, indent=1)
    print(f"CSS: {len(css_url)} (preskočenih knjižnic: {len(preskoceno)})  barv: {len(stevec)}  → {a.izhod}")
    for b in izid["barve"][:12]:
        print(f"  {b['hex']}  ×{b['st']:<3} {b['kje'][0] if b['kje'] else ''}")
    print("  pisave:", ", ".join(google) or "-", "|", ", ".join(d["ime"] for d in izid["pisave_css"][:5]))
    if izid["logotip"]:
        print("  logotip:", ", ".join(f"{b['hex']} ({b['delez']:.0%})" for b in izid["logotip"]["barve"][:4]))


if __name__ == "__main__":
    main()
