#!/usr/bin/env python3
"""@sermenkreatif Instagram slayt üreticisi.

Kullanım:  python3 uret.py gonderi.json cikis_klasoru
JSON şeması için SEMA.md dosyasına bak.
"""
import json
import math
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

MOR = (167, 139, 250)
RENKLER = {"mavi": BLUE, "mor": MOR, "yesil": GREEN, "turuncu": ORANGE, "sari": YELLOW,
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
    """Poppins'te U+03A9 ve birleşik nokta yok — ikisini de temizle."""
    return (s.replace("\u03a9", "\u2126")
             .replace("i\u0307", "i").replace("\u0307", ""))


PAL = {}


def _kar(c, t):
    return tuple(int(c[i] + (255 - c[i]) * t) for i in range(3))


def _koy(c, t):
    return tuple(int(c[i] * (1 - t)) for i in range(3))


CANLI = {
    "indigo":  ((46, 40, 128), (16, 12, 52), (255, 214, 102)),
    "kobalt":  ((18, 58, 146), (5, 20, 66), (94, 234, 212)),
    "okyanus": ((8, 84, 102), (3, 32, 50), (253, 224, 71)),
    "orman":   ((10, 84, 60), (3, 32, 28), (190, 242, 100)),
    "mor":     ((80, 30, 118), (26, 8, 50), (244, 114, 182)),
    "kiraz":   ((128, 24, 62), (46, 6, 28), (253, 186, 116)),
}


def zemin_ayarla(mod):
    """Zemin: koyu · acik · canlı renklerden biri (indigo, kobalt,
    okyanus, orman, mor, kiraz)."""
    global PAL
    if mod in CANLI:
        ust, alt, vurgu = CANLI[mod]
        PAL = {"mod": "canli", "ad": mod, "ust": ust, "alt": alt,
               "fg": WHITE, "fg2": _kar(ust, 0.74), "soluk": _kar(ust, 0.52),
               "rakam": WHITE, "vurgu": vurgu,
               "kart_op": 0.15, "kontur_op": 0.62}
    elif mod == "acik":
        PAL = {"mod": mod, "ust": (247, 249, 253), "alt": (224, 233, 247),
               "fg": (10, 20, 44), "fg2": (84, 98, 126),
               "soluk": (120, 134, 162), "rakam": None, "vurgu": None,
               "kart_op": 0.12, "kontur_op": 0.85}
    else:
        PAL = {"mod": "koyu", "ust": BG, "alt": BG, "fg": WHITE,
               "fg2": (190, 203, 224), "soluk": MUTE, "rakam": YELLOW,
               "vurgu": None, "kart_op": 0.09, "kontur_op": 0.55}


def _mod():
    return PAL.get("mod", "koyu") if PAL else "koyu"


def _P(k, d):
    v = PAL.get(k) if PAL else None
    return d if v is None else v


def FG():
    return _P("fg", WHITE)


def FG2():
    return _P("fg2", (205, 216, 232))


def SOFT():
    return _P("soluk", MUTE)


def AC():
    """Zemin moduna göre okunur vurgu rengi."""
    m = _mod()
    if m == "canli":
        return PAL["vurgu"]
    if m == "acik":
        return _koy(ACC, 0.42)
    return ACC


def RK(col=None):
    """Dev rakam rengi — açık zeminde kartın kendi rengi."""
    m = _mod()
    if m == "canli":
        return WHITE
    if m == "acik":
        return col if col else (12, 22, 46)
    return YELLOW


def KC(col):
    """Kart rengini zemine göre dengele."""
    m = _mod()
    if m == "canli":
        return _kar(col, 0.12)
    if m == "acik":
        l = 0.2126 * col[0] + 0.7152 * col[1] + 0.0722 * col[2]
        if l > 118:
            return tuple(int(v * 118.0 / l) for v in col)
    return col


def UZER(col):
    """Dolu buton üstünde okunur yazı rengi."""
    l = 0.2126 * col[0] + 0.7152 * col[1] + 0.0722 * col[2]
    return (6, 10, 20) if l > 140 else WHITE


def WR():
    """İletken rengi — açık zeminde koyu mürekkep."""
    return (22, 32, 56) if _mod() == "acik" else WIRE


def PNL():
    """Panel dolgusu."""
    return (252, 253, 255) if _mod() == "acik" else PANEL


def ISIK(x):
    """Açık zeminde parıltı kısılır."""
    return x * 0.26 if _mod() == "acik" else x


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
    if _mod() == "acik":
        lift = lambda v: int(v * 0.42)
    else:
        lift = lambda v: min(255, int(70 + v * 0.86))
    im = Image.merge("RGBA", (r.point(lift), g.point(lift), b.point(lift), al))
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def base():
    if PAL and PAL.get("mod") != "koyu":
        return base_renkli()
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


def base_renkli(W=W, H=H):
    """Canlı ya da açık zemin — düz siyah yerine renk."""
    img = Image.new("RGB", (W, H), PAL["ust"])
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(
            int(PAL["ust"][i] + (PAL["alt"][i] - PAL["ust"][i]) * t)
            for i in range(3)))
    img = img.convert("RGBA")

    acik = PAL["mod"] == "acik"
    oy = H / 1350.0
    vur = PAL.get("vurgu") or ACC
    for cx, cy, rad, col, op in [
            (210, 230 * oy, 560, ACC if acik else vur, 0.16 if acik else 0.22),
            (930, 1180 * oy, 520, BLUE if acik else WHITE,
             0.10 if acik else 0.13)]:
        blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(blob).ellipse([cx - rad, cy - rad, cx + rad, cy + rad],
                                     fill=a(col, op))
        img.alpha_composite(blob.filter(ImageFilter.GaussianBlur(170)))

    cizgi = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cizgi)
    taban = (10, 20, 44) if acik else WHITE
    cd.line([(-300, 760 * oy), (820, -420)], fill=a(taban, 0.07), width=200)
    cd.line([(320, 1700 * oy), (1400, 560 * oy)], fill=a(taban, 0.05),
            width=160)
    img.alpha_composite(cizgi.filter(ImageFilter.GaussianBlur(50)))

    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for y in range(0, H, 54):
        for x in range(0, W, 54):
            dd.ellipse([x - 1, y - 1, x + 1, y + 1], fill=a(taban, 0.11))
    img.alpha_composite(dots)
    return img


