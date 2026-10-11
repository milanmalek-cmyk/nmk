# Prenos v Claude Artifacts – {NAZIV}

Faza F6 se začne šele po odobritvi **V1** (dizajn potrjen v ChatGPT).

## 1. Kontrolni seznam vhodov

- [ ] `04_dizajn/` – posnetki odobrenega koncepta: `namizje.png`, `mobilno.png` (+ dodatni pogledi)
- [ ] `04_dizajn/specifikacija.md` – specifikacija iz ChatGPT (barve, pisave, mreža, bloki, animacije)
- [ ] `04_dizajn/opombe.md` – vaše opombe ob potrditvi (kaj spremeniti glede na koncept)
- [ ] `02_vsebina/besedila.md` in `seo-geo.md` – končna besedila, title, meta, JSON-LD
- [ ] `03_paket-chatgpt/slike/` – originalne slike (nespremenjene)
- [ ] `03_paket-chatgpt/barve.md` – paleta in pisave
- [ ] `animacije.md` (modul) – standard mikroanimacij

## 2. Tehnične zahteve

- Datoteke: `05_naslovnica/index.html`, `style.css`, `main.js`, `img/` – brez gradnje, brez Reacta, brez knjižnic.
- Zunanji viri: samo Google Fonts (ali lokalne pisave v `fonts/`). Brez sledilnih skript.
- Slike: kopije originalov v `img/` z istimi imeni; atributa `width`/`height`, `loading="lazy"` pod prvim zaslonom,
  hero s `fetchpriority="high"`. Izdelkov in etiket ne spreminjamo (tudi ne obrezujemo izrezanih izdelkov).
- CSS spremenljivke za barve, pisave in razmike (iz `barve.md` in specifikacije).
- Semantični HTML: en `<h1>`, `header` / `main` / `section` / `footer`, `alt` iz `seo-geo.md`, JSON-LD v `<head>`.
- Dostopnost: kontrast AA, vidni fokus, navigacija s tipkovnico, `prefers-reduced-motion`.
- Odzivnost: 1440 / 1024 / 768 / 390 px, brez vodoravnega drsnika (preveri s `screenshot.mjs`).
- Obrazci in povezave na podstrani kažejo na obstoječo stran naročnika (ali `#`), nič se ne pošilja.

## 3. Postopek

1. Zgradi `05_naslovnica/` po odobrenem dizajnu in specifikaciji.
2. Objavi kot **zaseben Artifact** za pregled (iste datoteke kot dodatne datoteke strani).
3. Posnetki 1440 / 768 / 390 → primerjava s konceptom → popravki.
4. Izvoz za gostovanje = mapa `05_naslovnica/` (ZIP), ki deluje na vsakem statičnem gostovanju.
   Rezervna pot, če bi bil potreben React: Vite → `dist/` (samostojne statične datoteke).

## 4. Poziv za gradnjo (za Claude)

> Zgradi odzivno naslovnico za {NAZIV} po odobrenem dizajnu v `04_dizajn/` in specifikaciji.
> Uporabi besedila iz `02_vsebina/besedila.md` dobesedno, SEO elemente iz `seo-geo.md`, originalne slike iz
> `03_paket-chatgpt/slike/` brez sprememb in mikroanimacije po `animacije.md`. Upoštevaj tehnične zahteve
> iz poglavja 2. Rezultat: `index.html`, `style.css`, `main.js`, `img/` – čist HTML/CSS/JS za običajno gostovanje.
