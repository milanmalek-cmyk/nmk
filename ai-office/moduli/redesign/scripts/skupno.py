"""Skupne nastavitve in pomočniki za skripte modula AI REDESIGN."""
import urllib.parse
import urllib.request

UA_MODUL = "Mozilla/5.0 (compatible; MultimedijaRedesign/1.0; +https://www.multimedija.net)"
UA_BRSKALNIK = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/129.0 Safari/537.36")


def ua(nacin):
    """Nekateri strežniki (npr. LiteSpeed z zaščito) zavrnejo neznan UA – takrat 'brskalnik'."""
    return UA_BRSKALNIK if nacin == "brskalnik" else UA_MODUL


def varen_url(url):
    """Zakodira presledke in šumnike v poti, ne da bi dvakrat kodiral že kodirano."""
    p = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(urllib.parse.unquote(p.path)), p.query, ""))


def odpri(url, nacin="modul", bajti=None, timeout=30):
    """urlopen z izbranim UA; `bajti` omeji prenos na začetek datoteke (HTTP Range)."""
    glave = {"User-Agent": ua(nacin), "Accept-Language": "sl,en;q=0.5"}
    if bajti:
        glave["Range"] = f"bytes=0-{bajti - 1}"
    return urllib.request.urlopen(urllib.request.Request(varen_url(url), headers=glave), timeout=timeout)
