---
name: pripravi-ponudbo
description: Multimedija AI Office – za podjetje iz Google Sheets »Podjetja Redesign« pripravi prodajne osnutke - tri glavne koristi prenove, kratek oseben predlog za lastnika ali direktorja, osnutek prodajne e-pošte, predlagan cenovni razred, predlog naslednjega kontakta in (s potrjenim cenikom) osnutek ponudbe. Nikoli ne pošilja. Uporabi za "/pripravi-ponudbo <ime>" ali ko je v preglednici naloga PRIPRAVI PONUDBO.
---

# /pripravi-ponudbo <ime>

Navodila za preglednico: `ai-office/moduli/marketing/README.md`.
Predloge: `ai-office/moduli/redesign/templates/prodaja/`.

## 1. Vhodi

- Vrstica podjetja (`evidenca.py najdi`) in zadnja ocena iz »AI ocene« s poročilom.
- Projekt `ai-office/projekti/<slug>/…`: analiza, dejstva in predogled, če obstajajo.
- Brez ocene najprej izvedi `/analiziraj-podjetje`. Koristi morajo temeljiti na ugotovitvah, ne na splošnih trditvah.
- Pošiljatelj in nagovor iz `ai-office/moduli/redesign/config/nastavitve.env`. Če manjkajo: `[POSILJATELJ_IME]` …,
  privzeto vikanje.
- Cene:
  - **Cenovni razred** iz stolpca »Cenovna skupina« in zavihka »Merila in postopek« (A 1.500–2.500 €, B 2.500–4.000 €).
    To je okvirni razred, ne ponudba.
  - **Natančne cene** samo iz `ai-office/moduli/redesign/config/cenik.md`. Sicer `[CENA – potrdi]`.

## 2. Osnutki

V `ai-office/projekti/<slug>/<projekt>/07_prodaja/` (oziroma `ai-office/projekti/<slug>/prodaja/`, če projekta
prenove ni):

| Datoteka | Vsebina |
|---|---|
| `koristi.md` | tri koristi; vsaka: ugotovitev danes (dokaz) → kaj prinese prenova |
| `osebni-predlog.md` | 5–8 stavkov za lastnika ali direktorja: zakaj pišemo prav njim, kaj smo opazili, kaj predlagamo (predogled naslovnice), kratek sestanek |
| `email.md` | zadeva, telo do 150 besed, povezava na predogled (geslo ločeno), podpis; na vrhu oznaka OSNUTEK – NE POŠILJAJ BREZ POTRDITVE |
| `cenovni-razred.md` | predlagan razred A ali B z utemeljitvijo (obseg, B2B zahtevnost, katalog) in kaj vključuje |
| `naslednji-kontakt.md` | datum in kanal (telefon, e-pošta, osebno), kdo, kaj povedati |
| `ponudba.md` | samo s potrjenim cenikom, sicer tabela s `[CENA – potrdi]` |

Imena oseb samo iz javnih virov (register, stran podjetja). Ne ugibaj e-poštnih naslovov.

## 3. Zapis

1. »Predizbor 30«: `prodajna_faza: PREDLOG PRIPRAVLJEN` (samo če je prazna), `naslednji_kontakt`
   (`"LLLL-MM-DD – kanal, kratko"`, samo če je prazen).
2. Vrstica v Dnevnik.
3. Commit in push.

## 4. Pošiljanje

**Nikoli.** Uporabnik osnutke pregleda, popravi in pošlje sam. Po pošiljanju uporabnik nastavi fazo POSLANO.
Claude lahko na njegovo prošnjo zapiše vrstico v Dnevnik.
