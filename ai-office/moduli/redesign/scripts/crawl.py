#!/usr/bin/env python3
"""Pregled spletne strani: naslovi, meta, besedila, povezave in slike po straneh.

Uporaba:
  python3 -I crawl.py URL IZHODNA_MAPA [--max-strani 300] [--zamik 0.3] [--cache MAPA]

Izhod:  IZHODNA_MAPA/pages.json – en zapis na stran (glej `analiziraj`).
Pregleda samo isto domeno in isti jezik kot začetni URL (npr. /sl/), strani samo bere.
Z --cache se HTML shrani na disk in ob ponovnem zagonu ne prenaša znova.
"""
import argparse
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skupno import odpri  # noqa: E402
SLIKA = re.compile(r"\.(jpe?g|png|gif|webp|avif|svg|bmp|tiff?|ico)(\?.*)?$", re.I)
DOKUMENT = re.compile(r"\.(pdf|zip|rar|docx?|xlsx?|pptx?|mp4|mp3)(\?.*)?$", re.I)
PRESKOCI = re.compile(r"(format=feed|mailto:|tel:|javascript:|/wp-json/|/feed/?$|"
                      r"[?&](print|tmpl)=|/wp-admin|/administrator|/login|/cart|/kosarica)", re.I)
JEZIK = re.compile(r"^/([a-z]{2}(?:-[a-z]{2})?)(/|$)", re.I)

ATTR = re.compile(r'''\b(src|data-src|data-lazy-src|data-image|data-bg|data-thumb|poster)\s*=\s*["']([^"']+)["']''', re.I)
SRCSET = re.compile(r'''\b(?:data-)?srcset\s*=\s*["']([^"']+)["']''', re.I)
CSSURL = re.compile(r'''url\(\s*['"]?([^'")]+)['"]?\s*\)''', re.I)
HREF = re.compile(r'''<a\b[^>]*?\bhref\s*=\s*["']([^"']+)["']''', re.I)
IMG = re.compile(r"<img\b[^>]*>", re.I)


def prenesi(url, stanje):
    """Vrne (končni_url, status, content_type, telo). Ob 403 enkrat preklopi na brskalniški UA."""
    for _ in range(2):
        try:
            with odpri(url, stanje.get("ua", "modul")) as r:
                return r.geturl(), r.status, r.headers.get("Content-Type", ""), r.read()
        except urllib.error.HTTPError as e:
            if e.code == 403 and stanje.get("ua") != "brskalnik":
                stanje["ua"] = "brskalnik"
                print("  strežnik zavrača neznan UA – nadaljujem z brskalniškim", flush=True)
                continue
            return url, e.code, "", b""
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"  napaka: {url} ({e})", flush=True)
            return url, 599, "", b""
    return url, 403, "", b""


def normaliziraj(url, osnova, gostitelji):
    url = html.unescape(url.strip())
    if not url or url.startswith(("#", "data:")):
        return None
    u = urllib.parse.urlsplit(urllib.parse.urljoin(osnova, url))
    if u.scheme not in ("http", "https") or u.netloc.lower() not in gostitelji:
        return None
    pot = urllib.parse.unquote(u.path) or "/"
    kon = pot.endswith("/")
    pot = os.path.normpath(pot).replace("\\", "/")
    if kon and not pot.endswith("/"):
        pot += "/"
    return urllib.parse.urlunsplit(("https" if u.scheme == "https" else "http", gostitelji[0],
                                    urllib.parse.quote(pot), u.query, ""))


def kljuc_cache(url):
    """Ključ brez gostitelja, da www. in gola domena delita isti zapis."""
    p = urllib.parse.urlsplit(url)
    return hashlib.sha1(f"{p.path}?{p.query}".encode()).hexdigest() + ".html"


def besedilo(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", h)
    h = re.sub(r"(?s)<!--.*?-->", " ", h)
    h = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr)>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    vrstice = [re.sub(r"\s+", " ", v).strip() for v in t.splitlines()]
    return "\n".join(v for v in vrstice if v)


def oznake(h, tag):
    return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m))).strip()
            for m in re.findall(rf"(?is)<{tag}\b[^>]*>(.*?)</{tag}>", h)]


def meta_vse(h, ime):
    vrednosti = []
    for m in re.finditer(r"(?is)<meta\b[^>]*>", h):
        t = m.group(0)
        if re.search(rf'''(name|property)\s*=\s*["']{re.escape(ime)}["']''', t, re.I):
            c = re.search(r'''content\s*=\s*["']([^"']*)["']''', t, re.I)
            vrednosti.append(html.unescape(c.group(1)).strip() if c else "")
    return vrednosti


def meta(h, ime):
    v = meta_vse(h, ime)
    return v[0] if v else None


