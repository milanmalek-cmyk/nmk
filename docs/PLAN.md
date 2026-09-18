# Načrt prenove multimedija.net

| Faza | Kaj | Kdo | Stanje |
|---|---|---|---|
| 0 | Projekt in lokalno okolje (`./start-multimedija`) | Claude | ✅ |
| 1 | Nalaganje kopije produkcije v lokalno okolje | Ti | ⬜ |
| 2 | Inventar (`./scripts/inventar.sh`) → commit + push | Ti | ⬜ |
| 3 | Analiza: tema, vtičniki, vsebine in duplikati, SEO, hitrost, varnost, dostopnost → `docs/ANALIZA.md` | Claude | ⬜ |
| 4 | Predlog prenove: kaj ohraniti / zamenjati, struktura strani, oblikovna smer, tehnična pot (child tema / nova tema / urejevalnik blokov) | Claude + Ti | ⬜ |
| 5 | Izvedba: tema, čiščenje vtičnikov, vsebine, mediji, preusmeritve | Claude | ⬜ |
| 6 | Testiranje (funkcionalno, mobilno, hitrost, SEO) | Ti + Claude | ⬜ |
| 7 | Prenos na produkcijo (varnostna kopija, migracija, preusmeritve, preverjanje) | Ti + Claude | ⬜ |

## Dogovori

- Delo poteka na lokalni kopiji v `www/`; produkcija se ne spreminja do faze 7.
- Lastna koda (child tema, mu-plugins) se verzionira v gitu (izjeme v `.gitignore`), jedro, vtičniki in `uploads` ne.
- Vsaka faza se zaključi z zapisom v `docs/` (kaj je bilo ugotovljeno / narejeno / kaj sledi).

## Odprta vprašanja

- Kakšen je cilj prenove (samo osvežitev videza, nova struktura, nove funkcije, več jezikov)?
- Ali ostane obstoječi page builder (Elementor/WPBakery/Gutenberg) ali gre stran na urejevalnik blokov?
- Kdo bo stran vzdrževal po prenovi (vpliva na izbiro teme in vtičnikov)?
