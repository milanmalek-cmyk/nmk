# SEO in GEO naslovnice – BIO-SAD d.o.o.

**Izhodišče:**

- Cilj so B2B povpraševanja za polnitve in prepoznavnost lastnih znamk.
- Ciljne skupine so nabavniki, trgovci in potrošniki v Sloveniji, nato DE/EN.
- Podatkov o obsegu iskanja in Search Console ni. Ključne besede so zato predlog na podlagi namena
  iskanja (⚠️ predpostavka) in jih je smiselno preveriti v orodju za ključne besede.

## Prednostni ukrepi

| Prednost | Ukrep | Zakaj |
|---|---|---|
| **Kritično** | odzivna naslovnica (odstranitev `viewport width=1200`) | stran na mobilnem ni uporabna; Google indeksira mobilno različico |
| **Visoko** | en H1, opisni `<title>` in meta description | zdaj 10 × H1, title »Domov«, brez opisa – iskalnik ne razume, kaj je glavna tema |
| **Visoko** | JSON-LD Organization + Store + WebSite (+ FAQPage za vidna vprašanja) | jasna entiteta za iskalnike in AI povzetke (GEO) |
| **Srednje** | alt besedila slik, og:image | 37/40 slik brez alt; deljenje brez slike |
| **Srednje** | robots.txt in sitemap.xml (cela stran, izven naslovnice) | oba vrneta 404 – naloga za tehnično izvedbo |

## Osnovno

| Element | Predlog | Dolžina |
|---|---|---|
| `<title>` | BIO-SAD \| Proizvajalec pijač in polnitve pod vašo znamko | 56 znakov |
| meta description | Žgane pijače, likerji, pijače na osnovi vina in sadni sirupi iz Lenarta v Slovenskih goricah. Polnitve pod vašo blagovno znamko. IFS Food in ISO 9001. | 150 znakov |
| H1 (en sam) | Proizvajalec pijač iz Slovenskih goric | |
| og:image | `slider6.jpg` ali `vsi-izdelki2.jpg` (1621×540) | |

## Ključne besede

| Ključna beseda | Namen iskanja | Kje na naslovnici |
|---|---|---|
| proizvajalec pijač | komercialni (B2B) | title, H1 |
| polnitve pijač, polnjenje pijač pod blagovno znamko, private label pijače | komercialni / transakcijski (B2B) | H2 Polnitve, FAQ, zaključni poziv |
| proizvodnja likerjev, proizvajalec žganih pijač | komercialni | kartice programa, FAQ |
| sadni sirupi | komercialni / transakcijski (potrošniki, gostinstvo) | kartica Sadni sirupi |
| Mister Gin, Miss Gin, The Borovnička, Domači rum Apis, Cremoso | navigacijski (blagovne znamke) | H3 v Nagrajeni okusi |
| BIO-SAD Lenart, industrijska prodajalna Lenart | navigacijski / lokalni | FAQ, noga, JSON-LD |

Brez ponavljanja iste fraze v vsakem naslovu – raven ključnih besed ostane naravna.

## Hierarhija naslovov

- H1 Proizvajalec pijač iz Slovenskih goric
  - H2 Naš program pijač → H3 Žgane pijače · Likerji · Pijače na osnovi vina · Sadni sirupi
  - H2 Nagrajeni okusi → H3 Mister & Miss Gin · The Borovnička · Domači rum Apis · Cremoso
  - H2 Polnitve pod vašo blagovno znamko
  - H2 Tradicija, znanje in sodobna proizvodnja
  - H2 Zaupajo nam
  - H2 Pogosta vprašanja → vprašanja kot H3
  - H2 Iščete partnerja za polnitev pijač?

Številke v pasu dokazov niso naslovi (ni H-oznak), nadnaslovi so `<p>`.

## Interne povezave

| Besedilo povezave | Cilj |
|---|---|
| Žgane pijače · Likerji · Pijače na osnovi vina · Sadni sirupi | `/sl/produkti?cat=…` (4 kategorije) |
| Vsi izdelki | `/sl/produkti` |
| Pošljite povpraševanje za polnitev | `/sl/polnitve` + obrazec za povpraševanje |
| Več o podjetju · Standardi kakovosti | `/sl/o-podjetju` · `/sl/standardi` |
| 11 medalj (pas dokazov) | `/sl/priznanja` |

## Alt besedila slik

