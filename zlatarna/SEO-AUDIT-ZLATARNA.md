# SEO audit – Zlatarna Brežnik (nova stran pred selitvijo)

Datum: 1. 10. 2026
Nova stran (dev): `zlatar.ddev.site` (lokalno) in javna kopija `https://zlatarna-breznik.mmedija.com/`
Produkcija (stara stran): `https://www.zlatarna-breznik.si/` (ciljna domena po selitvi)

Ta dokument je **samo audit**. Na strani ni bilo nič spremenjeno.

---

## 0. Metoda in omejitve

**Kaj je bilo pregledano**
- **Stara produkcija:** vseh 340 URL-jev iz Yoastovih sitemapov (22 člankov, 7 strani, 251 izdelkov, 8 kategorij izdelkov, 20 oznak izdelkov, 30 oznak bloga, 2 kategoriji bloga, 1 avtor).
- **Nova stran:** vseh 342 URL-jev iz njenih sitemapov. Vsak stari URL je bil odprt še na novi strani, brez sledenja preusmeritvam, da se vidijo verige.
- **Izdelki:** vseh 251 iz WooCommerce Store API na obeh straneh: imena, slugi, kategorije, oznake, slike, alt in opisi. Slike so bile primerjane še vizualno (dHash), da se najdejo podvojeni modeli.
- **Za vsak URL:** title, meta description, robots, canonical, Open Graph, H1/H2, JSON-LD, drobtine, slike (alt, width/height, loading), iframe, skripte, stili in pisave.
- **Hitrost in UX:** Lighthouse (mobile in desktop) in Playwright pri 360, 375, 390, 430 in 1440 px, glej poglavje 15.
- **Iskalni roboti:** dostop za Googlebot, Bingbot in AI robote (GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot).

**Omejitve**
- Audit je narejen **od zunaj, na javni kopiji `zlatarna-breznik.mmedija.com`**. Lokalni `zlatar.ddev.site` iz oblaka ni dosegljiv.
- Lokalna različica je lahko novejša. Če je bila po zadnjem prenosu na mmedija.com kaj spremenjena (npr. WebP, umik jQueryja, novi SEO odstavki), je treba označene točke preveriti še lokalno.
- **Od zunaj ni vidno, preveriti lokalno z WP-CLI:**
  - seznam vseh vtičnikov z neaktivnimi;
  - custom fields in ACF;
  - template datoteke child teme;
  - filtri `wp_robots`;
  - vrednost `blog_public`;
  - nastavitve Yoasta in LiteSpeed Cache;
  - Redirection pravila;
  - cron.
- **Ni bilo podatkov iz Google Search Console.** Stolpec `GSC PRIORITY` v `redirect-map.csv` je zato **ocena** in temelji na seznamu ključnih URL-jev iz navodil in na vrsti strani. Pred odločitvami MANUAL REVIEW ga je treba zamenjati z dejanskimi kliki in prikazi.

---

## 1. Povzetek: kaj je najbolj nujno

| # | Prioriteta | Problem | Kje |
|---|---|---|---|
| 1 | KRITIČNO | `/kontakt/` je na **obeh** domenah za strežniško zaščito »Bot Verification« (LiteSpeed reCAPTCHA). Googlebot, Bingbot in OAI-SearchBot gredo skozi. **PerplexityBot, ClaudeBot** in v našem testu **vsak zahtevek z navadnim brskalnikom** dobijo stran z reCAPTCHA (tudi slikovni izziv) namesto kontakta. Slabo za GEO, UX in konverzije. Preveri še z domačega omrežja in telefona. | strežnik / gostitelj |
| 2 | KRITIČNO ob prehodu | Dev ima `noindex, nofollow` samo iz WordPressa (`blog_public=0`), brez `X-Robots-Tag`. Ob prehodu je treba `blog_public` vklopiti, sicer bo produkcija noindex. | nastavitve |
| 3 | VISOKO | Vseh 340 starih URL-jev obstaja tudi na novi strani (200). Edina 301 je `/4017-2/ → /guess-nakit/`. `/cene-porocnih-prstanov-v-letu-2024/` še ni preusmerjen. `/kategorija-izdelka/porocni-prstani/` je **podvojen URL** z 200. | `redirect-map.csv` |
| 4 | VISOKO | Na vseh straneh (vzorec `zd-n__a`/`zd-n__b` in `zd-rokopis`) DOM ne vsebuje presledkov med `<span>` deli naslovov, npr. »Poročni prstani,ki«, »Dva prstana,ena zgodba.«, »Ročno.Z ljubeznijo.Za vedno.«, »Unikatni zaročni prstani,izdelani«. | Elementor / `zd-n__a` |
| 5 | VISOKO | `/3902-2/` še vsebuje »V oddaji vam bomo predstavili…«, odstavek o Tiffany & Co., Cartier in Bvlgari ter **izmišljeno primerjalno tabelo cen** (999 €, 2.499 €, 1.799 €, platina). | vsebina |
| 6 | VISOKO | `/cena-zarocnih-prstanov/`: »povprečne stroške zaročnega prstana v letu 2020«. `/cena-porocnih-prstanov/`: »od 200 € dalje« in »višino dveh mesečnih plač«. Naročnik mora potrditi, ali sme ostati. | vsebina |
| 7 | VISOKO | 251 izdelkov: **0** jih ima opis. H1 je skrajšan na »433 Poročna prstana« (144 izdelkov ima H1 s ≤ 3 besedami). 206 glavnih slik ima prazen alt. Opisi so predloga (»… Model si oglejte …«). | WooCommerce |
| 8 | VISOKO | Valuta WooCommerce je **USD** (cene 0). Na stari strani se v glavi izpiše »0.00$«. Če bi kdaj nastal Offer v shemi, bi bil napačen. | WooCommerce nastavitve |
| 9 | SREDNJE | Kanibalizacija: domača in `/porocni-prstani/` imata v predlogih skoraj enak title (»Poročni prstani po meri \| …«). Oznake (`/tag/zarocni-prstan/`, `/oznaka-izdelka/zarocni-prstan/` …) tekmujejo z glavnimi stranmi. | title, taksonomije |
| 10 | SREDNJE | Izdelek shema: ni `Product` (samo `ItemPage`). JSON drobtine izdelka (Domov › Katalog › izdelek) se ne ujemajo z vidnimi (Domov › Katalog › Poročni prstani › izdelek). Ime v drobtinah ima neodkodiran `&#8211;`. | Yoast / child tema |
| 11 | SREDNJE | Arhivi oznak izdelkov imajo napačen H1 »Katalog naših prstanov.«. 63 URL-jev nima meta description. | predloge, Yoast |
| 12 | SREDNJE | Stara produkcija preusmerja `http://zlatarna-breznik.si/` v **verigi dveh 301** (→ https brez www → https www). | `.htaccess` ob prehodu |
| 13 | SREDNJE | Ob prehodu odstraniti ali zakleniti razvojne vtičnike: Duplicator (javni REST `duplicator/v1`), **`elementor-mcp-composer`** (javni REST namespace) in `elementor-ai`. | varnost |
| 14 | NIZKO | Favicon je `.ico` tudi za `apple-touch-icon` in 192×192. Manjkata PNG 180×180 in 192/512. | tema |
| 15 | NIZKO | Stara stran ima Google Analytics **UA-135258619-1** (Universal Analytics ne zbira več podatkov). Nova ima GA4 `G-L0M9SC4KZ6`, ki se naloži šele po privolitvi ✅. Preveri, da je lastnina GA4 na računu naročnika in povezana z GSC. | naročnik / GA4 |

Podrobnosti in dokazi so v poglavjih spodaj.

---

## 2. Tehnično stanje nove strani

