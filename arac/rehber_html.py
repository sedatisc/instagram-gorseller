#!/usr/bin/env python3
"""Rehber / proje / ürün gönderisi şablonu — HTML/CSS sürümü.

`uret.py` ile aynı spec dosyasını okuyor. Fark iki tane:

1. Yedi ayrı kapak tipi (izgara, rakam, carpisma, liste, urun, pano,
   klasik) birikmişti; her biri kendi düzenini çiziyordu ve akışta yedi
   ayrı hesap gibi duruyorlardı. Hepsi tek kapağa indi: üstte etiket,
   iri başlık, spot; gövde içeriğe göre değişiyor (kart ızgarası, iri
   rakam, ürün fotoğrafı, ikili karşılaştırma, rozet + tablo).
2. Renk ve yazı `arac/html/sistem.py`den geliyor, yani ürün kartlarıyla
   aynı yerden. Eski `zemin` adları (okyanus, kiraz, orman...) artık
   okunmuyor; vurgu rengini kategori veriyor.

    python3 arac/rehber_html.py <spec.json> <cikti-klasoru>

Desteklenmeyen tek parça `cizim`: serbest çizim komutları, tek bir
slaytta kullanılıyor. O slayt gelirse başlık ve açıklamayla basılıyor,
çizim atlanıyor ve uyarı veriyor.
"""
import html as _h
import json
import re
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "arac"))
sys.path.insert(0, os.path.join(KOK, "arac", "html"))

import sistem as S                                          # noqa: E402
import cizim_png                                            # noqa: E402
from urun_karti import BUY                                  # noqa: E402

W, H = 1080, 1350
SW, SH = 1080, 1920

# Vurgu rengini kategori veriyor; eski spec'lerdeki "zemin" adları
# (okyanus, kiraz, orman) eski degrade sistemine aitti, okunmuyor.
KAT_RENK = {"3dbaski": "turuncu", "proje": "mor",
            "urun": "yesil", "kurumsal": "kirmizi",
            "elektronik": "turkuaz"}
KAT_ETIKET = {"3dbaski": "AYAR & REHBER", "proje": "PROJE & ATÖLYE",
              "urun": "ÜRÜN & MAĞAZA", "kurumsal": "SERMEN KREATİF",
              "elektronik": "ELEKTRONİK"}


def E(s):
    return _h.escape(str(s if s is not None else ""))


def _renk(ad, vars_):
    if ad in (None, "", "tema"):
        return vars_
    return S.RENK.get(ad, vars_)


def _gorsel(yol):
    if not yol:
        return None
    for aday in (os.path.join(KOK, "gorsel", yol), os.path.join(KOK, yol)):
        if os.path.exists(aday):
            return S.foto_uri(aday)
    return None


