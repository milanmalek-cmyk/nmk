# Barve, pisave in logotip – BIO-SAD d.o.o.

Vir: `01_analiza/brand.json` (CSS obstoječe strani in logotip), kontrasti po WCAG 2.1.

## Barvna paleta

| Vloga | HEX | Izvor | Uporaba v novem dizajnu |
|---|---|---|---|
| Zelena BIO-SAD (glavna) | `#98C93C` | logotip (kapljica, črti) + CSS (gumbi, povezave) | poudarki: gumbi, ikone, tanke črte, oznake. **Na gumbu vedno temen napis** (`#1E1E1E`, kontrast 8,5 : 1). Bel napis na zeleni ima samo 1,95 : 1 – ne uporabljaj. |
| Zelena za besedilo | `#5D7C22` | izpeljana iz `#98C93C` (isti odtenek, temnejša) | zelene povezave in poudarki v besedilu na svetli podlagi (4,6 : 1) |
| Oglje (temna) | `#1E1E1E` | CSS (meni, besedilo) | besedilo, temni bloki (ozadje za negativni logotip in zeleno) |
| Topla svetla (ozadje) | `#FFFAF4` | CSS (ozadje glave) | glavno ozadje strani |
| Bež | `#EFE6DA` | CSS (ozadja razdelkov) | izmenično ozadje blokov, ozadje kartic z izdelki |
| Siva (besedilo 2) | `#5C5C68` | CSS | podnaslovi, opisi (6,4 : 1 na `#FFFAF4`) |
| Vinsko rdeča (redko) | `#A32628` | CSS (oznake kategorij) | samo drobni poudarki, npr. oznaka medalje ali likerjev |
| Bela | `#FFFFFF` | logotip (napis) | besedilo na temnih fotografijah in v temnih blokih |

Razmerje: približno 70 % svetla ozadja, 20 % oglje, do 10 % zelena. Zelena je poudarek, ne ploskev.

## Logotip

- **Datoteka:** `slike/01_logotip/logotip.png` – prosojen PNG, 202×62 px. **Edina samostojna datoteka logotipa na strani.**
- **Različica:** negativ (bel napis »BIO SAD«, zelena kapljica in črti `#98C93C`, znak ®) – **samo na temnem ozadju
  ali čez temnejši del fotografije**. Na svetlem ozadju je napis neviden.
- **Pozitivna različica** (temen napis) obstaja – uporabljena je na certifikatu ISO –, a je na spletni strani ni.
  ❓ Od naročnika pridobiti vektorski logotip (SVG/AI/PDF) v pozitivni in negativni različici.
- `logo-clanek.png` je samo referenca za videz logotipa v večji velikosti (na črnem ozadju z izdelki).
- Logotipa ne prerisuj, ne prebarvaj in ne povečuj čez izvorno velikost na zaslonih z visoko gostoto (≈ 200 px
  širine je največ za oster prikaz). Glava naj bo zato temna ali prosojna čez hero fotografijo.

## Pisave

| Vloga | Obstoječa | Predlog | Vir |
|---|---|---|---|
| Naslovi | Playfair Display (in okrasna Norican za naslove drsnika) | **Playfair Display** 600/700 – ohrani prepoznavnost, premium serif; Norican opusti | Google Fonts |
| Besedilo | PT Sans | **Inter** 400/500/600 (ali PT Sans, če naročnik želi kontinuiteto) | Google Fonts |
| Številke v pasu dokazov | – | Playfair Display 600, velike (48–56 px) | Google Fonts |
