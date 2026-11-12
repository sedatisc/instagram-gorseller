#!/usr/bin/env python3
"""Mağaza ürün kataloğu — gönderiler buradan kuruluyor.

Baskı ürünü gönderileri artık klasörden değil, sitedeki ürünün
kendisinden geliyor: ad, açıklama, fiyat ve görseller sermenkreatif.com
ürün sayfasındaki Product verisinden alınıyor. Katalog `urunler.json`
içinde duruyor; `arac/katalog_cek.py` siteyi tarayıp onu yeniliyor.

Gönderi metni de buradan üretiliyor. Elle yazılmış metin.md yok: ürün
sayfası değişince gönderi metni de değişiyor.
"""
import json
import os

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KATALOG = os.path.join(KOK, "urunler.json")
SITE = "https://sermenkreatif.com"
ONEK = "urun/"                      # icerik.json'daki sanal klasör öneki

# Kategori -> gönderi metninde kullanılacak etiketler. Jenerik etiket
# erişime katkı vermiyor, o yüzden ürüne özel olanlar seçiliyor.
ETIKET = {
    "anahtarlik": ["anahtarlik", "cantasusu"],
    "aski": ["duvaraskisi", "portmanto"],
    "ayakkabilik": ["ayakkabilik", "antredüzeni"],
    "banyo-askisi": ["havluaskisi", "banyoduzeni"],
    "banyo-duzenleyici": ["banyoduzenleyici", "banyoduzeni"],
    "bebek-ve-aktivite-oyuncaklari": ["egiticioyuncak", "aktiviteoyuncagi"],
    "boyama-seti": ["boyamaseti", "cocuketkinligi"],
    "buzdolabi-duzenleyici": ["buzdolabiduzenleyici", "mutfakduzeni"],
    "camasirlik-gerecleri": ["camasirodasi", "evduzeni"],
    "cupcake-standi": ["sunumstandi", "pastastandi"],
    "dekoratif-obje-ve-biblo": ["dekoratifobje", "evdekorasyonu"],
    "dekoratif-tabak-ve-kase": ["sunumtabagi", "dekoratifkase"],
    "dis-fircalik": ["disfircaligi", "banyoduzeni"],
    "duvar-rafi": ["duvarrafi", "evdekorasyonu"],
    "egitici-oyuncak": ["egiticioyuncak", "cocukgelisimi"],
    "fotograf-albumu": ["fotografcercevesi", "anidefteri"],
    "kablo-duzenleyici": ["kabloduzenleyici", "masaduzeni"],
    "kalemlik-ataslik": ["kalemlik", "masaduzeni"],
    "kapi-stoperi": ["kapistoperi", "evduzeni"],
    "kasiklik": ["kasiklik", "mutfakduzeni"],
    "kedi-aksesuari": ["kediaksesuari", "kedili"],
    "kedi-ve-kopek-mama-su-kabi": ["mamakabi", "kedikopek"],
    "kulaklik-aksesuari": ["kulaklikstandi", "masaduzeni"],
    "kutu-oyunu": ["kutuoyunu", "masaoyunu"],
    "makyaj-ve-taki-organizeri": ["makyajorganizeri", "takiduzenleyici"],
    "masa-ve-gece-lambasi": ["gecelambasi", "evdekorasyonu"],
    "masaustu-organizer": ["masaustuduzenleyici", "masaduzeni"],
    "monitor-aparati": ["monitoryukseltici", "masaduzeni"],
    "mutfak-duzenleyici": ["mutfakduzenleyici", "mutfakduzeni"],
    "notebook-standi": ["laptopstandi", "masaduzeni"],
    "oyuncak-araba": ["oyuncakaraba", "cocukoyuncagi"],
    "pecetelik": ["pecetelik", "masadekoru"],
    "portmanto": ["portmanto", "antredüzeni"],
    "puzzle": ["yapboz", "egiticioyuncak"],
    "sabunluk": ["sabunluk", "banyoduzeni"],
    "saklama-kutusu": ["saklamakutusu", "evduzeni"],
    "saksi": ["saksi", "bitkisever"],
    "samdan-mumluk": ["mumluk", "evdekorasyonu"],
    "suzgec": ["mutfakgereci", "mutfakduzeni"],
    "tablet-standi": ["tabletstandi", "masaduzeni"],
    "tepsi": ["dekoratiftepsi", "evdekorasyonu"],
    "tuvalet-kagitligi": ["tuvaletkagitligi", "banyoduzeni"],
    "urunleri": ["3dbaskiurun", "evdekorasyonu"],
    "vazo": ["dekoratifvazo", "evdekorasyonu"],
    "yilbasi-agaci": ["yilbasiagaci", "yilbasi"],
    "yilbasi-susu": ["yilbasisusu", "yilbasi"],
}

