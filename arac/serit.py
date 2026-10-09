# -*- coding: utf-8 -*-
"""Birkaç ürün karesini tek şeride dizer — ortak yükseklik, eşit boşluk."""
import sys
from PIL import Image, ImageDraw, ImageFilter


def zemin_rengi(im):
    k = 8
    p = [im.crop((0, 0, im.width, k)), im.crop((0, im.height-k, im.width, im.height))]
    t = [0, 0, 0]
    for q in p:
        s = q.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
        t = [t[i] + s[i] for i in range(3)]
    return tuple(v // len(p) for v in t)


def serit(yollar, hedef, boy=520, bosluk=18, koyu=0.72):
    parca = []
    for y in yollar:
        im = Image.open(y).convert("RGB")
        o = boy / im.height
        parca.append(im.resize((max(1, int(im.width*o)), boy), Image.LANCZOS))
    gen = sum(p.width for p in parca) + bosluk * (len(parca) - 1)
    zem = tuple(int(v * koyu) for v in zemin_rengi(parca[0]))
    tuval = Image.new("RGB", (gen, boy), zem)
    x = 0
    for p in parca:
        tuval.paste(p, (x, 0))
        x += p.width + bosluk
    tuval.save(hedef, quality=95)
    return tuval


if __name__ == "__main__":
    hedef, boy = sys.argv[1], int(sys.argv[2])
    im = serit(sys.argv[3:], hedef, boy)
    print("%s  %d x %d" % (hedef, im.width, im.height))
