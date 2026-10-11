# Mikroanimacije – standard

Vse animacije: samo `transform` in `opacity`, brez knjižnic (CSS + IntersectionObserver),
ob `prefers-reduced-motion: reduce` izklopljene (elementi takoj vidni).

| # | Kje | Animacija | Vrednosti |
|---|---|---|---|
| 1 | Bloki ob drsenju | vstop: opacity 0→1, translateY 16px→0 | 600 ms, `cubic-bezier(.2,.7,.2,1)`, prag 15 % vidnosti, enkrat |
| 2 | Skupine kartic | zaporedni vstop | zamik 80 ms med karticami, največ 6 |
| 3 | Hero fotografija | počasna povečava (Ken Burns) | scale 1.04→1, 1600 ms ob nalaganju |
| 4 | Hero besedilo | vstop po vrsticah | naslov 0 ms, podnaslov +120 ms, gumbi +240 ms |
| 5 | Kartice izdelkov (hover) | dvig + senca, izdelek rahlo večji | translateY −4px, slika scale 1.03, 250 ms ease-out |
| 6 | Gumbi | hover: temnejše ozadje; pritisk: scale .98 | 150 ms |
| 7 | Glava | ob drsenju navzdol se zmanjša in dobi ozadje | višina 88→64 px, 250 ms |
| 8 | Logotipi partnerjev | sivi → barvni ob hoverju | filter grayscale 1→0, 300 ms |
| 9 | Številke/dejstva | štetje od 0 ob prikazu (samo preverjene številke) | 1200 ms, ease-out |

Ne uporabljaj: samodejnih drsnikov (carousel), paralakse na mobilnem, animacij, ki trajajo > 1 s ali se ponavljajo.
