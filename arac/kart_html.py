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
/* FÖY — koleksiyon kartları. Yuvarlak kart, hap rozet ve gölge
   kalktı; ürünler kenarı çizili pencerelerde, etiketler ince
   kurallarla ayrılıyor. */
.ic{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  padding:52px 56px 0}

/* ---- tek ürün karesi ---- */
.kare .urun{flex:1 1 auto;min-height:0}
.etiketler{position:absolute;top:18px;left:18px;right:18px;
  display:flex;justify-content:space-between;pointer-events:none}
.dizi{flex:0 0 auto;display:flex;align-items:baseline;gap:18px;
  padding:22px 0 0}
.dizi b{font-size:34px;font-weight:650;line-height:1;color:var(--mur);
  font-variation-settings:"wdth" 112;letter-spacing:-.02em}
.dizi hr{flex:1;height:1px;border:0;background:var(--cizgi)}
.dizi i{font-style:normal;font-family:Mono;font-size:19px;
  color:var(--soluk);letter-spacing:.01em}
.yazi{flex:0 0 auto;padding:16px 0 0}
.yazi h1{font-weight:650;font-size:56px;line-height:1.04;
  letter-spacing:-.025em;font-variation-settings:"wdth" 112}
.yazi p{font-size:28px;line-height:1.4;color:var(--soluk);margin-top:14px;
  max-width:94%}
.ozellik{list-style:none;margin:18px 0 0}
.ozellik li{display:flex;justify-content:space-between;align-items:baseline;
  gap:20px;border-top:1px solid var(--cizgi);padding:13px 0 0;margin-top:11px}
.ozellik b{font-family:Mono;font-weight:400;font-size:19px;
  color:var(--soluk);letter-spacing:.01em;white-space:nowrap}
.ozellik span{font-size:26px;text-align:right;font-weight:500}
.ayak{flex:0 0 auto;display:flex;align-items:center;
  justify-content:space-between;padding:22px 0 0}
.rozet{display:inline-flex;align-items:center;gap:10px;font-family:Mono;
  font-size:21px;color:var(--mur)}
.rozet::before{content:"";width:11px;height:11px;border-radius:50%;
  border:2px solid var(--marka)}
.ayak .not{font-family:Mono;font-size:20px;color:var(--soluk)}

/* ---- kapak ---- */
.kasnak{flex:0 0 auto}
.kas{display:flex;align-items:center;gap:14px;font-family:Mono;
  font-size:19px;color:var(--soluk)}
.kas s{flex:0 0 34px;height:1px;background:var(--cizgi);
  text-decoration:none}
.kasnak h1{font-size:84px;line-height:1;letter-spacing:-.028em;
  font-weight:650;font-variation-settings:"wdth" 112;margin-top:16px}
.kasnak p{font-size:28px;color:var(--soluk);margin-top:14px;line-height:1.4;
  max-width:92%}
.kgov{flex:1 1 auto;min-height:0;margin-top:22px;display:flex;
  flex-direction:column;justify-content:center;gap:12px}
.sahne{flex:0 0 auto;display:flex}
.sahne .urun{flex:1}
.serit{flex:0 0 auto;height:176px;display:grid;gap:12px;
  grid-auto-flow:column;grid-auto-columns:1fr}
.serit .urun img{max-width:88%;max-height:84%}
.spot{flex:0 0 auto;display:flex;align-items:baseline;
  justify-content:space-between;padding:20px 0 0;
  border-top:1px solid var(--cizgi);margin-top:18px}
.spot b{font-weight:600;font-size:27px;letter-spacing:-.012em}
.spot i{font-style:normal;font-family:Mono;font-size:20px;color:var(--marka)}

/* ---- kapanış ---- */
.kapanis h1{font-size:68px;line-height:1.03;font-weight:650;
  letter-spacing:-.025em;font-variation-settings:"wdth" 112}