STIL = """
.ic{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  padding:40px 40px 0}

/* ---- ortak başlık bloğu ---- */
.tepe{flex:0 0 auto}
.kas{display:flex;align-items:center;gap:14px;font-family:Mono;
  font-size:21px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--vr)}
.kas s{flex:0 0 46px;height:3px;background:var(--vr);text-decoration:none}
/* line-height 1.02: .94'te iki satırlı başlıkta Ğ ve İ üst satıra
   biniyordu, Anton'un kasa yüksekliği buna yer bırakmıyor. */
.tepe h1{font-family:Anton;text-transform:uppercase;line-height:1.02;
  letter-spacing:.004em;font-size:90px;margin-top:18px}
.tepe h1 em{font-style:normal;color:var(--vr)}
.tepe .spot{font-size:31px;line-height:1.34;color:#5a6678;margin-top:18px;
  max-width:94%}
.rozetler{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.rozetler span{font-family:Mono;font-size:20px;letter-spacing:.05em;
  padding:10px 18px;border-radius:999px;border:2px solid var(--rz);
  color:var(--rz)}

/* ---- gövde ---- */
.govde{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  justify-content:center;gap:14px;padding:26px 0}

/* kart ızgarası */
.kartlar{flex:1 1 auto;min-height:0;display:grid;
  grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:16px}
.kartlar .k{display:flex;flex-direction:column;justify-content:center;
  background:#fff;border-radius:18px;padding:24px 28px;
  border-left:7px solid var(--kr);
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.05)}
.kartlar .k.genis{grid-column:1/3}
.kartlar .k b{display:block;font-family:Mono;font-size:21px;
  letter-spacing:.09em;text-transform:uppercase;color:var(--kr)}
.kartlar .k strong{display:block;font-size:50px;line-height:1.04;
  letter-spacing:-.02em;margin-top:8px}
.kartlar .k span{display:block;font-size:26px;color:#5a6678;margin-top:10px;
  line-height:1.3}

/* İri rakam kendi panelinde: çıplak bırakılınca karenin ortasında
   boşlukta yüzüyordu. */
.rakam{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;text-align:center;
  background:#fff;border-radius:24px;padding:30px;
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.05)}
.rakam b{display:block;font-family:Anton;font-size:168px;line-height:.88;
  color:var(--vr);letter-spacing:-.01em}
.rakam span{display:block;font-size:36px;color:#101626;margin-top:18px;
  font-weight:600}

/* ikili karşılaştırma */
/* İki kutu kalan yeri paylaşıyor: içerik az olduğu için karenin
   ortasında küçücük kalıp altını üstünü boş bırakıyorlardı. */
.ikili{flex:1 1 auto;min-height:0;display:grid;
  grid-template-columns:1fr 1fr;gap:16px;
  align-items:start;align-content:center}
.ikili .y{display:flex;flex-direction:column;
  background:#fff;border-radius:20px;padding:30px;
  border-top:8px solid var(--kr);
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.05)}
.ikili .y b{display:block;font-family:Anton;font-size:58px;color:var(--kr);
  text-transform:uppercase;line-height:1}
.ikili .y span{display:block;font-size:28px;color:#2a3344;margin-top:16px;
  line-height:1.32}

/* tablo */
.tablo{display:flex;flex-direction:column}
.tablo .sr{display:flex;align-items:baseline;justify-content:space-between;
  gap:24px;border-top:2px solid #d6dde8;padding:16px 2px 0;margin-top:14px}
.tablo .sr:first-child{border-top:0;margin-top:0;padding-top:0}
/* Slaytta tablo kalan yeri paylaşıyor: sabit satırda kare ortasında
   yüzüyor, altında ve üstünde avuç içi kadar boşluk kalıyordu. */
.slayt .tablo{flex:1 1 auto;min-height:0}
.slayt .tablo .sr{flex:1 1 0;min-height:68px;max-height:136px;
  align-items:center}
.tablo .sr b{font-family:Mono;font-weight:400;font-size:24px;color:#5a6678;
  letter-spacing:.06em;text-transform:uppercase}
.tablo .sr span{font-size:38px;font-weight:600;letter-spacing:-.015em;
  text-align:right;white-space:nowrap}

/* devre şeması */
.sema{flex:0 1 auto;min-height:0;max-height:100%;width:100%;
  align-self:center;display:flex;align-items:center;
  justify-content:center;background:#fff;border-radius:24px;
  padding:26px 30px;
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.05)}
.sema img{width:100%;height:100%;object-fit:contain}
.slayt .sema{flex:1 1 auto;max-height:none}

/* Görselsiz slaytın tipografik kurgusu: giriş cümlesi iri,
   kalanı gövde puntosunda; ikisi kareyi dolduruyor. */
.soz{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  justify-content:center;padding:10px 0 20px}
.soz::before{content:"";flex:0 0 auto;width:120px;height:9px;
  border-radius:5px;background:var(--vr);margin-bottom:38px}
.soz .gir{font-size:var(--gir);line-height:1.18;font-weight:600;
  letter-spacing:-.022em;color:#101626;max-width:97%}
.soz .kal{font-size:var(--kal);line-height:1.42;color:#5a6678;
  margin-top:30px;max-width:96%}

/* satırlar: etiket + açıklama */
.satirlar{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  justify-content:center;gap:16px}
.slayt .satirlar .sr,.kapak .satirlar .sr{flex:1 1 0;max-height:260px;
  align-items:center}
.satirlar .sr{display:flex;gap:20px;background:#fff;border-radius:16px;
  padding:20px 24px;border-left:7px solid var(--vr);
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.05)}
.satirlar .sr b{flex:0 0 168px;font-family:Mono;font-size:21px;
  letter-spacing:.07em;text-transform:uppercase;color:var(--vr);
  padding-top:3px}
.satirlar .sr span{flex:1;font-size:28px;line-height:1.32;color:#2a3344}

/* vurgu: yan yana rakamlar */
.vurgu{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:14px}
.vurgu .v{background:#fff;border-radius:18px;padding:26px 18px;
  text-align:center;box-shadow:0 1px 0 rgba(16,22,38,.05),
  0 0 0 1px rgba(16,22,38,.05)}
.vurgu .v b{display:block;font-family:Anton;font-size:64px;line-height:.9;
  color:var(--vr)}

/* fotoğraf */
.foto{flex:1 1 auto;min-height:0;border-radius:22px;overflow:hidden;
  background:#fff;box-shadow:0 1px 0 rgba(16,22,38,.05),
  0 0 0 1px rgba(16,22,38,.05)}
.foto img{width:100%;height:100%;object-fit:cover;
  object-position:50% var(--odak,50%)}

/* Pano: iki-üç sütunlu karşılaştırma. Tek karelik gönderiler, en
   yoğun düzen; sütun başlığı renkli, altında ürün, sonra özellik ve
   kullanım satırları. */
/* align-items:start — sütunlar içeriğin boyunda kalıyor, artan yer
   ızgaranın altında beyaz delik değil, üstte ve altta eşit boşluk
   oluyor. */
.sutunlar{flex:1 1 auto;min-height:0;display:grid;gap:12px;
  grid-auto-flow:column;grid-auto-columns:1fr;
  align-items:start;align-content:center}
/* padding-bottom: son madde kartın yuvarlak köşesine değip
   kırpılıyordu. */
.sutunlar .s{background:#fff;border-radius:18px;overflow:hidden;
  display:flex;flex-direction:column;padding-bottom:18px;
  box-shadow:0 1px 0 rgba(16,22,38,.05), 0 0 0 1px rgba(16,22,38,.05)}
.sutunlar .s header{background:var(--kr);color:#fff;padding:16px 18px}
.sutunlar .s header b{display:block;font-family:Anton;font-size:34px;
  text-transform:uppercase;line-height:1.04;letter-spacing:.01em}
.sutunlar .s header span{display:block;font-family:Mono;font-size:16px;
  letter-spacing:.06em;margin-top:6px;opacity:.9}
.sutunlar .s figure{flex:0 0 auto;height:260px;margin:12px 12px 0;
  border-radius:12px;background:
    radial-gradient(118% 86% at 50% 6%, #fff 0%, #f5f7fb 56%, #e7ebf3 100%);
  display:flex;align-items:center;justify-content:center;padding:10px}
.sutunlar .s figure img{width:92%;height:88%;object-fit:contain;
  filter:drop-shadow(0 8px 10px rgba(16,22,38,.13))}
.sutunlar .s ul{list-style:none;margin:12px 14px 0;display:flex;
  flex-direction:column;gap:8px}
.sutunlar .s ul.kul{margin-top:10px;padding-top:10px;
  border-top:2px solid #e4e9f1}
.sutunlar .s li{font-size:20px;line-height:1.26;color:#2a3344;
  padding-left:14px;position:relative}
.sutunlar .s li::before{content:"";position:absolute;left:0;top:8px;
  width:6px;height:6px;border-radius:50%;background:var(--kr)}
.sutunlar .s ul.kul li{color:#5a6678}
.ipucu{flex:0 0 auto;display:flex;align-items:center;gap:16px;
  background:#1a2440;border-radius:16px;padding:18px 24px;margin-top:12px}
.ipucu b{font-family:Mono;font-size:17px;letter-spacing:.09em;
  text-transform:uppercase;color:var(--vr);white-space:nowrap}
.ipucu span{font-size:22px;line-height:1.34;color:#e7ebf3}

/* slayt başlığı */
.slayt h2{font-weight:700;font-size:52px;line-height:1.07;
  letter-spacing:-.022em}
.slayt .ac{font-size:26px;line-height:1.38;color:#5a6678;margin-top:14px;
  max-width:95%}

/* ---- kapanış ---- */
.kapanis h1{font-family:Anton;text-transform:uppercase;font-size:84px;
  line-height:.95}
.kapanis h1 em{font-style:normal;color:var(--vr)}
.kriter{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  gap:12px;padding:30px 0}
.kriter .sr{flex:1 1 0;min-height:76px;max-height:300px;display:flex;
  align-items:center;gap:24px;background:#1a2440;border-radius:14px;
  padding:14px 26px;position:relative;overflow:hidden}
.kriter .sr::before{content:"";position:absolute;left:0;top:14px;bottom:14px;
  width:6px;border-radius:3px;background:var(--vr)}
.kriter .sr b{flex:0 0 300px;font-family:Mono;font-size:22px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--vr)}
.kriter .sr span{flex:1;font-size:34px;font-weight:600;color:#fff;
  letter-spacing:-.012em}
.kutu{flex:0 0 auto;background:#1a2440;border-radius:16px;padding:22px 26px;
  font-size:22px;line-height:1.4;color:#d6dde8}

/* ---- hikaye ---- */
.hik .tepe h1{font-size:92px}
.hik .spot{font-size:32px}
.hik .cta{margin-top:auto;text-align:center;padding-bottom:210px}
.hik .cta b{display:block;font-weight:700;font-size:42px}
.hik .cta span{display:block;font-family:Mono;font-size:28px;color:#5a6678;
  margin-top:14px}
"""


