#!/usr/bin/env python3
"""Bayram karesi — tek seferlik özel tasarım.

Ay ve yıldız hazır çizim değil, iki aşamada üretiliyor:

1. Maske, Türk Bayrağı Tüzüğü'ndeki kurguyla kuruluyor. G ölçü birimi
   olmak üzere dış çemberin çapı G/2, iç çemberin çapı 2G/5 ve merkezi
   dış çemberden G/16 sağda, yıldızın çevrel çemberinin çapı G/4 ve bir
   ucu aya bakıyor. Kurgu şu bilinen sabitle doğrulanıyor: iç çemberin
   sol kenarından ayın iki ucundan geçen dikey çizgiye olan uzaklık
   0,34875 G.
2. Maske, bir dilimleyicinin kat planı gibi çiziliyor — dış çeper ve
   45 derecelik dolgu yolu. Düz dolu bir nişan her markanın bayram
   paylaşımında var; bu atölye şekilleri böyle üretiyor, nişan da
   öyle duruyor.

    python3 arac/bayram_html.py <spec.json> <cikti-klasoru>
"""
import base64
import hashlib
import html as _h
import json
import math
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "arac"))
sys.path.insert(0, os.path.join(KOK, "arac", "html"))

import sistem as S                                          # noqa: E402

W, H = 1080, 1350
SW, SH = 1080, 1920
BAYRAK = "#E30A17"          # Türk Bayrağı Tüzüğü'ndeki kırmızı
ONBELLEK = os.path.join(KOK, "gorsel", "bayram")


def E(s):
    return _h.escape(str(s), quote=False)


def _maske(g, pay=0.06):
    """Tüzük kurgusuyla ay ve yıldızın maskesi."""
    import cv2
    import numpy as np
    ro, ri, rs = g * .25, g * .20, g * .125
    xo, yo = g * (.55 + pay), g * (.5 + pay)
    xi = xo + g * .0625
    xuc = xo + (ro ** 2 - ri ** 2) / (2 * (xi - xo)) - (xi - xo) / 2
    xs = xuc + g * .0154 + rs
    en, boy = int(g * (1.18 + 2 * pay)), int(g * (1 + 2 * pay))
    m = np.zeros((boy, en), np.uint8)
    cv2.circle(m, (int(xo), int(yo)), int(ro), 255, -1)
    cv2.circle(m, (int(xi), int(yo)), int(ri), 0, -1)
    uc = []
    for i in range(10):
        a = math.radians(180 + i * 36)
        r = rs if i % 2 == 0 else rs * math.sin(math.radians(18)) / \
            math.sin(math.radians(126))
        uc.append([int(xs + r * math.cos(a)), int(yo + r * math.sin(a))])
    cv2.fillPoly(m, [np.array(uc, np.int32)], 255)
    return m