| Področje | Stanje (dev) | Stara stran (prod) |
|---|---|---|
| WordPress | 7.1.2 | 6.8.10 |
| WooCommerce | 11.1.2, katalog brez cen (`price 0`, `is_purchasable: false`), **valuta USD** | 10.7.0 + YITH Catalog Mode |
| Tema | `hello-elementor` + **`hello-elementor-child`** | Frank Jewelry Store (ThemeREX) + child |
| Gradnik | Elementor 4.3.3 (+ Elementor One, Elementor AI, **Elementor MCP Composer**) | WPBakery 8.7, Slider Revolution 6.7, trx_addons |
| SEO vtičnik | **Yoast SEO** (`yoast/v1`) | Yoast SEO |
| Cache | strežnik LiteSpeed; vtičnik LiteSpeed Cache (nastavitve preveriti lokalno) | LiteSpeed |
| Drugi vtičniki (zaznani prek REST/virov) | Contact Form 7, Cookie Notice, Trustindex (Widgets for Google Reviews), **Redirection**, Wordfence (+ Login Security), **Duplicator**, Jetpack, WP Mail SMTP, Limit Login Attempts Reloaded | enako + RevSlider, YITH |
| Tipi vsebin | `post`, `page`, `product`, `elementor_library`, `e-floating-buttons` | + `wpb_gutenberg_param` |
| Taksonomije | `category`, `post_tag`, `product_cat`, `product_tag`, `product_brand` (ni v uporabi) | enako |
| Permalinki | `/%postname%/`, izdelki in kategorije izdelkov **brez osnove** (`/porocni-prstani/`, `/445-…/`), oznake izdelkov `/oznaka-izdelka/…/` | enako, struktura ohranjena |
| Generiranje izdelkov | WooCommerce `product` z eno sliko, brez opisa. Model in material se na strani izpišeta iz imena in oznak (blok »Model / Material / Kategorija / Izdelava«). | WooCommerce |
| Custom fields | od zunaj ni vidno, preveriti lokalno | – |
| Predloge | child tema (Elementor + lastne WooCommerce predloge). Seznam datotek preveriti lokalno. | – |
| 404 | ✅ pravi status 404, `noindex`, H1 »Te strani ni mogoče najti.«, povezave na kategorije in izbrane modele, telefon | tema |
| Jezik | `lang="sl-SI"` | `sl-SI` |

---

## 3. Indeksiranje dev domene (točka 2 navodil)

- `https://zlatarna-breznik.mmedija.com/` vrača `<meta name='robots' content='noindex, nofollow' />` na vseh straneh, tudi na 404. ✅
  - Oblika z enojnimi narekovaji je WordPressova (`wp_robots`). Najverjetneje velja `blog_public = 0` (»Odvrni iskalnike«). Preveri lokalno: `wp option get blog_public`.
- **`X-Robots-Tag` ni nastavljen.** Ena varovalka (nastavitev v bazi) je premalo, ker se lahko ob uvozu baze ali sinhronizaciji prepiše.
  - Priporočilo: v `.htaccess` **samo za dev host** `Header set X-Robots-Tag "noindex, nofollow"` s pogojem na `HTTP_HOST` (`zlatarna-breznik.mmedija.com`, `zlatar.ddev.site`). Na produkcijski domeni pogoj ne velja, zato ga ob prehodu ni treba brisati.
- `robots.txt` na dev ne blokira CSS, JS ali slik. ✅ Blokira `/wp-admin/`, `/cart/`, `/checkout/`, `/my-account/`. Vsebuje `Sitemap: https://www.zlatarna-breznik.si/sitemap_index.xml`, ki je za produkcijo pravilen.
- Dev domena se v iskalniku ne pojavi (preverjeno z iskanjem po imenu domene). Ob prehodu vseeno preveri v GSC, ali je kakšen `mmedija.com` URL indeksiran.
- **Ob prehodu:** `blog_public = 1`, Yoast → Nastavitve → »Vidnost za iskalnike« vklopljena, preverjen `index, follow` na 10 ključnih URL-jih, `X-Robots-Tag` na produkciji ne sme obstajati.
- Na novi strani **ni canonicalov**, ker Yoast pri `noindex` canonical izpusti. To je pričakovano. Self-referencing canonicale na `https://www.zlatarna-breznik.si/` je treba preveriti **po** vklopu indeksiranja (točka 25).

---

## 4. Ohranitev starih URL-jev (točka 3, podrobno v `redirect-map.csv`)

`redirect-map.csv` ima 343 vrstic: 340 URL-jev iz starih sitemapov in nekaj dodatnih iz navodil.

| ACTION | Število | Pomen |
|---|---|---|
| KEEP | 283 | Isti URL na novi strani vrne 200. |
| 301 | 3 | `/4017-2/ → /guess-nakit/` (na dev že deluje kot en sam 301 ✅), `/cene-porocnih-prstanov-v-letu-2024/ → /cena-porocnih-prstanov/` (še ni narejen), `/kategorija-izdelka/porocni-prstani/ → /porocni-prstani/` (še ni narejen) |
| MANUAL REVIEW | 57 | Oznake bloga in izdelkov, kategorije bloga, arhiv avtorja, `/uncategorized/`, `/my-account/` in 2 morebitna podvojena izdelka. Za vsakega je v stolpcu NEW URL predlagan cilj. |

Stolpec `STATUS` je HTTP status iste poti na novi strani (dev) ob auditu. Stolpec `NOTE` je dodan za razlago.

**Vsi URL-ji s seznama iz navodil obstajajo in vrnejo 200** (tudi `/porocni-prstani/unikatni-porocni-prstani/` in `/ostali-prstani/zenski-prstani/`). Izjema je `/zlatarna-celje/`, ki še ne obstaja (predlog nove strani, točka 13).

**Posebnosti:**
- `/kategorija-izdelka/<kategorija>/` (privzeta WooCommerce pot) vrne 200 s polno vsebino. Na stari strani je imela canonical na `/porocni-prstani/`, na novi canonicala ni videti (noindex). Predlog: eno pravilo 301 `^/kategorija-izdelka/(.*)$ → /$1` (Redirection, regex).
- Trije izdelki imajo v slugu drugo številko kot v imenu: `003-porocni-prstani-…` je model »410 do 413«, `167-porocna-prstana-iz-rdecega-in-belega-zlata` je model »267«, `386-rocno-izdelana-…-2` je model »393«.
  - Model »410 do 413« je v Googlu indeksiran pod slugom `003-…`.
  - **Slugov ne spreminjaj.** Če jih kdaj spremeniš, je obvezen 301.
- Preusmeritve na stari produkciji: `http://zlatarna-breznik.si/ → https://zlatarna-breznik.si/ → https://www.zlatarna-breznik.si/` (**veriga 2 skokov**). `http://www`, `https` brez www, `/kontakt` brez poševnice, `index.php` in `?p=ID` so posamezni 301 ✅.
  - Na novem strežniku je treba en direkten 301 za vse različice nastaviti v `.htaccess` (primer v poglavju 17).
- Redirection je nameščen na obeh straneh. Preveri, ali ima stara stran v Redirectionu pravila, ki jih je treba prenesti: izvoz CSV iz Orodja → Redirection → Uvoz/izvoz.

---

## 5. Title in meta description (točki 4, 5, 17)

### 5.1 Stanje ključnih strani

