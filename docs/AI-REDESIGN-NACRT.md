# Multimedija AI Office – modul AI REDESIGN

**Status:** zasnova potrjena 11. 10. 2026. Izvedena K1 (ogrodje modula) in K2 (BIO-SAD faze F0–F5); čaka V1.
Modul: `ai-office/moduli/redesign/` · ukaz: `/redesign` · projekt BIO-SAD: `ai-office/projekti/bio-sad/naslovnica-2026-10/`
**Prvi testni projekt:** BIO-SAD (https://www.bio-sad.si/sl/)

## 1. Namen in meje

- **Vhod:** URL spletne strani obstoječe stranke.
- **Izhod:** paket za ChatGPT, nato po odobrenem dizajnu delujoča statična naslovnica, zaščiten predogled in prodajni osnutki.
- **Obseg:** samo naslovnica. Ne celotna stran, ne CMS in ne sistem AI Office kot celota.
- **Varovalke:** nič se ne objavi in nič se ne pošlje brez vaše izrecne potrditve. Modul nima povezave za pošiljanje e-pošte.
- **Povezljivost:** modul ima jasne vhode in izhode (manifest `projekt.json`), zato ga bomo lahko kasneje povezali z evidenco strank, e-pošto, marketingom in vodenjem projektov.

## 2. Uporaba: en ukaz `/redesign`

`/redesign` je projektni ukaz (skill) v Claude Code. Ob vsakem zagonu prebere stanje projekta in nadaljuje z naslednjo fazo, pri vratih potrditve pa se ustavi.

| Ukaz | Kaj naredi |
|---|---|
| `/redesign https://www.bio-sad.si/sl/` | ustvari ali najde projekt in izvede faze 0–5 do paketa za ChatGPT |
| `/redesign bio-sad` | nadaljuje projekt od trenutne faze |
| `/redesign bio-sad gradnja` · `predogled` · `prodaja` | izvede samo izbrano fazo |
| `/redesign bio-sad stanje` | pokaže, kaj je narejeno, kaj manjka in katera potrditev čaka |

## 3. Struktura modula

```
.claude/skills/redesign/SKILL.md      ukaz /redesign: potek, pravila kakovosti, vrata potrditve
ai-office/
  moduli/redesign/                    koda in predloge (brez podatkov strank)
    README.md
    scripts/                          deterministični koraki (Python stdlib + Pillow, Node za posnetke)
      crawl.py           pregled strani: naslovi, meta, besedila, povezave, slike po straneh
      probe_images.py    dimenzije in velikosti slik brez prenosa (HTTP Range)
      screenshot.mjs     posnetki naslovnice (namizje/tablica/mobilno) – Playwright + Chromium
      brand.py           barve iz CSS in logotipa, pisave
      contact_sheet.py   pregledni listi kandidatov (samo za izbor, ne gredo v paket)
      fetch_assets.py    prenos izbranih originalov, SHA-256, evidenca
      package.py         ZIP za ChatGPT in preverjanje vsebine
      preview_build.py   predogled: noindex, oznaka »PREDLOG PRENOVE«, .htaccess, robots.txt
      deploy_preview.sh  objava; privzeto samo suhi zagon, prava objava samo z --potrjeno
    templates/                        predloge izhodov
      dejstva.md  analiza.md  struktura.md  besedila.md  seo-geo.md
      smernice.md  chatgpt-poziv.md  prenos-artifact.md  animacije.md
      prodaja/  koristi.md  email.md  sodelovanje.md  obseg.md  ponudba.md
      predogled/  .htaccess  robots.txt  oznaka.html
    config/
      nastavitve.example.yaml         domena predogledov, strežnik, pošiljatelj (brez gesel)
      cenik.example.yaml              potrjene cene vnesete vi
    schema/projekt.schema.json        format manifesta = vmesnik za prihodnje module
  projekti/<stranka>/<projekt>/       npr. projekti/bio-sad/naslovnica-2026-10/
    projekt.json                      stranka, URL, faze, stanja, odobritve, izhodi
    01_analiza/      pages.json, slike.tsv, posnetki/, analiza.md, dejstva.md
    02_vsebina/      struktura.md, besedila.md, seo-geo.md
    03_paket-chatgpt/ slike/, logotip/, barve.md, smernice.md, chatgpt-poziv.md, EVIDENCA.md
    04_dizajn/       odobren koncept iz ChatGPT (posnetke naložite vi) in opombe
    05_naslovnica/   index.html, style.css, main.js, img/ – statična stran
    06_predogled/    izdaja z zaščito in dnevnik objav
    07_prodaja/      koristi, e-pošta, sodelovanje, obseg, ponudba (osnutki)
```

ZIP datoteke se ne shranjujejo v git (`.gitignore` že izključuje `*.zip`). Ustvarijo se iz map in pošljejo neposredno.

## 4. Potek in vrata potrditve

| Faza | Kaj naredi sistem | Izhod | Vaše delo |
|---|---|---|---|
| 0 Inventar | preveri obstoječe materiale projekta: kaj imamo, kaj manjka, kaj lahko ponovno uporabimo | stanje v `projekt.json` | – |
| 1 Pregled strani | pregled naslovnice in pomembnih podstrani (omejeno na en jezik in največ N strani, z zamikom med zahtevami), besedila, meta, posnetki zaslona, popis vseh slik z dimenzijami brez prenosa | `01_analiza/` | – |
| 2 Raziskava | podjetje, dejavnost, ponudba in prednosti iz lastne strani in javnih virov (poslovni registri, mediji, sejmi, certifikati), 3–5 konkurentov | `dejstva.md` z virom, datumom in statusom vsakega podatka | – |
| 3 Vsebina | ciljne skupine, glavno sporočilo, struktura blokov, končna besedila, CTA; SEO (title, meta, H1/H2, ključne besede, interne povezave, schema.org JSON-LD); GEO (jasna, citirana dejstva in FAQ, ki jih AI iskalniki lahko povzamejo) | `02_vsebina/` | pregled besedil (priporočeno) |
| 4 Vizualni materiali | logotip, barve, pisave; izbor fotografij in prenos samo izbranih originalov v najvišji ločljivosti, s preverjanjem SHA-256 | `03_paket-chatgpt/` | – |
| 5 Paket za ChatGPT | ZIP, smernice, natančen poziv | ZIP | 🔒 **V1:** v ChatGPT izdelate in potrdite koncept, posnetke odložite v `04_dizajn/` |
| 6 Gradnja | prenos v Claude Artifacts, statičen HTML/CSS/JS, zaseben Artifact za pregled; iste datoteke so izvoz za gostovanje | `05_naslovnica/` | pregled in popravki |
| 7 Predogled | zaščita, noindex, oznaka, test odzivnosti; suhi zagon pokaže, kaj bo objavljeno in kje | `06_predogled/` | 🔒 **V2:** potrditev pred objavo |
| 8 Prodaja | 3 koristi, e-pošta, predlog sodelovanja, obseg, ponudba (cene samo iz potrjenega cenika) | `07_prodaja/` | 🔒 **V3:** nič se ne pošlje brez potrditve |

Vsaka odobritev se zapiše v `projekt.json` (vrata, kdo, kdaj, opomba).

## 5. Pravila kakovosti, vgrajena v `/redesign`

- **Slike:** prenesemo samo izbrane, bajt-za-bajt originale z izvirnimi imeni. Izdelkov, embalaže, etiket in logotipov ne spreminjamo. Za vsako sliko preverimo, ali na strani obstaja večja različica. Evidenca vsebuje ime, izvorni URL, dimenzije in predlagano uporabo.
- **Dejstva:** status ✅ preverjeno (z virom), ⚠️ predpostavka ali ❓ potrdi naročnik. Brez izmišljenih številk, let, nagrad ali referenc.
- **Oblikovanje:** manj je več, 6–8 blokov, premium videz, dobre fotografije, jasni poudarki in diskretne mikroanimacije.
- **Do strani naročnika:** omejeno število zahtev z zamikom, samo branje, nobenih sprememb.
- **Pravice:** materiali so last naročnika ali tretjih oseb (logotipi partnerjev). Uporabljajo se samo za predlog temu naročniku.

## 6. Prenos v Claude Artifacts (standard)

Paket za prenos (`prenos-artifact.md`) vsebuje:

1. **Odobren dizajn:** posnetki iz ChatGPT (namizje in mobilno) z oznako različice.
2. **Originalne fotografije** iz `03_paket-chatgpt/slike`, nespremenjene.
3. **Končna besedila** iz `besedila.md`.
4. **Barve in pisave** kot CSS spremenljivke (design tokens).
5. **Navodila za animacije** (`animacije.md`): vstop elementov ob drsenju, odziv kartic in gumbov ob prehodu z miško, nežno gibanje hero fotografije. Vse animacije upoštevajo `prefers-reduced-motion` in delujejo brez knjižnic (CSS + IntersectionObserver).

**Tehnika:** `index.html` + `style.css` + `main.js` + `img/`, brez gradnje in brez Reacta. Artifact objavi iste datoteke kot dodatne datoteke strani, zato je izvoz za običajno gostovanje enak mapi `05_naslovnica/`. Če bi kdaj potrebovali React, je rezervna pot gradnja z Vite v samostojno mapo `dist/`. Privzeto se ji izognemo.

## 7. Objava predogleda

- **Naslov:** npr. `https://predlogi.multimedija.net/<stranka>-<naključni-niz>/` (domeno določite vi).
- **Zaščita:** HTTP Basic Auth (`.htaccess` + `.htpasswd`), posebno geslo za vsak projekt. Deluje na Apache in LiteSpeed.
- **Brez indeksiranja:** glava `X-Robots-Tag: noindex, nofollow, noarchive`, `<meta name="robots">`, `robots.txt` z `Disallow: /` in naključna pot.
- **Oznaka:** stalen trak »PREDLOG PRENOVE – ni objavljena stran · Multimedija · datum« in predpona v `<title>`.
- **Odzivnost:** pred objavo samodejni posnetki pri širinah 390, 768 in 1440 px. Priloženi so povzetku za potrditev.
- **Načini objave** (izberete enega):
  - **A) GitHub Actions z ročnim zagonom (priporočam):** gesla so v GitHub Secrets, objavo sprožite vi s klikom (to je hkrati potrditev). Deluje tudi s telefona.
  - **B) Lokalna skripta** na vašem računalniku, tako kot `start-multimedija`: `deploy_preview.sh bio-sad --potrjeno`.
  - **C) Neposredno iz oblačnega okolja Claude:** samo, če omrežna nastavitev okolja dovoli vaš strežnik. Orodij za SFTP/FTP (`lftp`, `rsync`) v okolju trenutno ni, zato ta pot ni zanesljiva.
