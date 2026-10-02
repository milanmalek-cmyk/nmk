# Odločitve – Zlatarna Brežnik

Milan, 2. 10. 2026, iz vprašalnika »Odločitve za Zlatarno Brežnik«. Številke se ujemajo z vprašalnikom.

## Tehnika in prehod

| # | Odločitev |
|---|---|
| 1 | LiteSpeed reCAPTCHA na `/kontakt/` **izklopimo**, spam ustavimo na obrazcu (honeypot ali Turnstile). |
| 2 | Gostovanje in DNS ureja Multimedija, dostopi so. |
| 3 | GSC: Milan ima polni dostop. Ima tudi dostop do **Google Business Profila** in **Google Analytics** (2. 10. 2026). |
| 4 | Dev domeni dobita `X-Robots-Tag: noindex, nofollow`, vezan na ime domene. |
| 5 | Valuta WooCommerce → **EUR**. |
| 6 | Pred objavo odstranimo **Duplicator** in **Elementor MCP Composer**. |
| 7 | Prehod na produkcijo, **ko naročnik potrdi vsebino**. |

## URL-ji in preusmeritve

| # | Odločitev |
|---|---|
| 8 | `/cene-porocnih-prstanov-v-letu-2024/`: vsebino prenesemo v `/cena-porocnih-prstanov/`, nato 301. |
| 9 | Eno pravilo 301 `^/kategorija-izdelka/(.*)$ → /$1`. |
| 10 | Oznake bloga: s kliki v GSC → 301 na glavno stran, ostale `noindex`. **Čaka izvoz GSC.** |
| 11 | Oznake izdelkov: zaročne in ženske 301 na kategorijo; dvojniki in napake 301 na pravilno; materialne `noindex` in ostanejo kot filtri. |
| 12 | Trendi 2020/2021: en posodobljen članek, drugi URL 301. **Kateri ostane, odloči GSC.** |
| 13 | Arhivi avtorjev v Yoastu **izklopljeni**. |
| 14 | `/uncategorized/` → 301 na `/swarovski-elements/`. |
| 15 | `/cart/`, `/checkout/`, `/my-account/`: `noindex` in iz sitemapa, strani ostanejo. |

## Izdelki

| # | Odločitev |
|---|---|
| 16 | Serija 432–442: oba URL-ja ostaneta, vrsta prstana (zaročni / poročna prstana) je vedno v imenu, naslovu, H1 in altu. |
| 17 | 118: isti model, URL z več kliki v GSC ostane, drugi 301. **Čaka izvoz GSC.** |
| 18 | 067/068: isti model, eden 301 na drugega (privzeto ostane 067, razen če GSC pokaže drugače). |
| 19 | 152: primarna Poročni prstani, ostane Z briljanti, odstranimo Ostali prstani. |
| 20 | Vsi poročni: primarna Poročni prstani, »Ostali prstani« samo, kjer ni druge kategorije (39 izdelkov). |
| 21 | Vsi s kamni (briljanti, diamanti) dobijo kategorijo Prstani z briljanti (40 izdelkov). |
| 22 | Title `445 – Poročna prstana iz belega zlata z briljanti | Brežnik`, H1 enak brez `| Brežnik`. |
| 23 | Alt iz imena in oznak: »Poročna prstana model 445 iz belega zlata z briljanti – Zlatarna Brežnik«. |
| 24 | Popravimo tipkarske napake v imenih, URL-ji ostanejo. |
| 25 | Product shema z modelom, materialom in sliko, **brez cene**. |
| 26 | Swarovski elements ostanejo. |
| 27 | **Stran Guess ni potrebna.** Guess je samo pasica na domači, brez povezave. `/guess-nakit/` v smeti, `/4017-2/` (stari »Guess«) in `/guess-nakit/` → 301 na domačo. |
| 28 | Unikatne opise izdelkov pišemo, ko naročnik pošlje karatnost, širino, profil in kamne za ključne modele. |

## Naslovi in vsebina

