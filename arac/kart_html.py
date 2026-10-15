#!/usr/bin/env python3
"""Ürün kartı şablonu — HTML/CSS sürümü.

`arac/urun_karti.py` ile aynı spec dosyasını okuyor, aynı kareleri
üretiyor; fark düzenin Pillow'da piksel sayarak değil, tarayıcının
yerleşim motoruyla kurulması. Yazı bloğu kendi yerini ölçüyor, kutular
kalan yeri paylaşıyor, altta boşluk kalmıyor.

    python3 arac/kart_html.py <spec.json> <cikti-klasoru>

spec.json'da ürünün yalnız "slug"ı yazılıyorsa ad, fiyat, fotoğraf ve
özellikler otomasyon/urun-bilgi.json'dan geliyor.
"""
import html as _h
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "arac"))
sys.path.insert(0, os.path.join(KOK, "arac", "html"))

import sistem as S                                          # noqa: E402
from urun_karti import BUY, _bilgi, _fiyat, _tam_yol, coz    # noqa: E402

W, H = 1080, 1350
SW, SH = 1080, 1920


def E(s):
    return _h.escape(str(s or ""))


def _renk(u, spec, vars_="turuncu"):
    return S.RENK.get(u.get("renk", spec.get("renk", vars_)),
                      S.RENK[vars_])


def _gorsel(u, spec):
    """Ürün görselini data URI olarak veriyor; kesim açıksa kesilmişini."""
    yol = _tam_yol(u.get("gorsel"))
    if not yol:
        return None, False
    if u.get("kesim", spec.get("kesim", True)):
        uri = S.kesik_uri(yol)
        if uri:
            return uri, True
    return S.foto_uri(yol), False


def _oran(u, spec):
    """Ürünün en/boy oranı. Kapak ızgarası buna göre seçiliyor."""
    yol = _tam_yol(u.get("gorsel"))
    if not yol:
        return 1.0
    try:
        from PIL import Image
        if u.get("kesim", spec.get("kesim", True)):
            from urun_karti import kesik_ac
            k = kesik_ac(yol)
            if k is not None:
                return k.width / float(k.height)
        with Image.open(yol) as im:
            return im.width / float(im.height)
    except Exception:
        return 1.0


def _kunye(spec):
    orta = spec.get("kunye", "")
    return ('<div class="kunye"><span>@sermenkreatif</span>'
            '<span class="orta">%s</span>'
            '<span class="sag">sermenkreatif.com</span></div>'
            % E(orta))


