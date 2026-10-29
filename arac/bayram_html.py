#!/usr/bin/env python3
"""Bayram karesi — tek seferlik özel tasarım.

Ay ve yıldız clip-art değil: Türk Bayrağı Tüzüğü'ndeki çizim
ölçüleriyle kuruluyor. G bayrağın eni olmak üzere dış çemberin çapı
G/2, iç çemberin çapı 2G/5 ve merkezi dış çemberden G/16 sağda,
yıldızın çevrel çemberinin çapı G/4. Kurgu şu bilinen değerle
doğrulanıyor: iç çemberin sol kenarından ayın iki ucundan geçen
dikey çizgiye olan uzaklık 0,34875 G.

    python3 arac/bayram_html.py <spec.json> <cikti-klasoru>
"""
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


def E(s):
    return _h.escape(str(s), quote=False)


def _yildiz(cx, cy, r, donme=180):
    """Beş köşeli yıldız; bir ucu aya, yani sola bakıyor."""
    n = []
    for i in range(10):
        a = math.radians(donme + i * 36)
        yr = r if i % 2 == 0 else r * math.sin(math.radians(18)) / \
            math.sin(math.radians(126))
        n.append("%.3f,%.3f" % (cx + yr * math.cos(a), cy + yr * math.sin(a)))
    return " ".join(n)


def ay_yildiz(g, renk="#fff"):
    """Tüzükteki kurguyla ay ve yıldız; G ayın ölçü birimi (px)."""
    ro, ri, rs = g * .25, g * .20, g * .125
    xo, yo = g * .55, g * .5                 # dış çember merkezi
    xi = xo + g * .0625                      # iç çember G/16 sağda
    # Ayın uçlarından geçen dikey çizgi; yıldızın sol ucu bunun
    # 0,0154 G sağında duruyor.
    xuc = xo + (ro ** 2 - ri ** 2) / (2 * (xi - xo)) - (xi - xo) / 2
    xs = xuc + g * .0154 + rs
    return (
        '<svg viewBox="0 0 %.1f %.1f" width="100%%" height="100%%" '
        'fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<defs><mask id="ay">'
        '<rect width="%.1f" height="%.1f" fill="#000"/>'
        '<circle cx="%.3f" cy="%.3f" r="%.3f" fill="#fff"/>'
        '<circle cx="%.3f" cy="%.3f" r="%.3f" fill="#000"/>'
        '</mask></defs>'
        '<rect width="%.1f" height="%.1f" fill="%s" mask="url(#ay)"/>'
        '<polygon points="%s" fill="%s"/></svg>'
        % (g * 1.18, g, g * 1.18, g, xo, yo, ro, xi, yo, ri,
           g * 1.18, g, renk, _yildiz(xs, yo, rs), renk))


STIL = """
.slide{background:%(bayrak)s;color:#fff;padding:56px 56px 0}
.ust{flex:0 0 auto;display:flex;align-items:center;
  justify-content:space-between;padding-bottom:20px;
  border-bottom:1px solid rgba(255,255,255,.34)}
.ust img{height:30px;filter:brightness(0) invert(1)}
.ust span{font-family:Mono;font-size:19px;color:rgba(255,255,255,.8)}
.nisan{flex:1 1 auto;min-height:0;display:flex;align-items:center;
  justify-content:center;padding:30px 0 30px}
.nisan svg{max-width:88%%;max-height:100%%}
.soz{flex:0 0 auto}
.soz h1{font-size:118px;font-weight:650;font-variation-settings:"wdth" 112;
  line-height:.96;letter-spacing:-.03em}
.soz h2{font-size:46px;font-weight:450;letter-spacing:-.02em;
  line-height:1.14;margin-top:14px;color:rgba(255,255,255,.94)}
.soz p{font-family:Mono;font-size:21px;color:rgba(255,255,255,.8);
  margin-top:20px}
.dip{flex:0 0 auto;display:flex;justify-content:space-between;
  align-items:baseline;margin-top:26px;padding:20px 0 30px;
  border-top:1px solid rgba(255,255,255,.34);
  font-family:Mono;font-size:19px;color:rgba(255,255,255,.8)}
.hik .nisan{padding:70px 0 56px}
.hik .soz h1{font-size:132px}
.hik .dip{padding-bottom:190px}
""" % {"bayrak": BAYRAK}


def _govde(spec, g, sinif=""):
    logo = S.foto_uri(os.path.join(KOK, "gorsel", "marka",
                                   "sermenkreatif.png"))
    return (
        '<div class="ust"><img src="%s" alt=""><span>%s</span></div>'
        '<div class="nisan">%s</div>'
        '<div class="soz"><h1>%s</h1><h2>%s</h2><p>%s</p></div>'
        '<div class="dip"><span>@sermenkreatif</span><span>%s</span></div>'
        % (logo, E(spec.get("yer", "Sermen Kreatif, Samsun")),
           ay_yildiz(g), E(spec["baslik"]), E(spec["alt"]),
           E(spec.get("not", "")), E(spec.get("dip_sag", "sermenkreatif.com"))))


def kare(spec, cikti):
    S.bas(S.sayfa(_govde(spec, 520), W, H, STIL), cikti, W, H)


def hikaye(spec, cikti):
    S.bas(S.sayfa(_govde(spec, 620), SW, SH, STIL, sinif="hik"),
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