| URL | Title na stari strani | Title na novi (dev) | Opomba |
|---|---|---|---|
| `/` | Poročni prstani \| Zaročni prstani \| Zlatarna Brežnik | Zlatarna Brežnik pri Celju \| Poročni in zaročni prstani | Dev **premakne »Poročni prstani« s prvega mesta**. Tveganje za glavno ključno besedo. |
| `/porocni-prstani/` | Poročni prstani | Poročni prstani po meri \| Zlatarna Brežnik | ok |
| `/porocni-prstani/unikatni-porocni-prstani/` | Unikatni poročni prstani | Unikatni poročni prstani \| Zlatarna Brežnik, Žalec | ok |
| `/zarocni-prstani/` | Zaročni prstani | Zaročni prstani po meri in z diamanti \| Brežnik | ok |
| `/ostali-prstani/zenski-prstani/` | Ženski prstani | Ženski prstani – zlati, diamantni in unikatni \| Brežnik | ok |
| `/ostali-prstani/prstani-z-briljanti/` | Prstani z briljanti | Prstani z briljanti \| Zlatarna Brežnik, Žalec | ok |
| `/cena-porocnih-prstanov/` | Cena poročnih prstanov - Zlatarna Brežnik | Cena poročnih prstanov \| Zlatarna Brežnik | ok |
| `/cena-zarocnih-prstanov/` | Cena zaročnih prstanov - Zlatarna Brežnik | Cena zaročnih prstanov \| Zlatarna Brežnik | navodila: H1 »Cena zaročnega prstana« |
| `/predstavitev-podjetja/` | Predstavitev podjetja - Zlatarna Brežnik | O nas \| Zlatarstvo Brežnik, Žalec pri Celju, od leta 1999 (57) | ok |
| `/kontakt/` | **Zlatarna Brežnik Celje** | Kontakt \| Zlatarna Brežnik, Šlandrov trg 39, Žalec pri Celju (62) | Stara stran je imela v naslovu »Celje«. Glej lokalni SEO. |

**Statistika nove strani:**
- **109** titlov je daljših od 60 znakov (večinoma izdelki: »… iz rumenega zlata z Brilijanti | Zlatarna Brežnik«).
- **63** URL-jev nima meta description: vse oznake, kategorije bloga, 5 člankov (`/5-stvari-…`, `/kako-uskladiti-…`, `/raje-porocni-ali-zarocni-…`, `/simbolika-…`, `/trendi-moskih-…`) in arhiv avtorja.
- Opis vseh 251 izdelkov je ista predloga: »{ime}. Model si oglejte v Zlatarni Brežnik v Žalcu ali pošljite povpraševanje.« Ni identičen, ni pa unikaten.
- Dejanskih podvojenih titlov ni. Izjemi sta `/porocni-prstani/` = `/kategorija-izdelka/porocni-prstani/` (rešuje 301) in `/cart/`, `/checkout/`, ki se preusmerita na domačo.

### 5.2 Predlogi iz navodil, preverjeni po dolžini

| Stran | Predlog | Znakov |
|---|---|---|
| Domača | Poročni prstani po meri \| Zlatarna Brežnik Žalec pri Celju | 58 |
| Poročni | Poročni prstani po meri \| Ročna izdelava \| Brežnik | 50 |
| Unikatni poročni | Unikatni poročni prstani po meri \| Zlatarna Brežnik | 51 |
| Zaročni | Unikatni zaročni prstani po meri \| Zlatarna Brežnik | 51 |
| Ženski | Unikatni ženski prstani po meri \| Zlatarna Brežnik | 50 |
| Briljanti | Prstani z briljanti in diamanti \| Zlatarna Brežnik | 50 |
| Cena poročni | Cena poročnih prstanov: kaj vpliva na ceno? \| Brežnik | 53 |
| Cena zaročni | Cena zaročnega prstana \| Vodnik Zlatarne Brežnik | 48 |
| Kontakt | Kontakt \| Zlatarna Brežnik Žalec pri Celju | 42 |
| O nas | Zlatarstvo Brežnik Žalec pri Celju \| Od leta 1999 | 49 |
| Izdelek (primer) | 445 – Poročna prstana iz belega zlata z briljanti \| Brežnik | 59 |

Vsi so pod 60 znaki.

**Opozorilo – kanibalizacija:** domača (»Poročni prstani po meri | …«) in `/porocni-prstani/` (»Poročni prstani po meri | Ročna izdelava …«) imata enak začetek.
- Pred uvedbo v GSC preveri, kateri URL danes dobiva klike za »poročni prstani«. Tisti naj obdrži najmočnejši title.
- Drugi naj se loči: domača z blagovno znamko in lokacijo, kategorija z »modeli / katalog / iz belega, rumenega in rdečega zlata«.

V Yoastu je treba te naslove vpisati kot celoten SEO title, brez dodatnega `%%sep%% %%sitename%%`, da se »Zlatarna Brežnik« ne podvoji.

---

## 6. Naslovi H1/H2 in besedilo v DOM (točki 6, 7)

**Napaka s presledki (potrjena v HTML):**

```html
<h1 …><span class="zd-n__a">Poročni prstani,</span><span class="zd-n__b">ki pripovedujejo vašo zgodbo.</span></h1>
<h2 …><span class="zd-n__a">Dva prstana,</span><span class="zd-n__b">ena zgodba.</span></h2>
<h2 …><span class="zd-n__a">Simbol ljubezni,</span><span class="zd-n__b">ki traja.</span></h2>
<p><span>Ročno.</span><span>Z ljubeznijo.</span><span>Za vedno.</span></p>
<h1 class="zd-naslov zd-naslov--stran"><span class="zd-n__a">Unikatni zaročni prstani,</span><span class="zd-n__b">izdelani po meri.</span></h1>
```

- `textContent` (crawler, bralnik zaslona, AI povzetki) zato bere »Poročni prstani,ki«, »Ročno.Z ljubeznijo.Za vedno.«.
- Podobno je v kartici bloga na domači: »nakit.Zgodbeza«.
- **Popravek brez spremembe videza:** med `</span>` in `<span>` vstavi navaden presledek. Pri `display:block` se ne vidi, v besedilu pa je. To velja za vse elemente `zd-n__a/__b` in za trojico »Ročno. Z ljubeznijo. Za vedno.«.

**Stanje H1:**
- Domača: »Poročni prstani, ki pripovedujejo **vašo** zgodbo.« Navodila zahtevajo »**vajino**«.
- `/porocni-prstani/`: »Poročni prstani za vajino zgodbo.« (s piko) ✅ vsebinsko.
- `/porocni-prstani/unikatni-porocni-prstani/`: »Unikatni poročni prstani«. Navodila zahtevajo »Unikatni poročni prstani **po meri**«.
- `/ostali-prstani/zenski-prstani/`: »Unikatni ženski prstani iz naše delavnice.« Navodila zahtevajo »Unikatni ženski prstani«.
- `/cena-zarocnih-prstanov/`: »Cena zaročnih prstanov«. Navodila zahtevajo »Cena zaročnega prstana«.
- `/kontakt/`: H1 »Obiščite nas v Žalcu.« ✅.
- **Izdelki:** H1 je skrajšan na model in tip (»445 Poročna prstana«, »005 Zaročni prstan«), brez materiala. Title je daljši. Navodila zahtevajo unikaten H1 z modelom in materialom.
- **Arhivi oznak izdelkov** (`/oznaka-izdelka/*`): H1 je »Katalog naših prstanov.«, torej enak na vseh 20 URL-jih. Napaka predloge `archive-product.php`.
- **Noga:** naslovi »Hitre povezave«, »O podjetju« in »Kontakt« so `<h2>` na vsaki strani, zato je v strukturi vsakega članka 3–4 H2 več. Predlog: `<p>` ali `<h2>` samo, kjer je smiselno. Prioriteta nizka.
- `/cene-porocnih-prstanov-v-letu-2024/`: ima prazne `<h2>` elemente. Stran se bo tako ali tako preusmerila.

**CTA na domači:** vsi štirje gumbi imajo napis »Ogled kolekcije«. Vodijo na `/katalog/`, `/porocni-prstani/`, `/zarocni-prstani/` in še enkrat na `/katalog/`. Predlog po navodilih:
- »Oglejte si poročne prstane« → `/porocni-prstani/`
- »Oglejte si zaročne prstane« → `/zarocni-prstani/`

