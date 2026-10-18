#!/usr/bin/env python3
"""Trendyol ilan görselinden temiz ürün fotoğrafı çıkarıyor.

İlan görsellerinde fotoğraf yuvarlak köşeli bir kartın içinde duruyor
ve sağ üstte kırmızı bir rozet (EĞİTİCİ, TAM SET, SANDIKLI…) gömülü
oluyor. Burada kart bulunup kırpılıyor, rozet ise kesilmeden
zeminden onarılıyor — üst şeridi kesince ürünün tepesi gidiyordu.

    python3 arac/ilan_foto.py <kaynak.png> <cikti-adi> [...]

Çiftler halinde verilir:
    python3 arac/ilan_foto.py a.png alyan-set b.png alyan-parcalar
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIK = os.path.join(KOK, "gorsel", "urun", "foto")


def _en_uzun(maske):
    en, bas = (0, 0, 0), None
    for i, v in enumerate(list(maske) + [False]):
        if v and bas is None:
            bas = i
        elif not v and bas is not None:
            if i - bas > en[0]:
                en = (i - bas, bas, i)
            bas = None
    return en[1], en[2]


def urun_kutusu(im, pay=34):
    """Ürünün kutusu.

    Kartı aramak güvenilir değil: beyaz kart beyaz sayfanın üstünde
    kayboluyor, kadrajı kesiyordu. Doygun renkli en büyük leke ürünün
    kendisi; başlık ve alt yazı doygun değil, böylece dışarıda kalıyor.
    Siyah stand gibi doygun olmayan parçalar ürünün yakınında olduğu
    için sonradan ekleniyor."""
    a = np.asarray(im)
    h, w = a.shape[:2]
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    S, V = hsv[:, :, 1].astype(int), hsv[:, :, 2].astype(int)
    cek = np.ones((15, 15), np.uint8)

    renk = ((S > 60) & (V > 40)).astype(np.uint8)
    renk[:int(h * .035)] = 0
    renk[int(h * .965):] = 0
    renk = cv2.morphologyEx(renk, cv2.MORPH_CLOSE, cek)
    n, _e, ist, _m = cv2.connectedComponentsWithStats(renk, 8)
    if n < 2:
        return (0, 0, w, h)
    i = 1 + int(np.argmax(ist[1:, cv2.CC_STAT_AREA]))
    x, yy = ist[i, cv2.CC_STAT_LEFT], ist[i, cv2.CC_STAT_TOP]
    bw, bh = ist[i, cv2.CC_STAT_WIDTH], ist[i, cv2.CC_STAT_HEIGHT]
    kutu = [x, yy, x + bw, y_alt] if False else [x, yy, x + bw, yy + bh]

    # ürüne yapışık doygun olmayan parçalar (siyah stand, gri delikler)
    gx, gy = bw * .12 + 40, bh * .12 + 40
    yakin = (kutu[0] - gx, kutu[1] - gy, kutu[2] + gx, kutu[3] + gy)
    tum = ((S > 45) | (V < 205)).astype(np.uint8)
    tum[:int(h * .035)] = 0
    tum[int(h * .965):] = 0
    tum = cv2.morphologyEx(tum, cv2.MORPH_CLOSE, cek)
    n2, _e2, ist2, mer2 = cv2.connectedComponentsWithStats(tum, 8)
    for j in range(1, n2):
        if ist2[j, cv2.CC_STAT_AREA] < 2500:
            continue
        cx, cy = mer2[j]
        if not (yakin[0] <= cx <= yakin[2] and yakin[1] <= cy <= yakin[3]):
            continue
        jx, jy = ist2[j, cv2.CC_STAT_LEFT], ist2[j, cv2.CC_STAT_TOP]
        jw, jh = ist2[j, cv2.CC_STAT_WIDTH], ist2[j, cv2.CC_STAT_HEIGHT]
        if jw > w * .9 and jh < h * .06:
            continue
        kutu = [min(kutu[0], jx), min(kutu[1], jy),
                max(kutu[2], jx + jw), max(kutu[3], jy + jh)]
    return (max(0, kutu[0] - pay), max(0, kutu[1] - pay),
            min(w, kutu[2] + pay), min(h, kutu[3] + pay))


def rozet_sil(im):
    """Sağ üst köşedeki rozeti onarıyor.

    Ürünün kendi kırmızısı da var; en büyük lekeyi değil, sağ üst
    köşeye en yakın olanı seçiyoruz."""
    a = np.asarray(im)
    h, w = a.shape[:2]
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    H = hsv[:, :, 0].astype(int)
    S = hsv[:, :, 1].astype(int)
    V = hsv[:, :, 2].astype(int)
    kir = (((H < 10) | (H > 168)) & (S > 95) & (V > 80)).astype(np.uint8)
    kir = cv2.morphologyEx(kir, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    n, etiket, ist, mer = cv2.connectedComponentsWithStats(kir, 8)
    secili, en_yakin = None, None
    for i in range(1, n):
        alan = ist[i, cv2.CC_STAT_AREA]
        bw, bh = ist[i, cv2.CC_STAT_WIDTH], ist[i, cv2.CC_STAT_HEIGHT]
        cx, cy = mer[i]
        if alan < 1500 or cy > h * .30 or cx < w * .45:
            continue
        # Rozet dolu bir yuvarlak dikdörtgen; oyuncağın kırmızı
        # parçaları hem düzensiz hem de kutusunu doldurmuyor.
        if alan / float(bw * bh) < 0.72:
            continue
        if not 1.7 <= bw / float(bh) <= 6.5:
            continue
        d = np.hypot(cx - w, cy)
        if en_yakin is None or d < en_yakin:
            secili, en_yakin = i, d
    if secili is None:
        return im, False
    maske = cv2.dilate((etiket == secili).astype(np.uint8),
                       np.ones((21, 21), np.uint8), iterations=3)
    # Rozetin dışına taşan soluk pembe hale doygunluk eşiğini
    # geçmiyor; kutunun çevresinde kırmızıya çalan ne varsa alıyoruz.
    ys, xs = np.nonzero(maske)
    p = 90
    bx1, bx2 = max(0, xs.min() - p), min(w, xs.max() + p)
    by1, by2 = max(0, ys.min() - p), min(h, ys.max() + p)
    b = a[by1:by2, bx1:bx2].astype(int)
    hale = (b[:, :, 0] - np.maximum(b[:, :, 1], b[:, :, 2]) > 7)
    ek = np.zeros((h, w), np.uint8)
    ek[by1:by2, bx1:bx2] = hale.astype(np.uint8)
    maske = cv2.dilate(np.maximum(maske, ek), np.ones((9, 9), np.uint8), 1)
    onar = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), maske, 16,
                       cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(onar, cv2.COLOR_BGR2RGB)), True


def cikar(kaynak, ad):
    os.makedirs(CIK, exist_ok=True)
    im = Image.open(kaynak).convert("RGB")
    temiz, silindi = rozet_sil(im)
    kirp = temiz.crop(urun_kutusu(temiz))
    yol = os.path.join(CIK, ad + ".jpg")
    kirp.save(yol, quality=95)
    return yol, kirp.size, silindi


def main():
    arg = sys.argv[1:]
    if not arg or len(arg) % 2:
        raise SystemExit(__doc__)
    for kaynak, ad in zip(arg[0::2], arg[1::2]):
        yol, boy, silindi = cikar(kaynak, ad)
        print("%-24s %-12s rozet %s"
              % (ad, "%dx%d" % boy, "onarıldı" if silindi else "yok"))


if __name__ == "__main__":
    main()