def analiziraj(url, koncni, h, gostitelji):
    """Izlušči podatke strani. Slike: atribut, iz katerega izvira, in alt (če je img)."""
    slike = {}

    def dodaj(raw, izvor, alt=None):
        cands = [normaliziraj(raw, koncni, gostitelji)]
        # relativna pot v data-* atributih se v JS pogosto razreši od korena, ne od strani
        if not raw.startswith(("/", "http", "//")):
            cands.append(normaliziraj("/" + raw, koncni, gostitelji))
        for i, u in enumerate(c for c in cands if c):
            if not SLIKA.search(urllib.parse.urlsplit(u).path):
                continue
            z = slike.setdefault(u, {"url": u, "izvor": set(), "alt": ""})
            z["izvor"].add(izvor + ("~koren" if i else ""))
            if alt and not z["alt"]:
                z["alt"] = alt

    for tag in IMG.findall(h):
        s = re.search(r'''\bsrc\s*=\s*["']([^"']+)["']''', tag, re.I)
        a = re.search(r'''\balt\s*=\s*["']([^"']*)["']''', tag, re.I)
        if s:
            dodaj(s.group(1), "img", html.unescape(a.group(1)).strip() if a else "")
    for atr, v in ATTR.findall(h):
        dodaj(v, atr.lower())
    for s in SRCSET.findall(h):
        for c in s.split(","):
            if c.strip():
                dodaj(c.strip().split(" ")[0], "srcset")
    for v in CSSURL.findall(h):
        dodaj(v, "css")
    for v in HREF.findall(h):
        if SLIKA.search(v.split("?")[0]):
            dodaj(v, "povezava")   # povezava na sliko je pogosto večja različica (lightbox)

    ld = re.findall(r'(?is)<script[^>]+application/ld\+json[^>]*>(.*?)</script>', h)
    tipi = sorted(set(re.findall(r'"@type"\s*:\s*"([^"]+)"', " ".join(ld))))
    lang = re.search(r'''<html\b[^>]*\blang\s*=\s*["']([^"']+)''', h, re.I)
    can = re.search(r'''<link\b[^>]*rel\s*=\s*["']canonical["'][^>]*href\s*=\s*["']([^"']+)''', h, re.I)
    t = besedilo(h[h.lower().find("<body"):] if "<body" in h.lower() else h)
    return {
        "url": url, "koncni_url": koncni,
        "title": (oznake(h, "title") or [""])[0],
        "description": meta(h, "description"),
        "robots": meta(h, "robots"),
        "viewport": meta_vse(h, "viewport"),   # več oznak: brskalnik upošteva zadnjo
        "og_image": meta(h, "og:image"),
        "lang": lang.group(1) if lang else None,
        "canonical": can.group(1) if can else None,
        "h1": oznake(h, "h1"), "h2": oznake(h, "h2"), "h3": oznake(h, "h3")[:30],
        "jsonld_tipi": tipi,
        "st_besed": len(t.split()),
        "besedilo": t[:15000],
        "slike": [dict(z, izvor=sorted(z["izvor"])) for z in slike.values()],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("izhod")
    ap.add_argument("--max-strani", type=int, default=300)
    ap.add_argument("--zamik", type=float, default=0.3, help="sekunde med zahtevami")
    ap.add_argument("--cache", help="mapa za shranjen HTML (ponovna raba)")
    a = ap.parse_args()

    os.makedirs(a.izhod, exist_ok=True)
    if a.cache:
        os.makedirs(a.cache, exist_ok=True)
    stanje = {}
    start = a.url
    koncni, status, _, _ = prenesi(start, stanje)
    if status >= 400:
        sys.exit(f"Začetni URL ni dosegljiv ({status}): {start}")
    gost = urllib.parse.urlsplit(koncni).netloc.lower()
    gola = gost[4:] if gost.startswith("www.") else gost
    gostitelji = (gost, gola, "www." + gola)
    jm = JEZIK.match(urllib.parse.urlsplit(koncni).path)
    jezik = jm.group(1).lower() if jm else None
    print(f"Domena: {gost}  jezik: {jezik or '-'}  UA: {stanje.get('ua', 'modul')}")

    vrsta, videno, strani = deque([normaliziraj(koncni, koncni, gostitelji)]), set(), []
    while vrsta and len(strani) < a.max_strani:
        url = vrsta.popleft()
        if url in videno:
            continue
        videno.add(url)
        pot_cache = os.path.join(a.cache, kljuc_cache(url)) if a.cache else None
        if pot_cache and os.path.exists(pot_cache):
            with open(pot_cache, encoding="utf-8", errors="replace") as f:
                prva, h = f.readline(), f.read()
            kon = prva[5:-5].strip() if prva.startswith("<!-- ") else url
            iz_cache = True
        else:
            kon, status, ctype, telo = prenesi(url, stanje)
            if status >= 400 or "html" not in ctype:
                continue
            h = telo.decode("utf-8", "replace")
            if pot_cache:
                with open(pot_cache, "w", encoding="utf-8") as f:
                    f.write(f"<!-- {kon} -->\n{h}")
            iz_cache = False
            time.sleep(a.zamik)
        kon = normaliziraj(kon, kon, gostitelji) or kon
        if kon != url and kon in videno:
            continue
        videno.add(kon)
        zapis = analiziraj(url, kon, h, gostitelji)
        strani.append(zapis)
        for v in HREF.findall(h):
            u = normaliziraj(v, kon, gostitelji)
            if not u or u in videno or PRESKOCI.search(u):
                continue
            pot = urllib.parse.urlsplit(u).path
            if SLIKA.search(pot) or DOKUMENT.search(pot):
                continue
            m = JEZIK.match(pot)
            if jezik and m and m.group(1).lower() != jezik:
                continue   # drug jezik
            vrsta.append(u)
        print(f"{len(strani):4d} {'C' if iz_cache else ' '} {kon}  slik: {len(zapis['slike'])}", flush=True)

    with open(os.path.join(a.izhod, "pages.json"), "w", encoding="utf-8") as f:
        json.dump({"zacetni_url": start, "domena": gost, "jezik": jezik,
                   "ua": stanje.get("ua", "modul"),
                   "datum": time.strftime("%Y-%m-%d"), "strani": strani}, f, ensure_ascii=False, indent=1)
    vse = {s["url"] for p in strani for s in p["slike"]}
    print(f"Strani: {len(strani)}  različnih slik: {len(vse)}  → {a.izhod}/pages.json")


if __name__ == "__main__":
    main()
