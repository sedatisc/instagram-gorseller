# -*- coding: utf-8 -*-
"""Ürün fotoğrafını kapak/bant kadrajına hazırla.

Konuyu zeminden ayırıp hedef tuvale istenen dikey konuma yerleştiriyor,
boş kalan yeri fotoğrafın kendi zemin renginden türeyen degradeyle dolduruyor.
"""
import sys
from PIL import Image, ImageChops, ImageFilter


def zemin_rengi(im):
    """Kenar şeridinin baskın rengi."""
    k = 6
    kenar = [im.crop((0, 0, im.width, k)), im.crop((0, im.height - k, im.width, im.height)),
             im.crop((0, 0, k, im.height)), im.crop((im.width - k, 0, im.width, im.height))]
    t = [0, 0, 0]
    n = 0
    for p in kenar:
        s = p.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
        t = [t[i] + s[i] for i in range(3)]
        n += 1
    return tuple(v // n for v in t)


def konu_kutusu(im, zem, esik=26):
    """Zeminden farklı piksellerin sınır kutusu."""
    fark = ImageChops.difference(im, Image.new("RGB", im.size, zem)).convert("L")
    fark = fark.filter(ImageFilter.GaussianBlur(3)).point(lambda v: 255 if v > esik else 0)
    return fark.getbbox()


def hazirla(kaynak, hedef, tw, th, ust_pay=0.10, alt_pay=0.30, kirp=True, hiza=None):
    im = Image.open(kaynak).convert("RGB")
    zem = zemin_rengi(im)
    kutu = konu_kutusu(im, zem) if kirp else (0, 0, im.width, im.height)
    if not kutu:
        kutu = (0, 0, im.width, im.height)
    # konuyu biraz nefesle kes
    pay = int(min(im.width, im.height) * 0.02)
    kutu = (max(0, kutu[0] - pay), max(0, kutu[1] - pay),
            min(im.width, kutu[2] + pay), min(im.height, kutu[3] + pay))
    konu = im.crop(kutu)

    # konunun kaplayacağı alan
    alan_w = tw * 0.94
    alan_h = th * (1.0 - ust_pay - alt_pay)
    o = min(alan_w / konu.width, alan_h / konu.height)
    konu = konu.resize((max(1, int(konu.width * o)), max(1, int(konu.height * o))),
                       Image.LANCZOS)

    tuval = Image.new("RGB", (tw, th), zem)
    x = (tw - konu.width) // 2
    if hiza is None:
        y = int(th * ust_pay) + int((alan_h - konu.height) / 2)
    else:                       # konunun altını th*hiza hizasına otur
        y = int(th * hiza) - konu.height
    tuval.paste(konu, (x, max(0, y)))
    return tuval, zem


if __name__ == "__main__":
    kaynak, hedef, tw, th, ust, alt = sys.argv[1:7]
    hiza = float(sys.argv[7]) if len(sys.argv) > 7 else None
    img, zem = hazirla(kaynak, hedef, int(tw), int(th), float(ust), float(alt),
                       hiza=hiza)
    img.save(hedef, quality=95)
    print("%s  %dx%d  zemin %s" % (hedef, img.width, img.height, zem))
