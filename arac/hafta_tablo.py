#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Haftalık onay tablosunu tek görsel olarak çizer.

otomasyon/hafta-onay.json'u okuyup her gönderi için saat, kategori,
gerçek kapak görseli ve yayına gidecek metnin başını alt alta diziyor.
Çıkan tek görsel telefonda kaydırılarak gözden geçiriliyor.

Depo dışındaki görselleri (sitenin ürün fotoğrafları) indirdiği için
internete açık bir yerde çalışması gerekiyor. Yazı tipi Inter; yoksa
indiriliyor.

Kullanım:
    python3 arac/hafta_tablo.py [hafta-onay.json yolu] [çıktı.jpg]
"""
import datetime
import io
import json
import os
import subprocess
import sys
import textwrap
import urllib.request

from PIL import Image, ImageDraw, ImageFont

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YAZI = os.path.join(KOK, ".yazitipi", "Inter-%s.otf")
INTER = "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip"

AY = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
      "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
GUN = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi",
       "Pazar"]
RENK = {"magaza": (34, 122, 160), "baski": (168, 116, 58),
        "proje": (95, 110, 80), "uygulama": (128, 86, 160),
        "rehber": (90, 96, 110)}

TH_W, TH_H = 216, 270
SATIR = TH_H + 34
BASLIK_Y = 84
EN = 1240


def yazitipi_kur():
    if os.path.exists(YAZI % "Bold"):
        return
    kok = os.path.dirname(YAZI)
    os.makedirs(kok, exist_ok=True)
    zip_yol = os.path.join(kok, "inter.zip")
    urllib.request.urlretrieve(INTER, zip_yol)
    subprocess.run(["unzip", "-oqj", zip_yol, "extras/otf/Inter-*.otf",
                    "-d", kok], check=True)
    os.remove(zip_yol)


def fnt(agirlik, boy):
    return ImageFont.truetype(YAZI % agirlik, boy)


def gunadi(t):
    d = datetime.date.fromisoformat(t)
    return "%d %s %s" % (d.day, AY[d.month - 1], GUN[d.weekday()])


def indir(u):
    try:
        with urllib.request.urlopen(u, timeout=25) as r:
            return Image.open(io.BytesIO(r.read())).convert("RGB")
    except Exception as e:                       # noqa: BLE001
        print("görsel alınamadı: %s (%s)" % (u, e))
        return None


def kirp(im, en, boy):
    w, h = im.size
    hedef = en / boy
    if w / h > hedef:
        yeni = int(h * hedef)
        im = im.crop(((w - yeni) // 2, 0, (w + yeni) // 2, h))
    else:
        yeni = int(w / hedef)
        ust = max(0, (h - yeni) // 2)
        im = im.crop((0, ust, w, ust + yeni))
    return im.resize((en, boy), Image.LANCZOS)


def ciz(plan, hedef):
    gunler = sorted({p["tarih"] for p in plan})
    boy = 150 + sum(BASLIK_Y + SATIR * len([p for p in plan
                                            if p["tarih"] == t])
                    for t in gunler) + 60
    im = Image.new("RGB", (EN, boy), (247, 246, 243))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, EN, 150], fill=(17, 20, 26))
    d.text((48, 40), "HAFTALIK YAYIN PLANI", font=fnt("Bold", 38),
           fill=(255, 255, 255))
    d.text((48, 92), "%s – %s · %d besleme gönderisi · onayına sunulur"
           % (gunadi(gunler[0]), gunadi(gunler[-1]), len(plan)),
           font=fnt("Medium", 24), fill=(150, 160, 175))

    y = 150
    for t in gunler:
        d.rectangle([0, y, EN, y + BASLIK_Y], fill=(232, 229, 223))
        d.line([(0, y), (EN, y)], fill=(210, 206, 198), width=2)
        d.text((48, y + 26), gunadi(t), font=fnt("SemiBold", 31),
               fill=(40, 44, 52))
        y += BASLIK_Y
        for p in [x for x in plan if x["tarih"] == t]:
            th = indir(p["kapak"]) if p.get("kapak") else None
            if th:
                im.paste(kirp(th, TH_W, TH_H), (48, y + 16))
                d.rectangle([48, y + 16, 48 + TH_W, y + 16 + TH_H],
                            outline=(214, 210, 202), width=2)
            x = 48 + TH_W + 30
            d.text((x, y + 20), p["saat"], font=fnt("Bold", 30),
                   fill=(24, 28, 34))
            et = p["kategori"].upper()
            fe = fnt("Bold", 17)
            d.rounded_rectangle([x + 92, y + 22,
                                 x + 92 + fe.getlength(et) + 26, y + 50],
                                radius=14,
                                fill=RENK.get(p["kategori"], (120, 120, 120)))
            d.text((x + 105, y + 28), et, font=fe, fill=(255, 255, 255))
            for n, s in enumerate(textwrap.wrap(p["ad"], 44)[:2]):
                d.text((x, y + 66 + n * 33), s, font=fnt("SemiBold", 26),
                       fill=(24, 28, 34))
            oz = " ".join(p.get("ozet", "").split())
            for n, s in enumerate(textwrap.wrap(oz, 62)[:4]):
                d.text((x, y + 142 + n * 28), s, font=fnt("Regular", 21),
                       fill=(96, 102, 112))
            d.line([(48, y + SATIR - 1), (EN - 48, y + SATIR - 1)],
                   fill=(226, 222, 214), width=1)
            y += SATIR
    im.save(hedef, quality=84, optimize=True)
    return im.size


def main():
    kaynak = (sys.argv[1] if len(sys.argv) > 1
              else os.path.join(KOK, "otomasyon", "hafta-onay.json"))
    hedef = sys.argv[2] if len(sys.argv) > 2 else os.path.join(KOK, "hafta.jpg")
    yazitipi_kur()
    if kaynak.startswith("http"):
        plan = json.load(urllib.request.urlopen(kaynak))
    else:
        with open(kaynak, encoding="utf-8") as f:
            plan = json.load(f)
    print("tablo: %s · %s" % (ciz(plan, hedef), hedef))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
