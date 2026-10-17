#!/usr/bin/env python3
"""Tek ürün satış ilanı — bayi reklamı düzeni.

Rakip bayilerin sponsorlu gönderilerinde oturmuş bir düzen var ve
satış için çalışan da bu: üstte bayi ve üretici logosu yan yana,
solda model adı dev tipografi, tek iddia cümlesi, üç ikonlu özellik
ve bir çağrı düğmesi; sağda ürün büyük; altta güven şeridi.
Kataloğa değil, tek ürünü satmaya kurulu.

    python3 arac/ilan_html.py <spec.json> <cikti-klasoru>

spec alanları:
  marka        "Bambu Lab"            üstte ve model adının üstünde
  model        "H2D"                  dev başlık
  rozet        "LAZER COMBO"          model altındaki kırmızı etiket
  iddia        "Lazer destekli akıllı üretim."
  spot         bir cümle destek metni
  ozellikler   [[ikon, "Çok Renkli", "Baskı"], ...]   üç tane
  guven        [[ikon, "Orijinal ve", "faturalı"], ...] dört tane
  cagri        "sermenkreatif.com'da"
  gorsel       "urun/kesik/bambulab-h2d-combo.png"
  marka_logo   "marka/bambu-lab.png"  (yoksa marka adı dizgiyle yazılıyor)
  renk         vurgu rengi adı

Üretici logosu `gorsel/marka/` altına konunca otomatik kullanılıyor.
"""
import html as _h
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "arac"))
sys.path.insert(0, os.path.join(KOK, "arac", "html"))

import sistem as S                                          # noqa: E402

W, H = 1080, 1350
SW, SH = 1080, 1920

# Çizgisel ikonlar; hepsi 24x24 kutuda, rengi yazıdan alıyor.
IKON = {
    "renk": '<circle cx="12" cy="12" r="8"/><path d="M12 4v16M4 12h16"/>',
    "lazer": '<path d="M12 3v7M12 14v7M5 8l4 4-4 4M19 8l-4 4 4 4"/>',
    "makara": '<rect x="4" y="6" width="16" height="12" rx="2"/>'
              '<path d="M8 6v12M16 6v12"/>',
    "kalkan": '<path d="M12 3l7 3v6c0 4-3 7-7 9-4-2-7-5-7-9V6z"/>'
              '<path d="M9 12l2 2 4-4"/>',
    "kargo": '<rect x="2" y="7" width="12" height="9" rx="1"/>'
             '<path d="M14 10h4l3 3v3h-7z"/><circle cx="6" cy="18" r="2"/>'
             '<circle cx="17" cy="18" r="2"/>',
    "kart": '<rect x="2" y="5" width="20" height="14" rx="2"/>'
            '<path d="M2 10h20"/>',
    "destek": '<path d="M4 13a8 8 0 0116 0"/>'
              '<rect x="2" y="13" width="4" height="7" rx="1.5"/>'
              '<rect x="18" y="13" width="4" height="7" rx="1.5"/>',
    "kurulum": '<path d="M14 5a4 4 0 00-5 5l-6 6 2 2 6-6a4 4 0 005-5l-2 2'
               '-2-2 2-2z"/>',
    "olcu": '<rect x="2" y="8" width="20" height="8" rx="1"/>'
            '<path d="M7 8v3M12 8v4M17 8v3"/>',
    "isi": '<path d="M10 14V5a2 2 0 114 0v9a4 4 0 11-4 0z"/>',
    "hiz": '<path d="M3 12h7l2-5 2 10 2-5h5"/>',
    "kamera": '<rect x="3" y="7" width="18" height="12" rx="2"/>'
              '<circle cx="12" cy="13" r="3.5"/><path d="M9 7l1.5-2h3L15 7"/>',
}


def E(s):
    return _h.escape(str(s if s is not None else ""))


def ikon(ad):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" '
            'stroke-linejoin="round">%s</svg>' % IKON.get(ad, IKON["kalkan"]))