# --------------------------------------------------------------- stil
STIL = """
.ic{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  padding:36px 36px 0}

/* ---- tek ürün karesi ---- */
.kare .urun{flex:1 1 auto;min-height:0}
.etiketler{position:absolute;top:22px;left:22px;right:22px;
  display:flex;justify-content:space-between;pointer-events:none}
.yazi{flex:0 0 auto;padding:26px 0 0;position:relative}
.yazi::before{content:"";position:absolute;left:0;top:4px;width:7px;
  height:60px;border-radius:4px;background:var(--vr)}
.yazi h1{font-weight:700;font-size:50px;line-height:1.08;
  letter-spacing:-.018em;padding-left:26px}
.yazi p{font-size:26px;line-height:1.38;color:#68748b;padding-left:26px;
  margin-top:12px}
.ozellik{list-style:none;margin:18px 0 0;padding-left:26px}
.ozellik li{display:flex;justify-content:space-between;align-items:baseline;
  gap:20px;border-top:2px solid #d6dde8;padding:13px 0 0;margin-top:11px}
.ozellik b{font-family:Mono;font-weight:400;font-size:20px;color:#68748b;
  letter-spacing:.05em;text-transform:uppercase;white-space:nowrap}
.ozellik span{font-size:24px;text-align:right}
.ayak{flex:0 0 auto;display:flex;align-items:center;
  justify-content:space-between;padding:26px 0 0}
.rozet{display:inline-flex;align-items:center;border-radius:999px;
  background:var(--vr);color:#fff;font-weight:600;font-size:26px;
  padding:15px 28px}
.ayak .not{font-size:23px;color:#68748b}

/* ---- kapak ---- */
.bant{flex:0 0 auto;background:#121a30;color:#fff;border-radius:20px;
  padding:26px 30px}
.bant h1{font-family:Anton;text-transform:uppercase;line-height:1;
  letter-spacing:.005em;font-size:68px}
.bant p{font-size:25px;color:#a8b6d0;margin-top:14px;line-height:1.3}
.izgara{flex:1 1 auto;min-height:0;display:grid;gap:12px;margin-top:20px}
/* Izgarada ürün dikeyde ortalanıyor: tabana yaslayınca en/boy oranı
   farklı ürünlerde bütün boşluk üstte toplanıyordu. */
.izgara .urun{border-radius:18px;align-items:center}
.izgara .urun img{max-width:94%;max-height:88%;margin-bottom:0}
.spot{flex:0 0 auto;display:flex;align-items:center;
  justify-content:space-between;padding:22px 0 0}
.spot b{font-weight:600;font-size:27px}
.spot i{font-style:normal;font-family:Mono;font-size:24px;color:var(--vr)}

/* ---- kapanış ---- */
.kapanis h1{font-family:Anton;text-transform:uppercase;font-size:64px;
  line-height:1}
.kapanis .alt{font-size:24px;color:#96a4c0;margin-top:12px;line-height:1.35}
/* Satırlar kalan yeri paylaşıyor: sabit yükseklikte listenin altında
   ve üstünde kocaman boşluk kalıyordu. */
.liste{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  gap:12px;padding:26px 0}
.liste .sr{flex:1 1 0;min-height:84px;max-height:132px;
  display:flex;align-items:center;gap:22px;background:#1a2440;
  border-radius:14px;padding:10px 24px 10px 20px;position:relative;
  overflow:hidden}
.liste .sr::before{content:"";position:absolute;left:0;top:14px;bottom:14px;
  width:6px;border-radius:3px;background:var(--vr)}
.liste .sr figure{flex:0 0 auto;height:78%;aspect-ratio:1;border-radius:10px;
  background:#fff;display:flex;align-items:center;justify-content:center;
  padding:6px;margin-left:12px}
.liste .sr figure img{max-width:100%;max-height:100%;object-fit:contain}
.liste .sr b{font-weight:600;font-size:29px;color:#fff;flex:1;
  letter-spacing:-.01em}
.liste .sr i{font-style:normal;font-weight:600;font-size:23px;color:var(--vr)}
.kutu{flex:0 0 auto;background:#1a2440;border-radius:16px;padding:20px 26px}
.kutu b{display:block;font-family:Mono;font-size:21px;color:var(--vr);
  letter-spacing:.08em;text-transform:uppercase}
.kutu span{display:block;font-size:23px;color:#d6dde8;margin-top:9px}

/* ---- hikaye ---- */
/* Marka cipi fotoğrafın üstünde değil, kadrajın sol üstünde duruyor;
   ürünün üstüne binince okunmuyordu. */
.hik .urun{flex:0 0 1240px;border-radius:0;margin:-48px -48px 0;
  align-items:center}
.hik .etiketler{top:66px;left:66px;right:66px}
.hik .govde{flex:1 1 auto;display:flex;flex-direction:column;
  padding:52px 0 0;position:relative}
.hik .govde::before{content:"";position:absolute;left:0;top:56px;width:8px;
  height:64px;border-radius:4px;background:var(--vr)}
.hik h1{font-weight:700;font-size:56px;line-height:1.06;
  letter-spacing:-.02em;padding-left:30px}
.hik p{font-size:30px;line-height:1.34;color:#68748b;padding-left:30px;
  margin-top:16px}
.hik .cta{margin-top:auto;text-align:center;padding-bottom:110px}
.hik .cta b{display:block;font-weight:700;font-size:36px}
.hik .cta span{display:block;font-family:Mono;font-size:28px;color:#68748b;
  margin-top:14px}
"""


# ----------------------------------------------------------- tek ürün
def _urun_kutusu(u, spec, ust="", stil=""):
    """Ürün çerçevesi. `ust` kutunun üstüne binen parçalar (cip, fiyat)."""
    uri, kesik = _gorsel(u, spec)
    ic = ('<img src="%s" alt="">' % uri) if uri else ""
    return ('<div class="urun%s"%s>%s%s</div>'
            % ("" if kesik else " sik",
               (' style="%s"' % stil) if stil else "", ic, ust))


