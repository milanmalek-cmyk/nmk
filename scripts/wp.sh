#!/usr/bin/env bash
# WP-CLI v spletnem kontejnerju, npr.:  ./scripts/wp.sh plugin list
set -euo pipefail
cd "$(dirname "$0")/.."

# brez psevdo-terminala, kadar izhod preusmerjamo v datoteko (čist izpis brez \r)
tty_flag=""
[ -t 1 ] || tty_flag="-T"

docker compose exec $tty_flag -u www-data -e HOME=/tmp web wp "$@"
