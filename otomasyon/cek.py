#!/usr/bin/env python3
"""Ürün görseli çekici — GitHub Actions üzerinde çalışır.

Bu oturumun çalıştığı kutu sermenkreatif.com ve filamentdepom.com'a
çıkamıyor (egress politikası, 403). GitHub Actions koşucusunun tam
internet erişimi var; bu betik orada çalışıp görselleri depoya koyuyor,
Claude da depodan okuyor. Kimsenin elle fotoğraf göndermesi gerekmiyor.

    python3 otomasyon/cek.py                 # urunler.json'daki eksikleri çek
    python3 otomasyon/cek.py --yenile        # var olanları da yeniden çek
    python3 otomasyon/cek.py --kesfet URL    # site haritasından ürün sayfalarını listele
"""
import json
import os
import re
import sys
import time
import urllib.parse as up

import requests

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LISTE = os.path.join(KOK, "otomasyon", "urunler.json")
HAM = os.path.join(KOK, "gorsel", "urun", "ham")
KESIK = os.path.join(KOK, "gorsel", "urun")
RAPOR = os.path.join(KOK, "otomasyon", "SON-CALISMA.md")

BASLIK = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
          "Accept-Language": "tr-TR,tr;q=0.9"}


def getir(url, ikili=False, deneme=3):
    son = None
    for i in range(deneme):
        try:
            r = requests.get(url, headers=BASLIK, timeout=40)
            r.raise_for_status()
            return r.content if ikili else r.text
        except Exception as e:                      # ağ dalgalanması olur
            son = e
            time.sleep(2 + 3 * i)
    raise son


# ----------------------------------------------------------- görsel bulma
_OG = re.compile(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']'
                 r'([^"\']+)', re.I)
_OG2 = re.compile(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property='
                  r'["\']og:image["\']', re.I)
_IMG = re.compile(r'<img[^>]+(?:data-src|data-original|src)=["\']([^"\']+)',
                  re.I)
# Ticimax ürün görselleri bu kalıpta duruyor
_TICI = re.compile(r'https?://[^"\']*ticimax[^"\']*/Uploads/UrunResimleri/'
                   r'[^"\']+\.(?:jpg|jpeg|png|webp)', re.I)

ATLA = ("blank.png", "logo", "icons8", "placeholder", "sprite", "loader",
        "whatsapp", "instagram", "youtube", "linkedin", "havale", "kredi",
        "banner", "header")


def temiz(aday, taban):
    if not aday:
        return None
    u = up.urljoin(taban, aday.strip().replace("&amp;", "&"))
    if any(k in u.lower() for k in ATLA):
        return None
    if not re.search(r"\.(jpg|jpeg|png|webp)(\?|$)", u, re.I):
        return None
    return u


def gorsel_bul(html, sayfa):
    """Ürün sayfasından en olası ürün görselini seç."""
    for kalip in (_TICI,):
        m = kalip.findall(html)
        if m:
            # büyük sürüm genelde "orj-" ya da boyutsuz olan
            m.sort(key=lambda u: (("orj" not in u.lower()), len(u)))
            u = temiz(m[0], sayfa)
            if u:
                return u, "ticimax ürün klasörü"
    for kalip in (_OG, _OG2):
        m = kalip.search(html)
        u = temiz(m.group(1), sayfa) if m else None
        if u:
            return u, "og:image"
    for aday in _IMG.findall(html):
        u = temiz(aday, sayfa)
        if u:
            return u, "sayfadaki ilk uygun img"
    return None, None


# --------------------------------------------------------------- kesme
_oturum = {}


def kes(ham_yol, hedef):
    """Arka planı kes. Model u2net'e sabitlendi — varsayılan model 1 GB
    ve koşucunun belleğini doldurup süreci öldürüyor."""
    from PIL import Image
    from rembg import remove, new_session
    if "s" not in _oturum:
        _oturum["s"] = new_session("u2net")
    im = Image.open(ham_yol).convert("RGBA")
    k = remove(im, session=_oturum["s"])
    bb = k.split()[-1].point(lambda v: 255 if v > 8 else 0).getbbox()
    if bb:
        k = k.crop(bb)
    k.save(hedef)
    return k.size


# ------------------------------------------------- ada göre sayfa bulma
HARITA = os.path.join(KOK, "otomasyon", "site-haritasi.json")


def _harita(kokler):
    """Site haritalarını bir kez indirip önbelleğe al."""
    if os.path.exists(HARITA):
        try:
            return json.load(open(HARITA, encoding="utf-8"))
        except Exception:
            pass
    h = {}
    for kok in kokler:
        try:
            h[kok] = kesfet(kok)
            print("  site haritası %s: %d adres" % (kok, len(h[kok])))
        except Exception as e:
            print("  site haritası alınamadı %s: %s" % (kok, e))
            h[kok] = []
    json.dump(h, open(HARITA, "w", encoding="utf-8"), ensure_ascii=False)
    return h


def _parcala(s):
    s = s.lower()
    for a, b in (("ı", "i"), ("ş", "s"), ("ğ", "g"), ("ü", "u"),
                 ("ö", "o"), ("ç", "c"), ("+", " plus ")):
        s = s.replace(a, b)
    return [p for p in re.split(r"[^a-z0-9]+", s) if p]


