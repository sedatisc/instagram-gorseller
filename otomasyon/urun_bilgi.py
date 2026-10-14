#!/usr/bin/env python3
"""Ürün sayfasından başlık, fiyat, özellik ve görselleri çıkar.

GitHub Actions üzerinde çalışır. Sayfalar tarayıcıda doluyor (Ticimax),
ham HTML'de ürün yok — o yüzden Playwright.

    python3 otomasyon/urun_bilgi.py <adres> [<adres> ...]

Yazdıkları:
    otomasyon/urun-bilgi.json      başlık, fiyat, özellik satırları, metin
    gorsel/urun/ham/<slug>.jpg     ürünün ana görseli
"""
import json
import os
import re
import sys
import urllib.parse as up

import requests

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIKTI = os.path.join(KOK, "otomasyon", "urun-bilgi.json")
HAM = os.path.join(KOK, "gorsel", "urun", "ham")

BASLIK = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def slug(adres):
    return up.urlparse(adres).path.strip("/").split("/")[-1]


def sayfayi_oku(sf, adres):
    sf.goto(adres, wait_until="networkidle", timeout=60000)
    for _ in range(3):
        sf.mouse.wheel(0, 2500)
        sf.wait_for_timeout(500)
    sf.wait_for_timeout(1500)
    return sf.evaluate("""() => {
        const al = s => {
            const e = document.querySelector(s);
            return e ? (e.innerText || '').replace(/\\s+/g, ' ').trim() : '';
        };
        const baslik = al('h1') || document.title;
        // fiyat: para birimi geçen en kısa metin
        let fiyat = '';
        document.querySelectorAll('span,div,p,strong,b').forEach(e => {
            const t = (e.innerText || '').trim();
            if (!t || t.length > 30) return;
            if (!/[₺]|TL/.test(t)) return;
            if (!/\\d/.test(t)) return;
            if (!fiyat || t.length < fiyat.length) fiyat = t;
        });
        // özellik tablosu
        const ozellik = [];
        document.querySelectorAll('table tr').forEach(tr => {
            const h = [...tr.querySelectorAll('th,td')]
                .map(c => (c.innerText || '').replace(/\\s+/g, ' ').trim());
            if (h.length === 2 && h[0] && h[1] && h[0].length < 60)
                ozellik.push(h);
        });
        // açıklama metni
        let metin = '';
        document.querySelectorAll(
            '[class*=aciklama],[class*=detay],[class*=description],[id*=detay]'
        ).forEach(e => {
            const t = (e.innerText || '').replace(/\\s+/g, ' ').trim();
            if (t.length > metin.length) metin = t;
        });
        // görseller
        const gorsel = [];
        document.querySelectorAll('img').forEach(i => {
            const s = i.currentSrc || i.src || '';
            if (!s || s.startsWith('data:')) return;
            if (i.naturalWidth < 300 || i.naturalHeight < 300) return;
            if (!gorsel.includes(s)) gorsel.push(s);
        });
        return {baslik, fiyat, ozellik, metin: metin.slice(0, 4000), gorsel};
    }""")


def indir(url, hedef):
    r = requests.get(url, headers=BASLIK, timeout=60)
    r.raise_for_status()
    with open(hedef, "wb") as f:
        f.write(r.content)
    return len(r.content)


def main():
    adresler = [a for a in sys.argv[1:] if a.startswith("http")]
    if not adresler:
        raise SystemExit("kullanım: urun_bilgi.py <ürün adresi> ...")
    os.makedirs(HAM, exist_ok=True)
    from playwright.sync_api import sync_playwright

    tum = {}
    if os.path.exists(CIKTI):
        try:
            tum = json.load(open(CIKTI, encoding="utf-8"))
        except Exception:
            pass

    with sync_playwright() as p:
        t = p.chromium.launch(args=["--no-sandbox"])
        sf = t.new_page(viewport={"width": 1400, "height": 1800},
                        locale="tr-TR")
        for adres in adresler:
            s = slug(adres)
            print("→ %s" % s)
            try:
                v = sayfayi_oku(sf, adres)
            except Exception as e:
                print("   HATA: %s" % e)
                continue
            v["adres"] = adres
            v["slug"] = s
            print("   başlık : %s" % v["baslik"][:90])
            print("   fiyat  : %s" % (v["fiyat"] or "—"))
            print("   özellik: %d satır · görsel: %d"
                  % (len(v["ozellik"]), len(v["gorsel"])))
            for k, d in v["ozellik"][:12]:
                print("      %-28s %s" % (k[:28], d[:50]))
            # Ürün görseli /urunresimleri/ altında; ilk sıradaki çoğu
            # zaman sitenin üst banner'ı (HeaderTasarim) oluyor.
            # "tr.jpg" sitenin "görsel yok" yer tutucusu (329x454). Ürün
            # fotoğrafı sanıp gönderiye koyunca kamera simgesi basılıyordu.
            v["gorsel"] = [g for g in v["gorsel"]
                           if not g.rsplit("/", 1)[-1].lower()
                           .startswith(("tr.jpg", "nophoto", "no-image"))]
            if not v["gorsel"]:
                print("   ! ÜRÜN FOTOĞRAFI YOK — sayfada yer tutucu var")
            aday = [g for g in v["gorsel"] if "urunresimleri" in g.lower()] \
                or [g for g in v["gorsel"]
                    if "headertasarim" not in g.lower()] or v["gorsel"]
            v["gorsel"] = aday + [g for g in v["gorsel"] if g not in aday]
            if v["gorsel"]:
                # Ticimax CDN'i genişliği adreste taşıyor; 698 yerine 1600
                # isteyip kapak için yeterli çözünürlük alıyoruz.
                v["gorsel"][0] = re.sub(r"/width=\d+,", "/width=1600,",
                                        v["gorsel"][0])
                uz = os.path.splitext(up.urlparse(v["gorsel"][0]).path)[1]
                uz = uz if uz.lower() in (".jpg", ".jpeg", ".png", ".webp") \
                    else ".jpg"
                hedef = os.path.join(HAM, s + uz)
                try:
                    boy = indir(v["gorsel"][0], hedef)
                    print("   görsel indi: %s (%.0f KB)" % (hedef, boy / 1024))
                except Exception as e:
                    print("   görsel inmedi: %s" % e)
            tum[adres] = v
        t.close()

    json.dump(tum, open(CIKTI, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("yazıldı: %s" % CIKTI)
    return 0


if __name__ == "__main__":
    sys.exit(main())
