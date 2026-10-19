#!/usr/bin/env python3
"""Baskı ürünü kartı — fotoğrafın başrolde olduğu şablon.

Dekoratif baskı ürünü teknik tabloyla satılmıyor; fotoğrafıyla
satılıyor. Bu yüzden kare, rehber gönderisinin açık zeminini koruyor
ama ortasında tablo değil ürünün kendi stüdyo fotoğrafı duruyor.

Ürün sayfalarının çoğu sıfır özellik satırı döndürüyor; şablon ad,
fiyat ve fotoğrafla çalışıyor, özellik varsa altına ekliyor.

    python3 arac/urun_karti.py <spec.json> <cikti-klasoru>

spec.json içinde ürünün yalnız "slug"ı yazılıyorsa ad, fiyat, fotoğraf
ve özellikler otomasyon/urun-bilgi.json'dan okunuyor. Yani yeni gönderi
için yazılacak tek şey slug ve bir cümle.
"""
import glob
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
import uret as U                                         # noqa: E402

W, H = 1080, 1350
SW, SH = 1080, 1920
KEN = 36

KAGIT = (243, 246, 250)
MUREKKEP = (16, 22, 38)
SOLUK = (104, 116, 139)
CIZGI = (214, 221, 232)
KART = (255, 255, 255)
LACI = (18, 26, 48)

RENK = {
    "kirmizi": (228, 62, 62), "turuncu": (236, 132, 42),
    "sari": (233, 184, 32), "yesil": (36, 162, 86),
    "mavi": (36, 118, 220), "mor": (134, 80, 226),
    "turkuaz": (22, 162, 173), "pembe": (222, 76, 140),
    "gri": (108, 118, 138),
}

BILGI = os.path.join(KOK, "otomasyon", "urun-bilgi.json")
HAM = os.path.join(KOK, "gorsel", "urun", "ham")


# ------------------------------------------------------------------ yazı
def f_bold(s):
    return U.pop(s, "SemiBold")


def f_reg(s):
    return U.pop(s, "Regular")


def f_mono(s, b=True):
    return U.mono(s, b)


def BUY(s):
    """Türkçe büyük harf: i » İ, ı » I. Python'un upper'ı 'çizgisel'i
    'ÇIZGISEL' yapıyor."""
    cik = []
    for i, c in enumerate(s):
        if c == "i" and i + 1 < len(s) and s[i + 1].isdigit():
            cik.append("I")
        elif c == "i":
            cik.append("İ")
        elif c == "ı":
            cik.append("I")
        else:
            cik.append(c.upper())
    return "".join(cik)


def yuvarlak(d, kutu, r, dolgu=None, kenar=None, kalin=2):
    d.rounded_rectangle(kutu, radius=r, fill=dolgu, outline=kenar,
                        width=kalin)


def sigdir(d, metin, font_fn, en, bas, taban=11):
    s = bas
    while s > taban and d.textlength(metin, font=font_fn(s)) > en:
        s -= 1
    return font_fn(s)


def sar(d, metin, font, en):
    kel, sat, su = metin.split(), [], ""
    for k in kel:
        dene = (su + " " + k).strip()
        if d.textlength(dene, font=font) <= en or not su:
            su = dene
        else:
            sat.append(su)
            su = k
    if su:
        sat.append(su)
    return sat


def blok(d, metin, font_fn, en, bas, taban, satir_sayisi):
    """Punto, metin verilen satır sayısına sığana kadar küçülüyor.
    Sabit puntoda uzun ürün adlarının sonu düşüyordu."""
    s = bas
    while s > taban:
        sat = sar(d, metin, font_fn(s), en)
        if len(sat) <= satir_sayisi:
            return font_fn(s), sat
        s -= 1
    return font_fn(taban), sar(d, metin, font_fn(taban), en)[:satir_sayisi]