def nisan(g=900, renk=(227, 10, 23), kalinlik=15, aralik=20, ceper=1):
    """Kat planı gibi çizilmiş nişan; saydam PNG yolu döndürüyor."""
    import cv2
    import numpy as np
    from PIL import Image

    imza = hashlib.sha1(("%d-%s-%d-%d-%d" % (g, renk, kalinlik, aralik,
                                             ceper)).encode()).hexdigest()[:12]
    yol = os.path.join(ONBELLEK, "nisan-%s.png" % imza)
    if os.path.exists(yol):
        return yol

    m = _maske(g)
    boy, en = m.shape
    tuval = np.zeros((boy, en, 4), np.uint8)

    def ciz(nm):
        for i, deger in enumerate(renk):
            tuval[..., i][nm > 0] = deger
        tuval[..., 3][nm > 0] = 255

    cekirdek = np.ones((3, 3), np.uint8)
    ic = m.copy()
    for _ in range(ceper):
        kon, _k = cv2.findContours(ic, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cizgi = np.zeros_like(m)
        cv2.drawContours(cizgi, kon, -1, 255, kalinlik)
        ciz(cv2.bitwise_and(cizgi, m))
        ic = cv2.erode(ic, cekirdek, iterations=kalinlik)

    # Dolgu yolu 45 derece. Çeperin yarısı kadar içeri çekiliyor ki ayın
    # inceldiği yerde de yol görünsün.
    dolgu = np.zeros_like(m)
    for c in range(-boy, en + boy, aralik):
        cv2.line(dolgu, (c, 0), (c + boy, boy), 255, max(3, kalinlik - 4))
    ciz(cv2.bitwise_and(dolgu, cv2.erode(m, cekirdek,
                                         iterations=max(1, kalinlik // 2))))

    os.makedirs(ONBELLEK, exist_ok=True)
    Image.fromarray(tuval, "RGBA").save(yol)
    return yol


def _uri(yol):
    with open(yol, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


STIL = """
.slide{background:#0E1013;color:#F3F2EE;position:relative;overflow:hidden}
.slide::before{content:"";position:absolute;inset:0;
  background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);
  background-size:54px 54px}
.ic{position:relative;z-index:2;display:flex;flex-direction:column;
  height:100%%;padding:56px 56px 0}
.ust{flex:0 0 auto;display:flex;align-items:center;
  justify-content:space-between;padding-bottom:20px;
  border-bottom:1px solid #2E3238}
.ust img{height:30px;filter:brightness(0) invert(1)}
.ust span{font-family:Mono;font-size:19px;color:#8C9099}
.nisan{flex:1 1 auto;min-height:0;display:flex;align-items:center;
  justify-content:center;padding:14px 0}
.nisan img{max-width:96%%;max-height:100%%}
.soz{flex:0 0 auto}
.soz h1{font-size:112px;font-weight:650;font-variation-settings:"wdth" 112;
  line-height:.96;letter-spacing:-.03em}
.soz h2{font-size:42px;font-weight:450;letter-spacing:-.02em;
  line-height:1.16;margin-top:14px}
.soz p{font-family:Mono;font-size:21px;margin-top:18px;color:#E8A0A1}
.dip{flex:0 0 auto;display:flex;justify-content:space-between;
  align-items:baseline;margin-top:24px;padding:20px 0 30px;
  border-top:1px solid #2E3238;font-family:Mono;font-size:19px;
  color:#8C9099}
.hik .nisan{padding:54px 0 40px}
.hik .soz h1{font-size:126px}
.hik .dip{padding-bottom:190px}
"""


def _govde(spec, g):
    logo = S.foto_uri(os.path.join(KOK, "gorsel", "marka",
                                   "sermenkreatif.png"))
    return (
        '<div class="ic"><div class="ust"><img src="%s" alt="">'
        '<span>%s</span></div>'
        '<div class="nisan"><img src="%s" alt=""></div>'
        '<div class="soz"><h1>%s</h1><h2>%s</h2><p>%s</p></div>'
        '<div class="dip"><span>@sermenkreatif</span><span>%s</span></div>'
        '</div>'
        % (logo, E(spec.get("yer", "Sermen Kreatif, Samsun")),
           _uri(nisan(g)), E(spec["baslik"]), E(spec["alt"]),
           E(spec.get("not", "")),
           E(spec.get("dip_sag", "sermenkreatif.com"))))


def kare(spec, cikti):
    S.bas(S.sayfa(_govde(spec, 900), W, H, STIL), cikti, W, H)


def hikaye(spec, cikti):
    S.bas(S.sayfa(_govde(spec, 900), SW, SH, STIL, sinif="hik"),
          cikti, SW, SH, kalite=92)


def uret(spec, klasor):
    os.makedirs(klasor, exist_ok=True)
    kare(spec, os.path.join(klasor, "1.jpg"))
    hikaye(spec, os.path.join(klasor, "hikaye.jpg"))
    return 1


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    print("%d kare + hikaye" % uret(spec, sys.argv[2]))


if __name__ == "__main__":
    main()
