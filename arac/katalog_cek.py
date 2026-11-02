#!/usr/bin/env python3
"""Mağazadaki baskı ürünlerini tarayıp urunler.json'u yeniliyor.

Site haritasından baskı kategorilerini, kategorilerden ürün sayfalarını,
ürün sayfalarından da Product verisini (ad, açıklama, fiyat, görseller)
okuyor. Stokta olmayan ürün katalogdan düşüyor.

İnternet gerekiyor; GitHub Actions'ta çalışıyor.

    python3 arac/katalog_cek.py            # katalogu yenile
    python3 arac/katalog_cek.py --kuru     # yalnız say, dosyaya yazma
"""
import concurrent.futures as cf
import html as H
import json
import os
import re
import sys
import urllib.request

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://sermenkreatif.com"
KATALOG = os.path.join(KOK, "urunler.json")
AJAN = {"User-Agent": "sermenkreatif-yayin/1.0"}


def al(yol):
    r = urllib.request.Request(SITE + yol, headers=AJAN)
    return urllib.request.urlopen(r, timeout=60).read().decode("utf-8",
                                                               "replace")


def kategoriler():
    h = al("/")
    return sorted(set(re.findall(r'href="/kategori/(baski-[^"?]+)"', h)))


def kategori_urunleri(kat):
    try:
        h = al("/kategori/" + kat)
    except Exception:
        return kat, []
    return kat, sorted(set(re.findall(r'href="/urun/([^"?]+)"', h)))


def urun(slug):
    try:
        h = al("/urun/" + slug)
    except Exception:
        return slug, None
    for m in re.finditer(
            r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S):
        try:
            j = json.loads(m.group(1))
        except Exception:
            continue
        for o in (j if isinstance(j, list) else [j]):
            if not (isinstance(o, dict) and o.get("@type") == "Product"):
                continue
            im = o.get("image") or []
            im = [im] if isinstance(im, str) else list(im)
            gor = [x.rsplit("/", 1)[-1].rsplit(".", 1)[0] for x in im]
            of = o.get("offers") or {}
            if isinstance(of, list):
                of = of[0] if of else {}
            if "InStock" not in (of.get("availability") or "InStock"):
                return slug, None
            ac = H.unescape(re.sub("<[^>]+>", " ", o.get("description") or ""))
            return slug, {"ad": o.get("name", ""),
                          "aciklama": re.sub(r"\s+", " ", ac).strip()[:200],
                          "fiyat": str(of.get("price", "")),
                          "gorsel": gor[:8]}
    return slug, None


def main():
    kuru = "--kuru" in sys.argv
    kats = kategoriler()
    print("baskı kategorisi: %d" % len(kats))
    esle = {}
    with cf.ThreadPoolExecutor(10) as ex:
        for kat, lst in ex.map(kategori_urunleri, kats):
            for s in lst:
                esle.setdefault(s, kat)
    print("ürün sayfası: %d" % len(esle))

    yeni = {}
    with cf.ThreadPoolExecutor(10) as ex:
        for s, v in ex.map(urun, list(esle)):
            if v and v["gorsel"]:
                v["kat"] = esle[s]
                yeni[s] = v
    print("görselli ve stokta: %d" % len(yeni))

    if kuru:
        return 0
    eski = {}
    if os.path.exists(KATALOG):
        with open(KATALOG, encoding="utf-8") as f:
            eski = json.load(f).get("urun", {})
    with open(KATALOG, "w", encoding="utf-8") as f:
        json.dump({"not": ("Mağaza baskı ürünleri. sermenkreatif.com ürün "
                           "sayfalarındaki Product verisinden alındı; "
                           "arac/katalog_cek.py yeniliyor. Gönderi metni ve "
                           "görselleri bu dosyadan üretiliyor."),
                   "kaynak": SITE, "urun": yeni}, f,
                  ensure_ascii=False, indent=1)
    print("eklenen: %d · düşen: %d"
          % (len(set(yeni) - set(eski)), len(set(eski) - set(yeni))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