# ------------------------------------------------------------------ veri
def _bilgi():
    try:
        with open(BILGI, encoding="utf-8") as f:
            ham = json.load(f)
    except Exception:
        return {}
    return {v.get("slug", ""): v for v in ham.values() if v.get("slug")}


def _foto(slug):
    for p in sorted(glob.glob(os.path.join(HAM, slug + ".*"))):
        return p
    return None


def coz(u, kat):
    """Üründe eksik olan alanları ürün-bilgi.json'dan tamamlıyor."""
    k = kat.get(u.get("slug", ""), {})
    cik = dict(u)
    if not cik.get("ad"):
        ad = k.get("baslik", "")
        for kes in (" – ", " - ", " — "):
            if kes in ad:
                ad = ad.split(kes)[0]
                break
        cik["ad"] = ad.strip().strip("“”\"")
    if not cik.get("fiyat"):
        cik["fiyat"] = k.get("fiyat", "")
    if not cik.get("gorsel"):
        p = _foto(u.get("slug", ""))
        if p:
            cik["gorsel"] = os.path.relpath(p, os.path.join(KOK, "gorsel"))
    if cik.get("ozellik") is None:
        cik["ozellik"] = k.get("ozellik", [])
    return cik


def _tam_yol(yol):
    if not yol:
        return None
    tam = yol if os.path.isabs(yol) else os.path.join(KOK, "gorsel", yol)
    if not os.path.exists(tam):
        tam = os.path.join(KOK, yol)
    return tam if os.path.exists(tam) else None


def _ac(yol):
    tam = _tam_yol(yol)
    return Image.open(tam).convert("RGB") if tam else None


