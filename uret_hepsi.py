#!/usr/bin/env python3
"""Bütün gönderi klasörlerini HTML şablonlarıyla yeniden basıyor.

Hangi şablonun kullanılacağını spec.json'ın şekli söylüyor:
  * "sablon": "ilan"                            -> arac/ilan_html.py
  * "urunler" listesi                           -> arac/kart_html.py
  * gerisi                                      -> arac/rehber_html.py

    python3 uret_hepsi.py              # hepsi
    python3 uret_hepsi.py 2026-10-10-*  # yalnız verilenler
"""
import json
import os
import sys
import traceback

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(KOK, "arac"))
sys.path.insert(0, os.path.join(KOK, "arac", "html"))

import ilan_html                                            # noqa: E402
import kart_html                                            # noqa: E402
import rehber_html                                          # noqa: E402


def sablon(spec):
    # Yalnız "urunler" listesi olan spec kart şablonuna gidiyor. Kapak
    # tipi "urun" olan tek ürünlük rehber gönderilerinde o liste yok,
    # kart şablonu onlarda KeyError veriyordu.
    if spec.get("sablon") == "ilan":
        return ilan_html
    if spec.get("urunler"):
        return kart_html
    return rehber_html


def klasorler(arg):
    if arg:
        return [a.rstrip("/") for a in arg]
    return sorted(k for k in os.listdir(KOK)
                  if k.startswith("2026-") and os.path.isdir(os.path.join(KOK, k)))


def main():
    tamam, atlanan, hata = 0, [], []
    for k in klasorler(sys.argv[1:]):
        yol = os.path.join(KOK, k, "spec.json")
        if not os.path.exists(yol):
            atlanan.append(k)
            continue
        with open(yol, encoding="utf-8") as f:
            spec = json.load(f)
        mod = sablon(spec)
        try:
            n = mod.uret(spec, os.path.join(KOK, k))
            print("%-44s %-11s %d kare + hikaye"
                  % (k, mod.__name__.replace("_html", ""), n))
            tamam += 1
        except Exception:
            hata.append(k)
            print("%-44s HATA" % k)
            traceback.print_exc()
    print("\n%d klasör basıldı." % tamam)
    if atlanan:
        print("spec.json yok: %s" % ", ".join(atlanan))
    if hata:
        print("hata veren: %s" % ", ".join(hata))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
