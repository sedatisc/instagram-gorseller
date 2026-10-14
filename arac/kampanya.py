#!/usr/bin/env python3
"""Kampanya afişi — üç panelli, kalın başlıklı duyuru karesi.

Piyasadaki bayi afişlerinin düzeni: üstte bağıran bir başlık, ortada üç
renkli kategori paneli, altta büyük teklif şeridi, en altta güven şeridi.
Burada o düzen bizim yazı ve renk sistemimizle kuruluyor; ürün
fotoğrafları gerçek ürün sayfalarından geliyor, çizilmiyor.

    python3 arac/kampanya.py <spec.json> <cikti.jpg> [<hikaye.jpg>]
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
import uret as U                                         # noqa: E402
from urun_karti import (BUY, KESIK, RENK, f_bold, f_mono,  # noqa: E402,F401
                        f_reg, kesik_ac, sar, sigdir, yuvarlak)

W, H = 1080, 1350
SW, SH = 1080, 1920
KEN = 30

LACI = (14, 20, 36)
KAGIT = (243, 246, 250)
MUREKKEP = (16, 22, 38)
SOLUK = (104, 116, 139)


def _kutu_rengi(renk, koyuluk=0.86):
    return tuple(int(c * koyuluk) for c in renk)


def panel(img, kutu, p, sira):
    """Tek kategori paneli: renkli başlık, ürün fotoğrafı, üç madde."""
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = [int(v) for v in kutu]
    renk = RENK.get(p.get("renk", "mavi"), RENK["mavi"])
    yuvarlak(d, [x0, y0, x1, y1], 18, dolgu=(255, 255, 255),
             kenar=renk, kalin=3)

    # başlık şeridi
    bh = 86
    yuvarlak(d, [x0 + 3, y0 + 3, x1 - 3, y0 + bh], 15, dolgu=renk)
    d.rectangle([x0 + 3, y0 + bh - 16, x1 - 3, y0 + bh], fill=renk)
    ic = x1 - x0 - 28
    fb, sat = None, None
    for boy in range(31, 17, -1):
        f = U.pop(boy, "SemiBold")
        s = sar(d, BUY(p["ad"]), f, ic)
        if len(s) <= 2:
            fb, sat = f, s
            break
    if fb is None:
        fb, sat = U.pop(18, "SemiBold"), [BUY(p["ad"])[:22]]
    oy = y0 + bh / 2 - (len(sat) - 1) * (fb.size * 0.58)
    for i, ln in enumerate(sat):
        d.text(((x0 + x1) / 2, oy + i * fb.size * 1.16), ln, font=fb,
               fill=(255, 255, 255), anchor="mm")

    # fotoğraf
    fy0, fy1 = y0 + bh + 12, y1 - 150
    kes = None
    yol = p.get("gorsel")
    if yol:
        tam = os.path.join(KOK, "gorsel", yol)
        if os.path.exists(tam):
            kes = kesik_ac(tam)
    if kes is not None:
        kw, kh = x1 - x0 - 34, fy1 - fy0
        o = min(kw / float(kes.width), kh / float(kes.height))
        u = kes.resize((max(1, int(kes.width * o)),
                        max(1, int(kes.height * o))), Image.LANCZOS)
        golge = Image.new("RGBA", img.size, (0, 0, 0, 0))
        gx, gy = (x0 + x1) // 2, fy1 - 10
        ImageDraw.Draw(golge).ellipse(
            [gx - u.width * 0.32, gy - 12, gx + u.width * 0.32, gy + 12],
            fill=(18, 24, 40, 60))
        img.alpha_composite(golge.filter(ImageFilter.GaussianBlur(10)))
        img.alpha_composite(u, ((x0 + x1) // 2 - u.width // 2,
                                fy1 - u.height))
    d = ImageDraw.Draw(img)

    # üç madde
    y = y1 - 136
    fm = f_reg(20)
    for m in p.get("maddeler", [])[:3]:
        d.ellipse([x0 + 18, y + 6, x0 + 30, y + 18], fill=renk)
        for ln in sar(d, U.P(m), fm, ic - 30)[:2]:
            d.text((x0 + 40, y), ln, font=fm, fill=MUREKKEP, anchor="la")
            y += 26
        y += 8


def afis(spec, cikti):
    img = Image.new("RGBA", (W, H), KAGIT + (255,))
    d = ImageDraw.Draw(img)
    vurgu = RENK.get(spec.get("renk", "turuncu"), RENK["turuncu"])

    # üst şerit
    d.rectangle([0, 0, W, 96], fill=LACI)
    logo = U.bright_logo(34)
    img.alpha_composite(logo, (KEN, 32))
    d = ImageDraw.Draw(img)
    d.text((W - KEN, 48), spec.get("ust", "sermenkreatif.com"),
           font=f_mono(24), fill=(168, 182, 208), anchor="rm")

    # başlık
    y = 124
    ic = W - 2 * KEN
    satirlar = [s for s in spec["baslik"] if s][:2]
    for i, s in enumerate(satirlar):
        f = sigdir(d, BUY(s), U.anton, ic, 108, 48)
        renk = (MUREKKEP if i == 0 else vurgu)
        d.text((W / 2, y + f.size * 0.56), BUY(s), font=f, fill=renk,
               anchor="mm")
        y += f.size * 1.02
    if spec.get("alt"):
        fa = f_reg(26)
        for ln in sar(d, U.P(spec["alt"]), fa, ic - 80)[:2]:
            d.text((W / 2, y + 20), ln, font=fa, fill=SOLUK, anchor="mm")
            y += 34
    y += 24

    # paneller
    pn = spec.get("paneller", [])[:3]
    n = max(1, len(pn))
    bos = 14
    pw = (W - 2 * KEN - (n - 1) * bos) / n
    # Şeritler alttan hizalanıyor; sabit konumda altta boşluk kalıyordu.
    gy = H - 150
    ty = gy - 132
    ph = 520
    py = max(y, ty - 18 - ph)
    for i, p in enumerate(pn):
        x = KEN + i * (pw + bos)
        panel(img, [x, py, x + pw, py + ph], p, i)
    d = ImageDraw.Draw(img)

    # teklif şeridi
    yuvarlak(d, [KEN, ty, W - KEN, ty + 112], 18, dolgu=vurgu)
    tek = spec.get("teklif", "")
    if tek:
        ft = sigdir(d, BUY(tek), U.anton, ic - 60, 64, 28)
        d.text((W / 2, ty + 56), BUY(tek), font=ft,
               fill=(255, 255, 255), anchor="mm")

    # güven şeridi
    guv = spec.get("guven", [])[:4]
    if guv:
        d.rectangle([0, gy, W, gy + 72], fill=LACI)
        gw = W / max(1, len(guv))
        for i, g in enumerate(guv):
            cx = gw * (i + 0.5)
            fg = sigdir(d, BUY(g), f_mono, gw - 24, 19, 12)
            d.text((cx, gy + 36), BUY(g), font=fg, fill=(214, 221, 232),
                   anchor="mm")

    d.text((KEN, H - 32), "@sermenkreatif", font=f_mono(22),
           fill=MUREKKEP, anchor="lm")
    d.text((W - KEN, H - 32), "sermenkreatif.com", font=f_mono(22),
           fill=SOLUK, anchor="rm")
    img.convert("RGB").save(cikti, "JPEG", quality=93, subsampling=0,
                            optimize=True)
    print("%s  %dx%d" % (cikti, W, H))


def hikaye(gonderi, cikti):
    kare = Image.open(gonderi).convert("RGB")
    img = Image.new("RGB", (SW, SH), LACI)
    o = (SW - 48) / float(kare.width)
    k = kare.resize((int(kare.width * o), int(kare.height * o)),
                    Image.LANCZOS)
    img.paste(k, (24, int((SH - k.height) / 2)))
    d = ImageDraw.Draw(img)
    d.text((SW / 2, SH - 110), "sermenkreatif.com", font=f_mono(28),
           fill=(168, 182, 208), anchor="mm")
    img.save(cikti, "JPEG", quality=92, subsampling=0, optimize=True)
    print("%s  %dx%d" % (cikti, SW, SH))


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    U.theme(spec.get("kategori", "3dbaski"))
    afis(spec, sys.argv[2])
    if len(sys.argv) > 3:
        hikaye(sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
