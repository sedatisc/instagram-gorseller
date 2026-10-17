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

KAGIT = "#eef2f8"
ZEMIN = "#ffffff"          # ürün kesimlerinin ortak zemini

MUREKKEP = "#101626"
SOLUK = "#5a6678"
CIZGI = "#d6dde8"
LACI = "#121a30"
LACI_KOYU = "#0b1326"


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
                ("Anton", "400", "Anton-Regular.ttf"),
                ("Pop", "400", "Poppins-Regular.ttf"),
                ("Pop", "500", "Poppins-Medium.ttf"),
                ("Pop", "600", "Poppins-SemiBold.ttf"),
                ("Pop", "700", "Poppins-Bold.ttf"),
                ("Mono", "400", "JetBrainsMono.ttf")):
            p.append("@font-face{font-family:%s;font-weight:%s;font-style:"
                     "normal;src:url(data:font/ttf;base64,%s) format('truetype')}"
                     % (aile, agirlik, _b64(os.path.join(d, dosya))))
        _FONT["css"] = "".join(p)
    return _FONT["css"]


# ---------------------------------------------------------------- ortak css
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#222}
.slide{position:relative;overflow:hidden;font-family:Pop,sans-serif;
  display:flex;flex-direction:column;background:%(kagit)s;color:%(mur)s}
.slide.koyu{background:%(laci)s;color:#fff}

/* başlık ailesi */
.d1{font-family:Anton;text-transform:uppercase;line-height:.96;
  letter-spacing:.005em}
.d2{font-weight:700;line-height:1.1;letter-spacing:-.015em}
.gov{font-family:Mono;letter-spacing:.14em;text-transform:uppercase}

/* Ürün çerçevesi. Düz beyaz kutuda ürün yapıştırılmış gibi duruyordu;
   yumuşak stüdyo degradesi, yere oturan gölge elipsi ve iki katmanlı
   düşen gölge ürünü sahneye oturtuyor. */
.urun{border-radius:24px;overflow:hidden;position:relative;
  display:flex;align-items:flex-end;justify-content:center;
  background:radial-gradient(118%% 86%% at 50%% 6%%,
    #ffffff 0%%, #f5f7fb 56%%, #e7ebf3 100%%);
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.055)}
/* temas gölgesi: ürünün tabanı kutunun altından %%4 yukarıda */
.urun::after{content:"";position:absolute;left:50%%;bottom:4%%;
  width:46%%;height:26px;transform:translate(-50%%,42%%);
  background:radial-gradient(50%% 50%% at 50%% 50%%,
    rgba(16,22,38,.26) 0%%, rgba(16,22,38,0) 72%%)}
/* width/height yüzde, max-width değil: max-* yalnız tavan koyuyor,
   küçük kesimler kendi piksel boyunda kalıp kutunun içinde minik
   duruyordu. Yüzde veriyoruz, contain oranı koruyor. */
.urun img{position:relative;z-index:1;
  width:88%%;height:88%%;object-fit:contain;margin-bottom:4%%;
  /* Dar gölge (2px bulanıklık) açık renkli ürünün siluetine yapışıp
     gri bir hale gibi duruyordu; ikisi de aşağı ve yumuşak. */
  filter:drop-shadow(0 10px 12px rgba(16,22,38,.13))
         drop-shadow(0 30px 34px rgba(16,22,38,.11))}
/* kesilemeyen fotoğraf kendi zeminini getiriyor, kutuyu doldursun */
.urun.sik{background:#fff}
.urun.sik::after{display:none}
.urun.sik img{width:100%%;height:100%%;object-fit:cover;margin-bottom:0;
  filter:none}

/* künye şeridi */
.kunye{display:flex;align-items:center;justify-content:space-between;
  border-top:2px solid %(cizgi)s;margin:0 36px;padding:18px 0 26px;
  font-family:Mono;font-size:23px;color:%(mur)s}
.kunye .orta{font-family:Pop;font-weight:600;font-size:22px}
.kunye .sag{color:%(soluk)s}
.koyu .kunye{border-top-color:#2a3654;color:#fff}
.koyu .kunye .sag{color:#96a4c0}

/* cip */
.cip{display:inline-flex;align-items:center;border-radius:999px;
  background:%(laci)s;color:#fff;font-family:Mono;font-size:20px;
  letter-spacing:.06em;padding:10px 17px;text-transform:uppercase}
""" % {"kagit": KAGIT, "mur": MUREKKEP, "laci": LACI, "zemin": ZEMIN,
       "cizgi": CIZGI, "soluk": SOLUK}


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
