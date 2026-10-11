# Analiza obstoječe strani – GEOFOTO d.o.o.

Vir: https://www.geofoto.si/ · pregled 11. 10. 2026 · 25 strani · posnetki: `01_analiza/posnetki/obstojeca-1440.jpg`, `obstojeca-390.jpg`
Tehnologija: lastna PHP stran (izdelava Solve-X), jQuery 1.12.3, flexslider, skripti za Internet Explorer, HTTP/1.1.
Ocena potencialne stranke: `../ocena-2026-10-11.md` (81/100).

## 1. Naslovnica danes

| # | Blok | Vsebina | Slike |
|---|---|---|---|
| 1 | Glava (temna, prosojna) | logotip, telefon, e-pošta, meni (Domov, Storitve, Reference, O podjetju, Kontakt); plavajoči zavihek »Naroči storitev« | `logo.png` (negativ) |
| 2 | Hero drsnik (4 slajdi) | Inženirska geodezija »Kadar mora biti zares natančno!«, Lasersko skeniranje, Aerofotogrametrija, GIS; ozadni video `Vinica.mp4` | `slide-1.jpg`, `prizma_JB.jpg`, … |
| 3 | Naše storitve | 8 krogov z ikonami brez opisov: inženirska geodezija, zemljiški kataster, lasersko skeniranje, bližjeslikovna fotogrametrija, GIS, kartografija, hidrografija, sodno izvedenstvo | ikone |
| 4 | Povpraševanje + Aktualno | »Na podlagi dvajset in več letnih izkušenj …« + gumb; novici 13. 12. 2020 in 21. 9. 2020 | zamegljeno ozadje |
| 5 | Noga | sedež in 2 poslovni enoti (Slovenske Konjice, Rogaška Slatina), storitve, delovni čas; »©2017« | – |

## 2. Kaj deluje in ohranimo

- Stran je odzivna, obrazec za povpraševanje deluje, telefon in e-pošta sta vidna v glavi.
- Prave fotografije terena in izdelkov: geodet z lato, totalna postaja, gradbišče s prizmo, laserski oblak točk,
  3D karte, batimetrija.
- Močan seznam referenc (DARS, DRSI, Infra, HESS, DEM, Elektro Celje, Lek, MOM, MOL, 7 občin).

## 3. Težave

| Področje | Ugotovitev | Dokaz | Vpliv |
|---|---|---|---|
| Zaupanje / zastarelost | zadnji novici iz leta 2020, »©2017« v nogi | naslovnica | obiskovalec dvomi, ali podjetje še aktivno skrbi za stran |
| Hero | ozadnega videa ni na strežniku (`/video/Vinica.mp4` vrne HTML naslovnice), prikazuje se samo zaslonska slika; drsnik menja sporočila | HTTP preverba | glavno sporočilo ni jasno, tehnična napaka |
| Dve ciljni skupini | zasebniki (meja, parcelacija, hišna številka) in investitorji/javni naročniki (inženirska geodezija, skeniranje, GIS) niso ločeni | blok storitev | zasebnik ne najde hitro »svoje« storitve, investitor ne vidi referenc |
| Storitve | samo ikone in imena, brez opisa in koristi | naslovnica 253 besed | nizka informativnost in SEO |
| Reference in dokazi | reference samo na podstrani; ni številk (30+ let, 17 zaposlenih, 7 s strokovnim izpitom, 3 enote) | /reference, /o-podjetju | izgubljena prednost pred konkurenco |
| Nedokončano | stran Hidrografija »Stran v izdelavi!«; podstran »Zaposleni« kaže naslovnico | /storitve/hidrografija | neprofesionalen vtis |
| Mobilno | `user-scalable=no` (ni povečave), plavajoči zavihek prekriva vsebino, šibek kontrast naslova | posnetek 390 | dostopnost |
| SEO | `<title>` »GEOFOTO« (6 strani enako), meta opis na 0/25 strani, `lang="en"`, H1 »NAŠE STORITVE«, brez JSON-LD, slike brez alt | `pages.json` | slaba vidnost za iskanja, kot sta »geodet Slovenska Bistrica« in »parcelacija« |
| Lokalno | 3 poslovne enote brez lokalne predstavitve | noga | izgubljena lokalna iskanja (Slovenske Konjice, Rogaška Slatina) |

## 4. Tehnični SEO naslovnice

| Element | Stanje |
|---|---|
| `<title>` | »GEOFOTO« |
| meta description | ni (nobena od 25 strani) |
| H1 | »NAŠE STORITVE«, »Pošljite povpraševanje«, »Aktualno« |
| lang / canonical / viewport | `en` (napačno) / ni / `user-scalable=no, maximum-scale=1.0` |
| JSON-LD | ni |
| og:image / alt | ni / slike brez alt |

## 5. Vizualni materiali (iz `slike.tsv`)

50 slik. Najboljše prave fotografije:

- `IMG_20170304_154651.jpg` (8273×1934): totalna postaja na travniku z mejno črto;
- `prizma.jpg` (3263×1475): gradbišče s prizmo;
- `lata.jpg` (2370×1447): nivelirna lata;
- `kontakt-cover.jpg` (1920×600): geodet z lato na mostu.

Izdelki: `slide-1.jpg` (oblak točk), `slides-fin-2.jpg` (ortofoto z modelom poplav), `kartografija-banner.jpg`,
`hidro-banner.jpg`. Logotip: samo negativ `logo.png` 292×69 (bel napis, rdeča črta `#D01623`).
Logotipi referenc: DARS, Infra, HESS, DEM, Ministrstvo za infrastrukturo.