- **Pred objavo** sistem pokaže seznam datotek, ciljni URL, način zaščite in posnetke, nato počaka na »potrjujem«.

## 8. Prodaja

- **3 koristi**, vsaka utemeljena z ugotovitvijo iz analize (npr. manjkajoč jasen poziv k akciji ali zastareli slider).
- **Kratka osebna e-pošta** v vašem imenu in tonu, s povezavo na predogled in geslom ločeno.
- **Predlog sodelovanja:** naslovnica → celotna stran → vzdrževanje, SEO in vsebine.
- **Okviren obseg:** postavke in ocena dni.
- **Ponudba:** samo s potrjenim cenikom (`cenik.yaml`). Brez njega ostanejo polja `[CENA – potrdi]`.
- **Pošiljanje:** vse ostane osnutek v `07_prodaja/`.

## 9. Povezljivost z AI Office (kasneje, ne zdaj)

- `projekt.json` po shemi `projekt.schema.json`: `stranka` (naziv, URL, ključ za kasnejši CRM), `faze[]` (stanje, čas, izhodi), `odobritve[]`, `viri[]`.
- Izhodi imajo stalne poti. Prihodnji moduli jih berejo neposredno: CRM poveže projekt s stranko, e-poštni modul prebere `07_prodaja/email.md`, marketing besedila, vodenje projektov pa faze in stanja.
- Integracije (CRM, osnutki v Gmailu, koledar) se kasneje priklopijo na vrata potrditve kot ločeni adapterji, brez sprememb jedra modula.