| # | Odločitev |
|---|---|
| 29 | Domača: »Poročni prstani po meri \| Zlatarna Brežnik Žalec pri Celju«. `/porocni-prstani/`: »Poročni prstani – modeli iz belega, rumenega in rdečega zlata \| Brežnik«. |
| 30 | Ostali naslovi točno po navodilih. |
| 31 | H1 domače »Poročni prstani, ki pripovedujejo vajino zgodbo.« in stavek »Unikatni, ročno izdelani poročni prstani po meri iz naše delavnice v Žalcu pri Celju.« |
| 32 | Gumbi »Oglejte si poročne prstane« in »Oglejte si zaročne prstane«. |
| 33 | `/3902-2/` napišemo na novo iz dejanskih prstanov, brez cen in tujih znamk. URL ostane. |
| 34 | »od 200 € dalje« in »dve mesečni plači« umaknemo, dokler naročnik ne potrdi. |
| 35 | Na straneh cen **ni cen ali razponov**, samo dejavniki cene in poziv za ponudbo. |
| 36 | Nova stran `/zlatarna-celje/`. |
| 37 | Avtor člankov je **Zlatarna Brežnik** (podjetje). |
| 38 | VideoObject za YouTube video. |

## Podatki o zlatarni

| # | Odločitev |
|---|---|
| 39 | Delovni čas drži: pon–pet 8–12 in 14–17, sobota po dogovoru, nedelja in prazniki zaprto. Prikažemo ga vidno na Kontaktu. |
| 40 | Mobilna 041 424 648 ostane javna. |
| 41 | Mod'Art Domžale ni več aktualen. Ne dodajamo ga, iz imenikov ga odstranimo (po objavi). |
| 42 | Začetek v Celju (1999), danes samo Žalec: drži. |
| 43 | Koordinate iz Google profila zlatarne. |
| 44 | Parkiranje in prihod: **vpraša se naročnika.** |
| 45 | Imenike uredimo **po objavi**. |

## Videz in uporabnost

| # | Odločitev |
|---|---|
| 46 | Presledki med deli naslovov: popravi. |
| 47 | `#90703e` za drobno zlato besedilo in zlate gumbe. |
| 48 | Gumb menija: večje območje dotika in dostopno ime. |
| 49 | Nižja piškotna pasica na telefonu, gumbi v eni vrstici. |
| 50 | Srce tudi na karticah v katalogu in kategorijah. |
| 51 | Gumb »Pošlji povpraševanje za izbrane modele« vstavi seznam priljubljenih v obrazec. |
| 52 | Filtri po materialu na `/porocni-prstani/`, brez novih indeksiranih URL-jev. |
| 53 | Obrazec: vidna oznaka obveznih polj in stavek o zasebnosti s povezavo. |
| 54 | Hitrost: vse predlagano (zemljevid in mnenja ob kliku oz. drsenju, WebP ozadje s prednalaganjem, predpomnilnik strani). |
| 55 | Brez WhatsApp in Viber. |

## Še odprto

- ~~GSC~~ **rešeno 2. 10. 2026** (audit, poglavje 20): 15 oznak in kategorij bloga s kliki → 301, 17 brez klikov → noindex. Ostanejo `/118-porocna-prstana/`, `/068-porocna-prstana/` in `/trendi-zarocnih-prstanov-za-leto-2021/`.
- **Potrjeno (Milan, 2. 10. 2026):** 301 tudi za oznake z veliko kliki, `/oznaka-izdelka/zarocni-prstan/` (68 klikov, pol. 2,2), `/tag/zarocni-prstan/` (53), `/tag/zarocni-prstani/` (33) → `/zarocni-prstani/` in `/tag/moski-porocni-prstani/` (32) → `/porocni-prstani/`. Po pravilu #10/#11 gredo na 301, a imajo več klikov kot ciljna stran.
- **Zaročni + Ostali prstani** (približno 18 izdelkov): ali velja isto pravilo kot #20? V `izdelki-popravki.csv` je označeno, ni izvedeno.
- **Od naročnika:** parkiranje in prihod (#44), podatki o modelih (#28), potrditev vsebine pred prehodom (#7). Glej `POTREBUJEMO-OD-NAROCNIKA.md`.
