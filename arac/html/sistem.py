#!/usr/bin/env python3
"""Tasarım sistemi — HTML şablonlarının tek kaynağı.

Kare üretimi iki yerde yapılıyordu: Pillow'da (`uret.py`, `urun_karti.py`)
ve elle. İkisinde de renk, punto ve boşluk ayrı ayrı yazılıyordu; biri
değişince öbürü eski kalıyordu. Buradaki değerler tek kaynak: renk
adları `uret.py`deki paletle aynı, fontlar `fonts/` içinden gömülüyor.

Kullanımı:

    from sistem import CSS, FONT_CSS, bas, urun_data, ZEMIN

    html = "<!doctype html>... <style>%s %s</style> ..." % (FONT_CSS, CSS)
    bas(html, "cikti.jpg", 1080, 1350)
"""
import base64
import io
import os
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(KOK, "arac"))

# --------------------------------------------------------------- jetonlar
# Renk adları uret.py'deki RENKLER ile birebir aynı tutuluyor; spec
# dosyalarında "renk": "yesil" yazınca iki motor da aynı rengi veriyor.
RENK = {
    "kirmizi": "#e43e3e", "turuncu": "#ec842a", "sari": "#e9b820",
    "yesil": "#24a256", "mavi": "#2476dc", "mor": "#8650e2",
    "turkuaz": "#16a2ad", "pembe": "#de4c8c", "gri": "#6c768a",
}

TEMA = {
    "3dbaski":    {"vurgu": "#ff8a3c", "etiket": "3D BASKI"},
    "proje":      {"vurgu": "#a78bfa", "etiket": "PROJE & ATÖLYE"},
    "kurumsal":   {"vurgu": "#f45d5a", "etiket": "SERMEN KREATİF"},
    "elektronik": {"vurgu": "#22d3ee", "etiket": "ELEKTRONİK & IoT"},
}

KAGIT = "#FBFAF7"
ZEMIN = "#ffffff"          # ürün kesimlerinin ortak zemini

MUREKKEP = "#16181C"
SOLUK = "#6A7079"
CIZGI = "#C9C5B9"
MARKA = "#a52628"        # logodan alındı
LACI = "#16181C"
LACI_KOYU = "#0E1013"


def _b64(yol):
    with open(yol, "rb") as f:
        return base64.b64encode(f.read()).decode()


_FONT = {}


def font_css():
    """Fontlar gömülü: Express'e aktarılan HTML'in dışarıya bağımlı
    olmaması, Chromium'un da sistem fontuna düşmemesi gerekiyor."""
    if "css" not in _FONT:
        d = os.path.join(KOK, "fonts")
        p = []
        for aile, agirlik, dosya in (
                ("Pop", "100 900", "Archivo.ttf"),
                ("Anton", "100 900", "Archivo.ttf"),
                ("Mono", "400", "JetBrainsMono.ttf")):
            # Archivo değişken font: ağırlık ve genişlik aralıklı
            # tanımlanıyor, başlıkta genişletilmiş kesim kullanılıyor.
            p.append("@font-face{font-family:%s;font-weight:%s;font-style:"
                     "normal;font-stretch:62%% 125%%;"
                     "src:url(data:font/ttf;base64,%s) format('truetype')}"
                     % (aile, agirlik, _b64(os.path.join(d, dosya))))
        _FONT["css"] = "".join(p)
    return _FONT["css"]


# ---------------------------------------------------------------- ortak css
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#222}
.slide{position:relative;overflow:hidden;font-family:Pop,sans-serif;
  display:flex;flex-direction:column;background:%(kagit)s;color:%(mur)s;
  font-variation-settings:"wdth" 100;
  --kagit:%(kagit)s;--mur:%(mur)s;--soluk:%(soluk)s;--cizgi:%(cizgi)s;
  --marka:%(marka)s}
