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
import math
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "arac"))
sys.path.insert(0, os.path.join(KOK, "arac", "html"))

import sistem as S                                          # noqa: E402
from urun_karti import BUY                                 # noqa: E402

W, H = 1080, 1350
SW, SH = 1080, 1920

# Dolu, renkli ikonlar — 48x48 kutuda. İnce konturlu sürüm karede
# boş ve cılız duruyordu; bunlar gövdeli, kendi renkleri var.
IKON = {
    # renk çarkı: altı dilim
    "renk": ''.join(
        '<path d="M24 24L%.1f %.1f A20 20 0 0 1 %.1f %.1f Z" fill="%s"/>'
        % (24 + 20 * math.cos(math.radians(a)),
           24 + 20 * math.sin(math.radians(a)),
           24 + 20 * math.cos(math.radians(a + 60)),
           24 + 20 * math.sin(math.radians(a + 60)),
           c)
        for a, c in ((-90, "#e4443f"), (-30, "#f0a92c"), (30, "#f7d93b"),
                     (90, "#39b96a"), (150, "#2f7fe0"), (210, "#8b5cf6")))
    + '<circle cx="24" cy="24" r="7" fill="#fff"/>',
    # lazer: kafa, kırmızı ışın ve tablada kesim izi
    "lazer": '<rect x="16" y="5" width="16" height="12" rx="3" '
             'fill="#2a3344"/>'
             '<rect x="20" y="8" width="8" height="3" rx="1.5" '
             'fill="#9fb0c6"/>'
             '<path d="M20 17h8l-2.6 5h-2.8z" fill="#4a5569"/>'
             '<path d="M24 17 L31 34 h-14 Z" fill="#e4443f" opacity=".3"/>'
             '<rect x="22" y="17" width="4" height="17" rx="2" '
             'fill="#e4443f"/>'
             '<rect x="5" y="34" width="38" height="7" rx="3.5" '
             'fill="#8e9bb0"/>'
             '<circle cx="24" cy="34" r="6" fill="#ffb199" '
             'opacity=".85"/>'
             '<circle cx="24" cy="34" r="2.6" fill="#fff"/>',
    # makara: yuvarlak gövde, sarılı filament ve çıkan tel
    "makara": '<circle cx="22" cy="24" r="18" fill="#2a3344"/>'
              '<circle cx="22" cy="24" r="13.5" fill="#e4443f"/>'
              '<path d="M22 10.5a13.5 13.5 0 0 1 13.5 13.5H22z" '
              'fill="#f07b77"/>'
              '<circle cx="22" cy="24" r="5" fill="#fff"/>'
              '<circle cx="22" cy="24" r="2" fill="#2a3344"/>'
              '<path d="M35 19c6 1.5 8 6 7 12" stroke="#e4443f" '
              'stroke-width="3" stroke-linecap="round" fill="none"/>',
    # oyuncak gönderileri için
    "sekil": '<circle cx="13" cy="14" r="9" fill="#e4443f"/>'
             '<rect x="25" y="5" width="18" height="18" rx="3" '
             'fill="#2476dc"/>'
             '<path d="M24 27 L40 43 H8 Z" fill="#e9b820"/>',
    "disli": '<path d="M24 4l4.2 1.1 2.3 3.7 4.3-.4 2.6 3.5-1.5 4.1 '
             '3.2 2.9-.6 4.3-4 1.7-.6 4.3-4 1.7-3.3-2.8-3.9 1.9-3.5-2.6'
             ' -3.9 1.9-2.6-3.5 1.1-4.2-3.4-2.7 1.1-4.2 4.1-1.4 1.1-4.2'
             ' 4.2-1.1z" fill="#24a256"/>'
             '<circle cx="24" cy="24" r="12" fill="#2b9150"/>'
             '<circle cx="24" cy="24" r="6" fill="#fff"/>',
    "el": '<path d="M17 25V9a3.2 3.2 0 0 1 6.4 0v12" fill="#f0b48a"/>'
          '<path d="M23.4 21V7a3.2 3.2 0 0 1 6.4 0v14" fill="#f6c6a2"/>'
          '<path d="M29.8 22V12a3.1 3.1 0 0 1 6.2 0v16c0 8-5 14-12.4 14'
          'S11 36 11 28v-6a3 3 0 0 1 6 0z" fill="#f0b48a"/>'
          '<path d="M14 30c0 7 4 11 9.6 11" stroke="#d99a6c" '
          'stroke-width="2" fill="none" stroke-linecap="round"/>',
    "istif": '<rect x="7" y="29" width="34" height="9" rx="4" '
             'fill="#e4443f"/>'
             '<rect x="10" y="20" width="28" height="9" rx="4" '
             'fill="#ec842a"/>'
             '<rect x="13" y="11" width="22" height="9" rx="4" '
             'fill="#e9b820"/>'
             '<rect x="16" y="4" width="16" height="8" rx="4" '
             'fill="#24a256"/>',
    "fincan": '<path d="M9 14h24v15a9 9 0 0 1-9 9h-6a9 9 0 0 1-9-9z" '
              'fill="#2476dc"/>'
              '<path d="M9 14h24v6H9z" fill="#4e91e6"/>'
              '<path d="M33 18h4a5 5 0 0 1 0 10h-4" stroke="#2476dc" '
              'stroke-width="4" fill="none" stroke-linecap="round"/>'
              '<rect x="11" y="40" width="20" height="4" rx="2" '
              'fill="#9fb0c6"/>',
    "kalkan": '<path d="M24 4l16 6v11c0 9-6.6 15.6-16 19-9.4-3.4-16-10-16-19'
              'V10z" fill="#e4443f"/>'
              '<path d="M24 8.6L12 13v8c0 6.8 4.7 12 12 14.9z" '
              'fill="#fff" opacity=".16"/>'
              '<path d="M17 24l5 5 10-10" stroke="#fff" stroke-width="4" '
              'fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "kargo": '<rect x="3" y="13" width="25" height="19" rx="3" '
             'fill="#2a3344"/>'
             '<path d="M28 19h8l7 7v6H28z" fill="#9fb0c6"/>'
             '<rect x="30" y="21" width="6" height="5" rx="1" fill="#e9eef5"/>'
             '<circle cx="13" cy="35" r="5" fill="#2a3344"/>'
             '<circle cx="13" cy="35" r="2" fill="#e9eef5"/>'
             '<circle cx="35" cy="35" r="5" fill="#2a3344"/>'
             '<circle cx="35" cy="35" r="2" fill="#e9eef5"/>',
    "kart": '<rect x="4" y="11" width="40" height="26" rx="4" '
            'fill="#2a3344"/><rect x="4" y="18" width="40" height="6" '
            'fill="#9fb0c6"/>'
            '<rect x="9" y="28" width="13" height="4" rx="2" fill="#e9eef5"/>',
    "destek": '<path d="M9 26a15 15 0 0130 0" fill="none" stroke="#2a3344" '
              'stroke-width="5" stroke-linecap="round"/>'
              '<rect x="4" y="24" width="9" height="15" rx="4.5" '
              'fill="#e4443f"/>'
              '<rect x="35" y="24" width="9" height="15" rx="4.5" '
              'fill="#e4443f"/>',
    "kurulum": '<path d="M31 6a11 11 0 00-13.6 13.6L6 31l11 11 11.4-11.4A11 '
               '11 0 0042 17l-6.5 6.5-5-5L37 12z" fill="#2a3344"/>'
               '<circle cx="15" cy="33" r="3" fill="#e9eef5"/>',
    "olcu": '<rect x="3" y="16" width="42" height="16" rx="3" '
            'fill="#f0a92c"/>'
            '<path d="M12 16v7M20 16v10M28 16v7M36 16v10" stroke="#8a5a10" '
            'stroke-width="3" stroke-linecap="round"/>',
    "isi": '<path d="M19 27V11a5 5 0 0110 0v16a9 9 0 11-10 0z" '
           'fill="#e9eef5" stroke="#2a3344" stroke-width="3"/>'
           '<path d="M24 16v12" stroke="#e4443f" stroke-width="5" '
           'stroke-linecap="round"/><circle cx="24" cy="33" r="6" '
           'fill="#e4443f"/>',
    "hiz": '<path d="M4 24h12l5-11 6 22 5-11h12" fill="none" '
           'stroke="#e4443f" stroke-width="5" stroke-linecap="round" '
           'stroke-linejoin="round"/>',
    "kamera": '<rect x="4" y="14" width="40" height="27" rx="4" '
              'fill="#2a3344"/><path d="M17 14l3-5h8l3 5z" fill="#2a3344"/>'
              '<circle cx="24" cy="27" r="9" fill="#9fb0c6"/>'
              '<circle cx="24" cy="27" r="4.5" fill="#e9eef5"/>',
}