def chrome(img, counter, kaydir=False):
    logo = bright_logo(34)
    img.alpha_composite(logo, (GUT, 56))
    d = ImageDraw.Draw(img)
    f = mono(26, True)
    tw = d.textlength(counter, font=f)
    x0 = RIGHT - tw - 44
    fl = mono(24, True)
    lw = d.textlength(LABEL, font=fl)
    lx = GUT + logo.width + 26

    AA = AC()

    def wash(g):
        g.rounded_rectangle([x0, 50, RIGHT, 98], radius=24,
                            fill=a(AA, 0.14), outline=a(AA, 0.6), width=2)
        g.rounded_rectangle([lx, 58, lx + lw + 40, 100], radius=21,
                            fill=a(AA, 0.12), outline=a(AA, 0.45), width=2)
        g.line([(GUT, 124), (RIGHT, 124)], fill=a(AA, 0.30), width=2)
        g.line([(GUT + 212, 1296), (cizgi_sag, 1296)], fill=a(AA, 0.20),
               width=2)
    fk = pop(24, "Bold")
    kw = d.textlength("KAYDIR", font=fk) + 46 if kaydir else 0
    cizgi_sag = RIGHT - kw - 24 if kaydir else RIGHT
    over(img, wash)
    d = ImageDraw.Draw(img)
    d.text(((x0 + RIGHT) / 2, 74), counter, font=f, fill=AA, anchor="mm")
    d.text((lx + 20, 79), LABEL, font=fl, fill=AA, anchor="lm")
    d.text((GUT, 1296), "@sermenkreatif", font=mono(26), fill=SOFT(),
           anchor="lm")
    if kaydir:
        ox = RIGHT - kw
        d.text((ox, 1296), "KAYDIR", font=fk, fill=AA, anchor="lm")
        ax = RIGHT - 34
        d.line([(ax, 1296), (ax + 22, 1296)], fill=AA, width=4)
        d.polygon([(ax + 18, 1288), (ax + 34, 1296), (ax + 18, 1304)],
                  fill=AA)


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
    d.text((x, y), ad, font=mono(42, True), fill=FG(), anchor=anchor)
    if deger:
        d.text((x, y + 52), P(deger), font=pop(38, "Medium"), fill=SOFT(),
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
            d.line(pts, fill=WR(), width=8, joint="curve")
        elif t == "n":
            d.ellipse([o["x"] - 13, o["y"] - 13, o["x"] + 13, o["y"] + 13],
                      fill=WR())
        elif t == "r":
            yon = o.get("yon", "h")
            w, h = (240, 76) if yon == "h" else (76, 240)
            w, h = o.get("w", w), o.get("h", h)
            d.rectangle([o["x"], o["y"], o["x"] + w, o["y"] + h],
                        fill=PNL() + (255,), outline=KC(ORANGE), width=8)
            lx, ly, an = _etiket_konum(o.get("etiket", "ust"), o["x"], o["y"],
                                       w, h)
            _label(d, lx, ly, o.get("ad", ""), o.get("deger", ""), an)
        elif t == "c":
            yon = o.get("yon", "v")
            if yon == "v":
                d.line([(o["x"] - 50, o["y"]), (o["x"] + 50, o["y"])],
                       fill=KC(GREEN), width=8)
                d.line([(o["x"] - 50, o["y"] + 32), (o["x"] + 50, o["y"] + 32)],
                       fill=KC(GREEN), width=8)
                lx, ly, an = o["x"] + 78, o["y"] - 6, "lm"
            else:
                d.line([(o["x"], o["y"] - 50), (o["x"], o["y"] + 50)],
                       fill=KC(GREEN), width=8)
                d.line([(o["x"] + 32, o["y"] - 50), (o["x"] + 32, o["y"] + 50)],
                       fill=KC(GREEN), width=8)
                lx, ly, an = o["x"] + 16, o["y"] + 86, "mm"
            _label(d, lx, ly, o.get("ad", ""), o.get("deger", ""), an)
        elif t == "g":
            b = o.get("b", 130)
            for i, ww in enumerate((b, int(b * 0.62), int(b * 0.3))):
                d.line([(o["x"] - ww / 2, o["y"] + i * 26),
                        (o["x"] + ww / 2, o["y"] + i * 26)], fill=WR(), width=8)
        elif t == "t":
            f = mono(38, True)
            tw = ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(
                o["metin"], font=f)
            d.rounded_rectangle([o["x"] - tw / 2 - 30, o["y"] - 38,
                                 o["x"] + tw / 2 + 30, o["y"] + 38], radius=38,
                                fill=a(AC(), 0.14), outline=a(AC(), 0.6),
                                width=3)
            d.text((o["x"], o["y"]), o["metin"], font=f, fill=AC(),
                   anchor="mm")
        elif t == "k":
            d.rounded_rectangle([o["x0"], o["y0"], o["x1"], o["y1"]], radius=24,
                                fill=a(KC(BLUE), 0.10), outline=a(KC(BLUE), 0.7),
                                width=5)
            if o.get("metin"):
                d.text(((o["x0"] + o["x1"]) / 2, o["y0"] + 48), o["metin"],
                       font=mono(34), fill=KC(BLUE), anchor="mm")
        elif t == "d":
            col = KC(RENKLER.get(o.get("renk", "kirmizi"), RED))
            f = pop(36, "Bold")
            tw = ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(
                o["metin"], font=f)
            d.rounded_rectangle([o["x"] - tw / 2 - 34, o["y"] - 36,
                                 o["x"] + tw / 2 + 34, o["y"] + 36], radius=36,
                                fill=a(col, 0.16), outline=a(col, 0.9), width=3)
            d.text((o["x"], o["y"]), o["metin"], font=f, fill=col, anchor="mm")
        elif t == "y":
            col = KC(RENKLER.get(o.get("renk", "beyaz"), WHITE))
            d.text((o["x"], o["y"]), P(o["metin"]),
                   font=pop(o.get("boy", 38), "Medium"), fill=col,
                   anchor=o.get("hiza", "mm"))
        elif t == "s":
            yon = o.get("yon", "v")
            if yon == "v":
                h = o.get("h", 90)
                d.ellipse([o["x"] - 9, o["y"] - 9, o["x"] + 9, o["y"] + 9],
                          fill=WR())
                d.ellipse([o["x"] - 9, o["y"] + h - 9, o["x"] + 9,
                           o["y"] + h + 9], fill=WR())
                d.line([(o["x"], o["y"]), (o["x"] + 60, o["y"] + h - 12)],
                       fill=WR(), width=8)
                lx, ly, an = o["x"] + 96, o["y"] + h / 2 - 26, "lm"
            else:
                w = o.get("w", 90)
                d.ellipse([o["x"] - 9, o["y"] - 9, o["x"] + 9, o["y"] + 9],
                          fill=WR())
                d.ellipse([o["x"] + w - 9, o["y"] - 9, o["x"] + w + 9,
                           o["y"] + 9], fill=WR())
                d.line([(o["x"], o["y"]), (o["x"] + w - 12, o["y"] - 60)],
                       fill=WR(), width=8)
                lx, ly, an = o["x"] + w / 2, o["y"] + 70, "mm"
            _label(d, lx, ly, o.get("ad", ""), o.get("deger", ""), an)
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
                   fill=a(AC(), 0.25), width=3)


