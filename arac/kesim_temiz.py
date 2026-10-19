#!/usr/bin/env python3
"""Kesilmiş ürün PNG'lerindeki arka plan artıklarını siliyor.

Arka plan kesildikten sonra geriye iki tür artık kalıyor:

* Soluk hayalet lekeler — duman, tül, gölge, yanındaki eşyanın yarısı.
  Yarı saydam oldukları için gözle beyaz zeminde fark edilmiyor, koyu
  kapaklarda leke olarak çıkıyor.
* Ürüne değmeyen küçük kopuk parçalar.

Ana kütleye bağlı olmayan ve ortalama matlığı düşük olan her parça
siliniyor; ürünün kendisi (en büyük mat kütle) ve ona değen her şey
duruyor.

    python3 arac/kesim_temiz.py                 # kesik/ klasörünün tamamı
    python3 arac/kesim_temiz.py a.png b.png     # verilenler
"""
import glob
import os
import sys

import numpy as np
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KESIK = os.path.join(KOK, "gorsel", "urun", "kesik")

ESIK = 110          # bu matlığın altındaki piksel "hayalet" sayılıyor
SIL = 40            # bunun altındaki matlık büsbütün siliniyor
PAY = 0.02          # ana kütlenin bu oranından küçük parçalar elenir


def yer_tutucu_mu(im):
    """Sitenin "görsel yok" kareleri — gri fotoğraf makinesi simgesi.

    Bunlar ürün fotoğrafı değil; gönderiye girerse kartta simge çıkıyor.
    Tek tonlu ve avuç içi kadar renk barındırdıkları için ayırt ediliyor;
    siyah nozul fotoğrafları bu eşiği geçmiyor."""
    a = np.asarray(im.convert("RGBA"))
    m = a[:, :, 3] > 100
    if m.sum() < 100:
        return False
    rgb = a[:, :, :3][m].astype(int)
    if (rgb.max(1) - rgb.min(1)).mean() >= 0.2:
        return False
    return len(np.unique(rgb // 24, axis=0)) <= 8


def _bilesenler(maske):
    """Bağlı bileşen etiketleri; OpenCV yoksa scipy, o da yoksa None."""
    try:
        import cv2
        n, et = cv2.connectedComponents(maske.astype(np.uint8), 8)
        return n, et
    except ImportError:
        pass
    try:
        from scipy import ndimage
        et, n = ndimage.label(maske)
        return n + 1, et
    except ImportError:
        return None, None


def temizle(yol, yaz=True):
    im = Image.open(yol).convert("RGBA")
    a = np.asarray(im).copy()
    alfa = a[:, :, 3].astype(int)
    if alfa.max() == 0:
        return None

    # Ürünün gövdesi: iyice mat pikseller. Hayaletler bu eşiği geçmiyor.
    cekirdek = alfa >= ESIK
    if not cekirdek.any():
        return None
    n, et = _bilesenler(alfa > SIL)
    if et is None:
        return None

    # Hangi bileşen gerçek ürün: en çok mat piksel barındıran.
    sayim = np.zeros(n, dtype=np.int64)
    np.add.at(sayim, et[cekirdek], 1)
    sayim[0] = 0
    ana = int(sayim.argmax())
    if sayim[ana] == 0:
        return None

    tut = np.zeros(n, dtype=bool)
    tut[ana] = True
    # Ürünün yanındaki ayrı ama mat duran parçalar (tabak, bitki, kapak)
    # kalsın; yalnız hem kopuk hem soluk olanlar gitsin.
    for i in range(1, n):
        if i == ana or sayim[i] == 0:
            continue
        if sayim[i] >= sayim[ana] * PAY:
            tut[i] = True

    kal = tut[et]
    yeni = np.where(kal, alfa, 0)
    yeni = np.where(yeni < SIL, 0, yeni)
    if yeni.max() == 0:
        return None
    a[:, :, 3] = yeni.astype(np.uint8)

    k = Image.fromarray(a, "RGBA")
    bb = k.split()[-1].point(lambda v: 255 if v > 8 else 0).getbbox()
    if bb:
        k = k.crop(bb)
    silinen = int((alfa > SIL).sum() - (yeni > SIL).sum())
    if yaz and silinen > 0:
        k.save(yol)
    return silinen, k.size


def main():
    hedef = sys.argv[1:] or sorted(glob.glob(os.path.join(KESIK, "*.png")))
    degisen = 0
    for p in hedef:
        s = temizle(p)
        if not s:
            continue
        silinen, boy = s
        if silinen > 0:
            degisen += 1
            print("%-56s -%d piksel  %dx%d"
                  % (os.path.basename(p)[:56], silinen, boy[0], boy[1]))
    print("%d dosyadan %d tanesi temizlendi." % (len(hedef), degisen))


if __name__ == "__main__":
    main()