def E(s):
    return _h.escape(str(s if s is not None else ""))


def ikon(ad):
    return ('<svg viewBox="0 0 48 48">%s</svg>'
            % IKON.get(ad, IKON["kalkan"]))


def _gorsel(yol, kesik=True):
    if not yol:
        return None
    tam = yol if os.path.isabs(yol) else os.path.join(KOK, "gorsel", yol)
    if not os.path.exists(tam):
        return None
    return (S.kesik_uri(tam) or S.foto_uri(tam)) if kesik else S.foto_uri(tam)


STIL = """
.slide{background:
  radial-gradient(90% 70% at 78% 30%, #ffffff 0%, #f2f5fa 55%, #e6ebf3 100%)}
.ic{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  padding:44px 48px 0}

/* marka kilidi */
.kilit{flex:0 0 auto;display:flex;align-items:center;gap:26px}
.kilit img.bayi{height:54px;width:auto}
.kilit s{width:2px;height:40px;background:#c9d2e0;text-decoration:none}
.kilit img.marka{height:46px;width:auto}
.kilit .ad{font-weight:700;font-size:36px;letter-spacing:-.02em;
  color:#101626}

/* gövde: solda söz, sağda ürün */
.govde{flex:1 1 auto;min-height:0;display:grid;
  grid-template-columns:1.04fr 1fr;gap:14px;
  align-items:stretch;padding:16px 0 0}
/* Üç grup, aralarına kalan yer dağılıyor: ortalayınca
   üstte ve altta ikişer parmak boşluk kalıyordu. */
.soz{display:flex;flex-direction:column;
  justify-content:center;gap:52px;padding:10px 0}
.soz .g{display:flex;flex-direction:column}
.soz .ust{font-weight:600;font-size:35px;color:#5a6678;letter-spacing:-.01em}
.soz h1{font-family:Anton;font-size:var(--h1,152px);
  line-height:1.06;
  letter-spacing:.005em;text-transform:uppercase;margin-top:4px}
.rozet{align-self:flex-start;margin-top:16px;background:var(--vr);
  color:#fff;font-family:Anton;font-size:31px;letter-spacing:.06em;
  text-transform:uppercase;padding:9px 18px;border-radius:8px}
.soz h2{font-weight:700;font-size:62px;line-height:1.08;
  letter-spacing:-.025em}
.soz h2 i{font-style:normal;color:var(--vr)}
.soz p{font-size:30px;line-height:1.36;color:#5a6678;margin-top:18px;
  max-width:96%}

.alt{flex:0 0 auto;display:flex;flex-direction:column;
  align-items:flex-start;gap:24px;margin-top:8px}
.ozellik{width:100%;display:flex;gap:30px;align-items:center}
.ozellik div{flex:1;min-width:0;display:flex;align-items:center;
  gap:14px;text-align:left}
.ozellik svg{flex:0 0 66px;width:66px;height:66px}
.ozellik b{font-weight:600;font-size:24px;line-height:1.18;color:#2a3344}

.dugme{flex:0 0 auto;background:var(--vr);
  color:#fff;font-weight:700;font-size:34px;letter-spacing:-.01em;
  padding:22px 42px;border-radius:12px;
  box-shadow:0 10px 22px rgba(16,22,38,.18)}

/* Sınıf adı "urun" olamaz: sistem.py onu beyaz ürün
   çerçevesi olarak boyuyor, makinenin arkasında kutu
   çıkıyordu. */
.sahne{position:relative;height:100%;display:flex;
  align-items:center;justify-content:center}
.foto-kapak .govde{grid-template-columns:.96fr 1fr}
.sahne.foto{align-self:center;width:100%;max-height:100%;
  border-radius:24px;overflow:hidden;background:#fff;
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.05)}
.sahne.foto img{width:100%;height:100%;object-fit:cover;
  filter:none}
.sahne img{width:100%;height:100%;object-fit:contain;
  filter:drop-shadow(0 26px 30px rgba(16,22,38,.18))}

/* güven şeridi */
.guven{flex:0 0 auto;display:grid;grid-template-columns:repeat(4,1fr);
  background:#fff;border-radius:18px;padding:22px 10px;margin-top:18px;
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.05)}
.guven div{display:flex;align-items:center;gap:12px;padding:0 14px;
  border-left:1px solid #e4e9f1}
.guven div:first-child{border-left:0}
.guven svg{flex:0 0 36px;width:36px;height:36px}
.guven b{font-weight:500;font-size:21px;line-height:1.22;color:#2a3344}
.dip{flex:0 0 auto;display:flex;align-items:center;
  justify-content:space-between;font-family:Mono;font-size:23px;
  color:#5a6678;padding:18px 0 24px}

/* Yığılmış fotoğraf kapağı: yatay fotoğrafta iki sütun dar kalıyor,
   fotoğraf üstte tam genişlikte duruyor. */
.yigin .govde{display:flex;flex-direction:column;gap:0;padding:14px 0 0}
.yigin .vitrin{flex:1 1 auto;min-height:0;width:auto;
  max-width:100%;align-self:center;border-radius:24px;
  overflow:hidden;background:#fff;
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.05)}
.yigin .vitrin img{width:100%;height:100%;object-fit:cover;
  display:block}
.yigin .soz{flex:0 0 auto;justify-content:flex-start;gap:0;
  padding:16px 0 0}
.yigin .soz h1{margin-top:2px}
.yigin .soz h2{margin-top:14px}
.yigin .soz p{margin-top:12px}

/* satış noktaları */
.cagri{display:flex;width:100%;align-items:center;
  justify-content:space-between;gap:22px;flex-wrap:wrap}
.cagri .satis{margin-top:0}
.satis{display:flex;align-items:center;gap:14px;margin-top:18px}
.satis span{display:inline-flex;align-items:center;gap:10px;
  background:#fff;border-radius:999px;padding:13px 24px;
  font-weight:600;font-size:25px;color:#2a3344;
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.07)}
.satis img{height:30px;width:auto;display:block}
.koyu .satis span{background:#1b2440;color:#fff;box-shadow:none}

/* fotoğraf slaytı */
.kare{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  padding-top:18px}
.kare .cerceve{flex:1 1 auto;min-height:0;border-radius:24px;
  overflow:hidden;background:#fff;
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.05)}
.kare .cerceve img{width:100%;height:100%;object-fit:cover;display:block}
.kare .yazi{flex:0 0 auto;padding:26px 4px 0}
.kare .yazi b{display:block;font-weight:700;font-size:46px;
  letter-spacing:-.022em;line-height:1.14}
.kare .yazi b i{font-style:normal;color:var(--vr)}
.kare .yazi span{display:block;font-size:29px;line-height:1.36;
  color:#5a6678;margin-top:12px}

/* kapanış */
.kapanis{color:#fff}
.kapanis h1{font-family:Anton;text-transform:uppercase;font-size:86px;
  line-height:1.02;letter-spacing:.004em;margin-top:34px}
.kapanis h1 em{font-style:normal;color:var(--vr)}
.kapanis .liste{flex:1 1 auto;min-height:0;display:flex;
  flex-direction:column;justify-content:center;gap:16px;padding:30px 0}
.kapanis .liste div{flex:1 1 0;max-height:190px;display:flex;
  align-items:center;gap:22px;background:#1b2440;border-radius:18px;
  padding:22px 28px;border-left:8px solid var(--vr)}
.kapanis .liste b{flex:0 0 190px;font-family:Mono;font-size:21px;
  letter-spacing:.07em;text-transform:uppercase;color:var(--vr)}
.kapanis .liste span{flex:1;font-size:31px;font-weight:600;line-height:1.24}
.kapanis .dugme{align-self:flex-start;margin-top:4px}
.kapanis .dip{color:#96a4c0}

/* hikaye */
.hik .govde{grid-template-columns:1fr;
  grid-template-rows:auto minmax(0,1fr);gap:0}
.hik .soz{justify-content:flex-start;gap:30px}

.hik .sahne{min-height:0;align-items:flex-end}
/* Kaynak kesim 338px; tam genişliğe yayınca bulanıklaşıyor,
   yüksekliğe oturtup genişliği serbest bırakıyoruz. */
.hik .sahne img{width:auto;max-width:100%;height:100%}
"""


