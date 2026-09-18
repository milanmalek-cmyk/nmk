#!/usr/bin/env bash
# IZBRIŠE lokalno bazo (docker volume) in vso vsebino www/ – za začetek od začetka.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "To bo IZBRISALO lokalno bazo in vso vsebino mape www/."
read -r -p "Nadaljujem? [y/N] " odgovor
[ "${odgovor:-}" = "y" ] || { echo "Prekinjeno."; exit 0; }

# brisanje znotraj kontejnerja (datoteke so lahko v lasti www-data)
docker compose run --rm --no-deps -T web sh -c 'find /var/www/html -mindepth 1 -not -name .gitkeep -delete'
docker compose --profile tools down -v
echo "Pobrisano. Nov začetek: ./start-multimedija"