def _gorsel(yol, kesik=True):
    if not yol:
        return None
    tam = yol if os.path.isabs(yol) else os.path.join(KOK, "gorsel", yol)
    if not os.path.exists(tam):
        return None
    return (S.kesik_uri(tam) or S.foto_uri(tam)) if kesik else S.foto_uri(tam)


STIL = """
.slide{background:
  radial-gradient(90%% 70%% at 78%% 30%%, #ffffff 0%%, #f2f5fa 55%%, #e6ebf3 100%%)}
.ic{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  padding:44px 48px 0}

/* marka kilidi */
.kilit{flex:0 0 auto;display:flex;align-items:center;gap:26px}
.kilit img.bayi{height:44px;width:auto}
.kilit s{width:2px;height:40px;background:#c9d2e0;text-decoration:none}
.kilit img.marka{height:38px;width:auto}
.kilit .ad{font-weight:700;font-size:30px;letter-spacing:-.02em;
  color:#101626}

/* gövde: solda söz, sağda ürün */
.govde{flex:1 1 auto;min-height:0;display:grid;
  grid-template-columns:1fr 0.95fr;gap:18px;
  align-items:stretch;padding:20px 0 0}
/* Üç grup, aralarına kalan yer dağılıyor: ortalayınca
   üstte ve altta ikişer parmak boşluk kalıyordu. */
.soz{display:flex;flex-direction:column;
  justify-content:space-between;padding:14px 0 10px}
.soz .g{display:flex;flex-direction:column}
.soz .ust{font-weight:600;font-size:30px;color:#5a6678;letter-spacing:-.01em}
.soz h1{font-family:Anton;font-size:132px;line-height:.84;
  letter-spacing:.005em;text-transform:uppercase;margin-top:4px}
.rozet{align-self:flex-start;margin-top:16px;background:var(--vr);
  color:#fff;font-family:Anton;font-size:26px;letter-spacing:.06em;
  text-transform:uppercase;padding:9px 18px;border-radius:8px}
.soz h2{font-weight:700;font-size:50px;line-height:1.1;
  letter-spacing:-.025em;margin-top:28px}
.soz h2 i{font-style:normal;color:var(--vr)}
.soz p{font-size:25px;line-height:1.38;color:#5a6678;margin-top:14px;
  max-width:95%%}

.ozellik{display:flex;gap:26px;margin-top:30px}
.ozellik div{flex:1;text-align:center}
.ozellik svg{width:46px;height:46px;color:var(--vr)}
.ozellik b{display:block;font-weight:600;font-size:19px;line-height:1.22;
  margin-top:10px;color:#2a3344}

.dugme{align-self:flex-start;margin-top:32px;background:var(--vr);
  color:#fff;font-weight:700;font-size:28px;letter-spacing:-.01em;
  padding:19px 38px;border-radius:12px;
  box-shadow:0 10px 22px rgba(16,22,38,.18)}

/* Sınıf adı "urun" olamaz: sistem.py onu beyaz ürün
   çerçevesi olarak boyuyor, makinenin arkasında kutu
   çıkıyordu. */
.sahne{position:relative;height:100%%;display:flex;
  align-items:center;justify-content:center}
.sahne img{width:100%%;height:100%%;object-fit:contain;
  filter:drop-shadow(0 26px 30px rgba(16,22,38,.18))}

/* güven şeridi */
.guven{flex:0 0 auto;display:grid;grid-template-columns:repeat(4,1fr);
  background:#fff;border-radius:18px;padding:20px 10px;margin-top:10px;
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.05)}
.guven div{display:flex;align-items:center;gap:12px;padding:0 14px;
  border-left:1px solid #e4e9f1}
.guven div:first-child{border-left:0}
.guven svg{flex:0 0 28px;width:28px;height:28px;color:var(--vr)}
.guven b{font-weight:500;font-size:17px;line-height:1.22;color:#2a3344}
.dip{flex:0 0 auto;display:flex;align-items:center;
  justify-content:space-between;font-family:Mono;font-size:21px;
  color:#5a6678;padding:18px 0 24px}

/* hikaye */
.hik .govde{grid-template-columns:1fr;grid-template-rows:auto 1fr;
  gap:0}
.hik .soz h1{font-size:150px}
.hik .sahne img{height:100%%}
"""