def _parcalar(spec):
    vr = S.RENK.get(spec.get("renk", "kirmizi"), S.RENK["kirmizi"])
    bayi = _gorsel(spec.get("bayi_logo", "marka/sermenkreatif.png"),
                   kesik=False)
    mlogo = _gorsel(spec.get("marka_logo", ""), kesik=False)
    sol = (('<img class="bayi" src="%s" alt="">' % bayi) if bayi
           else '<span class="ad">sermenkreatif</span>')
    # Kendi ürünümüzde ikinci marka yok: ayraç ve boş etiket basılmasın.
    sag = ''
    if mlogo:
        sag = '<s></s><img class="marka" src="%s" alt="">' % mlogo
    elif spec.get("marka"):
        sag = '<s></s><span class="ad">%s</span>' % E(spec["marka"])
    kilit = '<div class="kilit">%s%s</div>' % (sol, sag)

    ozl = "".join('<div>%s<b>%s<br>%s</b></div>'
                  % (ikon(i), E(a), E(b))
                  for i, a, b in spec.get("ozellikler", [])[:3])
    guven = "".join('<div>%s<b>%s<br>%s</b></div>' % (ikon(i), E(a), E(b))
                    for i, a, b in spec.get("guven", [])[:4])

    iddia = E(spec.get("iddia", ""))
    if iddia.endswith("."):
        iddia = iddia[:-1] + "<i>.</i>"
    return vr, kilit, ozl, guven, iddia


