# Multimedija AI Office – Marketing in AI Redesign z Google Sheets

**Status (11. 10. 2026):** potrjeno in izvedeno M1–M4.

- naloga v ločenem stolpcu;
- stolpci O–W, zavihka »AI ocene« in »Dnevnik«;
- zapolnjevanje praznih celic s preverjenimi podatki;
- neobvezne spremembe 3.3;
- ZIP-i v gitu.

Test GEOFOTO: ocena 81/100, paket za ChatGPT. Čaka M5 (dnevna rutina in združitev v glavno vejo).
**Preglednica:** »Podjetja Redesign« (`1kk_e0gYn79nxNZpbfxxVvlqYwNwJxvlOFRpkUdbGnH8`) – ostane glavna evidenca.

## 1. Ugotovljeno stanje

**Povezava.** Branje prek konektorja Google Sheets deluje (OAuth konektor claude.ai). Žetoni niso v repozitoriju
niti v okolju, preglednica ni javno objavljena.

**Struktura preglednice:**

| Zavihek | Vsebina | Opombe |
|---|---|---|
| Predizbor 30 | tabela `LeadPreselection` A1:N31: 30 podjetij, 14 stolpcev (Podjetje, Kraj, Dejavnost, Spletna stran, Prihodki 2025, Čisti dobiček 2025, Marža, Zaposleni, Cenovna skupina, **Status**, Ugotovitev / razlog, Predlagan naslednji korak, Vir financ, Vir strani) | prva vrstica zamrznjena; pogojno oblikovanje stolpca Status samo za vrstice 2–31 |
| Povzetek | ročno vpisan povzetek (30 imen, 15 s financami, 3 prednostni: GEOFOTO, SEAL & TRADE, ROBIEN; PRECIZ izločen) | statične vrednosti, ne formule |
| Merila in postopek | 10 pravil: lokacija Maribor ±50 km, prihodki 100.000–1.500.000 €, pozitiven dobiček vsaj 2 leti, dejanski vsebinski problem, ne prenavljaj sodobnih strani, komercialna korist, neposreden odločevalec, cenovni skupini A/B, statusi, **poln demo samo za najboljše 2–3** | to so pravila za ocenjevanje |

**Vrednosti v stolpcu Status:** PREDNOSTNO, PREVERI STRAN, PREVERI FINANCE, NI NUJNO,
IZLOČI – NOVA STRAN, IZLOČI – NIZEK DOBIČEK, IZVEN VELIKOSTNEGA FILTRA, NEPREVERJENO.

**Opažanja, pomembna za integracijo:**

1. **Status je ocena podjetja, ne naloga.** Če bi vanj vpisali »ZA ANALIZO«, bi izgubili ugotovitev (npr. PREDNOSTNO). Predlog: ločen stolpec »Naloga za Claude«.
2. **Ni matične številke.** Dvojnike lahko zato prepoznamo samo po imenu in domeni, ki sta nezanesljiva (»Mizarstvo Maribor«, »Mizart mizarstvo«). Matična številka je najboljši ključ.
3. **Časovni pas je `Etc/GMT`, lokalizacija `en_GB`.** Datume bom pisal kot besedilo `LLLL-MM-DD`, da se ne zamenjajo dan in mesec.
4. **Pogojno oblikovanje sega samo do vrstice 31.** Nove vrstice ne dobijo barv statusa.
5. **BIO-SAD (prvi testni projekt) ni v preglednici.**
6. **15 podjetij je NEPREVERJENO** – brez prihodkov, dobička in domene. To je glavno delo za samostojne raziskave.

**Stanje projekta:**

- modul `ai-office/moduli/redesign/` deluje;
- BIO-SAD je pripravljen do paketa za ChatGPT (F5) in čaka na potrditev dizajna (V1);
- veja `claude/quirky-shannon-vydgbs` je usklajena z GitHubom; glavna veja modula še nima.

## 2. Arhitektura

```
Google Sheets (glavna evidenca – vi dodajate, popravljate, označite nalogo)
   │  branje / pisanje samo prek konektorja, samo v dovoljene stolpce
   ▼
Claude: /podjetja · /analiziraj-podjetje · /redesign · /prodajne-priloznosti · /pripravi-ponudbo · /marketing-porocilo
   │  raziskava, ocena, materiali
   ▼
ai-office/projekti/<stranka>/…  (git: analiza, dejstva, besedila, slike, poziv, naslovnica, prodaja)
   │  ZIP → pošiljanje v pogovor (tudi na telefon)
   ▼
ChatGPT (vizualni koncept) → Claude Artifacts (HTML z originalnimi slikami) → predogled → povezava nazaj v Sheets
```

