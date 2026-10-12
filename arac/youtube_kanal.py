#!/usr/bin/env python3
"""YouTube kanal görselleri — banner, profil ve filigran.

    python3 arac/youtube_kanal.py

Çıktılar `youtube/gorsel/` altına yazılıyor:

- `banner.png`   2048 × 1152 — YouTube'un istediği boy. Yazı ve logo
  ortadaki 1235 × 338'lik güvenli alanda; televizyonda kenarlar kırpılıyor,
  telefonda yalnız bu alan görünüyor.
- `profil.png`   800 × 800 — daire kırpıldığında taşmasın diye marka
  işareti ortada ve kenarda bol boşluk var.
- `filigran.png` 150 × 150 — videonun köşesinde duran abone işareti,
  saydam zemin.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
import uret as U                                         # noqa: E402

CIKTI = os.path.join(KOK, "youtube", "gorsel")

ZEMIN = (9, 11, 18)
KOYU = (14, 18, 30)
KIRMIZI = (196, 42, 46)
TURUNCU = (255, 138, 60)
BEYAZ = (255, 255, 255)
SOLUK = (150, 162, 185)


def a(renk, op):
    return renk + (int(255 * op),)


def desen(img, yogun=1.0):
    """Zemine ince devre/filament çizgileri — markanın işi bu."""
    import random
    W, H = img.size
    kat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(kat)
    rnd = random.Random(21)
    for _ in range(int(30 * yogun)):
        x, y = rnd.randrange(W), rnd.randrange(H)
        yon = rnd.choice([(1, 0), (0, 1)])
        for _ in range(rnd.randint(2, 5)):
            u = rnd.randint(70, 240)
            x2, y2 = x + yon[0] * u, y + yon[1] * u
            g.line([(x, y), (x2, y2)], fill=a(SOLUK, 0.10), width=3)
            g.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5],
                      outline=a(SOLUK, 0.14), width=3)
            x, y = x2, y2
            yon = (yon[1], yon[0])
    img.alpha_composite(kat)


def isilti(img, kutu, renk, op, bulanik):
    kat = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(kat).ellipse(kutu, fill=a(renk, op))
    img.alpha_composite(kat.filter(ImageFilter.GaussianBlur(bulanik)))


def zemin(W, H):
    img = Image.new("RGBA", (W, H), ZEMIN + (255,))
    d = ImageDraw.Draw(img)
    for y in range(H):                       # üstte biraz açık, altta koyu
        t = y / float(H)
        c = tuple(int(KOYU[i] + (ZEMIN[i] - KOYU[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c + (255,))
    desen(img)
    return img


def banner():
    W, H = 2048, 1152
    GW, GH = 1235, 338                        # her ekranda görünen alan
    img = zemin(W, H)
    gx, gy = (W - GW) // 2, (H - GH) // 2

    isilti(img, [gx - 260, gy - 120, gx + GW + 260, gy + GH + 120],
           KIRMIZI, 0.20, 180)
    isilti(img, [W * 0.62, H * 0.1, W * 1.1, H * 0.7], TURUNCU, 0.10, 220)

    lg = U._logo.copy()                       # yatay logo
    k = 760.0 / lg.width
    lg = lg.resize((760, max(1, int(lg.height * k))), Image.LANCZOS)
    img.alpha_composite(lg, (gx + (GW - lg.width) // 2, gy + 42))

    d = ImageDraw.Draw(img)
    d.text((W / 2, gy + 196), "3D BASKI · ELEKTRONİK · ATÖLYE",
           font=U.mono(34, True), fill=TURUNCU, anchor="mm")
    d.text((W / 2, gy + 258),
           "Rakamı üreticinin kendi sayfasından veren, kısa ve net videolar",
           font=U.pop(32, "Medium"), fill=BEYAZ, anchor="mm")
    d.text((W / 2, gy + 300), "Her gün yeni Short · sermenkreatif.com",
           font=U.pop(27, "Medium"), fill=SOLUK, anchor="mm")

    # güvenli alanın dışı: yalnız doku kalsın, yazı girmesin
    img.convert("RGB").save(os.path.join(CIKTI, "banner.png"))
    return (W, H)


def profil():
    S = 800
    img = zemin(S, S)
    isilti(img, [S * 0.05, S * 0.05, S * 0.95, S * 0.95], KIRMIZI, 0.30, 120)

    im = Image.open(os.path.join(KOK, "marka", "logo-dikey.png")).convert("RGBA")
    # dikey logodaki işaret üstte; yalnız işareti al
    isaret = im.crop((0, 0, im.width, int(im.height * 0.74)))
    k = (S * 0.56) / isaret.height
    isaret = isaret.resize((int(isaret.width * k), int(isaret.height * k)),
                           Image.LANCZOS)
    img.alpha_composite(isaret, ((S - isaret.width) // 2,
                                 (S - isaret.height) // 2))
    img.convert("RGB").save(os.path.join(CIKTI, "profil.png"))
    return (S, S)


def filigran():
    S = 150
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    im = Image.open(os.path.join(KOK, "marka", "logo-dikey.png")).convert("RGBA")
    isaret = im.crop((0, 0, im.width, int(im.height * 0.74)))
    k = (S * 0.84) / isaret.height
    isaret = isaret.resize((int(isaret.width * k), int(isaret.height * k)),
                           Image.LANCZOS)
    img.alpha_composite(isaret, ((S - isaret.width) // 2,
                                 (S - isaret.height) // 2))
    img.save(os.path.join(CIKTI, "filigran.png"))
    return (S, S)


def main():
    os.makedirs(CIKTI, exist_ok=True)
    U.theme("3dbaski")
    print("banner.png   %dx%d" % banner())
    print("profil.png   %dx%d" % profil())
    print("filigran.png %dx%d" % filigran())


if __name__ == "__main__":
    main()
