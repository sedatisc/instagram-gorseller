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
/* Künye satırı: iri sıra numarası, ince çizgi, sağda etiket. Sıra
   numarası fotoğrafın üstünde yüzen bir cipti, orada hem okunmuyor
   hem de ürünün önüne geçiyordu. Burada kareyi bölen tipografik
   öğeye dönüştü. */
.dizi{flex:0 0 auto;display:flex;align-items:center;gap:20px;
  padding:24px 0 0}
.dizi b{font-family:Anton;font-size:52px;line-height:.8;color:var(--vr)}
.dizi hr{flex:1;height:2px;border:0;background:#d6dde8}
.dizi i{font-style:normal;font-family:Mono;font-size:21px;color:#5a6678;
  letter-spacing:.14em;text-transform:uppercase}
.yazi{flex:0 0 auto;padding:16px 0 0}
.yazi h1{font-weight:700;font-size:62px;line-height:1.05;
  letter-spacing:-.022em}
.yazi p{font-size:30px;line-height:1.36;color:#5a6678;margin-top:14px;
  max-width:92%}
.ozellik{list-style:none;margin:18px 0 0}
.ozellik li{display:flex;justify-content:space-between;align-items:baseline;
  gap:20px;border-top:2px solid #d6dde8;padding:13px 0 0;margin-top:11px}
.ozellik b{font-family:Mono;font-weight:400;font-size:22px;color:#5a6678;
  letter-spacing:.05em;text-transform:uppercase;white-space:nowrap}
.ozellik span{font-size:28px;text-align:right}
.ayak{flex:0 0 auto;display:flex;align-items:center;
  justify-content:space-between;padding:24px 0 0}
.rozet{display:inline-flex;align-items:center;border-radius:999px;
  background:var(--vr);color:#fff;font-weight:600;font-size:30px;
  padding:15px 28px}
.ayak .not{font-size:26px;color:#5a6678}

/* ---- kapak ----
   Altı eşit küçük resimlik ızgara katalog sayfası gibi duruyordu ve
   akışta hiçbir ürün okunmuyordu. Düzen tersine çevrildi: iri başlık,
   bir ürün büyük, kalanlar altta küçük şeritte. */
.kasnak{flex:0 0 auto}
.kas{display:flex;align-items:center;gap:14px;font-family:Mono;
  font-size:21px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--vr)}
.kas s{flex:0 0 46px;height:3px;background:var(--vr);
  text-decoration:none}
.kasnak h1{font-family:Anton;text-transform:uppercase;line-height:.94;
  letter-spacing:.004em;font-size:96px;margin-top:18px}
.kasnak p{font-size:31px;color:#5a6678;margin-top:16px;line-height:1.33;
  max-width:88%}
/* Kahraman kutunun boyu ürünün en/boy oranından geliyor: sabit uzun
   kutuda yatık ürün (yazıcı, makara) tepesinde kocaman boşlukla
   kalıyordu. Artan yer alttaki şeride gidiyor, küçük resimler büyür. */
.kgov{flex:1 1 auto;min-height:0;margin-top:22px;display:flex;
  flex-direction:column;justify-content:center;gap:10px}
.sahne{flex:0 0 auto;display:flex}
.sahne .urun{flex:1}
.serit{flex:0 0 auto;height:186px;display:grid;gap:10px;
  grid-auto-flow:column;grid-auto-columns:1fr}
.serit .urun{border-radius:14px;align-items:center}
.serit .urun img{max-width:86%;max-height:82%;margin-bottom:0}
.serit .urun::after{display:none}
.spot{flex:0 0 auto;display:flex;align-items:center;
  justify-content:space-between;padding:22px 0 0}
.spot b{font-weight:600;font-size:31px}
.spot i{font-style:normal;font-family:Mono;font-size:26px;color:var(--vr)}

/* ---- kapanış ---- */
.kapanis h1{font-family:Anton;text-transform:uppercase;font-size:76px;
  line-height:1}
.kapanis .alt{font-size:28px;color:#96a4c0;margin-top:14px;line-height:1.34}
/* Satırlar kalan yeri paylaşıyor: sabit yükseklikte listenin altında
   ve üstünde kocaman boşluk kalıyordu. */
.liste{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;
  gap:12px;padding:26px 0}
.liste .sr{flex:1 1 0;min-height:84px;max-height:164px;
  display:flex;align-items:center;gap:22px;background:#1a2440;
  border-radius:14px;padding:10px 24px 10px 20px;position:relative;
  overflow:hidden}
.liste .sr::before{content:"";position:absolute;left:0;top:14px;bottom:14px;
  width:6px;border-radius:3px;background:var(--vr)}
.liste .sr figure{flex:0 0 auto;height:78%;aspect-ratio:1;border-radius:10px;
  background:#fff;display:flex;align-items:center;justify-content:center;
  padding:6px;margin-left:12px}
.liste .sr figure img{max-width:100%;max-height:100%;object-fit:contain}
.liste .sr b{font-weight:600;font-size:33px;color:#fff;flex:1;
  letter-spacing:-.01em}
.liste .sr i{font-style:normal;font-weight:600;font-size:26px;color:var(--vr)}
.kutu{flex:0 0 auto;background:#1a2440;border-radius:16px;padding:20px 26px}
.kutu b{display:block;font-family:Mono;font-size:23px;color:var(--vr);
  letter-spacing:.08em;text-transform:uppercase}
.kutu span{display:block;font-size:26px;color:#d6dde8;margin-top:10px}

/* ---- hikaye ---- */
/* Marka cipi fotoğrafın üstünde değil, kadrajın sol üstünde duruyor;
   ürünün üstüne binince okunmuyordu. */
.hik .urun{flex:0 0 1240px;border-radius:0;margin:-48px -48px 0;
  align-items:center}
/* Ürün dikeyde ortalandığı için tabana sabitlenen temas gölgesi
   ürünün epey altında ayrı bir leke olarak kalıyordu. */
.hik .urun::after{display:none}
.hik .etiketler{top:66px;left:66px;right:66px}
.hik .govde{flex:1 1 auto;display:flex;flex-direction:column;
  padding:52px 0 0;position:relative}
.hik .govde::before{content:"";position:absolute;left:0;top:56px;width:8px;
  height:64px;border-radius:4px;background:var(--vr)}
.hik h1{font-weight:700;font-size:64px;line-height:1.05;
  letter-spacing:-.02em;padding-left:30px}
.hik p{font-size:34px;line-height:1.33;color:#5a6678;padding-left:30px;
  margin-top:16px}
.hik .cta{margin-top:auto;text-align:center;padding-bottom:110px}
.hik .cta b{display:block;font-weight:700;font-size:42px}
.hik .cta span{display:block;font-family:Mono;font-size:28px;color:#5a6678;
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
    # Kategori cipi fotoğrafın üstünden kalktı; künye satırında duruyor.
    # Fotoğrafın üstü boş kalınca ürün tek başına kadrajı tutuyor.
    etiket = BUY(u.get("etiket") or spec.get("baslik", ""))[:26]
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
        % (vr, E(BUY(spec.get("etiket", "baskı ürünleri"))),
           E(BUY(spec["baslik"])),
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