## 10. Potrebna orodja

| Orodje | Namen | Stanje |
|---|---|---|
| Claude Code (oblak ali lokalno) + projektni skill `/redesign` | orkestracija | ✅ na voljo |
| Python 3.x + Pillow | pregled, slike, barve, ZIP | ✅ nameščeno |
| Node 22 + Playwright + Chromium | posnetki zaslona, test odzivnosti, strani, ki potrebujejo JS | ✅ Chromium je prednameščen; npm paket `playwright` se namesti ob prvem zagonu |
| Spletno iskanje in branje strani (WebSearch / WebFetch) | raziskava podjetja in konkurence | ✅ na voljo |
| Claude Artifacts | zaseben pregled delujoče naslovnice | ✅ na voljo |
| Git + GitHub (`milanmalek-cmyk/nmk`) | hramba modula in projektov | ✅ na voljo |
| ChatGPT (vaš račun) | vizualni koncept | ročni korak |
| Strežnik za predoglede (domena, Apache/LiteSpeed z `.htaccess`, SFTP ali FTP) | objava predogledov | ❓ potrebujem podatke |
| GitHub Actions + Secrets (če izberete A) | varna objava | ❓ po vaši odločitvi |
| Cenik | ponudba | ❓ od vas |
| Podatki pošiljatelja (ime, funkcija, podpis, tikanje/vikanje) | e-pošta | ❓ od vas |