**Kartice izdelkov:** 24× gumb »Poglej« na vsaki kategoriji je neopisno besedilo povezave. Dodaj `aria-label="Poglej model 445 – Poročna prstana"` ali skrit opis.

---

## 7. Sitemap, robots, canonical

- **Sitemap (Yoast):**
  - V `page-sitemap.xml` so na dev **`/cart/`, `/checkout/` in `/my-account/`**. Te strani morajo biti noindex in izključene. `/cart/` in `/checkout/` se 302 preusmerita na domačo.
  - Arhiva avtorja na dev ni več v sitemapu ✅.
  - `/guess-nakit/` in nov članek `/kako-izbrati-unikaten-zarocni-prstan/` sta v sitemapu ✅.
- **Oznake** (30 bloga, 20 izdelkov) so v sitemapu in so indeksabilne, večinoma brez vsebine (22–90 besed). Glej poglavje 10.
- **Robots.txt na stari produkciji** je napačen: `Disallow: /zlatar/wp-admin/` (pot iz stare namestitve v podmapi). Nova datoteka je pravilna ✅.
- **Canonical:** na dev ni viden (noindex). Na stari strani je self-referencing ✅.

---

## 8. Structured data (točka 19)

**Stanje na dev:**
- **Organization + JewelryStore** (en vozel `#organization`): ime, alternativna imena, `legalName` »Zlatarna Brežnik, Dejan Brežnik s.p.«, `foundingDate` 1999, `vatID`, telefon `+386 3 710 40 60`, e-pošta, naslov Šlandrov trg 39, 3310 Žalec, `openingHoursSpecification` (pon–pet 8–12, 14–17), `hasMap`, `areaServed` (Žalec, Celje, Savinjska, Slovenija), `knowsAbout`, logo. ✅
  - **Manjka:**
    - `geo`: koordinate je treba preveriti. Stara stran je v Google Maps embedu imela 46.2506, 15.1605; pred uporabo potrdi.
    - `image`: fotografija zlatarne. Zdaj je slika samo logotip 214×233.
    - `sameAs`: na dev samo Facebook. Lokalna različica naj bi imela že Google profil (`place_id ChIJCf_FfvtwZUcReHnal3fewYQ`), preveri.
    - `priceRange` je neobvezen in brez podatka ne sodi zraven.
- **WebSite** s `SearchAction` ✅.
- **BreadcrumbList** na vseh straneh ✅.
  - Pri izdelkih je pot v JSON `Domov › Katalog › izdelek`, vidne drobtine pa so `Domov › Katalog › Poročni prstani › izdelek`. Poenoti (Yoast primarna kategorija).
  - V imenu je neodkodiran `&#8211;`, ki naj bo `–`.
- **Article** na člankih ✅. Avtor je hkrati organizacija in `Person` »Milan« z Gravatarjem.
  - Za E-E-A-T je bolje, da je avtor strokovnjak (npr. Dejan Brežnik, zlatar) z lastnim profilom ali organizacija, ne izvajalec spletne strani. Odloči naročnik.
- **FAQPage** na kategorijah (`/porocni-prstani/`, unikatni, zaročni, ženski, briljanti).
  - Vsebinsko dobro za GEO. FAQ rich results Google od 2023 kaže samo izbranim (vladnim in zdravstvenim) stranem, zato ne pričakuj zvezdic ali razširitev.
  - Vprašanja naj bodo vidna na strani (so) in **ne enaka na vseh kategorijah**: preveri, da se ne ponavljajo.
- **Product: ni ga.** Izdelki imajo samo `ItemPage` + `ImageObject`. Ni nobenega `Offer`, `AggregateRating` ali `Review` ✅ (pravilno po navodilih).
  - Če dodamo `Product` brez `offers/review/aggregateRating`, ga Google za rich results ne upošteva. V GSC bo »Product snippets – manjka offers«, kar ni napaka indeksiranja.
  - Predlog: `Product` z `name`, `image`, `sku`/`mpn` (model), `brand` (Zlatarna Brežnik), `material`, `category`, **brez cene**. Opozorilo v GSC sprejmemo. Druga možnost je, da Product ne dodamo. Odločitev v poglavju 18.
- **VideoObject: ga ni.** Na domači in na O nas je YouTube video `s2Mb0vOy48E` (»Ročna izdelava prstana«) kot fasada na klik ✅. Dodaj `VideoObject` z `name`, `description`, `thumbnailUrl`, `uploadDate` (z YouTuba) in `embedUrl`. Brez tega video ni upravičen do prikaza v Googlu kot video rezultat.

---

## 9. Open Graph, favicon

- `og:title` na domači je samo »Zlatarna Brežnik« (Yoast »site name«). Predlog: enak kot title strani.
- `og:image`:
  - na domači `skica-zarocnega-prstana-768x702.jpg` (premajhna, priporočeno 1200×630);
  - **na vseh kategorijah in oznakah ista slika** `9504-unikatna-prstana-rdeco-zlato.jpg`. Predlog: vsaka kategorija svojo reprezentativno sliko 1200×630.
- `og:type` na kategorijah je `article` (Yoast), izdelki `article` (na stari strani je bil `product`). Ni kritično.
- `twitter:card` = `summary_large_image` ✅.
- **Favicon:** `porocni_prstani_breznik_7C6_icon.ico` je uporabljen za `icon` 32×32, `icon` 192×192 **in** `apple-touch-icon`. Predlog: »Ikona spletnega mesta« v WP (PNG 512×512), ki ustvari 32, 180, 192 in 270. Potreben je kvaliteten logotip ali znak.

---

## 10. Vsebina, ključne besede in taksonomije (točke 4–13)

### 10.1 Mapiranje ključnih besed → ena primarna stran

| Namera | Primarna stran (obstaja) | Tekmovalci, ki jih je treba umiriti |
|---|---|---|
| brand + poročni prstani + Žalec/pri Celju | `/` | – |
| poročni prstani, zlati, moški, preprosti | `/porocni-prstani/` | `/tag/porocni-prstan/`, `/tag/porocni-prstani/`, `/kategorija-izdelka/porocni-prstani/`, `/oznaka-izdelka/*-porocni-prstan/` |
| unikatni poročni prstani | `/porocni-prstani/unikatni-porocni-prstani/` | `/tag/najlepsi-porocni-prstani/` |
| zaročni prstani, unikatni zaročni | `/zarocni-prstani/` | **`/oznaka-izdelka/zarocni-prstan/`, `/oznaka-izdelka/zarocni-prstani/`, `/tag/zarocni-prstan/`, `/tag/zarocni-prstani/`** |
| ženski prstani | `/ostali-prstani/zenski-prstani/` | `/oznaka-izdelka/zenski-prstan/` |
| prstani z briljanti/diamanti | `/ostali-prstani/prstani-z-briljanti/` | `/oznaka-izdelka/brili/`, `brilijanti/`, `diamanti/`, `/tag/diamantni-prstan(i)/` |
| cena poročnih prstanov | `/cena-porocnih-prstanov/` | **`/cene-porocnih-prstanov-v-letu-2024/`**, `/tag/cenik-porocnih-prstanov/`, `/tag/cena-porocnega-prstana/` |
| cena zaročnega prstana | `/cena-zarocnih-prstanov/` | `/tag/cena-zarocnega-prstana/` |
| zlatarna Celje / zlatarstvo Celje | (ni namenske) → predlog `/zlatarna-celje/` | `/kontakt/` (stari title »Zlatarna Brežnik Celje«) |
| zlatarna/zlatarstvo Žalec | `/kontakt/` in `/predstavitev-podjetja/` | – |

### 10.2 Oznake (`/tag/*`, `/oznaka-izdelka/*`)