- **Nov modul `ai-office/moduli/marketing/`:**
  - `config/evidenca.json`: ID preglednice, zavihki in vloge stolpcev po imenu glave, ne po črki;
  - `scripts/evidenca.py`: razčlenitev preglednice, ključi, dvojniki, »načrt pisanja« z varovali;
  - `scripts/ocena.py`: izračun ocene 0–100;
  - predloge.
- **Povezava z redesignom:** `projekt.json` → `stranka.crm_id` = ključ podjetja v preglednici.
  `/redesign` sprejme tudi ime podjetja iz preglednice.
- **Pravila za pisanje** so v kodi (`evidenca.py`), ne samo v navodilih. Vsak zapis se pred izvedbo preveri proti
  sveži kopiji preglednice.

## 3. Predlagane spremembe preglednice (čakajo potrditev)

Nič se ne briše, ne premika in ne preimenuje. Stolpci A–N ostanejo, kot so.

### 3.1 Novi stolpci v »Predizbor 30« (O–W, tabela se razširi do W)

| Stolpec | Ime | Kdo piše | Vrednosti |
|---|---|---|---|
| O | Naloga za Claude | **vi** | spustni seznam: OCENI · ZA ANALIZO · PRIPRAVI PONUDBO · USTAVI |
| P | Matična številka | Claude, samo če je prazno | 10 števk (ključ za dvojnike) |
| Q | AI ocena | Claude | 0–100 (podrobnosti v zavihku »AI ocene«) |
| R | Stanje priprave | Claude | OCENJENO · V TEKU · PAKET PRIPRAVLJEN · ČAKA DIZAJN · HTML PRIPRAVLJEN · PREDOGLED OBJAVLJEN · NAPAKA |
| S | Datum analize | Claude | LLLL-MM-DD |
| T | Mapa materialov | Claude | povezava na mapo projekta na GitHubu |
| U | Predogled | Claude | povezava na predogled (zaseben Artifact, kasneje vaš strežnik) |
| V | Prodajna faza | Claude samo »PREDLOG PRIPRAVLJEN«, ostalo **vi** | PREDLOG PRIPRAVLJEN · PREGLEDANO · POSLANO · ODGOVORIL · ŽELI PONUDBO · PRIDOBLJENO · ZAVRNJENO |
| W | Naslednji kontakt | Claude predlaga, vi popravite | LLLL-MM-DD – kratek predlog |

### 3.2 Nova zavihka

- **AI ocene** – ena vrstica na podjetje. Stolpci:
  - ključ in datum;
  - točke po skupinah: finance, spletna stran, poslovni potencial;
  - skupna ocena in predlagan status;
  - predlagana cenovna skupina;
  - obrazložitev, viri (URL-ji) in manjkajoči podatki;
  - razhajanja z vašimi vnosi (če najdem drugačen podatek, ga zapišem tu in ga ne prepišem).
- **Dnevnik** – ena vrstica na dogodek: datum, podjetje, kdo (Claude / vi), aktivnost, opomba, povezava.
  Iz njega nastane `/marketing-porocilo`.

### 3.3 Neobvezno (po vaši presoji)

- Pogojno oblikovanje Status razširiti na J2:J1000.
- Časovni pas preglednice nastaviti na `Europe/Ljubljana`.
- Povzetek povezati s formulami (štetje statusov in faz), da se ne vpisuje ročno.
- Dodati BIO-SAD kot vrstico (status: obstoječa stranka Multimedije, priprava do V1).

### 3.4 Pravila pisanja (v kodi)

1. Claude piše samo v svoje stolpce (P, Q, R, S, T, U, W, v V samo »PREDLOG PRIPRAVLJEN«) in v zavihka »AI ocene« in »Dnevnik«.
2. V stolpce A–N in O ne piše nikoli brez vaše potrditve. **Izjema za potrditev:** prazne celice v D–H, M, N
   (spletna stran, finance, viri) sme zapolniti s preverjenim podatkom in virom (vsak vpis gre v Dnevnik).
   Neprazne celice nikoli ne prepiše.
3. Pred vsakim zapisom ponovno prebere vrstico in jo poišče po ključu (matična ali ime + domena), ne po številki
   vrstice. Če ste vmes razvrstili ali vstavili vrstice, zapis ne zgreši podjetja.
