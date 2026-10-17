#!/usr/bin/env python3
"""spec'teki "cizim" ögelerini saydam PNG olarak basıyor.

Devre şemaları eski Pillow hattında kareyle birlikte çiziliyordu. HTML
şablonuna geçince çizim motoru dışarıda kaldı ve elektronik
gönderilerinin kapağı boş çıkıyordu. Burada aynı motor yalnız çizimi
basıyor, HTML şablonu da onu görsel olarak yerleştiriyor.

    python3 arac/cizim_png.py <spec.json> <cikti.png>
"""
import hashlib
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)

from PIL import Image, ImageDraw                            # noqa: E402

ONBELLEK = os.path.join(KOK, "gorsel", "cizim")


def _motor():
    """uret.py'yi açık zemine ayarlayıp çizim işlevini veriyor."""
    import uret
    uret.zemin_ayarla("acik")
    uret.stil_ayarla("duru") if hasattr(uret, "stil_ayarla") else None
    return uret


def bas(ogeler, cikti, tuval=(2400, 1800), kenar=24):
    """Ögeleri saydam zemine çizip içeriğe kırpıyor."""
    u = _motor()
    im = Image.new("RGBA", tuval, (0, 0, 0, 0))
    u.ciz(ImageDraw.Draw(im), ogeler)
    bb = im.getbbox()
    if not bb:
        return None
    bb = (max(0, bb[0] - kenar), max(0, bb[1] - kenar),
          min(tuval[0], bb[2] + kenar), min(tuval[1], bb[3] + kenar))
    im.crop(bb).save(cikti)
    return cikti


def kirpilmis(ogeler, kutu, pay=0.12):
    """Şemanın yalnız `kutu` ile gösterilen yerini basıyor.

    Slayt spec'lerindeki "vurgu" bu kutunun koordinatları; eski hat
    her slaytta şemanın o bölgesine yakınlaşıyordu."""
    os.makedirs(ONBELLEK, exist_ok=True)
    imza = hashlib.sha1(
        json.dumps([ogeler, list(kutu)], sort_keys=True,
                   ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:16]
    yol = os.path.join(ONBELLEK, imza + ".png")
    if os.path.exists(yol):
        return yol
    u = _motor()
    tuval = (2400, 1800)
    im = Image.new("RGBA", tuval, (0, 0, 0, 0))
    u.ciz(ImageDraw.Draw(im), ogeler)
    x1, y1, x2, y2 = [float(v) for v in kutu]
    mx = max(60.0, (x2 - x1) * pay)
    my = max(60.0, (y2 - y1) * pay)
    k = (max(0, int(x1 - mx)), max(0, int(y1 - my)),
         min(tuval[0], int(x2 + mx)), min(tuval[1], int(y2 + my)))
    if k[2] - k[0] < 40 or k[3] - k[1] < 40:
        return None
    par = im.crop(k)
    if not par.getbbox():
        return None
    par.save(yol)
    return yol


def onbellekli(ogeler):
    """Aynı çizim iki kere basılmasın; yol döndürüyor."""
    os.makedirs(ONBELLEK, exist_ok=True)
    imza = hashlib.sha1(
        json.dumps(ogeler, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:16]
    yol = os.path.join(ONBELLEK, imza + ".png")
    if os.path.exists(yol):
        return yol
    return bas(ogeler, yol)


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    ogeler = (spec.get("kapak") or {}).get("cizim")
    if not ogeler:
        raise SystemExit("spec'te kapak.cizim yok")
    print(bas(ogeler, sys.argv[2]))


if __name__ == "__main__":
    main()
