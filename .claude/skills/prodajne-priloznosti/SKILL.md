---
name: prodajne-priloznosti
description: Multimedija AI Office – razvrsti potencialne stranke iz Google Sheets »Podjetja Redesign« po AI oceni, statusu in merilih ter predlaga, komu narediti poln vizualni demo (najboljši 2–3), komu poslati kratko osebno povpraševanje in katera podjetja najprej oceniti. Samo branje. Uporabi za "/prodajne-priloznosti" ali vprašanja, katere stranke so najboljše.
---

# /prodajne-priloznosti

Samo branje. V preglednico ne piši ničesar. Navodila za branje: `ai-office/moduli/marketing/README.md`.

1. **Preberi** evidenco (`$S/evidenca.json`) in zavihek `'AI ocene'!A1:O` (zadnja ocena na podjetje).
2. **Izloči:**
   - status, ki se začne z IZLOČI, IZVEN, NI NUJNO;
   - nalogo USTAVI;
   - prodajno fazo PRIDOBLJENO ali ZAVRNJENO;
   - obstoječe stranke (te so v ločenem seznamu).
3. **Razvrsti:**
   1. AI ocena (višja prej; DELNA ocena za POLNO z enako vrednostjo);
   2. če ocene ni: status PREDNOSTNO pred PREVERI pred NEPREVERJENO;
   3. ob izenačenju: dobiček 2025 in cenovna skupina B pred A.
4. **Predlagaj po pravilu 10 iz »Merila in postopek«:**
   - **Poln demo** (`/redesign`): največ 3 najboljši z oceno ≥ 70 ali statusom PREDNOSTNO, ki še nimajo stanja
     PAKET PRIPRAVLJEN ali novejšega.
   - **Kratko osebno povpraševanje:** naslednjih 5. Za vsako predlagaj eno vrstico razloga, ki temelji na ugotovitvi.
   - **Najprej oceniti:** NEPREVERJENO z obetavno dejavnostjo. Predlagaj uporabniku, da jim v preglednici
     nastavi nalogo OCENI.
   - **Zamujeni kontakti:** »Naslednji kontakt« z datumom pred današnjim.
5. **Odgovor:** kratka tabela (podjetje, ocena, status, predlog, razlog) in en predlog naslednjega koraka.