H1_KADEME = ((6, 152), (10, 132), (14, 106), (20, 86), (10 ** 6, 72))


def _h1_punto(ad):
    for sinir, px in H1_KADEME:
        if len(ad) <= sinir:
            return px
    return 72


def _oran(yol):
    """Fotoğrafın en/boy oranı; kapak düzenini bu seçiyor."""
    if not yol:
        return None
    tam = yol if os.path.isabs(yol) else os.path.join(KOK, "gorsel", yol)
    if not os.path.exists(tam):
        return None
    from PIL import Image
    w, h = Image.open(tam).size
    return w / float(h)


def _satis(spec):
    """Satış noktası çipleri: site ve pazaryeri.

    Pazaryeri logosu gorsel/marka/ altına konunca kullanılıyor; yoksa
    adı dizgiyle yazılıyor (logoyu kendimiz çizmiyoruz)."""
    ciz = []
    for ad, logo in spec.get("satis", [["sermenkreatif.com", ""]]):
        uri = _gorsel(logo, kesik=False) if logo else None
        ciz.append('<span>%s%s</span>'
                   % (('<img src="%s" alt="">' % uri) if uri else "",
                      E(ad)))
    return '<div class="satis">%s</div>' % "".join(ciz) if ciz else ""


def _dip(spec):
    sag = spec.get("dip_sag") or "sermenkreatif.com"
    return ('<div class="dip"><span>@sermenkreatif</span>'
            '<span>%s</span></div>' % E(sag))