## 11. BIO-SAD: kaj imamo, kaj manjka, kaj ponovno uporabimo

**Imamo trajno (v gitu):** `materiali/bio-sad-naslovnica/` (zdaj `ai-office/projekti/bio-sad/naslovnica-2026-10/03_paket-chatgpt/`) – 29 originalnih datotek:

- logotip
- 2 hero fotografiji in 3 fotografije proizvodnje
- 5 slik kategorij in 5 izpostavljenih izdelkov
- 2 certifikata in 10 logotipov partnerjev
- `00_EVIDENCA.md`: vsebina obstoječe naslovnice, barve, pisave, izvorni URL-ji

→ **Ponovna raba v celoti:** premik v `03_paket-chatgpt/`. Zbiranja slik ne ponavljamo.

**Imamo samo začasno (v tej seji, ob koncu se izgubi):**

- pregled 104 slovenskih podstrani (`pages.json`, surovi HTML)
- popis 210 slik z dimenzijami
- CSS predloge in pregledni listi

→ Ob začetku razvoja jih shranimo v `01_analiza/` (brez surovega HTML). Če se seja prej konča, se pregled samodejno ponovi v približno minuti, slik pa ni treba ponovno prenašati.

**Manjka (naredi modul):**

- raziskava podjetja iz javnih virov in `dejstva.md` s statusi (leto ustanovitve, lastne blagovne znamke, seznam priznanj, veljavnost certifikatov IFS in ISO 9001)
- analiza konkurence ter trenutnega SEO/GEO stanja (title, meta, naslovi, strukturirani podatki)
- struktura in končna besedila nove naslovnice
- smernice in poziv za ChatGPT
- posnetki zaslona trenutne naslovnice (namizje in mobilno)

**Manjka od naročnika (ne blokira predloga, pride v ponudbo):**

- vektorski logotip in različica za svetlo ozadje
- fotografije izdelkov v višji ločljivosti (zdaj največ 362–650 px)

## 12. Izvajalni načrt (po potrditvi)

| Korak | Vsebina | Konec koraka |
|---|---|---|
| K1 | Ogrodje: mape, `projekt.schema.json`, skill `/redesign`, premik obstoječih skript iz te seje v modul, migracija BIO-SAD materialov | struktura v gitu |
| K2 | Faze 0–5 in test na BIO-SAD | ZIP + poziv za ChatGPT → 🔒 V1 |
| K3 | Faza 6: predloga za prenos, naslovnica BIO-SAD v Artifacts, izvoz | delujoča naslovnica |
| K4 | Faza 7: predogled po vaših podatkih o strežniku, suhi zagon | 🔒 V2 → objava |
| K5 | Faza 8: prodajni osnutki za BIO-SAD | osnutki → 🔒 V3 |
| K6 | Navodila za uporabo in pregled po prvem testu (kaj izboljšati) | modul pripravljen za naslednjo stranko |

## 13. Odločitve, ki jih potrebujem

1. Potrditev strukture in načrta. Ali modul ostane v tem repozitoriju (`ai-office/`, kasneje ga lahko izločimo) ali gre v nov repozitorij?
2. Način objave predogledov (A, B ali C), domena za predoglede in vrsta gostovanja.
3. Cenik. Ali naj ponudba za zdaj ostane brez cen?
4. Pošiljatelj: ime, funkcija, podpis in tikanje ali vikanje v e-pošti.
