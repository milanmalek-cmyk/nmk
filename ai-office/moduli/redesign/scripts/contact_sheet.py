#!/usr/bin/env python3
"""Pregledni list kandidatov za izbor fotografij – samo za ogled, originali ostanejo nedotaknjeni.

Uporaba:
  python3 -I contact_sheet.py IZHOD.jpg SIRINA_CELICE VISINA_CELICE STOLPCI SLIKA [SLIKA ...]
"""
import os
import sys

from PIL import Image, ImageDraw


def main():
    if len(sys.argv) < 6:
        sys.exit(__doc__)
    izhod, cw, ch, stolpci = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    datoteke = sys.argv[5:]
    vrstic = (len(datoteke) + stolpci - 1) // stolpci
    list_ = Image.new("RGB", (stolpci * cw, vrstic * (ch + 18)), (200, 200, 200))
    d = ImageDraw.Draw(list_)
    for i, pot in enumerate(datoteke):
        with Image.open(pot) as im:
            im = im.convert("RGBA")
            im.thumbnail((cw - 6, ch - 6))
            ozadje = Image.new("RGB", im.size, (235, 235, 235))   # svetlo siva pokaže prosojnost
            ozadje.paste(im, mask=im.split()[-1])
        x, y = (i % stolpci) * cw, (i // stolpci) * (ch + 18)
        list_.paste(ozadje, (x + (cw - ozadje.width) // 2, y + 3))
        d.text((x + 4, y + ch + 2), f"{i + 1}. {os.path.basename(pot)[:40]}", fill=(0, 0, 0))
    list_.save(izhod, quality=85)
    print(f"{len(datoteke)} slik → {izhod}")


if __name__ == "__main__":
    main()
