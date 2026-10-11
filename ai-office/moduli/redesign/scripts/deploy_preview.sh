#!/usr/bin/env bash
# Objava predogleda na strežnik. Privzeto SUHI ZAGON: samo pokaže, kaj bi se objavilo.
# Prava objava samo z --potrjeno IN zapisano odobritvijo V2 v projekt.json.
#
# Uporaba:  deploy_preview.sh PROJEKT [--potrjeno]
# Nastavitve: config/nastavitve.env (glej nastavitve.example.env), geslo strežnika v PREVIEW_PASSWORD
#             (okoljska spremenljivka ali GitHub Secret, nikoli v gitu). Potrebuje lftp.
set -euo pipefail
MODUL="$(cd "$(dirname "$0")/.." && pwd)"
projekt="${1:?Podaj mapo projekta}"
potrjeno="${2:-}"
set -a; [ -f "$MODUL/config/nastavitve.env" ] && . "$MODUL/config/nastavitve.env"; set +a

pot="$(python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["predogled"].get("pot") or "")' "$projekt/projekt.json")"
izdaja="$projekt/06_predogled/izdaja/$pot"
[ -n "$pot" ] && [ -d "$izdaja" ] || { echo "Ni izdaje predogleda – najprej zaženi preview_build.py."; exit 1; }
: "${PREVIEW_HOST:?Manjka PREVIEW_HOST v nastavitve.env}" "${PREVIEW_USER:?Manjka PREVIEW_USER}" \
  "${PREVIEW_REMOTE_DIR:?Manjka PREVIEW_REMOTE_DIR}" "${PREVIEW_HTPASSWD_DIR:?Manjka PREVIEW_HTPASSWD_DIR}"
protokol="${PREVIEW_PROTOCOL:-sftp}"
url="${PREVIEW_BASE_URL%/}/$pot/"

echo "== Objava predogleda =="
echo "Projekt:   $projekt"
echo "Cilj:      $protokol://$PREVIEW_HOST${PREVIEW_PORT:+:$PREVIEW_PORT}$PREVIEW_REMOTE_DIR/$pot/"
echo "URL:       $url"
echo "Zaščita:   .htpasswd → $PREVIEW_HTPASSWD_DIR/$pot.htpasswd"
echo "Datoteke:"
(cd "$izdaja" && find . -type f | sort | sed 's|^\./|  |')

if [ "$potrjeno" != "--potrjeno" ]; then
  echo
  echo "SUHI ZAGON – nič ni bilo objavljeno. Za objavo: potrditev V2, nato ponovi z --potrjeno."
  exit 0
fi

python3 -I -c 'import json,sys; m=json.load(open(sys.argv[1])); sys.exit(0 if any(o["vrata"]=="V2" for o in m["odobritve"]) else 1)' \
  "$projekt/projekt.json" || { echo "Odobritev V2 ni zapisana v projekt.json – objava zavrnjena."; exit 1; }
command -v lftp >/dev/null || { echo "Manjka lftp (Ubuntu: sudo apt install lftp)."; exit 1; }
: "${PREVIEW_PASSWORD:?Nastavi PREVIEW_PASSWORD (okolje ali GitHub Secret)}"

# geslo prek okolja, da se ne vidi v seznamu procesov
LFTP_PASSWORD="$PREVIEW_PASSWORD" lftp --env-password -u "$PREVIEW_USER" ${PREVIEW_PORT:+-p "$PREVIEW_PORT"} "$protokol://$PREVIEW_HOST" <<EOF
set sftp:auto-confirm yes
set ftp:ssl-allow yes
mkdir -p -f "$PREVIEW_HTPASSWD_DIR"
put "$projekt/06_predogled/.htpasswd" -o "$PREVIEW_HTPASSWD_DIR/$pot.htpasswd"
mkdir -p -f "$PREVIEW_REMOTE_DIR/$pot"
mirror -R --delete --verbose "$izdaja" "$PREVIEW_REMOTE_DIR/$pot"
bye
EOF

status="$(curl -s -o /dev/null -w '%{http_code}' "$url" || true)"
echo "$(date -Iseconds)  $url  HTTP brez gesla: $status" >> "$projekt/06_predogled/objave.log"
python3 -I -c 'import sys,datetime; sys.path.insert(0,sys.argv[2]); from manifest import beri,pisi; m=beri(sys.argv[1]); m["predogled"]["objavljeno"]=datetime.datetime.now().isoformat(timespec="seconds"); pisi(sys.argv[1],m)' \
  "$projekt" "$MODUL/scripts"
echo "Objavljeno: $url  (brez gesla strežnik vrne HTTP $status – pričakovano 401)"