.kapanis .alt{font-size:26px;color:#8C9099;margin-top:12px;line-height:1.4}
.liste{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  padding:22px 0}
.liste .sr{flex:1 1 0;min-height:84px;max-height:160px;
  display:flex;align-items:center;gap:22px;padding:12px 0;
  border-bottom:1px solid #2E3238;position:relative}
.liste .sr:first-child{border-top:1px solid #2E3238}
.liste .sr figure{flex:0 0 auto;height:76%;aspect-ratio:1;background:#fff;
  border:1px solid #2E3238;display:flex;align-items:center;
  justify-content:center;padding:6px}
.liste .sr figure img{max-width:100%;max-height:100%;object-fit:contain}
.liste .sr b{font-weight:600;font-size:31px;color:#F3F2EE;flex:1;
  letter-spacing:-.014em}
.liste .sr i{font-style:normal;font-family:Mono;font-size:20px;
  color:#E8A0A1}
.kutu{flex:0 0 auto;border-top:1px solid #2E3238;padding:18px 0 0}
.kutu b{display:block;font-family:Mono;font-size:19px;color:#8C9099}
.kutu span{display:block;font-size:25px;color:#F3F2EE;margin-top:8px}

/* ---- hikaye ---- */
.hik .urun{flex:0 0 1180px;margin:0;align-items:center}
.hik .etiketler{top:24px;left:24px;right:24px}
.hik .govde{flex:1 1 auto;display:flex;flex-direction:column;
  padding:44px 0 0}
.hik h1{font-weight:650;font-size:62px;line-height:1.04;
  letter-spacing:-.025em;font-variation-settings:"wdth" 112}
.hik p{font-size:30px;line-height:1.4;color:var(--soluk);margin-top:16px}
.hik .cta{margin-top:auto;padding-bottom:150px;
  border-top:1px solid var(--cizgi);padding-top:22px;
  display:flex;align-items:baseline;justify-content:space-between}
.hik .cta b{font-weight:600;font-size:30px}
.hik .cta span{font-family:Mono;font-size:21px;color:var(--marka)}
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
    # Kategori cipi fotoğrafın üstünden kalktı; künye satırında duruyor.
    # Fotoğrafın üstü boş kalınca ürün tek başına kadrajı tutuyor.
    etiket = (u.get("etiket") or spec.get("baslik", ""))[:26]
    if sira and toplam:
        sag = ("%s · %d/%d" % (etiket, sira, toplam)) if etiket \
            else "%d/%d" % (sira, toplam)
        dizi = ('<div class="dizi"><b>%02d</b><hr><i>%s</i></div>'
                % (sira, E(sag)))
    else:
        dizi = ('<div class="dizi"><b>&bull;</b><hr><i>%s</i></div>'
                % E(etiket or "ÜRÜN"))

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
        '<div class="ic kare" style="--vr:%s">%s%s'
        '<div class="yazi"><h1>%s</h1>%s%s</div>'
        '<div class="ayak">%s</div></div>%s'
        % (vr, _urun_kutusu(u, spec), dizi,
           E(u.get("ad", "")),
           ('<p>%s</p>' % E(u["satir"])) if u.get("satir") else "",
           ozl_html, ayak, _kunye(spec)))
    S.bas(S.sayfa(govde, W, H, STIL), cikti, W, H)


# -------------------------------------------------------------- kapak
def _hero(urunler, spec):
    """Kapakta büyük duracak ürünün sırası.

    Varsayılan ilk ürün: spec'teki sıra zaten yazarın seçimi. Oranına
    bakıp seçtirmeyi denedim, fotoğrafında büyüteç baloncuğu olan ürünü
    kapağa çıkardı. Başkası isteniyorsa spec'e "kapak": <sıra no>."""
    n = spec.get("kapak")
    if isinstance(n, int) and 1 <= n <= len(urunler):
        return n - 1
    return 0


def kapak(spec, urunler, cikti):
    vr = S.RENK.get(spec.get("renk", "turuncu"), S.RENK["turuncu"])
    i = _hero(urunler, spec)
    kalan = [u for j, u in enumerate(urunler) if j != i][:5]

    def _f(u):
        f = _fiyat(u, spec)
        return ('<span class="cip" style="position:absolute;right:14px;'
                'bottom:14px">%s</span>' % E(f)) if f else ""

    # Kutu yüksekliği: ürün kutu içinde en çok %92 en, %90 boy kaplıyor.
    oran = max(_oran(urunler[i], spec), .25)
    boy = int(min(660, max(400, (1008 * .92 / oran) / .90)))

    spot = spec.get("spot") or ("%d ürün · hepsi kendi atölyemizde basıldı"
                                % len(urunler))
    govde = (
        '<div class="ic" style="--vr:%s">'
        '<div class="kasnak"><div class="kas"><s></s>%s</div>'
        '<h1>%s</h1>%s</div>'
        '<div class="kgov"><div class="sahne" style="height:%dpx">%s</div>'
        '<div class="serit">%s</div></div>'
        '<div class="spot"><b>%s</b><i>kaydır »</i></div></div>%s'
        % (vr, E(spec.get("etiket", "baskı ürünleri")),
           E(spec["baslik"]),
           ('<p>%s</p>' % E(spec["alt"])) if spec.get("alt") else "",
           boy, _urun_kutusu(urunler[i], spec, ust=_f(urunler[i])),
           "".join(_urun_kutusu(u, spec) for u in kalan),
           E(spot), _kunye(spec)))
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
        % (vr, E(spec.get("kapanis_ust", "hepsi burada")),
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
          % E(etiket[:26])) if etiket else ""
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