# ------------------------------------------------------------------ foto
def _zemin_rengi(im):
    """Fotoğrafın kenar rengini örnekliyoruz: panelin zemini aynı renk
    olunca stüdyo fotoğrafı taşmış gibi duruyor, çerçeve görünmüyor."""
    k = im.resize((16, 16), Image.LANCZOS)
    px = [k.getpixel((x, y))
          for x in range(16) for y in range(16)
          if x in (0, 1, 14, 15) or y in (0, 1, 14, 15)]
    n = len(px)
    return tuple(sum(c[i] for c in px) // n for i in range(3))


def foto_panel(img, kutu, im, r=24, dolu=False, pay=1.0):
    """Fotoğrafı kutuya yerleştiriyor.

    dolu=False fotoğrafın tamamını koruyup boşluğu kendi kenar rengiyle
    dolduruyor — ürünün yarısını kesmemek için.
    dolu=True kutuyu dolduruyor ama `pay` kırpmaya tavan koyuyor: 1.25,
    "tam sığdırmanın en çok 1,25 katına kadar büyüt" demek. Tavansız
    kırpmada yatay fotoğrafın iki yanı gidiyordu."""
    x0, y0, x1, y1 = [int(v) for v in kutu]
    kw, kh = x1 - x0, y1 - y0
    zem = _zemin_rengi(im)
    kat = Image.new("RGB", (kw, kh), zem)
    sig = min(kw / float(im.width), kh / float(im.height))
    if dolu:
        o = min(max(kw / float(im.width), kh / float(im.height)), sig * pay)
    else:
        o = min((kw - 24) / im.width, (kh - 24) / im.height)
    yeni = im.resize((max(1, int(im.width * o)), max(1, int(im.height * o))),
                     Image.LANCZOS)
    kat.paste(yeni, ((kw - yeni.width) // 2, (kh - yeni.height) // 2))

    mask = Image.new("L", (kw, kh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, kw - 1, kh - 1], radius=r,
                                           fill=255)
    img.paste(kat, (x0, y0), mask)
    return zem


def _koyu(renk):
    return (renk[0] * 299 + renk[1] * 587 + renk[2] * 114) / 1000 < 140


# ------------------------------------------------------- tek zemin
KESIK = os.path.join(KOK, "gorsel", "urun", "kesik")

# u2net ürünün bir parçasını arka plan sanıp kesiyordu: kepçeliğin sol
# duvarı, üstünü örten maydanozla birlikte gitmişti. isnet-general-use
# aynı fotoğrafta ürünü bütün çıkarıyor; varsayılan model o oldu.
KESIM_MODELI = "isnet-general-use"
_OTURUM = {}
ZEMIN = (248, 249, 251)          # bütün ürünlerin ortak zemini


def kesik_ac(yol):
    """Arka planı kesilmiş sürüm; bir kere kesilip saklanıyor.

    Ürün fotoğrafları birbirini tutmuyor: biri beyaz stüdyo, biri koyu
    oda, biri ahşap masa. Yan yana gelince gönderi dağınık duruyor.
    Ürünü kesip hepsini aynı zemine oturtuyoruz."""
    ad = os.path.splitext(os.path.basename(yol))[0]
    hedef = os.path.join(KESIK, ad + ".png")
    if os.path.exists(hedef):
        return Image.open(hedef).convert("RGBA")
    try:
        from rembg import remove, new_session
    except ImportError:
        return None
    if "s" not in _OTURUM:
        _OTURUM["s"] = new_session(KESIM_MODELI)
    k = remove(Image.open(yol).convert("RGBA"), session=_OTURUM["s"])
    bb = k.split()[-1].point(lambda v: 255 if v > 8 else 0).getbbox()
    if bb:
        k = k.crop(bb)
    if k.width < 40 or k.height < 40:        # kesim boşa çıktı
        return None
    import kesim_temiz
    if kesim_temiz.yer_tutucu_mu(k):         # sitede fotoğraf yok
        return None
    os.makedirs(KESIK, exist_ok=True)
    k.save(hedef)
    kesim_temiz.temizle(hedef)               # soluk arka plan artıkları
    return Image.open(hedef).convert("RGBA")


def kesik_panel(img, kutu, kes, r=24, pay=0.84, taban=0.90):
    """Kesilmiş ürünü ortak zemine, temas gölgesiyle oturtuyor."""
    x0, y0, x1, y1 = [int(v) for v in kutu]
    kw, kh = x1 - x0, y1 - y0
    kat = Image.new("RGBA", (kw, kh), ZEMIN + (255,))

    o = min(kw * pay / kes.width, kh * pay / kes.height)
    u = kes.resize((max(1, int(kes.width * o)), max(1, int(kes.height * o))),
                   Image.LANCZOS)
    ux = (kw - u.width) // 2
    uy = max(int(kh * 0.05), int(kh * taban) - u.height)

    golge = Image.new("RGBA", (kw, kh), (0, 0, 0, 0))
    gw = u.width * 0.66
    gy = uy + u.height
    ImageDraw.Draw(golge).ellipse(
        [kw / 2 - gw / 2, gy - u.height * 0.045,
         kw / 2 + gw / 2, gy + u.height * 0.045],
        fill=(18, 24, 40, 58))
    kat.alpha_composite(golge.filter(ImageFilter.GaussianBlur(
        max(6, int(u.height * 0.035)))))
    kat.alpha_composite(u, (ux, uy))

    mask = Image.new("L", (kw, kh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, kw - 1, kh - 1], radius=r,
                                           fill=255)
    img.paste(kat.convert("RGB"), (x0, y0), mask)
    return ZEMIN


def yerlestir(img, kutu, u, spec, r=24, dolu=False, pay=1.0, taban=0.90):
    """Ürün görselini kutuya koyuyor: kesim açıksa ortak zemine,
    kapalıysa fotoğrafın kendi zeminiyle."""
    yol = _tam_yol(u.get("gorsel"))
    kesim = u.get("kesim", spec.get("kesim", True))
    if kesim and yol:
        kes = kesik_ac(yol)
        if kes is not None:
            return kesik_panel(img, kutu, kes, r=r, taban=taban,
                               pay=0.90 if dolu else 0.84)
    im = _ac(u.get("gorsel"))
    if im is None:
        ImageDraw.Draw(img).rounded_rectangle(kutu, radius=r, fill=ZEMIN)
        return ZEMIN
    return foto_panel(img, kutu, im, r=r, dolu=dolu, pay=pay)


# ------------------------------------------------------------------ parça
def cip(d, x, y, metin, renk=LACI, yazi=(255, 255, 255), punto=22,
        yukseklik=44, sag=False, fn=f_mono):
    f = fn(punto)
    gen = d.textlength(metin, font=f) + 34
    x0 = x - gen if sag else x
    yuvarlak(d, [x0, y, x0 + gen, y + yukseklik], yukseklik / 2, dolgu=renk)
    d.text((x0 + gen / 2, y + yukseklik / 2 + 1), metin, font=f, fill=yazi,
           anchor="mm")
    return gen


def kunye(d, orta="", koyu=False):
    y = H - 56
    ana = (255, 255, 255) if koyu else MUREKKEP
    ikinci = (150, 164, 192) if koyu else SOLUK
    d.line([(KEN, y - 22), (W - KEN, y - 22)],
           fill=(42, 54, 84) if koyu else CIZGI, width=2)
    d.text((KEN, y), "@sermenkreatif", font=f_mono(23), fill=ana, anchor="lm")
    if orta:
        d.text((W / 2, y), orta, font=f_bold(22), fill=U.ACC, anchor="mm")
    d.text((W - KEN, y), "sermenkreatif.com", font=f_mono(23), fill=ikinci,
           anchor="rm")


# ------------------------------------------------------------------ kart
def _fiyat(u, spec):
    """Gönderide fiyat gösterilsin mi.

    Varsayılan kapalı: fiyat gönderide donup kalıyor, mağazada
    değişince kare yanlış kalıyor. Açmak için spec'e "fiyat": true."""
    return u.get("fiyat") if spec.get("fiyat", False) else ""


def urun_karesi(u, spec, sira=None, toplam=None, cikti=None):
    """Tek ürün karesi: üstte fotoğraf, altta ad, cümle, fiyat."""
    img = Image.new("RGB", (W, H), KAGIT)
    d = ImageDraw.Draw(img)
    renk = RENK.get(u.get("renk", spec.get("renk", "turuncu")),
                    RENK["turuncu"])
    ozl = [o for o in (u.get("ozellik") or []) if len(o) == 2][:4]

    # Önce yazı bloğu ölçülüyor, fotoğraf kalan yeri doldurmak için
    # büyütülüyor. Sabit yükseklikte altta avuç içi kadar boşluk
    # kalıyordu.
    ic = W - 2 * KEN - 26
    fa, sat = blok(d, U.P(u["ad"]), f_bold, ic, 50, 30, 2)
    cumle = U.P(u.get("satir", ""))
    fc = f_reg(26)
    sat_c = sar(d, cumle, fc, ic)[:2 if ozl else 3] if cumle else []
    yazi_h = len(sat) * 54 + 10 + len(sat_c) * 36 + (8 if sat_c else 0)
    if ozl:
        yazi_h += 4 + len(ozl) * 50
    ALT = H - 154                       # fiyat şeridinin üst kenarı
    fh = int(min(900, max(560, ALT - 24 - yazi_h - 26 - KEN)))

    zem = yerlestir(img, [KEN, KEN, W - KEN, KEN + fh], u, spec)
    d = ImageDraw.Draw(img)

    etiket = u.get("etiket") or spec.get("baslik", "")
    if etiket:
        cip(d, KEN + 22, KEN + 22, BUY(etiket)[:28], renk=LACI, punto=20,
            yukseklik=40)
    if sira and toplam:
        cip(d, W - KEN - 22, KEN + 22, "%d/%d" % (sira, toplam),
            renk=LACI, punto=20, yukseklik=40, sag=True)

    y = KEN + fh + 26
    d.rounded_rectangle([KEN, y + 4, KEN + 7, y + 64], radius=4, fill=renk)

    for i, ln in enumerate(sat):
        d.text((KEN + 26, y + i * 54), ln, font=fa, fill=MUREKKEP,
               anchor="la")
    y += len(sat) * 54 + 10

    if sat_c:
        for ln in sat_c:
            d.text((KEN + 26, y), ln, font=fc, fill=SOLUK, anchor="la")
            y += 36
        y += 8

    if ozl:
        y += 4
        for ad, dgr in ozl:
            d.line([(KEN + 26, y), (W - KEN, y)], fill=CIZGI, width=2)
            y += 14
            d.text((KEN + 26, y), BUY(ad)[:22], font=f_mono(20), fill=SOLUK,
                   anchor="la")
            fd = sigdir(d, U.P(dgr), f_reg, 600, 24, 15)
            d.text((W - KEN, y - 2), U.P(dgr), font=fd, fill=MUREKKEP,
                   anchor="ra")
            y += 36

    if _fiyat(u, spec):
        fy = ALT
        cip(d, KEN, fy, U.P(u["fiyat"]), renk=renk, punto=30,
            yukseklik=58, fn=f_bold)
        d.text((W - KEN, fy + 30), "sermenkreatif.com'da", font=f_reg(23),
               fill=SOLUK, anchor="rm")
    else:
        cip(d, KEN, ALT, "sermenkreatif.com'da", renk=renk, punto=26,
            yukseklik=58, fn=f_bold)

    kunye(d, spec.get("kunye", ""))
    if cikti:
        img.save(cikti, "JPEG", quality=93, subsampling=0, optimize=True)
        print("%s  %dx%d" % (cikti, W, H))
    return img


# ------------------------------------------------------------------ kapak
def _izgara(n, kutu):
    x0, y0, x1, y1 = kutu
    b = 12
    if n <= 1:
        return [(x0, y0, x1, y1)]
    if n == 2:
        oy = (y1 - y0 - b) / 2
        return [(x0, y0, x1, y0 + oy), (x0, y0 + oy + b, x1, y1)]
    if n == 3:
        ust = (y1 - y0) * 0.52 - b / 2
        ox = (x1 - x0 - b) / 2
        return [(x0, y0, x1, y0 + ust),
                (x0, y0 + ust + b, x0 + ox, y1),
                (x0 + ox + b, y0 + ust + b, x1, y1)]
    if n == 4:
        ox, oy = (x1 - x0 - b) / 2, (y1 - y0 - b) / 2
        return [(x0, y0, x0 + ox, y0 + oy),
                (x0 + ox + b, y0, x1, y0 + oy),
                (x0, y0 + oy + b, x0 + ox, y1),
                (x0 + ox + b, y0 + oy + b, x1, y1)]
    ox = (x1 - x0 - 2 * b) / 3
    oy = (y1 - y0 - b) / 2
    if n == 5:
        # 3 + 2: altıncı kutu boş kalınca ızgaranın köşesi delik duruyordu
        gen2 = (x1 - x0 - b) / 2
        return [(x0 + c * (ox + b), y0, x0 + c * (ox + b) + ox, y0 + oy)
                for c in range(3)] + \
               [(x0 + c * (gen2 + b), y0 + oy + b,
                 x0 + c * (gen2 + b) + gen2, y1) for c in range(2)]
    kut = []
    for r in range(2):
        for c in range(3):
            kut.append((x0 + c * (ox + b), y0 + r * (oy + b),
                        x0 + c * (ox + b) + ox, y0 + r * (oy + b) + oy))
    return kut[:6]


def kapak(spec, urunler, cikti):
    img = Image.new("RGB", (W, H), KAGIT)
    d = ImageDraw.Draw(img)
    renk = RENK.get(spec.get("renk", "turuncu"), RENK["turuncu"])

    alt = sar(d, U.P(spec.get("alt", "")), f_reg(25), W - 2 * KEN - 60) \
        if spec.get("alt") else []
    alt = alt[:2]
    y0 = KEN
    y1 = y0 + (104 + len(alt) * 32 if alt else 128)
    yuvarlak(d, [KEN, y0, W - KEN, y1], 20, dolgu=LACI)
    en = W - 2 * KEN - 60
    fb = sigdir(d, BUY(spec["baslik"]), U.anton, en, 72, 32)
    d.text((KEN + 30, y0 + 58), BUY(spec["baslik"]),
           font=fb, fill=(255, 255, 255), anchor="lm")
    for i, ln in enumerate(alt):
        d.text((KEN + 32, y0 + 120 + i * 32), ln, font=f_reg(25),
               fill=(168, 182, 208), anchor="lm")

    n = min(len(urunler), 6)
    kutular = _izgara(n, (KEN, y1 + 20, W - KEN, H - 150))
    for u, kutu in zip(urunler[:n], kutular):
        yerlestir(img, kutu, u, spec, r=18, dolu=True, pay=1.18, taban=0.88)
        dd = ImageDraw.Draw(img)
        if _fiyat(u, spec):
            cip(dd, kutu[2] - 12, kutu[3] - 54, U.P(u["fiyat"]),
                renk=LACI, punto=20, yukseklik=42, sag=True, fn=f_bold)
    d = ImageDraw.Draw(img)

    say = spec.get("spot") or ("%d ürün · hepsi kendi atölyemizde basıldı"
                               % len(urunler))
    d.text((KEN, H - 120), U.P(say), font=f_bold(27), fill=MUREKKEP,
           anchor="lm")
    d.text((W - KEN, H - 120), "kaydır »", font=f_mono(24), fill=renk,
           anchor="rm")
    kunye(d, spec.get("kunye", ""))
    img.save(cikti, "JPEG", quality=93, subsampling=0, optimize=True)
    print("%s  %dx%d" % (cikti, W, H))


# ------------------------------------------------------------------ kapanış
def kapanis(spec, urunler, cikti):
    img = Image.new("RGB", (W, H), LACI)
    d = ImageDraw.Draw(img)
    renk = RENK.get(spec.get("renk", "turuncu"), RENK["turuncu"])

    d.text((KEN, KEN + 30), BUY(spec.get("kapanis_ust", "hepsi burada")),
           font=U.anton(64), fill=(255, 255, 255), anchor="lm")
    d.text((KEN, KEN + 86),
           U.P(spec.get("kapanis_alt",
                        "Hepsi kendi atölyemizde basıldı. Ölçü, renk "
                        "ve adet isteğe göre değişir.")),
           font=f_reg(24), fill=(150, 164, 192), anchor="lm")

    ust, alt_sinir = KEN + 140, H - 210
    n = max(1, len(urunler))
    sh = int(min(118, max(74, (alt_sinir - ust) / n)))
    y = int(ust + ((alt_sinir - ust) - sh * n) / 2)
    fm = f_bold(22)
    for u in urunler:
        yuvarlak(d, [KEN, y, W - KEN, y + sh - 10], 12, dolgu=(26, 36, 62))
        d.rounded_rectangle([KEN + 3, y + 12, KEN + 9, y + sh - 22],
                            radius=3, fill=renk)
        ad = U.P(u.get("kisa") or u["ad"])
        fa = sigdir(d, ad, f_bold, W - 2 * KEN - 260, 30, 18)
        d.text((KEN + 28, y + (sh - 10) / 2), ad, font=fa,
               fill=(255, 255, 255), anchor="lm")
        if _fiyat(u, spec):
            d.text((W - KEN - 24, y + (sh - 10) / 2), U.P(u["fiyat"]),
                   font=fm, fill=renk, anchor="rm")
        y += sh

    kutu = spec.get("kapanis_kutu",
                    ["3D BASKI HİZMETİ",
                     "Kendi dosyanı yükle, fiyatını anında gör."])
    if kutu:
        yuvarlak(d, [KEN, H - 190, W - KEN, H - 100], 16, dolgu=(26, 36, 62))
        d.text((KEN + 28, H - 162), BUY(kutu[0]), font=f_mono(21),
               fill=renk, anchor="lm")
        d.text((KEN + 28, H - 128), U.P(kutu[1]), font=f_reg(23),
               fill=(214, 221, 232), anchor="lm")
    kunye(d, spec.get("kunye", ""), koyu=True)
    img.save(cikti, "JPEG", quality=93, subsampling=0, optimize=True)
    print("%s  %dx%d" % (cikti, W, H))


# ------------------------------------------------------------------ hikaye
def hikaye(spec, urunler, cikti):
    u = urunler[0]
    img = Image.new("RGB", (SW, SH), KAGIT)
    d = ImageDraw.Draw(img)
    renk = RENK.get(u.get("renk", spec.get("renk", "turuncu")),
                    RENK["turuncu"])

    FY = 1150
    yerlestir(img, [0, 0, SW, FY], u, spec, r=0, dolu=True, pay=1.25,
              taban=0.88)
    d = ImageDraw.Draw(img)
    d.rectangle([0, FY, SW, SH], fill=KAGIT)

    cip(d, 48, 60, BUY(u.get("etiket") or spec.get("baslik", ""))[:26],
        renk=LACI, punto=22, yukseklik=48)

    y = FY + 70
    d.rounded_rectangle([48, y + 4, 55, y + 64], radius=4, fill=renk)
    fa, sat = blok(d, U.P(u.get("kisa") or u["ad"]), f_bold, SW - 150, 56,
                   32, 3)
    for i, ln in enumerate(sat):
        d.text((76, y + i * 62), ln, font=fa, fill=MUREKKEP, anchor="la")
    y += len(sat) * 62 + 20

    cumle = u.get("satir", "")
    if cumle:
        fc = f_reg(30)
        for ln in sar(d, U.P(cumle), fc, SW - 150)[:3]:
            d.text((76, y), ln, font=fc, fill=SOLUK, anchor="la")
            y += 42

    if _fiyat(u, spec):
        cip(d, 48, min(y + 34, SH - 280), U.P(u["fiyat"]), renk=renk,
            punto=36, yukseklik=72, fn=f_bold)
    d.text((SW / 2, SH - 150), U.P("linke dokun »"), font=f_bold(34),
           fill=MUREKKEP, anchor="mm")
    d.text((SW / 2, SH - 96), "sermenkreatif.com", font=f_mono(28),
           fill=SOLUK, anchor="mm")
    img.save(cikti, "JPEG", quality=92, subsampling=0, optimize=True)
    print("%s  %dx%d" % (cikti, SW, SH))


# ------------------------------------------------------------------ ana
def uret(spec, klasor):
    U.theme(spec.get("kategori", "3dbaski"))
    kat = _bilgi()
    urunler = [coz(u, kat) for u in spec["urunler"]]
    eksik = [u for u in urunler if not u.get("gorsel")]
    if eksik:
        raise SystemExit("fotoğraf yok: " +
                         ", ".join(u.get("slug", u.get("ad", "?"))
                                   for u in eksik))
    os.makedirs(klasor, exist_ok=True)

    tek = len(urunler) == 1 or spec.get("tip") == "tek"
    n = 0
    if not tek:
        n += 1
        kapak(spec, urunler, os.path.join(klasor, "1.jpg"))
    toplam = len(urunler)
    for i, u in enumerate(urunler, 1):
        n += 1
        urun_karesi(u, spec, None if tek else i, None if tek else toplam,
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