def tablo(d, satirlar):
    """Devre yerine veri paneli — satırlar paneli dolduracak kadar açılır."""
    n = max(1, len(satirlar))
    ust, alt, ara = 60, 880, 26
    h = min(250, (alt - ust) / n - ara)
    adim_y = h + ara
    y0 = ust + ((alt - ust) - (adim_y * n - ara)) / 2
    fk = mono(max(30, min(54, int(h * 0.30))), True)
    fv = pop(max(32, min(58, int(h * 0.33))), "Medium")
    for i, (k, v) in enumerate(satirlar):
        y = y0 + i * adim_y
        d.rounded_rectangle([120, y, 1790, y + h], radius=22,
                            fill=a(AC(), 0.09), outline=a(AC(), 0.34), width=3)
        d.text((165, y + h / 2), k, font=fk, fill=AC(), anchor="lm")
        d.text((1745, y + h / 2), P(v), font=fv, fill=FG(), anchor="rm")


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
        halo = Image.new("RGBA", (dw, dh), (AC() if _mod() == "acik"
                                           else YELLOW) + (0,))
        halo.putalpha(ImageChops.lighter(near, far))

    card = Image.new("RGBA", (dw, dh), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle([0, 0, dw - 1, dh - 1],
                                           radius=30 * S, fill=PNL() + (255,))
    grid = Image.new("RGBA", (dw, dh), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    izgara_renk = a(AC(), 0.09 if _mod() == "acik" else 0.05)
    for gy in range(0, dh, 44 * S):
        gd.line([(0, gy), (dw, gy)], fill=izgara_renk, width=2)
    for gx in range(0, dw, 44 * S):
        gd.line([(gx, 0), (gx, dh)], fill=izgara_renk, width=2)
    mask = Image.new("L", (dw, dh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, dw - 1, dh - 1],
                                           radius=30 * S, fill=255)
    card.paste(grid, (0, 0), Image.composite(
        mask, Image.new("L", (dw, dh), 0), grid.getchannel("A")))
    if halo is not None:
        card.alpha_composite(halo)
    card.alpha_composite(ink)
    ImageDraw.Draw(card).rounded_rectangle([1, 1, dw - 2, dh - 2],
                                           radius=30 * S,
                                           outline=a(AC(), _P("kontur_op",
                                                              0.55)),
                                           width=2 * S)
    return card.resize((w, h), Image.LANCZOS)


def place(img, card, x, y):
    img.alpha_composite(glow((W, H), lambda g: g.rounded_rectangle(
        [x + 10, y + 16, x + card.width - 10, y + card.height + 10],
        radius=30, fill=a(AC(), 0.30 if _mod() != "acik" else 0.22)), 40),
        (0, 0))
    img.alpha_composite(card, (x, y))


# ------------------------------------------------------------------ slaytlar
def govde(spec):
    if spec.get("tablo"):
        return lambda d: tablo(d, [tuple(r) for r in spec["tablo"]])
    if spec.get("cizim"):
        return lambda d: ciz(d, spec["cizim"])
    if spec.get("kartlar"):
        satir = [(k["etiket"], k["deger"]) for k in spec["kartlar"]]
        return lambda d: tablo(d, satir)
    return lambda d: ciz(d, [])


def _rozetler(img, d, spec):
    fx = pop(25, "Medium")
    boxes, x = [], GUT
    for metin, renk in spec.get("rozetler", []):
        metin = P(metin)
        col = KC(RENKLER.get(renk, ACC)) if renk != "tema" else AC()
        w = d.textlength(metin, font=fx) + 76
        boxes.append((x, w, metin, col))
        x += w + 14
    over(img, lambda g: [g.rounded_rectangle(
        [px, 1196, px + pw, 1264], radius=34, fill=a(col, 0.14),
        outline=a(col, 0.6), width=2) for px, pw, _, col in boxes])
    dd = ImageDraw.Draw(img)
    for px, pw, metin, col in boxes:
        dd.ellipse([px + 26, 1222, px + 42, 1238], fill=col)
        dd.text((px + 58, 1230), metin, font=fx, fill=FG2(), anchor="lm")


def kapak_rakam(spec, sayac, yol):
    """Dev rakam kapağı — tek sayı ekranı dolduruyor."""
    img = base()
    chrome(img, sayac, kaydir=True)
    d = ImageDraw.Draw(img)

    d.text((GUT, 190), P(spec["ustbilgi"]).upper(), font=mono(30, True),
           fill=AC(), anchor="la")

    rakam = P(spec["rakam"])
    f = fit(d, rakam, anton, 956, 400, 120)

    # blok yüksekliğini ölç, boşluğu üste ve alta eşit dağıt
    fa0 = fit(d, P(spec["rakam_alt"]), archivo, 956, 70, 38)
    fs0 = pop(32, "Medium")
    h_rakam = d.textbbox((0, 0), rakam, font=f, anchor="la")[3]
    h_alt = d.textbbox((0, 0), P(spec["rakam_alt"]), font=fa0,
                       anchor="la")[3]
    h_spot = 46 * len(wrap(d, P(spec["spot"]), fs0, 900))
    blok = h_rakam + 26 + h_alt + 54 + h_spot
    ry = max(250, int(250 + ((1160 - 250) - blok) / 2))
    img.alpha_composite(glow((W, H), lambda g: g.text(
        (GUT - 10, ry), rakam, font=f, fill=a(AC(), ISIK(0.9)), anchor="la"),
        50))
    img.alpha_composite(glow((W, H), lambda g: g.text(
        (GUT - 10, ry), rakam, font=f, fill=a(FG(), ISIK(0.5)), anchor="la"),
        14))
    d = ImageDraw.Draw(img)
    d.text((GUT - 10, ry), rakam, font=f, fill=FG(), anchor="la")
    bot = d.textbbox((GUT - 10, ry), rakam, font=f, anchor="la")[3]

    fa = fit(d, P(spec["rakam_alt"]), archivo, 956, 70, 38)
    d.text((GUT, bot + 26), P(spec["rakam_alt"]), font=fa, fill=AC(),
           anchor="la")
    ab = d.textbbox((GUT, bot + 26), P(spec["rakam_alt"]), font=fa,
                    anchor="la")[3]

    fs = pop(32, "Medium")
    ty = ab + 54
    for ln in wrap(d, P(spec["spot"]), fs, 900):
        d.text((GUT, ty), ln, font=fs, fill=FG2(), anchor="la")
        ty += 46

    _rozetler(img, d, spec)
    img.convert("RGB").save(yol)


def kapak_carpisma(spec, sayac, yol):
    """Çapraz bölünmüş kapak — yanlış ile doğru karşı karşıya."""
    img = base()

    kirmizi = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(kirmizi).polygon([(0, 0), (W, 0), (W, 430), (0, 930)],
                                    fill=a(KC(RED), 0.32))
    img.alpha_composite(kirmizi.filter(ImageFilter.GaussianBlur(60)))
    yesil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(yesil).polygon([(0, 930), (W, 430), (W, H), (0, H)],
                                  fill=a(KC(GREEN), 0.30))
    img.alpha_composite(yesil.filter(ImageFilter.GaussianBlur(60)))

    img.alpha_composite(glow((W, H), lambda g: g.line(
        [(0, 930), (W, 430)], fill=a(FG(), ISIK(0.55)), width=5), 18))
    chrome(img, sayac, kaydir=True)
    d = ImageDraw.Draw(img)

    f = fit(d, max(spec["satir1"], spec["satir2"], key=len), anton, 956, 118)
    y = 210
    img.alpha_composite(glow((W, H), lambda g: [
        g.text((GUT, y), spec["satir1"], font=f, fill=a(KC(RED), ISIK(0.5)),
               anchor="la"),
        g.text((GUT, y + f.size * 1.16), spec["satir2"], font=f,
               fill=a(KC(GREEN), ISIK(0.5)), anchor="la")], 30))
    d = ImageDraw.Draw(img)
    d.text((GUT, y), spec["satir1"], font=f, fill=FG(), anchor="la")
    d.text((GUT, y + f.size * 1.16), spec["satir2"], font=f, fill=FG(),
           anchor="la")
    bot = d.textbbox((GUT, y + f.size * 1.16), spec["satir2"], font=f,
                     anchor="la")[3]

    fs = pop(32, "Medium")
    taraf = [(spec["sol_etiket"], spec["sol_metin"], KC(RED), bot + 132),
             (spec["sag_etiket"], spec["sag_metin"], KC(GREEN), bot + 344)]
    for etiket, metin, col, cy in taraf:
        fb = pop(34, "Bold")
        tw = d.textlength(P(etiket), font=fb)
        sag = GUT + tw + 60
        over(img, lambda g, t=cy, c=col, w=tw: g.rounded_rectangle(
            [GUT, t - 34, GUT + w + 60, t + 34], radius=34,
            fill=a(c, 0.18), outline=a(c, 0.9), width=3))
        d = ImageDraw.Draw(img)
        d.text((GUT + 30, cy), P(etiket), font=fb, fill=col, anchor="lm")
        # açıklama sığıyorsa aynı satırda, sığmıyorsa altında
        mw = d.textlength(P(metin), font=fs)
        if sag + 30 + mw <= RIGHT:
            d.text((RIGHT, cy), P(metin), font=fs, fill=FG(), anchor="rm")
        else:
            my = cy + 58
            for ln in wrap(d, P(metin), fs, RIGHT - GUT):
                d.text((GUT, my), ln, font=fs, fill=FG(), anchor="lm")
                my += 44

    fsp = pop(32, "Medium")
    ty = bot + 496
    for ln in wrap(d, P(spec["spot"]), fsp, 900):
        d.text((GUT, ty), ln, font=fsp, fill=FG2(), anchor="la")
        ty += 46

    _rozetler(img, d, spec)
    img.convert("RGB").save(yol)


def kapak_yakin(spec, sayac, yol):
    """Çerçeveyi kıran yakın plan — çizim kenarlardan taşıyor."""
    img = base()
    kart = panel(1480, 1100, govde(spec), spec.get("vurgu"))
    kirp = kart.crop((170, 120, 170 + 1080, 120 + 760))
    img.alpha_composite(kirp, (0, 600))

    perde = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(perde)
    ust = tuple(_P("ust", BG))
    alt = tuple(_P("alt", BG))
    for i in range(760):
        pd.line([(0, i), (W, i)],
                fill=ust + (int(255 * min(1, (760 - i) / 180)),))
    for i in range(1150, H):
        pd.line([(0, i), (W, i)],
                fill=alt + (int(255 * min(1, (i - 1150) / 110)),))
    img.alpha_composite(perde)

    chrome(img, sayac, kaydir=True)
    d = ImageDraw.Draw(img)
    f = fit(d, max(spec["satir1"], spec["satir2"], key=len), anton, 956, 124)
    y = 190
    img.alpha_composite(glow((W, H), lambda g: g.text(
        (GUT, y + f.size * 1.16), spec["satir2"], font=f,
        fill=a(AC(), ISIK(0.8)), anchor="la"), 28))
    d = ImageDraw.Draw(img)
    d.text((GUT, y), spec["satir1"], font=f, fill=FG(), anchor="la")
    d.text((GUT, y + f.size * 1.16), spec["satir2"], font=f, fill=AC(),
           anchor="la")
    bot = d.textbbox((GUT, y + f.size * 1.16), spec["satir2"], font=f,
                     anchor="la")[3]

    fs = pop(32, "Medium")
    ty = bot + 42
    for ln in wrap(d, P(spec["spot"]), fs, 860):
        d.text((GUT, ty), ln, font=fs, fill=FG2(), anchor="la")
        ty += 46

    _rozetler(img, d, spec)
    img.convert("RGB").save(yol)


def ikon(d, ad, cx, cy, s, col):
    """Kart içi vektör simgesi — kalın, ikonik, tek renk."""
    w3 = max(4, int(s * 0.075))
    r = s * 0.5

    if ad == "katman":
        for i in range(4):
            gen = r * (1.75 - i * 0.18)
            yy = cy + r * 0.62 - i * s * 0.21
            d.rounded_rectangle([cx - gen / 2, yy - s * 0.085,
                                 cx + gen / 2, yy + s * 0.085],
                                radius=s * 0.05, outline=col, width=w3)
    elif ad == "nozzle":
        d.polygon([(cx - r * 0.72, cy - r * 0.9), (cx + r * 0.72, cy - r * 0.9),
                   (cx + r * 0.72, cy - r * 0.15), (cx + r * 0.2, cy + r * 0.5),
                   (cx - r * 0.2, cy + r * 0.5), (cx - r * 0.72, cy - r * 0.15)],
                  outline=col, width=w3)
        d.ellipse([cx - r * 0.17, cy + r * 0.68, cx + r * 0.17, cy + r * 1.02],
                  fill=col)
    elif ad == "makara":
        for sg in (-1, 1):
            d.rounded_rectangle([cx + sg * r * 0.78 - r * 0.17, cy - r * 0.92,
                                 cx + sg * r * 0.78 + r * 0.17, cy + r * 0.92],
                                radius=s * 0.05, outline=col, width=w3)
        d.rectangle([cx - r * 0.61, cy - r * 0.46, cx + r * 0.61, cy + r * 0.46],
                    outline=col, width=w3)
        for t in (-0.2, 0.2):
            d.line([(cx - r * 0.61, cy + r * t), (cx + r * 0.61, cy + r * t)],
                   fill=col, width=max(2, w3 - 2))
        d.line([(cx + r * 0.95, cy - r * 0.55), (cx + r * 1.25, cy - r * 0.9)],
               fill=col, width=w3)
    elif ad == "dis":
        d.ellipse([cx - r * 0.56, cy - r * 0.56, cx + r * 0.56, cy + r * 0.56],
                  outline=col, width=w3)
        for i in range(8):
            a_ = i * 3.1416 / 4
            d.line([(cx + math.cos(a_) * r * 0.62, cy + math.sin(a_) * r * 0.62),
                    (cx + math.cos(a_) * r * 0.97, cy + math.sin(a_) * r * 0.97)],
                   fill=col, width=int(w3 * 1.5))
    elif ad == "olcu":
        d.rounded_rectangle([cx - r * 0.98, cy - r * 0.34, cx + r * 0.98,
                             cy + r * 0.34], radius=s * 0.04, outline=col,
                            width=w3)
        for i in range(5):
            xx = cx - r * 0.72 + i * r * 0.36
            uz = r * 0.3 if i % 2 == 0 else r * 0.17
            d.line([(xx, cy - r * 0.34), (xx, cy - r * 0.34 + uz)], fill=col,
                   width=max(2, w3 - 2))
    elif ad == "soru":
        d.ellipse([cx - r * 0.95, cy - r * 0.95, cx + r * 0.95, cy + r * 0.95],
                  outline=col, width=w3)
        d.arc([cx - r * 0.38, cy - r * 0.62, cx + r * 0.38, cy + r * 0.04],
              180, 20, fill=col, width=w3)
        d.line([(cx + r * 0.05, cy - r * 0.08), (cx, cy + r * 0.3)], fill=col,
               width=w3)
        d.ellipse([cx - w3 * 0.9, cy + r * 0.5, cx + w3 * 0.9,
                   cy + r * 0.5 + w3 * 1.8], fill=col)
    elif ad == "kup":
        ust = [(cx, cy - r * 0.95), (cx + r * 0.85, cy - r * 0.45),
               (cx, cy + r * 0.05), (cx - r * 0.85, cy - r * 0.45)]
        d.polygon(ust, outline=col, width=w3)
        d.line([(cx - r * 0.85, cy - r * 0.45), (cx - r * 0.85, cy + r * 0.5),
                (cx, cy + r * 0.98), (cx + r * 0.85, cy + r * 0.5),
                (cx + r * 0.85, cy - r * 0.45)], fill=col, width=w3)
        d.line([(cx, cy + r * 0.05), (cx, cy + r * 0.98)], fill=col, width=w3)
        for t in (0.3, 0.62):
            d.line([(cx - r * 0.85, cy - r * 0.45 + r * 0.95 * t),
                    (cx, cy + r * 0.05 + r * 0.93 * t)], fill=col,
                   width=max(2, w3 - 2))
    elif ad == "isi":
        for i, ox in enumerate((-r * 0.6, 0, r * 0.6)):
            pts = []
            for j in range(13):
                t = j / 12
                pts.append((cx + ox + math.sin(t * 6.3 + i) * r * 0.22,
                            cy + r * 0.95 - t * r * 1.9))
            d.line(pts, fill=col, width=w3)
    elif ad == "hiz":
        for i, (uz, yy) in enumerate([(1.5, -0.55), (1.1, 0), (1.5, 0.55)]):
            d.line([(cx - r * 0.95, cy + r * yy),
                    (cx - r * 0.95 + r * uz * 0.72, cy + r * yy)],
                   fill=col, width=w3)
        d.polygon([(cx + r * 0.42, cy - r * 0.42), (cx + r * 0.98, cy),
                   (cx + r * 0.42, cy + r * 0.42)], fill=col)
    elif ad == "duvar":
        for i in range(3):
            g = r * (0.95 - i * 0.26)
            d.rounded_rectangle([cx - g, cy - g, cx + g, cy + g],
                                radius=s * 0.06, outline=col, width=w3)
    elif ad == "tabla":
        d.rounded_rectangle([cx - r * 0.98, cy - r * 0.22, cx + r * 0.98,
                             cy + r * 0.18], radius=s * 0.04, outline=col,
                            width=w3)
        for ox in (-r * 0.5, 0, r * 0.5):
            pts = [(cx + ox + math.sin(t / 4 * 6.3) * r * 0.14,
                    cy + r * 0.4 + t * r * 0.14) for t in range(5)]
            d.line(pts, fill=col, width=max(3, w3 - 1))
    elif ad == "uyari":
        d.polygon([(cx, cy - r * 0.95), (cx + r * 0.98, cy + r * 0.78),
                   (cx - r * 0.98, cy + r * 0.78)], outline=col, width=w3)
        d.line([(cx, cy - r * 0.3), (cx, cy + r * 0.24)], fill=col, width=w3)
        d.ellipse([cx - w3 * 0.8, cy + r * 0.44, cx + w3 * 0.8, cy + r * 0.44 +
                   w3 * 1.6], fill=col)
    elif ad == "zaman":
        d.ellipse([cx - r * 0.92, cy - r * 0.92, cx + r * 0.92, cy + r * 0.92],
                  outline=col, width=w3)
        d.line([(cx, cy), (cx, cy - r * 0.52)], fill=col, width=w3)
        d.line([(cx, cy), (cx + r * 0.44, cy + r * 0.2)], fill=col, width=w3)
    elif ad == "cip":
        d.rounded_rectangle([cx - r * 0.62, cy - r * 0.62, cx + r * 0.62,
                             cy + r * 0.62], radius=s * 0.06, outline=col,
                            width=w3)
        for t in (-0.34, 0, 0.34):
            for sg in (-1, 1):
                d.line([(cx + sg * r * 0.62, cy + r * t),
                        (cx + sg * r * 0.97, cy + r * t)], fill=col, width=w3)
                d.line([(cx + r * t, cy + sg * r * 0.62),
                        (cx + r * t, cy + sg * r * 0.97)], fill=col, width=w3)
    elif ad == "pil":
        d.rounded_rectangle([cx - r * 0.95, cy - r * 0.5, cx + r * 0.75,
                             cy + r * 0.5], radius=s * 0.05, outline=col,
                            width=w3)
        d.rectangle([cx + r * 0.78, cy - r * 0.2, cx + r * 0.98, cy + r * 0.2],
                    fill=col)
        for i in range(2):
            d.rectangle([cx - r * 0.78 + i * r * 0.46, cy - r * 0.26,
                         cx - r * 0.48 + i * r * 0.46, cy + r * 0.26], fill=col)
    elif ad == "dalga":
        pts = [(cx - r * 0.98 + i / 24 * r * 1.96,
                cy - math.sin(i / 24 * 12.6) * r * 0.62) for i in range(25)]
        d.line(pts, fill=col, width=w3, joint="curve")
    elif ad == "damla":
        d.polygon([(cx, cy - r * 0.98), (cx + r * 0.6, cy + r * 0.25),
                   (cx - r * 0.6, cy + r * 0.25)], outline=col, width=w3)
        d.ellipse([cx - r * 0.6, cy - r * 0.35, cx + r * 0.6, cy + r * 0.85],
                  outline=col, width=w3)
    elif ad == "terazi":
        d.line([(cx, cy - r * 0.9), (cx, cy + r * 0.85)], fill=col, width=w3)
        d.line([(cx - r * 0.92, cy - r * 0.5), (cx + r * 0.92, cy - r * 0.5)],
               fill=col, width=w3)
        for sg in (-1, 1):
            d.arc([cx + sg * r * 0.92 - r * 0.38, cy - r * 0.5,
                   cx + sg * r * 0.92 + r * 0.38, cy + r * 0.26], 0, 180,
                  fill=col, width=w3)
        d.line([(cx - r * 0.5, cy + r * 0.85), (cx + r * 0.5, cy + r * 0.85)],
               fill=col, width=w3)


def _kart(img, x, y, w, h, k):
    col = KC(RENKLER.get(k.get("renk", "tema"), ACC))
    if k.get("renk", "tema") == "tema":
        col = AC()
    over(img, lambda g: g.rounded_rectangle(
        [x, y, x + w, y + h], radius=20, fill=a(col, _P("kart_op", 0.09)),
        outline=a(col, _P("kontur_op", 0.55)), width=3))
    d = ImageDraw.Draw(img)

    d.text((x + 26, y + 34), P(k["etiket"]).upper(), font=mono(23, True),
           fill=col, anchor="lm")

    durum = k.get("durum")
    if durum:
        dc = KC(GREEN) if durum == "dogru" else KC(RED)
        bx = x + w - 26
        over(img, lambda g, c=dc, b=bx: g.ellipse(
            [b - 34, y + 17, b, y + 51], fill=a(c, 0.18), outline=c, width=3))
        d = ImageDraw.Draw(img)
        cx, cy = bx - 17, y + 34
        if durum == "dogru":
            d.line([(cx - 8, cy), (cx - 2, cy + 7)], fill=dc, width=4)
            d.line([(cx - 2, cy + 7), (cx + 9, cy - 7)], fill=dc, width=4)
        else:
            d.line([(cx - 8, cy - 8), (cx + 8, cy + 8)], fill=dc, width=4)
            d.line([(cx + 8, cy - 8), (cx - 8, cy + 8)], fill=dc, width=4)

    simge = k.get("ikon")
    ik_s = min(h * 0.52, 108) if simge else 0
    metin_gen = w - 52 - (ik_s + 26 if simge else 0)
    if simge:
        ikx, iky = x + w - 30 - ik_s / 2, y + h / 2 + 8
        img.alpha_composite(glow((W, H), lambda g: ikon(
            g, simge, ikx, iky, ik_s, a(col, 0.85)), 16))
        d = ImageDraw.Draw(img)
        ikon(d, simge, ikx, iky, ik_s, col)

    fa, satir = pop(24, "Medium"), []
    if k.get("alt"):
        maks = 3 if h >= 165 else 2
        for boy in (24, 23, 22, 21, 20, 19, 18, 17, 16):
            fa = pop(boy, "Medium")
            satir = wrap(d, P(k["alt"]), fa, metin_gen)
            if len(satir) <= maks:
                break
        satir = satir[:maks]
    ara = fa.size + 6
    alt_ust = y + h - 26 - (len(satir) - 1) * ara if satir else y + h - 8

    deger = P(k["deger"])
    ust_sinir, alt_sinir = y + 56, alt_ust - 20
    bant = max(40, alt_sinir - ust_sinir)
    boy = int(bant * 1.05)
    while boy > 28:
        fd = anton(boy)
        bb = d.textbbox((0, 0), deger, font=fd, anchor="ls")
        if (d.textlength(deger, font=fd) <= metin_gen
                and bb[3] - bb[1] <= bant):
            break
        boy -= 2
    fd = anton(max(28, boy))
    dy = (ust_sinir + alt_sinir) / 2
    img.alpha_composite(glow((W, H), lambda g: g.text(
        (x + 26, dy), deger, font=fd, fill=a(RK(col), ISIK(0.75)),
        anchor="lm"), 18))
    d = ImageDraw.Draw(img)
    d.text((x + 26, dy), deger, font=fd, fill=RK(col), anchor="lm")

    ay = alt_ust
    for ln in satir:
        d.text((x + 26, ay), ln, font=fa, fill=FG2(), anchor="lm")
        ay += ara


def kapak_izgara(spec, sayac, yol):
    """Kopya kâğıdı kapağı — tek karede yoğun, kaydedilesi bilgi."""
    img = base()
    chrome(img, sayac, kaydir=True)
    d = ImageDraw.Draw(img)

    s1, s2 = spec["satir1"], spec["satir2"]
    f = fit(d, max(s1, s2, key=len), anton, 956, 92)
    y = 172
    img.alpha_composite(glow((W, H), lambda g: g.text(
        (GUT, y + f.size * 1.12), s2, font=f, fill=a(AC(), ISIK(0.8)),
        anchor="la"), 24))
    d = ImageDraw.Draw(img)
    d.text((GUT, y), s1, font=f, fill=FG(), anchor="la")
    d.text((GUT, y + f.size * 1.12), s2, font=f, fill=AC(), anchor="la")
    ust = d.textbbox((GUT, y + f.size * 1.12), s2, font=f, anchor="la")[3] + 26
    if spec.get("spot"):
        fs = pop(28, "Medium")
        d.text((GUT, ust), P(spec["spot"]), font=fs, fill=FG2(),
               anchor="la")
        ust += 52

    kartlar = spec["kartlar"]
    bosluk = 22
    satirlar, i = [], 0
    while i < len(kartlar):
        if kartlar[i].get("genis"):
            satirlar.append([kartlar[i]])
            i += 1
        elif i + 1 < len(kartlar) and not kartlar[i + 1].get("genis"):
            satirlar.append(kartlar[i:i + 2])
            i += 2
        else:
            satirlar.append([kartlar[i]])
            i += 1

    alt = 1268
    yuk = (alt - ust - bosluk * (len(satirlar) - 1)) / len(satirlar)
    cy = ust
    for satir in satirlar:
        if len(satir) == 1:
            _kart(img, GUT, cy, RIGHT - GUT, yuk, satir[0])
        else:
            gen = (RIGHT - GUT - bosluk) / 2
            for j, k in enumerate(satir):
                _kart(img, GUT + j * (gen + bosluk), cy, gen, yuk, k)
        cy += yuk + bosluk

    img.convert("RGB").save(yol)


def kapak_liste(spec, sayac, yol):
    """Solda ikonlu liste, sağda katlı kule — her satır kendi katına bağlı."""
    img = base()
    chrome(img, sayac, kaydir=True)
    d = ImageDraw.Draw(img)

    s1, s2 = spec["satir1"], spec["satir2"]
    f = fit(d, max(s1, s2, key=len), anton, 956, 84)
    y = 168
    img.alpha_composite(glow((W, H), lambda g: g.text(
        (GUT, y + f.size * 1.12), s2, font=f, fill=a(AC(), ISIK(0.8)),
        anchor="la"), 24))
    d = ImageDraw.Draw(img)
    d.text((GUT, y), s1, font=f, fill=FG(), anchor="la")
    d.text((GUT, y + f.size * 1.12), s2, font=f, fill=AC(), anchor="la")
    ust = d.textbbox((GUT, y + f.size * 1.12), s2, font=f, anchor="la")[3] + 24
    if spec.get("spot"):
        fs = pop(27, "Medium")
        for ln in wrap(d, P(spec["spot"]), fs, 956)[:2]:
            d.text((GUT, ust), ln, font=fs, fill=FG2(), anchor="la")
            ust += 40
        ust += 14

    satirlar = spec["satirlar"][:10]
    n = len(satirlar)
    alt = 1258
    ara = 12 if n > 7 else 16
    yuk = (alt - ust - ara * (n - 1)) / n

    SOL, SAG = GUT, 648           # liste sütunu
    KUL_X0, KUL_X1 = 742, RIGHT   # kule

    renkler = [KC(RENKLER.get(r.get("renk", "tema"), ACC))
               if r.get("renk", "tema") != "tema" else AC()
               for r in satirlar]

    # kule gövdesi
    over(img, lambda g: g.rounded_rectangle(
        [KUL_X0, ust, KUL_X1, alt], radius=26, fill=a(AC(), 0.07),
        outline=a(AC(), _P("kontur_op", 0.55)), width=3))

    fe = pop(max(20, min(27, int(yuk * 0.34))), "SemiBold")
    fd = mono(max(19, min(26, int(yuk * 0.31))), True)

    for i, (r, col) in enumerate(zip(satirlar, renkler)):
        ry = ust + i * (yuk + ara)
        cy = ry + yuk / 2

        # --- liste satırı
        over(img, lambda g, t=ry, c=col: g.rounded_rectangle(
            [SOL, t, SAG, t + yuk], radius=16, fill=a(c, _P("kart_op", 0.09)),
            outline=a(c, _P("kontur_op", 0.55)), width=2))
        d = ImageDraw.Draw(img)
        isim = P(r["etiket"])
        deger = P(r.get("deger", ""))
        dw = d.textlength(deger, font=fd) if deger else 0
        ikx = SOL + 26 + yuk * 0.22
        if r.get("ikon"):
            ikon(d, r["ikon"], ikx, cy, yuk * 0.52, col)
            tx = ikx + yuk * 0.30 + 16
        else:
            tx = SOL + 26
        fi = fe
        while (d.textlength(isim, font=fi) > SAG - 24 - dw - tx
               and fi.size > 17):
            fi = pop(fi.size - 1, "SemiBold")
        d.text((tx, cy), isim, font=fi, fill=FG(), anchor="lm")
        if deger:
            d.text((SAG - 22, cy), deger, font=fd, fill=col, anchor="rm")

        # --- bağlantı çizgisi
        over(img, lambda g, c=col, m=cy: [
            g.ellipse([x, m - 2, x + 4, m + 2], fill=a(c, 0.75))
            for x in range(SAG + 14, KUL_X0 - 8, 14)])

        # --- kule katı
        ky0, ky1 = ry + 2, ry + yuk - 2
        over(img, lambda g, c=col, p0=ky0, p1=ky1: (
            g.rectangle([KUL_X0 + 6, p0, KUL_X1 - 6, p1], fill=a(c, 0.20)),
            g.line([(KUL_X0 + 6, p1 + ara / 2), (KUL_X1 - 6, p1 + ara / 2)],
                   fill=a(AC(), 0.35), width=2)))
        d = ImageDraw.Draw(img)
        fn = anton(int(min(yuk * 0.66, 64)))
        d.text(((KUL_X0 + KUL_X1) / 2, cy), str(n - i), font=fn, fill=col,
               anchor="mm")

    img.convert("RGB").save(yol)


def kapak(spec, sayac, yol):
    img = base()
    chrome(img, sayac, kaydir=True)
    d = ImageDraw.Draw(img)
    s1, s2 = spec["satir1"], spec["satir2"]
    f = fit(d, max(s1, s2, key=len), anton, 956, 128)
    y = 178
    img.alpha_composite(glow((W, H), lambda g: g.text(
        (GUT, y + f.size * 1.16), s2, font=f, fill=a(AC(), ISIK(0.75)),
        anchor="la"), 26))
    d = ImageDraw.Draw(img)
    d.text((GUT, y), s1, font=f, fill=FG(), anchor="la")
    d.text((GUT, y + f.size * 1.16), s2, font=f, fill=AC(), anchor="la")
    bot = d.textbbox((GUT, y + f.size * 1.16), s2, font=f, anchor="la")[3]

    fs = pop(32, "Medium")
    ty = bot + 44
    for ln in wrap(d, P(spec["spot"]), fs, 780):
        d.text((GUT, ty), ln, font=fs, fill=FG2(), anchor="la")
        ty += 46

    place(img, panel(956, 466, govde(spec)), GUT, 690)

    fx = pop(25, "Medium")
    boxes, x = [], GUT
    for metin, renk in spec.get("rozetler", []):
        col = KC(RENKLER.get(renk, ACC)) if renk != "tema" else AC()
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
        d.text((px + 58, 1230), metin, font=fx, fill=FG2(), anchor="lm")
    img.convert("RGB").save(yol)


def adim(spec, govde_fn, no, toplam, sayac, yol):
    img = base()
    chrome(img, sayac, kaydir=True)
    d = ImageDraw.Draw(img)
    over(img, lambda g: g.rounded_rectangle(
        [GUT, 168, GUT + 96, 264], radius=22, fill=a(AC(), 0.14),
        outline=a(AC(), 0.6), width=3))
    d = ImageDraw.Draw(img)
    d.text((GUT + 48, 216), "%02d" % no, font=anton(58), fill=AC(),
           anchor="mm")
    d.text((GUT + 124, 216), "ADIM %d / %d" % (no, toplam), font=mono(28),
           fill=SOFT(), anchor="lm")

    fh = fit(d, max(wrap(d, spec["baslik"], archivo(58), 940), key=len),
             archivo, 940, 58)
    y = 320
    for ln in wrap(d, spec["baslik"], fh, 940):
        d.text((GUT, y), ln, font=fh, fill=FG(), anchor="la")
        y += fh.size * 1.26
    d.rectangle([GUT, y + 18, GUT + 110, y + 24], fill=AC())

    fs = pop(30)
    ty = y + 66
    for ln in wrap(d, P(spec["aciklama"]), fs, 860):
        d.text((GUT, ty), ln, font=fs, fill=FG2(), anchor="la")
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
    d.text((GUT, y), s1, font=f, fill=FG(), anchor="la")
    img.alpha_composite(glow((W, H), lambda g: g.text(
        (GUT, y + f.size * 1.16), s2, font=f, fill=a(AC(), ISIK(0.75)),
        anchor="la"), 26))
    d = ImageDraw.Draw(img)
    d.text((GUT, y + f.size * 1.16), s2, font=f, fill=AC(), anchor="la")
    bot = d.textbbox((GUT, y + f.size * 1.16), s2, font=f, anchor="la")[3]

    fy = bot + 86
    fs = pop(30, "Medium")
    for i, (k, v) in enumerate(spec["kriterler"]):
        top = fy + i * 128
        over(img, lambda g, t=top: g.rounded_rectangle(
            [GUT, t, RIGHT, t + 104], radius=18, fill=a(AC(), 0.08),
            outline=a(AC(), 0.32), width=2))
        dd = ImageDraw.Draw(img)
        dd.text((GUT + 30, top + 52), k, font=mono(26, True), fill=AC(),
                anchor="lm")
        dd.text((RIGHT - 30, top + 52), P(v), font=fs, fill=FG(),
                anchor="rm")

    d = ImageDraw.Draw(img)
    btn = "ARKADAŞINA YOLLA"
    fb = pop(30, "Bold")
    tw = d.textlength(btn, font=fb)
    by = 1176
    BC, BY = AC(), UZER(AC())
    img.alpha_composite(glow((W, H), lambda g: g.rounded_rectangle(
        [GUT, by, GUT + tw + 112, by + 74], radius=37,
        fill=a(BC, ISIK(0.55))), 30))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([GUT, by, GUT + tw + 112, by + 74], radius=37, fill=BC)
    d.text((GUT + 44, by + 37), btn, font=fb, fill=BY, anchor="lm")
    ax = GUT + 44 + tw + 26
    d.line([(ax, by + 37), (ax + 26, by + 37)], fill=BY, width=5)
    d.polygon([(ax + 23, by + 29), (ax + 40, by + 37), (ax + 23, by + 45)],
              fill=BY)
    d.text((GUT, by - 46), P(spec.get("not", "")), font=pop(26), fill=SOFT(),
           anchor="lm")
    img.convert("RGB").save(yol)


def hikaye(spec, yol):
    """1080 x 1920 hikaye — gönderiye yönlendiren tek kare."""
    SW, SH = 1080, 1920
    if _mod() != "koyu":
        img = base_renkli(SW, SH)
    else:
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
        [lx, 296, lx + lw + 40, 338], radius=21, fill=a(AC(), 0.12),
        outline=a(AC(), 0.45), width=2))
    d = ImageDraw.Draw(img)
    d.text((lx + 20, 317), LABEL, font=fl, fill=AC(), anchor="lm")

    s1 = spec.get("satir1", spec.get("ustbilgi", "").upper())
    s2 = spec.get("satir2", spec.get("rakam", ""))
    f = fit(d, max(s1, s2, key=len), anton, 956, 132)
    y = 420
    img.alpha_composite(glow((SW, SH), lambda g: g.text(
        (GUT, y + f.size * 1.16), s2, font=f, fill=a(AC(), ISIK(0.75)),
        anchor="la"), 26))
    d = ImageDraw.Draw(img)
    d.text((GUT, y), s1, font=f, fill=FG(), anchor="la")
    d.text((GUT, y + f.size * 1.16), s2, font=f, fill=AC(), anchor="la")
    bot = d.textbbox((GUT, y + f.size * 1.16), s2, font=f, anchor="la")[3]

    fs = pop(34, "Medium")
    ty = bot + 50
    for ln in wrap(d, P(spec["spot"]), fs, 900):
        d.text((GUT, ty), ln, font=fs, fill=FG2(), anchor="la")
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
    BC, BY = AC(), UZER(AC())
    img.alpha_composite(glow((SW, SH), lambda g: g.rounded_rectangle(
        [GUT, by, GUT + tw + 120, by + 80], radius=40,
        fill=a(BC, ISIK(0.55))), 30))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([GUT, by, GUT + tw + 120, by + 80], radius=40, fill=BC)
    d.text((GUT + 46, by + 40), btn, font=fb, fill=BY, anchor="lm")
    ax = GUT + 46 + tw + 28
    d.line([(ax, by + 40), (ax + 28, by + 40)], fill=BY, width=5)
    d.polygon([(ax + 25, by + 31), (ax + 44, by + 40), (ax + 25, by + 49)],
              fill=BY)
    d.text((GUT, by + 128), "profilde yeni gönderi", font=pop(28),
           fill=SOFT(), anchor="lm")
    img.convert("RGB").save(yol)


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    theme(spec["kategori"])
    zemin_ayarla(spec.get("zemin", spec["kapak"].get("zemin", "koyu")))

    slaytlar = spec["slaytlar"]
    toplam = 1 + len(slaytlar) + (1 if spec.get("kapanis") else 0)
    n = 1
    tip = spec["kapak"].get("tip", "klasik")
    {"rakam": kapak_rakam, "carpisma": kapak_carpisma,
     "yakin": kapak_yakin, "izgara": kapak_izgara,
     "liste": kapak_liste}.get(tip, kapak)(
        spec["kapak"], "%d/%d" % (n, toplam), os.path.join(out, "%d.png" % n))
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
