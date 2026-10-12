#!/usr/bin/env python3
"""Referans tablosu gönderisi — açık zeminli, yoğun, saklanası kare.

Öteki kapaklar koyu zeminli ve seyrek: bir başlık, bir spot, birkaç kart.
Bu başka bir tür: insanın ekran görüntüsü alıp telefonunda sakladığı
tablo. Açık zemin, renk kodlu satırlar, altta uyarı kutuları.

    python3 arac/rehber.py <spec.json> <cikti.jpg>
"""
import json
import os
import sys

from PIL import Image, ImageDraw

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
import uret as U                                         # noqa: E402

W, H = 1080, 1350
KEN = 36

KAGIT = (243, 246, 250)
MUREKKEP = (16, 22, 38)
SOLUK = (104, 116, 139)
CIZGI = (214, 221, 232)
KART = (255, 255, 255)
LACI = (18, 26, 48)

RENK = {
    "kirmizi": (228, 62, 62), "turuncu": (236, 132, 42),
    "sari": (233, 184, 32), "yesil": (36, 162, 86),
    "mavi": (36, 118, 220), "mor": (134, 80, 226),
    "turkuaz": (22, 162, 173), "pembe": (222, 76, 140),
    "gri": (108, 118, 138),
}


def f_bold(s):
    return U.pop(s, "SemiBold")


def f_reg(s):
    return U.pop(s, "Regular")


def f_mono(s, b=True):
    return U.mono(s, b)


def a(c, op):
    return tuple(c[:3]) + (int(255 * op),)


def yuvarlak(d, kutu, r, dolgu=None, kenar=None, kalin=2):
    d.rounded_rectangle(kutu, radius=r, fill=dolgu, outline=kenar,
                        width=kalin)


def tint(img, kutu, r, renk, op, ust=False):
    """Yarı saydam dolgu. RGB tuvalde alfa yok sayılıyordu; ayrı
    katmana çizip kompozitliyoruz."""
    kat = Image.new("RGBA", img.size, (0, 0, 0, 0))
    k = ImageDraw.Draw(kat)
    k.rounded_rectangle(kutu, radius=r, fill=a(renk, op))
    if ust:                     # üst köşeler yuvarlak, alt düz kalsın
        k.rectangle([kutu[0], kutu[3] - r, kutu[2], kutu[3]],
                    fill=a(renk, op))
    img.alpha_composite(kat)


def isaret(d, tur, x, y, s, renk):
    """✓ ve ✕ yazı tipinde yok, kutu basıyordu; çizgiyle çiziyoruz."""
    w = max(2, int(s * 0.17))
    if tur == "ok":
        d.line([(x, y + s * 0.52), (x + s * 0.36, y + s * 0.86),
                (x + s, y + s * 0.12)], fill=renk, width=w, joint="curve")
    elif tur == "yok":
        d.line([(x + s * 0.1, y + s * 0.12), (x + s * 0.9, y + s * 0.86)],
               fill=renk, width=w)
        d.line([(x + s * 0.9, y + s * 0.12), (x + s * 0.1, y + s * 0.86)],
               fill=renk, width=w)
    else:
        d.ellipse([x + s * 0.34, y + s * 0.4, x + s * 0.66, y + s * 0.72],
                  fill=renk)


def sigdir(d, metin, font_fn, en, bas, taban=11):
    s = bas
    while s > taban and d.textlength(metin, font=font_fn(s)) > en:
        s -= 1
    return font_fn(s)


def sar(d, metin, font, en):
    kel, sat, su = metin.split(), [], ""
    for k in kel:
        dene = (su + " " + k).strip()
        if d.textlength(dene, font=font) <= en or not su:
            su = dene
        else:
            sat.append(su)
            su = k
    if su:
        sat.append(su)
    return sat


