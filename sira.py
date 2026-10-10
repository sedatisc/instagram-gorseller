#!/usr/bin/env python3
"""Yayın sırası — 4 gönderi + 4 hikaye + 1 reels / gün.

DURUM.json'daki kuyruğu okur, saat ızgarasını uygular, YAYIN-LISTESI.md'yi
üretir. Metricool kotası açılınca aynı kuyruk doğrudan createScheduledPost
ile planlanır; saatler buradan okunur.

    python3 sira.py           # listeyi yeniden üret
    python3 sira.py --eksik   # yalnız boş slotları say
"""
import json
import os
import re
import sys
from datetime import date, datetime, timedelta

GUN = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma",
       "Cumartesi", "Pazar"]

# Slot sırası sabit; saatler güne göre değişiyor.
SLOTLAR = ["3dbaski", "elektronik", "urun", "proje"]

BASLIK = {"3dbaski": "3D BASKI & ÜRETİM DONANIMI",
          "elektronik": "ELEKTRONİK & IoT",
          "urun": "ÜRÜN & MAĞAZA",
          "proje": "PROJE & ATÖLYE"}

# gün indeksi -> {slot: "SS:DD"} + "reels"
IZGARA = {
    0: {"3dbaski": "08:12", "elektronik": "12:38", "urun": "17:24",
        "proje": "19:40", "reels": "21:10"},            # Pazartesi
    1: {"3dbaski": "08:12", "elektronik": "12:38", "urun": "17:24",
        "reels": "19:36", "proje": "20:42"},            # Salı
    2: {"3dbaski": "08:12", "elektronik": "12:38", "urun": "17:24",
        "reels": "19:36", "proje": "20:42"},            # Çarşamba
    3: {"3dbaski": "08:12", "elektronik": "12:38", "urun": "17:24",
        "reels": "19:36", "proje": "20:42"},            # Perşembe
    4: {"3dbaski": "08:12", "elektronik": "12:38", "urun": "16:40",
        "proje": "18:10", "reels": "20:30"},            # Cuma
    5: {"3dbaski": "11:10", "elektronik": "12:20", "urun": "16:50",
        "reels": "19:20", "proje": "20:10"},            # Cumartesi
    6: {"3dbaski": "11:40", "elektronik": "12:20", "urun": "17:10",
        "reels": "19:50", "proje": "21:00"},            # Pazar
}

HIKAYE_GECIKME = 40      # gönderiden kaç dakika sonra


def saat(g, anahtar):
    return IZGARA[g][anahtar]


def arti(hhmm, dk):
    t = datetime.strptime(hhmm, "%H:%M") + timedelta(minutes=dk)
    return t.strftime("%H:%M")


def kuyruk():
    d = json.load(open("DURUM.json", encoding="utf-8"))
    return d, d["kuyruk_bekleyen"]["slotlar"]


def gunler(slotlar):
    """Kuyruğu tarihe göre grupla, slot sırasına diz."""
    out = {}
    for s in slotlar:
        out.setdefault(s["tarih"], {})[s["slot"]] = s
    return dict(sorted(out.items()))


def kare_sayisi(klasor):
    if not os.path.isdir(klasor):
        return 0
    return len([f for f in os.listdir(klasor)
                if f[:-4].isdigit() and f.endswith(".jpg")])


def liste():
    d, slotlar = kuyruk()
    gun = gunler(slotlar)
    reelsler = {r["tarih"]: r["klasor"]
                for r in d["kuyruk_bekleyen"].get("reels", [])}

    sat = ["# YAYIN LİSTESİ",
           "",
           "Günde **4 gönderi · 4 hikaye · 1 reels**. Hikaye, gönderiden "
           "%d dakika sonra." % HIKAYE_GECIKME,
           "",
           "Bu dosya `sira.py` tarafından üretiliyor, elle düzenleme — "
           "kuyruk `DURUM.json` içinde.",
           ""]

    eksik = []
    for tarih, sl in gun.items():
        g = date.fromisoformat(tarih).weekday()
        sat += ["## %s · %s" % (tarih, GUN[g]), "",
                "| Saat | Tür | Slot | Klasör | Kare |",
                "|---|---|---|---|---|"]

        satirlar = []
        for ad in SLOTLAR:
            s = sl.get(ad)
            if not s:
                eksik.append((tarih, ad))
                satirlar.append((saat(g, ad), "— | **%s** | _boş — üretilecek_ | —"
                                 % BASLIK[ad]))
                continue
            k = s["klasor"]
            n = kare_sayisi(k)
            satirlar.append((saat(g, ad),
                             "Gönderi | %s | `%s` | %d" % (BASLIK[ad], k, n)))
            satirlar.append((arti(saat(g, ad), HIKAYE_GECIKME),
                             "Hikaye | %s | `%s/hikaye.jpg` | 1"
                             % (BASLIK[ad], k)))

        r = reelsler.get(tarih)
        if r:
            satirlar.append((saat(g, "reels"),
                             "**Reels** | — | `%s/reels.mp4` | video" % r))
        else:
            eksik.append((tarih, "reels"))
            satirlar.append((saat(g, "reels"),
                             "**Reels** | — | _boş — üretilecek_ | —"))

        for t, geri in sorted(satirlar):
            sat.append("| %s | %s |" % (t, geri))
        sat.append("")

    if eksik:
        sat += ["## Boş slotlar", "",
                "Bu slotlar için içerik henüz üretilmedi:", ""]
        for t, a in eksik:
            sat.append("- %s · %s" % (t, BASLIK.get(a, a.upper())))
        sat.append("")

    open("YAYIN-LISTESI.md", "w", encoding="utf-8").write("\n".join(sat))
    return len(gun), len(eksik)




