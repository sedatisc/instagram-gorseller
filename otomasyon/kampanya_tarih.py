#!/usr/bin/env python3
"""Kampanya karelerindeki tarihleri plana göre basıyor.

Çekiliş afişinde "SON TARİH" kareye basılı bir yazı; plan ileri kayınca
görseldeki tarih yanlış kalıyordu — bir kere 15 Ekim yazılıp gönderi
19 Ekim'e kaydı. Bu yüzden spec dosyalarında tarih yerine simge
duruyor ({son_tarih}, {oylama_gunu}); gerçek tarih plan takvime
oturduğunda buradan hesaplanıp kareler yeniden basılıyor.

Simgeler:
  {son_tarih}    yorumların kapandığı an  — "22 Ekim Çarşamba 23.59"
  {oylama_gunu}  finalist ve anket günü   — "23 Ekim Perşembe"

    python3 otomasyon/kampanya_tarih.py          # plan oturduysa bas
    python3 otomasyon/kampanya_tarih.py --zorla  # oturmasa da bas
"""
import json
import os
import subprocess
import sys
import tempfile
from datetime import timedelta

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
import sira                                              # noqa: E402

AY = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
      "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


def uzun(t, saat=""):
    s = "%d %s %s" % (t.day, AY[t.month - 1], sira.GUN[t.weekday()])
    return (s + " " + saat).strip()


def simgeler():
    """Çekilişin son günü kampanya kuyruğundaki en geç gönderiden,
    oylama onun ertesi gününden geliyor."""
    bas = sira.baslangic()
    kamp = [k for k in sira.kampanyalar() if k.get("tur", "gonderi") == "gonderi"]
    if not kamp:
        return None
    son = max(int(k.get("gun", 0)) for k in kamp)
    bitis = bas + timedelta(days=son)
    return {"son_tarih": uzun(bitis, "23.59"),
            "oylama_gunu": uzun(bitis + timedelta(days=1))}


def bas(klasor, deger):
    yol = os.path.join(KOK, klasor, "spec.json")
    if not os.path.exists(yol):
        return False
    ham = open(yol, encoding="utf-8").read()
    if not any("{%s}" % a in ham for a in deger):
        return False
    dolu = ham
    for a, d in deger.items():
        dolu = dolu.replace("{%s}" % a, d)
    with tempfile.TemporaryDirectory() as t:
        gecici = os.path.join(t, "spec.json")
        with open(gecici, "w", encoding="utf-8") as f:
            f.write(dolu)
        subprocess.run([sys.executable, os.path.join(KOK, "uret.py"),
                        gecici, os.path.join(KOK, klasor)],
                       check=True, cwd=KOK)
    print("%s · tarihler basıldı" % klasor)
    return True


def main():
    if not sira.plan_durumu().get("baslangic") and "--zorla" not in sys.argv:
        print("Plan henüz takvime oturmadı — kampanya kareleri "
              "ilk yayında basılacak.")
        return 0
    deger = simgeler()
    if not deger:
        print("Kampanya kuyruğu boş.")
        return 0
    print("son tarih: %s · oylama: %s"
          % (deger["son_tarih"], deger["oylama_gunu"]))
    d = json.load(open(os.path.join(KOK, "DURUM.json"), encoding="utf-8"))
    n = 0
    for k in d["kuyruk_bekleyen"].get("kampanya", []):
        if bas(k["klasor"], deger):
            n += 1
    print("%d kampanya klasörü yeniden basıldı" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