.slide.koyu{--cizgi:#2E3238;--soluk:#8C9099;--mur:#F3F2EE}
.slide.koyu{background:%(laci)s;color:#F3F2EE}

/* Başlık ailesi. Eski hat sıkışık büyük harf bir başlık yüzü
   kullanıyordu; Türkçede büyük harf okunurluğu düşürüyor ve her
   sektörde aynı duran bir kalıp üretiyordu. Tek aile, genişletilmiş
   kesim, cümle düzeni. */
.d1{font-family:Pop;font-weight:650;line-height:.99;letter-spacing:-.025em;
  font-variation-settings:"wdth" 112}
.d2{font-weight:600;line-height:1.14;letter-spacing:-.018em}
.gov{font-family:Mono;letter-spacing:.01em;color:%(soluk)s}

/* Fotoğraf penceresi: föy mantığında görsel, kenarı çizili bir
   pencerede duruyor. Yuvarlak köşe, degrade ve gölge yok — ürünün
   kendi fotoğrafı ne ise o. */
.urun{overflow:hidden;position:relative;background:#fff;
  border:1px solid %(cizgi)s;
  display:flex;align-items:center;justify-content:center}
.urun img{width:100%%;height:100%%;object-fit:contain}
/* kesilemeyen fotoğraf kendi zeminini getiriyor */
.urun.sik img{object-fit:cover}

/* künye şeridi */
.kunye{display:flex;align-items:center;justify-content:space-between;
  border-top:1px solid %(cizgi)s;margin:0 56px;padding:20px 0 26px;
  font-family:Mono;font-size:20px;color:%(soluk)s}
.kunye .orta{font-family:Pop;font-weight:600;font-size:21px;color:%(mur)s;
  letter-spacing:-.01em}
.kunye .sag{color:%(marka)s}
.koyu .kunye{border-top-color:#2E3238;color:#8C9099}
.koyu .kunye .orta{color:#F3F2EE}
.koyu .kunye .sag{color:#E8A0A1}

/* etiket: yuvarlak rozet değil, işaretli satır */
.cip{display:inline-flex;align-items:center;gap:10px;
  font-family:Mono;font-size:20px;color:%(mur)s;letter-spacing:.005em}
.cip::before{content:"";width:11px;height:11px;border-radius:50%%;
  border:2px solid %(marka)s;flex:0 0 auto}
.koyu .cip{color:#F3F2EE}
""" % {"kagit": KAGIT, "mur": MUREKKEP, "laci": LACI, "zemin": ZEMIN,
       "cizgi": CIZGI, "soluk": SOLUK, "marka": MARKA}


# ------------------------------------------------------------------ görsel
def _data_uri(ham, tur="png"):
    return "data:image/%s;base64,%s" % (tur, base64.b64encode(ham).decode())


def kesik_uri(yol):
    """Arka planı kesilmiş ürünü data URI olarak veriyor.

    Kesim `urun_karti.kesik_ac` ile yapılıyor; önbellek de orada, iki
    motor aynı PNG'yi paylaşıyor."""
    from urun_karti import kesik_ac
    kes = kesik_ac(yol)
    if kes is None:
        return None
    tmp = io.BytesIO()
    kes.save(tmp, "PNG")
    return _data_uri(tmp.getvalue())


def foto_uri(yol):
    """Kesilemeyen ürün için ham fotoğraf."""
    uz = os.path.splitext(yol)[1].lower().lstrip(".")
    with open(yol, "rb") as f:
        return _data_uri(f.read(), "jpeg" if uz in ("jpg", "jpeg") else uz)


# ------------------------------------------------------------------- baskı
OLCEK = 2          # ekran çarpanı — 2x basıp küçültüyoruz


def bas(html, cikti, w, h, kalite=93):
    """HTML'i Chromium'da açıp JPEG'e basıyor.

    İki katı çözünürlükte basılıp LANCZOS ile küçültülüyor: tarayıcı
    1x'te yazı kenarlarını ve yuvarlatılmış köşeleri piksel ızgarasına
    oturtuyor, harfler kalınlaşıp kirli çıkıyordu. 2x'te örnekleme
    dörde katlanıyor, küçültme de kenarları yumuşatıyor.

    JPEG zorunlu: Instagram Graph API /media ucu PNG kabul etmiyor."""
    from PIL import Image

    cikti = os.path.abspath(cikti)
    os.makedirs(os.path.dirname(cikti) or ".", exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        hy = os.path.join(t, "k.html")
        with open(hy, "w", encoding="utf-8") as f:
            f.write(html)
        ham = os.path.join(t, "k.png")
        js = os.path.join(t, "k.js")
        with open(js, "w") as f:
            f.write(
                "const {chromium}=require('playwright');(async()=>{"
                "const b=await chromium.launch();"
                "const p=await b.newPage({viewport:{width:%d,height:%d},"
                "deviceScaleFactor:%d});"
                "await p.goto('file://%s');"
                "await p.evaluate(()=>document.fonts.ready);"
                "await p.waitForTimeout(300);"
                "await p.screenshot({path:%r,type:'png'});"
                "await b.close();})();" % (w, h, OLCEK, hy, ham))
        subprocess.run(["node", js], check=True, cwd=KOK,
                       capture_output=True, text=True)
        im = Image.open(ham).convert("RGB")
        if im.size != (w, h):
            im = im.resize((w, h), Image.LANCZOS)
        im.save(cikti, "JPEG", quality=kalite, subsampling=0, optimize=True)
    print("%s  %dx%d" % (cikti, w, h))
    return cikti


def sayfa(govde, w, h, ek_css="", sinif=""):
    """Tek kareyi tam HTML belgesine sarıyor."""
    return (
        '<!doctype html><html lang="tr"><head><meta charset="utf-8">'
        '<meta name="hz:slide-selector" content=".slide">'
        '<style>%s%s\n.slide{width:%dpx;height:%dpx}\n%s</style></head>'
        '<body><section class="slide %s" data-canvas-width="%d" '
        'data-canvas-height="%d">%s</section></body></html>'
        % (font_css(), CSS, w, h, ek_css, sinif, w, h, govde))
