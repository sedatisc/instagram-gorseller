# -*- coding: utf-8 -*-
"""Arka planı temizlenmiş ürünü stüdyo karesine oturtur.

Zemin degradesi, temas gölgesi ve yere yansıma. Çıktı gönderi
kapağının beklediği 1080 x 800 bant.
"""
import sys
from PIL import Image, ImageDraw, ImageFilter


def kirp(im):
    bb = im.getbbox()
    return im.crop(bb) if bb else im


def degrade(w, h, ust, alt):
    g = Image.new("RGB", (1, h))
    d = ImageDraw.Draw(g)
    for y in range(h):
        t = (y / max(1, h - 1)) ** 0.85
        d.point((0, y), tuple(int(ust[i] + (alt[i] - ust[i]) * t) for i in range(3)))
    return g.resize((w, h), Image.BILINEAR)


def isik(w, h, merkez, renk, yaric, guc=0.5):
    lay = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(lay)
    cx, cy = merkez
    d.ellipse([cx - yaric, cy - yaric * 0.62, cx + yaric, cy + yaric * 0.62],
              fill=int(255 * guc))
    lay = lay.filter(ImageFilter.GaussianBlur(yaric * 0.55))
    renkli = Image.new("RGB", (w, h), renk)
    return renkli, lay


def studyo(kaynaklar, hedef, w=1080, h=800, ust=(38, 42, 52), alt=(12, 14, 20),
           vurgu=(120, 150, 190), doluluk=0.70, bosluk=0.05):
    kares = [kirp(Image.open(k).convert("RGBA")) for k in kaynaklar]

    tuval = degrade(w, h, ust, alt).convert("RGBA")
    r, m = isik(w, h, (w * 0.5, h * 0.30), vurgu, w * 0.42, 0.30)
    tuval = Image.composite(Image.alpha_composite(
        tuval, r.convert("RGBA")), tuval, m)

    n = len(kares)
    bos = int(w * bosluk)
    kullan = w - bos * (n + 1)
    alan_h = h * doluluk
    taban = int(h * 0.80)
    # boyları eşitle, genişliği orana göre paylaştır
    oranlar = [k.width / k.height for k in kares]
    boy = min(alan_h, kullan / sum(oranlar))

    golge = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(golge)
    yerlesim = []
    x_imdi = bos + (kullan - boy * sum(oranlar)) / 2
    for i, k in enumerate(kares):
        o = boy / k.height
        yeni = k.resize((max(1, int(k.width * o)), max(1, int(boy))),
                        Image.LANCZOS)
        x = int(x_imdi)
        cx = x + yeni.width // 2
        x_imdi += yeni.width + bos
        y = taban - yeni.height
        yerlesim.append((yeni, x, y))
        gw = int(yeni.width * 0.86)
        gd.ellipse([cx - gw // 2, taban - 16, cx + gw // 2, taban + 26],
                   fill=(0, 0, 0, 150))
    tuval.alpha_composite(golge.filter(ImageFilter.GaussianBlur(22)))

    for yeni, x, y in yerlesim:
        # yere yansıma
        yan = yeni.transpose(Image.FLIP_TOP_BOTTOM)
        yh = int(yeni.height * 0.34)
        yan = yan.crop((0, 0, yan.width, yh))
        maske = Image.new("L", (yan.width, yh), 0)
        md = ImageDraw.Draw(maske)
        for j in range(yh):
            md.line([(0, j), (yan.width, j)],
                    fill=int(96 * (1 - j / yh) ** 1.8))
        yan.putalpha(Image.composite(
            yan.getchannel("A").point(lambda v: v), maske,
            maske.point(lambda v: 255 - v)) if False else
            maske.point(lambda v: v))
        a = yan.getchannel("A")
        yan.putalpha(a)
        tuval.alpha_composite(yan, (x, taban + 2))
        tuval.alpha_composite(yeni, (x, y))

    tuval.convert("RGB").save(hedef, quality=95)
    return tuval


if __name__ == "__main__":
    hedef = sys.argv[1]
    ust = tuple(int(sys.argv[2][i:i+2], 16) for i in (0, 2, 4))
    alt = tuple(int(sys.argv[3][i:i+2], 16) for i in (0, 2, 4))
    vur = tuple(int(sys.argv[4][i:i+2], 16) for i in (0, 2, 4))
    im = studyo(sys.argv[5:], hedef, ust=ust, alt=alt, vurgu=vur)
    print("%s  %dx%d  (%d ürün)" % (hedef, im.width, im.height, len(sys.argv)-5))