def ilan(spec, cikti):
    vr, kilit, ozl, guven, iddia = _parcalar(spec)
    foto = bool(spec.get("kapak_foto"))
    uri = (_gorsel(spec["kapak_foto"], kesik=False) if foto
           else _gorsel(spec.get("gorsel")))
    # Dikey fotoğraf sağ sütuna oturuyor; yatay fotoğraf o sütunda
    # küçük kalıyordu, onu tam genişlikte üste alıyoruz. İki düzende
    # de object-fit contain: kadrajdan hiçbir şey kesilmiyor.
    oran = _oran(spec.get("kapak_foto")) if foto else None
    yigin = bool(oran and oran > 0.95)
    sinif = (" foto-kapak" if foto else "") + (" yigin" if yigin else "")
    im = ('<img src="%s" alt="">' % uri) if uri else ""
    soz = ('<div class="soz">'
           '<div class="g"><span class="ust">%s</span><h1>%s</h1>%s</div>'
           '<div class="g"><h2>%s</h2>%s</div></div>'
           % (E(spec.get("ust") or spec.get("marka", "")),
              E(spec.get("model", "")),
              ('<span class="rozet">%s</span>' % E(spec["rozet"]))
              if spec.get("rozet") else "",
              iddia,
              ("" if yigin else
               ('<p>%s</p>' % E(spec["spot"])) if spec.get("spot")
               else "")))
    if yigin:
        # Kutu fotoğrafın oranını alıyor: sabit kutuda kenarlar kesiliyordu.
        govde_ic = ('<div class="vitrin" style="aspect-ratio:%s">%s</div>%s'
                    % (("%.4f" % oran), im, soz))
    else:
        if foto:
            govde_ic = ('%s<div class="sahne foto" '
                        'style="aspect-ratio:%s">%s</div>'
                        % (soz, "%.4f" % oran, im))
        else:
            govde_ic = '%s<div class="sahne">%s</div>' % (soz, im)
    govde = (
        '<div class="ic%s" style="--vr:%s;--h1:%dpx">%s'
        '<div class="govde">%s</div>'
        '<div class="alt">%s<div class="cagri">'
        '<span class="dugme">%s</span>%s</div></div>'
        '<div class="guven">%s</div>%s</div>'
        % (sinif, vr, _h1_punto(spec.get("model", "")), kilit, govde_ic,
           ('<div class="ozellik">%s</div>' % ozl) if ozl else "",
           E(spec.get("cagri", "sermenkreatif.com'da")),
           _satis(spec), guven, _dip(spec)))
    S.bas(S.sayfa(govde, W, H, STIL), cikti, W, H)


