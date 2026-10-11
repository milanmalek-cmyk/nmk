# SEO in GEO naslovnice – GEOFOTO d.o.o.

**Izhodišče:**

- Cilj so povpraševanja zasebnikov (lokalna iskanja) ter investitorjev in javnih naročnikov.
- Podatkov iz Search Console ni. Ključne besede so predlog na podlagi namena iskanja (⚠️ predpostavka) in jih je
  smiselno preveriti v orodju za ključne besede.

## Prednostni ukrepi

| Prednost | Ukrep | Zakaj |
|---|---|---|
| **Visoko** | `lang="sl"`, en H1, opisni `<title>` in meta opis | zdaj `lang="en"`, title »GEOFOTO«, 3 neopisni H1, meta opis na nobeni strani |
| **Visoko** | lokalna vsebina: 3 poslovne enote z naslovi in JSON-LD za vsako | lokalna iskanja (»geodet Slovenska Bistrica«, »geodet Slovenske Konjice«) |
| **Visoko** | storitve z opisi in povezavami na podstrani | naslovnica ima 253 besed in samo ikone |
| **Srednje** | JSON-LD Organization + 3 × LocalBusiness + FAQPage | jasna entiteta za iskalnike in AI povzetke |
| **Srednje** | alt besedila, og:image, dovoljena povečava (viewport) | dostopnost in deljenje |
| **Srednje** | odstranitev neobstoječega videa, dokončanje strani Hidrografija | napake in nedokončane strani |

## Osnovno

| Element | Predlog | Dolžina |
|---|---|---|
| `<title>` | Geodetske storitve Slovenska Bistrica \| GEOFOTO | 47 znakov |
| meta description | Ureditev meje, parcelacija, evidentiranje stavb, zakoličbe, lasersko skeniranje in GIS. Geodetske storitve v Slovenski Bistrici in okolici. | 139 znakov |
| H1 | Geodetske storitve za lastnike nepremičnin in investitorje | |
| `lang` | `sl` | |
| og:image | `kontakt-cover.jpg` (1920×600) | |

## Ključne besede

| Ključna beseda | Namen | Kje |
|---|---|---|
| geodet Slovenska Bistrica, geodetske storitve Slovenska Bistrica | lokalni / transakcijski | title, H1 okolica, blok enot |
| geodet Slovenske Konjice, geodet Rogaška Slatina | lokalni | blok poslovnih enot, JSON-LD |
| ureditev meje, parcelacija, evidentiranje stavbe, hišna številka | transakcijski (zasebniki) | kartica »Za lastnike nepremičnin«, FAQ |
| zakoličba objekta, geodetski načrt, monitoring objektov | komercialni (investitorji) | kartica »Za investitorje« |
| lasersko skeniranje, aerofotogrametrija, snemanje z dronom, GIS | komercialni | blok »Sodobne metode« |

## Hierarhija naslovov

- H1 Geodetske storitve za lastnike nepremičnin in investitorje
  - H2 Kaj potrebujete? → H3 Za lastnike nepremičnin · Za investitorje in javne naročnike
  - H2 Sodobne metode zajema podatkov → H3 Lasersko skeniranje · Aerofotogrametrija · GIS in kartografija · Hidrografija
  - H2 Zaupajo nam
  - H2 Kako poteka geodetska storitev
  - H2 Blizu vas
  - H2 Pogosta vprašanja

## Interne povezave

| Besedilo | Cilj |
|---|---|
| Kaj potrebujem? (zasebniki) | `/storitve/zemljiski-kataster` |
| Vse storitve | `/storitve` |
| Lasersko skeniranje · Aerofotogrametrija · GIS · Kartografija · Hidrografija | ustrezne podstrani `/storitve/…` |
| Vse reference | `/reference` |
| Pošljite povpraševanje | `/kontakt` |

## Alt besedila