# ------------------------------------------------------------- parçalar
def _kunye(spec, orta=""):
    return ('<div class="kunye"><span>@sermenkreatif</span>'
            '<span class="orta">%s</span>'
            '<span class="sag">sermenkreatif.com</span></div>' % E(orta))


def _basliklar(k, vr, etiket):
    s1, s2 = k.get("satir1", ""), k.get("satir2", "")
    ust = k.get("ustbilgi") or etiket
    # "rakam" kapaklarında satir1 yok, başlık ustbilgi'de duruyordu;
    # kare başlıksız çıkıp iri rakam havada kalıyordu.
    if not s1 and k.get("ustbilgi"):
        s1, ust = k["ustbilgi"], etiket
    bas = E(BUY(s1))
    if s2:
        bas += "<br><em>%s</em>" % E(BUY(s2))
    rz = ""
    if k.get("rozetler"):
        rz = '<div class="rozetler">%s</div>' % "".join(
            '<span style="--rz:%s">%s</span>' % (_renk(r[1], vr), E(r[0]))
            for r in k["rozetler"][:4])
    return ('<div class="tepe"><div class="kas"><s></s>%s</div>'
            '<h1>%s</h1>%s%s</div>'
            % (E(ust), bas,
               ('<p class="spot">%s</p>' % E(k["spot"]))
               if k.get("spot") else "", rz))


