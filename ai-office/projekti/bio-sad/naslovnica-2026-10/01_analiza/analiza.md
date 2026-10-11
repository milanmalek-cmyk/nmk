# Analiza obstoječe strani – BIO-SAD d.o.o.

Vir: https://www.bio-sad.si/sl/ · pregled 11. 10. 2026 · 79 strani (jezik: sl) · posnetki: `01_analiza/posnetki/obstojeca-1440.jpg`, `obstojeca-390.jpg`
Tehnologija: Joomla (predloga `wt_app_free`, UIkit/Warp), jQuery 1.11.2, LiteSpeed. Izdelava: Multimedija.net.

## 1. Naslovnica danes (bloki po vrstnem redu)

| # | Blok | Vsebina (povzetek) | Slike |
|---|---|---|---|
| 1 | Glava (črna) | meni razdeljen levo/desno od logotipa (O podjetju, Produkti, Ustvarjamo, Priznanja, Polnitve · Standardi, Kontakt), zastavice SL/DE/EN; ob robu stalni zavihek »Povpraševanje« | `logotip.png` (negativ) |
| 2 | Hero drsnik (4 slajdi) | Družba · Ustvarjamo z naravo · Priznano podjetje · Polnitve drugih programov; naslov v okrasni pisavi Norican, kratek opis | `slider5`, `slider6`, `slider3`, `slider7` (vinogradi, pokrajina) |
| 3 | Produkti (temno ozadje) | 3 skupinske slike: žgane pijače, pijače na osnovi vina, likerji; imena kategorij so vidna šele ob prehodu z miško | `zgane-nova`, `vina-nova`, `likerji-2022` |
| 4 | Produkti 2 (bež ozadje) | sadni sirupi, polnitve – prav tako brez vidnih napisov | `sokovi-nova`, `polnitve-home-2022-1` |
| 5 | Aktualno | drsnik 10 novic (polnilni program, Eurospin, Mister & Miss Gin, priznanja, Hofer Selekcija, Cremoso, Lidl, boniteta, Jager) | slike novic |
| 6 | Naši partnerji | 10 logotipov trgovcev in partnerjev | `sponzorji/*` |
| 7 | Pas s pozivom | »Ali se zanimate za naše produkte?« + gumb »Pošlji povpraševanje« | – |
| 8 | Noga | o podjetju, kontakt, delovni čas tovarniške prodajalne, kategorije, e-novice, družbena omrežja (Facebook, Twitter, Google+), TÜV SÜD ISO 9001, IFS / Bureau Veritas | certifikati |

## 2. Kaj deluje in ohranimo

- **Prava zgodba podjetja:** lastna proizvodnja v Lenartu, več kot 30 let na trgu, polnitve za največje trgovce.
- **Dokazi zaupanja so na voljo:** IFS Food, ISO 9001, HACCP, medalje Novi Sad 2017–2021, partnerji Hofer, Lidl, Mercator, Spar, Eurospin.
- **Kakovostne fotografije proizvodnje** obstajajo (`slider8/9/10` na O podjetju), a jih naslovnica ne uporablja.
- **Izrezane fotografije izdelkov** (prosojni PNG) so enotne in primerne za sodobne kartice.
- **Jasen poslovni poziv** »Pošlji povpraševanje« z obrazcem.

## 3. Težave

