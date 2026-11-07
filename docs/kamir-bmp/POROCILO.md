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

- `bmp-neuporabljene.csv` – 68 priponk, ki niso glavna/galerijska slika nobenega izdelka (preverjeno tudi
  za 6 osnutkov in 6 zasebnih izdelkov) in se njihovo ime ne pojavi na nobeni strani. 12 jih ni bilo pripetih
  na noben objekt, 56 je bilo pripetih na izdelke, ki imajo zdaj drugo glavno sliko (jpg/png).
  **Izbrisane 7. 11. 2026** prek REST API-ja (priponka + `.bmp`, preverjeno: vseh 68 `.bmp` vrača 404).
  Njihove `.webp` dvojnice (68 datotek) so ostale na disku; izbriše jih skripta v načinu `delete-orphan-webp`.
- `bmp-v-uporabi.csv` – 345 priponk z izdelkom, kjer so glavna slika. **Ne briši**; pretvori s skripto.

Opomba: strežnikova zaščita pred roboti (stran "One moment, please") ob hitrem zaporedju zahtev vrne
HTML namesto JSON-a, zato je treba skripte prek API-ja izvajati s premori in preverjati odgovore.

## Postopek na strežniku

Varnostna kopija baze in `wp-content/uploads` najprej. Nato v korenu WordPressa:

```bash
wp eval-file kamir-bmp-cleanup.php dry-run
```

```bash
wp eval-file kamir-bmp-cleanup.php delete-orphan-webp
```

```bash
wp eval-file kamir-bmp-cleanup.php convert
```

```bash
wp eval-file kamir-bmp-cleanup.php orphan-bmp
```

```bash
wp eval-file kamir-bmp-cleanup.php delete-orphan-bmp
```

```bash
wp litespeed-purge all
```

`orphan-bmp` prebrska celo mapo uploads in izpiše `.bmp` datoteke, ki nimajo priponke v medijski knjižnici
(prek API-ja jih ni mogoče videti). `delete-orphan-bmp` jih izbriše, razen tistih, katerih ime se še kje
pojavi v bazi (vsebina, Elementor, meta). Datoteka `bmp-ostale-v-knjiznici.txt` našteva 345 BMP priponk,
ki po brisanju ostajajo v knjižnici, po mapah (2026/01: 122 datotek, 376 MB).

`convert` pri vsaki priponki: `_wp_attached_file` → `.webp`, `post_mime_type` → `image/webp`, popravi `guid`,
z `wp_generate_attachment_metadata` ustvari pomanjšane različice in izbriše `.bmp`. Če strežnikov GD/Imagick
ne zna brati WebP, shrani osnovne metapodatke in to javi (slika kljub temu deluje, le brez pomanjšanih različic).

Za 345 slik v uporabi REST API ne zadošča (ne omogoča zamenjave pripete datoteke), zato je potreben
WP-CLI na strežniku ali vtičnik, ki zna zamenjati datoteko priponke.
