---
name: marketing-porocilo
description: Multimedija AI Office – poročilo o marketinških in prodajnih aktivnostih iz Google Sheets »Podjetja Redesign« (Dnevnik, prodajne faze, odgovori, pridobljeni in zavrnjeni projekti, zamujeni in prihodnji kontakti, pripravljeni paketi). Samo branje. Uporabi za "/marketing-porocilo [teden|mesec|LLLL-MM-DD:LLLL-MM-DD]".
---

# /marketing-porocilo [obdobje]

Samo branje. Privzeto obdobje: zadnjih 7 dni. Navodila za branje: `ai-office/moduli/marketing/README.md`.

1. **Preberi:**
   - evidenco (`$S/evidenca.json`);
   - `'Dnevnik'!A1:F` (datumi so prikazani kot dd/MM/yyyy);
   - `'AI ocene'!A1:O`;
   - `Povzetek!A20:B47` (števci po fazah in stanjih).
2. **Izračunaj za obdobje:**
   - aktivnosti iz Dnevnika po vrsti: ocene, paketi, predlogi, poslano, odgovori;
   - prehodi prodajnih faz;
   - stanje lijaka danes: PREDLOG PRIPRAVLJEN → … → PRIDOBLJENO / ZAVRNJENO, s številom in imeni;
   - odzivnost: odgovoril / poslano;
   - pridobljeni in zavrnjeni projekti z razlogom, če je v Dnevniku;
   - **zamujeni kontakti** (»Naslednji kontakt« pred danes) in **kontakti v naslednjih 7 dneh**;
   - pripravljeni paketi in predogledi, ki še niso bili poslani.
3. **Odgovor:**
   - kratek povzetek s številkami;
   - tabela lijaka;
   - seznam »za ta teden« (največ 5 konkretnih dejanj z imeni).
   Na željo uporabnika ga shrani v `ai-office/porocila/marketing-LLLL-MM-DD.md` in naredi commit.

Številke so štetja iz preglednice. Ne ocenjuj in ne izmišljuj vrednosti, ki jih ni.
