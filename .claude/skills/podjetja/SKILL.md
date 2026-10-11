---
name: podjetja
description: Multimedija AI Office – pregled evidence potencialnih strank v Google Sheets »Podjetja Redesign« (statusi, stanje priprave, prodajne faze, čakajoče naloge, dvojniki, manjkajoči podatki). Z argumentom »izvedi« opravi čakajoče naloge iz stolpca »Naloga za Claude« (OCENI, ZA ANALIZO, PRIPRAVI PONUDBO). Uporabi za "/podjetja", "/podjetja izvedi" ali vprašanja o seznamu podjetij.
---

# /podjetja – pregled evidence in izvajanje nalog

Navodila za branje in pisanje: `ai-office/moduli/marketing/README.md`, razdelek »Delo s preglednico«. Upoštevaj jih natančno.

## Brez argumenta: pregled (samo branje)

1. Preberi evidenco v `$S/evidenca.json`, nato
   `python3 -I ai-office/moduli/marketing/scripts/evidenca.py pregled $S/evidenca.json`.
2. Uporabniku kratko poročaj:
   - število podjetij in statusi;
   - čakajoče naloge (vrstica, naloga, podjetje);
   - stanje priprave, prodajne faze in najvišje AI ocene;
   - možni dvojniki (samo predlagaj, nikoli ne briši);
   - koliko podjetij nima financ, spletne strani ali matične številke.
3. Predlagaj naslednji korak, npr. »3 naloge čakajo – zaženi `/podjetja izvedi`«.
4. V preglednico ne piši ničesar.

## `izvedi`: opravi čakajoče naloge

1. `evidenca.py naloge $S/evidenca.json` vrne seznam. Naloga USTAVI se nikoli ne izvaja.
2. Vrstni red: najprej OCENI, nato ZA ANALIZO, nato PRIPRAVI PONUDBO.
3. Na en zagon največ 2 nalogi ZA ANALIZO (`omejitve.polnih_paketov_na_zagon`). Ostale ostanejo za naslednji zagon.
4. Za vsako nalogo:
   - Ob začetku zapiši stanje »V TEKU« (prek načrta zapisa) in vrstico v Dnevnik.
   - **OCENI** → postopek `/analiziraj-podjetje` (skill `analiziraj-podjetje`). Konec: stanje OCENJENO.
   - **ZA ANALIZO** → najprej ocena, če je še ni ali je starejša od 90 dni.
     - Če je predlagan status izločitev (npr. IZLOČI – NOVA STRAN), se ustavi. Stanje: OCENJENO, v Dnevnik pa razlog.
     - Sicer `/redesign <podjetje>` (skill `redesign`) do paketa za ChatGPT. Konec: stanje PAKET PRIPRAVLJEN,
       Mapa materialov, ZIP poslan uporabniku.
   - **PRIPRAVI PONUDBO** → postopek `/pripravi-ponudbo` (skill `pripravi-ponudbo`). Konec: prodajna faza PREDLOG PRIPRAVLJEN.
   - Ob napaki: stanje NAPAKA in vzrok v Dnevnik. Nadaljuj z naslednjo nalogo.
5. Ob koncu enotno poročilo:
   - kaj je narejeno, povezave in ZIP-i;
   - kaj čaka uporabnika (potrditev dizajna, pregled osnutkov);
   - kaj je ostalo za naslednji zagon.

Uporabnikovih stolpcev (tudi »Naloga za Claude«) ne spreminjaj. Naloga je opravljena, ko je stanje ustrezno
zapisano. Uporabnik nalogo ponovi tako, da izprazni »Stanje priprave«.
