#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gönderi spec'inden dikey Reels videosu üretir.

Kullanım:  python3 reels.py gonderi/spec.json gonderi/reels.mp4

1080 x 1920, 30 fps, sessiz. Ses Instagram'da eklenecek — uygulamadaki
trend sesi seçmek hem kolay hem erişime yarıyor.

Kareler ffmpeg'e ham olarak boru ile veriliyor, diske yazılmıyor.
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw

import uret as U
from uret import (P, a, anton, archivo, bright_logo, fit, glow, gorsel_var,
                  mono, over, pop, wrap)

SW, SH = 1080, 1920
FPS = 30
GUT = 72
SAG = SW - GUT

# Instagram arayüzü üstte ~250, altta ~380 px kaplıyor
UST_EMNIYET = 300
ALT_EMNIYET = 1560


def yum(t):
    """ease-out cubic"""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def gecis(t, sure, basla=0.0, hiz=0.45):
    """0..1 arası ilerleme — basla saniyesinde başlayıp hiz saniyede biter."""
    if sure <= 0:
        return 1.0
    return yum((t - basla) / hiz) if hiz > 0 else 1.0


_ZEMIN = {}
_MASKE = {}


def zemin():
    """Arka plan karede değişmiyor — bir kere çiz, kopyasını ver."""
    if "z" not in _ZEMIN:
        _ZEMIN["z"] = _zemin_ciz()
    return _ZEMIN["z"].copy()


def _zemin_ciz():
    if U._mod() != "koyu":
        return U.base_renkli(SW, SH)
    img = Image.new("RGBA", (SW, SH), U.BG + (255,))

    if U._duru():
        gr = Image.new("RGB", (SW, SH), U.BG)
        gd = ImageDraw.Draw(gr)
        ust = U._kar(U.BG, 0.055)
        for y in range(SH):
            t = y / (SH - 1)
            gd.line([(0, y), (SW, y)], fill=tuple(
                int(ust[i] + (U.BG[i] - ust[i]) * t) for i in range(3)))
        img = gr.convert("RGBA")
    else:
        def huzme(d):
            d.line([(-300, 1200), (900, -200)], fill=a(U.AC(), 0.55),
                   width=190)
            d.line([(200, 2200), (1400, 700)], fill=a(U.AC(), 0.35),
                   width=130)
        img.alpha_composite(glow((SW, SH), huzme, 110))

    nokta = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    nd = ImageDraw.Draw(nokta)
    for y in range(0, SH, 58):
        for x in range(0, SW, 58):
            nd.ellipse([x - 1, y - 1, x + 1, y + 1], fill=a(U.AC(), 0.09))
    img.alpha_composite(nokta)
    return img


def serit(img, oran):
    """Üstte ince ilerleme çubuğu — izleyici ne kadar kaldığını görüyor."""
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([GUT, 232, SAG, 240], radius=4,
                        fill=a(U.FG(), 0.18))
    w = (SAG - GUT) * max(0.0, min(1.0, oran))
    if w > 6:
        d.rounded_rectangle([GUT, 232, GUT + w, 240], radius=4, fill=U.AC())


def kunye(img):
    logo = bright_logo(30)
    d = ImageDraw.Draw(img)
    lw = d.textlength(U.LABEL, font=mono(21, True))
    if U._parlaklik(img, 150, 250) > 105:
        # şerit parlak zemine denk geldi — altına yumuşak karartma
        img.alpha_composite(glow((SW, SH), lambda g: g.rounded_rectangle(
            [GUT - 34, 136, GUT + logo.width + 36 + lw, 266], radius=44,
            fill=(2, 4, 10, 225)), 32))
    img.alpha_composite(logo, (GUT, 160))
    d = ImageDraw.Draw(img)
    d.text((GUT + logo.width + 20, 177), U.LABEL, font=mono(21, True),
           fill=a(U.AC(), 0.9), anchor="lm")


BANT = 1060          # fotoğraf bandının yüksekliği
ZOOM = 1.12          # yavaş yaklaşma payı


