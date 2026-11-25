#!/usr/bin/env python3
"""Ürün görsellerini JPEG olarak depoya aktarıyor.

Instagram, medyayı verdiğimiz adresten kendisi indiriyor ve yalnız
JPEG kabul ediyor. Sitedeki ürün görselleri .webp olduğu için gönderiler
"Only photo or video can be accepted as media type" ve "It takes too
long to download the media" hatalarıyla düşüyordu — 25 Kasım'da altı
işin altısı bu yüzden yayına çıkmadı.

Görsel değiştirilmiyor: sitedeki karenin aynısı, yalnız JPEG'e çevrilip
depoya konuyor. Gönderi de depodaki hızlı adresi kullanıyor.

İnternet gerekiyor; GitHub Actions'ta çalışıyor.

    python3 arac/urun_gorsel_aktar.py --kilit        # onaylı günler
    python3 arac/urun_gorsel_aktar.py --gun 2026-11-26
    python3 arac/urun_gorsel_aktar.py --urun kurdele-vazo-silk-parlak-3d-baski
    python3 arac/urun_gorsel_aktar.py --kilit --kuru # yalnız rapor
"""
import concurrent.futures as cf
import io
import os
import sys
import time
import urllib.request

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
sys.path.insert(0, os.path.join(KOK, "arac"))

import sira                                                # noqa: E402
import urun_katalog as UK                                   # noqa: E402

HEDEF = os.path.join(KOK, "gorsel", "urun")
AJAN = {"User-Agent": "sermenkreatif-yayin/1.0"}
UZUN_KENAR = 1440          # Instagram zaten 1440'a indiriyor
KALITE = 88
# Instagram akış gönderisinde kabul edilen en/boy aralığı. Dışına taşan
# kare beyaz zeminle kareye tamamlanıyor, kırpılmıyor.
EN_DAR, EN_GENIS = 0.80, 1.91


# Tek karenin indirilmesi için üst sınır. Site medyayı bazen çok yavaş
# veriyor; 25 Kasım'da aktarım 20 dakikada tek kare bitirmeden iş akışı
# zaman aşımına düştü. Takılan kare bütçeyi yemesin diye kısa tutuluyor,
# denemesi yineleniyor.
ZAMAN_ASIMI = 25
DENEME = 3


def indir(url):
    son = None
    for d in range(DENEME):
        try:
            r = urllib.request.Request(url, headers=AJAN)
            return urllib.request.urlopen(r, timeout=ZAMAN_ASIMI).read()
        except Exception as e:
            son = e
            time.sleep(1 + d)
    raise son


def cevir(ham):
    from PIL import Image
    g = Image.open(io.BytesIO(ham))
    if g.mode in ("RGBA", "LA", "P"):
        zemin = Image.new("RGB", g.size, (255, 255, 255))
        g = g.convert("RGBA")
        zemin.paste(g, mask=g.split()[-1])
        g = zemin
    else:
        g = g.convert("RGB")

    oran = g.width / g.height
    if oran < EN_DAR or oran > EN_GENIS:
        k = max(g.width, g.height)
        zemin = Image.new("RGB", (k, k), (255, 255, 255))
        zemin.paste(g, ((k - g.width) // 2, (k - g.height) // 2))
        g = zemin

    if max(g.size) > UZUN_KENAR:
        p = UZUN_KENAR / max(g.size)
        g = g.resize((round(g.width * p), round(g.height * p)),
                     Image.LANCZOS)

    tampon = io.BytesIO()
    g.save(tampon, "JPEG", quality=KALITE, optimize=True, progressive=True)
    return tampon.getvalue(), g.size


def slugler():
    """İşlenecek ürün slugları."""
    if "--urun" in sys.argv:
        return [sys.argv[sys.argv.index("--urun") + 1]]
    gunler = None
    if "--gun" in sys.argv:
        gunler = {sys.argv[sys.argv.index("--gun") + 1]}
    kil = sira.kilit() or {}
    if gunler is None and "--kilit" not in sys.argv:
        gunler = set(kil)                      # öntanımlı: onaylı günler
    out, gorulen = [], set()
    for t, satirlar in sorted(kil.items()):
        if gunler is not None and t not in gunler:
            continue
        for s in satirlar:
            sl = UK.slug(s["klasor"])
            if sl and sl not in gorulen:
                gorulen.add(sl)
                out.append(sl)
    return out


def main():
    kuru = "--kuru" in sys.argv
    yenile = "--yenile" in sys.argv
    if not kuru:
        os.makedirs(HEDEF, exist_ok=True)
    sl = slugler()
    print("ürün: %d" % len(sl), flush=True)

    isler, atlanan, hata = [], 0, 0
    for s in sl:
        urller = UK.gorseller(UK.ONEK + s)
        if not urller:
            print("  %s — site görseli yok" % s, flush=True)
            hata += 1
            continue
        for i, u in enumerate(urller[:10], 1):
            ad = "%s-%d.jpg" % (s, i)
            if os.path.exists(os.path.join(HEDEF, ad)) and not yenile:
                atlanan += 1
                continue
            isler.append((ad, u))
    print("indirilecek kare: %d · zaten vardı: %d" % (len(isler), atlanan),
          flush=True)

    def getir(is_):
        ad, u = is_
        t = time.time()
        try:
            veri, boy = cevir(indir(u))
        except Exception as e:
            return ad, None, None, time.time() - t, str(e)
        return ad, veri, boy, time.time() - t, ""

    yeni = 0
    with cf.ThreadPoolExecutor(6) as ex:
        for ad, veri, boy, sure, e in ex.map(getir, isler):
            if veri is None:
                print("  %s — %.1f sn sonra: %s" % (ad, sure, e), flush=True)
                hata += 1
                continue
            if not kuru:
                with open(os.path.join(HEDEF, ad), "wb") as f:
                    f.write(veri)
            print("  %s  %dx%d  %d KB  %.1f sn%s"
                  % (ad, boy[0], boy[1], len(veri) // 1024, sure,
                     " (kuru)" if kuru else ""), flush=True)
            yeni += 1

    print("yeni: %d · zaten vardı: %d · hata: %d" % (yeni, atlanan, hata),
          flush=True)
    return 1 if hata and not yeni else 0


if __name__ == "__main__":
    raise SystemExit(main())
