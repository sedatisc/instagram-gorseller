#!/usr/bin/env python3
"""YouTube Shorts kurgusu — Instagram reels'inden ayrı bir video.

Reels sakin: 4 saniyelik sahneler, yavaş açılan paneller. Shorts akışında
o kurgu ilk saniyede kaybediyor. Buradaki kurgu başka:

- Ürün arka planından kesilmiş olarak geliyor; beyaz kutu yok, kadrajın
  altına taşıyor, nefes alıyor
- Metinden **rakam** ayrılıyor: "55 W" ekranı dolduruyor, cümlenin kalanı
  altında küçük. Rakam sıfırdan yukarı sayıyor
- Her kesim vuruşa denk geliyor (96 BPM, 0,625 sn); kesimde kadraj sıçrıyor
- Üstte ilerleme çubuğu — izleyici videonun kısa olduğunu görüyor
- Altında kendi ürettiğimiz ritim var: telifsiz, çünkü biz üretiyoruz

Metin YouTube kuyruğundan geliyor (`youtube/DURUM.json`): `baslik` kanca,
`satirlar` vuruşlar. Yani videonun içeriği de Instagram'dan ayrı.

    python3 shorts.py <klasor>              # <klasor>/shorts.mp4
    python3 shorts.py <klasor> --sessiz     # ritim koymadan
    python3 shorts.py --tumu                # kuyruktaki her video
"""
import json
import math
import os
import re
import subprocess
import sys
import wave

from PIL import Image, ImageDraw, ImageFilter

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import uret as U                                         # noqa: E402
import reels as R                                        # noqa: E402

SW, SH = 1080, 1920
FPS = 30
GUT = 84
SAG = SW - GUT
BPM = 96.0
VURUS = 60.0 / BPM                                        # 0,625 sn


def yum(t):
    return R.yum(t)


def vur(t, basla=0.0, hiz=0.24):
    """Hızlı giren, sonunda yavaşlayan ilerleme."""
    if hiz <= 0:
        return 1.0
    x = max(0.0, min(1.0, (t - basla) / hiz))
    return 1 - (1 - x) ** 3


def zipla(t, hiz=0.34, tasma=1.12):
    """Yaylanma: hedefi aşıp geri oturuyor. Kesimdeki sıçrama bu."""
    x = max(0.0, min(1.0, t / hiz))
    return 1 + (tasma - 1) * (1 - x) * math.cos(x * math.pi * 1.6)


def a(renk, op):
    return tuple(renk[:3]) + (int(max(0, min(255, 255 * op))),)


# ----------------------------------------------------------------- zemin
_Z = {}


def zemin():
    if "z" not in _Z:
        _Z["z"] = R._zemin_ciz()
    return _Z["z"].copy()


def golge_yazi(img, xy, metin, font, renk, alfa=255, anchor="la", kalin=0):
    if alfa <= 4:
        return
    d = ImageDraw.Draw(img)
    d.text(xy, metin, font=font, fill=a(renk, alfa / 255.0), anchor=anchor,
           stroke_width=kalin, stroke_fill=a((0, 0, 0), 0.6 * alfa / 255.0))


def sar(d, metin, font, en):
    kel, satir, suan = metin.split(), [], ""
    for k in kel:
        dene = (suan + " " + k).strip()
        if d.textlength(dene, font=font) <= en or not suan:
            suan = dene
        else:
            satir.append(suan)
            suan = k
    if suan:
        satir.append(suan)
    return satir


def blok(d, metin, maker, en, azami, bas, taban=40):
    """Punto, metnin **tamamı** sığacak şekilde küçülüyor.

    Eskiden en uzun kelimeye göre punto seçilip satırlar kesiliyordu;
    "…ne kesmez?" gibi son satır sessizce düşüyordu. Artık satır sayısı
    sınırı aşarsa punto iniyor, cümle hep tam."""
    s = bas
    while s > taban:
        f = maker(s)
        sat = sar(d, metin, f, en)
        if len(sat) <= azami:
            return f, sat
        s -= 4
    f = maker(taban)
    return f, sar(d, metin, f, en)