# --------------------------------------------------------------- paket
DEPO = "https://github.com/sedatisc/instagram-gorseller/tree/main/"
HAM = "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/main/"


def metin_oku(klasor):
    """metin.md'den gönderi metnini ve ilk yorumu ayır."""
    yol = os.path.join(klasor, "metin.md")
    if not os.path.exists(yol):
        return None, None
    govde = yorum = None
    for p in re.split(r"^##\s+", open(yol, encoding="utf-8").read(), flags=re.M):
        bas = p.split("\n", 1)[0].strip().lower()
        if bas.startswith("gönderi metni"):
            govde = p.split("\n", 1)[1].strip()
        elif bas.endswith("ilk yorum"):
            yorum = p.split("\n", 1)[1].strip()
    if govde:
        govde = re.sub(r"\*\*(.+?)\*\*", r"\1", govde)   # Instagram yıldızı gösteriyor
    return govde, yorum


def kare_adlari(klasor):
    if not os.path.isdir(klasor):
        return []
    f = [x for x in os.listdir(klasor) if x.endswith(".jpg") and x[:-4].isdigit()]
    return sorted(f, key=lambda x: int(x[:-4]))


def paket():
    """Tek sayfa yayın paketi: kapak küçük resmi, klasör linki, kopyalanabilir
    metin. Kod bloğunun sağ üstünde GitHub'ın kopyala düğmesi çıkıyor."""
    d, slotlar = kuyruk()
    gun = gunler(slotlar)
    reelsler = {r["tarih"]: r["klasor"]
                for r in d["kuyruk_bekleyen"].get("reels", [])}

    sat = ["# YAYIN PAKETİ", "",
           "Her gönderinin kapağı, klasörü ve metni burada. Metin kutusunun "
           "sağ üstündeki kopyala düğmesine basıp Instagram'a yapıştır; "
           "başlığa dokununca klasör açılıyor, kareler sırayla orada.", "",
           "Hikaye gönderiden %d dakika sonra, aynı klasörde `hikaye.jpg`."
           % HIKAYE_GECIKME, "",
           "Bu dosya `sira.py` tarafından üretiliyor, elle düzenleme.", ""]

    for tarih, sl in gun.items():
        g = date.fromisoformat(tarih).weekday()
        sat += ["---", "", "# %s · %s" % (tarih, GUN[g]), ""]
        sira_ = []
        for ad in SLOTLAR:
            s = sl.get(ad)
            if s:
                sira_.append((saat(g, ad), "gonderi", s["klasor"], ad))
        r = reelsler.get(tarih)
        if r:
            sira_.append((saat(g, "reels"), "reels", r, None))
        for t, tur, kl, ad in sorted(sira_):
            if tur == "reels":
                sat += ["## %s · REELS — [%s](%s)" % (t, kl + "/reels.mp4",
                                                      DEPO + kl), "",
                        "Açıklama gönderi metniyle aynı. Trend sesi eklemek "
                        "istersen uygulamadan paylaş.", ""]
                continue
            govde, yorum = metin_oku(kl)
            kare = kare_adlari(kl)
            sat += ["## %s · %s" % (t, BASLIK[ad]), "",
                    '<a href="%s%s"><img src="%s%s/1.jpg" width="240"></a>'
                    % (DEPO, kl, HAM, kl), "",
                    "**[%s](%s)** · %d kare · hikaye %s"
                    % (kl, DEPO + kl, len(kare), arti(t, HIKAYE_GECIKME)), ""]
            if govde:
                sat += ["```", govde, "```", ""]
            else:
                sat += ["_metin.md yok_", ""]
            if yorum:
                sat += ["İlk yorum:", "", "```", yorum, "```", ""]

    open("YAYIN-PAKETI.md", "w", encoding="utf-8").write("\n".join(sat) + "\n")
    return sum(len(v) for v in gun.values())


if __name__ == "__main__":
    n, e = liste()
    paket()
    if "--eksik" in sys.argv:
        print("%d gün, %d boş slot" % (n, e))
    else:
        print("YAYIN-LISTESI.md yazıldı — %d gün, %d boş slot" % (n, e))
