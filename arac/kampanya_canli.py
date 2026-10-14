#!/usr/bin/env python3
"""Kampanya afişi — bayi afişi tonunda, yüksek sesli sürüm.

Referans aldığımız bayi afişlerinin işi yapan tarafı şu: konturlu ve
gölgeli sarı başlık, başlığı taşıyan eğik kırmızı kurdele, beyaz gövdeli
renkli kategori panelleri, panellerin altında üç simgeli fayda şeridi ve
en altta rakamı devasa basılmış teklif bandı. Burada hepsi var; yazı
koddan basılıyor, ürün fotoğrafı gerçek ürün sayfasından geliyor.

    python3 arac/kampanya_canli.py <spec.json> <cikti.jpg> [<hikaye.jpg>]
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
sys.path.insert(0, os.path.join(KOK, "arac"))
import uret as U                                          # noqa: E402
from urun_karti import (BUY, RENK, f_bold, f_mono, f_reg,  # noqa: E402
                        kesik_ac, sar, sigdir, yuvarlak)

W, H = 1080, 1350
SW, SH = 1080, 1920
KEN = 24

LACI = (12, 17, 32)
BEYAZ = (255, 255, 255)
MUREKKEP = (16, 22, 38)
SOLUK = (104, 116, 139)
SARI = (255, 211, 46)
KIRMIZI = (214, 38, 42)


# ------------------------------------------------------------------ yardım
def konturlu(d, xy, metin, font, dolgu, kontur=(22, 14, 10), kalin=6,
             anchor="mm", golge=(0, 0, 0, 120), kaydir=(4, 6)):
    """Konturlu ve gölgeli yazı — afişin sesini veren şey bu."""
    if golge:
        d.text((xy[0] + kaydir[0], xy[1] + kaydir[1]), metin, font=font,
               fill=golge[:3], anchor=anchor, stroke_width=kalin,
               stroke_fill=golge[:3])
    d.text(xy, metin, font=font, fill=dolgu, anchor=anchor,
           stroke_width=kalin, stroke_fill=kontur)


def kurdele(img, kutu, renk, egim=-2.2, r=18):
    """Eğik kurdele bandı — başlığın altına giriyor."""
    x0, y0, x1, y1 = [int(v) for v in kutu]
    pad = 90
    kat = Image.new("RGBA", (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad),
                    (0, 0, 0, 0))
    k = ImageDraw.Draw(kat)
    k.rounded_rectangle([pad, pad, pad + (x1 - x0), pad + (y1 - y0)],
                        radius=r, fill=renk + (255,))
    kat = kat.rotate(egim, resample=Image.BICUBIC, center=(kat.width / 2,
                                                           kat.height / 2))
    img.alpha_composite(kat, (x0 - pad, y0 - pad))


def isin(img, merkez, yaricap, renk, kol=14, op=58):
    """Başlığın arkasındaki ışın patlaması."""
    kat = Image.new("RGBA", img.size, (0, 0, 0, 0))
    k = ImageDraw.Draw(kat)
    cx, cy = merkez
    for i in range(kol):
        a0 = 2 * math.pi * i / kol
        a1 = a0 + math.pi / kol * 0.74
        k.polygon([(cx, cy),
                   (cx + yaricap * math.cos(a0), cy + yaricap * math.sin(a0)),
                   (cx + yaricap * math.cos(a1), cy + yaricap * math.sin(a1))],
                  fill=renk + (op,))
    img.alpha_composite(kat.filter(ImageFilter.GaussianBlur(3)))


def _zemin(img, renk):
    """Köşelere doğru koyulaşan renkli zemin."""
    k = Image.new("RGB", (W, H), renk)
    d = ImageDraw.Draw(k)
    for i in range(0, H, 3):
        o = abs(i - H * 0.32) / float(H)
        c = tuple(int(v * (1 - min(0.55, o * 0.9))) for v in renk)
        d.rectangle([0, i, W, i + 3], fill=c)
    img.paste(k.convert("RGBA"), (0, 0))


def simge(d, kutu, tur, renk):
    """Fayda şeridindeki minik simge — kalkan, ev, dişli, etiket."""
    x0, y0, x1, y1 = kutu
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = (x1 - x0) / 2
    d.ellipse([x0, y0, x1, y1], fill=renk)
    b = BEYAZ
    if tur == "kalkan":
        d.polygon([(cx, cy - r * 0.55), (cx + r * 0.42, cy - r * 0.3),
                   (cx + r * 0.42, cy + r * 0.12), (cx, cy + r * 0.58),
                   (cx - r * 0.42, cy + r * 0.12),
                   (cx - r * 0.42, cy - r * 0.3)], fill=b)
    elif tur == "ev":
        d.polygon([(cx, cy - r * 0.55), (cx + r * 0.5, cy - r * 0.05),
                   (cx - r * 0.5, cy - r * 0.05)], fill=b)
        d.rectangle([cx - r * 0.33, cy - r * 0.05, cx + r * 0.33,
                     cy + r * 0.5], fill=b)
    elif tur == "disli":
        d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5],
                  fill=b)
        d.ellipse([cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2],
                  fill=renk)
        for i in range(8):
            a = 2 * math.pi * i / 8
            d.ellipse([cx + r * 0.58 * math.cos(a) - r * 0.11,
                       cy + r * 0.58 * math.sin(a) - r * 0.11,
                       cx + r * 0.58 * math.cos(a) + r * 0.11,
                       cy + r * 0.58 * math.sin(a) + r * 0.11], fill=b)
    else:                                   # yıldız
        n = []
        for i in range(10):
            a = -math.pi / 2 + math.pi * i / 5
            rr = r * (0.58 if i % 2 == 0 else 0.26)
            n.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(n, fill=b)


# ------------------------------------------------------------------ panel
def panel(img, kutu, p):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = [int(v) for v in kutu]
    renk = RENK.get(p.get("renk", "mavi"), RENK["mavi"])
    koyu = tuple(int(c * 0.72) for c in renk)

    yuvarlak(d, [x0, y0, x1, y1], 20, dolgu=koyu)
    yuvarlak(d, [x0 + 5, y0 + 5, x1 - 5, y1 - 5], 16, dolgu=renk)

    # başlık
    bh = 74
    ic = x1 - x0 - 26
    fb = sigdir(d, BUY(p["ad"]), U.anton, ic, 40, 20)
    konturlu(d, ((x0 + x1) / 2, y0 + bh / 2 + 2), BUY(p["ad"]), fb, BEYAZ,
             kontur=koyu, kalin=4, kaydir=(2, 3), golge=(0, 0, 0, 90))

    # beyaz gövde
    gy0, gy1 = y0 + bh, y1 - 92
    yuvarlak(d, [x0 + 12, gy0, x1 - 12, gy1], 14, dolgu=BEYAZ)

    # fotoğraf
    yol = p.get("gorsel")
    kes = None
    if yol:
        tam = os.path.join(KOK, "gorsel", yol)
        if os.path.exists(tam):
            kes = kesik_ac(tam)
    fy0, fy1 = gy0 + 14, gy1 - 14
    if kes is not None:
        kw, kh = x1 - x0 - 52, fy1 - fy0
        o = min(kw / float(kes.width), kh / float(kes.height))
        u = kes.resize((max(1, int(kes.width * o)),
                        max(1, int(kes.height * o))), Image.LANCZOS)
        # Ürün beyaz gövdenin ortasına; alta yapıştırınca üstte avuç
        # içi kadar boşluk kalıyordu.
        uy = fy0 + max(0, (fy1 - fy0 - u.height) // 2)
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        gx, gy = (x0 + x1) // 2, uy + u.height
        ImageDraw.Draw(g).ellipse([gx - u.width * 0.3, gy - 9,
                                   gx + u.width * 0.3, gy + 9],
                                  fill=(18, 24, 40, 70))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(9)))
        img.alpha_composite(u, ((x0 + x1) // 2 - u.width // 2, uy))
        d = ImageDraw.Draw(img)

    # fayda şeridi — üç simge, altında iki satırlık etiket
    fa = p.get("faydalar", [])[:3]
    if fa:
        gen = (x1 - x0) / max(1, len(fa))
        sy = y1 - 82
        ff = f_mono(13)
        for i, (tur, yazi) in enumerate(fa):
            cx = x0 + gen * (i + 0.5)
            simge(d, [cx - 15, sy, cx + 15, sy + 30], tur, BEYAZ)
            d.ellipse([cx - 15, sy, cx + 15, sy + 30], fill=BEYAZ)
            simge(d, [cx - 15, sy, cx + 15, sy + 30], tur, koyu)
            yy = sy + 38
            for ln in sar(d, BUY(yazi), ff, gen - 10)[:2]:
                d.text((cx, yy), ln, font=ff, fill=BEYAZ, anchor="ma")
                yy += 17


# ------------------------------------------------------------------ afiş
def afis(spec, cikti):
    img = Image.new("RGBA", (W, H), LACI + (255,))
    zemin = RENK.get(spec.get("zemin", "mavi"), RENK["mavi"])
    _zemin(img, tuple(int(c * 0.42) for c in zemin))
    vurgu = RENK.get(spec.get("renk", "kirmizi"), RENK["kirmizi"])

    # üst şerit
    d = ImageDraw.Draw(img)
    logo = U.bright_logo(32)
    img.alpha_composite(logo, (KEN + 6, 26))
    d = ImageDraw.Draw(img)
    d.text((W - KEN - 6, 42), BUY(spec.get("ust", "sermenkreatif.com")),
           font=f_mono(21), fill=(235, 240, 250), anchor="rm")

    # başlık
    sat = [s for s in spec["baslik"] if s][:3]
    isin(img, (W / 2, 250), 620, SARI, kol=16, op=34)
    d = ImageDraw.Draw(img)
    y = 112
    for i, s in enumerate(sat):
        son = (i == len(sat) - 1)
        f = sigdir(d, BUY(s), U.anton, W - 2 * KEN - 80,
                   112 if son else 78, 34)
        if son:
            # Kurdele bir öncekinin kuyruğunu örtmesin diye aşağıdan
            # başlıyor; eğim yüzünden köşesi 10 piksel yukarı çıkıyor.
            kurdele(img, [KEN + 10, y + 10, W - KEN - 10, y + f.size + 24],
                    KIRMIZI if vurgu != RENK["kirmizi"] else vurgu)
            d = ImageDraw.Draw(img)
        konturlu(d, (W / 2, y + f.size * 0.62), BUY(s), f, SARI,
                 kontur=(26, 16, 12), kalin=7 if son else 5)
        y += f.size * (1.18 if son else 1.06) + (20 if son else 16)

    if spec.get("alt"):
        fa = f_bold(25)
        for ln in sar(d, U.P(spec["alt"]), fa, W - 2 * KEN - 120)[:2]:
            d.text((W / 2, y + 18), ln, font=fa, fill=(236, 242, 252),
                   anchor="mm")
            y += 34
    y += 18

    # paneller — alttan hizalı
    gy = H - 118
    ty = gy - 152
    # Panel boyu kalan yeri dolduruyor; sabit boyda ortada boşluk kalıyordu.
    ph = int(min(540, max(450, ty - 20 - y)))
    py = max(y, ty - 20 - ph)
    pn = spec.get("paneller", [])[:3]
    n = max(1, len(pn))
    bos = 12
    pw = (W - 2 * KEN - (n - 1) * bos) / n
    for i, p in enumerate(pn):
        panel(img, [KEN + i * (pw + bos), py,
                    KEN + i * (pw + bos) + pw, py + ph], p)
    d = ImageDraw.Draw(img)

    # teklif bandı — rakam devasa
    yuvarlak(d, [KEN, ty, W - KEN, ty + 132], 20,
             dolgu=tuple(int(c * 0.72) for c in vurgu))
    yuvarlak(d, [KEN + 5, ty + 5, W - KEN - 5, ty + 127], 16, dolgu=vurgu)
    tek = spec.get("teklif", "")
    if tek:
        parca = ([[tek, "orta"]] if isinstance(tek, str) else tek)
        fdev = U.anton(96)
        fort = U.anton(46)
        pw2 = []
        for m, boy in parca:
            f = fdev if boy == "dev" else fort
            pw2.append((BUY(m), f, d.textlength(BUY(m), font=f)))
        top = sum(w for _, _, w in pw2) + 18 * (len(pw2) - 1)
        olc = min(1.0, (W - 2 * KEN - 60) / max(1.0, top))
        if olc < 1.0:
            fdev = U.anton(max(40, int(96 * olc)))
            fort = U.anton(max(22, int(46 * olc)))
            pw2 = []
            for m, boy in parca:
                f = fdev if boy == "dev" else fort
                pw2.append((BUY(m), f, d.textlength(BUY(m), font=f)))
            top = sum(w for _, _, w in pw2) + 18 * (len(pw2) - 1)
        x = W / 2 - top / 2
        for m, f, w in pw2:
            konturlu(d, (x + w / 2, ty + 68), m, f, BEYAZ,
                     kontur=(26, 16, 12), kalin=5, kaydir=(3, 4))
            x += w + 18

    # güven şeridi
    guv = spec.get("guven", [])[:4]
    if guv:
        yuvarlak(d, [KEN, gy, W - KEN, gy + 62], 14, dolgu=(10, 15, 28))
        gw = (W - 2 * KEN) / len(guv)
        for i, g in enumerate(guv):
            cx = KEN + gw * (i + 0.5)
            fg = sigdir(d, BUY(g), f_mono, gw - 26, 17, 11)
            d.text((cx, gy + 31), BUY(g), font=fg, fill=(214, 226, 244),
                   anchor="mm")
            if i:
                d.line([(KEN + gw * i, gy + 16), (KEN + gw * i, gy + 46)],
                       fill=(40, 52, 78), width=2)

    d.text((W / 2, H - 32), "@sermenkreatif  ·  sermenkreatif.com",
           font=f_mono(21), fill=(210, 220, 238), anchor="mm")
    img.convert("RGB").save(cikti, "JPEG", quality=93, subsampling=0,
                            optimize=True)
    print("%s  %dx%d" % (cikti, W, H))


def hikaye(gonderi, cikti):
    kare = Image.open(gonderi).convert("RGB")
    img = Image.new("RGB", (SW, SH), (10, 14, 26))
    o = (SW - 40) / float(kare.width)
    k = kare.resize((int(kare.width * o), int(kare.height * o)),
                    Image.LANCZOS)
    img.paste(k, (20, int((SH - k.height) / 2)))
    d = ImageDraw.Draw(img)
    d.text((SW / 2, SH - 104), "sermenkreatif.com", font=f_mono(28),
           fill=(190, 204, 228), anchor="mm")
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