def slayt(spec, s, cikti):
    """Tek fotoğraflık ara kare: görsel büyük, altında iki satır."""
    vr, kilit, _ozl, _guven, _iddia = _parcalar(spec)
    uri = _gorsel(s.get("foto"), kesik=False)
    oran = _oran(s.get("foto"))
    bas = E(s.get("baslik", ""))
    if "|" in bas:
        a, b = bas.split("|", 1)
        bas = "%s<i>%s</i>" % (a, b)
    govde = (
        '<div class="ic" style="--vr:%s">%s'
        '<div class="kare"><div class="cerceve"%s>%s</div>'
        '<div class="yazi"><b>%s</b>%s</div></div>%s</div>'
        % (vr, kilit,
           (' style="aspect-ratio:%.4f"' % oran) if oran else "",
           ('<img src="%s" alt="">' % uri) if uri else "", bas,
           ('<span>%s</span>' % E(s["metin"])) if s.get("metin") else "",
           _dip(spec)))
    S.bas(S.sayfa(govde, W, H, STIL), cikti, W, H)


def kapanis(spec, cikti):
    """Koyu kapanış: ne aldığın, kime uyduğu ve çağrı."""
    vr, kilit, _ozl, guven, _iddia = _parcalar(spec)
    k = spec.get("kapanis") or {}
    bas = E(BUY(k.get("satir1", "")))
    if k.get("satir2"):
        bas += "<br><em>%s</em>" % E(BUY(k["satir2"]))
    govde = (
        '<div class="ic kapanis" style="--vr:%s">%s<h1>%s</h1>'
        '<div class="liste">%s</div>'
        '<span class="dugme">%s</span>%s%s</div>'
        % (vr, kilit, bas,
           "".join('<div><b>%s</b><span>%s</span></div>' % (E(BUY(a)), E(b))
                   for a, b in k.get("satirlar", [])[:4]),
           E(spec.get("cagri", "sermenkreatif.com\'da")),
           _satis(spec), _dip(spec)))
    S.bas(S.sayfa(govde, W, H, STIL, sinif="koyu"), cikti, W, H)


def uret(spec, klasor):
    os.makedirs(klasor, exist_ok=True)
    n = 1
    ilan(spec, os.path.join(klasor, "1.jpg"))
    for s in spec.get("slaytlar", []):
        n += 1
        slayt(spec, s, os.path.join(klasor, "%d.jpg" % n))
    if spec.get("kapanis"):
        n += 1
        kapanis(spec, os.path.join(klasor, "%d.jpg" % n))
    hikaye(spec, os.path.join(klasor, "hikaye.jpg"))
    return n


def hikaye(spec, cikti):
    vr, kilit, ozl, guven, iddia = _parcalar(spec)
    foto = bool(spec.get("kapak_foto"))
    uri = (_gorsel(spec["kapak_foto"], kesik=False) if foto
           else _gorsel(spec.get("gorsel")))
    govde = (
        '<div class="ic hik" style="--vr:%s;--h1:%dpx;padding:70px 56px 0">%s'
        '<div class="govde"><div class="soz">'
        '<span class="ust">%s</span><h1>%s</h1>%s<h2>%s</h2>%s</div>'
        '<div class="sahne%s">%s</div></div>'
        '<div class="guven">%s</div>'
        '%s</div>'
        % (vr, int(_h1_punto(spec.get("model", "")) * 1.12), kilit,
           E(spec.get("ust") or spec.get("marka", "")),
           E(spec.get("model", "")),
           ('<span class="rozet">%s</span>' % E(spec["rozet"]))
           if spec.get("rozet") else "",
           iddia,
           ('<p>%s</p>' % E(spec["spot"])) if spec.get("spot") else "",
           " foto" if foto else "",
           ('<img src="%s" alt="">' % uri) if uri else "", guven,
           _dip(spec).replace('class="dip"',
                              'class="dip" style="padding-bottom:190px"')))
    S.bas(S.sayfa(govde, SW, SH, STIL), cikti, SW, SH, kalite=92)


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    klasor = sys.argv[2]
    print("%d kare + hikaye: %s" % (uret(spec, klasor), klasor))


if __name__ == "__main__":
    main()
