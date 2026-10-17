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


def _genislet(im, k, adim=10, bant=48):
    """Kırpma kenarı bir ögenin ortasından geçiyorsa dışarı açıyor.

    Vurgu kutusu etiketlerden dar olabiliyor; olduğu gibi kırpınca
    yazı yarım, kutular kesik çıkıyordu. Kenar çizgisinde boya
    kaldığı sürece o kenarı geri çekiyoruz."""
    a = im.getchannel("A")
    tam = im.getbbox() or (0, 0, im.width, im.height)
    x1, y1, x2, y2 = k
    # Tek piksellik kenar yoklaması iki yazı satırı arasındaki
    # boşlukta duruyordu; kenarın dışına doğru bir bant bakıyoruz.
    for _ in range(400):
        degisti = False
        if x1 > tam[0] and a.crop((max(tam[0], x1 - bant), y1,
                                   x1 + 1, y2)).getbbox():
            x1 = max(tam[0], x1 - adim); degisti = True
        if x2 < tam[2] and a.crop((x2 - 1, y1,
                                   min(tam[2], x2 + bant), y2)).getbbox():
            x2 = min(tam[2], x2 + adim); degisti = True
        if y1 > tam[1] and a.crop((x1, max(tam[1], y1 - bant),
                                   x2, y1 + 1)).getbbox():
            y1 = max(tam[1], y1 - adim); degisti = True
        if y2 < tam[3] and a.crop((x1, y2 - 1, x2,
                                   min(tam[3], y2 + bant))).getbbox():
            y2 = min(tam[3], y2 + adim); degisti = True
        if not degisti:
            break
    # İki yazı satırı arasındaki boşlukta durup altta kalan etiketi
    # kesiyordu: kenara yakınsa çizimin tamamına yapışıyoruz.
    tw, th = tam[2] - tam[0], tam[3] - tam[1]
    if x1 - tam[0] < tw * 0.1:
        x1 = tam[0]
    if tam[2] - x2 < tw * 0.1:
        x2 = tam[2]
    if y1 - tam[1] < th * 0.1:
        y1 = tam[1]
    if tam[3] - y2 < th * 0.1:
        y2 = tam[3]
    pay = 18
    return (x1 - pay, y1 - pay, x2 + pay, y2 + pay)


def kirpilmis(ogeler, kutu, pay=0.32):
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
    mx = max(180.0, (x2 - x1) * pay)
    my = max(180.0, (y2 - y1) * pay)
    k = (max(0, int(x1 - mx)), max(0, int(y1 - my)),
         min(tuval[0], int(x2 + mx)), min(tuval[1], int(y2 + my)))
    if k[2] - k[0] < 40 or k[3] - k[1] < 40:
        return None
    k = _genislet(im, k)
    # Kırpma çizimin neredeyse tamamını kapsıyorsa yakınlaşmanın
    # anlamı kalmıyor: üç slayt aynı kare oluyor. Böyle durumda
    # slayt metin kurgusuna düşüyor, şema yalnız kapakta kalıyor.
    tam = im.getbbox() or (0, 0, im.width, im.height)
    ta = float((tam[2] - tam[0]) * (tam[3] - tam[1])) or 1.0
    if (k[2] - k[0]) * (k[3] - k[1]) / ta > 0.65:
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