# Kategori -> gönderiyi kime yollatacağımız. Gönderim, takipçi olmayana
# ulaşmada en ağır sinyal; cümle ürüne göre değişiyor.
YOLLA = {
    "bebek-ve-aktivite-oyuncaklari": "Küçük çocuğu olan bir arkadaşına yolla.",
    "egitici-oyuncak": "Küçük çocuğu olan bir arkadaşına yolla.",
    "boyama-seti": "Çocuğuyla vakit geçiren bir arkadaşına yolla.",
    "puzzle": "Yapboz seven bir arkadaşına yolla.",
    "oyuncak-araba": "Küçük çocuğu olan bir arkadaşına yolla.",
    "kutu-oyunu": "Oyun gecesi kurduğun arkadaşına yolla.",
    "kedi-aksesuari": "Kedisi olan bir arkadaşına yolla.",
    "kedi-ve-kopek-mama-su-kabi": "Kedisi ya da köpeği olan birine yolla.",
    "saksi": "Evi bitki dolu olan arkadaşına yolla.",
    "cupcake-standi": "Pasta yapan arkadaşına yolla.",
    "dekoratif-tabak-ve-kase": "Misafir ağırlamayı seven birine yolla.",
    "pecetelik": "Masasını toplamayı seven birine yolla.",
    "yilbasi-agaci": "Yılbaşı hazırlığına başlayan arkadaşına yolla.",
    "yilbasi-susu": "Yılbaşı hazırlığına başlayan arkadaşına yolla.",
    "masaustu-organizer": "Masası dağınık olan arkadaşına yolla.",
    "kalemlik-ataslik": "Masası dağınık olan arkadaşına yolla.",
    "monitor-aparati": "Evden çalışan bir arkadaşına yolla.",
    "notebook-standi": "Evden çalışan bir arkadaşına yolla.",
}
YOLLA_GENEL = "Evini toplamayı seven bir arkadaşına bu gönderiyi yolla."


def oku():
    try:
        with open(KATALOG, encoding="utf-8") as f:
            return json.load(f).get("urun", {})
    except Exception:
        return {}


def slug(klasor):
    return klasor[len(ONEK):] if klasor.startswith(ONEK) else None


def kayit(klasor):
    s = slug(klasor)
    return oku().get(s) if s else None


def gorseller(klasor):
    """Gönderi kareleri, akışa göre sıralı.

    Sitedeki ilk görsel pazaryeri bilgi kartı: başlık, detay kutuları ve
    ölçü çizimi. Akışta ilan gibi duruyor, durdurmuyor. İkinci görsel
    ürünün kendi ortamındaki fotoğrafı; kapakta o duruyor. Bilgi kartı
    ikinci kareye geçiyor, kalan kareler sırasını koruyor."""
    k = kayit(klasor)
    if not k:
        return []
    g = list(k.get("gorsel", []))
    if len(g) > 1:
        g[0], g[1] = g[1], g[0]
    return ["%s/media/urun/%s.webp" % (SITE, u) for u in g]


def sayfa(klasor):
    s = slug(klasor)
    return "%s/urun/%s" % (SITE, s) if s else ""


def ad(klasor):
    k = kayit(klasor)
    return k.get("ad", "") if k else ""


def fiyat(klasor):
    k = kayit(klasor)
    if not k or not k.get("fiyat"):
        return ""
    try:
        f = float(k["fiyat"])
    except ValueError:
        return ""
    tam, kurus = divmod(round(f * 100), 100)
    return "%s,%02d ₺" % ("{:,}".format(tam).replace(",", "."), kurus)


def metin(klasor):
    """Gönderi metni. Ürün sayfasındaki veriden kuruluyor."""
    k = kayit(klasor)
    if not k:
        return "", ""
    kat = k.get("kat", "").replace("baski-", "")
    p = [k.get("ad", "")]
    if k.get("aciklama"):
        p.append(k["aciklama"])
    f = fiyat(klasor)
    p.append("Atölyemizde PLA filament ile basılıyor. Katman dokusu 3D "
             "baskının kendi dokusu; renk seçenekleri için yazabilirsin.")
    p.append("Faturalı satış, Samsun'dan kargo." + (" %s." % f if f else ""))
    p.append("Ürün sayfası: " + sayfa(klasor).replace("https://", ""))
    p.append(YOLLA.get(kat, YOLLA_GENEL))
    et = ["#sermenkreatif", "#3dbaski"] + \
         ["#" + x for x in ETIKET.get(kat, ["3dbaskiurun", "evdekorasyonu"])]
    p.append(" ".join(et[:5]))
    return "\n\n".join(x for x in p if x), ""
