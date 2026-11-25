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

    for tur in ("Post", "PostStatus", "PostError"):
        ad, hata = alanlar(tur)
        print("\n--- %s alanlari --- %s" % (tur, hata))
        print("  " + ", ".join(ad))

    # Tek tek sorma: şemada post(id:) varsa onu kullanıyoruz.
    kokler = {f["name"]: [a["name"] for a in f.get("args") or []]
              for f in kok_alanlar()}
    if "post" in kokler:
        ad, _ = alanlar("Post")
        sec = [a for a in ("id", "status", "dueAt", "sentAt", "error",
                           "errorMessage", "channelId", "text")
               if a in ad]
        print("\n--- Gonderi durumlari (%s) ---" % ", ".join(sec))
        for x in kayit:
            try:
                d = B._sorgu("query P($i: PostId!) { post(id: $i) { %s } }"
                             % " ".join(sec), {"i": x["buffer"]})
                print("  %s -> %s" % (x["anahtar"], json.dumps(
                    d.get("post"), ensure_ascii=False)))
            except Exception as e:
                print("  %s -> SORGU HATASI: %s" % (x["anahtar"], e))
    else:
        print("\nSemada post(id:) yok; yukaridaki Query alanlarindan "
              "uygun olani secip sorgu yazilacak.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
