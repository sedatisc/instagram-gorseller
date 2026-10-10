#!/usr/bin/env python3
"""Var olan bir gönderinin kapağından hikaye üretir.

Kullanım:  python3 hikaye_kapaktan.py <klasor> <kategori>
Spec JSON'u elde olmayan eski gönderiler için. Yeni gönderilerde
uret.py zaten hikaye.jpg üretiyor, bunu kullanma.
"""
import os
import sys
from PIL import Image, ImageDraw

import uret
from uret import (BG, ACC, MUTE, GUT, a, glow, over, bright_logo, mono, pop,
                  theme, LABEL)

SW, SH = 1080, 1920


def main():
    klasor, kategori = sys.argv[1], sys.argv[2]
    theme(kategori)
    acc, label = uret.ACC, uret.LABEL

    ilk = os.path.join(klasor, "1.jpg")
    if not os.path.exists(ilk):
        ilk = os.path.join(klasor, "1.png")
    kapak = Image.open(ilk).convert("RGBA")
    img = Image.new("RGBA", (SW, SH), BG + (255,))

    def bands(d):
        d.line([(-300, 900), (860, -360)], fill=a(acc, 0.85), width=170)
        d.line([(300, 2200), (1400, 900)], fill=a(acc, 0.55), width=150)
    img.alpha_composite(glow((SW, SH), bands, 90))
    img.alpha_composite(glow((SW, SH), lambda d: [
        d.line([(-300, 900), (860, -360)], fill=a(acc, 0.95), width=6),
        d.line([(300, 2200), (1400, 900)], fill=a(acc, 0.7), width=5)], 4))

    dots = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for y in range(0, SH, 54):
        for x in range(0, SW, 54):
            dd.ellipse([x - 1, y - 1, x + 1, y + 1], fill=a(acc, 0.10))
    img.alpha_composite(dots)

    kw = 940
    kh = int(kapak.height * kw / kapak.width)
    kapak = kapak.resize((kw, kh), Image.LANCZOS)
    yuvarlak = Image.new("L", (kw, kh), 0)
    ImageDraw.Draw(yuvarlak).rounded_rectangle([0, 0, kw - 1, kh - 1],
                                               radius=28, fill=255)
    kapak.putalpha(yuvarlak)
    kx, ky = (SW - kw) // 2, 330
    img.alpha_composite(glow((SW, SH), lambda g: g.rounded_rectangle(
        [kx + 14, ky + 20, kx + kw - 14, ky + kh + 14], radius=28,
        fill=a(acc, 0.32)), 44))
    img.alpha_composite(kapak, (kx, ky))

    d = ImageDraw.Draw(img)
    btn = "GÖNDERİYE BAK"
    fb = pop(32, "Bold")
    tw = d.textlength(btn, font=fb)
    by = ky + kh + 66
    img.alpha_composite(glow((SW, SH), lambda g: g.rounded_rectangle(
        [GUT, by, GUT + tw + 120, by + 80], radius=40, fill=a(acc, 0.55)), 30))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([GUT, by, GUT + tw + 120, by + 80], radius=40, fill=acc)
    d.text((GUT + 46, by + 40), btn, font=fb, fill=(6, 10, 20), anchor="lm")
    ax = GUT + 46 + tw + 28
    d.line([(ax, by + 40), (ax + 28, by + 40)], fill=(6, 10, 20), width=5)
    d.polygon([(ax + 25, by + 31), (ax + 44, by + 40), (ax + 25, by + 49)],
              fill=(6, 10, 20))
    d.text((GUT, by + 128), "profilde yeni gönderi", font=pop(28), fill=MUTE,
           anchor="lm")

    print(uret.yaz(img, os.path.join(klasor, "hikaye.jpg")))


if __name__ == "__main__":
    main()
