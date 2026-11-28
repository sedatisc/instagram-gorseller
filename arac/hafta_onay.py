#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Onaya sunulacak haftayı otomasyon/hafta-onay.json olarak yazıyor.

Türetilmiş plandan belirtilen aralıktaki gönderileri (hikayeler hariç)
alıp onay tablosunun beklediği biçime çeviriyor: saat, kategori, ad,
kapak ve metnin başı. Tabloyu `arac/hafta_tablo.py` çiziyor.

Kilit yazmıyor; onay alınınca `arac/hafta_kilitle.py` çalıştırılıyor.

    python3 arac/hafta_onay.py                  # yarından 7 gün
    python3 arac/hafta_onay.py 2026-11-30 7
"""
import json
import os
import re
import sys
from datetime import date, timedelta

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
sys.path.insert(0, os.path.join(KOK, "otomasyon"))
sys.path.insert(0, os.path.join(KOK, "arac"))

import urun_katalog as UK                                   # noqa: E402
import yayinla                                              # noqa: E402

CIKTI = os.path.join(KOK, "otomasyon", "hafta-onay.json")
OZET_UZUNLUK = 220


def metin_basi(klasor):
    """Klasördeki metin.md'nin gönderi metninin başı."""
    yol = os.path.join(KOK, klasor, "metin.md")
    if not os.path.exists(yol):
        return "", ""
    ham = open(yol, encoding="utf-8").read()
    govde = ham.split("## Gönderi metni", 1)[-1].strip()
    satirlar = [s.strip() for s in govde.split("\n") if s.strip()
                and not s.startswith("#")]
    if not satirlar:
        return "", ""
    duz = " ".join(satirlar)
    duz = re.sub(r"\s+", " ", duz)
    return satirlar[0][:80], duz[:OZET_UZUNLUK]


def kapak(klasor):
    """Gönderinin ilk karesi: ürün ise site adresi, değilse depo yolu."""
    if klasor.startswith(UK.ONEK):
        # Depoya aktarılmış JPEG varsa o: hem indirme gerekmiyor hem de
        # yayına gidecek karenin aynısı görünüyor.
        import sira
        y = sira.urun_kareleri(klasor)
        if y:
            return y[0]
        g = UK.gorseller(klasor)
        return g[0] if g else ""
    for ad in ("1.jpg", "1.png", "1.jpeg"):
        y = os.path.join(KOK, klasor, ad)
        if os.path.exists(y):
            return "%s/%s" % (klasor, ad)
    return ""


def main():
    bas = (date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1
           else date.today() + timedelta(days=1))
    gun = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    son = bas + timedelta(days=gun - 1)

    # icerik.json'da "baslik" varsa tabloda o yazıyor; yoksa metnin ilk
    # satırı kullanılıyor ve o çoğu zaman cümle oluyor.
    with open(os.path.join(KOK, "icerik.json"), encoding="utf-8") as f:
        baslik = {i["klasor"]: i.get("baslik", "")
                  for i in json.load(f)["icerik"]}

    out = []
    for i in yayinla.gundem():
        if i["tur"] != "gonderi":
            continue
        t = date.fromisoformat(i["zaman"][:10])
        if not (bas <= t <= son):
            continue
        k = i["klasor"]
        if k.startswith(UK.ONEK):
            ad = UK.ad(k)
            ozet = (UK.metin(k)[0] or "").replace("\n", " ")
            ozet = re.sub(r"\s+", " ", ozet)[:OZET_UZUNLUK]
        else:
            ad, ozet = metin_basi(k)
            ad = baslik.get(k) or ad
        out.append({"tarih": i["zaman"][:10], "saat": i["zaman"][11:16],
                    "kategori": i.get("kategori", ""), "klasor": k,
                    "ad": ad or k, "kapak": kapak(k), "ozet": ozet})

    out.sort(key=lambda x: (x["tarih"], x["saat"]))
    with open(CIKTI, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("%s – %s · %d gönderi" % (bas, son, len(out)))
    eksik = [p["klasor"] for p in out if not p["kapak"]]
    if eksik:
        print("kapağı olmayan: %s" % ", ".join(eksik))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
