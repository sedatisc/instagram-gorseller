#!/usr/bin/env python3
"""@sermenkreatif Instagram slayt üreticisi.

Kullanım:  python3 uret.py gonderi.json cikis_klasoru
JSON şeması için SEMA.md dosyasına bak.
"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "fonts") + "/"

W, H = 1080, 1350
GUT = 62
RIGHT = W - GUT

BG = (5, 8, 16)
PANEL = (10, 15, 28)
WHITE = (255, 255, 255)
MUTE = (148, 163, 184)
WIRE = (220, 230, 245)
BLUE = (96, 165, 250)
GREEN = (74, 222, 128)
ORANGE = (251, 146, 60)
YELLOW = (250, 204, 21)
RED = (255, 71, 102)
GREY = (150, 165, 195)

RENKLER = {"mavi": BLUE, "yesil": GREEN, "turuncu": ORANGE, "sari": YELLOW,
           "kirmizi": RED, "gri": GREY, "beyaz": WHITE}

THEMES = {
    "elektronik": {"accent": (34, 211, 238), "label": "ELEKTRONİK & IoT"},
    "3dbaski": {"accent": (255, 138, 60), "label": "3D BASKI"},
    "proje": {"accent": (167, 139, 250), "label": "PROJE & ATÖLYE"},
}
ACC = THEMES["elektronik"]["accent"]
LABEL = THEMES["elektronik"]["label"]


def theme(key):
    global ACC, LABEL
    ACC = THEMES[key]["accent"]
    LABEL = THEMES[key]["label"]


def anton(s):
    return ImageFont.truetype(F + "Anton-Regular.ttf", s)


def archivo(s):
    return ImageFont.truetype(F + "ArchivoBlack-Regular.ttf", s)


def pop(s, w="Regular"):
    return ImageFont.truetype(F + "Poppins-%s.ttf" % w, s)


def mono(s, bold=False):
    f = ImageFont.truetype(F + "JetBrainsMono.ttf", s)
    try:
        f.set_variation_by_name("Bold" if bold else "Regular")
    except Exception:
        pass
    return f


def P(s):
    """Poppins'te U+03A9 yok, U+2126 var — omega'yı ohm işaretine çevir."""
    return s.replace("\u03a9", "\u2126")


def a(c, alpha):
    return tuple(c) + (int(255 * alpha),)


def over(img, fn):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    fn(ImageDraw.Draw(lay))
    img.alpha_composite(lay)


def glow(size, fn, radius):
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    fn(ImageDraw.Draw(lay))
    return lay.filter(ImageFilter.GaussianBlur(radius))


_logo = Image.open(os.path.join(HERE, "marka", "logo-yatay.png")).convert("RGBA")


def bright_logo(h):
    im = _logo.copy()
    r, g, b, al = im.split()
    lift = lambda v: min(255, int(70 + v * 0.86))
    im = Image.merge("RGBA", (r.point(lift), g.point(lift), b.point(lift), al))
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def base():
    img = Image.new("RGBA", (W, H), BG + (255,))

    def bands(d):
        d.line([(-300, 620), (760, -420)], fill=a(ACC, 0.85), width=150)
        d.line([(40, 860), (1060, -180)], fill=a(BLUE, 0.55), width=90)
        d.line([(380, 1620), (1360, 640)], fill=a(ACC, 0.55), width=130)
    img.alpha_composite(glow((W, H), bands, 80))

    def cores(d):
        d.line([(-300, 620), (760, -420)], fill=a(ACC, 0.95), width=6)
        d.line([(40, 860), (1060, -180)], fill=a(ACC, 0.6), width=3)
        d.line([(380, 1620), (1360, 640)], fill=a(ACC, 0.7), width=5)
    img.alpha_composite(glow((W, H), cores, 4))

    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for y in range(0, H, 54):
        for x in range(0, W, 54):
            dd.ellipse([x - 1, y - 1, x + 1, y + 1], fill=a(ACC, 0.10))
    img.alpha_composite(dots)
    return img


def chrome(img, counter):
    logo = bright_logo(34)
    img.alpha_composite(logo, (GUT, 56))
    d = ImageDraw.Draw(img)
    f = mono(26, True)
    tw = d.textlength(counter, font=f)
    x0 = RIGHT - tw - 44
    fl = mono(24, True)
    lw = d.textlength(LABEL, font=fl)
    lx = GUT + logo.width + 26

    def wash(g):
        g.rounded_rectangle([x0, 50, RIGHT, 98], radius=24,
                            fill=a(ACC, 0.14), outline=a(ACC, 0.6), width=2)
        g.rounded_rectangle([lx, 58, lx + lw + 40, 100], radius=21,
                            fill=a(ACC, 0.12), outline=a(ACC, 0.45), width=2)
        g.line([(GUT, 124), (RIGHT, 124)], fill=a(ACC, 0.30), width=2)
        g.line([(GUT + 212, 1296), (RIGHT, 1296)], fill=a(ACC, 0.20), width=2)
    over(img, wash)
    d = ImageDraw.Draw(img)
    d.text(((x0 + RIGHT) / 2, 74), counter, font=f, fill=ACC, anchor="mm")
    d.text((lx + 20, 79), LABEL, font=fl, fill=ACC, anchor="lm")
    d.text((GUT, 1296), "@sermenkreatif", font=mono(26), fill=MUTE, anchor="lm")


def fit(d, text, maker, maxw, start, floor=40):
    s = start
    while s > floor and d.textlength(text, font=maker(s)) > maxw:
        s -= 2
    return maker(s)


def wrap(d, text, font, maxw):
    out, line = [], ""
    for word in text.split():
        t = (line + " " + word).strip()
        if d.textlength(t, font=font) <= maxw or not line:
            line = t
        else:
            out.append(line)
            line = word
    out.append(line)
    return out


# ------------------------------------------------------------------ çizim
def _label(d, x, y, ad, deger, anchor="mm"):
    d.text((x, y), ad, font=mono(42, True), fill=WHITE, anchor=anchor)
    if deger:
        d.text((x, y + 52), P(deger), font=pop(38, "Medium"), fill=MUTE,
               anchor=anchor)


def _etiket_konum(e, x, y, w, h):
    return {"ust": (x + w / 2, y - 100, "mm"),
            "alt": (x + w / 2, y + h + 40, "mm"),
            "sol": (x - 40, y + h / 2 - 26, "rm"),
            "sag": (x + w + 40, y + h / 2 - 26, "lm")}[e]


def ciz(d, ogeler):
    for o in ogeler:
        t = o["t"]
        if t == "w":
            pts = [tuple(p) for p in o["p"]]
            d.line(pts, fill=WIRE, width=8, joint="curve")
        elif t == "n":
            d.ellipse([o["x"] - 13, o["y"] - 13, o["x"] + 13, o["y"] + 13],
                      fill=WIRE)
        elif t == "r":
            yon = o.get("yon", "h")
            w, h = (240, 76) if yon == "h" else (76, 240)
            w, h = o.get("w", w), o.get("h", h)
            d.rectangle([o["x"], o["y"], o["x"] + w, o["y"] + h],
                        fill=PANEL + (255,), outline=ORANGE, width=8)
            lx, ly, an = _etiket_konum(o.get("etiket", "ust"), o["x"], o["y"],
                                       w, h)
            _label(d, lx, ly, o.get("ad", ""), o.get("deger", ""), an)
        elif t == "c":
            yon = o.get("yon", "v")
            if yon == "v":
                d.line([(o["x"] - 50, o["y"]), (o["x"] + 50, o["y"])],
                       fill=GREEN, width=8)
                d.line([(o["x"] - 50, o["y"] + 32), (o["x"] + 50, o["y"] + 32)],
                       fill=GREEN, width=8)
                lx, ly, an = o["x"] + 78, o["y"] - 6, "lm"
            else:
                d.line([(o["x"], o["y"] - 50), (o["x"], o["y"] + 50)],
                       fill=GREEN, width=8)
                d.line([(o["x"] + 32, o["y"] - 50), (o["x"] + 32, o["y"] + 50)],
                       fill=GREEN, width=8)
                lx, ly, an = o["x"] + 16, o["y"] + 86, "mm"
            _label(d, lx, ly, o.get("ad", ""), o.get("deger", ""), an)
        elif t == "g":
            b = o.get("b", 130)
            for i, ww in enumerate((b, int(b * 0.62), int(b * 0.3))):
                d.line([(o["x"] - ww / 2, o["y"] + i * 26),
                        (o["x"] + ww / 2, o["y"] + i * 26)], fill=WIRE, width=8)
        elif t == "t":
            f = mono(38, True)
            tw = ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(
                o["metin"], font=f)
            d.rounded_rectangle([o["x"] - tw / 2 - 30, o["y"] - 38,
                                 o["x"] + tw / 2 + 30, o["y"] + 38], radius=38,
                                fill=a(ACC, 0.14), outline=a(ACC, 0.6), width=3)
            d.text((o["x"], o["y"]), o["metin"], font=f, fill=ACC, anchor="mm")
        elif t == "k":
            d.rounded_rectangle([o["x0"], o["y0"], o["x1"], o["y1"]], radius=24,
                                fill=a(BLUE, 0.10), outline=a(BLUE, 0.7),
                                width=5)
            if o.get("metin"):
                d.text(((o["x0"] + o["x1"]) / 2, o["y0"] + 48), o["metin"],
                       font=mono(34), fill=BLUE, anchor="mm")
        elif t == "d":
            col = RENKLER.get(o.get("renk", "kirmizi"), RED)
            f = pop(36, "Bold")
            tw = ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(
                o["metin"], font=f)
            d.rounded_rectangle([o["x"] - tw / 2 - 34, o["y"] - 36,
                                 o["x"] + tw / 2 + 34, o["y"] + 36], radius=36,
                                fill=a(col, 0.16), outline=a(col, 0.9), width=3)
            d.text((o["x"], o["y"]), o["metin"], font=f, fill=col, anchor="mm")
        elif t == "y":
            col = RENKLER.get(o.get("renk", "beyaz"), WHITE)
            d.text((o["x"], o["y"]), P(o["metin"]),
                   font=pop(o.get("boy", 38), "Medium"), fill=col,
                   anchor=o.get("hiza", "mm"))
        elif t == "renk":
            w = o.get("w", 190)
            h = o.get("h", 190)
            d.rounded_rectangle([o["x"], o["y"], o["x"] + w, o["y"] + h],
                                radius=18, fill=o["hex"],
                                outline=a(WHITE, 0.25), width=4)
            if o.get("ad"):
                d.text((o["x"] + w / 2, o["y"] + h + 44), P(o["ad"]),
                       font=pop(32, "Medium"), fill=(225, 233, 245),
                       anchor="mm")
        elif t == "cizgi":
            d.line([(o["x0"], o["y0"]), (o["x1"], o["y1"])],
                   fill=a(ACC, 0.18), width=3)


def tablo(d, satirlar):
    """Devre yerine veri paneli — 3D baskı ve proje kategorileri için."""
    top = 120
    for i, (k, v) in enumerate(satirlar):
        y = top + i * 150
        d.rounded_rectangle([120, y, 1790, y + 120], radius=22,
                            fill=a(ACC, 0.07), outline=a(ACC, 0.30), width=3)
        d.text((165, y + 60), k, font=mono(40, True), fill=ACC, anchor="lm")
        d.text((1745, y + 60), P(v), font=pop(42, "Medium"),
               fill=(225, 233, 245), anchor="rm")


def panel(w, h, fn, vurgu=None):
    S = 2
    dw, dh = w * S, h * S
    ink = Image.new("RGBA", (dw, dh), (0, 0, 0, 0))
    fn(ImageDraw.Draw(ink))

    pad = 56 * S
    bb = ink.getbbox()
    k = min((dw - 2 * pad) / (bb[2] - bb[0]), (dh - 2 * pad) / (bb[3] - bb[1]),
            1.4)
    nw, nh = int((bb[2] - bb[0]) * k), int((bb[3] - bb[1]) * k)
    ox, oy = (dw - nw) // 2, (dh - nh) // 2
    fitted = Image.new("RGBA", (dw, dh), (0, 0, 0, 0))
    fitted.alpha_composite(ink.crop(bb).resize((nw, nh), Image.LANCZOS),
                           (ox, oy))
    ink = fitted

    halo = None
    if vurgu:
        hl = [int((vurgu[0] - bb[0]) * k) + ox, int((vurgu[1] - bb[1]) * k) + oy,
              int((vurgu[2] - bb[0]) * k) + ox, int((vurgu[3] - bb[1]) * k) + oy]
        dim = ink.copy()
        dim.putalpha(dim.getchannel("A").point(lambda v: int(v * 0.22)))
        m = Image.new("L", (dw, dh), 0)
        ImageDraw.Draw(m).rounded_rectangle(hl, radius=70, fill=255)
        ink = Image.composite(ink, dim, m)
        ra = ImageChops.multiply(ink.getchannel("A"), m)
        near = ra.filter(ImageFilter.GaussianBlur(18 * S)).point(
            lambda v: min(255, int(v * 2.6)))
        far = ra.filter(ImageFilter.GaussianBlur(56 * S)).point(
            lambda v: min(140, int(v * 1.7)))
        halo = Image.new("RGBA", (dw, dh), YELLOW + (0,))
        halo.putalpha(ImageChops.lighter(near, far))

    card = Image.new("RGBA", (dw, dh), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle([0, 0, dw - 1, dh - 1],
                                           radius=30 * S, fill=PANEL + (255,))
    grid = Image.new("RGBA", (dw, dh), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for gy in range(0, dh, 44 * S):
        gd.line([(0, gy), (dw, gy)], fill=a(ACC, 0.05), width=2)
    for gx in range(0, dw, 44 * S):
        gd.line([(gx, 0), (gx, dh)], fill=a(ACC, 0.05), width=2)
    mask = Image.new("L", (dw, dh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, dw - 1, dh - 1],
                                           radius=30 * S, fill=255)
    card.paste(grid, (0, 0), Image.composite(
        mask, Image.new("L", (dw, dh), 0), grid.getchannel("A")))
    if halo is not None:
        card.alpha_composite(halo)
    card.alpha_composite(ink)
    ImageDraw.Draw(card).rounded_rectangle([1, 1, dw - 2, dh - 2],
                                           radius=30 * S, outline=a(ACC, 0.55),
                                           width=2 * S)
    return card.resize((w, h), Image.LANCZOS)


def place(img, card, x, y):
    img.alpha_composite(glow((W, H), lambda g: g.rounded_rectangle(
        [x + 10, y + 16, x + card.width - 10, y + card.height + 10],
        radius=30, fill=a(ACC, 0.30)), 40), (0, 0))
    img.alpha_composite(card, (x, y))


# ------------------------------------------------------------------ slaytlar
def govde(spec):
    if spec.get("tablo"):
        return lambda d: tablo(d, [tuple(r) for r in spec["tablo"]])
    return lambda d: ciz(d, spec.get("cizim", []))


def kapak(spec, sayac, yol):
    img = base()
    chrome(img, sayac)
    d = ImageDraw.Draw(img)
    s1, s2 = spec["satir1"], spec["satir2"]
    f = fit(d, max(s1, s2, key=len), anton, 956, 128)
    y = 178
    img.alpha_composite(glow((W, H), lambda g: g.text(
        (GUT, y + f.size * 1.16), s2, font=f, fill=a(ACC, 0.75), anchor="la"),
        26))
    d = ImageDraw.Draw(img)
    d.text((GUT, y), s1, font=f, fill=WHITE, anchor="la")
    d.text((GUT, y + f.size * 1.16), s2, font=f, fill=ACC, anchor="la")
    bot = d.textbbox((GUT, y + f.size * 1.16), s2, font=f, anchor="la")[3]

    fs = pop(32, "Medium")
    ty = bot + 44
    for ln in wrap(d, P(spec["spot"]), fs, 780):
        d.text((GUT, ty), ln, font=fs, fill=(205, 216, 232), anchor="la")
        ty += 46

    place(img, panel(956, 466, govde(spec)), GUT, 690)

    fx = pop(25, "Medium")
    boxes, x = [], GUT
    for metin, renk in spec.get("rozetler", []):
        col = RENKLER.get(renk, ACC) if renk != "tema" else ACC
        metin = P(metin)
        w = d.textlength(metin, font=fx) + 76
        boxes.append((x, w, metin, col))
        x += w + 14
    over(img, lambda g: [g.rounded_rectangle(
        [px, 1196, px + pw, 1264], radius=34, fill=a(col, 0.14),
        outline=a(col, 0.6), width=2) for px, pw, _, col in boxes])
    d = ImageDraw.Draw(img)
    for px, pw, metin, col in boxes:
        d.ellipse([px + 26, 1222, px + 42, 1238], fill=col)
        d.text((px + 58, 1230), metin, font=fx, fill=(225, 233, 245),
               anchor="lm")
    img.convert("RGB").save(yol)


def adim(spec, govde_fn, no, toplam, sayac, yol):
    img = base()
    chrome(img, sayac)
    d = ImageDraw.Draw(img)
    over(img, lambda g: g.rounded_rectangle(
        [GUT, 168, GUT + 96, 264], radius=22, fill=a(ACC, 0.14),
        outline=a(ACC, 0.6), width=3))
    d = ImageDraw.Draw(img)
    d.text((GUT + 48, 216), "%02d" % no, font=anton(58), fill=ACC, anchor="mm")
    d.text((GUT + 124, 216), "ADIM %d / %d" % (no, toplam), font=mono(28),
           fill=MUTE, anchor="lm")

    fh = fit(d, max(wrap(d, spec["baslik"], archivo(58), 940), key=len),
             archivo, 940, 58)
    y = 320
    for ln in wrap(d, spec["baslik"], fh, 940):
        d.text((GUT, y), ln, font=fh, fill=WHITE, anchor="la")
        y += fh.size * 1.26
    d.rectangle([GUT, y + 18, GUT + 110, y + 24], fill=ACC)

    fs = pop(30)
    ty = y + 66
    for ln in wrap(d, P(spec["aciklama"]), fs, 860):
        d.text((GUT, ty), ln, font=fs, fill=(196, 208, 226), anchor="la")
        ty += 45

    py = max(600, int(ty) + 34)
    ph = min(556, 1244 - py)
    place(img, panel(956, ph, govde_fn, spec.get("vurgu")), GUT, py)
    img.convert("RGB").save(yol)


def kapanis(spec, sayac, yol):
    img = base()
    chrome(img, sayac)
    d = ImageDraw.Draw(img)
    s1, s2 = spec["satir1"], spec["satir2"]
    f = fit(d, max(s1, s2, key=len), anton, 956, 118)
    y = 210
    d.text((GUT, y), s1, font=f, fill=WHITE, anchor="la")
    img.alpha_composite(glow((W, H), lambda g: g.text(
        (GUT, y + f.size * 1.16), s2, font=f, fill=a(ACC, 0.75), anchor="la"),
        26))
    d = ImageDraw.Draw(img)
    d.text((GUT, y + f.size * 1.16), s2, font=f, fill=ACC, anchor="la")
    bot = d.textbbox((GUT, y + f.size * 1.16), s2, font=f, anchor="la")[3]

    fy = bot + 86
    fs = pop(30, "Medium")
    for i, (k, v) in enumerate(spec["kriterler"]):
        top = fy + i * 128
        over(img, lambda g, t=top: g.rounded_rectangle(
            [GUT, t, RIGHT, t + 104], radius=18, fill=a(ACC, 0.07),
            outline=a(ACC, 0.30), width=2))
        dd = ImageDraw.Draw(img)
        dd.text((GUT + 30, top + 52), k, font=mono(26, True), fill=ACC,
                anchor="lm")
        dd.text((RIGHT - 30, top + 52), P(v), font=fs, fill=(225, 233, 245),
                anchor="rm")

    d = ImageDraw.Draw(img)
    btn = "ARKADAŞINA YOLLA"
    fb = pop(30, "Bold")
    tw = d.textlength(btn, font=fb)
    by = 1176
    img.alpha_composite(glow((W, H), lambda g: g.rounded_rectangle(
        [GUT, by, GUT + tw + 112, by + 74], radius=37, fill=a(ACC, 0.55)), 30))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([GUT, by, GUT + tw + 112, by + 74], radius=37, fill=ACC)
    d.text((GUT + 44, by + 37), btn, font=fb, fill=(6, 10, 20), anchor="lm")
    ax = GUT + 44 + tw + 26
    d.line([(ax, by + 37), (ax + 26, by + 37)], fill=(6, 10, 20), width=5)
    d.polygon([(ax + 23, by + 29), (ax + 40, by + 37), (ax + 23, by + 45)],
              fill=(6, 10, 20))
    d.text((GUT, by - 46), P(spec.get("not", "")), font=pop(26), fill=MUTE,
           anchor="lm")
    img.convert("RGB").save(yol)


def hikaye(spec, yol):
    """1080 x 1920 hikaye — gönderiye yönlendiren tek kare."""
    SW, SH = 1080, 1920
    img = Image.new("RGBA", (SW, SH), BG + (255,))

    def bands(d):
        d.line([(-300, 900), (860, -360)], fill=a(ACC, 0.85), width=170)
        d.line([(60, 1240), (1160, -60)], fill=a(BLUE, 0.55), width=100)
        d.line([(300, 2200), (1400, 900)], fill=a(ACC, 0.55), width=150)
    img.alpha_composite(glow((SW, SH), bands, 90))

    def cores(d):
        d.line([(-300, 900), (860, -360)], fill=a(ACC, 0.95), width=6)
        d.line([(300, 2200), (1400, 900)], fill=a(ACC, 0.7), width=5)
    img.alpha_composite(glow((SW, SH), cores, 4))

    dots = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for y in range(0, SH, 54):
        for x in range(0, SW, 54):
            dd.ellipse([x - 1, y - 1, x + 1, y + 1], fill=a(ACC, 0.10))
    img.alpha_composite(dots)

    # üst şerit — Instagram arayüzü ilk 250 px'i kapatıyor
    logo = bright_logo(34)
    img.alpha_composite(logo, (GUT, 300))
    d = ImageDraw.Draw(img)
    fl = mono(24, True)
    lw = d.textlength(LABEL, font=fl)
    lx = GUT + logo.width + 26
    over(img, lambda g: g.rounded_rectangle(
        [lx, 296, lx + lw + 40, 338], radius=21, fill=a(ACC, 0.12),
        outline=a(ACC, 0.45), width=2))
    d = ImageDraw.Draw(img)
    d.text((lx + 20, 317), LABEL, font=fl, fill=ACC, anchor="lm")

    s1, s2 = spec["satir1"], spec["satir2"]
    f = fit(d, max(s1, s2, key=len), anton, 956, 132)
    y = 420
    img.alpha_composite(glow((SW, SH), lambda g: g.text(
        (GUT, y + f.size * 1.16), s2, font=f, fill=a(ACC, 0.75), anchor="la"),
        26))
    d = ImageDraw.Draw(img)
    d.text((GUT, y), s1, font=f, fill=WHITE, anchor="la")
    d.text((GUT, y + f.size * 1.16), s2, font=f, fill=ACC, anchor="la")
    bot = d.textbbox((GUT, y + f.size * 1.16), s2, font=f, anchor="la")[3]

    fs = pop(34, "Medium")
    ty = bot + 50
    for ln in wrap(d, P(spec["spot"]), fs, 900):
        d.text((GUT, ty), ln, font=fs, fill=(205, 216, 232), anchor="la")
        ty += 50

    # alt çağrı — arayüz son 250 px'i kapatıyor
    by = 1560
    py = int(ty) + 66
    ph = min(640, by - 80 - py)
    kart = panel(956, ph, govde(spec))
    img.alpha_composite(glow((SW, SH), lambda g: g.rounded_rectangle(
        [GUT + 10, py + 16, GUT + 946, py + ph + 10], radius=30,
        fill=a(ACC, 0.30)), 40))
    img.alpha_composite(kart, (GUT, py))

    d = ImageDraw.Draw(img)
    btn = "GÖNDERİYE BAK"
    fb = pop(32, "Bold")
    tw = d.textlength(btn, font=fb)
    img.alpha_composite(glow((SW, SH), lambda g: g.rounded_rectangle(
        [GUT, by, GUT + tw + 120, by + 80], radius=40, fill=a(ACC, 0.55)), 30))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([GUT, by, GUT + tw + 120, by + 80], radius=40, fill=ACC)
    d.text((GUT + 46, by + 40), btn, font=fb, fill=(6, 10, 20), anchor="lm")
    ax = GUT + 46 + tw + 28
    d.line([(ax, by + 40), (ax + 28, by + 40)], fill=(6, 10, 20), width=5)
    d.polygon([(ax + 25, by + 31), (ax + 44, by + 40), (ax + 25, by + 49)],
              fill=(6, 10, 20))
    d.text((GUT, by + 128), "profilde yeni gönderi", font=pop(28), fill=MUTE,
           anchor="lm")
    img.convert("RGB").save(yol)


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    theme(spec["kategori"])

    slaytlar = spec["slaytlar"]
    toplam = 1 + len(slaytlar) + (1 if spec.get("kapanis") else 0)
    n = 1
    kapak(spec["kapak"], "%d/%d" % (n, toplam),
          os.path.join(out, "%d.png" % n))
    ortak = govde(spec["kapak"])
    for i, sl in enumerate(slaytlar, 1):
        n += 1
        fn = govde(sl) if (sl.get("cizim") or sl.get("tablo")) else ortak
        adim(sl, fn, i, len(slaytlar), "%d/%d" % (n, toplam),
             os.path.join(out, "%d.png" % n))
    if spec.get("kapanis"):
        n += 1
        kapanis(spec["kapanis"], "%d/%d" % (n, toplam),
                os.path.join(out, "%d.png" % n))
    hikaye(spec["kapak"], os.path.join(out, "hikaye.png"))
    print("%d slayt + hikaye: %s" % (n, out))


if __name__ == "__main__":
    main()