# ------------------------------------------------------------------ başlık
def baslik_bandi(img, d, spec):
    y0, y1 = KEN, KEN + 150
    yuvarlak(d, [KEN, y0, W - KEN, y1], 20, dolgu=LACI)

    cip = spec.get("cipler", [])[:4]
    gen, bos = 96, 12
    tx = W - KEN - 26
    if cip:
        tx = W - KEN - 26 - len(cip) * gen - (len(cip) - 1) * bos
    # Başlık çiplerin soluna sığıyor; sığdırmadan basınca altına giriyordu.
    en = tx - (KEN + 30) - 24
    ana = spec["baslik"]
    alt = spec.get("alt", "")
    fb = sigdir(d, ana, U.anton, en, 72, 32)
    d.text((KEN + 30, y0 + (54 if alt else 74)), ana, font=fb,
           fill=(255, 255, 255), anchor="lm")
    if alt:
        fa = sigdir(d, alt, f_reg, en, 25, 15)
        for i, ln in enumerate(sar(d, alt, fa, en)[:2]):
            d.text((KEN + 32, y0 + 100 + i * 28), ln, font=fa,
                   fill=(168, 182, 208), anchor="lm")

    if cip:
        for i, (ad, dgr) in enumerate(cip):
            x = tx + i * (gen + bos)  # noqa: E501
            yuvarlak(d, [x, y0 + 26, x + gen, y0 + 124], 14,
                     dolgu=(30, 40, 68))
            d.text((x + gen / 2, y0 + 58), U.P(dgr), font=f_bold(27),
                   fill=(255, 255, 255), anchor="mm")
            fa = sigdir(d, U.P(ad), f_reg, gen - 12, 17, 11)
            d.text((x + gen / 2, y0 + 96), U.P(ad), font=fa,
                   fill=(150, 166, 196), anchor="mm")
    return y1 + 22


# ------------------------------------------------------------------ tablo
def tablo(img, d, spec, y):
    sut = spec["sutunlar"]
    sat = spec["satirlar"]
    pay = [c.get("pay", 1) for c in sut]
    top = float(sum(pay))
    ic = W - 2 * KEN
    gen = [ic * p / top for p in pay]

    # başlık satırı
    yuvarlak(d, [KEN, y, W - KEN, y + 44], 10, dolgu=(226, 232, 242))
    x = KEN
    for i, c in enumerate(sut):
        d.text((x + 16, y + 22), c["ad"].upper(), font=f_mono(19),
               fill=SOLUK, anchor="lm")
        x += gen[i]
    y += 50

    sh = spec.get("satir_yuksekligi", 72)
    # Punto sütun başına bir kez: hücre başına hesaplanınca satırdan
    # satıra değişip tablo dalgalanıyordu.
    boy = []
    for i in range(len(sut)):
        bas, taban = (30, 16) if i == 0 else (25, 14)
        fn = f_bold if i == 0 else f_reg
        en = gen[i] - (44 if i == 0 else 28)
        s_ = bas
        for r in sat:
            m = U.P(str(r["hucre"][i]))
            if i == 0 or len(m) <= 26:
                while s_ > taban and d.textlength(m, font=fn(s_)) > en:
                    s_ -= 1
        boy.append(s_)

    for r in sat:
        renk = RENK.get(r.get("renk", "mavi"), RENK["mavi"])
        yuvarlak(d, [KEN, y, W - KEN, y + sh], 12, dolgu=KART,
                 kenar=CIZGI, kalin=2)
        d.rounded_rectangle([KEN + 3, y + 10, KEN + 9, y + sh - 10],
                            radius=3, fill=renk)
        x = KEN
        for i, hucre in enumerate(r["hucre"]):
            metin = U.P(str(hucre))
            if i == 0:
                fh = f_bold(boy[i])
                d.text((x + 26, y + sh / 2), metin, font=fh, fill=renk,
                       anchor="lm")
            else:
                fh = f_reg(boy[i])
                sl = sar(d, metin, fh, gen[i] - 28)[:2]
                oy = y + sh / 2 - (len(sl) - 1) * 16
                for j, ln in enumerate(sl):
                    d.text((x + 16, oy + j * 32), ln, font=fh,
                           fill=MUREKKEP, anchor="lm")
            x += gen[i]
        y += sh + 8
    return y + 8


