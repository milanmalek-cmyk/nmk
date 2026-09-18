# Analiza obstoječe strani multimedija.net

> Izpolni se po fazi 2 (inventar). Viri: `docs/inventar/`, `snapshot/`, lokalna stran.

## 1. Osnovni podatki

- WordPress / PHP verzija, jezik, predpona tabel
- Tema (starš / otrok, izvor, verzija), page builder
- Vtičniki: aktivni / neaktivni / z razpoložljivimi posodobitvami
- Velikost baze, `uploads`, število strani / objav / medijev

## 2. Tema in oblikovanje

- [ ] izvor in posodabljanje teme, obstoj child teme, lastne prilagoditve (kje?)
- [ ] odzivnost (mobilno, tablica), tipografija, barvna paleta, doslednost
- [ ] postavitev glave, noge, menijev; struktura domače strani
- [ ] zastarele tehnike (slider revolution, shortcodi, inline stili, jQuery vtičniki)

## 3. Vtičniki

- [ ] neaktivni ali opuščeni (brez posodobitev > 2 leti)
- [ ] podvojene funkcije (dva SEO, dva cache, dva form vtičnika ...)
- [ ] varnostno tvegani, vpliv na hitrost (glej `plugins-size.txt`, `options-autoload-top.csv`)
- [ ] kaj je nujno za delovanje strani, kaj se lahko odstrani

## 4. Vsebine

- [ ] seznam strani in objav: sirote, prazne, zastarele, osnutki, zasebne
- [ ] duplikati: enaki naslovi, slugi z `-2`, podobna vsebina, kopije strani iz page builderja
- [ ] mediji: neuporabljene datoteke, prevelike slike, formati (WebP), poimenovanje
- [ ] meniji in navigacija: mrtve povezave, globina, doslednost
- [ ] jezik, pravopis, ton, klici k dejanju, kontaktni podatki (točnost)

## 5. SEO

- [ ] naslovi, meta opisi, H1/H2 struktura, permalinki
- [ ] sitemap, robots.txt, kanonični URL-ji, indeksiranje
- [ ] preusmeritve (obstoječe in potrebne po prenovi), 404
- [ ] strukturirani podatki (Organization, LocalBusiness, Breadcrumb)
- [ ] lokalni SEO (Google Business, NAP)

## 6. Hitrost

- [ ] velikost strani, št. zahtevkov, LCP/CLS/INP (Lighthouse na lokalni in produkcijski strani)
- [ ] slike (lazy load, velikosti, WebP), pisave, CSS/JS iz vtičnikov
- [ ] cache, minifikacija, CDN, baza (autoload, transienti, revizije)

## 7. Varnost in vzdrževanje

- [ ] uporabniki in vloge (`users.csv`), uporabnik `admin`, neaktivni računi
- [ ] integriteta jedra in vtičnikov (`checksums-*.txt`)
- [ ] zastarele komponente, PHP verzija, HTTPS, varnostne kopije, cron (`cron.csv`)

## 8. Dostopnost

- [ ] kontrast, alt besedila, fokus, tipkovnična navigacija, semantika

## 9. Povzetek in priporočila

| Področje | Ocena | Ključne ugotovitve | Priporočilo |
|---|---|---|---|
| Tema | | | |
| Vtičniki | | | |
| Vsebine | | | |
| SEO | | | |
| Hitrost | | | |
| Varnost | | | |