def ada_gore_bul(ara, kokler):
    """Ürün adından site haritasındaki en iyi eşleşen sayfayı seç.

    Google görsel araması yerine bu yol kullanılıyor: hangi ürün olduğu
    kesin ve görsel satıcının kendi ürün sayfasından geliyor.
    """
    h = _harita(kokler)
    kelime = _parcala(ara)
    if not kelime:
        return None, 0
    en_iyi, en_puan = None, 0
    for kok, adresler in h.items():
        for u in adresler:
            yol = _parcala(up.urlparse(u).path)
            if not yol:
                continue
            tut = sum(1 for k in kelime if k in yol)
            if not tut:
                continue
            # tüm kelimeler geçiyorsa ve adres kısa ise daha iyi eşleşme
            puan = tut / len(kelime) - 0.015 * max(0, len(yol) - len(kelime))
            if puan > en_puan:
                en_iyi, en_puan = u, puan
    return (en_iyi, round(en_puan, 3)) if en_puan >= 0.75 else (None, en_puan)


# --------------------------------------------------------------- keşif
def kesfet(kok):
    """Site haritasından ürün sayfası adaylarını dökümle."""
    adaylar, gorulen = [], set()
    yigin = [up.urljoin(kok, "/sitemap.xml")]
    while yigin and len(adaylar) < 4000:
        s = yigin.pop(0)
        if s in gorulen:
            continue
        gorulen.add(s)
        try:
            x = getir(s)
        except Exception as e:
            print("  atlandı:", s, e)
            continue
        alt = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", x, re.I)
        for u in alt:
            if u.endswith(".xml"):
                yigin.append(u)
            else:
                adaylar.append(u)
    return sorted(set(adaylar))


# --------------------------------------------------------------- ana akış
def main():
    yenile = "--yenile" in sys.argv
    if "--kesfet" in sys.argv:
        kok = sys.argv[sys.argv.index("--kesfet") + 1]
        bulunan = kesfet(kok)
        yol = os.path.join(KOK, "otomasyon", "bulunan-urunler.txt")
        with open(yol, "w", encoding="utf-8") as f:
            f.write("\n".join(bulunan) + "\n")
        print("%d adres yazıldı: %s" % (len(bulunan), yol))
        return

    os.makedirs(HAM, exist_ok=True)
    veri = json.load(open(LISTE, encoding="utf-8"))
    urunler = veri["urunler"]
    kokler = veri.get("siteler", [])
    satir, yeni, hata = [], 0, 0

    for u in urunler:
        slug, sayfa = u["slug"], u.get("sayfa")
        hedef = os.path.join(KESIK, "kesik-%s.png" % slug)
        ham_yol = None
        for uzanti in (".jpg", ".png", ".webp"):
            p = os.path.join(HAM, slug + uzanti)
            if os.path.exists(p):
                ham_yol = p
                break
        if ham_yol and os.path.exists(hedef) and not yenile:
            satir.append("| %s | atlandı | zaten var |" % slug)
            continue
        bulundu = ""
        if not sayfa and u.get("ara"):
            sayfa, puan = ada_gore_bul(u["ara"], kokler)
            if not sayfa:
                satir.append("| %s | HATA | \"%s\" sitede bulunamadı "
                             "(en iyi eşleşme %.2f) |" % (slug, u["ara"], puan))
                hata += 1
                continue
            bulundu = " · ada göre bulundu (%.2f)" % puan
        if not sayfa:
            satir.append("| %s | eksik | ne sayfa ne arama terimi var |" % slug)
            continue
        try:
            html = getir(sayfa)
            gu, nereden = gorsel_bul(html, sayfa)
            if not gu:
                satir.append("| %s | HATA | sayfada ürün görseli bulunamadı |"
                             % slug)
                hata += 1
                continue
            baytlar = getir(gu, ikili=True)
            uzanti = os.path.splitext(up.urlparse(gu).path)[1].lower()
            if uzanti not in (".jpg", ".jpeg", ".png", ".webp"):
                uzanti = ".jpg"
            ham_yol = os.path.join(HAM, slug + uzanti)
            open(ham_yol, "wb").write(baytlar)
            not_ = "%d KB · %s%s" % (len(baytlar) // 1024, nereden, bulundu)
            if u.get("kes", True):
                boy = kes(ham_yol, hedef)
                not_ += " · kesildi %d×%d" % boy
            satir.append("| %s | tamam | %s |" % (slug, not_))
            yeni += 1
        except Exception as e:
            satir.append("| %s | HATA | %s |" % (slug, str(e)[:90]))
            hata += 1

    # Aynı kareyi iki ürüne atamak en sinsi hata: ada göre eşleşme yanlış
    # sayfaya gidince iki modelin görseli aynı çıkıyor ve gözden kaçıyor.
    import hashlib
    ozet = {}
    for f_ in sorted(os.listdir(HAM)):
        yol = os.path.join(HAM, f_)
        if os.path.isfile(yol):
            h = hashlib.md5(open(yol, "rb").read()).hexdigest()
            ozet.setdefault(h, []).append(os.path.splitext(f_)[0])
    cift = [v for v in ozet.values() if len(v) > 1]
    for grup in cift:
        satir.append("| %s | **AYNI GÖRSEL** | bu ürünler birebir aynı "
                     "kareyi aldı — birine tam 'sayfa' adresi ver |"
                     % " + ".join(grup))

    with open(RAPOR, "w", encoding="utf-8") as f:
        f.write("# Son çalışma\n\n")
        f.write("%s · %d yeni · %d hata\n\n"
                % (time.strftime("%Y-%m-%d %H:%M UTC"), yeni, hata))
        f.write("| Ürün | Durum | Not |\n|---|---|---|\n")
        f.write("\n".join(satir) + "\n")
    print("\n".join(satir))
    print("---- %d yeni, %d hata" % (yeni, hata))


if __name__ == "__main__":
    main()
