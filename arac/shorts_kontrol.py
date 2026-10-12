#!/usr/bin/env python3
"""Basılan Shorts'ların toptan kontrolü.

Yirmi videoyu tek tek açmak yerine hepsinden birer kare alıp tek bir
sayfaya diziyor; eksik, boş ya da kırpılmış olan orada görünüyor.
Ayrıca her videonun ölçüsünü, ses akışını ve süresini doğruluyor.

    python3 arac/shorts_kontrol.py              # youtube/DURUM.json sırası
    python3 arac/shorts_kontrol.py 0.45         # kareyi %45'inden al
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIKTI = os.path.join(KOK, "youtube", "gorsel", "kontrol.jpg")
SUTUN = 7


def bilgi(yol):
    g = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,codec_name,width,height:format=duration",
         "-of", "json", yol], capture_output=True, text=True)
    d = json.loads(g.stdout or "{}")
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"),
             {})
    s = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"),
             {})
    return (v.get("width"), v.get("height"), s.get("codec_name"),
            float(d.get("format", {}).get("duration", 0)))


def kare(yol, an, hedef):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.2f" % an,
                    "-i", yol, "-frames:v", "1", "-vf", "scale=300:-1", hedef],
                   check=True)


def main():
    oran = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    kuyruk = json.load(open(os.path.join(KOK, "youtube", "DURUM.json"),
                            encoding="utf-8"))["kuyruk"]
    gec, sorun, kareler = 0, [], []
    gecici = tempfile.mkdtemp()

    for k in kuyruk:
        yol = os.path.join(KOK, k["klasor"], "shorts.mp4")
        ad = k["klasor"]
        if not os.path.exists(yol):
            sorun.append("%s · dosya yok" % ad)
            continue
        en, boy, ses, sure = bilgi(yol)
        if (en, boy) != (1080, 1920):
            sorun.append("%s · ölçü %sx%s" % (ad, en, boy))
        if ses != "aac":
            sorun.append("%s · ses akışı %s" % (ad, ses))
        if not 6 <= sure <= 60:
            sorun.append("%s · süre %.1f sn" % (ad, sure))
        p = os.path.join(gecici, ad + ".png")
        kare(yol, sure * oran, p)
        kareler.append((ad, p, sure))
        gec += 1

    if kareler:
        ilk = Image.open(kareler[0][1])
        w, h = ilk.size
        sat = (len(kareler) + SUTUN - 1) // SUTUN
        sayfa = Image.new("RGB", (w * SUTUN, (h + 26) * sat), (16, 16, 20))
        d = ImageDraw.Draw(sayfa)
        for i, (ad, p, sure) in enumerate(kareler):
            x, y = (i % SUTUN) * w, (i // SUTUN) * (h + 26)
            sayfa.paste(Image.open(p), (x, y))
            d.text((x + 6, y + h + 6), "%s  %.1fs" % (ad[5:], sure),
                   fill=(190, 190, 200))
        os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
        sayfa.save(CIKTI, "JPEG", quality=88)
        print("%s  (%d video)" % (CIKTI, gec))

    print("%d/%d video hazır" % (gec, len(kuyruk)))
    for s in sorun:
        print("  SORUN: " + s)
    return 1 if sorun else 0


if __name__ == "__main__":
    sys.exit(main())