- **50 indeksabilnih arhivov** s 22–90 besedami in brez meta description.
- Napake v imenih:
  - `redeco-zlato` (pravilno `rdeco-zlato`);
  - `rose-gold` (angleški dvojnik);
  - `brili`, `brilijanti` in `diamanti` za isto stvar (pravilno »briljanti«);
  - `pose` (nedokončano).
- **Predlog** (vse je v `redirect-map.csv` kot MANUAL REVIEW, ničesar ni izvedeno):
  1. Oznake, ki tekmujejo z glavnimi stranmi: **301** na glavno stran (zaročne, cene, poročne, graviranje, barve diamanta).
  2. Materialne oznake izdelkov (`belo-zlato`, `rumeno-zlato`, `rdeco-zlato`, `kombinirani-porocni-prstan`): ostanejo kot URL in UX filtri z **`noindex, follow`**.
  3. Dvojnike in napake: 301 na pravilno oznako, izdelke prestavi na pravilno oznako.
  4. Ostale oznake bloga brez vrednosti (`poroka`, `srebro`, `platina`, `nalozba` …): `noindex, follow` in izključiti iz sitemapa.
- **Pogoj:** pred vsakim 301 preveri v GSC, ali ima oznaka klike. Oznaka s kliki dobi 301 na najbolj podobno stran, ne noindex.

### 10.3 Članki in strani

- **`/3902-2/`** (3.118 besed): mora se v celoti prenoviti. Vsebuje:
  - »V oddaji vam bomo predstavili«;
  - odstavek o **Tiffany & Co., Cartier in Bvlgari**;
  - **»Primerjalna tabela: Diamantni prstani … 999 €, 2.499 €, 1.799 €«** (izmišljene cene, platina);
  - meta opis v prvi osebi »Predstavljam vam izbor«.
  - URL ostane `/3902-2/`.
- **`/cene-porocnih-prstanov-v-letu-2024/`** (2.278 besed): večinoma o stroških poroke (banket, obleka, potovanje, »14.000 €«). Uporaben je samo del o dejavnikih cene prstanov. Ta del prenesi v `/cena-porocnih-prstanov/`, nato 301.
- **`/cena-porocnih-prstanov/`:**
  - »stroškovno znaša približno višino dveh mesečnih plač« in »tudi od 200€ dalje« **potrdi naročnik ali umakni**;
  - H2 »IZBERI POROČNI PRSTAN« se ponovi 2×.
- **`/cena-zarocnih-prstanov/`:** »povprečne stroške zaročnega prstana v letu 2020« odstrani, vsebino naredi evergreen.
- **Datumi v naslovih:** `/trendi-zarocnih-prstanov-v-letu-2020/` in `/trendi-zarocnih-prstanov-za-leto-2021/` sta zastarela in tekmujeta. URL-jev ne spreminjaj. Predlog: posodobiti vsebino ali jih združiti v en evergreen članek s 301 (MANUAL REVIEW, odvisno od GSC).
- **Domača, sekcija »Zanimivosti«:** prikazuje »Cene poročnih prstanov v letu 2024« (stran, ki bo preusmerjena). Zamenjaj z evergreen stranjo cen.
- Novi strani `/guess-nakit/` (64 besed) in `/kako-izbrati-unikaten-zarocni-prstan/` sta ✅. Guess je tanka vsebina, sprejemljivo za stran blagovne znamke.
- `/swarovski-elements/` (20 izdelkov y1–y20, brez opisov). Barvne variante istih modelov imajo skoraj enake fotografije. **Naročnik naj potrdi, ali Swarovski še prodaja.**
- Interne povezave: na dev je le 1 trdo kodirana povezava na `www.zlatarna-breznik.si` (`/ideje-za-romanticno-snubitev/`), kar je po selitvi pravilno. Povezav na `zlatar.ddev.site` v HTML ni ✅.

---

## 11. Izdelki in podvojeni modeli (točki 14, 15)

### 11.1 Ugotovljeni pari z enako številko modela (11 parov)

| Model | URL A | URL B | Ugotovitev |
|---|---|---|---|
| **432–442** | `/43x-porocna-prstana-iz-…` (2025/12, WebP, poročni par) | `/43x-zarocni-prstan-iz-…` (2024/12, zaročni prstan s kamnom) | **Niso duplikati.** Vizualno preverjeno za 432, 433 in 434: na A je par poročnih prstanov, na B zaročni prstan s solitairom. Gre za **dve seriji z enakimi številkami**. Oba URL-ja ostaneta (KEEP). |
| 433 (iz navodil) | `/433-porocna-prstana-iz-belega-zlata/` | `/433-zarocni-prstan-iz-belega-zlata/` | Različna izdelka (par belih poročnih / zaročni prstan z diamantom). **Brez 301.** Priporočilo: v imenu jasno ločiti (npr. »Zaročni prstan 433« in »Poročna prstana 433«). Naročnik naj pove, ali imata seriji v delavnici drugačno oznako. |
| 039 | `/039-porocna-prstana-iz-rumenega-zlata-in-enim-briljantom/` | `/039-porocna-prstana-z-prevleko-iz-crnega-rodija/` | Različna (rumeno zlato z briljantom / črni rodij s prstnim odtisom). |
| 057 | `/057-porocna-prstana-iz-rumenega-zlata-in-briljanti/` | `/057-porocna-prstana/` | Različna (rumeno zlato z briljanti / gravura »I love you«). |
| **118** | `/118-rocno-izdelana-porocna-prstana-iz-belega-in-rumenega-zlata/` | `/118-porocna-prstana/` | **Verjetno isti model** (enak teksturiran belo-rumen dizajn z vrsto kamnov, druga fotografija). MANUAL REVIEW: po GSC izberi canonical, drugi 301. |
| **067 / 068** | `/067-porocna-prstana/` | `/068-porocna-prstana/` | Fotografiji skoraj enaki (bel prstan + prstan s črnimi/belimi kamni). MANUAL REVIEW, naročnik naj potrdi. |
| y1–y20 | Swarovski | | Barvne variante, ne duplikati. Vsebinsko tanke. |

Popolnoma enakih slik ali naslovov med izdelki ni.

### 11.2 Napačne ali nejasne kategorije

- **152 – Posebni – Unikatni poročni prstani:** kategorije `ostali-prstani` + `porocni-prstani` + `prstani-z-briljanti`. Fotografija kaže poročna prstana iz belega zlata, eden z diamanti. Predlog:
  - primarna kategorija (Yoast) = Poročni prstani;
  - obdrži Prstani z briljanti;
  - odstrani nadrejeno »Ostali prstani«, ki je odveč, ker podkategorija že spada pod njo.
- **39 izdelkov** iz kategorije Poročni prstani je hkrati v `ostali-prstani` (večinoma prek `prstani-z-briljanti`), med njimi 152, 057, 075, 125, 146, 149, 150, x, x1 in x2. Isti predlog: primarna kategorija Poročni prstani, »Ostali prstani« samo, kjer nima druge.
- **x1 – Kombinacija poročnega in zaročnega prstana:** ni v zaročnih.
- **x3 – Poročna in zaročna prstana:** ni v poročnih.
- 17 izdelkov z briljanti v imenu ni v kategoriji `prstani-z-briljanti` (npr. 445, 444, 443, 440, 439, 436, 415, 414 …). Naročnik naj potrdi, ali so v »Prstani z briljanti« zaželeni vsi prstani s kamni.
- Kategorija `/uncategorized/` je prazna, `product_brand` pa ni v uporabi.

### 11.3 Kakovost izdelkov

