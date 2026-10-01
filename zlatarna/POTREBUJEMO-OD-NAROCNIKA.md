# Kaj potrebujemo od naročnika – Zlatarna Brežnik

Za novo stran `www.zlatarna-breznik.si` (SEO, GEO, UX/UI). Datum: 1. 10. 2026

Vse spodaj izhaja iz auditu (`SEO-AUDIT-ZLATARNA.md`) in navodila »ne izmišljaj podatkov«. Brez teh podatkov lahko stran tehnično uredimo, vsebine pa ne napišemo do konca.

**Prioritete**
- **P1:** blokira objavo ali tvega izgubo obstoječih pozicij.
- **P2:** potrebno, da bo SEO in GEO »top«.
- **P3:** dodatna izboljšava.

---

## 1. Dostopi (P1)

| Kaj | Zakaj |
|---|---|
| **Google Search Console** za `zlatarna-breznik.si` (polni uporabnik) | Katere strani in poizvedbe prinašajo klike. Brez tega so odločitve o oznakah, podvojenih izdelkih in naslovih domače strani ugibanje. Po selitvi spremljamo napake. |
| **Google Business Profile** (upravitelj) | Usklajen naslov, delovni čas, kategorije, fotografije in spletna stran; odgovori na mnenja. Najpomembnejši signal za »zlatarna Žalec / pri Celju«. |
| **Gostovanje (cPanel / LiteSpeed)** in **DNS / registrar** | `/kontakt/` je za strežniškim »Bot Verification« (reCAPTCHA), zaradi česar AI iskalniki in nekateri obiskovalci ne vidijo kontakta. Nastavitev je pri gostitelju. Za prehod potrebujemo tudi `.htaccess`, SSL in DNS. |
| **Facebook stran** (admin) ali nekdo, ki jo ureja | Ime strani je »Zlatarna Brežnik – Celje, Žalec«. Uskladiti naslov in povezavo. |
| Google Analytics: kdo je lastnik starega računa `UA-135258619-1` | UA ne deluje več. Postavimo GA4 (ali alternativo brez piškotkov) na račun naročnika. |

---

## 2. Podatki o podjetju – potrditev (P1)

Na novi strani so že objavljeni. Potrdite ali popravite:

- **Delovni čas:**
  - pon–pet 8–12 in 14–17, sobota po dogovoru, nedelja in prazniki zaprto;
  - ali velja tudi poleti in v decembru;
  - kako se dogovori za soboto.
- **Telefona:** 03 710 40 60 in **041 424 648**. Ali je mobilna številka lahko javna? Čigava je (Dejan)?
- **E-pošta:** info@zlatarna-breznik.si. Kam naj prihajajo povpraševanja iz obrazca?
- **Lokacija:**
  - točen vhod;
  - **parkiranje** (kje, ali je plačljivo);
  - dostop za invalide;
  - pot iz Celja (približno 10 km, 15 min).
  - Potrebno za novo stran »Zlatarna pri Celju – obiščite nas v Žalcu« in za GEO odgovore.
- **Koordinate / Google profil:** povezava do vašega profila na Google Zemljevidih (da shema in zemljevid kažeta točno lokacijo).
- **Zgodovina:**
  - začetek leta 1999 v Celju;
  - **kdaj** ste se preselili v Žalec;
  - ali je bila trgovina v Celju zaprta (stran zdaj piše »ne več«).
- **Mod'Art, razstavni salon Domžale** (Slamnikarska c. 3) je bil na stari kontaktni strani. Ali je še aktualen? Če ne, ga odstranimo iz vseh imenikov.
- **Dejan Brežnik:**
  - naziv (mojster zlatar?), leta izkušenj, izobrazba, nagrade, članstva.
  - **Samo resnični podatki.** Uporabimo jih za »O nas« in kot avtorja strokovnih člankov (E-E-A-T).

---

## 3. Podatki o izdelkih (P1 za ključne modele, P2 za ostale)

