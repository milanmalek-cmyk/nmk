# Multimedija – lokalno dev okolje (multimedija.net)

Lokalna razvojna kopija spletne strani **multimedija.net** za analizo in prenovo.
Okolje teče v Dockerju (PHP 8.2 + Apache, MariaDB 11, WP-CLI) in se zažene z enim ukazom.

## Zahteve

- Ubuntu (ali WSL2) z Dockerjem in Compose v2 (`docker compose version`)
- git

## Zagon

```bash
./start-multimedija
```

Ob prvem zagonu skripta:

1. ustvari `.env` iz `.env.example`,
2. zgradi in zažene kontejnerje,
3. v `www/` namesti svež WordPress (sl_SI) → http://localhost:8080 (admin: `admin` / `admin`).

Ustavitev: `./stop-multimedija`

Ukaz od koderkoli (kot pri ostalih projektih):

```bash
sudo ln -sf "$(pwd)/start-multimedija" /usr/local/bin/start-multimedija
sudo ln -sf "$(pwd)/stop-multimedija"  /usr/local/bin/stop-multimedija
```

## Nalaganje kopije produkcije

Baza je vedno: host `db`, ime `multimedija`, uporabnik `wp`, geslo `wp` (glej `.env`).

**A) Datoteke + SQL izvoz**

1. Kopiraj datoteke strani v `www/` (prepiši svež WP ali samo `wp-content/`).
2. Uvozi bazo in zamenjaj produkcijske URL-je z lokalnimi:
   ```bash
   ./scripts/import-db.sh pot/do/baza.sql      # ali .sql.gz; 2. argument = produkcijski URL (privzeto https://multimedija.net)
   ```
3. `./start-multimedija` – popravi DB podatke v `wp-config.php`, če si prepisal tudi tega.

**B) Duplicator installer** (če ti je lažje)

1. `installer.php` in arhiv skopiraj v `www/`, odpri http://localhost:8080/installer.php.
2. Baza: Action *Empty Database*, Host `db`, Database `multimedija`, User `wp`, Password `wp`;
   nov URL `http://localhost:8080`, path `/var/www/html`.

Prijava po uvozu: produkcijski uporabniki. Novo geslo: `./scripts/wp.sh user update <login> --user_pass=novo`

## Ukazi

| Ukaz | Kaj naredi |
|---|---|
| `./start-multimedija` | zažene okolje (in namesti svež WP, če ga še ni) |
| `./stop-multimedija` | ustavi kontejnerje (baza in datoteke ostanejo) |
| `./scripts/wp.sh <ukaz>` | WP-CLI, npr. `./scripts/wp.sh plugin list` |
| `./scripts/import-db.sh baza.sql` | uvoz baze + zamenjava URL-jev + predpona tabel |
| `./scripts/inventar.sh` | inventar strani v `docs/inventar/` in posnetek teme v `snapshot/` |
| `./scripts/reset.sh` | izbriše bazo in `www/` (začetek od začetka) |
| `docker compose --profile tools up -d adminer` | Adminer na http://localhost:8081 (strežnik `db`) |
| `docker compose logs -f web` | logi Apache/PHP |

## Naslednji korak: inventar za analizo

Ko stran lokalno deluje:

```bash
./scripts/inventar.sh
git add -A && git commit -m "Inventar multimedija.net" && git push
```

Skripta izvozi vtičnike, teme, vsebine, menije, uporabnike, velikosti baze in medijev, WXR izvoz vsebine
in kopijo aktivne teme (`wp-config.php` se shrani brez gesel in ključev). Na tej podlagi nastaneta
analiza (`docs/ANALIZA.md`) in predlog prenove (`docs/PLAN.md`).

## Težave

- **500 / bela stran po nalaganju**: `docker compose logs -f web`; preveri `www/.htaccess` (direktive gostitelja) in `www/wp-content/debug.log`.
- **Preusmerja na multimedija.net**: URL-ji v bazi so še produkcijski → `./scripts/import-db.sh` ali
  `./scripts/wp.sh search-replace 'https://multimedija.net' 'http://localhost:8080' --all-tables --skip-columns=guid`.
- **Vtičnik zahteva starejši PHP**: `PHP_VERSION=8.1` v `.env`, nato `./start-multimedija`.
- **Dovoljenja v `www/`**: `www-data` v kontejnerju dobi tvoj UID/GID samodejno; po spremembi uporabnika `docker compose build --no-cache web`.
- **Vrata zasedena**: spremeni `WEB_PORT` v `.env`.

## Struktura

```
start-multimedija / stop-multimedija   zagon / ustavitev
docker-compose.yml, docker/            okolje (Dockerfile, php.ini, apache)
www/                                   WordPress (ni v gitu)
scripts/                               wp.sh, import-db.sh, inventar.sh, reset.sh
docs/                                  PLAN.md, ANALIZA.md, inventar/
snapshot/                              kopija aktivne teme za analizo (v gitu)
```
