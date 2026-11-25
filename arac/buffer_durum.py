#!/usr/bin/env python3
"""Buffer'daki gönderilerin durumunu okuyor. Hiçbir şey göndermiyor.

Defterdeki (otomasyon/buffer-defter.json) son kayıtların Buffer'daki
hâlini soruyor: yayınlandı mı, hata mı aldı, hâlâ kuyrukta mı. Şema
alan adlarını bilmediğimiz için önce introspection ile Query ve Post
alanları yazdırılıyor, sonra bulunan alana göre sorgu atılıyor.

    python3 arac/buffer_durum.py            # son 12 kaydı sor
    python3 arac/buffer_durum.py 2026-11-25 # o günün kayıtlarını sor
"""
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "otomasyon"))

import buffer_gonder as B                                  # noqa: E402

DEFTER = os.path.join(KOK, "otomasyon", "buffer-defter.json")


def alanlar(tur):
    try:
        d = B._sorgu('query T($n: String!) { __type(name: $n) '
                     '{ fields { name type { name kind ofType '
                     '{ name kind } } } } }', {"n": tur})
    except Exception as e:
        return [], str(e)
    t = d.get("__type") or {}
    return [f["name"] for f in (t.get("fields") or [])], ""


def kok_alanlar():
    d = B._sorgu("query { __schema { queryType { fields { name args "
                 "{ name type { name kind ofType { name } } } } } } }")
    f = ((d.get("__schema") or {}).get("queryType") or {}).get("fields") or []
    return f


def defter_kayitlari(gun=None):
    with open(DEFTER, encoding="utf-8") as f:
        g = json.load(f).get("gonderilen", [])
    if gun:
        g = [x for x in g if x.get("zaman", "").startswith(gun)]
    return g[-12:]


def main():
    gun = sys.argv[1] if len(sys.argv) > 1 else None
    kayit = defter_kayitlari(gun)
    print("Sorulacak kayit: %d" % len(kayit))
    for x in kayit:
        print("  %s  %s  %s" % (x.get("zaman"), x.get("buffer"),
                                x.get("anahtar")))

    print("\n--- Query alanlari ---")
    for f in kok_alanlar():
        print("  %s(%s)" % (f["name"], ", ".join(a["name"]
                                                 for a in f.get("args") or [])))

    ad, _ = alanlar("Post")
    print("\n--- Post alanlari ---\n  " + ", ".join(ad))

    try:
        d = B._sorgu('query T($n: String!) { __type(name: $n) '
                     '{ inputFields { name type { name kind ofType '
                     '{ name } } } } }', {"n": "PostInput"})
        girdi = [f["name"]
                 for f in ((d.get("__type") or {}).get("inputFields") or [])]
    except Exception as e:
        girdi = ["(okunamadi: %s)" % e]
    print("\n--- PostInput alanlari ---\n  " + ", ".join(girdi))

    hata_ad, _ = alanlar("PostPublishingError")
    print("\n--- PostPublishingError alanlari ---\n  " + ", ".join(hata_ad))

    # Gönderinin medyası: Buffer'a hangi adresi verdiğimizi görmek için.
    varlik_tur = ""
    try:
        d = B._sorgu('query { __type(name: "Post") { fields { name type '
                     '{ name kind ofType { name kind ofType '
                     '{ name kind ofType { name } } } } } } }')
        for f in ((d.get("__type") or {}).get("fields") or []):
            if f["name"] != "assets":
                continue
            t = f["type"]
            while t and not t.get("name"):
                t = t.get("ofType")
            varlik_tur = (t or {}).get("name") or ""
    except Exception as e:
        print("varlik turu okunamadi: %s" % e)
    varlik_ad = []
    if varlik_tur:
        varlik_ad, _ = alanlar(varlik_tur)
        print("\n--- %s alanlari ---\n  %s" % (varlik_tur,
                                               ", ".join(varlik_ad)))

    sec = [a for a in ("id", "status", "dueAt", "sentAt",
                       "notificationStatus", "schedulingType", "sharedNow",
                       "shareMode", "channelId") if a in ad]
    if "error" in ad and hata_ad:
        sec.append("error { %s }" % " ".join(hata_ad))
    varlik_sec = [a for a in ("id", "mimeType", "source", "thumbnail",
                              "url", "type") if a in varlik_ad]
    if varlik_sec:
        sec.append("assets { %s }" % " ".join(varlik_sec))

    print("\n--- Gonderi durumlari ---")
    for x in kayit:
        try:
            d = B._sorgu("query P($i: PostInput!) { post(input: $i) { %s } }"
                         % " ".join(sec), {"i": {"id": x["buffer"]}})
            print("  %s\n    %s" % (x["anahtar"], json.dumps(
                d.get("post"), ensure_ascii=False)))
        except Exception as e:
            print("  %s -> SORGU HATASI: %s" % (x["anahtar"], e))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
