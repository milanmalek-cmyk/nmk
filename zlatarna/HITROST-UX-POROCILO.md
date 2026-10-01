# Revizija hitrosti, mobilne uporabnosti in dostopnosti: zlatarna-breznik.mmedija.com

**Datum:** 1. 10. 2026
**Testirana stran:** https://zlatarna-breznik.mmedija.com/ (razvojna, `noindex`; WordPress 7.1, hello-elementor-child, Elementor 4.3.3, WooCommerce v kataloškem načinu, LiteSpeed)
**Primerjava:** stara produkcija https://www.zlatarna-breznik.si/ (ThemeREX »frank-jewelry-store« + WPBakery + Revolution Slider)
**Način dela:** samo branje. Nobenega obrazca nisem oddal, se nikamor prijavil in ničesar spremenil. Edina interakcija s stanjem je bil klik na srce za priljubljene. To se zapiše le v `localStorage` testnega brskalnika in sem ga takoj počistil. Strežnik ne prejme ničesar.

---

## 0. Metodologija in omejitve (preberite najprej)

| Postavka | Vrednost |
|---|---|
| Lighthouse | 12.8.2 (privzeti mobilni profil s simuliranim omrežjem »slow 4G« in 4× upočasnitvijo CPU; namizno `--preset=desktop`) |
| Brskalnik | Chromium 141.0.7390.37 (headless) |
| Playwright | 1.56.1, širine 360, 375, 390 in 430 (DPR 3, `isMobile`, `hasTouch`) ter 1440 (DPR 1) |
| axe-core | različica, ki je priložena Lighthouse 12, pravila WCAG 2.0/2.1/2.2 A+AA in best-practice |
| Omrežje | ves promet gre skozi izhodni proxy. Ta doda TLS-rokovanje ~0,3–0,5 s na vsako novo povezavo, zato so **absolutni časi (zlasti TTFB, FCP, LCP) le okvirni in verjetno previsoki**. Relativne primerjave in strukturne ugotovitve so zanesljive. |
| TLS | Proxy ponovno podpiše promet. Chromium sem zagnal z `--ignore-certificate-errors-spki-list=<SPKI hash CA proxyja>`, kar pomeni, da zaupa **le** CA-ju proxyja. Splošnega `--ignore-certificate-errors` nisem uporabil. |
| Ponovljivost | Vsak URL je bil z Lighthouse izmerjen enkrat. Za `/`, `/porocni-prstani/` in `/katalog/` sem mobilni test ponovil, rezultata sta v tabeli 1b. Raztros je ±6–11 točk. |
| **/kontakt/** | Strežnik LiteSpeed na `/kontakt/` vsakemu »navadnemu« obiskovalcu najprej pokaže stran **»Bot Verification« (reCAPTCHA)**, v headless brskalniku celo slikovni izziv. **Meritve Lighthouse za /kontakt/ so zato NEVELJAVNE**, ker merijo stran za preverjanje. Vsebino strani Kontakt (obrazec, podatke, zemljevid, posnetke zaslona) sem pregledal z uporabniškim agentom Googlebot, ki ga LiteSpeed spusti mimo (glej težavo P0-1). |

Surovi podatki so v `perf/`: `lh/*.json` (Lighthouse), `lh2/*.json` (ponovitve), `pw-*.json` (Playwright/axe), `html/` (HTML in glave), `shots/` (posnetki).

---

## 1. Povzetek

### Ključne številke (mobilno, Lighthouse)

| | Stara produkcija | Nova dev stran |
|---|---|---|
| Domača stran: Performance | **56** | **77–83** |
| Domača stran: LCP | 6,3 s | 3,6–4,1 s |
| Domača stran: FCP | 5,8 s | 2,7 s |
| Domača stran: TBT | 153 ms | 0–2 ms |
| Domača stran: teža / zahtevki | 4.717 KB / 116 | 836 KB / 53 |
| /porocni-prstani/: Performance | **51** | **75–86** |
| /porocni-prstani/: CLS | **0,234** (slabo) | 0,000 |
| /porocni-prstani/: teža | 1.450 KB | 484 KB |

Nova stran je bistveno lažja in hitrejša od stare. Glavno nit izvajanja skoraj nič ne blokira (TBT ≈ 0, kar je dober posredni kazalnik za INP), CLS je povsod ≈ 0. Mobilni LCP pa je še vedno 3,5–4,9 s, na `/3902-2/` celo 6,8 s, cilj je < 2,5 s. Vzroki so:
(a) pozno odkrita CSS-ozadja v glavah podstrani,
(b) ni predpomnilnika strani (TTFB),
(c) 9–16 blokirajočih CSS/JS virov v `<head>`.

Dostopnost: 86–88 točk mobilno in 91–93 namizno (stara stran 86–87). SEO dosega 66 **izključno** zaradi `noindex` na razvojni strani, vse ostale SEO-presoje so uspešne. Best Practices: 100 na vseh pravih straneh.

### 15 najpomembnejših težav (po prioriteti)

| # | Prio | Težava | Kje |
|---|---|---|---|
| 1 | **P0** | Pred stranjo Kontakt se prikaže **LiteSpeed »Bot Verification« (reCAPTCHA)**. To je vmesna stran z ~830 KB Googlovih skript. V testu je zahtevala slikovni izziv, Lighthouse strani ni mogel izmeriti. Pravi Kontakt dobi brez izziva le UA Googlebot. | `/kontakt/` (tudi s poizvedbo `?x=1`) |
| 2 | P1 | LCP podstrani je **CSS-ozadje `ozadje-marmor-svetlo.jpg`** (82 KB JPG, 2048×768) v `section.zd-glava-strani`. Odkrije se šele po CSS in ni prednaloženo: »load delay« je 2,1–2,6 s mobilno, na /3902-2/ 4,8 s. | porocni, zarocni, katalog, cena, predstavitev, 3902-2 |
| 3 | P1 | **Ni predpomnilnika strani**: HTML nima `cache-control` ne `x-litespeed-cache`. HTML ima TTFB ~0,95 s, statična datoteka prek istega proxyja ~0,45–0,65 s, torej PHP potrebuje ~0,3–0,5 s. | vse strani |
| 4 | P1 | **9–16 render-blocking virov** v `<head>`: jQuery + jquery-migrate (strani Elementor), `cookie-notice/front.min.js`, 10+ ločenih CSS. Trustindex CSS je vključen dvakrat. LH ocenjuje prihranek 0,8–1,5 s mobilno. | vse strani |
| 5 | P1 | Mobilni gumb **menija (hamburger) nima dostopnega imena** (besedilo »Meni« ima `display:none`) in meri samo **22×13 px**. | `button.zd-glava__odpri` |
| 6 | P1 | **Tipkovnica v mobilnem meniju**: povezave so v DOM pred gumbom. Po odprtju gre Tab na vsebino *za* prekrivnim menijem, fokus se ne ujame. Ko je meni zaprt, je fokusabilna nevidna povezava »Svet prstanov«. | `nav#zd-meni`, `li#menu-item-4157` |
| 7 | P1 | **/3902-2/**: v vsebini je 5 slik **base64 (data:image/jpeg)**, zato ima HTML 569 KB prenosa (798 KB). Mobilno: Perf 64, FCP 4,8 s, LCP 6,8 s. Slike nimajo `width/height`. (Slug `3902-2` po navodilih naročnika ostane.) | `/3902-2/` |
| 8 | P1 | **Kontrast zlate barve**: `#a07d45` na beli 3,8:1, `#a8844e` 3,45:1, bel tekst na zlatih gumbih 3,45–3,8:1 (zahteva 4,5:1 za 12–13 px). Primeri: 24× »POGLEJ« na vsakem arhivu, »NAŠA IZBIRA«, »OGLED KOLEKCIJE«, »Pošlji sporočilo« … | vse strani |
| 9 | P1 | Na **Kontaktu ni vidnega delovnega časa**. Je le v JSON-LD (pon–pet 8–12 in 14–17). Stara stran ga je prikazovala, skupaj s »Sobota po dogovoru«. Obvezna polja obrazca niso vidno označena, ob obrazcu ni obvestila o zasebnosti. | `/kontakt/` |
| 10 | P2 | **Piškotna pasica** prekrije 25 % mobilnega zaslona (208 px pri 390×844) in **zakrije fokusirane elemente** (WCAG 2.4.11). Ima angleški `aria-label="Cookie Compliance"`. | `#cookie-notice` |
| 11 | P2 | **Srca (priljubljeni)** na karticah domače strani merijo 19×19 px, v glavi 21×21 px (pod 24 px). Na karticah kataloga/arhivov (`li.zd-izdelek-k`) srca sploh ni. Števec v glavi ni del dostopnega imena. | `button.zd-srce` |
| 12 | P2 | **Zlepljene besede v `textContent`** naslovov (`<span class="zd-n__a">…</span><span class="zd-n__b">…</span>` brez presledka), npr. »Poročni prstani,ki …«, »Izbrani prstaniiz naše delavnice«, »147Porocna prstana«, »Ročno.Z ljubeznijo.Za vedno.«. Na zaslonu so ločene vrstice. | vse strani |
| 13 | P2 | **Google Maps iframe** na Kontaktu ima `loading="lazy"`, a ga Chrome naloži že ob nalaganju strani (~470 KB, po drsenju ~630 KB), še pred privolitvijo v piškotke. | `/kontakt/` |
| 14 | P2 | **Slike**: ozadja kolekcij na domači so polne JPG (1672×941; 127 KB in 89 KB), logotip je PNG, starejši izdelki so JPG, slike na predstavitvi so prevelike (768×768 prikazane ~228 px). Na domači se 5 slik izven zaslona naloži takoj. | domača, predstavitev, cena, izdelki |
| 15 | P2 | **Trustindex** se naloži takoj ob odprtju domače (9 zahtev, 97 KB; `loader.js` brez cache glave). Vtičnik je do izvedbe zunanjega JS nevidni (`opacity:0;height:0`). | `/` (#mnenja) |

Dodatno (P2–P3): povezava »Preskoči na vsebino« ob fokusu ostane nevidna (`top:-170000px`), statični viri imajo predpomnilnik le 7 dni, `latin-ext` pisave (č/š/ž) niso prednaložene, ime izdelka je brez »č« (»147-porocna prstana«), na arhivih manjkajo orientirji (`region`), `aria-label` video fasade se ne ujema z vidnim besedilom, na /3902-2/ je preskočen nivo naslova.

---

## 2. Lighthouse po URL-jih

### 1a. Vsi rezultati (enkratni zagon)

`*TTFB` vključuje zakasnitev proxyja. ⚠ = izmerjena je bila stran »Bot Verification«, ne Kontakt.

| URL | Način | Perf | LCP (s) | FCP (s) | TBT (ms) | CLS | SI (s) | Teža (KB) | Zahtev | TTFB* (ms) | A11y | BP | SEO |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| / | mobilno | **77** | 4.1 | 2.7 | 2 | 0.000 | 6.3 | 836 | 53 | 790 | 87 | 100 | 66 |
| / | namizno | **89** | 1.4 | 1.1 | 0 | 0.000 | 2.2 | 1004 | 61 | 807 | 93 | 100 | 66 |
| /porocni-prstani/ | mobilno | **75** | 4.9 | 2.7 | 0 | 0.000 | 4.8 | 484 | 28 | 804 | 87 | 100 | 66 |
| /porocni-prstani/ | namizno | **93** | 1.4 | 0.8 | 0 | 0.001 | 1.7 | 784 | 46 | 715 | 93 | 100 | 66 |
| /zarocni-prstani/ | mobilno | **78** | 4.6 | 2.4 | 0 | 0.000 | 4.7 | 373 | 25 | 723 | 87 | 100 | 66 |
| /zarocni-prstani/ | namizno | **85** | 2.0 | 1.1 | 0 | 0.001 | 2.0 | 701 | 46 | 683 | 93 | 100 | 66 |
| /katalog/ | mobilno | **82** | 4.1 | 2.1 | 0 | 0.000 | 4.6 | 419 | 27 | 850 | 87 | 100 | 66 |
| /katalog/ | namizno | **94** | 1.3 | 0.7 | 0 | 0.000 | 1.8 | 534 | 38 | 882 | 92 | 100 | 66 |
| /kontakt/ ⚠ | mobilno | (88) | (1.1) | (1.1) | (319) | (0.004) | (5.4) | (834) | (20) | (400) | (90) | (75) | (91) |
| /kontakt/ ⚠ | namizno | (95) | (0.6) | (0.6) | (48) | (0.020) | (2.3) | (855) | (20) | (377) | (90) | (74) | (91) |
| /predstavitev-podjetja/ | mobilno | **76** | 4.8 | 2.5 | 0 | 0.000 | 4.9 | 469 | 43 | 841 | 87 | 100 | 66 |
| /predstavitev-podjetja/ | namizno | **89** | 1.6 | 0.9 | 0 | 0.001 | 2.1 | 727 | 50 | 853 | 92 | 100 | 66 |
| /cena-porocnih-prstanov/ | mobilno | **81** | 4.4 | 2.1 | 0 | 0.000 | 4.0 | 390 | 24 | 671 | 87 | 100 | 66 |
| /cena-porocnih-prstanov/ | namizno | **94** | 1.3 | 0.8 | 0 | 0.000 | 1.7 | 537 | 27 | 821 | 93 | 100 | 66 |
| /147-porocna-prstana/ (izdelek) | mobilno | **86** | 3.5 | 2.3 | 0 | 0.000 | 4.3 | 409 | 32 | 711 | 88 | 100 | 66 |
| /147-porocna-prstana/ (izdelek) | namizno | **92** | 1.4 | 0.9 | 0 | 0.000 | 1.8 | 502 | 37 | 700 | 93 | 100 | 66 |
| /3902-2/ | mobilno | **64** | 6.8 | 4.8 | 0 | 0.000 | 5.3 | 929 | 28 | 755 | 86 | 100 | 66 |
| /3902-2/ | namizno | **86** | 1.8 | 1.2 | 0 | 0.001 | 2.0 | 1067 | 31 | 832 | 91 | 100 | 66 |

### 1b. Ponovitev mobilnega zagona (raztros)

| URL | 1. zagon Perf / LCP | 2. zagon Perf / LCP |
|---|---|---|
| / | 77 / 4,06 s | 83 / 3,56 s |
| /porocni-prstani/ | 75 / 4,85 s | 86 / 3,85 s |
| /katalog/ | 82 / 4,08 s | 82 / 4,35 s |

### 1c. Pred in po: stara produkcija proti novi strani (mobilno)

| URL | Stara: Perf / LCP / FCP / TBT / CLS / KB / zahtev | Nova: Perf / LCP / FCP / TBT / CLS / KB / zahtev |
|---|---|---|
| / | 56 / 6,3 s / 5,8 s / 153 ms / 0,027 / 4.717 KB / 116 | 77 / 4,1 s / 2,7 s / 2 ms / 0,000 / 836 KB / 53 |
| /porocni-prstani/ | 51 / 5,2 s / 5,1 s / 103 ms / **0,234** / 1.450 KB / 76 | 75 / 4,9 s / 2,7 s / 0 ms / 0,000 / 484 KB / 28 |

Glavni viri teže na stari strani:
- YouTube iframe ob nalaganju (1.035 KB),
- `guess-nakit.png` (2.018 KB),
- Google Fonts (183–218 KB),
- GTM/GA, dva taga (~293 KB),
- Revolution Slider (rs6 101 KB),
- fontello/trx ikone (256 KB neuporabljenega CSS).

Stara stran je imela tudi 27 blokirajočih virov in a11y napake `meta-viewport`, `link-name` ×4 ter `heading-order`, ki jih nova stran nima.

---

## 3. LCP: element, faze in nalaganje

Faze LCP so iz mobilnega zagona Lighthouse: TTFB / zakasnitev nalaganja / čas nalaganja / zakasnitev izrisa, v ms.

| URL | LCP element (mobilno) | Vir | Lazy? | fetchpriority / preload | Faze (ms) |
|---|---|---|---|---|---|
| / | `section.elementor-element-d9a9400.zd-junak` (CSS ozadje) | `/wp-content/uploads/2026/10/porocna-prstana-na-marmorju-zlatarna-breznik.webp` (59 KB, 2048×768) | ne | ✅ `<link rel="preload" as="image" fetchpriority="high">` | 963 / 513 / 1919 / 661 |
| /porocni-prstani/ | `body > section.zd-glava-strani` (CSS ozadje) | `/wp-content/uploads/2026/09/ozadje-marmor-svetlo.jpg` (82 KB JPG, 2048×768) | ne | ❌ ni preloada | 955 / **2179** / 1686 / 31 |
| /zarocni-prstani/ | isto | isto | ne | ❌ | 851 / **2249** / 1473 / 31 |
| /katalog/ | isto | isto | ne | ❌ | 1144 / **2128** / 747 / 63 |
| /predstavitev-podjetja/ | `section.elementor-element-879243e.zd-glava-strani` | isto | ne | ❌ | 1006 / **2598** / 1130 / 33 |
| /cena-porocnih-prstanov/ | `section.zd-glava-strani` | isto | ne | ❌ | 761 / **2524** / 981 / 97 |
| /147-porocna-prstana/ | `div.zd-izdelek__slika > img.attachment-large` | `147-porocna-prstana-768x591.jpg` (JPG) | ne (`loading="eager"`) | ✅ `fetchpriority="high"` | 762 / 540 / 2153 / 22 |
| /3902-2/ | `section.zd-glava-strani` | `ozadje-marmor-svetlo.jpg` | ne | ❌ | 815 / **4840** / 1042 / 112 |

Ugotovitve:
- Na nobeni strani LCP ni lazy-loaded. Presoja `lcp-lazy-loaded` je povsod uspešna.
- Domača stran je dobro nastavljena (preload + `fetchpriority=high`). Isto sliko pa vleče tudi logotip `zlatarna-breznik-logotip-2026.png` s `fetchpriority="high"`, zato logotip tekmuje s heroem. Logotip naj ima `fetchpriority` privzeto ali `low`.
- Na vseh podstraneh je LCP enako marmorno ozadje iz `dizajn.css`: `.zd-glava-strani { background: #f6f1e9 url("../../../uploads/2026/09/ozadje-marmor-svetlo.jpg") … }`. Brskalnik ga odkrije šele po prenosu in razčlenitvi CSS, zato je največji posamezni zaviralec mobilnega LCP. LH `prioritize-lcp-image` ima oceno 0,5.
- Rešitev brez vizualne spremembe:
  1. dodajte `<link rel="preload" as="image" href="…/ozadje-marmor-svetlo.webp" fetchpriority="high">` na vseh straneh z `zd-glava-strani`;
  2. pretvorite ga v WebP/AVIF (LH ocenjuje prihranek ~43 KB);
  3. za mobilne naprave pripravite manjšo različico (npr. 1024 px) z `image-set()` ali medijsko poizvedbo.
- Na izdelku je LCP slika še JPG. Na DPR 3 (390 px) brskalnik izbere `…-1200x923.jpg` (~100 KB). Pretvorba v WebP bi skrajšala »load time« 2,1 s.

---

## 4. Blokirajoči viri, CSS in JS

Blokirajoči viri v `<head>` (mobilno): **16** na domači in predstavitvi, **13** na izdelku, **9** na arhivih in vsebinskih straneh. LH ocenjuje prihranek 0,84–1,52 s mobilno in 0,25–0,69 s namizno.

| Vir | Velikost (prenos) | Opomba |
|---|---|---|
| `/wp-includes/js/jquery/jquery.min.js?ver=3.7.1` | 29 KB | Blokira v `<head>` na straneh Elementor (/, predstavitev, izdelek). Na izdelku LH navaja 20 KB neuporabljenega. |
| `/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1` | 5 KB | Verjetno nepotreben |
| `/wp-content/plugins/cookie-notice/js/front.min.js?ver=3.1.12` | 2–3 KB | Blokira na **vseh** straneh |
| `/wp-content/plugins/cookie-notice/css/front.min.css` | 2 KB | |
| `/wp-content/themes/hello-elementor/assets/css/reset.css` | 2 KB | |
| `/wp-content/plugins/elementor/assets/css/frontend.min.css` | 7 KB | |
| `/wp-content/uploads/elementor/css/post-4050.css`, `post-4.css`, `base-desktop.css`, `base-mobile.css` | ~1 KB vsak | 4 drobne zahteve |
| `/wp-content/plugins/elementor/assets/css/widget-heading.min.css`, `widget-image.min.css` | ~1 KB vsak | |
| `/wp-content/themes/hello-elementor-child/assets/fonts/pisave.css` + `pisave-2026.css` | ~1 KB vsak | Samo `@font-face`. Lahko se vključita inline. |
| `/wp-content/themes/hello-elementor-child/assets/zb.css` | 9 KB (43 KB nestisnjeno) | Stari slog. Preverite, ali je še potreben poleg `dizajn.css`. |
| `/wp-content/themes/hello-elementor-child/assets/dizajn.css` | 13 KB (67 KB nestisnjeno) | Na /cena/ in /3902-2/ je ~10 KB neuporabljenega |
| `/wp-content/uploads/trustindex-google-widget.css` | 9 KB | **Dvakrat**: v `<head>` in še enkrat inline v `#mnenja` |

Neuporabljen JS/CSS je zanemarljiv (le jQuery na izdelku in `dizajn.css` na dveh straneh). Glavna nit je skoraj prosta: bootup ≤ 0,96 s mobilno, TBT 0–2 ms.

Priporočila brez vpliva na videz:
- V LiteSpeed Cache vklopite »JS Defer« za jQuery in cookie-notice (ali pa v nastavitvah Cookie Notice »Script placement: Footer«).
- Odstranite `jquery-migrate`. Preverite Elementor »Optimized asset loading / Load JS in footer«.
- Združite drobne CSS datoteke (CSS Combine) ali uporabite »UCSS/Critical CSS« v LSCache.
- `@font-face` iz `pisave*.css` vključite inline v `<head>`.
- Odstranite podvojeni Trustindex `<link>`.

---

## 5. Zunanje storitve (Trustindex, YouTube, Google Maps, reCAPTCHA, GA)

Bajti so izmerjeni s Playwright (390 px, brez predpomnilnika) in vključujejo tudi zahteve iz iframov.

| Storitev | Kje | Kako se naloži | Zahtevki / bajti | iframe ob nalaganju? |
|---|---|---|---|---|
| **Trustindex** (Google mnenja) | samo `/` (`section#mnenja` → `div.zd-google--vticnik > pre.ti-widget`) | **Takoj**: `<script async src="https://cdn.trustindex.io/loader.js">`. HTML vtičnika je strežniško izrisan, a skrit (`opacity:0;height:0`), dokler `loader.js` ne zažene. | Ob nalaganju **9 zahtev / 97 KB**: `loader.js` 25 KB brez `cache-control`, 4× Poppins woff2 ~30 KB, `icon.svg` 37 KB, zvezdice in logotip. Ob drsenju še 3 avatarji (`lh3.googleusercontent.com`, ~20 KB) in 1 svg. | ne |
| **YouTube** | `/` in `/predstavitev-podjetja/` | ✅ **Fasada na klik**: `a.zd-video[data-zd-video]` z lokalno sliko. Šele klik doda `<iframe src="https://www.youtube-nocookie.com/embed/…?autoplay=1">`. | Pred klikom **0 B**. Po kliku ~**1,1 MB** (youtube-nocookie ~1.024 KB / 16 zahtev + fonts.gstatic 58 KB + ytimg 15 KB …). | ne (šele po kliku) |
| **Google Maps** | samo `/kontakt/` (`section.zd-zemljevid iframe`) | `<iframe loading="lazy" src="https://maps.google.com/maps?q=…&output=embed">` je v HTML. Pri 390×844 ga Chrome **naloži že ob nalaganju strani**, ker je znotraj praga za lazy-load. | Ob nalaganju ~**468 KB** (maps.googleapis 391 KB, maps.gstatic 75 KB …). Po drsenju še ~159 KB (fonts.gstatic 90 KB, google.com 48 KB …), skupaj ~**627 KB**. | **da**, 1 iframe |
| Povezave na Google Maps | noga in podatki na vseh straneh | Le `<a href="https://www.google.com/maps/search/?api=1&query=…">` | 0 B | ne |
| **LiteSpeed reCAPTCHA** | `/kontakt/` pred pravo stranjo | Vmesna stran »Bot Verification« (`recaptcha.net/api.js` + gstatic) | ~**830 KB** (LH: Google CDN 736 KB, reCAPTCHA 60 KB, Roboto 35 KB). TBT 319 ms mobilno. | da (reCAPTCHA) |
| Google Analytics (G-L0M9SC4KZ6) | vse | ✅ Šele **po privolitvi** (`script#zb-analitika` posluša `setCookieNotice`). Pred privolitvijo ni nobene GA zahteve. | 0 B pred privolitvijo | ne |
| Google Fonts | – | ✅ Ni uporabljen. Vse pisave so lokalne. | 0 | – |

Priporočila:
- Trustindex: `loader.js` vstavite šele, ko se `#mnenja` približa pogledu (IntersectionObserver, `rootMargin: 600px`), ali vklopite »delay JS« v LSCache. Ohranite strežniški HTML, a ga ne skrivajte z `opacity:0;height:0` (v CSS nastavite le `min-height`). Tako ostanejo mnenja vidna tudi brez zunanjega JS in CLS ostane 0.
- Google Maps: uporabite enako fasado kot za YouTube (statična slika zemljevida + gumb »Prikaži zemljevid« / »Odpri v Google Zemljevidih«). To prihrani ~470–630 KB in odpravi Googlove piškotke pred privolitvijo (GDPR).
- YouTube fasada je dobro narejena. Popravita naj se le `aria-label` (glej §9) in fiksni `iframe.title` v `dizajn.js` (vsi videi imajo naslov »Ročna izdelava prstana v zlatarni Brežnik«).

---

## 6. Pisave

| Lastnost | Stanje |
|---|---|
| Vir | ✅ Vse lokalne (`/wp-content/themes/hello-elementor-child/assets/fonts/*.woff2`). Google Fonts ni. |
| Format | ✅ woff2, razdeljen po `unicode-range` (`latin` + `latin-ext`) |
| `font-display` | ✅ `swap` v vseh `@font-face` (`pisave.css`, `pisave-2026.css`). Presoja LH `font-display` je povsod uspešna. |
| Preload | `jost-latin.woff2`, `cinzel-400-600-latin.woff2`, `sorts-mill-goudy-400-italic-latin.woff2` (3 datoteke, `crossorigin` ✓) |
| Naložene na `/` (390 px) | jost-latin 26 KB, cinzel-latin 26 KB, goudy-italic-latin 25 KB (prednaložene, ~1,2 s); **jost-latin-ext 17 KB, cinzel-latin-ext 15 KB, goudy-italic-latin-ext 11 KB, goudy-latin 23 KB** (odkrite šele ~2,5 s). Skupaj ~143 KB. Trustindex doda še 4× svoj Poppins (~30 KB, cdn.trustindex.io). |
| Na /kontakt/ | dodatno `parisienne-400-latin` 22 KB + `-latin-ext` 14 KB in goudy normal latin-ext 10 KB |
| Deklarirane, a ne prenesene | Playfair Display, Poppins (lokalni), Parisienne (razen na Kontaktu). Ne stanejo nič, `pisave.css` pa je še vedno ločena blokirajoča zahteva. |

Ugotovitev: slovensko besedilo vsebuje č/š/ž, ki so v `latin-ext`. Te datoteke **niso prednaložene**, zato se znaki č/š/ž v naslovih (Cinzel) in besedilu (Jost) za kratek čas izrišejo z nadomestno pisavo, nato se zamenjajo. To je viden »preklop« v besedah, kot sta »Poročni« in »Žalec«.

Priporočilo: prednaložite tudi `jost-latin-ext.woff2` in `cinzel-400-600-latin-ext.woff2`, ali pa za vsako družino pripravite eno združeno datoteko latin+latin-ext. `goudy-400-latin` (navaden rez) je prav tako na prvem zaslonu.

---

## 7. Slike

### Domača stran (390 px in 1440 px)

| Slika | Format | width/height | loading | fetchpriority | srcset/sizes | alt | Opomba |
|---|---|---|---|---|---|---|---|
| Hero: CSS ozadje `porocna-prstana-na-marmorju-zlatarna-breznik.webp` | webp, 2048×768 | – (CSS) | – | preload high ✅ | ena velikost za vse naprave | – | **LCP**, ni lazy ✅ |
| Logotip v glavi `zlatarna-breznik-logotip-2026.png` | **PNG** 143×137, 13 KB | ✅ 143×137 | eager | **high** | ne | »Zlatarna Brežnik, Žalec« | `fetchpriority=high` tekmuje s heroem. Bolje SVG/WebP (LH: −11 KB). |
| Ozadje kartice `.zd-kolekcija--porocni` `porocna-prstana-rumeno-zlato-kovana.jpg` | **JPG** 1672×941, **127 KB** | – (CSS) | – | – | ne | – | LH: −59 KB z WebP, ista datoteka za mobilne naprave |
| Ozadje kartice `.zd-kolekcija--zarocni` `zarocni-prstan-rumeno-zlato-briljant.jpg` | **JPG**, 89 KB | – | – | – | ne | – | LH: −45 KB |
| 9× kartica izdelka (`ul.zd-kartice img`) | 7× webp, 2× jpg (`433-…jpg`, `065-600x600.jpg`, `410-413-…-600x575.jpg`) | ✅ | lazy ✅ | – | ✅ `sizes="auto, (max-width: 600px) 100vw, 600px"` (`410-413` **brez srcset**) | ✅ ime izdelka | |
| `a.zd-video > img` `rocna-izdelava-prstana-delavnica-*.jpg` | JPG | ✅ 800×419 | **ni lazy** | – | ✅ | »Ročna izdelava prstana« | Izven zaslona, a se naloži takoj (27–40 KB) |
| `skica-zarocnega-prstana-768x702.jpg` | JPG | ✅ | **ni lazy** | – | ✅ | prazen (dekor) | Izven zaslona. Namizno prikazana 228×228 px, LH: −38 KB. |
| Trustindex zvezdice, logotip, avatarji | svg / jpg | ✅ / avatarji **brez** | lazy | – | – | »Google star 1…5« | alt zvezdic je šum za bralnike zaslona |
| `guess-nakit-novo-v-ponudbi-*.jpg` (pasica) | JPG | ✅ 2560×898 | **ni lazy** | – | ✅ | ✅ opisen | Izven zaslona. Na 360 px je besedilo v sliki neberljivo. |
| 3× članek `clanek-*.jpg` | JPG | ✅ | lazy ✅ | – | ne | prazen | Znotraj povezave z naslovom, zato sprejemljivo |
| Logotip v nogi, `noga-cvetje.jpg` | PNG / JPG | ✅ | **ni lazy** | – | – | – / prazen | Izven zaslona |

### Katalog `/katalog/`

| Slika | Format | width/height | loading | srcset/sizes | alt | Opomba |
|---|---|---|---|---|---|---|
| LCP: CSS ozadje `ozadje-marmor-svetlo.jpg` | **JPG** 82 KB | – | – | ne | – | ni preloada (§3) |
| 12 kartic »poročni« 2025 | **webp** ✅ | ✅ 600×462 | lazy | ✅ `sizes="auto, …"` | ✅ | **Prva kartica je pri 390 px v prvem zaslonu, a ima `loading="lazy"`.** Prva 1–2 kartici naj bosta `eager`. |
| 12 kartic »zaročni« 2024 (`44x-scaled-600x400.jpg`) | **JPG** | ✅ 600×400 | lazy | ✅ | ✅ | Pretvorba v WebP prihrani ~12–16 KB na sliko |

Stanje: vse vsebinske slike imajo `width`/`height` (razen 5 base64 slik na /3902-2/) in `alt`, lazy-load je pravilen za kartice. Možne izboljšave:
- pretvorba vseh JPG/PNG v WebP/AVIF (LiteSpeed Image Optimization),
- `loading="lazy"` za vse slike pod prvim zaslonom,
- manjše različice CSS-ozadij za mobilne naprave,
- popravek prevelikih slik na predstavitvi: `rocna-izdelava-zarocnega-prstana-768x768.jpg`, `skica-oblikovanje-prstanov-768x768.jpg`, `zarocni-prstan-rumeno-zlato-koncni-768x768.jpg`, `skica-ideja-in-navdih-768x768.jpg` (LH: skupaj ~180 KB odvečnih),
- `/cena-porocnih-prstanov/` namizno: `porocni-prstan-strosek.jpg` (121 KB, polna velikost, −52 KB).

---

## 8. Odzivne glave (HTTP)

| Vir | cache-control | expires | content-encoding | x-litespeed-cache |
|---|---|---|---|---|
| HTML `/` (in vse strani) | **ni** | **ni** | `br` ✅ | **ni** (stran ni v predpomnilniku) |
| HTML `/kontakt/` (navaden UA) | `no-cache,no-store,private` | – | gzip | – (stran »Bot Verification«) |
| CSS `dizajn.css?ver=…` | `public, max-age=604800` (7 dni) | +7 dni | `br` ✅ | – |
| JS `jquery.min.js?ver=3.7.1`, `elementor/…/frontend.min.js?ver=4.3.3` | `public, max-age=604800` | +7 dni | `br` ✅ | – |
| Slika `…/porocna-prstana-na-marmorju-zlatarna-breznik.webp` | `public, max-age=604800` | +7 dni | – (ni potrebno) | – |
| Slika `ozadje-marmor-svetlo.jpg` | `public, max-age=604800` | +7 dni | – | – |
| Pisava `jost-latin.woff2` | `public, max-age=604800` | +7 dni | – (woff2 je že stisnjen) | – |
| 3P `cdn.trustindex.io/loader.js` | **ni** | – | gzip | – |
| `/favicon.ico` | 404 | – | – | (ikona je sicer v `<link rel="icon">`) |

TTFB (curl prek proxyja, 4 ponovitve):
- HTML `/porocni-prstani/`: **0,94–1,02 s**
- statični CSS: 0,44–0,67 s
- `robots.txt`: 0,43–0,61 s

Razlika ~0,3–0,5 s je čas, ki ga PHP/WordPress porabi za izdelavo strani. Predpomnilnik strani tega trenutno ne pokriva.

Priporočila:
- Pred zagonom v LSCache vklopite **predpomnilnik strani** (glava `x-litespeed-cache: hit`).
- Za vire z `?ver=` in za `uploads` nastavite `max-age=31536000` (1 leto), po možnosti z `immutable`. Lighthouse sicer 7 dni sprejme, a povratni obiskovalci po tednu dni znova prenesejo vse.
- Na HTML manjkajo varnostne glave (`Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy`). To ni del te naloge, a jih je smiselno dodati ob zagonu.

---

## 9. Dostopnost (Lighthouse + axe-core)

### Neuspešne presoje

| Presoja | Strani | Element / podrobnosti |
|---|---|---|
| **button-name** (kritično) | vse, mobilno (< 1240 px) | `header.zd-glava > div.zd-glava__v > div.zd-glava__desno > button.zd-glava__odpri`. Besedilo `span.zd-glava__odpri-besedilo` ima v `dizajn.css` `display:none`, zato gumb nima imena. |
| **color-contrast** | vse | Glej tabelo spodaj |
| **target-size** (WCAG 2.5.8) | vse | `button.zd-srce` na karticah **19×19 px** (domača); povezavi s telefonskima številkama v nogi `.zd-noga__telefoni > a` 143×23 px, premalo razmika |
| **label-content-name-mismatch** | `/`, `/predstavitev-podjetja/` | `a.zd-video` ima `aria-label="Predvajaj video: ročna izdelava prstana"`, vidno besedilo pa je »OGLEJTE SI FILM« (WCAG 2.5.3) |
| **heading-order** | `/3902-2/` | `main#content > div.zd-besedilo__v > h3` »Pomembne ugotovitve:« preskoči nivo |
| **region** (axe) | arhivi: porocni, zarocni, katalog | `body > section.zd-glava-strani` (H1 in uvod) je **zunaj `<main>`**. Prestavite ga v `main#content` ali dodajte `role="region"`/`<header>`. |

### Kontrast (izračun WCAG)

| Barve | Razmerje | Kje (primeri) | Najmanjši popravek do 4,5:1 |
|---|---|---|---|
| `#a07d45` na `#ffffff`, 12 px | **3,8:1** | `span.zd-izdelek-k__poglej` »POGLEJ« (24× na vsakem arhivu); »ZANIMIVOSTI«; `p.zd-nad` »MODEL 147«; drobtine na izdelku; »Zlatarna Brežnik« na Kontaktu; povezave v besedilu 18 px na /cena/ in /3902-2/ | `#90703e` (4,59:1), skoraj neopazna razlika |
| `#a8844e` na `#ffffff`, 12 px | **3,45:1** | »NAŠA IZBIRA« | `#90703e` |
| `#ffffff` na `#a07d45`, 13 px | **3,8:1** | gumbi »OGLED KOLEKCIJE«, `a.zd-gumb` »POŠLJITE POVPRAŠEVANJE«, `button.wpcf7-submit` »Pošlji sporočilo« | ozadje `#90703e` ali temno besedilo `#1a1612` (4,7:1) |
| `#ffffff` na `#a8844e`, 13 px | **3,45:1** | »VEČ O NAŠI IZDELAVI«, en »OGLED KOLEKCIJE« | isto |
| `#a07d45` na `#f5ede0` / `#f6f1e9` | 3,28 / 3,39:1 | »OD IDEJE DO PRSTANA« (predstavitev) | `#836739` |
| `#f1e7d6`, `#d9b77a`, `#cfae74` »na beli« | 1,2–2,1:1 | `/predstavitev-podjetja/` sekcija »Ustvarimo vajina prstana skupaj« | **Lažni pozitiv.** Ozadje je temni `radial-gradient(#241d16 → #14110e)`, ki ga axe ne zna oceniti. Posnetek: `shots/predstavitev-m390-poziv.png` |

### Vidnost fokusa (Tab čez prvih 18 elementov na `/`)

- **Fokus ima obrobo pri vseh 18 korakih**, na 1440 px in na 390 px. Povezave imajo `outline: 2px solid #a07d45; outline-offset: 3px`, gumbi (srca, meni) 1 px obrobo. Posnetki: `shots/focus-*.png`.
- Prvi Tab doseže »Preskoči na vsebino« (`a.skip-link.screen-reader-text`), **a povezava ob fokusu ostane nevidna**. Izmerjeno ob fokusu: `position:absolute; top:-170000px; clip:rect(0,0,0,0); 1×1 px` (`shots/skiplink-d1440-focus.png`). Pravilo `.screen-reader-text:focus` iz teme se ne uporabi. Popravek: `.skip-link:focus { position:fixed; top:8px; left:8px; width:auto; height:auto; clip:auto; z-index:100000; padding:12px 16px; background:#fff; color:#1a1612; }` (WCAG 2.4.7). Videz strani se ne spremeni, ker se povezava pokaže le ob fokusu s tipkovnico.
- **Težava A, zakrit fokus (WCAG 2.4.11):** dokler je odprta piškotna pasica (390 px: 208 px = 25 % višine, 1440 px: 77 px), fokusirani elementi pristanejo *pod* pasico. Primeri: »Ogled kolekcije« pri y=765 in srca kartic pri y=732–791 (390×844), srce pri y=820 (1440×900). Posnetka `focus-m390-09.png` in `focus-d1440-14.png` pokažeta samo temno pasico.
- **Težava B, nevidna fokusna točka:** pri zaprtem mobilnem meniju je fokusabilna povezava **»Svet prstanov«** (`li#menu-item-4157 > a`, podmeni »Kontakt«). `nav#zd-meni` ima `visibility:hidden; opacity:0`, `ul.sub-menu` pa eksplicitno `visibility:visible`. Fokus izgine na točko (36, 395) sredi heroja (`focus-m390-02.png`). Popravek: `.zd-glava:not(.je-odprt) .zd-meni .sub-menu { visibility: hidden; }` ali `inert` na zaprtem `nav`.
- **Težava C, polja obrazca:** `.zd-kontakt__obrazec .wpcf7 :is(input,select,textarea):focus { outline: none; border-color: var(--zd-zlato); }`. Fokus je le sprememba barve 1-px obrobe, kar je šibak indikator. Dodajte npr. `outline: 2px solid #90703e; outline-offset: 2px`.

### Primerjava s staro stranjo

Stara stran je padla na `meta-viewport` (onemogočena povečava), `link-name` ×4, `heading-order` in `color-contrast` ×11. Nova stran teh napak nima, razen kontrasta.

---

## 10. Mobilna postavitev (Playwright 360 / 375 / 390 / 430 / 1440)

### Vodoravni preliv

| Stran | 360 | 375 | 390 | 430 | 1440 |
|---|---|---|---|---|---|
| / | ✅ 360 = 360 | ✅ | ✅ | ✅ | ✅ |
| /porocni-prstani/ | ✅ | ✅ | ✅ | ✅ | ✅ |
| /katalog/ | ✅ | ✅ | ✅ | ✅ | ✅ |
| /kontakt/ (Googlebot UA) | ✅ | ✅ | ✅ | ✅ | ✅ |
| /147-porocna-prstana/ | ✅ | ✅ | ✅ | ✅ | ✅ |

`document.documentElement.scrollWidth === innerWidth` in `window.scrollTo(200,0)` ne premakne strani. `body` ima `overflow-x: clip`, kar na domači skrije ~46 elementov, ki segajo čez rob (drsnik Trustindex, dekoracije). Vidne težave ni.

### Mobilni meni (`button.zd-glava__odpri[data-zd-odpri]`)

| Preverba | Rezultat |
|---|---|
| Najden in viden < 1240 px | ✅ (namizno skrit; pri 1024 px meri 68×32 z napisom »Meni«) |
| Velikost na mobilnem | ❌ **22×13 px** |
| Dostopno ime | ❌ ga ni (glej §9) |
| `aria-expanded` / `aria-controls="zd-meni"` | ✅ preklaplja `false` → `true`, napis se zamenja »Meni« → »Zapri« |
| Odpri s klikom | ✅ `.je-odprt`, zaklep drsenja `html.zd-zaklep`, 8 vidnih povezav (vrstice 22–25 px visoke). Posnetki `*-menu-open.png`. |
| Zapri z Escape | ✅ meni se zapre, fokus se vrne na gumb |
| Zapri s ponovnim klikom | ✅ in zaklep drsenja se odstrani (`*-menu-closed.png`) |
| Tipkovnica po odprtju | ❌ Tab gre na vsebino **za** prekrivnim menijem (»Ogled kolekcije«, drobtine …), ker so povezave `nav#zd-meni` v DOM **pred** gumbom. Fokus ni ujet. |

### Cilji dotika < 44×44 px (izbor najslabših, 360 px)

| Element | Velikost | Selektor |
|---|---|---|
| Gumb menija | **22×13** | `div.zd-glava__desno > button.zd-glava__odpri` |
| Srce na kartici (domača) | **19×19** | `ul.zd-kartice > li.zd-kartica > button.zd-srce` |
| Srce v glavi (priljubljeni) | **21×21** | `div.zd-priljubljeni > button.zd-srce` |
| Facebook ikona v nogi | 20×28 | `div.zd-noga__omrezja > a` |
| Drobtine »Domov«, »Katalog«, »Poročni prstani« | 54–130 × 20 | `nav.zd-drobtine > a` |
| Povezave v nogi (Blog, O nas, Kontakt, Kolekcije …) | 30–118 × 23 | `nav.zd-noga__stolpec > ul > li > a` |
| Telefona in e-pošta v nogi | 143×23 | `.zd-noga__telefoni > a`, `.zd-noga__kontakt > a` |
| »Več zanimivosti« | 151×20 | `.zd-zanimivosti__vec > a` |
| Politika zasebnosti / Nastavitve piškotkov / Multimedija.net | 87–114 × 20–23 | `p.zd-noga__pravno > a/button` |

V redu (≥ 44 px): gumbi piškotne pasice (44 px), oštevilčenje strani, polja obrazca (55 px), »Pošlji sporočilo« (240×52), srce na izdelku (56×56), telefoni na Kontaktu (214×31, širina nadomesti višino).

Popravek brez vizualne spremembe: povečajte območje dotika z `padding` + negativnim `margin`, ali s `::before { content:""; position:absolute; inset:-12px; }` na gumbih in ikonah. Pri povezavah v nogi zadošča `display:inline-block; padding-block: 10px`.

### Piškotna pasica (`#cookie-notice`, role="dialog")

Pri 390×844 je visoka 208 px (25 % zaslona), pri 1440×900 77 px (9 %). Na vseh mobilnih posnetkih prvega zaslona prekrije CTA in vsebino pod herojem. Priporočila:
- na mobilnem zmanjšajte notranje robove oziroma postavite gumbe v eno vrstico (ne spremeni dizajna strani, le pasico);
- `aria-label` prevedite v slovenščino (»Obvestilo o piškotkih«);
- dodajte `scroll-padding-bottom` ali premik fokusa, da fokus ne pade pod pasico.

---

## 11. Presledki v besedilu (zlepljene besede v `textContent`)

**Vzrok:** naslovi so sestavljeni iz dveh `<span>` brez presledka med njima, npr. `<span class="zd-n__a">…</span><span class="zd-n__b">…</span>`. Spani so `display:block`, zato je **na zaslonu vse v redu** (dve vrstici), in `innerText` vsebuje prelom vrstice. Chromovo dostopnostno drevo naslovom doda presledek, Playwright `ariaSnapshot` ni pokazal zlepljenih imen. **`textContent` pa je zlepljen.** To uporabljajo SEO orodja, izvlečki, deljenje na družbenih omrežjih, nekateri iskalniki, Elementor/Yoast analize in kopiranje v nekaterih kontekstih.

**Popravek (brez vizualne spremembe):** v predlogi/kratki kodi oziroma v polju naslova Elementor dodajte navaden presledek med spana: `</span> <span class="zd-n__b">`. Ker sta spana bločna, se presledek ne vidi. Enako velja za `div.zd-rokopis` in `p` v `.zd-izdelava__podpis`.

Najdeno z regex `/[,.!?][A-Za-zČŠŽčšž]/` na `textContent` in s pregledom sosednjih besedilnih vozlišč brez presledka:

| Stran | Element | `textContent` (zlepljeno) | HTML |
|---|---|---|---|
| / | `h1.elementor-heading-title` (hero) | »Poročni prstani**,ki** pripovedujejo vašo zgodbo.« | `<h1 class="elementor-heading-title elementor-size-default"><span class="zd-n__a">Poročni prstani,</span><span class="zd-n__b">ki pripovedujejo vašo zgodbo.</span></h1>` |
| / | `h2` (kolekcija poročni) | »Dva prstana**,ena** zgodba.« | `<h2 class="elementor-heading-title elementor-size-default"><span class="zd-n__a">Dva prstana,</span><span class="zd-n__b">ena zgodba.</span></h2>` |
| / | `h2` (kolekcija zaročni) | »Simbol ljubezni**,ki** traja.« | `<h2 …><span class="zd-n__a">Simbol ljubezni,</span><span class="zd-n__b">ki traja.</span></h2>` |
| / | `h2` | »Izbrani **prstaniiz** naše delavnice« | `<h2 …><span class="zd-n__a">Izbrani prstani</span><span class="zd-n__b">iz naše delavnice</span></h2>` |
| / | `h2` | »Ročna **izdelavav** vsakem detajlu.« | `<h2 …><span class="zd-n__a">Ročna izdelava</span><span class="zd-n__b">v vsakem detajlu.</span></h2>` |
| / | `h2` | »Navdih iz **svetaprstanov**.« | `<h2 …><span class="zd-n__a">Navdih iz sveta</span><span class="zd-n__b">prstanov.</span></h2>` |
| / | `div.zd-izdelava__podpis > p` | »Ročno**.Z** ljubeznijo**.Za** vedno.« (**brez** `aria-label`; na mobilnem skrit) | `<p><span>Ročno.</span><span>Z ljubeznijo.</span><span>Za vedno.</span></p>` |
| / | `div.zd-rokopis` (hero, `role="img"`, `aria-label` ✅) | »Več kot nakit**.Zgodbeza** vse življenje.« | `<div class="zd-rokopis " role="img" aria-label="Več kot nakit. Zgodbe za vse življenje."><span aria-hidden="true" style="--i:0">Več kot nakit.</span><span aria-hidden="true" style="--i:1">Zgodbe</span><span aria-hidden="true" style="--i:2">za vse življenje.</span></div>` |
| / | `a.zd-kartica__povezava` (9×) | »433 – Zaročni **prstanBelo** zlato« | `<h3 class="zd-kartica__ime">433 – Zaročni prstan</h3>` + `<p>` brez presledka (nizka prioriteta) |
| / in vse | `#cookie-notice .cookie-notice-container` | »…obiskanost **strani.Sprejmem**« | markup vtičnika (nizka prioriteta) |
| /porocni-prstani/ | `h1.zd-naslov.zd-naslov--stran` | »Poročni **prstaniza** vajino zgodbo.« | `<h1 class="zd-naslov zd-naslov--stran"><span class="zd-n__a">Poročni prstani</span><span class="zd-n__b">za vajino zgodbo.</span></h1>` |
| porocni, zarocni, katalog, cena, 3902-2 | `h2#zd-po-meri` | »Niste **našlipravega** prstana?« | `<h2 id="zd-po-meri"><span class="zd-n__a">Niste našli</span><span class="zd-n__b">pravega prstana?</span></h2>` |
| porocni, zarocni | `section.zb-faq details` | »…poročne **prstane?Iz** belega …« (`summary` + odgovor) | `<details class="zb-faq__vpr"><summary>…?</summary><div>Iz …</div></details>` (običajno za `details`, nizka prioriteta) |
| /zarocni-prstani/ | `h1.zd-naslov` | »Unikatni zaročni **prstani,izdelani** po meri.« | `<h1 class="zd-naslov zd-naslov--stran"><span class="zd-n__a">Unikatni zaročni prstani,</span><span class="zd-n__b">izdelani po meri.</span></h1>` |
| /katalog/ | `h1.zd-naslov` | »**Katalognaših** prstanov.« | `<span class="zd-n__a">Katalog</span><span class="zd-n__b">naših prstanov.</span>` |
| /kontakt/ | `h1.elementor-heading-title` | »Obiščite **nasv** Žalcu.« | `<h1 …><span class="zd-n__a">Obiščite nas</span><span class="zd-n__b">v Žalcu.</span></h1>` |
| /kontakt/ | `h2` (obrazec) | »**Pošljitepovpraševanje**« | `<h2 …><span class="zd-n__a">Pošljite</span><span class="zd-n__b">povpraševanje</span></h2>` |
| /predstavitev-podjetja/ | `h1` | »Zlatarna **Brežnikže** od leta 1999.« | `<span class="zd-n__a">Zlatarna Brežnik</span><span class="zd-n__b">že od leta 1999.</span>` |
| /predstavitev-podjetja/ | `div.zd-rokopis` (`role="img"`, `aria-label` ✅) | »Ročno**.Z** ljubeznijo**.Za** vedno.« | `<div class="zd-rokopis " role="img" aria-label="Ročno. Z ljubeznijo. Za vedno."><span aria-hidden="true" style="--i:0">Ročno.</span><span aria-hidden="true" style="--i:1">Z ljubeznijo.</span><span aria-hidden="true" style="--i:2">Za vedno.</span></div>` |
| /predstavitev-podjetja/ | `h2` ×3 | »Ročna **izdelavav** vsakem detajlu.«, »Vaš poročni **prstanpo** meri.«, »Ustvarimo **vajinaprstana** skupaj.« | isti vzorec `zd-n__a` / `zd-n__b` |
| /147-porocna-prstana/ | `h1.zd-naslov--izdelek` | »**147Porocna** prstana« (in brez »č«) | `<h1 class="zd-naslov zd-naslov--izdelek"><span class="zd-n__a">147</span><span class="zd-n__b">Porocna prstana</span></h1>` |
| /147-porocna-prstana/ | `h2#zd-podobni` | »Morda vam **bovšeč** tudi« | `<span class="zd-n__a">Morda vam bo</span><span class="zd-n__b">všeč tudi</span>` |
| /3902-2/ | `li` | (vizualno »prstani«, povezava razdeli besedo) | `<li>Najlepši <b><a href="…/zarocni-prstani">unikatni zaročni prstan</a>i</b> za …</li>` |

Ker se vzorec ponovi na vsaki strani, je najbolj učinkovit popravek v **eni** PHP funkciji ali kratki kodi, ki izpiše `zd-n__a`/`zd-n__b`, ter v predlogi `zd-rokopis`.

---

## 12. Priljubljeni (srce)

| Lastnost | Kartica na domači (`ul.zd-kartice > li.zd-kartica > button.zd-srce`) | Stran izdelka (`.zd-izdelek__gumbi .zd-srce`) | Glava (`div.zd-priljubljeni > button.zd-srce`) |
|---|---|---|---|
| Element | ✅ `<button type="button">` | ✅ `<button type="button">` | ✅ `<button type="button">` |
| role | implicitni `button` | implicitni `button` | implicitni `button` |
| aria-label | ✅ »Dodaj med priljubljene: 433 – Zaročni prstan iz belega zlata« | ✅ podobno | »Priljubljeno« (števec `span.zd-priljubljeni__st` je v gumbu, a ga `aria-label` prekrije, zato se **število ne prebere**) |
| aria-pressed | ✅ `false` ↔ `true` (že v strežniškem HTML) | ✅ | – (`aria-expanded` + `aria-controls="zd-priljubljeni"` ✅) |
| Fokusabilen s Tab | ✅ (10. korak na 390 px, 14. na 1440 px) | ✅ | ✅ |
| Enter / Space | ✅ Enter: `false` → `true`; Space: `true` → `false` | ✅ | ✅ |
| Fokus viden | da, a le 1-px obroba (`fav-*-focus.png`) | da | da |
| Velikost | ❌ **19×19 px** | ✅ 56×56 px | ❌ **21×21 px** |
| Gnezdenje | ✅ sosed povezave `a.zd-kartica__povezava`, ni znotraj `<a>` | ✅ | ✅ |
| Obvestilo bralniku zaslona | ni `aria-live`. Sprememba se sporoči le prek `aria-pressed` (OK), števec v glavi pa ne. | | |

Ugotovitve:
- Na **karticah kataloga in arhivov** (`/katalog/`, `/porocni-prstani/`, `/zarocni-prstani/`, `li.zd-izdelek-k`) **srca ni**, `[data-zd-srce]` = 0. Srce je le na 9 karticah domače strani in na strani izdelka. Če je to namenoma, je v redu, sicer gre za nedoslednost.
- Hranjenje v `localStorage['zb-priljubljeni']` deluje (preverjeno in nato počiščeno). Seznam ni vezan na napravo ali račun, kar je pričakovano.
- Priporočila:
  - povečajte območje dotika na ≥ 24 px (idealno 44 px) z `padding`/`::before` brez spremembe ikone;
  - `aria-label` je lahko nespremenljiv (»Priljubljeno: 433 – …«), ker stanje sporoča `aria-pressed`;
  - glavi dodajte število v ime, npr. `aria-label="Priljubljeno (2)"`, ali `aria-describedby` na števec.

---

## 13. Kontaktni obrazec in podatki (`/kontakt/`)

> Navaden obiskovalec najprej dobi stran »Bot Verification« (posnetek `shots/kontakt-m390-full.png`, slikovni izziv reCAPTCHA »Izberite vse kvadrate s stopnicami«). Obrazec sem pregledal z UA Googlebot (`shots/kontakt-gb-*-full.png`, `kontakt-form-*.png`) in ga **nisem oddal**.

Obrazec je **Contact Form 7 6.1.7** (`div#wpcf7-f4093-p34-o1 > form.wpcf7-form`, `novalidate`, `aria-label="Kontaktni obrazec"`).

| Polje | Tip | Oznaka (povezava) | Obvezno | Vidna oznaka obveznosti | autocomplete | Velikost (390 px) |
|---|---|---|---|---|---|---|
| `ime` | text | »Ime in priimek« (ovijajoči `<label class="zd-pol">`, ni `for`/`id`) | `aria-required="true"` | ❌ ni zvezdice ali legende | ✅ `name` | 286×55, 16 px |
| `telefon` | tel | »Telefon« (ovijajoči label) | ne | – | ✅ `tel` | 286×55 |
| `eposta` | email | »E-pošta« (ovijajoči label) | `aria-required="true"` | ❌ | ✅ `email` | 286×55 |
| `tema` | select | »Zanima me« (ovijajoči label). Privzeto izbrano »Poročni prstani«, brez praznega izbora. | ne | – | – | 286×57 |
| `sporocilo` | textarea | »Sporočilo« (ovijajoči label) | **ne** (sporočilo ni obvezno) | – | – | 286×112 |
| Gumb | `button[type=submit].wpcf7-submit` | »Pošlji sporočilo« | | | | 240×52 ✅ (kontrast 3,8:1 ❌) |

- **Oznake:** vse so povezane implicitno (ovijajoči `<label>`), kar je dostopno. Nobeno polje ni »samo placeholder« ✅.
- **Napake:** CF7 validira na strežniku po oddaji (`novalidate`, brez HTML `required`). Mehanizem obstaja: `div.screen-reader-response > p[role=status][aria-live=polite]` + seznam napak, `aria-invalid="false"` na poljih, `.wpcf7-response-output[aria-hidden=true]`. CF7 ob napaki doda `span.wpcf7-not-valid-tip` in `aria-describedby`. Brez oddaje tega nisem mogel preveriti v praksi.
- **Manjka:**
  - vidna oznaka obveznih polj (»*« in legenda »Polja z * so obvezna«, WCAG 3.3.2);
  - kratko obvestilo o obdelavi osebnih podatkov s povezavo na Politiko zasebnosti;
  - zaščita pred neželeno pošto na ravni obrazca (honeypot/Turnstile) **namesto** reCAPTCHA na celotni strani;
  - jasen fokus na poljih (`outline:none`, §9).

### Vidni podatki na strani Kontakt

| Podatek | Prikazan? | Kje / opomba |
|---|---|---|
| Naslov | ✅ | »Šlandrov trg 39, 3310 Žalec«, povezava na Google Maps (`dl.zd-kontakt__seznam`) |
| Telefon | ✅ | `tel:+38637104060` »03 710 40 60« |
| Mobilni | ✅ | `tel:+38641424648` »041 424 648« |
| E-pošta | ✅ | `mailto:info@zlatarna-breznik.si` |
| **Delovni čas** | ❌ **NI** | Samo v JSON-LD (`openingHoursSpecification`: pon–pet 08–12 in 14–17). Stara stran je prikazovala »Pon – Pet od 8 – 12 in 14 – 17 ure. Sobota odprto po dogovoru. Nedelja in prazniki zaprto.« |
| Zemljevid | ✅ | Google Maps iframe (§5). Na posnetku zaslona je bil prazen, prek proxyja se ni izrisal, a zahteve so bile uspešne. |
| CTA | delno | Gumb obrazca »Pošlji sporočilo« in klikljivi telefoni. Ni izrazitega gumba »Pokličite« ali »Rezervirajte termin« nad pregibom. |
| Facebook | ✅ | |
| Drugo | – | Stara stran je navajala tudi razstavni salon Mod Art (Domžale) z drugim zemljevidom. Preverite, ali je izpust namenski. |

---

## 14. Prioritetna priporočila (dizajn ostane enak)

### P0: pred zagonom

1. **Odstranite LiteSpeed reCAPTCHA s `/kontakt/`.**
   - V LiteSpeed WebAdmin / cPanel »reCAPTCHA Protection« ali v `.htaccess` (`verifycaptcha`) poiščite pravilo za ta URL.
   - Spam rešujte na obrazcu: CF7 + Cloudflare Turnstile ali honeypot (»Really Simple CAPTCHA«/»Flamingo«/»Akismet«).
   - Pravilo naj velja kvečjemu za `POST` na `/wp-json/contact-form-7/…`.
   - Ponovno izmerite Kontakt z Lighthouse, ker sedanje meritve niso veljavne.
2. Ob zagonu odstranite `noindex` (SEO 66 → pričakovano 100; vse druge SEO presoje so uspešne).

### P1: hitrost

3. Prednaložite LCP ozadje podstrani in ga pretvorite v WebP/AVIF:
   `<link rel="preload" as="image" href="/wp-content/uploads/2026/09/ozadje-marmor-svetlo.webp" fetchpriority="high">`
   Velja za vse predloge z `section.zd-glava-strani`. Po želji dodajte mobilno različico z `imagesrcset`/`imagesizes`.
4. Vklopite **LSCache predpomnilnik strani** (cilj: `x-litespeed-cache: hit`, TTFB brez ~0,3–0,5 s PHP).
5. Zmanjšajte blokirajoče vire:
   - jQuery, jquery-migrate in cookie-notice JS → `defer` ali noga;
   - združite drobne Elementor CSS (`post-*.css`, `base-*.css`, `widget-*.css`);
   - `pisave*.css` vključite inline;
   - odstranite podvojeni `trustindex-google-widget.css`;
   - po možnosti Critical CSS.
6. `/3902-2/`: base64 slike prenesite v knjižnico medijev (z `width/height`, `srcset`, `loading="lazy"`). **Slug `/3902-2/` ostane nespremenjen** (navodila naročnika: URL ima SEO vrednost).
7. Logotipu v glavi odstranite `fetchpriority="high"` (ostane naj na heroju) in ga pretvorite v SVG ali WebP.

### P1: dostopnost in UX

8. Gumb menija:
   - besedilo »Meni« skrijte z `.screen-reader-text` namesto `display:none`, ali dodajte `aria-label="Odpri meni"`;
   - območje dotika naj bo ≥ 44×44 (padding);
   - ob odprtju premaknite fokus na prvo povezavo in ujemite Tab znotraj menija (ali `inert` na `main`/`footer`);
   - zaprtemu `nav` nastavite `visibility:hidden` tudi za `.sub-menu`, da »Svet prstanov« ni fokusabilna.
9. Kontrast: zlato za drobno besedilo in ozadja gumbov iz `#a07d45`/`#a8844e` zamenjajte s `#90703e` (na beli 4,59:1). Na kremnih ozadjih uporabite `#836739`. Velike naslove in dekor lahko ostanejo v obstoječi zlati.
10. Povezava »Preskoči na vsebino« naj bo ob fokusu vidna (CSS v §9).
11. Kontakt:
    - dodajte viden delovni čas (usklajen z JSON-LD) in označite obvezna polja;
    - ob gumbu dodajte stavek o zasebnosti;
    - vidno oznako fokusa na poljih.

### P2

12. Piškotna pasica:
    - na mobilnem nižja (ena vrstica gumbov, manjši robovi);
    - slovenski `aria-label`;
    - `scroll-padding-bottom`, da fokus ne pade pod pasico.
13. Srca: območje dotika ≥ 24 px (idealno 44 px); števec v dostopnem imenu gumba v glavi; po potrebi srca tudi na karticah kataloga.
14. Presledek med `span.zd-n__a` in `span.zd-n__b` ter med spani v `zd-rokopis` in `.zd-izdelava__podpis` (§11).
15. Google Maps → fasada na klik (prihranek ~470–630 KB, brez piškotkov pred privolitvijo).
16. Trustindex: `loader.js` šele ob približanju `#mnenja`; vsebina vidna brez JS.
17. Slike:
    - WebP/AVIF za ozadja kolekcij (`.zd-kolekcija--porocni/--zarocni`, 127 + 89 KB) z mobilno različico;
    - pretvorba starejših JPG izdelkov;
    - `loading="lazy"` za `a.zd-video > img`, `skica-zarocnega-prstana`, `guess-nakit-…`, logotip in `noga-cvetje.jpg` v nogi;
    - prva 1–2 kartici v katalogu `eager`;
    - pravilni `sizes` za 768×768 slike na predstavitvi.
18. Pisave: prednaložite `jost-latin-ext` in `cinzel-400-600-latin-ext` (č/š/ž). Odstranite neuporabljene deklaracije (Playfair Display, lokalni Poppins), če niso potrebne.
19. Predpomnilnik statičnih virov: `max-age=31536000, immutable` za `?ver=`, pisave in `uploads`.
20. Manjše:
    - `aria-label` na `a.zd-video` naj vsebuje vidno besedilo (»Oglejte si film: ročna izdelava prstana«);
    - `iframe.title` naj bo nastavljiv;
    - `section.zd-glava-strani` znotraj `<main>`;
    - na /3902-2/ `h3` → `h2`;
    - ime izdelka »147-porocna prstana« → »147 – Poročna prstana« (tudi `alt`);
    - slovnica Trustindex »Naslednji oceno«.

---

## 15. Datoteke

- **To poročilo:** `zlatarna/HITROST-UX-POROCILO.md`. Surovi podatki (Lighthouse JSON, Playwright, 44 MB posnetkov) so ostali v delovni mapi seje in niso v repozitoriju. Izbrani posnetki so v `zlatarna/posnetki/`.
- **Lighthouse JSON:** `perf/lh/dev-{home,porocni,zarocni,katalog,kontakt,predstavitev,cena,produkt,p3902}-{mobile,desktop}.json`, `perf/lh/old-{home,porocni}-mobile.json`, ponovitve `perf/lh2/*.json`. Povzetki so v `perf/lh/*.detail.txt`.
- **Playwright/axe:** `perf/pw-layout.json`, `pw-layout-gb.json` (Kontakt), `pw-text.json`, `pw-focus.json`, `pw-fav.json`, `pw-form.json`, `pw-net.json`, `pw-3p.json`, `pw-extra.json`
- **HTML in glave:** `perf/html/`
- **Posnetki zaslona** (`perf/shots/`):
  - celotne strani: `{home,porocni,katalog,produkt}-{m360,m375,m390,m430,d1440}-full.png`, `kontakt-gb-{m360,m375,m390,m430,d1440}-full.png`, stran za preverjanje `kontakt-{m360,m375,m390,m430,d1440}-full.png`;
  - meni: `*-{m360,m375,m390,m430}-menu-open.png` in `*-menu-closed.png`;
  - fokus: `focus-{d1440,m390}-NN.png`, `fav-{home,produkt}-{m390,d1440}-focus.png`;
  - ostalo: `home-m390-first-viewport.png`, `home-t1024-first-viewport.png`, `predstavitev-m390-poziv.png`, `kontakt-form-{m390,d1440}.png`, `skiplink-d1440-focus.png`.
- **Skripte:** `perf/run-lh.sh`, `common.js`, `pw-layout.js`, `pw-detail.js`, `pw-extra.js`, `pw-3p.js`, `lh-summary.js`, `lh-detail.js`