- **Opis:** 251/251 nima opisa (`description` prazen). 123 nima niti kratkega opisa. Kratki opisi, ki obstajajo, so ena vrstica (npr. »Ročno izdelana poročna prstana iz belega in rumenega zlata.«).
- **Besedilo na strani izdelka** je pri vseh enako (»Ročno izdelan v naši delavnici v Žalcu. Model lahko prilagodimo …«). Zato so si strani izdelkov skoraj enake. Unikatnih 50–100 besed brez dejanskih podatkov naročnika (širina, profil, obdelava, kamni) **ne napišemo**.
- **Alt:** pri 206/251 glavnih slikah je alt prazen. Kjer obstaja, ima napake (»Birlijanti«, »št- 445«, »rumenga«, »brilanti«).
- **Imena** z napakami: »rumenga« (437, 439, 441), »Birlijanti« (434), »brilanti« (427), »Brilijanti« (410–413), »porocna« brez šumnika (125, 194), »Rocno« (115), manjkajoči pomišljaji (»047-«, »006-«, »125-unikatna«, »393 Poročna…«).
  - Popravek imena ne spremeni URL-ja, zato je varen.
- **Valuta USD in cena 0:** nastavi EUR (WooCommerce → Nastavitve → Splošno). Cena 0 ostane, ker ni nakupa. Ne sme pa nastati `Offer`.
- **Na strani izdelka je ✅:**
  - model, material in kategorija v tabeli;
  - CTA »Pošljite povpraševanje« in telefon;
  - sorodni izdelki (»Morda vam bo všeč tudi«);
  - vidne drobtine;
  - srce kot `<button>` z `aria-label="Dodaj med priljubljene: 433 – …"`.

### 11.4 Predlog strukture za izdelke (brez izmišljenih podatkov)

- **Title:** `[MODEL] – [Poročna prstana | Zaročni prstan | Ženski prstan] iz [belega/rumenega/rdečega/kombiniranega zlata][ z briljanti] | Brežnik`
  - Material in kamni **samo iz obstoječih oznak in imena**. Kjer jih ni, se izpustijo.
- **H1:** isto brez »| Brežnik«, na primer »445 – Poročna prstana iz belega zlata z briljanti«.
- **Alt:** `[Tip] model [MODEL] iz [materiala][ z briljanti] – Zlatarna Brežnik`
- **Ime datoteke** (samo za nove nalaganja, obstoječih ne preimenovati zaradi Google Images): `445-porocna-prstana-belo-zlato-briljanti.webp`.

---

## 12. Slike (točka 16)

**Stanje na dev:**
- Vse vsebinske slike izdelkov imajo `width`/`height` in `srcset`/`sizes` ✅.
- Na domači so 3 `<img>` brez dimenzij (ikone ali SVG, glej poročilo hitrosti).
- Domača preloada hero `porocna-prstana-na-marmorju-zlatarna-breznik.webp` ✅.
- Kategorije: 24 od 27 slik ima `loading="lazy"` ✅. Ali je prva vrstica (nad pregibom) lazy, glej poglavje 15.
- Izdelki iz 2025/12 so WebP. Starejši so na mmedija.com še JPG.
  - Lokalno je bilo po poročilu seje »zlatar« vse pretvorjeno v WebP s 301 iz `.jpg` na `.webp`. Ob prenosu preveri, da preusmeritev slik deluje tudi na LiteSpeedu (pravilo v `.htaccess`, ne samo v PHP).
- AVIF: LiteSpeed Cache (QUIC.cloud) ali WP 6.5+ to zmore. Za nakit je WebP q≈82 dober kompromis. AVIF le, če ostanejo podrobnosti kamnov.

---

## 13. Lokalni SEO (točka 18)

- **NAP na novi strani** je dosleden: Zlatarna Brežnik, Dejan Brežnik s.p., Šlandrov trg 39, 3310 Žalec, 03 710 40 60, 041 424 648, info@zlatarna-breznik.si ✅.
- **Kontakt na dev:**
  - Ima naslov, telefon, mobilni telefon, e-pošto, Facebook, zemljevid (iframe) in obrazec ✅.
  - **Delovni čas ni viden v besedilu strani.** Je samo v meta opisu in shemi. Navodila ga zahtevajo vidno.
- **Stara stran je imela drugo lokacijo:** »Mod'Art, razstavni salon – Domžale, Slamnikarska c. 3, 1230 Domžale, tel. 01 724 45 88«. Na novi je ni. Naročnik naj potrdi, ali salon še prodaja njihove prstane, ker vpliva na lokalne citate.
- **Zunanji imeniki** (iskanje po imenu podjetja) še vedno navajajo **Celje**:
  - Facebook stran »Zlatarna Brežnik – Celje, Žalec«;
  - moja-dejavnost.si (»Poročni prstani Celje«, »… Domžale«);
  - poroka-bo.si (»Zlatarna Celje«);
  - visitcelje.eu;
  - toplocalplaces.com;
  - na nekaterih je naslov napačno zapisan kot »Šlandov trg«.
  - Za lokalni SEO je treba NAP poenotiti. Delo za naročnika, glej `POTREBUJEMO-OD-NAROCNIKA.md`.
- **Predlog `/zlatarna-celje/`:**
  - H1 »Zlatarna pri Celju – obiščite nas v Žalcu«;
  - jasno navede, da je poslovalnica **v Žalcu, ~10 km od Celja** (podatek je že na strani);
  - pot iz Celja (avto, parkiranje, avtobus, kar potrdi naročnik), zemljevid, delovni čas, poročni in zaročni prstani, posvet;
  - **ne trdi, da je poslovalnica v Celju**;
  - meta title »Zlatarna pri Celju – obiščite nas v Žalcu | Brežnik« (51).

---

## 14. GEO / generativno iskanje (točka 20)

- **Pozitivno:**
  - FAQ bloki na kategorijah z neposrednimi odgovori (»Ali imate zlatarno v Celju? Ne več. … danes samo v Žalcu …«);
  - shema JewelryStore z `knowsAbout`, `areaServed` in `foundingDate`.
- **Blokada AI robotov na `/kontakt/`** (poglavje 1, točka 1). Ravno stran z NAP je za PerplexityBot in ClaudeBot nedosegljiva. Na stari produkciji je za GPTBot vrnila prazen odgovor.
  - Rešitev pri gostitelju: izklop »reCAPTCHA protection« za URI `/kontakt/` ali seznam dovoljenih robotov. Zaščito pred spamom obrazca naj prevzame CF7 (honeypot, Turnstile).
- **Manjkajoči odgovori za GEO:** »Kakšna je razlika med diamantom in briljantom?«, »Koliko prej naročiti poročna prstana?« (le »2–3 mesece« v FAQ, potrdi naročnik), »Katere vrste zlata uporabljate?« (karati 14 k/18 k niso nikjer navedeni, potrdi naročnik).
- `llms.txt`: lokalna seja ga je dodala. Na mmedija.com preveri po naslednjem prenosu.
- **Dosledna raba izrazov:** Zlatarna Brežnik · Dejan Brežnik s.p. · Šlandrov trg 39, 3310 Žalec · od leta 1999 · ročna izdelava · izdelava po meri. Na dev je to večinoma spoštovano.
  - Izjema je »Zlatarstvo Brežnik« (O nas). Je legitimno alternativno ime, a ga uporabljaj zavestno.

---

## 15. Hitrost, UX in dostopnost (točke 22–24)

Celotno poročilo s tabelami, selektorji in priporočili je v **`HITROST-UX-POROCILO.md`**.
- Merjeno z Lighthouse 12.8 (mobilno: slow 4G, 4× CPU) in Playwright pri 360, 375, 390, 430 in 1440 px, z axe-core.
- Merjeno prek izhodnega proxyja, ki doda ~0,3–0,5 s na povezavo, zato so absolutni časi okvirni.
- Izbrani posnetki so v `posnetki/`.

### 15.1 Številke

