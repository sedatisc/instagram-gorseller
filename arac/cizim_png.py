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