4. Dvojnikov ne briše. Označi jih v Dnevniku in vam jih predlaga.
5. Neznano ostane neznano. Prazno polje ali »ni podatka« je boljše od ocene na pamet (pravilo 9 iz »Merila«).

## 4. Ocena 0–100 (po zavihku »Merila in postopek«)

| Skupina | Točke | Merila |
|---|---|---|
| **Finančna sposobnost** | 30 | prihodki v ciljnem razponu 100.000–1.500.000 € (10) · pozitiven dobiček vsaj 2 leti (10) · marža in trend zadnjih let (10) |
| **Spletna stran – potreba po prenovi** | 40 | zastarelost dizajna (10) · mobilna izkušnja (10) · SEO in GEO (8) · predstavitev izdelkov/storitev, besedila, reference (7) · pot do povpraševanja in obrazci (3) · hitrost (2) |
| **Poslovni potencial** | 30 | boljša stran prinese več kakovostnih povpraševanj (10) · jasen poslovni razlog (8) · dostop do lastnika/direktorja (6) · lokacija ±50 km od Maribora (3) · ustreza skupini A ali B (3) |

- **Izločitve** (ne glede na točke):
  - zelo sodobna stran → IZLOČI – NOVA STRAN;
  - dobiček negativen ali skoraj ničen 2 leti → IZLOČI ali PREVERI FINANCE;
  - izven območja → IZVEN OBMOČJA.
- **Predlagan status:** ≥ 70 PREDNOSTNO · 50–69 PREVERI · < 50 NI PRIORITETA. Status v stolpcu J spremenite vi.
  Claude ga samo predlaga v »AI ocene«.
- **Manjkajoči podatki:** točke se ne dodelijo, ocena je označena kot »delna«, manjkajoči podatki so našteti.
- **Viri financ:**
  - CompanyWall in bizi.si (kot jih že uporabljate);
  - AJPES, kjer je javno dostopen;
  - številke vedno z letom in povezavo.
- **Odločevalec:** samo javni poslovni podatki (zakoniti zastopnik iz registra, kontakt s strani podjetja).
  Zasebnih kontaktov ne iščem in ne ugibam.

## 5. Ukazi (Claude Code skills v `.claude/skills/`)

| Ukaz | Kaj naredi | Piše v Sheets |
|---|---|---|
| `/podjetja` | prebere preglednico in pokaže pregled: statusi, faze, naloge, ki čakajo, dvojniki, manjkajoči podatki. `/podjetja izvedi` opravi čakajoče naloge (OCENI, ZA ANALIZO) | samo pri `izvedi`, po pravilih 3.4 |
| `/analiziraj-podjetje <ime>` | finance in trend, hiter pregled strani (posnetek mobilno/namizje, tehnični SEO, hitrost, obrazci, reference), odločevalec, ocena 0–100 z viri → `projekti/<stranka>/ocena-LLLL-MM-DD.md` | P (če prazno), Q, R = OCENJENO, S, W, »AI ocene«, Dnevnik |
| `/redesign <ime ali URL>` | obstoječi modul F0–F5 (raziskava, analiza, struktura, besedila, originalne slike, logotip, barve, SEO/GEO, smernice, poziv, ZIP); kasneje F6 HTML in F7 predogled | R, S, T, U, Dnevnik |
| `/prodajne-priloznosti` | razvrsti kandidate po oceni in merilih. Za najboljše 2–3 predlaga poln demo, za ostale kratko osebno povpraševanje (pravilo 10) | ne – samo poročilo |
| `/pripravi-ponudbo <ime>` | 3 koristi, kratek oseben predlog lastniku/direktorju, osnutek e-pošte, cenovna skupina, predlog naslednjega kontakta, ponudba (cene samo iz potrjenega cenika) → `07_prodaja/` | V = PREDLOG PRIPRAVLJEN, W, Dnevnik |
| `/marketing-porocilo [obdobje]` | aktivnosti, faze, odgovori, pridobljeni/zavrnjeni, zamujeni kontakti, naslednji koraki | ne |

**Nikoli brez vaše potrditve:**

- pošiljanje e-pošte ali ponudb (modul nima orodja za pošiljanje);
- objava predogleda;
- spreminjanje vaših podatkov;
- brisanje ali preurejanje stolpcev in zavihkov.

## 6. Samostojnost

