#!/usr/bin/env python3
"""Çekiliş afişi — kampanya kapağı ve hikaye karesi.

Normal gönderi kapakları `uret.py` ile çıkıyor; kampanya afişi ayrı,
çünkü düzeni başka: dev başlık, konfeti, podyumda dört ürün, kural
kutusu ve alt şerit.

    python3 arac/cekilis_afis.py <klasor>

`<klasor>/1.jpg` ve `<klasor>/hikaye.jpg` dosyalarını yazıyor — yani
uret.py çalıştıktan SONRA çalıştırılıyor, kapağı o üzerine yazıyor.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
import uret as U                                         # noqa: E402

URUN = [("1 Adet", "Silk Blue", "cekilis-silk-blue"),
        ("1 Adet", "TPU · Black", "cekilis-tpu-siyah"),
        ("1 Adet", "PETG · Blue", "cekilis-petg-mavi"),
        ("1 Adet", "ABS · Blue", "cekilis-abs-mavi")]

KURAL = ["Sayfamızı takip edin (@sermenkreatif)",
         "Bu gönderiyi beğenin",
         "Yoruma ne basacağınızı yazın"]

LACI = (6, 20, 56)
KOYU = (3, 10, 30)
MAVI = (38, 130, 235)
ACIK = (120, 200, 255)
ALTIN = (247, 196, 62)
BEYAZ = (255, 255, 255)


def a(renk, op):
    return renk + (int(255 * op),)


# ------------------------------------------------------------- zemin
def zemin(W, H):
    img = Image.new("RGB", (W, H), LACI)
    d = ImageDraw.Draw(img)
    for y in range(H):                      # dikey geçiş
        t = y / float(H)
        k = 1 - abs(t - 0.38) * 1.5
        c = tuple(int(KOYU[i] + (LACI[i] - KOYU[i]) * max(0.0, k) +
                      (MAVI[i] - LACI[i]) * max(0.0, k) * 0.30)
                  for i in range(3))
        d.line([(0, y), (W, y)], fill=c)

    kat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(kat)
    rnd = random.Random(7)
    for _ in range(26):                     # devre yolları
        x, y = rnd.randrange(W), rnd.randrange(H)
        yon = rnd.choice([(1, 0), (0, 1)])
        for _ in range(rnd.randint(2, 4)):
            u = rnd.randint(60, 190)
            x2, y2 = x + yon[0] * u, y + yon[1] * u
            g.line([(x, y), (x2, y2)], fill=a(ACIK, 0.13), width=3)
            g.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], outline=a(ACIK, 0.2),
                      width=3)
            x, y = x2, y2
            yon = (yon[1], yon[0])
    img.paste(Image.alpha_composite(img.convert("RGBA"), kat).convert("RGB"))

    par = Image.new("RGBA", (W, H), (0, 0, 0, 0))     # merkez ışığı
    pg = ImageDraw.Draw(par)
    pg.ellipse([-W * 0.3, -H * 0.25, W * 1.3, H * 0.75], fill=a(MAVI, 0.26))
    par = par.filter(ImageFilter.GaussianBlur(160))
    return Image.alpha_composite(img.convert("RGBA"), par)


def konfeti(img, tohum=3, adet=90, bitis=0.42, bosluk=None):
    """Konfeti yalnız üst bantta; etiket bandına girmiyor, yazı okunsun."""
    W, H = img.size
    kat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rnd = random.Random(tohum)
    for _ in range(adet):
        x, y = rnd.randrange(W), rnd.randrange(int(H * bitis))
        if bosluk and any(b0 <= y <= b1 for b0, b1 in bosluk):
            continue
        w, h = rnd.randint(9, 20), rnd.randint(16, 34)
        renk = rnd.choice([ALTIN, BEYAZ, ACIK, (255, 164, 60)])
        parca = Image.new("RGBA", (w, h), a(renk, rnd.uniform(0.55, 0.95)))
        parca = parca.rotate(rnd.randrange(360), expand=True,
                             resample=Image.BICUBIC)
        kat.alpha_composite(parca, (x, y))
    img.alpha_composite(kat)


def isilti(img, kutu, renk, op=0.5, bulanik=70):
    W, H = img.size
    kat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(kat).ellipse(kutu, fill=a(renk, op))
    img.alpha_composite(kat.filter(ImageFilter.GaussianBlur(bulanik)))


def golgeli_yazi(img, xy, metin, font, dolgu, kenar=(2, 8, 28), kalin=6,
                 hiza="mm"):
    kat = Image.new("RGBA", img.size, (0, 0, 0, 0))
    g = ImageDraw.Draw(kat)
    g.text((xy[0], xy[1] + 7), metin, font=font, fill=a(kenar, 0.55),
           anchor=hiza, stroke_width=kalin, stroke_fill=a(kenar, 0.55))
    img.alpha_composite(kat.filter(ImageFilter.GaussianBlur(7)))
    d = ImageDraw.Draw(img)
    d.text(xy, metin, font=font, fill=dolgu, anchor=hiza,
           stroke_width=kalin, stroke_fill=kenar)


# ------------------------------------------------------------- parçalar
def urun_sirasi(img, ust, yuk, kucuk=False):
    """Dört ürünü podyumların üstüne diz, etiketlerini yaz."""
    W = img.size[0]
    pay = W / 4.0
    fk = U.pop(23 if not kucuk else 21, "SemiBold")
    fb = U.pop(27 if not kucuk else 25, "Bold")
    d = ImageDraw.Draw(img)
    for i, (adet, ad, dosya) in enumerate(URUN):
        cx = pay * i + pay / 2
        d.text((cx, ust), adet, font=fk, fill=a(BEYAZ, 0.82)[:3], anchor="mm")
        d.text((cx, ust + 34), ad, font=fb, fill=BEYAZ, anchor="mm")

        yol = os.path.join(KOK, "gorsel", "urun", "kesik-%s.png" % dosya)
        if not os.path.exists(yol):
            continue
        im = Image.open(yol).convert("RGBA")
        k = min((pay - 34) / im.width, yuk / im.height)
        im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))),
                       Image.LANCZOS)
        y0 = ust + 70
        taban = y0 + yuk
        isilti(img, [cx - pay * 0.42, taban - 46, cx + pay * 0.42, taban + 42],
               MAVI, 0.5, 42)
        pod = Image.new("RGBA", img.size, (0, 0, 0, 0))
        pg = ImageDraw.Draw(pod)
        pg.ellipse([cx - pay * 0.36, taban - 20, cx + pay * 0.36, taban + 26],
                   fill=a(ACIK, 0.30))
        pg.ellipse([cx - pay * 0.30, taban - 14, cx + pay * 0.30, taban + 18],
                   fill=a(BEYAZ, 0.22))
        img.alpha_composite(pod)
        img.alpha_composite(im, (int(cx - im.width / 2),
                                 int(taban - im.height)))


def kural_kutusu(img, y, genislik=None, fs=30):
    W = img.size[0]
    gen = genislik or int(W * 0.86)
    x0 = (W - gen) // 2
    h = 56 * len(KURAL) + 34
    kat = Image.new("RGBA", img.size, (0, 0, 0, 0))
    g = ImageDraw.Draw(kat)
    g.rounded_rectangle([x0, y, x0 + gen, y + h], radius=26,
                        fill=a(KOYU, 0.55), outline=a(ACIK, 0.35), width=3)
    img.alpha_composite(kat)
    d = ImageDraw.Draw(img)
    f = U.pop(fs, "SemiBold")
    yy = y + 17
    for k in KURAL:
        d.ellipse([x0 + 34, yy + 20, x0 + 48, yy + 34], fill=ALTIN)
        d.text((x0 + 66, yy + 27), k, font=f, fill=BEYAZ, anchor="lm")
        yy += 56
    return y + h


def alt_serit(img, y, sol, sag, fs=29):
    W = img.size[0]
    gen = int(W * 0.86)
    x0 = (W - gen) // 2
    kat = Image.new("RGBA", img.size, (0, 0, 0, 0))
    g = ImageDraw.Draw(kat)
    g.rounded_rectangle([x0, y, x0 + gen, y + 74], radius=20,
                        fill=a(ALTIN, 0.16), outline=a(ALTIN, 0.85), width=3)
    img.alpha_composite(kat)
    d = ImageDraw.Draw(img)
    f = U.pop(fs, "Bold")
    d.text((x0 + 34, y + 37), sol, font=f, fill=ALTIN, anchor="lm")
    d.text((x0 + gen - 34, y + 37), sag, font=f, fill=ALTIN, anchor="rm")
    orta = x0 + gen / 2
    d.line([(orta, y + 16), (orta, y + 58)], fill=a(ALTIN, 0.5), width=2)


def logo(img, y):
    W = img.size[0]
    lg = U._logo.copy()
    k = 300.0 / lg.width
    lg = lg.resize((300, max(1, int(lg.height * k))), Image.LANCZOS)
    img.alpha_composite(lg, ((W - lg.width) // 2, y))
    return y + lg.height


# ------------------------------------------------------------- afişler
def gonderi(yol, son=False):
    W, H = 1080, 1350
    img = zemin(W, H)
    konfeti(img, bitis=0.40, bosluk=[(40, 130), (430, 545)])
    d = ImageDraw.Draw(img)

    logo(img, 52)
    f1 = U.anton(158)
    f2 = U.anton(150)
    golgeli_yazi(img, (W / 2, 232), "SON GÜN" if son else "BÜYÜK", f1, BEYAZ)
    golgeli_yazi(img, (W / 2, 372), "ÇEKİLİŞ!", f2, ALTIN)

    d = ImageDraw.Draw(img)
    d.text((W / 2, 516),
           "BU GECE 23.59'DA KAPANIYOR" if son else "DÖRT MAKARA · TEK KAZANAN",
           font=U.mono(28, True), fill=a(ACIK, 0.95)[:3], anchor="mm")

    urun_sirasi(img, 566, 286)
    alt = kural_kutusu(img, 975)
    alt_serit(img, alt + 22, "TEK KAZANAN · 4 MAKARA",
              "BUGÜN SON" if son else "SÜRE: 4 GÜN")

    d = ImageDraw.Draw(img)
    d.text((W / 2, 1312),
           "Yarın üç finalist hikayede, kazananı anket seçiyor" if son
           else "Kazananı 16 Ekim'de takipçi anketi seçiyor",
           font=U.pop(24, "Medium"), fill=a(BEYAZ, 0.72)[:3], anchor="mm")
    U.yaz(img, yol)


def hikaye(yol):
    W, H = 1080, 1920
    img = zemin(W, H)
    konfeti(img, tohum=11, adet=130, bitis=0.42,
            bosluk=[(240, 360), (740, 840)])

    logo(img, 258)
    golgeli_yazi(img, (W / 2, 486), "BÜYÜK", U.anton(168), BEYAZ)
    golgeli_yazi(img, (W / 2, 648), "ÇEKİLİŞ!", U.anton(160), ALTIN)

    d = ImageDraw.Draw(img)
    d.text((W / 2, 794), "DÖRT MAKARA · TEK KAZANAN",
           font=U.mono(30, True), fill=a(ACIK, 0.95)[:3], anchor="mm")

    urun_sirasi(img, 846, 352)
    alt = kural_kutusu(img, 1346, fs=31)
    alt_serit(img, alt + 34, "TEK KAZANAN · 4 MAKARA", "SÜRE: 4 GÜN", fs=30)

    d = ImageDraw.Draw(img)
    d.text((W / 2, 1724), "Son gün 15 Ekim 23.59",
           font=U.pop(34, "Bold"), fill=BEYAZ, anchor="mm")
    d.text((W / 2, 1776), "Kazananı 16 Ekim'de takipçi anketi seçiyor",
           font=U.pop(26, "Medium"), fill=a(BEYAZ, 0.75)[:3], anchor="mm")
    U.yaz(img, yol)


def main():
    arg = [x for x in sys.argv[1:] if not x.startswith("--")]
    klasor = arg[0] if arg else "2026-10-12-cekilis-duyuru"
    son = "--son" in sys.argv          # son gün sürümü
    U.theme("3dbaski")
    gonderi(os.path.join(KOK, klasor, "1.jpg"), son=son)
    if not son:
        hikaye(os.path.join(KOK, klasor, "hikaye.jpg"))
    print("afiş yazıldı: %s/1.jpg ve hikaye.jpg" % klasor)


if __name__ == "__main__":
    main()