def urun_karesi(u, spec, sira, toplam, cikti):
    vr = _renk(u, spec)
    etiket = u.get("etiket") or spec.get("baslik", "")
    cipler = []
    if etiket:
        cipler.append('<span class="cip">%s</span>' % E(BUY(etiket)[:28]))
    else:
        cipler.append("<span></span>")
    if sira and toplam:
        cipler.append('<span class="cip">%d/%d</span>' % (sira, toplam))
    else:
        cipler.append("<span></span>")
    ust = '<div class="etiketler">%s</div>' % "".join(cipler)

    ozl = [o for o in (u.get("ozellik") or []) if len(o) == 2][:4]
    ozl_html = ""
    if ozl:
        ozl_html = ('<ul class="ozellik">%s</ul>' % "".join(
            "<li><b>%s</b><span>%s</span></li>" % (E(BUY(a)[:22]), E(d))
            for a, d in ozl))

    fiyat = _fiyat(u, spec)
    if fiyat:
        ayak = ('<span class="rozet">%s</span>'
                '<span class="not">sermenkreatif.com\'da</span>' % E(fiyat))
    else:
        ayak = '<span class="rozet">sermenkreatif.com\'da</span><span></span>'

    govde = (
        '<div class="ic kare" style="--vr:%s">%s'
        '<div class="yazi"><h1>%s</h1>%s%s</div>'
        '<div class="ayak">%s</div></div>%s'
        % (vr, _urun_kutusu(u, spec, ust=ust),
           E(u.get("ad", "")),
           ('<p>%s</p>' % E(u["satir"])) if u.get("satir") else "",
           ozl_html, ayak, _kunye(spec)))
    S.bas(S.sayfa(govde, W, H, STIL), cikti, W, H)


# -------------------------------------------------------------- kapak
# Ürünler yatıksa (yazıcı, makara, kutu) dar dikey hücrede küçücük
# kalıyor. Bu yüzden ızgara, ürünlerin ortanca en/boy oranına göre
# seçiliyor: yatık ürünlere az sütunlu geniş hücre.
_DAR = {
    1: ("1fr", "1fr", []),
    2: ("1fr 1fr", "1fr", []),
    3: ("1fr 1fr", "1.05fr 1fr", ["grid-column:1/3"]),
    4: ("1fr 1fr", "1fr 1fr", []),
    5: ("1fr 1fr 1fr", "1fr 1fr", [None, None, None,
                                   "grid-column:1/3", "grid-column:3/4"]),
    6: ("1fr 1fr 1fr", "1fr 1fr", []),
}
_GENIS = {
    1: ("1fr", "1fr", []),
    2: ("1fr", "1fr 1fr", []),
    3: ("1fr", "1fr 1fr 1fr", []),
    4: ("1fr 1fr", "1fr 1fr", []),
    5: ("1fr 1fr", "1fr 1fr 1fr", [None, None, None, None,
                                   "grid-column:1/3"]),
    6: ("1fr 1fr", "1fr 1fr 1fr", []),
}


