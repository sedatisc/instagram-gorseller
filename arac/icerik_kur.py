#!/usr/bin/env python3
"""icerik.json'u bir kere kurar: eski DURUM.json + klasörler.

Eski yapıda her gönderinin elle tutulan bir gün numarası vardı. Numara
kaydıkça aynı iş iki kere planlanıyor, elle paylaşılan iş kuyrukta kalıyor,
aksayan gün sessizce düşüyordu. Yeni yapıda gönderinin tarihi yok: hazır
işler sırayla takvime diziliyor, tarih konumdan çıkıyor.

    python3 arac/icerik_kur.py
"""
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Eski slot adları -> yeni kategori adları
KATEGORI = {"3dbaski": "rehber", "baski": "baski",
            "urun": "magaza", "proje": "proje",
            "elektronik": "kapali"}

# Aynı konunun iki klasörü varsa ikisi de bu anahtara bağlanıyor;
# plan aynı konuyu iki kere dizmiyor.
KONU = {
    "2026-10-06-bambu-r1-lazer": "bambu-r1",
    "2026-10-10-bambu-r1-tanitim": "bambu-r1",
    "2026-10-17-polymaker-ht-pla": "ht-pla",
    "2026-10-19-ht-pla-pano": "ht-pla",
    "2026-10-14-sunlu-filadryer": "filament-kurutucu",
    "2026-10-18-filament-kurutucu-pano": "filament-kurutucu",
    "2026-10-16-sunlu-filament-pano": "sunlu-filament",
    "2026-10-11-sunlu-pla-kartelasi": "sunlu-filament",
    "2026-10-21-ams-israf": "renk-degisimi",
    "2026-10-21-u1-k3-pano": "renk-degisimi",
    "2026-10-17-cok-renkli-yazici-pano": "cok-renkli-yazici",
}


def konu(klasor):
    if klasor in KONU:
        return KONU[klasor]
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", klasor)


def kareli(klasor):
    yol = os.path.join(KOK, klasor)
    if not os.path.isdir(yol):
        return 0
    return len([f for f in os.listdir(yol)
                if f[:-4].isdigit() and f.endswith(".jpg")])


def main():
    eski = json.load(open(os.path.join(KOK, "DURUM.json"), encoding="utf-8"))
    kb = eski["kuyruk_bekleyen"]

    durum, neden, kategori = {}, {}, {}

    for g in eski.get("gecmis", []):
        k = g.get("klasor")
        if k:
            durum[k] = ("yayinlandi", g.get("tarih", ""))
            kategori.setdefault(k, KATEGORI.get(g.get("slot"), ""))
    for g in eski.get("yayinlanmis_disarida", []):
        k = g.get("klasor") if isinstance(g, dict) else g
        if k:
            durum[k] = ("yayinlandi", (g or {}).get("tarih", "")
                        if isinstance(g, dict) else "")
    for b in kb.get("beklemede", []):
        durum[b["klasor"]] = ("beklemede", "")
        neden[b["klasor"]] = b.get("neden", "")
    for i in kb.get("iptal", []):
        durum[i["klasor"]] = ("iptal", "")
        neden[i["klasor"]] = i.get("sebep", "")[:160]
    for c in kb.get("kuyruktan_cikan", []):
        k = c.get("klasor") if isinstance(c, dict) else c
        if k and k not in durum:
            durum[k] = ("beklemede", "")
            neden[k] = "Elektronik kategorisi kapandı"
    for s in kb.get("slotlar", []):
        kategori[s["klasor"]] = KATEGORI.get(s["slot"], "")
        durum.setdefault(s["klasor"], ("hazir", ""))

    reels = {r["klasor"] for r in kb.get("reels", [])}

    # Klasörlerden kategori tamamlama: kuyruğa hiç girmemiş olanlar da
    # listeye girsin, kaybolmasın.
    for k in sorted(os.listdir(KOK)):
        if not (k.startswith("2026-") and os.path.isdir(os.path.join(KOK, k))):
            continue
        sp = os.path.join(KOK, k, "spec.json")
        if k not in kategori and os.path.exists(sp):
            try:
                kat = json.load(open(sp, encoding="utf-8")).get("kategori", "")
            except Exception:
                kat = ""
            kategori[k] = {"3dbaski": "rehber", "elektronik": "kapali",
                           "kurumsal": "magaza"}.get(kat, "")
        durum.setdefault(k, ("hazir", ""))

    icerik = []
    for k in sorted(durum):
        d, t = durum[k]
        kat = kategori.get(k, "")
        n = kareli(k)
        if d == "hazir" and (not kat or not n):
            # Kategorisi ya da karesi olmayan iş plana giremez; arşivde
            # durup gözden kaçmasın diye sebebi yazılıyor.
            d = "beklemede"
            neden.setdefault(k, "kategori yok" if not kat else "kare yok")
        kayit = {"klasor": k, "kategori": kat, "konu": konu(k),
                 "durum": d, "kare": n}
        if k in reels:
            kayit["reels"] = True
        if t:
            kayit["tarih"] = t
        if neden.get(k):
            kayit["neden"] = neden[k]
        icerik.append(kayit)

    kampanya = [dict(k) for k in kb.get("kampanya", [])]

    yeni = {
        "surum": 2,
        "not": ("Tek kaynak. Her gönderi burada bir satır; gün numarası "
                "tutulmuyor. Takvim, durumu 'hazir' olan işlerin "
                "kategorisindeki sırasından çıkıyor — iş aksarsa kaybolmaz, "
                "bir gün kayar. Durum: hazir | yayinlandi | beklemede | iptal."),
        "kategori_sirasi": ["rehber", "baski", "magaza", "proje"],
        "icerik": icerik,
        "kampanya": kampanya,
    }
    yol = os.path.join(KOK, "icerik.json")
    json.dump(yeni, open(yol, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    say = {}
    for i in icerik:
        say[i["durum"]] = say.get(i["durum"], 0) + 1
    print(yol)
    print("toplam %d kayıt: %s" % (len(icerik), say))
    for kat in yeni["kategori_sirasi"]:
        h = [i for i in icerik if i["durum"] == "hazir" and i["kategori"] == kat]
        print("  %-8s hazır %d" % (kat, len(h)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
