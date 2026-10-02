# Navodila za izvedbo – Zlatarna Brežnik

**Za:** sejo »zlatar« na `~/projekti/zlatar` (`zlatar.ddev.site`)
**Vir:** `SEO-AUDIT-ZLATARNA.md`, `ODLOCITVE.md` (Milanove odločitve, 2. 10. 2026), `redirect-map.csv`, `izdelki-popravki.csv`, `HITROST-UX-POROCILO.md`
Vse datoteke so v repozitoriju `milanmalek-cmyk/nmk`, veja `claude/vibrant-clarke-q4xbdv`, mapa `zlatarna/`.

Številke v oklepajih (#12) so številke odločitev v `ODLOCITVE.md`.

---

## 0. Pravila

1. **Pred vsakim sklopom:** `ddev snapshot --name seo-<sklop>-<datum>` in git commit child teme. Brez tega ne začni.
2. **Dizajn ostane.** Spremembe videza so samo odobrene: #47 barva drobnega zlata, #49 pasica, #50 srce v katalogu, #51 gumb za povpraševanje, #52 filtri, #53 obrazec.
3. **URL-jev ne spreminjaj.** Brez spreminjanja slugov in permalinkov. Ničesar ne briši, razen `/guess-nakit/` (#27, v smeti). Vse preusmeritve so v `redirect-map.csv`. Vrstic MANUAL REVIEW ne izvajaj.
4. **Ne izmišljuj.** Cen, karatov, širin, kamnov, rokov, garancij, certifikatov in parkiranja ne piši, dokler jih ne potrdi naročnik. Velja `docs/vir-resnice.md`. Vanj dodaj potrjena dejstva iz `ODLOCITVE.md` (#39–#43).
5. **Brez keyword stuffinga.** Ena primarna stran na namero (audit, poglavje 10.1).
6. **Po vsakem sklopu** zaženi preizkuse (obrazec, piškotki, mnenja, brez napak v JS) in preverjanja iz tega dokumenta. Commit z jasnim sporočilom.
7. **Na produkcijo ne objavljaj** (#7). Prehod šele, ko Milan potrdi.

---

## 1. Hitri tehnični popravki (brez vpliva na videz)

| Naloga | Kako | Preveri |
|---|---|---|
| **Presledki v naslovih** (#46) | V PHP funkciji ali kratki kodi, ki izpiše `<span class="zd-n__a">…</span><span class="zd-n__b">…</span>`, dodaj presledek med spana. Enako v `zd-rokopis`, `.zd-izdelava__podpis` in v kartici `zd-kartica` (ime + material). Najdeš z `grep -rn "zd-n__a\|zd-rokopis\|zd-izdelava__podpis" wp-content/themes/hello-elementor-child`. Če je besedilo v Elementorjevih podatkih, popravi skripte v `scripts/strani/`. | Na `/`, `/porocni-prstani/`, `/zarocni-prstani/`, `/katalog/`, `/kontakt/`, `/predstavitev-podjetja/` in izdelku `textContent` naslovov ne vsebuje vzorca `[,.!?][A-Za-zČŠŽčšž]` ali zlepljenih besed (»prstaniiz«, »Katalognaših«). |
| **H1 arhivov oznak izdelkov** | `woocommerce/archive-product.php`: na `is_product_tag()` naj bo H1 ime oznake, ne »Katalog naših prstanov.« | `/oznaka-izdelka/belo-zlato/` ima H1 »Belo zlato«. |
| **Valuta** (#5) | `ddev wp option update woocommerce_currency EUR` | `wp option get woocommerce_currency` = EUR. Nikjer se ne izpiše cena. |
| **Dev noindex** (#4) | MU-plugin (deluje na ddev/nginx in LiteSpeed): na `send_headers` pošlji `X-Robots-Tag: noindex, nofollow`, kadar `$_SERVER['HTTP_HOST']` ni `www.zlatarna-breznik.si`. Na produkciji se ne sproži. | `curl -sI https://zlatar.ddev.site/` ima glavo, z `Host: www.zlatarna-breznik.si` je nima. |
| **Trustindex CSS dvakrat** | Odstrani drugo vključitev (`<link>` v `<head>` ali inline v `#mnenja`). | Na `/` se `trustindex-google-widget.css` pojavi enkrat. |
| **Footer naslovi** | »Hitre povezave«, »O podjetju« in »Kontakt« v nogi naj ne bodo `<h2>` (npr. `<p class="…">` z istim slogom). | V člankih ni več teh H2. |

---

## 2. Preusmeritve in taksonomije

Vse v vtičniku **Redirection** (izvozi pravila v `docs/redirection-<datum>.json`):

| Pravilo | Odločitev |
|---|---|
| `/4017-2/` → `/`, `/guess-nakit/` → `/` | #27 |
| regex `^/kategorija-izdelka/(.*)$` → `/$1` | #9 |
| `/uncategorized/` → `/swarovski-elements/` | #14 |
| Oznake izdelkov: `zarocni-prstan`, `zarocni-prstani` → `/zarocni-prstani/`; `zenski-prstan` → `/ostali-prstani/zenski-prstani/`; `redeco-zlato`, `rose-gold` → `/oznaka-izdelka/rdeco-zlato/`; `brili`, `brilijanti`, `diamanti` → `/ostali-prstani/prstani-z-briljanti/`; `pose` → `/oznaka-izdelka/posebni-prstan/` | #11 (natančno v `redirect-map.csv`) |
| `/cene-porocnih-prstanov-v-letu-2024/` → `/cena-porocnih-prstanov/` | #8, **šele po** prenosu vsebine (sklop 5) |

**Ostale nastavitve:**
- **Izdelki na odstranjenih oznakah:** izdelke z `redeco-zlato` in `rose-gold` prestavi na `rdeco-zlato`, z `pose` na `posebni-prstan`. Oznak ne briši.
- **Yoast:**
  - arhivi avtorjev izklopljeni (#13; Yoast jih sam preusmeri na domačo);
  - materialne oznake izdelkov (`belo-zlato`, `rumeno-zlato`, `rdeco-zlato`, `beli-/rumeni-/rdeci-porocni-prstan`, `kombinirani-porocni-prstan`, `posebni-prstan`, `prstan-iz-srebra-in-zlata`, `prstan-z-naravnimi-kamni`, `zarocni-in-porocni-prstan`) dobijo `noindex, follow` (#11);
  - `/cart/`, `/checkout/` in `/my-account/` dobijo noindex (#15).
  - Vse te izginejo iz sitemapa.
- **Oznake bloga in kategorije bloga** (#10) ter MANUAL REVIEW za 118 (#17), 067/068 (#18) in članke Trendi (#12): **še ne.** Čakajo izvoz GSC, Milan ga pošlje.

**Preveri:** skripta prebere `redirect-map.csv` in za vsako vrstico z ACTION 301 preveri, da OLD (na `zlatar.ddev.site`) vrne **en** 301 na NEW in NEW vrne 200. Za KEEP mora isti URL vrniti 200. Rezultat shrani v `docs/redirect-preverba-<datum>.txt`.

---

## 3. Izdelki (`izdelki-popravki.csv`, 251 vrstic)

Stolpci so ID, URL (ostane), IME ZDAJ, IME NOVO (= H1), SEO TITLE, H1, ALT GLAVNE SLIKE, PRIMARNA KATEGORIJA, DODAJ KATEGORIJE, ODSTRANI KATEGORIJE in OPOMBA.
- Imena in alti so sestavljeni **samo iz obstoječega imena in oznak** (#22–#24). Kjer je material dodan iz oznak, to piše v OPOMBI.
- 4 vrstice z »preveri« ali »nejasne« pusti in jih pokaži Milanu (147, 151, 192, x3).

1. **Uvoz** z WP-CLI skripto (`scripts/izdelki-popravki.php`), ki prebere CSV:
   - `post_title` = IME NOVO;
   - Yoast `_yoast_wpseo_title` = SEO TITLE (brez `%%sitename%%`);
   - alt glavne slike (`_wp_attachment_image_alt` na `_thumbnail_id`) = ALT;
   - Yoast primarna kategorija `_yoast_wpseo_primary_product_cat` = PRIMARNA;
   - dodaj in odstrani kategorije (#19–#21).
   - **Slug ostane.** Pred uvozom suh tek (`--dry-run`), ki izpiše razlike.
2. **H1 na strani izdelka** = celotno ime (#22), ne skrajšano »445 Poročna prstana«. Spani ostanejo zaradi oblikovanja, a s presledkom.
3. **Vrsta prstana je vedno vidna** (#16). V kartici, H1, altu in vrstici »Model« naj piše tip, npr. »Zaročni prstan · model 433«. Tako se seriji 432–442 ne zamenjata.
4. **Meta description izdelka** ostane predloga, a z novim imenom.
5. **Drobtine v JSON-LD:** Domov › kategorija (primarna) › izdelek, ime brez `&#8211;` (dekodiraj). Ujemati se morajo z vidnimi.
6. **Product shema** (#25), v child temi prek Yoastovega grafa (`wpseo_schema_graph_pieces` ali `wpseo_schema_webpage`):
   - polja: `name`, `image`, `sku` in `mpn` = model, `brand` = `#organization`, `category` = primarna, `material` iz oznak (»belo zlato« …), `url`;
   - **brez `offers`, `aggregateRating` in `review`**;
   - `@id` = URL + `#product`, `mainEntityOfPage` = ItemPage.
7. **Srce na karticah kataloga** (#50): isti `<button class="zd-srce">` z `aria-label`, `aria-pressed`, območje dotika ≥ 44 px.
8. **Unikatnih opisov ne pišemo** (#28), dokler naročnik ne pošlje podatkov.

**Preveri:**
- 10 naključnih izdelkov in 433 (oba), 152 ter 445: title, H1, alt, primarna kategorija, drobtine (vidne in JSON) in Product brez offers (Rich Results Test lokalno: shrani HTML in ga prilepi kot kodo).
- `/ostali-prstani/prstani-z-briljanti/` ima 40 izdelkov več kot prej (oziroma vse s kamni).

---

## 4. Naslovi, meta in domača

**SEO title** (Yoast, celoten naslov brez dodajanja imena strani):

| URL | SEO title |
|---|---|
| `/` | Poročni prstani po meri \| Zlatarna Brežnik Žalec pri Celju |
| `/porocni-prstani/` | Poročni prstani – modeli iz belega, rumenega in rdečega zlata \| Brežnik |
| `/porocni-prstani/unikatni-porocni-prstani/` | Unikatni poročni prstani po meri \| Zlatarna Brežnik |
| `/zarocni-prstani/` | Unikatni zaročni prstani po meri \| Zlatarna Brežnik |
| `/ostali-prstani/zenski-prstani/` | Unikatni ženski prstani po meri \| Zlatarna Brežnik |
| `/ostali-prstani/prstani-z-briljanti/` | Prstani z briljanti in diamanti \| Zlatarna Brežnik |
| `/cena-porocnih-prstanov/` | Cena poročnih prstanov: kaj vpliva na ceno? \| Brežnik |
| `/cena-zarocnih-prstanov/` | Cena zaročnega prstana \| Vodnik Zlatarne Brežnik |
| `/kontakt/` | Kontakt \| Zlatarna Brežnik Žalec pri Celju |
| `/predstavitev-podjetja/` | Zlatarstvo Brežnik Žalec pri Celju \| Od leta 1999 |
| `/zlatarna-celje/` (nova) | Zlatarna pri Celju – obiščite nas v Žalcu \| Brežnik |

- Naslov `/porocni-prstani/` ima 71 znakov in ga bo Google morda skrajšal. Pomembni del je na začetku.
- **Meta description:**
  - obstoječi opisi na dev so dobri, ostanejo;
  - napiši unikatne za 5 člankov brez opisa (`/5-stvari-…`, `/kako-uskladiti-…`, `/raje-porocni-ali-zarocni-…`, `/simbolika-…`, `/trendi-moskih-…`), 140–155 znakov, iz vsebine članka.
- **og:title** naj bo enak SEO naslovu. **og:image:** vsaka kategorija svojo sliko (1200×630, iz obstoječih fotografij kategorije).

**Domača:**
- H1 »Poročni prstani, ki pripovedujejo vajino zgodbo.« (#31);
- pod njim stavek »Unikatni, ročno izdelani poročni prstani po meri iz naše delavnice v Žalcu pri Celju.«;
- gumbi »Oglejte si poročne prstane« → `/porocni-prstani/` in »Oglejte si zaročne prstane« → `/zarocni-prstani/` (#32). Gumb v heroju naj vodi na poročne;
- Guess: pasica ostane, **brez povezave** (#27);
- v »Zanimivosti« zamenjaj članek »Cene poročnih prstanov v letu 2024« s `/cena-porocnih-prstanov/`.

**Interne povezave** (navodila, točka 21). Opisna sidra, brez pretiravanja:
- domača → poročni, unikatni poročni, zaročni, katalog;
- poročni → unikatni, cena poročnih, graviranje, katalog, kontakt;
- zaročni → cena zaročnih, barve diamanta, prstani z briljanti, kontakt;
- članki → ustrezna komercialna stran.

---

## 5. Vsebina (samo potrjena dejstva)

**Potrjeno:**
- Zlatarna Brežnik, Dejan Brežnik s.p., Šlandrov trg 39, 3310 Žalec, dobrih 10 km od Celja.
- Od leta 1999; začeli v Celju, danes samo v Žalcu.
- Ročna izdelava, izdelava po meri, osebni posvet.
- Belo, rumeno, rdeče in kombinirano zlato; prstani z briljanti in diamanti (iz kataloga).
- Delovni čas pon–pet 8–12 in 14–17, sobota po dogovoru.
- Telefona 03 710 40 60 in 041 424 648, info@zlatarna-breznik.si.

**Ne piši** (čaka naročnika):
- karatnost, rok izdelave, garancija, cena graviranja, parkiranje;
- cene in razponi (#35);
- »od 200 €« in »dve plači« (#34);
- srebro, les in platina, dokler niso potrjeni.

| Stran | Kaj |
|---|---|
| `/3902-2/` (#33) | Na novo, H1 »Najlepši unikatni prstani za poroko«. Brez »v oddaji«, Tiffany, Cartier in Bvlgari, tabele cen, generičnih citatov in ponavljanja. Vsebina: izbor **dejanskih** modelov iz kataloga z njihovimi fotografijami (npr. 445, 444, 438, 152, 163, 126) in opisom samo iz imena; vrste zlata; ročna izdelava; unikatnost; nasveti pri izbiri (širina, udobje, zlato za vsak dan, gravura, brez cen); povezave na katalog in unikatne poročne; CTA za posvet. 5 base64 slik zamenjaj s slikami iz knjižnice (`width`, `height`, `srcset`, `loading="lazy"`). Avtor: Zlatarna Brežnik (#37). URL ostane. |
| `/cena-porocnih-prstanov/` (#8, #34, #35) | Evergreen, H1 »Cena poročnih prstanov«. Teme: kaj vpliva na ceno, vrsta in količina zlata, širina in debelina, površinska obdelava, briljanti in drugi kamni, zahtevnost izdelave, graviranje, izdelava po meri, kako pridobiti ponudbo (obrazec, telefon, obisk). Iz članka 2024 prenesi samo uporabne dele o prstanih, brez stroškov poroke. **Nato** 301 iz sklopa 2. |
| `/cena-zarocnih-prstanov/` | H1 »Cena zaročnega prstana«. Odstrani »… v letu 2020« in druge zastarele formulacije. Evergreen, brez cen. |
| `/porocni-prstani/unikatni-porocni-prstani/` | Namenska stran, H1 »Unikatni poročni prstani po meri«. Postopek: ideja in skica → izbor materiala → oblikovanje → ročna izdelava → pomerjanje → končni izdelek. Primeri iz kataloga (kategorija unikatni) s fotografijami. CTA za posvet. Povezave nanjo z domače, `/porocni-prstani/`, `/predstavitev-podjetja/` in iz člankov. Ne preusmerjaj. |
| `/ostali-prstani/zenski-prstani/` | H1 »Unikatni ženski prstani«, uvod 100–200 besed (ženski prstani, zlati ženski prstani, iz belega zlata) in izdelki pod njim. |
| `/porocni-prstani/` | H1 »Poročni prstani za vajino zgodbo«, konkreten uvod (ročna izdelava, po meri, Žalec, belo, rumeno, rdeče in kombinirano zlato, briljanti, osebni posvet). **Filtri** po materialu (#52) kot UX: JavaScript ali `?material=`, ki ima `noindex` in canonical na `/porocni-prstani/`, brez novih URL-jev v sitemapu. |
| `/zlatarna-celje/` (#36) | Nova stran, H1 »Zlatarna pri Celju – obiščite nas v Žalcu«. Jasno: trgovina je **v Žalcu**, dobrih 10 km od Celja, v Celju ni poslovalnice. Naslov, telefon, delovni čas, zemljevid (fasada), poročni in zaročni prstani, osebni posvet. Odstavek o parkiranju in poti **izpusti**, dokler ga naročnik ne pošlje (#44). Povezava iz noge in s Kontakta. Dodaj v sitemap. |
| `/kontakt/` (#39, #53) | Viden delovni čas (enak kot v shemi). Obvezna polja označena z »*« in legendo. Stavek o zasebnosti s povezavo na Varovanje osebnih podatkov. Fokus na poljih: `outline: 2px solid #90703e`. Mod'Art se ne doda (#41). |
| Članki (#37) | Avtor v shemi in podpisu: **Zlatarna Brežnik** (Yoast filter `wpseo_schema_article`: `author` = `#organization`; byline v predlogi). |
| GEO | Na ključnih straneh kratki odgovori (1–3 stavki, nato podrobnosti) **samo na potrjena vprašanja**: Kje je Zlatarna Brežnik? Ali imate zlatarno v Celju? Katere vrste zlata uporabljate (barve, brez karatov)? Ali izdelujete zaročne prstane po meri? Kakšna je razlika med diamantom in briljantom (splošno znanje: briljant je diamant z briljantnim brusom)? Od česa je odvisna cena (brez zneskov)? FAQ vprašanja se med kategorijami ne smejo ponavljati. |

---

## 6. Strukturirani podatki

- **JewelryStore/Organization:**
  - `geo` iz Google profila (#43): place_id `ChIJCf_FfvtwZUcReHnal3fewYQ`, koordinate preberi iz profila, ne iz starega embed zemljevida;
  - `image` (fotografija zlatarne, ko jo pošlje naročnik, do takrat izpusti);
  - `sameAs`: Facebook in Google profil;
  - `openingHoursSpecification` ostane.
- **VideoObject** (#38) za `s2Mb0vOy48E` na `/` in `/predstavitev-podjetja/`:
  - `name` »Zlatarstvo Brežnik« (naslov na YouTubu, kanal »Trgovina Virum«);
  - `description`, `thumbnailUrl` `https://i.ytimg.com/vi/s2Mb0vOy48E/hqdefault.jpg`, `embedUrl`;
  - `uploadDate`: preberi z YouTuba, ne ugibaj; če ga ne dobiš, VideoObject počaka.
- **Product** in **drobtine:** sklop 3.
- **FAQPage** ostane, **AggregateRating ne.**

---

## 7. Dostopnost in UX (#47–#53)

Selektorji in podrobnosti so v `HITROST-UX-POROCILO.md`, poglavja 9–13.
- **#47:**
  - `#a07d45` in `#a8844e` → `#90703e` samo za drobno besedilo (≤ 14 px) in ozadje zlatih gumbov;
  - na kremnih ozadjih `#836739`;
  - veliki naslovi in okraski ostanejo.
- **#48 gumb menija** `button.zd-glava__odpri`:
  - besedilo »Meni« skrito z `.screen-reader-text` (ne `display:none`), ali `aria-label="Odpri meni"`;
  - območje dotika 44×44 s paddingom, ikona enaka;
  - ob odprtju fokus na prvo povezavo in ujet v meniju (ali `inert` na `main` in nogi);
  - pri zaprtem meniju `.sub-menu` tudi `visibility:hidden` (»Svet prstanov« ni fokusabilna).
- **»Preskoči na vsebino«** vidna ob fokusu.
- **#49 pasica:** na telefonu nižja, gumbi v eni vrstici, `aria-label` »Obvestilo o piškotkih«, `scroll-padding-bottom`, da fokus ne pade pod pasico.
- **#50 in #51 srca:**
  - območje dotika ≥ 44 px;
  - števec v dostopnem imenu (»Priljubljeno (2)«);
  - v oknu priljubljenih gumb »Pošlji povpraševanje za izbrane modele«, ki odpre `/kontakt/` in v sporočilo vstavi seznam modelov (prek `?modeli=` ali `localStorage`, brez strežnika).
- **Cilji dotika** v nogi in drobtinah ≥ 44 px visoki (padding, videz enak).
- **Video fasada:** `aria-label` vsebuje vidno besedilo (»Oglejte si film: …«), `iframe.title` iz podatkov.
- **Arhivi:** `section.zd-glava-strani` znotraj `<main>`. Na `/3902-2/` brez preskoka nivoja naslova.

---

## 8. Hitrost (#54)

1. **Ozadje glave podstrani:**
   - `ozadje-marmor-svetlo.jpg` → WebP (in mobilna različica 1024 px);
   - `<link rel="preload" as="image" fetchpriority="high">` na vseh predlogah z `zd-glava-strani`.
2. Logotip v glavi: brez `fetchpriority="high"`, WebP ali SVG.
3. Ozadji kolekcij na domači (127 KB in 89 KB JPG) → WebP z mobilno različico.
4. `loading="lazy"` za vse slike pod pregibom na domači (video sličica, skica, Guess pasica, noga). Prva 1–2 kartici v katalogu `eager`.
5. **Google Maps na Kontaktu:** fasada (statična slika in gumb »Prikaži zemljevid«, povezava »Odpri v Google Zemljevidih«). iframe šele po kliku.
6. **Trustindex:** `loader.js` šele, ko je `#mnenja` blizu pogleda (IntersectionObserver, `rootMargin: 600px`). Strežniški HTML viden brez JS (brez `opacity:0;height:0`).
7. Pisave: preload `jost-latin-ext` in `cinzel-400-600-latin-ext`.
8. Blokirajoči viri:
   - jQuery, jquery-migrate in Cookie Notice JS → `defer` ali noga (če lokalno še niso umaknjeni);
   - `@font-face` inline;
   - drobni Elementor CSS združeni ali v LSCache.
9. **LiteSpeed Cache:** predpomnilnik strani (deluje na LiteSpeed strežniku, ne na ddev), statični viri `max-age=31536000`.

**Preveri:** Lighthouse mobile na `/`, `/porocni-prstani/`, `/katalog/`, izdelku in `/3902-2/` (cilj LCP ≤ 2,5 s na strežniku z LSCache, CLS ≤ 0,1, TBT ≈ 0). Primerjaj s tabelo v auditu, poglavje 15.1.

---

## 9. Strežnik (mmedija.com in produkcija, ne ddev)

- **#1:** v cPanelu ali LiteSpeedu izklopi »reCAPTCHA protection« za `/kontakt/`. V CF7 vklopi honeypot ali Turnstile.
  - Preveri: `curl -A "Mozilla/5.0 … Chrome/140" https://zlatarna-breznik.mmedija.com/kontakt/ | grep -c "Bot Verification"` = 0.
  - Preveri še z UA PerplexityBot in ClaudeBot.
- **#6:** Duplicator in Elementor MCP Composer odstrani **ob prehodu** (lokalno lahko ostaneta za delo). `curl …/wp-json/ | grep -c "duplicator\|mcp-composer"` = 0.

---

## 10. Na koncu: poročilo Milanu

Kratko, po točkah iz navodil (točka 27):
1. kaj si spremenil;
2. katere URL-je si ohranil;
3. katere preusmeritve si dodal;
4. katere strani si vsebinsko prenovil;
5. katere SEO naslove in opise si spremenil;
6. kaj si naredil z oznakami;
7. katere podvojene izdelke si našel in kaj je z njimi;
8. kaj si naredil s shemo;
9. katere optimizacije hitrosti so narejene (meritve pred in po);
10. kaj še zahteva ročni pregled (MANUAL REVIEW, 4 izdelki z opombo, GSC, podatki naročnika).

Pri vsaki točki navedi, kako je preverjeno (ukaz ali posnetek). Kar ni narejeno ali ni preverjeno, napiši izrecno.
