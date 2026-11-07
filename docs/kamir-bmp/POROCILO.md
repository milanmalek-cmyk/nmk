# kamir.si – pregled BMP slik (7. 11. 2026)

Pregled je narejen samo prek javnega dela strani (REST API, Store API, sitemap, HTML vseh 1345 strani).
Do datotek na strežniku iz te seje ni dostopa, zato je brisanje pripravljeno kot WP-CLI skripta.

## Ugotovitve

| | |
|---|---|
| BMP priponk v medijski knjižnici | 413 (847 MB) |
| … z obstoječo `.webp` dvojnico na disku | 413 (vse) |
| … ki so glavna slika objavljenega izdelka | 345 (752 MB) |
| … brez kakršne koli uporabe | 68 (96 MB) |

**Kako stran zdaj prikazuje slike.** Priponke v bazi še vedno kažejo na `.bmp` (`_wp_attached_file`,
`post_mime_type = image/bmp`, brez pomanjšanih različic). Na strani se `.webp` prikazuje zato, ker
vtičnik **LiteSpeed Cache 7.9.2** (funkcija *Image WebP Replacement*) v HTML-ju zamenja URL, če ob
originalu obstaja `.webp`. Na 341 straneh izdelkov `.bmp` URL še vedno ostane v strukturiranih podatkih
(JSON-LD `"image"`), ker jih LiteSpeed ne zamenjuje.

**Posledica:** `.bmp` datotek izdelkov, ki so v uporabi, ni varno samo pobrisati z diska. Priponka bi
ostala brez datoteke (polomljene sličice v administraciji, JSON-LD, izvozi, regeneracija sličic).
Pravilen postopek je: priponko preusmeriti na `.webp`, ustvariti metapodatke/pomanjšane različice in
šele nato izbrisati `.bmp`. To naredi skripta v načinu `convert`.

## Seznami

- `bmp-neuporabljene.csv` – 68 priponk, ki niso glavna/galerijska slika nobenega objavljenega izdelka in
  se njihovo ime ne pojavi na nobeni strani. 12 jih ni pripetih na noben objekt, 56 je pripetih na
  izdelke, ki imajo zdaj drugo glavno sliko (jpg/png). **Varno za brisanje** (priponka + `.bmp` + `.webp`).
- `bmp-v-uporabi.csv` – 345 priponk z izdelkom, kjer so glavna slika. **Ne briši**; pretvori s skripto.

Omejitev: javno so vidni samo objavljeni izdelki. Če je katera od 68 slik uporabljena v osnutku ali
skritem izdelku, jo skripta pred brisanjem še enkrat preveri (`_thumbnail_id`, `_product_image_gallery`)
in preskoči.

## Postopek na strežniku

Varnostna kopija baze in `wp-content/uploads` najprej. Nato v korenu WordPressa:

```bash
wp eval-file kamir-bmp-cleanup.php dry-run
```

```bash
wp eval-file kamir-bmp-cleanup.php delete-unused
```

```bash
wp eval-file kamir-bmp-cleanup.php convert
```

```bash
wp litespeed-purge all
```

`convert` pri vsaki priponki: `_wp_attached_file` → `.webp`, `post_mime_type` → `image/webp`, popravi `guid`,
z `wp_generate_attachment_metadata` ustvari pomanjšane različice in izbriše `.bmp`. Če strežnikov GD/Imagick
ne zna brati WebP, shrani osnovne metapodatke in to javi (slika kljub temu deluje, le brez pomanjšanih različic).

Če WP-CLI ni na voljo, je možna alternativa za 68 neuporabljenih: brisanje prek REST API-ja z aplikacijskim
geslom (`DELETE /wp-json/wp/v2/media/{id}?force=true`), ker WordPress pri tem izbriše tudi datoteko.
Za 345 slik v uporabi REST API ne zadošča (ne omogoča zamenjave pripete datoteke).