def reels_yolu(ad):
    """Varsa Reels için ayrıca hazırlanmış kareyi kullan."""
    if not ad:
        return None
    kok, uz = os.path.splitext(ad)
    return gorsel_var(kok + "-reels" + uz) or gorsel_var(kok + "-reels.jpg") \
        or gorsel_var(ad)


def foto_katman(ad, bant=BANT, odak=0.34):
    """Bandı dolduracak, zoom payı olan fotoğraf katmanı."""
    yol = reels_yolu(ad)
    if not yol:
        return None
    gw, gh = int(SW * ZOOM), int(bant * ZOOM)
    im = Image.open(yol).convert("RGB")
    o = max(gw / im.width, gh / im.height)
    im = im.resize((max(1, int(im.width * o)), max(1, int(im.height * o))),
                   Image.LANCZOS)
    kx = max(0, (im.width - gw) // 2)
    ky = max(0, int((im.height - gh) * odak))
    return im.crop((kx, ky, kx + gw, ky + gh))


def _erit_maske(w, h, erit):
    k = (w, h, erit)
    if k not in _MASKE:
        m = Image.new("L", (w, h), 255)
        md = ImageDraw.Draw(m)
        for i in range(min(erit, h)):
            md.line([(0, h - 1 - i), (w, h - 1 - i)],
                    fill=int(255 * (i / float(erit)) ** 0.9))
        _MASKE[k] = m
    return _MASKE[k]


def bant_ciz(img, kat, t, bant=BANT, erit=240, ilerle=0.0):
    """Fotoğraf bandını yavaş yaklaşarak çiz, alt kenarını zemine erit."""
    s = ZOOM - (ZOOM - 1.0) * yum(min(1.0, ilerle + t))
    pw, ph = int(SW * s), int(bant * s)
    x = (kat.width - pw) // 2
    y = int((kat.height - ph) * 0.5)
    kare = kat.crop((x, y, x + pw, y + ph)).resize((SW, bant), Image.BILINEAR)
    kare = kare.convert("RGBA")
    kare.putalpha(_erit_maske(SW, bant, erit))
    img.alpha_composite(kare, (0, 0))
    ust = U._perde_op(U._parlaklik(img, 120, 300)) * 0.9
    U._perde(img, 0, 340, ust, 0.0)


def yazi(d, xy, metin, font, renk, alfa, anchor="la"):
    if alfa <= 2:
        return
    d.text(xy, metin, font=font, fill=renk + (int(alfa),), anchor=anchor)


# ----------------------------------------------------------------- sahneler
def sahne_kanca(spec, kat, t, sure):
    img = zemin()
    if kat:
        bant_ciz(img, kat, t / sure, BANT, 240, 0.0)
    kunye(img)
    d = ImageDraw.Draw(img)

    s1, s2 = spec["satir1"], spec["satir2"]
    f = fit(d, max(s1, s2, key=len), anton, SAG - GUT, 118)
    y0 = 1120
    for i, (s, col) in enumerate([(s1, U.WHITE), (s2, U.AC())]):
        p = gecis(t, sure, 0.12 + i * 0.16, 0.5)
        yazi(d, (GUT, y0 + i * f.size * 1.1 + (1 - p) * 60), s, f, col,
             255 * p)
    pu = gecis(t, sure, 0.5, 0.5)
    yazi(d, (GUT, y0 - 56 + (1 - pu) * 30),
         P(spec.get("ustbilgi", "YENİ MAKİNE")).upper(), mono(26, True),
         U.AC(), 230 * pu)

    ps = gecis(t, sure, 0.75, 0.6)
    sy = y0 + 2 * f.size * 1.1 + 36
    for ln in wrap(d, P(spec.get("spot", "")), pop(31, "Medium"), 900)[:3]:
        yazi(d, (GUT, sy + (1 - ps) * 24), ln, pop(31, "Medium"),
             (216, 226, 242), 235 * ps)
        sy += 46
    return img


def sahne_ozet(spec, kat2, t, sure):
    img = zemin()
    if kat2:
        bant_ciz(img, kat2, t / sure, 820, 250, 0.35)
    kunye(img)
    d = ImageDraw.Draw(img)

    oz = [tuple(r) for r in spec.get("ozet", [])][:3]
    yk = 190
    top = 940
    for i, (k, v) in enumerate(oz):
        p = gecis(t, sure, 0.15 + i * 0.28, 0.5)
        ty = top + i * (yk + 22) + (1 - p) * 70
        over(img, lambda g, ty=ty, p=p: g.rounded_rectangle(
            [GUT, ty, SAG, ty + yk], radius=26,
            fill=a(U.AC(), 0.16 * p), outline=a(U.AC(), 0.6 * p), width=3))
        dd = ImageDraw.Draw(img)
        yazi(dd, (GUT + 40, ty + 56), P(k).upper(), mono(26, True), U.AC(),
             240 * p, "lm")
        fv = fit(dd, P(v), lambda s: anton(s), SAG - GUT - 80, 78, 40)
        yazi(dd, (GUT + 40, ty + 126), P(v), fv, U.WHITE, 255 * p, "lm")
    return img


def sahne_satir(baslik, satirlar, t, sure):
    img = zemin()
    kunye(img)
    d = ImageDraw.Draw(img)

    pb = gecis(t, sure, 0.05, 0.4)
    fb = fit(d, max(wrap(d, baslik, archivo(62), SAG - GUT), key=len),
             archivo, SAG - GUT, 62, 40)
    y = 560
    for ln in wrap(d, baslik, fb, SAG - GUT):
        yazi(d, (GUT, y + (1 - pb) * 36), ln, fb, U.FG(), 255 * pb)
        y += fb.size * 1.24
    d.rectangle([GUT, y + 18, GUT + 120 * pb, y + 26], fill=U.AC())

    y += 90
    yk = 150
    for i, (k, v) in enumerate(satirlar[:4]):
        p = gecis(t, sure, 0.35 + i * 0.30, 0.45)
        ty = y + i * (yk + 20)
        kx = (1 - p) * 90
        over(img, lambda g, ty=ty, kx=kx, p=p: g.rounded_rectangle(
            [GUT + kx, ty, SAG + kx, ty + yk], radius=22,
            fill=a(U.AC(), 0.10 * p), outline=a(U.AC(), 0.42 * p), width=3))
        dd = ImageDraw.Draw(img)
        yazi(dd, (GUT + 34 + kx, ty + 52), P(k).upper(), mono(26, True),
             U.AC(), 245 * p, "lm")
        fv = fit(dd, P(v), lambda s: pop(s, "SemiBold"), SAG - GUT - 70, 40, 24)
        yazi(dd, (GUT + 34 + kx, ty + 104), P(v), fv, U.FG(), 250 * p, "lm")
    return img


def sahne_kapanis(spec, t, sure):
    img = zemin()
    kunye(img)
    d = ImageDraw.Draw(img)
    s1 = spec.get("satir1", "TAMAMI")
    s2 = spec.get("satir2", "PROFİLDE")
    f = fit(d, max(s1, s2, key=len), anton, SAG - GUT, 128)
    y = 760
    for i, (s, col) in enumerate([(s1, U.FG()), (s2, U.AC())]):
        p = gecis(t, sure, 0.08 + i * 0.18, 0.5)
        yazi(d, (GUT, y + i * f.size * 1.12 + (1 - p) * 50), s, f, col,
             255 * p)

    pn = gecis(t, sure, 0.5, 0.5)
    ny = y + 2 * f.size * 1.12 + 40
    for ln in wrap(d, P(spec.get("not", "")), pop(31, "Medium"), 900)[:3]:
        yazi(d, (GUT, ny), ln, pop(31, "Medium"), U.FG2(), 225 * pn)
        ny += 46

    pb = gecis(t, sure, 0.75, 0.45)
    fb = pop(36, "Bold")
    tw = d.textlength("GÖNDERİYE BAK", font=fb)
    by = 1300
    BC, BY = U.AC(), U.UZER(U.AC())
    if pb > 0.02:
        img.alpha_composite(glow((SW, SH), lambda g: g.rounded_rectangle(
            [GUT, by, GUT + tw + 130, by + 92], radius=46,
            fill=a(BC, 0.5 * pb)), 34))
        dd = ImageDraw.Draw(img)
        dd.rounded_rectangle([GUT, by, GUT + tw + 130, by + 92], radius=46,
                             fill=BC + (int(255 * pb),))
        yazi(dd, (GUT + 50, by + 46), "GÖNDERİYE BAK", fb, BY, 255 * pb, "lm")
        yazi(dd, (GUT, by + 150), "@sermenkreatif", mono(30, True),
             U.SOFT(), 230 * pb, "lm")
    return img


# -------------------------------------------------------------------- akış
def pano_kurgu(spec):
    """Pano gönderisinin reels'i: kanca, her sütun bir sahne, kapanış.

    Panonun slaytı yok — bilgi sütunlarda duruyor. Her sütunu ayrı
    sahneye açıp künye satırlarını sırayla gösteriyoruz.
    """
    k = dict(spec["kapak"])
    # panoda ustbilgi yok; marka_alt onun yerine geçiyor, yoksa kanca
    # sahnesi "YENİ MAKİNE" varsayılanına düşüyor
    k.setdefault("ustbilgi", k.get("marka_alt", ""))
    sut = k.get("sutunlar", [])[:3]
    kat = foto_katman(sut[0].get("gorsel") if sut else None, BANT)
    sahneler = [(3.6, lambda t, s: sahne_kanca(k, kat, t, s))]
    for c in sut:
        oz = [tuple(r) for r in (c.get("ozellikler") or [])][:3]
        rows = [(c.get("alt", ""), "")] + [(v, "") for _, v in oz]
        sahneler.append((4.2, lambda t, s, b=c["baslik"], r=rows:
                         sahne_satir(b, r, t, s)))
    kapanis = {"satir1": P(k.get("satir1", "")),
               "satir2": P(k.get("satir2", "")),
               "kriterler": [], "not": k.get("ipucu", "")}
    sahneler.append((4.0, lambda t, s: sahne_kapanis(kapanis, t, s)))
    return sahneler


def kurgu(spec):
    """(süre, çizici) listesi."""
    k = spec["kapak"]
    if k.get("tip") == "pano":
        return pano_kurgu(spec)
    kat = foto_katman(k.get("gorsel"), BANT)
    kat2 = foto_katman(k.get("gorsel"), 820, odak=0.88)
    sahneler = [(3.6, lambda t, s: sahne_kanca(k, kat, t, s))]
    if k.get("ozet"):
        sahneler.append((3.6, lambda t, s: sahne_ozet(k, kat2, t, s)))
    for sl in spec["slaytlar"][:3]:
        rows = sl.get("satirlar") or sl.get("tablo") or []
        rows = [tuple(r) for r in rows][:4]
        if not rows:
            continue
        sahneler.append((4.2, lambda t, s, b=sl["baslik"], r=rows:
                         sahne_satir(b, r, t, s)))
    sahneler.append((3.6, lambda t, s: sahne_kapanis(spec.get("kapanis", {}),
                                                     t, s)))
    return sahneler


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    cikti = sys.argv[2]
    U.theme(spec["kategori"])
    U.zemin_ayarla(spec.get("zemin", "koyu"))
    U.stil_ayarla(spec.get("stil", "neon"))

    sahneler = kurgu(spec)
    toplam = sum(s for s, _ in sahneler)
    tk = int(toplam * FPS)

    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (SW, SH),
         "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", cikti],
        stdin=subprocess.PIPE)

    gecen = 0.0
    sayac = 0
    for sure, ciz in sahneler:
        for i in range(int(sure * FPS)):
            t = i / FPS
            kare = ciz(t, sure)
            serit(kare, (gecen + t) / toplam)
            ff.stdin.write(kare.convert("RGB").tobytes())
            sayac += 1
            if sayac % 60 == 0:
                print("  %d / %d kare" % (sayac, tk), flush=True)
        gecen += sure
    ff.stdin.close()
    ff.wait()
    mb = os.path.getsize(cikti) / 1048576.0
    print("%s  %.1f sn  %d kare  %.1f MB" % (cikti, toplam, sayac, mb))


if __name__ == "__main__":
    main()