def _parcalar(spec):
    vr = S.RENK.get(spec.get("renk", "kirmizi"), S.RENK["kirmizi"])
    bayi = _gorsel(spec.get("bayi_logo", "marka/sermenkreatif.png"),
                   kesik=False)
    mlogo = _gorsel(spec.get("marka_logo", ""), kesik=False)
    kilit = ('<div class="kilit">%s<s></s>%s</div>'
             % (('<img class="bayi" src="%s" alt="">' % bayi) if bayi
                else '<span class="ad">sermenkreatif</span>',
                ('<img class="marka" src="%s" alt="">' % mlogo) if mlogo
                else '<span class="ad">%s</span>' % E(spec.get("marka", ""))))

    ozl = "".join('<div>%s<b>%s<br>%s</b></div>'
                  % (ikon(i), E(a), E(b))
                  for i, a, b in spec.get("ozellikler", [])[:3])
    guven = "".join('<div>%s<b>%s<br>%s</b></div>' % (ikon(i), E(a), E(b))
                    for i, a, b in spec.get("guven", [])[:4])

    iddia = E(spec.get("iddia", ""))
    if iddia.endswith("."):
        iddia = iddia[:-1] + "<i>.</i>"
    return vr, kilit, ozl, guven, iddia


def ilan(spec, cikti):
    vr, kilit, ozl, guven, iddia = _parcalar(spec)
    uri = _gorsel(spec.get("gorsel"))
    govde = (
        '<div class="ic" style="--vr:%s">%s'
        '<div class="govde"><div class="soz">'
        '<div class="g"><span class="ust">%s</span>'
        '<h1>%s</h1>%s</div>'
        '<div class="g"><h2>%s</h2>%s</div>'
        '<div class="g">%s'
        '<span class="dugme">%s</span></div></div>'
        '<div class="sahne">%s</div></div>'
        '<div class="guven">%s</div>'
        '<div class="dip"><span>@sermenkreatif</span>'
        '<span>sermenkreatif.com</span></div></div>'
        % (vr, kilit, E(spec.get("marka", "")), E(spec.get("model", "")),
           ('<span class="rozet">%s</span>' % E(spec["rozet"]))
           if spec.get("rozet") else "",
           iddia,
           ('<p>%s</p>' % E(spec["spot"])) if spec.get("spot") else "",
           ('<div class="ozellik">%s</div>' % ozl) if ozl else "",
           E(spec.get("cagri", "sermenkreatif.com'da")),
           ('<img src="%s" alt="">' % uri) if uri else "",
           guven))
    S.bas(S.sayfa(govde, W, H, STIL), cikti, W, H)


def hikaye(spec, cikti):
    vr, kilit, ozl, guven, iddia = _parcalar(spec)
    uri = _gorsel(spec.get("gorsel"))
    govde = (
        '<div class="ic hik" style="--vr:%s;padding:70px 56px 0">%s'
        '<div class="govde"><div class="soz">'
        '<span class="ust">%s</span><h1>%s</h1>%s<h2>%s</h2>%s</div>'
        '<div class="sahne">%s</div></div>'
        '<div class="guven">%s</div>'
        '<div class="dip" style="padding-bottom:110px">'
        '<span>@sermenkreatif</span><span>sermenkreatif.com</span></div></div>'
        % (vr, kilit, E(spec.get("marka", "")), E(spec.get("model", "")),
           ('<span class="rozet">%s</span>' % E(spec["rozet"]))
           if spec.get("rozet") else "",
           iddia,
           ('<p>%s</p>' % E(spec["spot"])) if spec.get("spot") else "",
           ('<img src="%s" alt="">' % uri) if uri else "", guven))
    S.bas(S.sayfa(govde, SW, SH, STIL), cikti, SW, SH, kalite=92)


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    klasor = sys.argv[2]
    os.makedirs(klasor, exist_ok=True)
    ilan(spec, os.path.join(klasor, "1.jpg"))
    hikaye(spec, os.path.join(klasor, "hikaye.jpg"))


if __name__ == "__main__":
    main()