Trenutno nima opisa noben od 251 izdelkov. Unikatnih opisov **ne bomo izmišljevali**. Za vsak model (najprej serija 4xx in 30 najbolj obiskanih po GSC) potrebujemo:

| Podatek | Primer odgovora |
|---|---|
| Vrsta zlata in **karatnost** | belo zlato 585 (14 k) / 750 (18 k) |
| Širina in debelina | 4 mm / 1,8 mm |
| Profil in površina | ravni, zaobljen, mat, kovan, peskan, poliran |
| Kamni | briljanti, skupaj 0,10 ct, kakovost (če jo poznate), cirkoni? |
| Kaj se da prilagoditi | širina, zlato, kamni, gravura |
| Ali model še izdelujete | da / ne / samo po naročilu |

**Odprta vprašanja pri izdelkih:**
1. **Serija 432–442** obstaja dvakrat:
   - poročna prstana (dodana dec. 2025);
   - zaročni prstani s kamnom (dodani dec. 2024).
   - To niso podvojeni izdelki, številke pa so enake. Imate v delavnici drugačno oznako (npr. Z-433)?
2. **118** (dva URL-ja z istim dizajnom) in **067/068** (skoraj enaka fotografija): isti model ali različna?
3. **152 – Posebni – Unikatni poročni prstani:** potrdite, da je poročni par (z diamanti na enem).
4. **Swarovski elements** (20 izdelkov y1–y20) in **Guess nakit:** ali ju še prodajate?
5. **Srebro, slovenski les, platina** se omenjajo v FAQ in člankih. Ali jih res izdelujete?
6. Napake v imenih (»rumenga«, »Birlijanti« …) popravimo sami. Ne vpliva na URL.

---

## 4. Cene in storitve (P1, za strani cen)

Navodilo je: brez izmišljenih cen. Potrebujemo odločitev:

- **Ali smemo objaviti okvirne cene ali razpone?** Na primer »poročna prstana iz 14 k zlata od X € za par« ali »graviranje vključeno«.
  - Stara stran piše »**od 200 € dalje**« in »približno **dve mesečni plači**«. Je to še res? Če ne, umaknemo.
- **Graviranje:** ali je brezplačno (stari članek trdi »brezplačno graviranje zaročnega prstana«), kakšna besedila in pisave, ročno ali laser.
- **Rok izdelave:** koliko tednov za model iz kataloga in koliko za unikat po meri. Koliko prej priporočate naročilo (FAQ zdaj piše 2–3 mesece)?
- **Merjenje velikosti:** brezplačno v trgovini (piše na strani)? Pošiljate merilni obroček?
- **Predelava starega zlata:** ali vzamete staro zlato v račun ali v predelavo?
- **Garancija**, čiščenje, poliranje, rodiniranje belega zlata, povečava/zmanjšava prstana: ali so storitve in pod katerimi pogoji?
- **Plačilo:** obroki, predračun, avans za izdelavo po meri.

---

## 5. Vsebine in fotografije (P2)

- **3–5 resničnih zgodb unikatnih prstanov po meri:** ideja ali želja stranke → **skica** → izbor materiala → izdelava → pomerjanje → končni izdelek. Fotografije (skice, delo v delavnici, končni prstan). **Dovoljenje strank** za objavo (lahko brez imen).
  - Potrebno za `/porocni-prstani/unikatni-porocni-prstani/` in prenovo članka `/3902-2/`.
- **Fotografije lokacije:** zunanjost trgovine (z napisom), notranjost, delavnica, Dejan pri delu. Za shemo LocalBusiness, »O nas«, Google profil in stran »Zlatarna pri Celju«.
- **Logotip** v vektorski obliki (SVG/AI/PDF) in kvadraten znak za favicon (vsaj 512×512).
- **Video:** imate posnetke izdelave ali YouTube kanal? Če da, jih vključimo z lahko vgradnjo (brez upočasnitve).
- **Kratke izjave Dejana** (2–3 stavki) na vprašanja:
  - kaj je unikaten prstan;
  - belo ali rumeno zlato;
  - diamant ali briljant;
  - kako izbrati širino.
  - Citati strokovnjaka močno pomagajo pri GEO (AI povzetki).

