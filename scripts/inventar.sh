#!/usr/bin/env bash
# Izvozi inventar obnovljene strani v docs/inventar/ in posnetek teme v snapshot/.
# Rezultat commitaš in pushaš – na tej podlagi poteka analiza.
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; [ -f .env ] && . ./.env; set +a

OUT=docs/inventar
SNAP=snapshot
url="${SITE_URL:-http://localhost:${WEB_PORT:-8080}}"
mkdir -p "$OUT" "$SNAP"

wp() { ./scripts/wp.sh "$@"; }
korak() { echo; echo "== $* =="; }

korak "Jedro in okolje"
{
  wp core version --extra
  echo
  wp eval 'echo "PHP: " . PHP_VERSION . "\n"; echo "WP_DEBUG: " . (defined("WP_DEBUG") && WP_DEBUG ? "on" : "off") . "\n"; echo "table_prefix: " . $GLOBALS["table_prefix"] . "\n";'
  echo
  wp cli info
} > "$OUT/core.txt"

korak "Nastavitve (options)"
{
  for o in siteurl home blogname blogdescription admin_email WPLANG timezone_string date_format \
           permalink_structure template stylesheet show_on_front page_on_front page_for_posts \
           posts_per_page blog_public default_role users_can_register default_comment_status \
           active_plugins; do
    printf '%s = %s\n' "$o" "$(wp option get "$o" --format=json 2>/dev/null || echo '(ni nastavljeno)')"
  done
} > "$OUT/options.txt"

korak "Vtičniki in teme"
wp plugin list --format=csv --fields=name,title,status,version,update,update_version,auto_update > "$OUT/plugins.csv" \
  || wp plugin list --format=csv > "$OUT/plugins.csv"
wp theme list --format=csv --fields=name,title,status,version,update,update_version,auto_update > "$OUT/themes.csv" \
  || wp theme list --format=csv > "$OUT/themes.csv"
stylesheet=$(wp option get stylesheet)
template=$(wp option get template)
wp theme get "$stylesheet" > "$OUT/theme-active.txt" || true
du -sk www/wp-content/plugins/* 2>/dev/null | sort -rn > "$OUT/plugins-size.txt" || true
wp core verify-checksums > "$OUT/checksums-core.txt" 2>&1 || true
wp plugin verify-checksums --all > "$OUT/checksums-plugins.txt" 2>&1 || true

korak "Tipi vsebin in taksonomije"
wp post-type list --format=csv > "$OUT/post-types.csv"
wp taxonomy list --format=csv > "$OUT/taxonomies.csv"

korak "Vsebine (seznam in števci)"
: > "$OUT/counts.txt"
: > "$OUT/posts.csv"
first=1
for pt in $(wp post-type list --field=name); do
  n=$(wp post list --post_type="$pt" --post_status=any --format=count 2>/dev/null || echo 0)
  printf '%-30s %s\n' "$pt" "$n" >> "$OUT/counts.txt"
  case "$pt" in
    revision|nav_menu_item|customize_changeset|oembed_cache|user_request|wp_global_styles) continue ;;
  esac
  if [ "$first" = 1 ]; then
    wp post list --post_type="$pt" --post_status=any --format=csv \
      --fields=ID,post_type,post_status,post_title,post_name,post_date,post_modified,post_parent,post_author,comment_count >> "$OUT/posts.csv" || true
    first=0
  else
    wp post list --post_type="$pt" --post_status=any --format=csv \
      --fields=ID,post_type,post_status,post_title,post_name,post_date,post_modified,post_parent,post_author,comment_count 2>/dev/null | tail -n +2 >> "$OUT/posts.csv" || true
  fi
done
wp term list category,post_tag --format=csv --fields=term_id,taxonomy,name,slug,count,parent > "$OUT/terms.csv" || true

korak "Meniji, stranske vrstice, widgeti"
wp menu list --format=csv > "$OUT/menus.csv" || true
wp menu list --format=csv --fields=term_id,slug 2>/dev/null | tail -n +2 | while IFS=, read -r id slug; do
  [ -n "$id" ] && wp menu item list "$id" --format=csv > "$OUT/menu-${slug}.csv" || true
done
wp sidebar list --format=csv > "$OUT/sidebars.csv" || true
: > "$OUT/widgets.txt"
for s in $(wp sidebar list --field=id 2>/dev/null); do
  { echo "## $s"; wp widget list "$s" --format=csv 2>/dev/null; echo; } >> "$OUT/widgets.txt" || true
done

korak "Uporabniki, cron, baza"
wp user list --format=csv --fields=ID,user_login,display_name,roles,user_registered > "$OUT/users.csv"
wp cron event list --format=csv > "$OUT/cron.csv" || true
wp db size --tables --format=csv > "$OUT/db-tables.csv" || true
wp option list --autoload=on --fields=option_name,size_bytes --format=csv 2>/dev/null | sort -t, -k2 -nr | head -n 60 > "$OUT/options-autoload-top.csv" || true
wp transient list --format=count > "$OUT/transients-count.txt" 2>/dev/null || true

korak "Mediji (uploads)"
{
  echo "Skupaj www/:"; du -sh www
  echo; echo "Uploads po mapah:"; du -sh www/wp-content/uploads 2>/dev/null; du -sk www/wp-content/uploads/* 2>/dev/null | sort -rn
} > "$OUT/uploads-size.txt" || true
find www/wp-content/uploads -type f 2>/dev/null | sed -E 's/.*\.([A-Za-z0-9]+)$/\1/' | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn > "$OUT/uploads-types.txt" || true
find www/wp-content/uploads -type f -size +2M -exec du -k {} + 2>/dev/null | sort -rn | head -n 100 > "$OUT/uploads-large.txt" || true

korak "Izvoz vsebine (WXR) in HTML posnetki"
wp export --stdout --skip_comments > "$OUT/vsebina.xml" || true
curl -sL "$url/" -o "$OUT/domov.html" || true
curl -sL "$url/wp-sitemap.xml" -o "$OUT/sitemap.xml" || true
curl -sL "$url/sitemap_index.xml" -o "$OUT/sitemap_index.xml" || true
curl -sL "$url/robots.txt" -o "$OUT/robots.txt" || true

korak "Posnetek teme, mu-plugins, .htaccess, wp-config (brez skrivnosti)"
rm -rf "$SNAP/themes" "$SNAP/mu-plugins"
mkdir -p "$SNAP/themes"
for t in $template $stylesheet; do
  if [ -d "www/wp-content/themes/$t" ] && [ ! -d "$SNAP/themes/$t" ]; then
    cp -R "www/wp-content/themes/$t" "$SNAP/themes/$t"
  fi
done
[ -d www/wp-content/mu-plugins ] && cp -R www/wp-content/mu-plugins "$SNAP/mu-plugins" || true
[ -f www/.htaccess ] && cp www/.htaccess "$SNAP/htaccess.txt" || true
if [ -f www/wp-config.php ]; then
  grep -vE "define\(\s*'(DB_|AUTH_|SECURE_AUTH_|LOGGED_IN_|NONCE_)" www/wp-config.php > "$SNAP/wp-config.sanitized.php" || true
fi
find "$SNAP" -type d \( -name node_modules -o -name vendor -o -name .git \) -prune -exec rm -rf {} + 2>/dev/null || true

echo
echo "Inventar je v $OUT/, posnetek teme v $SNAP/."
echo "Naprej:  git add -A && git commit -m \"Inventar multimedija.net\" && git push"
