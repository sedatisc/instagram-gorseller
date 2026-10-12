#!/usr/bin/env python3
"""Kategori sayfasındaki ürünleri çıkar — GitHub Actions üzerinde çalışır.

Neden ayrı bir betik: sermenkreatif.com'un kategori sayfaları tarayıcıda
doluyor. Ham HTML'de yalnız Handlebars şablonu (`{{name}}`) ve menü var,
ürün yok. Site haritasında da yalnız marka sayfaları geçiyor
(espressif-116, pixhawk-65 gibi), ürün sayfaları yok. Yani ürünlere tek
yol sayfayı gerçekten açmak.

    python3 otomasyon/kategori.py https://sermenkreatif.com/espressif-116
    python3 otomasyon/kategori.py <adres> --sayfa 4     # 4 sayfa gez

Sonuç `otomasyon/kategori-urunleri.json` içine yazılıyor:
{ "<kategori adresi>": { "<ürün adresi>": {"ad": ..., "fiyat": ...} } }
"""
import json
import os
import re
import sys
import urllib.parse as up

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIKTI = os.path.join(KOK, "otomasyon", "kategori-urunleri.json")

# Marka/kategori sayfaları da düz adreste duruyor ve sonları sayıyla
# bitiyor (espressif-116). Ürün adresleri böyle bitmiyor.
_KATEGORI = re.compile(r"-\d{1,3}$")
_ELE = ("sepet", "uyelik", "giris", "iletisim", "hakkimizda", "blog",
        "sozlesme", "kvkk", "gizlilik", "kargo", "iade", "stl-dunyasi")


def urunleri_al(sayfa_adresi, sayfa_sayisi=3, bekle=2500):
    from playwright.sync_api import sync_playwright

    kok = "%s://%s" % up.urlparse(sayfa_adresi)[:2]
    bulunan = {}
    with sync_playwright() as p:
        t = p.chromium.launch(args=["--no-sandbox"])
        sf = t.new_page(viewport={"width": 1400, "height": 2000},
                        locale="tr-TR")
        for no in range(1, sayfa_sayisi + 1):
            adres = sayfa_adresi if no == 1 else "%s?page=%d" % (sayfa_adresi,
                                                                 no)
            try:
                sf.goto(adres, wait_until="networkidle", timeout=60000)
            except Exception as e:
                print("  açılamadı: %s (%s)" % (adres, e))
                continue
            for _ in range(4):                     # tembel yüklenen liste
                sf.mouse.wheel(0, 4000)
                sf.wait_for_timeout(600)
            sf.wait_for_timeout(bekle)
            if no == 1:                        # ne gördüğümüzü kaydet
                tani = os.path.join(KOK, "otomasyon", "tani")
                os.makedirs(tani, exist_ok=True)
                sf.screenshot(path=os.path.join(tani, "kategori.png"),
                              full_page=False)
                govde = sf.evaluate("() => document.body.innerText")
                open(os.path.join(tani, "kategori.txt"), "w",
                     encoding="utf-8").write(govde[:6000])
            kayit = sf.evaluate("""() => {
                const out = [];
                document.querySelectorAll('a[href]').forEach(a => {
                    const ad = (a.innerText || '').replace(/\\s+/g, ' ').trim();
                    if (!ad || ad.length < 8 || ad.length > 160) return;
                    out.push({href: a.href, ad: ad});
                });
                return out;
            }""")
            onceki = len(bulunan)
            for k in kayit:
                tam = k["href"].split("#")[0].split("?")[0]
                if not tam.startswith(kok):
                    continue
                yol = up.urlparse(tam).path.strip("/")
                if not yol or "/" in yol or _KATEGORI.search(yol):
                    continue
                if any(e in yol for e in _ELE):
                    continue
                bulunan.setdefault(tam, {"ad": k["ad"]})
            print("  sayfa %d: %d yeni (toplam %d)"
                  % (no, len(bulunan) - onceki, len(bulunan)))
            if len(bulunan) == onceki and no > 1:   # yeni ürün gelmiyor
                break
        t.close()
    return bulunan


def main():
    arg = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not arg:
        raise SystemExit("kullanım: kategori.py <kategori adresi> [--sayfa N]")
    n = 3
    if "--sayfa" in sys.argv:
        n = int(sys.argv[sys.argv.index("--sayfa") + 1])
    hedef = arg[0]
    print("→ %s" % hedef)
    bulunan = urunleri_al(hedef, n)

    tum = {}
    if os.path.exists(CIKTI):
        try:
            tum = json.load(open(CIKTI, encoding="utf-8"))
        except Exception:
            pass
    tum[hedef] = bulunan
    json.dump(tum, open(CIKTI, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("%d ürün yazıldı: %s" % (len(bulunan), CIKTI))
    for u, k in list(bulunan.items())[:60]:
        print("  %-60s %s" % (k["ad"][:58], u.split("/")[-1]))
    return 0 if bulunan else 1


if __name__ == "__main__":
    sys.exit(main())
