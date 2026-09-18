#!/usr/bin/env bash
# Uvozi SQL izvoz produkcijske baze v lokalno bazo in zamenja produkcijske URL-je z lokalnimi.
# Uporaba:  ./scripts/import-db.sh pot/do/baza.sql[.gz] [https://multimedija.net]
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; [ -f .env ] && . ./.env; set +a

dump="${1:?Podaj pot do .sql ali .sql.gz datoteke}"
old="${2:-${PROD_URL:-https://multimedija.net}}"
new="${SITE_URL:-http://localhost:${WEB_PORT:-8080}}"
[ -f "$dump" ] || { echo "Datoteka '$dump' ne obstaja."; exit 1; }

db() { docker compose exec -T db mariadb -u"${DB_USER:-wp}" -p"${DB_PASSWORD:-wp}" "${DB_NAME:-multimedija}" "$@"; }
wp() { ./scripts/wp.sh "$@"; }

echo "Uvažam '$dump' v bazo '${DB_NAME:-multimedija}' ..."
if [[ "$dump" == *.gz ]]; then
  gzip -dc "$dump" | db
else
  db < "$dump"
fi

# predpona tabel iz uvožene baze -> wp-config.php
prefix=$(db -N -e "SHOW TABLES LIKE '%options'" | head -n 1 | sed 's/options$//')
if [ -n "$prefix" ]; then
  echo "Predpona tabel: $prefix"
  wp config set table_prefix "$prefix" --type=variable --quiet 2>/dev/null || echo "Opozorilo: table_prefix nisem mogel zapisati v wp-config.php – preveri ročno."
fi

# zamenjava URL-jev (www in brez, https in http, tudi JSON-escaped oblika za Elementor & co.)
host=$(echo "$old" | sed -E 's#^https?://##; s#/$##')
bare=${host#www.}
new_esc=${new//\//\\/}
echo "Zamenjujem URL-je -> $new"
for h in "www.$bare" "$bare"; do
  for s in https http; do
    wp search-replace "$s://$h" "$new" --all-tables --skip-columns=guid --report-changed-only || true
    wp search-replace "$s:\\/\\/$h" "$new_esc" --all-tables --skip-columns=guid --report-changed-only || true
  done
done

if wp plugin is-active elementor 2>/dev/null; then
  wp elementor replace-urls "https://$bare" "$new" 2>/dev/null || true
  wp elementor flush-css 2>/dev/null || true
fi
wp cache flush >/dev/null 2>&1 || true
wp rewrite flush --hard >/dev/null 2>&1 || true

echo
echo "Končano. Stran: $new   Admin: $new/wp-admin (produkcijski uporabniki)"
echo "Novo geslo po potrebi:  ./scripts/wp.sh user update <login> --user_pass=novo"