def BUY(s):
    """Türkçe büyük harf: i → İ, ı → I. Python'un upper'ı 'kesmiyor'u
    'KESMIYOR' yapıyor; okuyan gözü tırmalıyor.

    Rakamdan önce gelen i'ye dokunulmuyor: "i8", "i7" model adı, "İ8"
    olmaz."""
    cik = []
    for i, c in enumerate(s):
        if c == "i" and i + 1 < len(s) and s[i + 1].isdigit():
            cik.append("I")
        elif c == "i":
            cik.append("İ")
        elif c == "ı":
            cik.append("I")
        else:
            cik.append(c)
    return "".join(cik).upper()


# ------------------------------------------------------------ ürün kesiti
def _kesik_yolu(ad):
    """Kesilmiş sürümün yolu. Görselin kendisi zaten kesikse (adı
    `kesik-` ile başlıyorsa) tekrar kesilmiyor — `kesik-kesik-*`
    dosyaları böyle oluşmuştu ve ikinci kesme kenarları yiyordu."""
    kok = os.path.splitext(os.path.basename(ad))[0]
    if kok.startswith("kesik-"):
        return os.path.join(KOK, "gorsel", "urun", kok + ".png")
    return os.path.join(KOK, "gorsel", "urun", "kesik-%s.png" % kok)


def _kes(kaynak, hedef):
    """Arka planı kes. Model u2net'e sabit — varsayılan model belleği
    dolduruyor. Sonuç saklanıyor, bir daha kesilmiyor."""
    from rembg import remove, new_session
    if "s" not in _Z:
        _Z["s"] = new_session("u2net")
    k = remove(Image.open(kaynak).convert("RGBA"), session=_Z["s"])
    bb = k.split()[-1].point(lambda v: 255 if v > 8 else 0).getbbox()
    if bb:
        k = k.crop(bb)
    os.makedirs(os.path.dirname(hedef), exist_ok=True)
    k.save(hedef)
    return k


def foto(klasor, spec):
    """Gönderinin ürün karesi — arka planı kesilmiş hâliyle.

    Beyaz zeminli ürün fotoğrafı koyu kadrajda beyaz bir kutu gibi
    duruyordu; kesik sürüm kadraja yayılıyor."""
    adaylar = []
    k = spec.get("kapak", {})
    for c in k.get("sutunlar", []) or []:
        if c.get("gorsel"):
            adaylar.append(c["gorsel"])
    if k.get("gorsel"):
        adaylar.append(k["gorsel"])
    for g in spec.get("gorseller", []) or []:
        adaylar.append(g if isinstance(g, str) else g.get("gorsel", ""))
    for ad in adaylar:
        if not ad:
            continue
        kes_yol = _kesik_yolu(ad)
        if os.path.exists(kes_yol):
            im = Image.open(kes_yol).convert("RGBA")
            im.info["anahtar"] = kes_yol
            return im
        ham = os.path.join(KOK, "gorsel", ad)
        if not os.path.exists(ham):
            ham = os.path.join(KOK, "gorsel", "urun", ad)
        if os.path.exists(ham):
            try:
                im = _kes(ham, kes_yol)
            except Exception as e:
                print("   kesilemedi (%s): %s" % (ad, e))
                im = Image.open(ham).convert("RGBA")
            im.info["anahtar"] = kes_yol
            return im
    return None


KS = 6                       # yumuşak katmanlar 1/6 ölçekte çiziliyor
_ON = {}


MARJ = 36                    # ürün ile kadraj kenarı arasındaki en az boşluk


def _taban(kat, yuk):
    """Kesiti bir kez ölçekle — her karede LANCZOS pahalı.

    Ölçek hem yüksekliğe hem genişliğe bakıyor: geniş bir makine
    yüksekliğe sığdırılınca yanlardan taşıyordu.

    Anahtar **dosya yolu**. Önce `id(kat)` idi: bir görsel serbest
    kalınca Python aynı adresi yeni görsele veriyor ve toplu basımda
    video başka ürünün fotoğrafıyla çıkıyordu."""
    k = "%s-%d" % (kat.info.get("anahtar", id(kat)), yuk)
    if k not in _ON:
        o = min((SW - 2 * MARJ) / kat.width, yuk / kat.height)
        _ON[k] = kat.resize((max(1, int(kat.width * o)),
                             max(1, int(kat.height * o))), Image.LANCZOS)
    return _ON[k]