def _kart_izgara(kartlar, vr):
    # İki sütunlu ızgarada tek başına kalan kart yanında delik
    # bırakıyordu; satırı tek dolduruyorsa tam genişliğe çıkıyor.
    kartlar = [dict(c) for c in kartlar[:6]]
    sut = 0
    for i, c in enumerate(kartlar):
        if c.get("genis"):
            if sut == 1:
                kartlar[i - 1]["genis"] = True
            sut = 0
        else:
            sut = (sut + 1) % 2
    if sut == 1:
        kartlar[-1]["genis"] = True

    ic = []
    for c in kartlar:
        kr = _renk(c.get("renk"), vr)
        ic.append('<div class="k%s" style="--kr:%s"><b>%s</b>'
                  '<strong>%s</strong>%s</div>'
                  % (" genis" if c.get("genis") else "", kr,
                     E(BUY(c.get("etiket", ""))), E(c.get("deger", "")),
                     ('<span>%s</span>' % E(c["alt"])) if c.get("alt") else ""))
    return '<div class="kartlar">%s</div>' % "".join(ic)


def _sutunlar(k, vr):
    ic = []
    for s in k["sutunlar"][:3]:
        kr = _renk(s.get("renk"), vr)
        uri = _gorsel(s.get("gorsel"))
        ozl = "".join("<li>%s</li>" % E(b)
                      for _, b in (s.get("ozellikler") or [])[:4])
        kul = "".join("<li>%s</li>" % E(b)
                      for _, b in (s.get("kullanim") or [])[:3])
        ic.append(
            '<article class="s" style="--kr:%s"><header><b>%s</b>%s</header>'
            '%s<ul>%s</ul>%s</article>'
            % (kr, E(s.get("baslik", "")),
               ('<span>%s</span>' % E(s["alt"])) if s.get("alt") else "",
               ('<figure><img src="%s" alt=""></figure>' % uri) if uri else "",
               ozl, ('<ul class="kul">%s</ul>' % kul) if kul else ""))
    govde = '<div class="sutunlar">%s</div>' % "".join(ic)
    if k.get("ipucu"):
        govde += ('<div class="ipucu"><b>hangisi</b><span>%s</span></div>'
                  % E(k["ipucu"]))
    return govde