| Datoteka | alt |
|---|---|
| `logotip.png` | BIO-SAD |
| `slider6.jpg` | Gričevje Slovenskih goric s cerkvico na hribu |
| `slider5.jpg` | Vinogradi v Slovenskih goricah ob sončnem zahodu ⚠️ (lokacija fotografije ni potrjena) |
| `slider8.jpg` | Polnilna linija za steklenice v proizvodnji BIO-SAD |
| `slider9.jpg` | Etiketiranje steklenic zeliščnega likerja Fazan |
| `slider10.jpg` | Proizvodna dvorana BIO-SAD v Lenartu |
| `zgane-nova.png` | Žgane pijače BIO-SAD in Apis |
| `likerji-2022.png` | Sadni in zeliščni likerji BIO-SAD |
| `bishee-jagoda.png` | Bishé – pijača na osnovi vina z okusom jagode |
| `sokovi-nova.png` | Sadni sirupi BIO-SAD |
| `mr-miss.png` | Mister Gin in Miss Gin |
| `borovnicka.png` | The Borovnička – borovničev liker |
| `domaci-rumo-apis.png` | Domači rum Apis |
| `cremoso3-1.png` | Cremoso – kremne pijače z okusom kave, kokosa in lešnika |
| `polnitve-home-2022-1.png` | Pijače, polnjene za blagovne znamke kupcev |

## GEO – vidnost v AI iskalnikih

Jedrnata, preverljiva dejstva v besedilu strani (ne samo v slikah), dosledni podatki o imenu, naslovu in
telefonu (NAP), vidna vprašanja in odgovori ter strukturirani podatki, ki ponavljajo isto.

### Povzetek podjetja (za blok O podjetju in opis entitete)

BIO-SAD d.o.o. je slovenski proizvajalec žganih pijač, likerjev, pijač na osnovi vina in sadnih sirupov s
sedežem in proizvodnjo v Lenartu v Slovenskih goricah, na trgu od leta 1994. Proizvaja pod blagovnima znamkama
Bio-Sad in Apis ter polni pijače pod blagovnimi znamkami trgovskih verig in podjetij, med drugim za Hofer, Lidl,
Mercator, Spar, Eurospin, Jager in Tuš. Ima certifikata IFS Food (višja raven) in ISO 9001:2015.

### FAQ

Vprašanja in odgovori so v `besedila.md`, blok 9. Na strani morajo biti vidni, da je `FAQPage` upravičen.
Google od leta 2023 prikazuje FAQ izseke samo še za izbrane spletne strani, zato je vrednost predvsem v
razumevanju vsebine in v AI povzetkih, ne v izseku v rezultatih.

## Strukturirani podatki (JSON-LD)

`foundingDate` je namerno izpuščen: register navaja 1990, podjetje 1994 (❓). `sameAs` (družbena omrežja) dodamo
po potrditvi aktivnih profilov.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.bio-sad.si/#organizacija",
      "name": "BIO-SAD d.o.o.",
      "legalName": "BIO-SAD družba za proizvodnjo, trgovino in storitve d.o.o.",
      "url": "https://www.bio-sad.si/",
      "logo": "https://www.bio-sad.si/templates/wt_app_free/images/logotip.png",
      "slogan": "Pijače za vaš okus",
      "description": "Slovenski proizvajalec žganih pijač, likerjev, pijač na osnovi vina in sadnih sirupov ter polnitve pod blagovno znamko kupca.",
      "email": "info@bio-sad.si",
      "telephone": "+386 59 739 564",
      "vatID": "SI87898764",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Industrijska ulica 1",
        "postalCode": "2230",
        "addressLocality": "Lenart v Slovenskih goricah",
        "addressCountry": "SI"
      },
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "sales",
        "telephone": "+386 59 739 564",
        "email": "info@bio-sad.si",
        "availableLanguage": ["sl", "de", "en"]
      },
      "brand": [
        { "@type": "Brand", "name": "Bio-Sad" },
        { "@type": "Brand", "name": "Apis" }
      ],
      "award": [
        "Zlata medalja za Višnjevec, Novi Sad 2021",
        "Zlata medalja za Mister Gin, Novi Sad 2019",
        "Zlata medalja za Sadjevec, Novi Sad 2018",
        "Zlata medalja za Vodko Apis, Novi Sad 2017"
      ],
      "knowsAbout": ["polnitve pijač pod blagovno znamko kupca", "likerji", "žgane pijače", "sadni sirupi"]
    },
    {
      "@type": "Store",
      "@id": "https://www.bio-sad.si/#prodajalna",
      "name": "Industrijska prodajalna BIO-SAD",
      "parentOrganization": { "@id": "https://www.bio-sad.si/#organizacija" },
      "telephone": "+386 59 739 564",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Industrijska ulica 1",
        "postalCode": "2230",
        "addressLocality": "Lenart v Slovenskih goricah",
        "addressCountry": "SI"
      },
      "openingHoursSpecification": [
        { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "10:00" },
        { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "12:30", "closes": "14:30" }
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.bio-sad.si/#spletnastran",
      "url": "https://www.bio-sad.si/",
      "name": "BIO-SAD",
      "inLanguage": "sl-SI",
      "publisher": { "@id": "https://www.bio-sad.si/#organizacija" }
    }
  ]
}
```

`FAQPage` z istimi 5 vprašanji in odgovori se doda ob gradnji (F6) iz končnega besedila bloka 9.