# ------------------------------------------------------------------ kutular
def kutular(img, d, spec, y):
    kut = spec.get("kutular", [])
    if not kut:
        return y
    n = len(kut)
    bos = 12
    gen = (W - 2 * KEN - (n - 1) * bos) / n
    fm = f_reg(18)
    # Kutu boyu içeriğe göre; sabit boyda altta boşluk kalıyordu.
    yuk = 0
    for k in kut:
        h = 56
        for sat in k["satirlar"]:
            m = sat[1] if isinstance(sat, (list, tuple)) else sat
            h += len(sar(d, U.P(m), fm, gen - 48)[:3]) * 24 + 7
        yuk = max(yuk, h + 10)
    yuk = min(yuk, H - 86 - y)

    for i, k in enumerate(kut):
        renk = RENK.get(k.get("renk", "mavi"), RENK["mavi"])
        x = KEN + i * (gen + bos)
        yuvarlak(d, [x, y, x + gen, y + yuk], 14, dolgu=KART,
                 kenar=renk, kalin=2)
        tint(img, [x + 2, y + 2, x + gen - 2, y + 42], 12, renk, 0.13,
             ust=True)
        d = ImageDraw.Draw(img)
        fb = sigdir(d, k["baslik"].upper(), f_mono, gen - 24, 19, 12)
        d.text((x + 14, y + 22), k["baslik"].upper(), font=fb, fill=renk,
               anchor="lm")
        ty = y + 58
        for sat in k["satirlar"]:
            tur, metin = (sat if isinstance(sat, (list, tuple))
                          else ("nokta", sat))
            ir = {"ok": RENK["yesil"], "yok": RENK["kirmizi"]}.get(tur, SOLUK)
            isaret(d, tur, x + 15, ty + 2, 16, ir)
            for ln in sar(d, U.P(metin), fm, gen - 48)[:3]:
                d.text((x + 41, ty), ln, font=fm, fill=MUREKKEP, anchor="la")
                ty += 24
            ty += 7
    return y + yuk


# ------------------------------------------------------------------ künye
def kunye(img, d, spec):
    y = H - 56
    d.line([(KEN, y - 22), (W - KEN, y - 22)], fill=CIZGI, width=2)
    d.text((KEN, y), "@sermenkreatif", font=f_mono(23), fill=MUREKKEP,
           anchor="lm")
    orta = spec.get("kunye", "Kaydet — lazım olacak")
    d.text((W / 2, y), orta, font=f_bold(22), fill=RENK["turuncu"],
           anchor="mm")
    d.text((W - KEN, y), "sermenkreatif.com", font=f_mono(23), fill=SOLUK,
           anchor="rm")


def ciz(spec, cikti):
    img = Image.new("RGBA", (W, H), KAGIT + (255,))
    d = ImageDraw.Draw(img)
    y = baslik_bandi(img, d, spec)
    y = tablo(img, d, spec, y)
    kutular(img, d, spec, y)
    kunye(img, ImageDraw.Draw(img), spec)
    img.convert("RGB").save(cikti, "JPEG", quality=93, subsampling=0,
                            optimize=True)
    print("%s  %dx%d" % (cikti, W, H))


def hikaye(gonderi, cikti):
    """Hikaye sürümü: tablo olduğu gibi, koyu zemin ortasında.

    Tabloyu 9:16'ya yeniden dizmek satırları inceltip okunmaz yapıyor;
    kare olduğu gibi duruyor, hikayede zaten yakınlaştırılıp okunuyor."""
    kare = Image.open(gonderi).convert("RGB")
    sh = 1920
    img = Image.new("RGB", (W, sh), (14, 18, 30))
    o = (W - 2 * 24) / float(kare.width)
    k = kare.resize((int(kare.width * o), int(kare.height * o)),
                    Image.LANCZOS)
    img.paste(k, (24, int((sh - k.height) / 2)))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 120), "KAYDET", font=U.anton(74), fill=(255, 255, 255),
           anchor="mm")
    d.text((W / 2, 182), "lazım olacak", font=f_reg(30),
           fill=(150, 164, 192), anchor="mm")
    d.text((W / 2, sh - 110), "sermenkreatif.com", font=f_mono(28),
           fill=(150, 164, 192), anchor="mm")
    img.save(cikti, "JPEG", quality=92, subsampling=0, optimize=True)
    print("%s  %dx%d" % (cikti, W, sh))


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    U.theme(spec.get("kategori", "3dbaski"))
    ciz(spec, sys.argv[2])
    if len(sys.argv) > 3:
        hikaye(sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