def _sema_kirpik(ogeler, kutu):
    """Slaytta şemanın vurgulanan bölgesi."""
    yol = cizim_png.kirpilmis(ogeler, kutu)
    if not yol:
        return ""
    # Slaytta kart kalan yeri dolduruyor; oranını alsaydı yassı
    # kırpmada altta üstte boş kağıt kalıyordu.
    return '<div class="sema"><img src="%s" alt=""></div>' % S.foto_uri(yol)


def _sema(ogeler):
    """Devre şeması: eski çizim motoru PNG basıyor, kapak onu
    görsel olarak yerleştiriyor."""
    yol = cizim_png.onbellekli(ogeler)
    if not yol:
        return ""
    from PIL import Image
    w, h = Image.open(yol).size
    # Kutu çizimin oranını alıyor: sabit kutuda geniş şema üstte ve
    # altta kocaman beyaz boşluk bırakıyordu.
    return ('<div class="sema" style="aspect-ratio:%d/%d">'
            '<img src="%s" alt=""></div>' % (w, h, S.foto_uri(yol)))


def _govde_kapak(k, vr):
    """Kapağın gövdesi içeriğe göre değişiyor; eski yedi kapak tipi
    buraya iniyor."""
    if k.get("cizim"):
        return _sema(k["cizim"])
    if k.get("sutunlar"):
        return _sutunlar(k, vr)
    if k.get("kartlar"):
        return _kart_izgara(k["kartlar"], vr)
    if k.get("satirlar"):
        return '<div class="satirlar">%s</div>' % "".join(
            '<div class="sr"><b>%s</b><span>%s</span></div>'
            % (E(BUY(x.get("etiket", ""))), E(x.get("deger", "")))
            for x in k["satirlar"][:6])
    if k.get("rakam"):
        return ('<div class="rakam"><b>%s</b>%s</div>'
                % (E(k["rakam"]),
                   ('<span>%s</span>' % E(k["rakam_alt"]))
                   if k.get("rakam_alt") else ""))
    if k.get("sol_etiket") or k.get("sag_etiket"):
        return ('<div class="ikili">'
                '<div class="y" style="--kr:%s"><b>%s</b><span>%s</span></div>'
                '<div class="y" style="--kr:%s"><b>%s</b><span>%s</span></div>'
                '</div>'
                % (vr, E(k.get("sol_etiket", "")), E(k.get("sol_metin", "")),
                   S.RENK["mavi"], E(k.get("sag_etiket", "")),
                   E(k.get("sag_metin", ""))))
    uri = _gorsel(k.get("gorsel"))
    if uri:
        ozet = ""
        if k.get("ozet"):
            ozet = '<div class="tablo">%s</div>' % "".join(
                '<div class="sr"><b>%s</b><span>%s</span></div>'
                % (E(BUY(a)), E(b)) for a, b in k["ozet"][:4])
        return ('<div class="foto" style="--odak:%d%%">'
                '<img src="%s" alt=""></div>%s'
                % (int(float(k.get("odak", .5)) * 100), uri, ozet))
    if k.get("tablo"):
        return '<div class="tablo">%s</div>' % "".join(
            '<div class="sr"><b>%s</b><span>%s</span></div>'
            % (E(BUY(a)), E(b)) for a, b in k["tablo"][:6])
    return ""


