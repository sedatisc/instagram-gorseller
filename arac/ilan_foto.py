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


# İlan görselleri tek şablondan çıkıyor ve fotoğraf kartının yeri
# sabit. Kartı görüntüden bulmaya çalışmak güvenilir değildi: beyaz
# kart beyaz sayfada kayboluyor, gri ürün doygunluk eşiğini geçmiyor,
# başlık yazısı kadraja giriyordu. Ölçüler ölçülüp sabitlendi.
KAPAK_KUTU = (76, 456, 1125, 1364)      # üstte başlık, altta özellik kartları
DETAY_KUTU = (42, 120, 1158, 1247)      # altında tek satır açıklama
SABLON_BOY = (1200, 1800)


def _kapak_mi(a):
    """Kapakta altta siyah şerit var, detayda yok."""
    h = a.shape[0]
    return float(a[int(h * .945):int(h * .985)].mean()) < 120


def kart_kutusu(im):
    a = np.asarray(im)
    if (im.width, im.height) != SABLON_BOY:
        return (0, 0, im.width, im.height)
    return KAPAK_KUTU if _kapak_mi(a) else DETAY_KUTU


def _kirp_bosluk(im, esik=6, pay=16):
    """Kartın içindeki boş beyaz kenarları alıyor; ürüne dokunmuyor."""
    a = np.asarray(im, dtype=np.int16)
    h, w = a.shape[:2]
    zem = np.median(np.concatenate([a[:4].reshape(-1, 3),
                                    a[-4:].reshape(-1, 3)]), axis=0)
    dolu = np.abs(a - zem).max(axis=2) > esik
    ys, xs = np.nonzero(dolu)
    if len(ys) == 0:
        return im
    return im.crop((max(0, xs.min() - pay), max(0, ys.min() - pay),
                    min(w, xs.max() + pay), min(h, ys.max() + pay)))


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
        # Rozet yaklaşık kare-dikdörtgen bir etiket; logodaki
        # "KREATİF" yazısı ve kırmızı başlık satırları da kırmızı
        # ama ince ve uzun, yükseklik/oran eşiğiyle eleniyor.
        if alan < 1500 or bh < 60 or cx < w * .58:
            continue
        if not h * .10 <= cy <= h * .34:
            continue
        # Rozet dolu bir yuvarlak dikdörtgen; oyuncağın kırmızı
        # parçaları hem düzensiz hem de kutusunu doldurmuyor.
        if alan / float(bw * bh) < 0.72:
            continue
        if not 1.3 <= bw / float(bh) <= 4.6:
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
    kirp = _kirp_bosluk(temiz.crop(kart_kutusu(temiz)))
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