def _yumusak(ciz, bulanik):
    """Küçük tuvale çiz, bulanıklaştır, büyüt. Sonuç zaten yumuşak."""
    k = Image.new("RGBA", (SW // KS, SH // KS), (0, 0, 0, 0))
    ciz(ImageDraw.Draw(k), 1.0 / KS)
    return k.filter(ImageFilter.GaussianBlur(bulanik / KS)).resize(
        (SW, SH), Image.BILINEAR)


def urun(img, kat, t, sure, taban=1760, yuk=940, kay=0.0, acilis=0.0,
         kadraj=0, ust=None):
    """Ürün kadrajın altına oturuyor, nefes alıyor, hafif süzülüyor.

    Beyaz dikdörtgen yok: kesilmiş görselin arkasına renkli bir ışık
    konuyor, görsel onun üstünde duruyor.

    `kadraj` sahne sırası: her sahnede ölçek, yan kayma ve süzülme yönü
    değişiyor. Aynı kadraj baştan sona durursa video tek kare gibi
    görünüyor — asıl şikâyet oydu."""
    if kat is None:
        return
    p = t / max(0.001, sure)
    yuk = yuk * (1.0, 0.88, 1.06, 0.94)[kadraj % 4]
    kay = kay + (0, -88, 74, -40)[kadraj % 4]
    yon = 1 if kadraj % 2 == 0 else -1
    # Nefes ve giriş **küçülterek** çalışıyor, büyüterek değil: büyüterek
    # yaparken ürün kutuyu aşıp kadrajdan taşıyordu, yarısı görünüyordu.
    nefes = 0.955 + 0.045 * p + 0.010 * math.sin(2 * math.pi * (t / VURUS) / 4)
    giris = min(1.0, zipla(t, 0.4, 1.07) - 0.07) if acilis else 1.0
    # `buyuk` zaten kutuya tam sığan en büyük hâli; buradan yalnız
    # küçülüyoruz. Önce genişliğe sığdırıp sonra yüksekliğe göre tekrar
    # büyütmek, geniş makineleri yanlardan kırpan hataydı.
    buyuk = _taban(kat, yuk)
    o = min(1.0, nefes) * min(1.0, giris)
    yeni = buyuk.resize((max(1, int(buyuk.width * o)),
                         max(1, int(buyuk.height * o))), Image.BILINEAR)
    x = int((SW - yeni.width) / 2 + kay + yon * 22 * math.sin(p * math.pi))
    # Geniş makine yüksekliğe sığmıyor, alta yapışınca ortada koca boşluk
    # kalıyordu. Kalan bandın ortasına oturuyor.
    if ust is None:
        y = int(taban - yeni.height)
    else:
        y = int(ust + (taban - ust - yeni.height) / 2)
    # Son kontrol: hiçbir karede kenardan taşmasın. Kayma ve nefes ne
    # yaparsa yapsın ürün bütün görünüyor.
    x = max(MARJ, min(SW - MARJ - yeni.width, x))
    y = max(MARJ, min(SH - MARJ - yeni.height, y))
    cx, cy = x + yeni.width / 2, y + yeni.height * 0.62

    def isik(d, s):
        rw, rh = yeni.width * 0.62 * s, yeni.height * 0.46 * s
        d.ellipse([cx * s - rw, cy * s - rh, cx * s + rw, cy * s + rh],
                  fill=a(U.AC(), 0.34))
        d.ellipse([cx * s - rw * .5, cy * s - rh * .5,
                   cx * s + rw * .5, cy * s + rh * .5], fill=a(U.AC(), 0.30))
    img.alpha_composite(_yumusak(isik, 120))

    def golge(d, s):
        d.ellipse([(cx - yeni.width * 0.40) * s, (taban - 54) * s,
                   (cx + yeni.width * 0.40) * s, (taban + 34) * s],
                  fill=(0, 0, 0, 150))
    img.alpha_composite(_yumusak(golge, 40))
    img.alpha_composite(yeni, (x, y))


def karart(img, y0, y1, op=0.62):
    """Yazının arkasını karart — ürünün üstüne binen satır okunsun."""
    img.alpha_composite(_yumusak(
        lambda d, s: d.rectangle([0, y0 * s, SW * s, y1 * s], fill=a(U.BG, op)),
        44))


def serit(img, p):
    """Üstte ilerleme çubuğu: video kısa, izleyici bunu görsün."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, SW, 9], fill=a(U.FG(), 0.14))
    d.rectangle([0, 0, SW * max(0.0, min(1.0, p)), 9], fill=U.AC())


def carp(img, t, guc=0.5):
    """Kesimde kısa parlama — göz kesimi fark etsin."""
    if t > 0.07:
        return
    op = (1 - t / 0.07) * guc * 0.13
    kat = Image.new("RGBA", (SW, SH), a(U.AC(), op))
    img.alpha_composite(kat)


# ---------------------------------------------------------- metin ayırma
BIRIM = (r"mm/s|mm³/s|km/h|mAh|MHz|GHz|kWh|°C|mm|cm|µm|kg|kW|GB|MB|TB|Wh|"
         r"dpi|rpm|ml|dk|sn|W|V|A|g|L|\$|₺|TL|dolar|kat|adet|renk|saat|"
         r"inç|bit|çekirdek|kanal|eksen|nozul|kafa")
_HARF = "A-Za-zÇĞİIÖŞÜçğıöşü"
_RAKAM = re.compile(r"(?<![%s\d])(\d[\d.,]*(?:\s*[×x]\s*\d[\d.,]*)*)\s*(%s)?"
                    r"(?![%s])" % (_HARF, BIRIM, _HARF), re.IGNORECASE)


def ayir(metin):
    """Cümleden rakamı çek: ('55 W', 'CO2 lazer, 600 × 300 mm tezgâh').

    İki kural var, ikisi de yanlış kesmeyi engelliyor:
    - Rakamın önünde harf olmayacak. Yoksa "R1" → "1", "S2" → "2" oluyor.
    - Rakam cümlenin kalanından ancak **başındaysa** çıkarılıyor. Ortadan
      çıkarınca "…yapıyor, 0,2 mm altı" → "…yapıyor, altı" gibi sakat
      cümle kalıyor; o durumda cümle olduğu gibi altta duruyor.

    Rakam yoksa (None, cümle) dönüyor; o zaman cümle sahnesi çiziliyor."""
    for m in _RAKAM.finditer(metin):
        sayi = re.sub(r"\s*([×x])\s*", " × ", m.group(1)).strip()
        birim = (m.group(2) or "").strip()
        if not birim and "×" not in sayi:     # birimsiz yalın sayı başlık olmaz
            continue
        buyuk = (sayi + " " + birim).strip()
        if len(buyuk) > 16:                   # "600 × 300 mm" sınırda, üstü yok
            continue
        if m.start() <= 1:
            kalan = re.sub(r"\s+", " ", metin[m.end():]).strip(" ,;·-–—")
        else:
            kalan = metin.strip()
        return buyuk, kalan
    return None, metin.strip()


def say(buyuk, p):
    """Rakamı sıfırdan yukarı say — duran rakam fark edilmiyor."""
    if p >= 0.999:
        return buyuk
    def tek(m):
        ham = m.group(0)
        try:
            deger = float(ham.replace(".", "").replace(",", "."))
        except ValueError:
            return ham
        simdi = deger * yum(p)
        if deger >= 1000:
            return "{:,.0f}".format(simdi).replace(",", ".")
        if deger == int(deger):
            return "%d" % round(simdi)
        return ("%.1f" % simdi).replace(".", ",")
    return re.sub(r"\d[\d.,]*", tek, buyuk)


# ----------------------------------------------------------------- sahneler
def sahne_kanca(baslik, kanca, kat, t, sure, ilerleme):
    img = zemin()
    # Ürün fotoğrafı olmayan konularda (nozul aşınması, kondansatör ESR)
    # yazı kadrajın ortasına iniyor; yoksa alt yarı bomboş kalıyor.
    bos = kat is None
    if not bos:
        urun(img, kat, t, sure, taban=1880, yuk=900, acilis=1.0, ust=1060)
        karart(img, 0, 1030, 0.72)
    d = ImageDraw.Draw(img)

    f, satir = blok(d, BUY(baslik), U.anton, SAG - GUT, 4, 168, 96)
    y = 290 if not bos else 560 - len(satir) * f.size * 0.5
    for i, s in enumerate(satir):
        p = vur(t, 0.04 + i * 0.1, 0.19)
        if p <= 0.01:
            continue
        golge_yazi(img, (GUT, y + i * f.size * 1.08 + (1 - p) * 56), s, f,
                   U.FG() if i < len(satir) - 1 else U.AC(), 255 * p)
    alt = y + len(satir) * f.size * 1.08 + 24
    pb = vur(t, 0.42, 0.3)
    if pb > 0.02:
        ImageDraw.Draw(img).rounded_rectangle(
            [GUT, alt, GUT + (SAG - GUT) * pb, alt + 12], radius=6, fill=U.AC())
    if kanca:
        pk = vur(t, 0.58, 0.3)
        fk, sk = blok(d, kanca, lambda s: U.pop(s, "SemiBold"), SAG - GUT, 3,
                      54, 38)
        for i, s in enumerate(sk):
            golge_yazi(img, (GUT, alt + 46 + i * fk.size * 1.34
                             + (1 - pk) * 24), s, fk, U.FG2(), 240 * pk)
    carp(img, t, 0.7)
    serit(img, ilerleme)
    return img


def sahne_rakam(buyuk, kalan, sira, toplam, kat, t, sure, ilerleme,
                kadraj=0):
    """Rakam ekranı dolduruyor, cümlenin kalanı altında küçük."""
    img = zemin()
    bos = kat is None
    if not bos:
        urun(img, kat, t, sure, taban=1880, yuk=940, acilis=1.0,
             kadraj=kadraj, ust=980)
        karart(img, 0, 1030, 0.68)
    kay = 0 if not bos else 420
    d = ImageDraw.Draw(img)

    golge_yazi(img, (GUT, 250 + kay), "%02d / %02d" % (sira, toplam),
               U.mono(36, True), U.SOFT(), 215 * vur(t, 0, 0.2))

    oran = min(1.0, (t / max(0.001, sure)) / 0.5)
    yazi = say(buyuk, oran)
    f = U.fit(d, buyuk, U.anton, SAG - GUT, 300, 150)
    p = vur(t, 0.0, 0.2)
    ol = zipla(t, 0.3, 1.08)
    fy = U.anton(max(60, int(f.size * ol)))
    golge_yazi(img, (GUT, 330 + kay + (1 - p) * 40), yazi, fy, U.FG(), 255 * p)

    y = 330 + kay + f.size * 1.1 + 40
    if kalan:
        fk, sk = blok(d, kalan, lambda s: U.pop(s, "SemiBold"), SAG - GUT, 3,
                      62, 40)
        for i, s in enumerate(sk):
            pp = vur(t, 0.18 + i * 0.07, 0.22)
            golge_yazi(img, (GUT, y + i * fk.size * 1.3 + (1 - pp) * 26), s, fk,
                       U.FG2(), 240 * pp)
    cp = vur(t, 0.0, 0.26)
    ImageDraw.Draw(img).rounded_rectangle(
        [GUT, 286 + kay, GUT + 150 * cp, 298 + kay], radius=6, fill=U.AC())
    carp(img, t, 1.0)
    serit(img, ilerleme)
    return img


def sahne_cumle(metin, sira, toplam, kat, t, sure, ilerleme, kadraj=0):
    """Rakamsız satır: kelime kelime vuran cümle."""
    img = zemin()
    bos = kat is None
    if not bos:
        urun(img, kat, t, sure, taban=1880, yuk=900, acilis=1.0,
             kadraj=kadraj, ust=1020)
        karart(img, 0, 1000, 0.68)
    kay = 0 if not bos else 420
    d = ImageDraw.Draw(img)

    golge_yazi(img, (GUT, 250 + kay), "%02d / %02d" % (sira, toplam),
               U.mono(36, True), U.SOFT(), 215 * vur(t, 0, 0.2))

    f, satir = blok(d, BUY(metin), U.anton, SAG - GUT, 4, 150, 86)
    y = 360 + kay
    for i, s in enumerate(satir):
        p = vur(t, 0.03 + i * 0.1, 0.2)
        if p <= 0.01:
            continue
        golge_yazi(img, (GUT, y + i * f.size * 1.1 + (1 - p) * 44), s, f,
                   U.FG() if i < len(satir) - 1 else U.AC(), 255 * p)
    cp = vur(t, 0.0, 0.26)
    ImageDraw.Draw(img).rounded_rectangle(
        [GUT, 300 + kay, GUT + 150 * cp, 312 + kay], radius=6, fill=U.AC())
    carp(img, t, 1.0)
    serit(img, ilerleme)
    return img


def sahne_kapanis(kat, t, sure, ilerleme):
    img = zemin()
    if kat is not None:
        urun(img, kat, t, sure, taban=1890, yuk=620, acilis=1.0, kadraj=2,
             ust=1330)
        karart(img, 0, 1330, 0.80)
    p0 = vur(t, 0.0, 0.26)
    R.marka_yazi(img, (SW / 2, 700), 84, int(255 * p0))
    p1 = vur(t, 0.16, 0.26)
    ol = zipla(t - 0.16, 0.34, 1.1) if t > 0.16 else 1.0
    golge_yazi(img, (SW / 2, 960), "ABONE OL", U.anton(max(60, int(146 * ol))),
               U.AC(), 255 * p1, "mm")
    p2 = vur(t, 0.42, 0.28)
    golge_yazi(img, (SW / 2, 1110), "Her gün yeni bir Short",
               U.pop(40, "Medium"), U.FG(), 240 * p2, "mm")
    golge_yazi(img, (SW / 2, 1190), "sermenkreatif.com", U.mono(32, True),
               U.SOFT(), 225 * p2, "mm")
    carp(img, t, 1.0)
    serit(img, ilerleme)
    return img


# -------------------------------------------------------------------- ses
def ritim(saniye, yol):
    """Kendi ürettiğimiz ritim — telif derdi yok, tempo kurguyla aynı."""
    import numpy as np
    sr = 44100
    n = int(saniye * sr)
    t = np.arange(n) / sr
    ses = np.zeros(n)

    k = 0
    while k * VURUS < saniye:                     # kick
        i = int(k * VURUS * sr)
        boy = int(0.18 * sr)
        tt = np.arange(min(boy, n - i)) / sr
        f = 130 * np.exp(-tt * 30) + 48
        ses[i:i + len(tt)] += 0.60 * np.sin(2 * np.pi * f * tt) \
            * np.exp(-tt * 15)
        k += 1

    k = 0
    while (k + 0.5) * VURUS < saniye:             # hi-hat
        i = int((k + 0.5) * VURUS * sr)
        boy = int(0.045 * sr)
        gur = np.random.RandomState(k).rand(min(boy, n - i)) * 2 - 1
        ses[i:i + len(gur)] += 0.11 * gur * np.exp(
            -np.arange(len(gur)) / sr * 95)
        k += 1

    k = 2                                         # 2. ve 4. vuruşta trampet
    while k * VURUS < saniye:
        i = int(k * VURUS * sr)
        boy = int(0.12 * sr)
        tt = np.arange(min(boy, n - i)) / sr
        gur = np.random.RandomState(100 + k).rand(len(tt)) * 2 - 1
        ses[i:i + len(tt)] += (0.16 * gur + 0.10 * np.sin(
            2 * np.pi * 190 * tt)) * np.exp(-tt * 26)
        k += 4

    bas = 55.0 * 2 ** (np.floor(t / (VURUS * 8)) % 2 * 3 / 12.0)
    ses += 0.07 * np.sin(2 * np.pi * np.cumsum(bas) / sr)
    ses = np.tanh(ses * 1.25)
    ses = (ses / max(1e-6, np.abs(ses).max()) * 0.70 * 32767).astype("<i2")

    with wave.open(yol, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(ses.tobytes())


# ------------------------------------------------------------------- akış
def kurgu(klasor):
    spec = json.load(open(os.path.join(KOK, klasor, "spec.json"),
                          encoding="utf-8"))
    yt = json.load(open(os.path.join(KOK, "youtube", "DURUM.json"),
                        encoding="utf-8"))
    kayit = next((k for k in yt["kuyruk"] if k["klasor"] == klasor), None)
    if kayit is None:
        raise SystemExit("%s YouTube kuyruğunda yok — metin oradan geliyor"
                         % klasor)

    # Zemin her zaman koyu — gönderinin kendi zemini alınmıyor.
    # Açık zeminli gönderilerde U.FG() koyu laciverte dönüyor; shorts
    # kadrajı koyu olduğu için yazı yazının üstünde kayboluyordu.
    # Kanalın tek bir görünümü olması da doğrusu: vurgu rengi
    # kategoriden geliyor, çeşitlilik oradan.
    U.theme(spec["kategori"])
    U.zemin_ayarla("koyu")
    U.stil_ayarla(spec.get("stil", "neon"))

    kat = foto(klasor, spec)
    # Kanca açılışta başlığın altında duruyor; vuruşlar yalnız maddelerden.
    # Eskiden kanca ilk vuruş olarak da çiziliyordu, başlıkla tekrar ediyordu.
    kanca = (kayit.get("kanca") or "").strip(" -–—·")
    satir = [s.strip() for s in kayit.get("satirlar", []) if s.strip()][:4]
    if not satir and kanca:
        satir = [kanca]
        kanca = ""

    # kesimler vuruş ızgarasında: kanca 5, her satır 3, kapanış 3 vuruş
    plan = [(5, "kanca")] + [(3, s) for s in satir] + [(3, "kapanis")]
    toplam = sum(v for v, _ in plan) * VURUS
    sahneler, gecen = [], 0.0
    for i, (v, ne) in enumerate(plan):
        sure = v * VURUS
        bas = gecen
        if ne == "kanca":
            f = lambda t, s, b=bas: sahne_kanca(
                kayit["baslik"], kanca, kat, t, s, (b + t) / toplam)
        elif ne == "kapanis":
            f = lambda t, s, b=bas: sahne_kapanis(kat, t, s, (b + t) / toplam)
        else:
            sira = i
            buyuk, kalan = ayir(ne)
            if buyuk:
                f = lambda t, s, b=bas, B=buyuk, K=kalan, n=sira: sahne_rakam(
                    B, K, n, len(satir), kat, t, s, (b + t) / toplam, n)
            else:
                f = lambda t, s, b=bas, M=kalan, n=sira: sahne_cumle(
                    M, n, len(satir), kat, t, s, (b + t) / toplam, n)
        sahneler.append((sure, f))
        gecen += sure
    return sahneler


def uret_bir(klasor, cikti=None, sessiz=False):
    cikti = cikti or os.path.join(KOK, klasor, "shorts.mp4")
    # Önbellekler videoya özel: zemin gönderinin kendi vurgu renginden
    # çiziliyor, --tumu ilk videonunkini ötekilere taşımasın.
    _Z.pop("z", None)
    _ON.clear()
    sahneler = kurgu(klasor)
    toplam = sum(s for s, _ in sahneler)

    ses_yolu = os.path.join("/tmp", "shorts-ritim.wav")
    if not sessiz:
        ritim(toplam + 0.4, ses_yolu)

    komut = ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (SW, SH),
             "-r", str(FPS), "-i", "-"]
    if sessiz:
        komut += ["-f", "lavfi", "-i",
                  "anullsrc=channel_layout=stereo:sample_rate=44100"]
    else:
        komut += ["-i", ses_yolu]
    komut += ["-c:v", "libx264", "-preset", "medium", "-crf", "20",
              "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
              "-shortest", "-movflags", "+faststart", cikti]
    ff = subprocess.Popen(komut, stdin=subprocess.PIPE)

    sayac = 0
    for sure, ciz in sahneler:
        for i in range(int(round(sure * FPS))):
            ff.stdin.write(ciz(i / FPS, sure).convert("RGB").tobytes())
            sayac += 1
    ff.stdin.close()
    ff.wait()
    print("%s  %.1f sn  %d kare  %.1f MB"
          % (cikti, toplam, sayac, os.path.getsize(cikti) / 1048576.0))


def main():
    arg = [x for x in sys.argv[1:] if not x.startswith("--")]
    sessiz = "--sessiz" in sys.argv
    if "--tumu" in sys.argv:
        yt = json.load(open(os.path.join(KOK, "youtube", "DURUM.json"),
                            encoding="utf-8"))
        for k in yt["kuyruk"]:
            kl = k["klasor"]
            if not os.path.exists(os.path.join(KOK, kl, "spec.json")):
                print("· %s — spec.json yok, atlandı" % kl)
                continue
            try:
                uret_bir(kl, sessiz=sessiz)
            except Exception as e:
                print("· %s — HATA: %s" % (kl, e))
        return
    uret_bir(arg[0], arg[1] if len(arg) > 1 else None, sessiz)


if __name__ == "__main__":
    main()