| Področje | Ugotovitev | Dokaz | Vpliv |
|---|---|---|---|
| Mobilno | stran ni odzivna: na telefonu se izriše 1200 px široka namizna različica, pomanjšana | dve oznaki viewport, zadnja `width=1200`; mobilni posnetek je 2400 px širok (1200 × 2) | drobno, neberljivo besedilo, slaba izkušnja in slabša uvrstitev v mobilnem iskanju |
| Prodajna jasnost | prvi zaslon ne pove, kaj podjetje izdeluje in za koga; glavno sporočilo je v drsniku, ki se menja | hero: »Družba« + splošen opis | obiskovalec (trgovec, kupec) ne ve takoj, ali je na pravem mestu |
| Dve ciljni skupini v enem | potrošniške blagovne znamke (Bio-Sad, Apis, Mister & Miss Gin) in B2B polnitve so pomešane | kategorije in polnitve v istem bloku brez razlage | B2B ponudba (polnitve pod blagovno znamko kupca) je skrita |
| Kategorije | imena kategorij so skrita do prehoda z miško; na dotičnih napravah jih ni | posnetek 1440: pod slikami ni napisov | uporabnik ne ve, kam vodi klik |
| Postavitev | velika prazna bela ploskev v bloku Aktualno | posnetek 1440: ~600 px praznega prostora pod novico | videz nedokončane strani |
| Zaupanje | priznanja in certifikati so samo v nogi ali na podstraneh; ni številk (30 let, medalje) na vidnem mestu | noga: majhna znaka TÜV in IFS | premalo izkoriščeni dokazi kakovosti |
| Fotografije | hero uporablja splošne fotografije vinogradov namesto lastne proizvodnje | `slider3/5/7` | slabša avtentičnost, podjetje ni prepoznavno |
| Zastarelost | Google+ v nogi, okrasna pisava Norican, drsniki | noga, hero | vtis zastarele strani |
| Dostopnost | 37 od 40 slik na naslovnici je brez besedila `alt` | `pages.json` | slabša dostopnost in SEO slik |

## 4. Tehnični SEO naslovnice

| Element | Stanje | Opomba |
|---|---|---|
| `<title>` | »Domov« | brez imena podjetja in ključnih besed; 23 podstrani ima naslov »Produkti«, 19 »Polnitve« |
| meta description | ni | opis ima samo 2 od 79 strani |
| H1 | 10 oznak H1 (Povpraševanje, Družba, Ustvarjamo z naravo, …, Hvala za zaupanje!) | potreben en sam H1 z glavnim sporočilom |
| lang, canonical, viewport | `sl-si` ✓ · canonical ni · viewport podvojen (`width=1200` prevlada) | |
| strukturirani podatki (JSON-LD) | ni na nobeni strani | priložnost za Organization, LocalBusiness, Product (GEO) |
| og:image, alt besedila | og:image ni · 37/40 slik brez alt | deljenje na omrežjih brez slike |
| robots.txt, sitemap.xml | oba 404 | |
| Večjezičnost | SL / DE / EN obstajajo | hreflang ni preverjen (izven obsega naslovnice) |

## 5. Podstrani, pomembne za naslovnico

- **O podjetju** – zgodovina (od 1994, Jakobski Dol → Lenart 2020), blagovni znamki Bio-Sad in Apis, partnerji, certifikati, poziv k lastni blagovni znamki. Glavni vir dejstev.
- **Produkti** (4 kategorije: žgane pijače, likerji, pijače na osnovi vina, sadni sirupi) – vse fotografije izdelkov.
- **Polnitve** – B2B ponudba, kupci (Hofer, Lidl, Mercator, Eurospin, Jager, Ahac, Akustika Group, Arteska …).
- **Priznanja** – medalje Novi Sad 2017–2021 (seznam v `dejstva.md`).
- **Standardi** – politika kakovosti, IFS Food, ISO 9001, HACCP, brez GSO, reciklabilna embalaža.
- **Kontakt** – naslov, telefoni po oddelkih, delovni čas, tovarniška prodajalna.

## 6. Vizualni materiali na strani (iz `slike.tsv`)

- 209 različnih slik. Fotografije izdelkov so največ 362×550 px (posamezni) oziroma 492–650 px (skupinske); izjema `borovnicevec-sadni-liker-siva.jpg` 1000×1374 (izdelek trgovca).
- Panoramske fotografije (hero, proizvodnja, sestavine): 1621×540 px.
- Logotip: samo negativna različica 202×62 px (bel napis, zelena kapljica `#98C93C`). Vektorja ni.
- Izbor za paket in razlogi: `03_paket-chatgpt/EVIDENCA.md`.