---

## 6. Zunanji imeniki – usklajen naslov (P2)

V imenikih se še pojavlja **Celje** ali napačen zapis »Šlandov trg«. Uskladiti je treba ime, naslov, telefon in spletno stran:

- Facebook (»Zlatarna Brežnik – Celje, Žalec«)
- moja-dejavnost.si (vnosa »Poročni prstani Celje« in »… Domžale«)
- poroka-bo.si (»Zlatarna Celje«)
- visitcelje.eu, povezujemo.si, bizi.si, toplocalplaces.com

Naredite sami ali nam dajte dovoljenje in dostope. Enoten zapis:

> Zlatarna Brežnik, Dejan Brežnik s.p., Šlandrov trg 39, 3310 Žalec · 03 710 40 60 · https://www.zlatarna-breznik.si/

---

## 7. Odločitve (P1 pred objavo)

| # | Odločitev | Naš predlog |
|---|---|---|
| 1 | Oznake bloga in izdelkov (50 URL-jev) | Glede na GSC: tiste s kliki → 301 na glavno stran, ostale `noindex`. Seznam v `redirect-map.csv`. |
| 2 | `/cene-porocnih-prstanov-v-letu-2024/` | Uporabno vsebino prenesemo v `/cena-porocnih-prstanov/`, nato 301 (po navodilih). |
| 3 | Članka »Trendi zaročnih prstanov 2020 / 2021« | Posodobimo v en evergreen članek, drugega preusmerimo (po GSC). |
| 4 | Nova stran `/zlatarna-celje/` | Da, če potrdite podatke za prihod in parkiranje. |
| 5 | Avtor člankov | Dejan Brežnik ali »Zlatarna Brežnik« namesto izvajalca. |
| 6 | Strukturirani podatki izdelka (Product) brez cene | Da. Google bo opozoril, da manjka cena. Ni napaka in ne škodi. |
| 7 | Prikaz Google mnenj | Ostanejo vidni (zvezdic v shemi ne dodajamo, tako zahtevajo Googlova pravila). |
| 8 | Arhiv avtorja »Milan« | Izklopimo. |

---

## 8. UX/UI – potrditve in želje (P2)

Dizajna ne spreminjamo brez razloga. Za te popravke potrebujemo potrditev:

- **Gumbi na domači:** namesto 4× »Ogled kolekcije« uporabimo »Oglejte si poročne prstane« in »Oglejte si zaročne prstane«.
- **Filtri po materialu** na `/porocni-prstani/`: Belo zlato · Rumeno zlato · Rdeče zlato · Kombinirano zlato · Z briljanti. Potrdite, da so oznake materiala na izdelkih pravilne.
- **Priljubljeni (srce):** kaj naj se zgodi s seznamom? Predlog: gumb »Pošlji povpraševanje za izbrane modele«, ki seznam vstavi v obrazec.
- **Kontaktni obrazec:** ali želite možnost **priloge** (skica, slika prstana) in izbiro »želim termin posveta«?
- **Naročanje termina:** samo telefon, ali spletni koledar za posvet (tudi sobota po dogovoru)?
- **Kanali:** naj bodo na strani vidni še WhatsApp ali Viber (mobilna številka)?
- **Piškotki in analitika:** GA4 s soglasjem? Meta Pixel ali oglasi (Google Ads)?

---

## 9. Kaj naredimo sami (ne rabimo naročnika)

- Tehnični SEO: presledki v naslovih, H1, title in meta, sitemap, sheme, drobtine, favicon, valuta, varnost.
- Popravke imen izdelkov, alt besedila slik iz obstoječih podatkov, primarne kategorije.
- Hitrost in dostopnost (glej poglavje 15 v auditu).
- Preusmeritve, ki so nedvoumne (`/4017-2/`, `/kategorija-izdelka/*`).
- Prehod na produkcijo po checklisti, ko potrdite datum.
