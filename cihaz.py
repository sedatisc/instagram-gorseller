#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cihaz kaydından gönderi üretir: spec.json + metin.md.

Kullanım:
  python3 cihaz.py cihazlar/bambu-lab/x2d.json 2026-10-14-bambu-x2d
  python3 cihaz.py --sira                  # yayın sırasını yazdır
  python3 cihaz.py --foto                  # eksik fotoğraf listesi

Kapak `urun` tipinde, yani gerçek fotoğraf istiyor. Fotoğraf
`gorsel/cihaz/<marka>-<model>.jpg` yolunda aranıyor; yoksa üretici
kareye "FOTOĞRAF YOK" basıp uyarı veriyor (bkz. gorsel/BENIOKU.md).
"""
import glob
import json
import zlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# markaya göre kategori ve zemin — arka arkaya aynı görünmesin
KATEGORI = {"Recine": "3dbaski", "FDM": "3dbaski",
            "Lazer": "proje", "CNC": "proje", "Cok islevli": "proje"}
ZEMIN = ["koyu", "indigo", "kobalt", "okyanus", "orman", "mor", "kiraz", "acik"]


def kisalt(s, n):
    """n karakteri aşarsa kelime sınırında kes."""
    s = (s or "").strip()
    if len(s) <= n:
        return s
    kes = s[:n]
    bosluk = kes.rfind(" ")
    if bosluk > n * 0.6:
        kes = kes[:bosluk]
    return kes.rstrip(" ,;·—-") + "…"


def satir_ekle(satirlar, etiket, deger, sinir=30):
    if deger:
        satirlar.append([etiket, kisalt(str(deger), sinir)])


def ozet_serit(c):
    """Kapaktaki 3 gözlü künye — cihaz tipine göre en çarpıcı üç rakam."""
    oz = []
    if c["tip"] == "Recine":
        satir_ekle(oz, "ALAN", (c.get("alan") or "").split("(")[0].strip(), 18)
        ekran = (c.get("ekran_cozunurluk") or "").split(",")[0]
        satir_ekle(oz, "EKRAN", ekran, 14)
        satir_ekle(oz, "HIZ", c.get("hiz"), 14)
    elif c["tip"] == "Cok islevli":
        satir_ekle(oz, "BASKI", (c.get("alan") or "").split("(")[0].strip(), 18)
        satir_ekle(oz, "LAZER", (c.get("lazer") or "").split(",")[0], 14)
        satir_ekle(oz, "CNC", (c.get("cnc") or "").split(",")[0], 14)
    else:
        satir_ekle(oz, "ALAN", (c.get("alan") or "").split("(")[0].strip(), 18)
        satir_ekle(oz, "HIZ", (c.get("hiz") or "").split("(")[0].strip(), 14)
        satir_ekle(oz, "NOZUL", c.get("nozul_sicaklik"), 12)
    return [o for o in oz if o][:3]


def kunye_tablosu(c):
    s = []
    satir_ekle(s, "BASKI ALANI", c.get("alan"), 30)
    if c["tip"] == "Recine":
        satir_ekle(s, "EKRAN", c.get("ekran_cozunurluk"), 34)
        satir_ekle(s, "HIZ", c.get("hiz"), 28)
    else:
        satir_ekle(s, "HIZ", c.get("hiz"), 28)
        satir_ekle(s, "İVME", c.get("ivme"), 20)
        satir_ekle(s, "EKSTRUDER", c.get("ekstruder"), 32)
        satir_ekle(s, "NOZUL / TABLA", "%s / %s" % (
            c.get("nozul_sicaklik") or "?", c.get("tabla_sicaklik") or "?"), 24)
    satir_ekle(s, "LAZER", c.get("lazer"), 30)
    satir_ekle(s, "CNC", c.get("cnc"), 30)
    return s[:6]


def masa_tablosu(c):
    s = []
    satir_ekle(s, "CİHAZ ÖLÇÜSÜ", c.get("olcu"), 28)
    satir_ekle(s, "AĞIRLIK", c.get("agirlik"), 18)
    satir_ekle(s, "GÜÇ", c.get("guc"), 26)
    satir_ekle(s, "KAPALI KABİN", {True: "var", False: "yok"}.get(
        c.get("kapali_kabin")), 18)
    satir_ekle(s, "ÇOK RENK", c.get("cok_renk"), 30)
    satir_ekle(s, "BAĞLANTI", c.get("baglanti"), 30)
    return s[:6]


def spec_uret(c, zemin):
    marka, model = c["marka"], c["model"]
    tip_adi = {"Recine": "REÇİNE", "FDM": "FDM",
               "Lazer": "LAZER", "Cok islevli": "ÇOK İŞLEVLİ"}.get(c["tip"], "")
    durum = {"satista": "SATIŞTA", "duyuruldu": "DUYURULDU",
             "durduruldu": "ÜRETİMDEN KALKTI"}.get(c["durum"], "")

    slaytlar = []
    kt = kunye_tablosu(c)
    if kt:
        slaytlar.append({
            "baslik": "Rakamlar ne diyor",
            "aciklama": "Hepsi üreticinin kendi lansman verisi. Bağımsız "
                        "test çıktıkça buraya not düşeceğim.",
            "tablo": kt})
    oc = c.get("one_cikan") or []
    if oc:
        slaytlar.append({
            "baslik": "Bu makineyi ayıran ne",
            "aciklama": kisalt(c.get("ozet", ""), 190),
            "satirlar": [[("%02d" % (i + 1)), kisalt(x, 112)]
                         for i, x in enumerate(oc[:4])]})
    mt = masa_tablosu(c)
    if mt:
        slaytlar.append({
            "baslik": "Masaya ve prize bakın",
            "aciklama": "Cihazın kapladığı yer ve çektiği güç, satın alma "
                        "kararının en çok atlanan kısmı.",
            "tablo": mt})
    dk = c.get("dikkat") or []
    if dk:
        slaytlar.append({
            "baslik": "Satıcının söylemedikleri",
            "aciklama": "Her makinenin bir bedeli var; bu modelinki şunlar.",
            "satirlar": [["%02d" % (i + 1), kisalt(x, 112)]
                         for i, x in enumerate(dk[:4])]})

    kriterler = []
    satir_ekle(kriterler, "DURUM", durum.lower(), 24)
    satir_ekle(kriterler, "GLOBAL FİYAT", c.get("fiyat_usd"), 24)
    tr = {"var": "stokta görünüyor", "yok": "tükenmiş",
          "bilinmiyor": "teyit edilmeli"}.get(c.get("tr_stok"), "bilinmiyor")
    satir_ekle(kriterler, "TÜRKİYE", "%s · %s" % (c.get("tr_satici") or "satıcı yok", tr), 30)
    satir_ekle(kriterler, "TR FİYATI", c.get("tr_fiyat") or "açıklanmadı", 24)

    notu = "Rakamların tamamı üretici beyanı."
    if c.get("dogrulanmadi"):
        notu += " Doğrulanamayan: " + kisalt(
            ", ".join(c["dogrulanmadi"][:3]), 70) + "."

    return {
        "kategori": KATEGORI.get(c["tip"], "3dbaski"),
        "zemin": zemin,
        "kapak": {
            "tip": "urun",
            "gorsel": c["gorsel"],
            "odak": 0.0,
            "ustbilgi": "%s · %s" % (tip_adi, durum),
            "satir1": marka.upper(),
            "satir2": model.upper(),
            "spot": kisalt(c.get("ozet", ""), 155),
            "ozet": ozet_serit(c),
        },
        "slaytlar": slaytlar[:4],
        "kapanis": {
            "satir1": "SENİN İŞİNE",
            "satir2": "YARAR MI?",
            "kriterler": kriterler[:4],
            "not": notu,
        },
    }


ETIKET = {"Creality": "#creality", "Bambu Lab": "#bambulab",
          "Anycubic": "#anycubic", "Prusa": "#prusa", "Snapmaker": "#snapmaker"}
HESAP = {"Creality": "@creality3dofficial", "Bambu Lab": "@bambulab",
         "Anycubic": "@anycubic3dprinting", "Prusa": "@josefprusa",
         "Snapmaker": "@snapmaker"}


def metin_uret(c):
    p = []
    p.append("%s %s — %s" % (c["marka"], c["model"], c.get("ozet", "")))

    rak = []
    if c.get("alan"):
        rak.append("Baskı alanı %s" % c["alan"])
    if c.get("hiz"):
        rak.append("hız %s" % c["hiz"])
    if c.get("nozul_sicaklik"):
        rak.append("nozul %s" % c["nozul_sicaklik"])
    if c.get("ekran_cozunurluk"):
        rak.append("ekran %s" % c["ekran_cozunurluk"])
    if rak:
        p.append("Rakamlar → " + ", ".join(rak) + ".")

    for x in (c.get("one_cikan") or [])[:3]:
        p.append("%s" % x)

    dk = c.get("dikkat") or []
    if dk:
        p.append("Dikkat → " + dk[0])
    if len(dk) > 1:
        p.append(dk[1])

    tr = c.get("tr_stok")
    if c.get("tr_satici"):
        cumle = "Türkiye tarafı → %s listeliyor" % c["tr_satici"]
        if c.get("tr_fiyat"):
            cumle += ", %s" % c["tr_fiyat"]
        cumle += {"var": ". Stokta görünüyor ama sipariş öncesi teyit alın.",
                  "yok": ". Şu an tükenmiş durumda.",
                  }.get(tr, ". Stok durumu sayfadan okunmuyor, telefonla sorun.")
        p.append(cumle)
    else:
        p.append("Türkiye tarafı → doğrulanmış yetkili satıcı bulamadım. "
                 "Alım üreticinin kendi mağazasından yapılıyor.")

    if c.get("dogrulanmadi"):
        p.append("Şunları doğrulayamadım, açık söylüyorum: %s."
                 % ", ".join(c["dogrulanmadi"][:3]))

    p.append("Bu makineyi konuşan bir arkadaşın varsa bu gönderiyi ona yolla.")
    p.append("#sermenkreatif #3dbaski %s #3dyazici #makerturkiye"
             % ETIKET.get(c["marka"], ""))

    yorum = "Rakamların tamamı üreticinin lansman belgesinden. Bağımsız " \
            "test sonuçları çıktıkça buraya not düşeceğim."
    if HESAP.get(c["marka"]):
        yorum += " Üreticinin hesabı: %s" % HESAP[c["marka"]]
    return "## Gönderi metni\n\n%s\n\n## İlk yorum\n\n%s\n" % (
        "\n\n".join(p), yorum)


def kayitlar():
    return [json.load(open(y, encoding="utf-8"))
            for y in sorted(glob.glob(os.path.join(HERE, "cihazlar", "*", "*.json")))
            if not y.endswith("hepsi.json")]


def yayin_sirasi():
    """Markaları dönüşümlü diz — arka arkaya aynı marka çıkmasın."""
    k = kayitlar()
    markalar = sorted({c["marka"] for c in k})
    kova = {m: sorted([c for c in k if c["marka"] == m],
                      key=lambda c: c["sira"]) for m in markalar}
    sira, i = [], 0
    while any(kova.values()):
        m = markalar[i % len(markalar)]
        if kova[m]:
            sira.append(kova[m].pop(0))
        i += 1
    return sira


def main():
    if "--sira" in sys.argv or "--foto" in sys.argv:
        sira = yayin_sirasi()
        eksik = 0
        for i, c in enumerate(sira, 1):
            var = os.path.exists(os.path.join(HERE, "gorsel", c["gorsel"]))
            if "--foto" in sys.argv and var:
                continue
            eksik += 0 if var else 1
            print("%2d. %-11s %-24s %-13s %s" % (
                i, c["marka"], c["model"], c["tip"],
                "fotoğraf var" if var else "gorsel/" + c["gorsel"]))
        print("\n%d cihaz, %d tanesinin fotoğrafı eksik." % (len(sira), eksik))
        return

    c = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    # crc32 sabit: aynı cihaz her çalıştırmada aynı zemini alıyor
    zemin = ZEMIN[zlib.crc32(c["slug"].encode()) % len(ZEMIN)]
    spec = spec_uret(c, zemin)
    json.dump(spec, open(os.path.join(out, "spec.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    open(os.path.join(out, "metin.md"), "w", encoding="utf-8").write(metin_uret(c))
    print("%s · %s → %s (zemin %s, %d slayt)" % (
        c["marka"], c["model"], out, zemin, len(spec["slaytlar"])))


if __name__ == "__main__":
    main()