| | Stara produkcija (mobilno) | Nova dev (mobilno) | Nova dev (namizno) |
|---|---|---|---|
| Domača: Performance | 56 | 77–83 | 89 |
| Domača: LCP / FCP | 6,3 s / 5,8 s | 3,6–4,1 s / 2,7 s | 1,4 s / 1,1 s |
| Domača: TBT / CLS | 153 ms / 0,027 | 2 ms / 0 | 0 / 0 |
| Domača: teža / zahtevki | 4.717 KB / 116 | 836 KB / 53 | 1.004 KB / 61 |
| `/porocni-prstani/`: Performance / LCP / CLS | 51 / 5,2 s / **0,234** | 75–86 / 3,9–4,9 s / 0 | 93 / 1,4 s / 0 |
| Izdelek (`/147-porocna-prstana/`) | – | 86 / 3,5 s | 92 / 1,4 s |
| `/3902-2/` | – | **64 / 6,8 s** | 86 / 1,8 s |

- **CLS ≤ 0,1** ✅ povsod.
- **INP:** TBT 0–2 ms je dober posredni kazalnik (≤ 200 ms) ✅.
- **LCP ≤ 2,5 s:** namizno ✅, mobilno ❌ (3,5–4,9 s, `/3902-2/` 6,8 s).
- Dostopnost: 86–88 mobilno in 91–93 namizno. Best Practices: 100. SEO: 66 izključno zaradi `noindex`.

### 15.2 Glavni vzroki in popravki brez spremembe dizajna

1. **LCP podstrani je CSS ozadje `ozadje-marmor-svetlo.jpg`** v `section.zd-glava-strani` (82 KB JPG).
   - Ni prednaloženo, zato se odkrije šele po CSS: zakasnitev 2,1–2,6 s, na `/3902-2/` 4,8 s.
   - Popravek: pretvorba v WebP, `<link rel="preload" as="image" fetchpriority="high">` na vseh predlogah z glavo strani, mobilna različica.
2. **Ni predpomnilnika strani:** HTML nima `x-litespeed-cache`, PHP doda ~0,3–0,5 s TTFB. Popravek: LSCache »Cache« vklopljen na produkciji.
3. **9–16 blokirajočih virov v `<head>`:** jQuery + jquery-migrate (Elementor strani), Cookie Notice JS, 10+ drobnih CSS, Trustindex CSS dvakrat.
   - Popravek: defer in JS v nogo, združitev drobnih CSS, `@font-face` inline, odstranitev dvojnika.
   - Lokalna seja je jQuery že umaknila, a na mmedija.com se še nalaga. Preveri po prenosu.
4. **`/3902-2/`:** 5 slik v HTML kot **base64** (HTML ima 569 KB), brez `width/height`. Prenesi jih v knjižnico medijev. Slug ostane.
5. **Logotip** v glavi ima `fetchpriority="high"` in tekmuje s hero sliko. Odstrani prioriteto, pretvori v SVG/WebP.
6. **Trustindex:**
   - takoj ob nalaganju pomeni 9 zahtev in 97 KB, `loader.js` brez cache glave;
   - widget je do zagona JS skrit (`opacity:0;height:0`).
   - Popravek: nalaganje ob približanju `#mnenja` (IntersectionObserver) in strežniško izrisan HTML viden brez JS.
7. **Google Maps** na Kontaktu se kljub `loading="lazy"` naloži takoj (~470–630 KB) in pred privolitvijo v piškotke. Popravek: fasada na klik, enako kot za YouTube.
8. **Slike:**
   - ozadji kolekcij na domači sta JPG (127 KB in 89 KB);
   - starejši izdelki so JPG;
   - 5 slik pod pregibom na domači ni lazy;
   - prva kartica v katalogu je lazy, čeprav je na 390 px v prvem zaslonu;
   - prevelike slike na O nas (~180 KB).
9. **Pisave:** lokalne woff2 s `font-display: swap` ✅. Prednaložene so samo `latin`, **`latin-ext` (č/š/ž) ne**, zato se č/š/ž v naslovih na kratko izrišejo z nadomestno pisavo. Popravek: preload `jost-latin-ext` in `cinzel-…-latin-ext`.
10. **Predpomnilnik statičnih virov** je 7 dni. Priporočeno je 1 leto + `immutable` za `?ver=`, pisave in `uploads`.
11. Stisnjenje: `br` ✅.

### 15.3 UX in dostopnost

- **Gumb mobilnega menija** `button.zd-glava__odpri`:
  - nima dostopnega imena (»Meni« ima `display:none`);
  - meri **22×13 px**;
  - po odprtju Tab gre na vsebino za menijem (povezave so v DOM pred gumbom, fokus ni ujet);
  - pri zaprtem meniju je fokusabilna nevidna povezava »Svet prstanov«.
- **»Preskoči na vsebino«** ob fokusu ostane nevidna.
- **Kontrast zlate:**
  - `#a07d45` na beli 3,8:1, `#a8844e` 3,45:1, bel tekst na zlatih gumbih 3,45–3,8:1;
  - primeri: »POGLEJ« 24× na vsakem arhivu, »OGLED KOLEKCIJE«, »Pošlji sporočilo«;
  - `#90703e` doseže 4,59:1 in je komaj opazno temnejši;
  - velike naslove in dekor lahko ostanejo.
- **Srca (priljubljeni):**
  - pravilno: `<button>`, `aria-label` z modelom, `aria-pressed`, Enter/Space delujeta ✅;
  - na karticah domače merijo 19×19 px, v glavi 21×21 px;
  - števec v glavi ni del imena;
  - **na karticah kataloga in kategorij srca ni**: nedoslednost ali namen?
- **Piškotna pasica:**
  - na mobilnem prekrije 25 % zaslona (208 px) in zakrije fokusirane elemente (WCAG 2.4.11);
  - `aria-label` »Cookie Compliance« je angleški.
  - Posnetek: `posnetki/domaca-prvi-zaslon-390.jpg`.
- **Kontaktni obrazec:**
  - ✅ oznake (ovijajoči `<label>`), `autocomplete`, napake prek CF7 `aria-live`;
  - ❌ obvezna polja niso vidno označena;
  - ❌ ob obrazcu ni stavka o zasebnosti;
  - ❌ polja imajo ob fokusu `outline:none`.
- **Cilji dotika < 44 px:** povezave v nogi in drobtine so visoke 20–23 px, Facebook ikona 20×28. Popravek s paddingom, ikone ostanejo enake.
- **Postavitev:** vodoravnega preliva ni na nobeni širini (360–1440) ✅. Meni se odpre in zapre s klikom in z Escape, `aria-expanded` ✅.
- **YouTube:** fasada na klik (`a.zd-video`, video `s2Mb0vOy48E`, `youtube-nocookie`) na domači in O nas ✅, pred klikom 0 B. Popraviti:
  - `aria-label` se ne ujema z vidnim »Oglejte si film«;
  - vsi videi imajo enak `iframe.title`.
- **Analitika:** GA4 `G-L0M9SC4KZ6` se naloži šele po privolitvi ✅.
- Arhivi: `section.zd-glava-strani` (H1 in uvod) je zunaj `<main>`. Na `/3902-2/` je preskočen nivo naslova (h3 brez h2).

---

## 16. Tretje strani, analitika, varnost

- **Trustindex (Google mnenja):**
  - CSS `trustindex-google-widget.css` se na domači naloži **dvakrat**;
  - vtičnik nalaga JS in vire s cdn.trustindex.io (glej poglavje 15);
  - shema `AggregateRating` iz teh mnenj **ni** dodana ✅ in je ne dodajamo.
