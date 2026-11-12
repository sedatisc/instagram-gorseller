#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Önümüzdeki haftayı onaya kilitler.

Plan her yayından sonra kendini yeniden türetiyor: bir iş yayınlanınca
sıradaki işler kayıyor, onaylanan hafta elde kalmıyordu. Bu araç o anki
sırayı alıp otomasyon/hafta-kilit.json'a yazıyor; kilitli günler bir daha
kıpırdamıyor, sıra yalnız kilitten sonraki günleri doldurmaya devam
ediyor. Stoktan düşen ürün kilitli günde de atlanıyor — satılmayan ürün
paylaşılmıyor.

Kullanım:
    python3 arac/hafta_kilitle.py [gün sayısı]      # varsayılan 8

Bugünün slotları gece yarısı Buffer'a gittiği için kilit yarından
başlıyor.
"""
import json
import os
import sys
from datetime import date, timedelta

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)

import sira  # noqa: E402

HEDEF = os.path.join(KOK, "otomasyon", "hafta-kilit.json")
NOT = ("Onaylanmış günler. Buradaki gün plandan çıkmaz, sırası kaymaz. "
       "Stoktan düşen ürün yine atlanır. Hafta onaylanınca "
       "arac/hafta_kilitle.py ile yenilenir.")


def main():
    adet = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    _, slotlar = sira.kuyruk()
    bugun = date.today()
    bug_s = bugun.isoformat()
    gunler = sorted({s["tarih"] for s in slotlar if s["tarih"] >= bug_s})
    kilit = {}
    for n, t in enumerate(gunler[:adet]):
        yeni = (bugun + timedelta(days=n + 1)).isoformat()
        kilit[yeni] = [
            {"slot": s["slot"], "klasor": s["klasor"]}
            for s in sorted((x for x in slotlar if x["tarih"] == t),
                            key=lambda x: x["slot"])]
    with open(HEDEF, "w", encoding="utf-8") as f:
        json.dump({"not": NOT, "gunler": kilit}, f,
                  ensure_ascii=False, indent=1)
    for t in sorted(kilit):
        print(t, "·", ", ".join(s["klasor"] for s in kilit[t]))
    print("\n%d gün kilitlendi: %s" % (len(kilit), HEDEF))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
