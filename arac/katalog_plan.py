#!/usr/bin/env python3
"""Katalogdaki ürünleri plana alıyor, katalogdan düşeni plandan çıkarıyor.

Yeni ürün siteye girince kendiliğinden yayın sırasına katılıyor; satıştan
kalkan ürün de plandan düşüyor. Yayınlanmış işe dokunmuyor.

    python3 arac/katalog_plan.py
"""
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "arac"))
import urun_katalog as UK                                      # noqa: E402

ICERIK = os.path.join(KOK, "icerik.json")


def main():
    with open(ICERIK, encoding="utf-8") as f:
        d = json.load(f)
    kat = UK.oku()
    kayit = {i["klasor"]: i for i in d["icerik"]}

    eklenen = 0
    for slug, v in kat.items():
        kl = UK.ONEK + slug
        i = kayit.get(kl)
        if i is None:
            d["icerik"].append({"klasor": kl, "kategori": "baski",
                                "konu": slug, "durum": "hazir",
                                "kare": len(v.get("gorsel", []))})
            eklenen += 1
        elif i.get("durum") == "katalogdan-dustu":
            i["durum"] = "hazir"
            i.pop("neden", None)

    dusen = 0
    for i in d["icerik"]:
        s = UK.slug(i["klasor"])
        if s and s not in kat and i.get("durum") == "hazir":
            i["durum"] = "katalogdan-dustu"
            i["neden"] = "Üründen kaldırıldı ya da stokta yok"
            dusen += 1

    with open(ICERIK, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("plana eklenen: %d · plandan düşen: %d" % (eklenen, dusen))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
