# Modul MARKETING – evidenca podjetij in prodaja

Google Sheets **»Podjetja Redesign«** je glavna evidenca (`config/evidenca.json`). Uporabnik v njej dodaja,
popravlja in odstranjuje podjetja ter v stolpcu **»Naloga za Claude«** označi, kaj naj Claude naredi.
Claude raziskuje, ocenjuje, pripravlja materiale in osnutke ter zapisuje stanje. Načrt:
`docs/MARKETING-INTEGRACIJA-NACRT.md`.

## Ukazi

| Ukaz | Namen |
|---|---|
| `/podjetja [izvedi]` | pregled evidence; z `izvedi` opravi čakajoče naloge |
| `/analiziraj-podjetje <ime>` | finance, spletna stran, odločevalec, ocena 0–100 z viri |
| `/redesign <ime ali URL>` | paket za prenovo naslovnice (modul `redesign`) |
| `/prodajne-priloznosti` | razvrstitev kandidatov in predlog, komu narediti poln demo |
| `/pripravi-ponudbo <ime>` | koristi, oseben predlog, e-pošta, cenovni razred, naslednji kontakt |
| `/marketing-porocilo [obdobje]` | aktivnosti, faze, odgovori, rezultati |

## Delo s preglednico (velja za vse ukaze)

Spodaj `$K` = `ai-office/moduli/marketing`, `$S` = začasna mapa seje (scratchpad).

### Branje

1. Naloži orodja konektorja Google Sheets (ToolSearch »google sheets«).
   Pred prvim **pisanjem** v seji preberi skill `anthropic-skills:google-workspace` in `references/sheets.md`.
2. `get_values` z obsegom `'Predizbor 30'!A1:W` (vedno z glavo). Rezultat shrani dobesedno v
   `$S/evidenca.json`. Če je bil rezultat samodejno shranjen v datoteko, uporabi to pot.
3. `python3 -I $K/scripts/evidenca.py pregled $S/evidenca.json` (ali `razcleni`, `naloge`, `najdi`).
   Stolpci se iščejo po imenu glave, zato premiki in preimenovanja let (»Prihodki 2026«) ne pokvarijo branja.

### Pisanje v »Predizbor 30«

1. **Tik pred zapisom** ponovno preberi evidenco (korak 2 zgoraj). Uporabnik je morda vmes kaj spremenil.
2. Predlog zapiši v `$S/predlog.json`, npr.
   `[{"podjetje": "GEOFOTO d.o.o.", "maticna": "…", "polja": {"stanje": "OCENJENO", "datum_analize": "2026-10-11"}}]`.
3. `python3 -I $K/scripts/evidenca.py nacrt $S/evidenca.json $S/predlog.json` vrne:
   - `nacrt`: obsege in vrednosti;
   - `zavrnjeno`: kaj ni dovoljeno in zakaj;
   - `razhajanja`: drugačen podatek, kot je v evidenci.
4. Vsak element `nacrt` zapiši z `update_formulas` (`range` in `values` iz načrta; `null` preskoči celico).
   Ničesar ne zapisuj mimo načrta.
5. Razhajanja zapiši v »AI ocene« (stolpec »Razhajanja z evidenco«) in jih omeni uporabniku. Ne prepiši jih.
6. Preveri z `get_values` zapisanih celic.

**Lastništvo stolpcev** (`config/evidenca.json`, potrdil uporabnik):

- **samo uporabnik:** Podjetje, Kraj, Dejavnost, Cenovna skupina, Status, Ugotovitev, Predlagan naslednji korak,
  Naloga za Claude.
- **Claude samo v prazno celico, s preverjenim podatkom in virom:**
  - Spletna stran, Prihodki, Čisti dobiček, Zaposleni, Vir financ, Vir strani;
  - Marža (vedno kot formula `=IFERROR(F{r}/E{r},"")`);
  - Matična številka (z apostrofom: `'5386683000`), Naslednji kontakt.
- **Claude:** AI ocena, Stanje priprave, Datum analize, Mapa materialov, Predogled.
- **Prodajna faza:** Claude sme vpisati samo »PREDLOG PRIPRAVLJEN« in samo v prazno celico.

**Oblike vrednosti:**

- Datumi: `"2026-10-11"` (preglednica jih prikaže kot dd/MM/yyyy).
- Finance kot števila (`1288895.77`), ne kot besedilo.
- AI ocena kot formula, ki bere zadnjo oceno iz »AI ocene«:
  `=XLOOKUP($A{r},'AI ocene'!$A$2:$A,'AI ocene'!$G$2:$G,"",0,-1)`.
- Mapa materialov: `github_projekti` iz nastavitev + `<stranka>/<projekt>`.

### Dodajanje v »AI ocene« in »Dnevnik«

- **AI ocene:**
  - Preberi `'AI ocene'!A1:O`, prva prazna vrstica je `r`.
  - Zapiši `vrstica_ai_ocene` iz `ocena.py` (zamenjaj `{r}`) z `update_formulas` v `'AI ocene'!A{r}:O{r}`.
  - Če je `r` zunaj tabele `AIOcene`, tabelo razširi z `updateTable` (`fields: "range"`, id in `sheet_id` iz nastavitev).
- **Dnevnik:**
  - Vsaka aktivnost je ena vrstica: `[datum, podjetje, "Claude", aktivnost, opomba, povezava]`.
  - Vpiše se na enak način (prva prazna vrstica, po potrebi razširi tabelo `Dnevnik`).
- **Nikoli** ne briši in ne prepisuj obstoječih vrstic v teh zavihkih. Nova ocena je nova vrstica (zgodovina ocen).

## Pravila

- **Viri:** finance s CompanyWall ali bizi.si (AJPES, kjer je javno), vedno z letom in URL-jem.
  Odločevalec samo iz javnega registra ali s strani podjetja. Zasebnih kontaktov ne iščem in ne ugibam.
- **Manjkajoče ostane manjkajoče.** Ocena je takrat DELNA. Neznanega ne pretvarjaj v potrjeno
  (pravilo 9 v »Merila in postopek«).
- **Brez potrditve:** raziskave, ocene, materiali, osnutki, zapisi v Claudove stolpce in zavihka »AI ocene« in
  »Dnevnik«.
- **S potrditvijo:**
  - spremembe strukture preglednice;
  - pisanje v uporabnikove stolpce (razen dovoljenih praznih celic);
  - objava predogleda;
  - poln demo za več kot 3 podjetja hkrati.
- **Pošiljanje** e-pošte in ponudb nikoli: modul nima orodja za pošiljanje, uporabnik pošlje sam.
- Na en zagon največ 2 polna paketa za prenovo (`omejitve` v nastavitvah).

## Skripte

| Skripta | Namen |
|---|---|
| `scripts/evidenca.py` | razčlenitev evidence po imenih stolpcev, ključi in dvojniki, čakajoče naloge, varen načrt zapisa |
| `scripts/ocena.py` | ocena 0–100 po `config/merila.json`, popolnost, predlagan status, vrstica za »AI ocene«, tabela za poročilo |