def _izgara(urunler, spec):
    oranlar = sorted(_oran(u, spec) for u in urunler)
    orta = oranlar[len(oranlar) // 2]
    n = min(len(urunler), 6)
    return (_GENIS if orta >= 1.15 else _DAR)[n]


def kapak(spec, urunler, cikti):
    vr = S.RENK.get(spec.get("renk", "turuncu"), S.RENK["turuncu"])
    n = min(len(urunler), 6)
    sut, sat, yer = _izgara(urunler[:n], spec)
    kutular = []
    for i, u in enumerate(urunler[:n]):
        st = yer[i] if i < len(yer) and yer[i] else ""
        f = _fiyat(u, spec)
        rz = ('<span class="cip" style="position:absolute;right:12px;'
              'bottom:12px">%s</span>' % E(f)) if f else ""
        kutular.append(_urun_kutusu(u, spec, ust=rz, stil=st))

    spot = spec.get("spot") or ("%d ürün · hepsi kendi atölyemizde basıldı"
                               % len(urunler))
    govde = (
        '<div class="ic" style="--vr:%s">'
        '<div class="bant"><h1>%s</h1>%s</div>'
        '<div class="izgara" style="grid-template-columns:%s;'
        'grid-template-rows:%s">%s</div>'
        '<div class="spot"><b>%s</b><i>kaydır »</i></div></div>%s'
        % (vr, E(BUY(spec["baslik"])),
           ('<p>%s</p>' % E(spec["alt"])) if spec.get("alt") else "",
           sut, sat, "".join(kutular), E(spot), _kunye(spec)))
    S.bas(S.sayfa(govde, W, H, STIL), cikti, W, H)


# ------------------------------------------------------------ kapanış
def kapanis(spec, urunler, cikti):
    vr = S.RENK.get(spec.get("renk", "turuncu"), S.RENK["turuncu"])
    satirlar = []
    for u in urunler:
        f = _fiyat(u, spec)
        uri, _ = _gorsel(u, spec)
        kck = ('<figure><img src="%s" alt=""></figure>' % uri) if uri else ""
        satirlar.append('<div class="sr">%s<b>%s</b>%s</div>'
                        % (kck, E(u.get("kisa") or u.get("ad", "")),
                           ("<i>%s</i>" % E(f)) if f else ""))
    kutu = spec.get("kapanis_kutu",
                    ["3D BASKI HİZMETİ",
                     "Kendi dosyanı yükle, fiyatını anında gör."])
    kutu_html = ('<div class="kutu"><b>%s</b><span>%s</span></div>'
                 % (E(BUY(kutu[0])), E(kutu[1]))) if kutu else ""
    govde = (
        '<div class="ic kapanis" style="--vr:%s">'
        '<h1>%s</h1><div class="alt">%s</div>'
        '<div class="liste">%s</div>%s</div>%s'
        % (vr, E(BUY(spec.get("kapanis_ust", "hepsi burada"))),
           E(spec.get("kapanis_alt",
                      "Hepsi kendi atölyemizde basıldı. Ölçü, renk ve adet "
                      "isteğe göre değişir.")),
           "".join(satirlar), kutu_html, _kunye(spec)))
    S.bas(S.sayfa(govde, W, H, STIL, sinif="koyu"), cikti, W, H)


# ------------------------------------------------------------- hikaye
def hikaye(spec, urunler, cikti):
    u = urunler[0]
    vr = _renk(u, spec)
    etiket = u.get("etiket") or spec.get("baslik", "")
    et = ('<div class="etiketler"><span class="cip">%s</span></div>'
          % E(BUY(etiket)[:26])) if etiket else ""
    fiyat = _fiyat(u, spec)
    govde = (
        '<div class="ic hik" style="--vr:%s;padding:48px 48px 0">%s'
        '<div class="govde"><h1>%s</h1>%s%s'
        '<div class="cta"><b>linke dokun »</b>'
        '<span>sermenkreatif.com</span></div></div></div>'
        % (vr, _urun_kutusu(u, spec, ust=et),
           E(u.get("kisa") or u.get("ad", "")),
           ('<p>%s</p>' % E(u["satir"])) if u.get("satir") else "",
           ('<p style="padding-left:30px;margin-top:22px">'
            '<span class="rozet">%s</span></p>' % E(fiyat)) if fiyat else ""))
    S.bas(S.sayfa(govde, SW, SH, STIL), cikti, SW, SH, kalite=92)


# ---------------------------------------------------------------- ana
def uret(spec, klasor):
    kat = _bilgi()
    urunler = [coz(u, kat) for u in spec["urunler"]]
    eksik = [u for u in urunler if not u.get("gorsel")]
    if eksik:
        raise SystemExit("fotoğraf yok: " + ", ".join(
            u.get("slug", u.get("ad", "?")) for u in eksik))
    os.makedirs(klasor, exist_ok=True)

    tek = len(urunler) == 1 or spec.get("tip") == "tek"
    n = 0
    if not tek:
        n += 1
        kapak(spec, urunler, os.path.join(klasor, "1.jpg"))
    for i, u in enumerate(urunler, 1):
        n += 1
        urun_karesi(u, spec, None if tek else i,
                    None if tek else len(urunler),
                    os.path.join(klasor, "%d.jpg" % n))
    if not tek and spec.get("kapanis", True):
        n += 1
        kapanis(spec, urunler, os.path.join(klasor, "%d.jpg" % n))
    hikaye(spec, urunler, os.path.join(klasor, "hikaye.jpg"))
    return n


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    uret(spec, sys.argv[2])


if __name__ == "__main__":
    main()
