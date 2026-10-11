# Modul AI REDESIGN

Iz URL-ja obstoječe strani pripravi predlog prenove **naslovnice**: analizo, raziskavo, besedila (SEO/GEO),
izbor originalnih slik, paket za ChatGPT, po odobrenem dizajnu statično naslovnico, zaščiten predogled in
prodajne osnutke. Uporaba v Claude Code: `/redesign https://www.stranka.si/` (navodila: `.claude/skills/redesign/SKILL.md`).

## Faze in vrata potrditve

F0 inventar → F1 pregled strani → F2 raziskava → F3 vsebina → F4 vizualni materiali → F5 paket za ChatGPT
→ 🔒 **V1** dizajn potrjen v ChatGPT → F6 gradnja → F7 predogled → 🔒 **V2** objava → F8 prodaja → 🔒 **V3** pošiljanje (vedno ročno)

## Skripte (`scripts/`)

| Skripta | Namen |
|---|---|
| `manifest.py` | projekt: `init`, `najdi`, `stanje`, `faza`, `odobri` |
| `crawl.py` | pregled strani (isti jezik, predpomnilnik `--cache`) → `pages.json` |
| `probe_images.py` | dimenzije vseh slik brez prenosa (HTTP Range), `--prejsnji` za ponovno rabo → `slike.tsv` |
| `screenshot.mjs` | posnetki pri več širinah, opozorilo na vodoravni drsnik (Node + playwright-core) |
| `brand.py` | barve iz CSS in logotipa, pisave → `brand.json` |
| `contact_sheet.py` | pregledni list kandidatov (samo za izbor) |
| `fetch_assets.py` | prenos izbranih originalov iz `izbor.tsv`, SHA-256, `EVIDENCA.md` |
| `package.py` | ZIP za ChatGPT + preverjanje |
| `preview_build.py` | izdaja predogleda: noindex, oznaka, `.htaccess`, `.htpasswd` |
| `deploy_preview.sh` | objava; privzeto suhi zagon, prava objava samo z `--potrjeno` in odobritvijo V2 |

## Namestitev

- Python 3.9+ s Pillow, Node 18+ (`npm install` v tej mapi za `playwright-core`), Chromium
  (`CHROMIUM_PATH` ali `/opt/pw-browsers`), `openssl` (geslo predogleda), `lftp` (samo za objavo).
- `config/nastavitve.example.env` → `config/nastavitve.env` (ni v gitu). Geslo strežnika samo v okolju (`PREVIEW_PASSWORD`).
- `config/cenik.example.md` → `config/cenik.md` s potrjenimi cenami (sicer ponudba ostane brez cen).