| Brez potrditve | S potrditvijo |
|---|---|
| javne raziskave, ocene, zbiranje in prenos izbranih slik, analize, besedila, ZIP, osnutki prodaje, zapisi v svoje stolpce in zavihka »AI ocene«/»Dnevnik« | sprememba strukture preglednice, vpis v vaše stolpce, objava predogleda, pošiljanje, ponudba s cenami, poln demo za več kot 3 podjetja hkrati |

## 7. Avtomatizacija »ob naslednjem zagonu«

1. **Faza 1 – ročni zagon:** odprete Claude Code in vpišete `/podjetja izvedi`. Claude opravi vse naloge iz stolpca O.
2. **Faza 2 – dnevna rutina** (ko se faza 1 izkaže):
   - vsak delovnik zjutraj se samodejno zažene nova seja s konektorjem Google Sheets;
   - izvede `/podjetja izvedi` (največ 2 polna paketa na dan);
   - zapiše stanje v Sheets in vam pošlje obvestilo z ZIP-om.
   - **Pogoj:** modul mora biti na glavni veji repozitorija (združitev te veje), rutino pa potrdite vi.

## 8. Varnost

- **Danes:** dostop samo prek OAuth konektorja Google Sheets v claude.ai. Gesel in žetonov ni v gitu, v datotekah
  ali v okolju. Preglednica ostane zasebna, javne objave ni. ID preglednice je v `config/evidenca.json`
  (ni skrivnost, repozitorij je zaseben).
- **Kasneje v spletni aplikaciji AI Office:** Google Cloud *service account* z dostopom samo do te preglednice.
  Ključ je v upravitelju skrivnosti strežnika, nikoli v gitu.
- **Osebni podatki:** samo javni poslovni podatki (register, spletna stran podjetja), z virom.

## 9. Test na GEOFOTO (po potrditvi)

**Že preverjeno (samo branje):** vrstica 2 – GEOFOTO d.o.o., Slovenska Bistrica, geodetske storitve,
https://www.geofoto.si/:

- prihodki 2025: 1.288.896 €, čisti dobiček 2025: 164.887 €, marža 12,8 %, zaposleni 16,4;
- skupina B, status PREDNOSTNO.

**Koraki testa:**

1. `/podjetja`: branje, ključi, dvojniki, pregled.
2. `/analiziraj-podjetje GEOFOTO`:
   - finance s trendom (CompanyWall, bizi.si);
   - pregled strani: zastarele novice iz 2020 in ©2017 iz vaše ugotovitve, mobilno, SEO/GEO;
   - odločevalec in ocena 0–100 z viri.
3. Pred prvim zapisom vam pokažem **točno katere celice** bi zapisal (stolpec, vrednost, vir) in počakam na potrditev.
4. Po potrditvi: zapis. Nato po vaši odločitvi še `/redesign GEOFOTO` do ZIP-a za ChatGPT.

## 10. Izvajalni koraki (po potrditvi)

| Korak | Vsebina |
|---|---|
| M1 | modul `marketing` (config, `evidenca.py` z varovali, `ocena.py`, predloge) in 6 ukazov |
| M2 | test branja + `/analiziraj-podjetje GEOFOTO` → prikaz načrta zapisa → po potrditvi zapis |
| M3 | po potrditvi strukturne spremembe preglednice (3.1–3.3) |
| M4 | `/redesign GEOFOTO` do paketa za ChatGPT, zapis stanja in mape v Sheets |
| M5 | po nekaj uspešnih ročnih zagonih: predlog dnevne rutine in združitve v glavno vejo |

## 11. Odločitve, ki jih potrebujem

1. **Naloga:** ločen stolpec »Naloga za Claude« (priporočam) ali »ZA ANALIZO« neposredno v stolpcu Status?
2. **Novi stolpci O–W in zavihka »AI ocene« in »Dnevnik«:** jih lahko dodam (razširitev tabele `LeadPreselection`)?
3. **Prazne celice v vaših stolpcih** (spletna stran, finance, viri): jih sme Claude zapolniti s preverjenim
   podatkom in virom ali naj predlogi ostanejo samo v »AI ocene«?
4. **Neobvezno 3.3:** pogojno oblikovanje do vrstice 1000, časovni pas Ljubljana, formule v Povzetku, vrstica BIO-SAD?
5. **ZIP paketi:** pošiljanje v pogovor (privzeto) ali tudi shranjevanje v git za stalno povezavo
   (približno 8 MB na projekt)?