| Datoteka | alt |
|---|---|
| `kontakt-cover.jpg` | Geodet GEOFOTO z nivelirno lato pri meritvah na mostu |
| `IMG_20170304_154651.jpg` | Totalna postaja na travniku pri ureditvi meje parcele |
| `prizma.jpg` | Geodetska prizma na gradbišču |
| `slide-1.jpg` | Oblak točk stavbe, zajet z laserskim skenerjem |
| `slides-fin-5.jpg` | Dron za aerofotogrametrijo |
| `kartografija-banner.jpg` | 3D karta pokrajine |
| `hidro-banner.jpg` | 3D model dna vodotoka |
| `lata.jpg` | Nivelirna lata |

## GEO – povzetek podjetja

GEOFOTO d.o.o. je geodetsko podjetje s sedežem v Slovenski Bistrici in poslovnima enotama v Slovenskih Konjicah
in Rogaški Slatini, ki na trgu deluje več kot 30 let. Izvaja geodetske storitve za lastnike nepremičnin (ureditev
meje, parcelacija, evidentiranje stavb) in za investitorje ter javne naročnike (geodetski načrti, zakoličbe,
monitoring, lasersko skeniranje, aerofotogrametrija, GIS). Med naročniki so DARS, Direkcija RS za ceste, HESS in DEM.

FAQ je v `besedila.md`, blok 9. Na strani mora biti viden; `FAQPage` je predvsem za razumevanje vsebine in AI povzetke.

## JSON-LD

Leto ustanovitve je izpuščeno, ker je neusklajeno (❓).

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.geofoto.si/#organizacija",
      "name": "GEOFOTO d.o.o.",
      "url": "https://www.geofoto.si/",
      "logo": "https://www.geofoto.si/images/logo.png",
      "email": "info@geofoto.si",
      "telephone": "+386 2 840 13 40",
      "vatID": "SI85454435",
      "slogan": "Kadar mora biti zares natančno.",
      "address": {"@type": "PostalAddress", "streetAddress": "Mariborska cesta 5", "postalCode": "2310", "addressLocality": "Slovenska Bistrica", "addressCountry": "SI"},
      "knowsAbout": ["ureditev meje", "parcelacija", "evidentiranje stavb", "zakoličba objektov", "monitoring", "lasersko skeniranje", "aerofotogrametrija", "GIS", "kartografija"]
    },
    {
      "@type": "LocalBusiness",
      "@id": "https://www.geofoto.si/#slovenska-bistrica",
      "name": "GEOFOTO d.o.o. – Slovenska Bistrica",
      "parentOrganization": {"@id": "https://www.geofoto.si/#organizacija"},
      "telephone": "+386 2 840 13 40",
      "address": {"@type": "PostalAddress", "streetAddress": "Mariborska cesta 5", "postalCode": "2310", "addressLocality": "Slovenska Bistrica", "addressCountry": "SI"},
      "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Thursday"], "opens": "07:00", "closes": "15:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Wednesday", "opens": "07:00", "closes": "16:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "07:00", "closes": "14:00"}
      ]
    },
    {
      "@type": "LocalBusiness",
      "@id": "https://www.geofoto.si/#slovenske-konjice",
      "name": "GEOFOTO d.o.o. – PE Slovenske Konjice",
      "parentOrganization": {"@id": "https://www.geofoto.si/#organizacija"},
      "telephone": "+386 51 663 330",
      "address": {"@type": "PostalAddress", "streetAddress": "Mestni trg 6", "postalCode": "3210", "addressLocality": "Slovenske Konjice", "addressCountry": "SI"}
    },
    {
      "@type": "LocalBusiness",
      "@id": "https://www.geofoto.si/#rogaska-slatina",
      "name": "GEOFOTO d.o.o. – PE Rogaška Slatina",
      "parentOrganization": {"@id": "https://www.geofoto.si/#organizacija"},
      "address": {"@type": "PostalAddress", "streetAddress": "Gubčeva ulica 2", "postalCode": "3250", "addressLocality": "Rogaška Slatina", "addressCountry": "SI"}
    },
    {"@type": "WebSite", "@id": "https://www.geofoto.si/#spletnastran", "url": "https://www.geofoto.si/", "name": "GEOFOTO", "inLanguage": "sl-SI", "publisher": {"@id": "https://www.geofoto.si/#organizacija"}}
  ]
}
```
