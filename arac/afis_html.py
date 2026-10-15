#!/usr/bin/env python3
"""Kampanya afişi — üç kategorili bayi afişi düzeni, HTML/CSS ile.

Afişin istediği şeyler (katmanlı gölge, konturlu başlık, eğik kurdele,
hassas satır aralığı) CSS'te hazır geliyor; Pillow'da tek tek
çizilince sonuç kodla çizilmiş gibi duruyordu. Renk ve font
`arac/html/sistem.py`den, yani ürün kartlarıyla aynı yerden geliyor.

    python3 arac/afis_html.py <spec.json> <cikti.jpg> [--html <dosya>]

spec alanları: `baslik` (iki satır), `alt`, `ust`, `renk`, üç `paneller`
(`ad`, `renk`, `gorsel`, üç `maddeler`), `guven` (dört ibare) ve
isteğe bağlı `teklif`. `teklif` boşsa yerine mağaza şeridi geçiyor;
gerçekten uygulanacak bir kampanya yoksa şerit boş bırakılmıyor.
"""
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "arac"))
sys.path.insert(0, os.path.join(KOK, "arac", "html"))

import sistem as S                                          # noqa: E402

W, H = 1080, 1350


def _gorsel(yol):
    """Ürün görseli: kesilmişi varsa o, yoksa ham fotoğraf."""
    tam = yol if os.path.isabs(yol) else os.path.join(KOK, "gorsel", yol)
    if not os.path.exists(tam):
        raise SystemExit("görsel yok: " + tam)
    return S.kesik_uri(tam) or S.foto_uri(tam)


STIL = """
/* Zemin: düz lacivert + başlığın arkasında tek yumuşak hâle.
   Işın deseni (repeating-conic-gradient) sert kenarlı dilimler
   yapıyordu; JPEG sıkıştırması da üstüne binince zemin kirli
   görünüyordu. Doku yerine ince ve eşit nokta ızgarası var. */
.slide{color:#fff;background:
    radial-gradient(70%% 42%% at 50%% 16%%,
      rgba(90,125,210,.34) 0%%, rgba(90,125,210,0) 70%%),
    radial-gradient(circle at 1px 1px,
      rgba(255,255,255,.055) 1px, transparent 1.6px) 0 0/22px 22px,
    linear-gradient(180deg, #16224a 0%%, #101a36 46%%, #0a1026 100%%)}
.ust{display:flex;justify-content:space-between;align-items:center;
  padding:30px 36px 0;position:relative}
.ust .marka{font-weight:600;font-size:29px;letter-spacing:-.01em}
.ust .marka i{font-style:normal;color:%(vurgu)s}
.ust .yer{font-family:Mono;font-size:19px;letter-spacing:.22em;
  color:#93a3c4}
.bas{position:relative;text-align:center;padding:14px 40px 0}
.bas h1{font-family:Anton;font-size:72px;line-height:.98;
  letter-spacing:.01em;color:#ffd32e;text-transform:uppercase;
  -webkit-text-stroke:5px #19100a;paint-order:stroke fill;
  text-shadow:0 6px 0 rgba(0,0,0,.35)}
.kurdele{position:relative;margin:16px 24px 0;padding:16px 26px 20px;
  background:linear-gradient(180deg,#e8363a,#bf1d22);border-radius:18px;
  transform:rotate(-1.4deg);
  box-shadow:0 14px 28px rgba(0,0,0,.45),inset 0 2px 0 rgba(255,255,255,.28)}
.kurdele h2{font-family:Anton;font-size:98px;line-height:.92;color:#ffd32e;
  text-transform:uppercase;-webkit-text-stroke:6px #19100a;
  paint-order:stroke fill;text-shadow:0 6px 0 rgba(0,0,0,.35)}
.spot{margin:18px auto 0;max-width:840px;font-weight:500;font-size:25px;
  line-height:1.38;color:#d7e0f2}
.paneller{flex:1 1 auto;min-height:0;display:grid;
  grid-template-columns:repeat(3,1fr);gap:14px;
  align-items:start;align-content:center;padding:22px 28px 0;
  position:relative}
.panel{background:var(--pr);border-radius:20px;padding:0 0 16px;
  box-shadow:0 12px 26px rgba(0,0,0,.38);display:flex;
  flex-direction:column;overflow:hidden}
.panel h3{font-family:Anton;font-size:30px;text-transform:uppercase;
  text-align:center;padding:16px 10px 14px;letter-spacing:.02em;
  text-shadow:0 2px 0 rgba(0,0,0,.28)}
/* Sabit yükseklik: kutu esnerse geniş ürünün üstünde altında beyaz
   boşluk kalıyor, dar ürün ise kutuyu dolduruyordu. */
.panel figure{background:#fff;border-radius:13px;margin:0 12px;
  flex:0 0 auto;height:368px;display:flex;align-items:center;
  justify-content:center;padding:16px}
.panel figure img{max-width:100%%;max-height:100%%;object-fit:contain;
  filter:drop-shadow(0 10px 12px rgba(16,22,38,.22))}
/* min-height: bir panelde iki madde olunca alt hizalar kayıyordu. */
.ozellik{list-style:none;margin:16px 14px 0;flex:0 0 auto;min-height:106px;
  display:flex;flex-direction:column;gap:9px}
.ozellik li{display:flex;align-items:flex-start;gap:9px;font-weight:500;
  font-size:17px;line-height:1.25}
.tik{flex:0 0 17px;height:17px;margin-top:2px;border-radius:50%%;
  background:#fff;position:relative}
.tik::after{content:"";position:absolute;left:5px;top:3px;width:5px;
  height:9px;border:solid var(--pr);border-width:0 2.4px 2.4px 0;
  transform:rotate(42deg)}
.teklif{margin:22px 28px 0;padding:22px 20px;border-radius:20px;
  background:linear-gradient(180deg,#e8363a,#bf1d22);text-align:center;
  box-shadow:0 12px 26px rgba(0,0,0,.4),inset 0 2px 0 rgba(255,255,255,.26);
  display:flex;align-items:center;justify-content:center;gap:16px}
.teklif b{font-family:Anton;font-size:86px;line-height:.8;color:#fff;
  -webkit-text-stroke:4px #19100a;paint-order:stroke fill}
.teklif span{font-family:Anton;font-size:42px;line-height:1;color:#ffd32e;
  text-transform:uppercase;-webkit-text-stroke:3px #19100a;
  paint-order:stroke fill}
.teklif.sade{flex-direction:column;gap:7px;padding:24px 20px;
  background:linear-gradient(180deg,#182548,#101a36);border:2px solid #2b3a63;
  box-shadow:0 12px 26px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.08)}
.teklif.sade span{font-size:46px;-webkit-text-stroke:0;
  text-shadow:0 2px 0 rgba(0,0,0,.4)}
.teklif.sade em{font-style:normal;font-weight:500;font-size:22px;
  color:#aebbd6}
.guven{margin:22px 28px 0;flex:0 0 auto;list-style:none;display:grid;
  grid-template-columns:repeat(4,1fr);background:#070c1a;border-radius:14px;
  padding:17px 8px}
.guven li{font-family:Mono;font-size:14px;letter-spacing:.05em;
  text-align:center;color:#c3d0e8;border-left:1px solid #1d2742}
.guven li:first-child{border-left:0}
.dip{text-align:center;font-family:Mono;font-size:19px;color:#8fa0c0;
  padding:18px 0 22px}
"""