- **YouTube:** video `s2Mb0vOy48E` na domači in O nas je narejen kot fasada (iframe `youtube-nocookie` šele po kliku) ✅. Manjka VideoObject (poglavje 8).
- **Google Maps:** iframe na `/kontakt/` ima `loading="lazy"`, a se naloži takoj (~470–630 KB, piškotki pred privolitvijo). Predlog: fasada s statično sliko in povezavo.
- **Analitika:** stara stran ima Universal Analytics `UA-135258619-1` (ne deluje več). Nova ima GA4 `G-L0M9SC4KZ6`, ki se naloži šele po privolitvi (Cookie Notice) ✅. Pred prehodom preveri lastništvo računa, povezavo z GSC in nastavljene konverzije (oddaja obrazca, klik na telefon).
- **Pred prehodom odstrani ali zakleni:**
  - **Duplicator** (javni REST `duplicator/v1`; po selitvi izbriši pakete in `installer.php`);
  - **Elementor MCP Composer** (javni REST `elementor-mcp-composer/v1.0.18` je razvojno orodje za AI urejanje);
  - Elementor AI po želji.
  - Jetpack: preveri, ali se sploh uporablja.

---

## 17. Produkcijski prehod – checklist (točki 25, 26)

**Ne izvajaj brez potrditve.** Postopek predvideva, da nova stran nadomesti staro na istem strežniku ali na novem gostovanju z domeno `www.zlatarna-breznik.si`.

**Pred prehodom**
1. Popolna varnostna kopija **stare** produkcije (datoteke + baza) in nove dev strani. Git commit child teme.
2. Izvoz Redirection pravil s stare strani.
3. GSC: izvoz »Strani« in »Poizvedbe« za zadnjih 16 mesecev (osnova za stolpec GSC PRIORITY in MANUAL REVIEW).
4. Vse odločitve MANUAL REVIEW iz `redirect-map.csv` potrjene in vpisane v Redirection (regex za `/kategorija-izdelka/(.*)`).
5. Valuta EUR. Duplicator, MCP Composer in testni uporabniki odstranjeni. WP in vtičniki posodobljeni.
6. Gostitelj: izklop reCAPTCHA za `/kontakt/` (ali allowlist robotov).

**Prehod**
1. Prenos datotek in baze na produkcijo.
2. Varen search-replace (najprej `--dry-run`, GUID-ov ne spreminjamo):
   ```bash
   wp search-replace 'https://zlatarna-breznik.mmedija.com' 'https://www.zlatarna-breznik.si' --all-tables --skip-columns=guid --precise --report-changed-only --dry-run
   wp search-replace 'https://zlatarna-breznik.mmedija.com' 'https://www.zlatarna-breznik.si' --all-tables --skip-columns=guid --precise --report-changed-only
   # če baza pride z lokalnega ddev:
   wp search-replace 'https://zlatar.ddev.site' 'https://www.zlatarna-breznik.si' --all-tables --skip-columns=guid --precise --report-changed-only
   # serializirani zapisi Elementorja (JSON z ubežnimi poševnicami):
   wp search-replace 'https:\/\/zlatarna-breznik.mmedija.com' 'https:\/\/www.zlatarna-breznik.si' --all-tables --skip-columns=guid --precise --report-changed-only
   wp option get home && wp option get siteurl   # oba: https://www.zlatarna-breznik.si
   ```
   Nato Elementor → Orodja → Zamenjaj URL (za `_elementor_data`) in Elementor → Orodja → Regeneriraj CSS.
3. `wp option update blog_public 1`. Odstrani dev `X-Robots-Tag` (če je vezan na host, ni treba).
4. `.htaccess`: **en** direkten 301 za vse različice:
   ```apache
   RewriteEngine On
   RewriteCond %{HTTPS} off [OR]
   RewriteCond %{HTTP_HOST} !^www\.zlatarna-breznik\.si$ [NC]
   RewriteRule ^(.*)$ https://www.zlatarna-breznik.si/$1 [R=301,L]
   ```
   Pravilo mora biti pred blokom WordPress. Poševnico na koncu doda WordPress v istem koraku le, če pravilo ne naredi prvega skoka. Preveri, da `http://zlatarna-breznik.si/kontakt` naredi en sam 301.
5. `wp rewrite flush --hard`, LiteSpeed Cache → Nastavitve → Shrani (zapiše pravila), nato »Počisti vse«.
6. Yoast: Orodja → »Optimiziraj podatke SEO« (indeksabilni podatki), odpri `sitemap_index.xml` (ponovno se ustvari).

**Takoj po prehodu**
1. 10 ključnih URL-jev: 200, `index, follow`, self canonical na `https://www.zlatarna-breznik.si/…`, brez `mmedija.com` v HTML:
   - `/`
   - `/porocni-prstani/`
   - `/porocni-prstani/unikatni-porocni-prstani/`
   - `/zarocni-prstani/`
   - `/ostali-prstani/zenski-prstani/`
   - `/cena-porocnih-prstanov/`
   - `/cena-zarocnih-prstanov/`
   - `/kontakt/`
   - `/3902-2/`
   - `/445-porocna-prstana-iz-belega-zlata-in-z-briljanti/`
2. Sitemap: samo produkcijski URL-ji, brez `/cart/`, `/checkout/`, `/my-account/`.
3. `robots.txt` brez `/zlatar/` in z vrstico Sitemap.
4. Celoten `redirect-map.csv`: skripta preveri vsak OLD URL (pričakovan status, en skok, končni 200).
5. Rich Results Test na domači, eni kategoriji, enem izdelku in enem članku.
6. GSC: oddaj sitemap, »Pregled URL-ja« za 10 ključnih strani, spremljaj »Strani« in »Preusmeritve« 4–6 tednov.
7. Google Business Profile: spletna stran = `https://www.zlatarna-breznik.si/`.

---

## 18. Odločitve, ki čakajo (MANUAL REVIEW)

1. Oznake bloga in izdelkov: 301, `noindex, follow` ali KEEP, po GSC klikih (poglavje 10.2, `redirect-map.csv`).
2. Podvojeni izdelki 118 in 067/068: kateri URL je canonical.
3. Product shema brez cene (sprejmemo opozorilo GSC) ali brez Product.
4. Članka o trendih 2020/2021: posodobitev ali združitev.
5. Swarovski elements in Guess: ali ostaneta v ponudbi.
6. Arhiv avtorja »Milan«: izklop ali preusmeritev. Avtor člankov v shemi.
7. Title domače in `/porocni-prstani/` po GSC (kanibalizacija).
8. Nova stran `/zlatarna-celje/`: da/ne.

---

## 19. Predlagan vrstni red izvedbe (lokalno na `zlatar.ddev.site`)

1. **Backup + git commit** child teme in posnetek baze (`ddev export-db`) pred vsako spremembo.
2. Hitri tehnični popravki brez vpliva na dizajn:
   - presledki v `zd-n__a/__b`;
   - H1 arhivov oznak;
   - valuta EUR;
   - `/cart/`, `/checkout/` in `/my-account/` iz sitemapa;
   - podvojen Trustindex CSS;
   - dev `X-Robots-Tag`;
   - favicon.
3. Title in meta za 10 ključnih strani (poglavje 5.2). Manjkajoči meta opisi pri člankih.
4. Vsebina:
   - `/3902-2/`;
   - evergreen cene (poročni in zaročni) + 301 za 2024;
   - unikatni poročni (landing);
   - ženski (100–200 besed);
   - poročni (uvod + UX filtri po materialu).
   - Vse samo z dejstvi, ki jih potrdi naročnik.
5. Izdelki: imena (tipkarske napake), H1, title, alt (iz imena in oznak), primarne kategorije. Unikatni opisi šele s podatki naročnika.
6. Shema: `geo`, `image`, `sameAs` (Google), drobtine izdelkov, Product (po odločitvi).
7. Hitrost in UX po poglavju 15.
8. Oznake in preusmeritve po odločitvah MANUAL REVIEW.
9. Ponoven audit (isti skripti) in šele nato prehod (poglavje 17).