def kapak(spec, cikti):
    kat = spec.get("kategori", "3dbaski")
    vr = S.RENK[KAT_RENK.get(kat, "turuncu")]
    k = spec.get("kapak") or {}
    govde = ('<div class="ic" style="--vr:%s">%s<div class="govde">%s</div>'
             '</div>%s'
             % (vr, _basliklar(k, vr, KAT_ETIKET.get(kat, "")),
                _govde_kapak(k, vr), _kunye(spec, k.get("marka_alt", ""))))
    S.bas(S.sayfa(govde, W, H, STIL), cikti, W, H)


def _govde_slayt(s, vr, spec=None):
    if s.get("tablo"):
        return '<div class="tablo">%s</div>' % "".join(
            '<div class="sr"><b>%s</b><span>%s</span></div>'
            % (E(BUY(a)), E(b)) for a, b in s["tablo"][:7])
    if s.get("satirlar"):
        return '<div class="satirlar">%s</div>' % "".join(
            '<div class="sr"><b>%s</b><span>%s</span></div>'
            % (E(BUY(a)), E(b)) for a, b in s["satirlar"][:5])
    # "vurgu" eski Pillow hattında kapak çiziminde karartılacak
    # kutunun koordinatlarıydı; sayısalsa içerik değil, atlanıyor.
    vu = s.get("vurgu")
    if vu and len(vu) == 4 and all(isinstance(v, (int, float)) for v in vu):
        ciz = ((spec or {}).get("kapak") or {}).get("cizim")
        if ciz:
            kare = _sema_kirpik(ciz, vu)
            if kare:
                return kare
    if vu and not all(isinstance(v, (int, float)) for v in vu):
        return '<div class="vurgu">%s</div>' % "".join(
            '<div class="v"><b>%s</b></div>' % E(v) for v in vu[:4])
    if s.get("ikili"):
        return '<div class="ikili">%s</div>' % "".join(
            '<div class="y" style="--kr:%s"><b>%s</b><span>%s</span></div>'
            % (_renk(r, vr), E(BUY(et)), E(m)) for et, r, m in s["ikili"][:2])
    uri = _gorsel(s.get("foto"))
    if uri:
        return ('<div class="foto" style="--odak:%d%%">'
                '<img src="%s" alt=""></div>'
                % (int(float(s.get("odak", .5)) * 100), uri))
    if s.get("cizim"):
        print("   ! çizim slaytı atlandı: %s" % s.get("baslik", ""))
    return ""


def _cumleler(metin):
    """İlk cümle giriş, kalanı gövde."""
    p = re.split(r"(?<=[.!?])\s+", (metin or "").strip())
    p = [c for c in p if c]
    return (p[0] if p else ""), " ".join(p[1:])


# Metin uzunluğuna göre punto: tek ölçüde kısa metin kareyi boş,
# uzun metin taşkın bırakıyordu.
KADEME = ((120, 86, 42), (200, 76, 39), (300, 66, 37),
          (430, 57, 34), (10 ** 6, 49, 31))