def html_kur(spec):
    vurgu = S.RENK.get(spec.get("renk", "kirmizi"), S.RENK["kirmizi"])

    paneller = []
    for p in spec.get("paneller", [])[:3]:
        renk = S.RENK.get(p.get("renk", "mavi"), S.RENK["mavi"])
        maddeler = "".join('<li><span class="tik"></span>%s</li>' % m
                           for m in p.get("maddeler", [])[:3])
        paneller.append(
            '<article class="panel" style="--pr:%s"><h3>%s</h3>'
            '<figure><img src="%s" alt=""></figure>'
            '<ul class="ozellik">%s</ul></article>'
            % (renk, p["ad"], _gorsel(p["gorsel"]), maddeler))

    # Teklif cümlesi yoksa şerit boş bırakılmıyor; yerine mağaza şeridi
    # geçiyor. Boş bırakılınca afişin ortasında delik kalıyordu.
    teklif = spec.get("teklif", "")
    if teklif:
        parca = teklif if isinstance(teklif, list) else [teklif]
        ic = "".join('<b>%s</b>' % m if str(m).isdigit()
                     else '<span>%s</span>' % m for m in parca)
        serit = '<div class="teklif">%s</div>' % ic
    else:
        serit = ('<div class="teklif sade"><span>%s</span><em>%s</em></div>'
                 % (spec.get("cagri", "Tümü sermenkreatif.com'da"),
                    spec.get("cagri_alt", "Samsun'dan Türkiye'nin her yerine")))

    govde = (
        '<header class="ust"><div class="marka"><i>●</i> sermenkreatif</div>'
        '<div class="yer">%s</div></header>'
        '<div class="bas"><h1>%s</h1><div class="kurdele"><h2>%s</h2></div>'
        '<p class="spot">%s</p></div>'
        '<main class="paneller">%s</main>%s'
        '<ul class="guven">%s</ul>'
        '<div class="dip">@sermenkreatif &nbsp;·&nbsp; sermenkreatif.com</div>'
        % (spec.get("ust", ""), spec["baslik"][0],
           spec["baslik"][1] if len(spec["baslik"]) > 1 else "",
           spec.get("alt", ""), "".join(paneller), serit,
           "".join('<li>%s</li>' % g for g in spec.get("guven", [])[:4])))

    return S.sayfa(govde, W, H, STIL % {"vurgu": vurgu})


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    html = html_kur(spec)
    if "--html" in sys.argv:
        hy = sys.argv[sys.argv.index("--html") + 1]
        with open(hy, "w", encoding="utf-8") as f:
            f.write(html)
        print(hy)
    S.bas(html, sys.argv[2], W, H)


if __name__ == "__main__":
    main()
