---
name: analiziraj-podjetje
description: Multimedija AI Office – analiza in ocena potencialne stranke iz Google Sheets »Podjetja Redesign« - finance in trend (CompanyWall, bizi.si), pregled spletne strani (dizajn, mobilno, SEO/GEO, hitrost, ponudba, reference, obrazci), odločevalec, ocena 0–100 z viri, poročilo in zapis v preglednico. Uporabi za "/analiziraj-podjetje <ime>" ali ko je v preglednici naloga OCENI.
---

# /analiziraj-podjetje <ime>

- Navodila za preglednico: `ai-office/moduli/marketing/README.md`.
- Merila: `config/merila.json` (povzeto po zavihku »Merila in postopek«). Preberi tudi sam zavihek
  `'Merila in postopek'!A1:C20`, če se je morda spremenil.
- Spodaj `$K` = `ai-office/moduli/marketing`, `$R` = `ai-office/moduli/redesign`.

## 1. Podjetje

Preberi evidenco in `evidenca.py najdi $S/evidenca.json "<ime>"`. Natanko en zadetek, sicer vprašaj, katero podjetje.
Projektna mapa: `ai-office/projekti/<slug>/`.
- Slug izpelji iz domene ali imena, npr. `geofoto`.
- Če projekt že obstaja (`redesign/scripts/manifest.py najdi URL`), uporabi isto mapo.

## 2. Raziskava (samostojno, brez potrditev)

**Finance:**
- Stran CompanyWall iz stolpca »Vir financ« ali iskanje `https://www.companywall.si/iskanje?n=<ime>`.
- Iz HTML izlušči tabelo FINANČNI PODATKI: celotni prihodki, čisti poslovni izid in zaposleni za zadnja 3 leta,
  ter direktorja oziroma zastopnika in lastnike.
- Dopolnilno bizi.si (matična, dejavnost SKD, velikost).
- Vsaka številka mora imeti leto in URL.

**Spletna stran (samo naslovnica in nekaj ključnih podstrani):**
```bash
python3 -I $R/scripts/crawl.py URL $P/01_analiza --cache $P/01_analiza/.cache --max-strani 25
node $R/scripts/screenshot.mjs URL $P/01_analiza/posnetki --predpona obstojeca --sirine 1440,390 --jpg
```
Ocenjuješ:
- zastarelost (letnice v nogi, datumi novic, tehnologija);
- mobilno (viewport, posnetek 390);
- SEO in GEO (title, meta, H1, JSON-LD, alt);
- hitrost (velikost HTML in slik, število zahtev, če je enostavno);
- ponudbo, besedila in reference;
- obrazec ali pot do povpraševanja.
Posnetke si oglej.

**Odločevalec:** samo javni podatki (register: direktor, prokurist; kontakt na strani podjetja).

**Lokacija:** razdalja do Maribora (pravilo 1). Pri robnih primerih jo označi.

## 3. Ocena

1. Izpolni `$S/ocena.json` po `$K/scripts/ocena.py` (vsako merilo s točkami, dokazom in virom ali `null` + `manjka`).
2. Zaženi `python3 -I $K/scripts/ocena.py $S/ocena.json` in `--md` za tabelo. Napake popravi.
3. Izločitve po merilih: zelo sodobna stran, nizek ali negativen dobiček 2 leti, izven območja, izven velikosti.

## 4. Poročilo

`ai-office/projekti/<slug>/ocena-LLLL-MM-DD.md`:
- povzetek v 3 vrsticah;
- finance (tabela 3 let);
- spletna stran (ugotovitve z dokazi in posnetki);
- odločevalec;
- tabela ocene;
- predlagan status in cenovna skupina;
- naslednji korak (pravilo 10: poln demo samo za najboljše 2–3, sicer kratko osebno povpraševanje);
- viri.

Commit in push.

## 5. Zapis v preglednico

1. **Predlog za »Predizbor 30«:**
   - `maticna`, če je prazna;
   - prazne `spletna_stran`, `prihodki`, `dobicek`, `marza` (formula), `zaposleni`, `vir_financ`, `vir_strani`
     s preverjenimi podatki;
   - `ai_ocena` (formula XLOOKUP);
   - `stanje: OCENJENO`, `datum_analize`;
   - `naslednji_kontakt`, če je prazen;
   - `mapa`, če projekt obstaja.
2. `evidenca.py nacrt` → zapiši samo `nacrt`.
3. Vrstica v »AI ocene« (`vrstica_ai_ocene`, s povezavo na poročilo in razhajanji).
4. Vrstica v Dnevnik.
5. **Prvi zapis za posamezno podjetje** uporabniku najprej pokaži kot tabelo (celica, zdaj, novo) in počakaj
   na potrditev, razen če je naloga prišla iz `/podjetja izvedi` (takrat je uporabnik nalogo že naročil v preglednici).

## 6. Poročilo uporabniku

- ocena in predlagan status z razlogom;
- ključne ugotovitve;
- kaj manjka;
- razhajanja z evidenco;
- predlog naslednjega koraka.