def _punto(n):
    for sinir, gir, kal in KADEME:
        if n <= sinir:
            return gir, kal
    return 49, 31


def slayt(spec, s, cikti):
    kat = spec.get("kategori", "3dbaski")
    vr = S.RENK[KAT_RENK.get(kat, "turuncu")]
    ic = _govde_slayt(s, vr, spec)
    if ic:
        ust = ('<p class="ac">%s</p>' % E(s["aciklama"])) \
            if s.get("aciklama") else ""
    else:
        # Görseli olmayan slayt: metni tipografiyle kuruyoruz,
        # yoksa karenin üçte ikisi boş kalıyordu.
        gir, kalan = _cumleler(s.get("aciklama", ""))
        pg, pk = _punto(len(gir) + len(kalan))
        ust = ""
        ic = ('<div class="soz" style="--gir:%dpx;--kal:%dpx">'
              '<p class="gir">%s</p>%s</div>'
              % (pg, pk, E(gir),
                 ('<p class="kal">%s</p>' % E(kalan)) if kalan else ""))
    govde = ('<div class="ic slayt" style="--vr:%s">'
             '<div class="tepe"><div class="kas"><s></s>%s</div>'
             '<h2 style="margin-top:16px">%s</h2>%s</div>'
             '<div class="govde">%s</div></div>%s'
             % (vr, E(KAT_ETIKET.get(kat, "")), E(s.get("baslik", "")),
                ust, ic, _kunye(spec)))
    S.bas(S.sayfa(govde, W, H, STIL), cikti, W, H)


def kapanis(spec, cikti):
    kat = spec.get("kategori", "3dbaski")
    vr = S.RENK[KAT_RENK.get(kat, "turuncu")]
    k = spec["kapanis"]
    bas = E(BUY(k.get("satir1", "")))
    if k.get("satir2"):
        bas += "<br><em>%s</em>" % E(BUY(k["satir2"]))
    govde = ('<div class="ic kapanis" style="--vr:%s"><h1>%s</h1>'
             '<div class="kriter">%s</div>%s</div>%s'
             % (vr, bas,
                "".join('<div class="sr"><b>%s</b><span>%s</span></div>'
                        % (E(BUY(a)), E(b)) for a, b in k.get("kriterler", [])),
                ('<div class="kutu">%s</div>' % E(k["not"]))
                if k.get("not") else "", _kunye(spec)))
    S.bas(S.sayfa(govde, W, H, STIL, sinif="koyu"), cikti, W, H)


def hikaye(spec, cikti):
    kat = spec.get("kategori", "3dbaski")
    vr = S.RENK[KAT_RENK.get(kat, "turuncu")]
    k = spec.get("kapak") or {}
    govde = ('<div class="ic hik" style="--vr:%s;padding:70px 56px 0">%s'
             '<div class="govde">%s</div>'
             '<div class="cta"><b>kaydır, hepsi burada »</b>'
             '<span>@sermenkreatif</span></div></div>'
             % (vr, _basliklar(k, vr, KAT_ETIKET.get(kat, "")),
                _govde_kapak(k, vr)))
    S.bas(S.sayfa(govde, SW, SH, STIL), cikti, SW, SH, kalite=92)


def uret(spec, klasor):
    os.makedirs(klasor, exist_ok=True)
    n = 1
    kapak(spec, os.path.join(klasor, "1.jpg"))
    for s in spec.get("slaytlar", []):
        n += 1
        slayt(spec, s, os.path.join(klasor, "%d.jpg" % n))
    if spec.get("kapanis"):
        n += 1
        kapanis(spec, os.path.join(klasor, "%d.jpg" % n))
    hikaye(spec, os.path.join(klasor, "hikaye.jpg"))
    return n


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    print("%d kare + hikaye: %s" % (uret(spec, sys.argv[2]), sys.argv[2]))


if __name__ == "__main__":
    main()
