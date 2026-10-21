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
SLOTLAR = ["3dbaski", "baski", "urun", "proje"]

BASLIK = {"3dbaski": "AYAR & REHBER",
          "baski": "BASKI ÜRÜNLERİ",
          # Elektronik kategorisi kapandı (sitede satılmıyor); anahtar
          # eski kuyruk satırları okunabilsin diye duruyor.
          "elektronik": "ELEKTRONİK (kapandı)",
          "urun": "ÜRÜN & MAĞAZA",
          "proje": "PROJE & ATÖLYE"}

# gün indeksi -> {slot: "SS:DD"} + "reels"
IZGARA = {
    0: {"3dbaski": "08:12", "elektronik": "12:38",
        "baski": "12:38", "urun": "17:24",
        "proje": "19:40", "reels": "21:10"},            # Pazartesi
    1: {"3dbaski": "08:12", "elektronik": "12:38",
        "baski": "12:38", "urun": "17:24",
        "reels": "19:36", "proje": "20:42"},            # Salı
    2: {"3dbaski": "08:12", "elektronik": "12:38",
        "baski": "12:38", "urun": "17:24",
        "reels": "19:36", "proje": "20:42"},            # Çarşamba
    3: {"3dbaski": "08:12", "elektronik": "12:38",
        "baski": "12:38", "urun": "17:24",
        "reels": "19:36", "proje": "20:42"},            # Perşembe
    4: {"3dbaski": "08:12", "elektronik": "12:38",
        "baski": "12:38", "urun": "16:40",
        "proje": "18:10", "reels": "20:30"},            # Cuma
    5: {"3dbaski": "11:10", "elektronik": "12:20",
        "baski": "12:20", "urun": "16:50",
        "reels": "19:20", "proje": "20:10"},            # Cumartesi
    6: {"3dbaski": "11:40", "elektronik": "12:20",
        "baski": "12:20", "urun": "17:10",
        "reels": "19:50", "proje": "21:00"},            # Pazar
}

HIKAYE_GECIKME = 40      # gönderiden kaç dakika sonra

KOK = os.path.dirname(os.path.abspath(__file__))
DURUM = os.path.join(KOK, "DURUM.json")
PLAN_DURUM = os.path.join(KOK, "otomasyon", "plan-durumu.json")


def saat(g, anahtar):
    return IZGARA[g][anahtar]


def arti(hhmm, dk):
    t = datetime.strptime(hhmm, "%H:%M") + timedelta(minutes=dk)
    return t.strftime("%H:%M")


# ----------------------------------------------------- planın takvimi
def plan_durumu():
    try:
        with open(PLAN_DURUM, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"baslangic": None, "kacirilan": []}


def baslangic():
    """Planın birinci gününün takvim tarihi.

    Plan eskiden sabit tarihlere çivilenmişti: yayıncı kapalı olduğu her
    gün o günün dört gönderisi "vakti geçmiş" diye siliniyordu, altı gün
    böyle kayboldu. Artık kuyrukta tarih değil gün sırası (0, 1, 2...)
    duruyor; takvime oturması ilk gerçek yayında oluyor.

    Henüz oturmadıysa plan bugünden başlıyor gibi gösteriliyor — bugünün
    ilk slotu geçtiyse yarından, yarım günle başlamasın diye."""
    s = plan_durumu().get("baslangic")
    if s:
        return date.fromisoformat(s)
    bug = date.today()
    izg = IZGARA[bug.weekday()]
    ilk = min(izg[a] for a in SLOTLAR if a in izg)
    return bug if datetime.now().strftime("%H:%M") < ilk \
        else bug + timedelta(days=1)


def _tarihle(kayit, bas):
    """Kayda takvim tarihini yazıyor. Eski kayıtlarda tarih hazır."""
    k = dict(kayit)
    if "gun" in k:
        k["tarih"] = (bas + timedelta(days=int(k["gun"]))).isoformat()
    return k


def _kacirilani_kaydir(slotlar, bas):
    """Cron aksayınca atlanan gönderi planın sonuna taşınıyor.

    İş kuyrukta duruyor ama günü geçtiği için bir daha hiç yayınlanmıyor,
    içerik sessizce düşüyordu. Taşıma bir kere oluyor: günü hâlâ ileride
    olan kayda dokunulmuyor."""
    kac = {k.get("klasor") for k in (plan_durumu().get("kacirilan") or [])}
    if not kac:
        return slotlar
    bugun = date.today()
    sl = [dict(s) for s in slotlar]
    son = max((int(s.get("gun", 0)) for s in sl), default=0)
    dolu = {(int(s.get("gun", 0)), s["slot"]) for s in sl}
    for s in sl:
        if s["klasor"] not in kac:
            continue
        if bas + timedelta(days=int(s.get("gun", 0))) >= bugun:
            continue                      # günü gelmemiş, taşımaya gerek yok
        dolu.discard((int(s["gun"]), s["slot"]))
        g = son + 1
        while (g, s["slot"]) in dolu:
            g += 1
        dolu.add((g, s["slot"]))
        s["gun"] = g
        s["not"] = "kaçırıldı, sona alındı"
    return sl


def kuyruk():
    with open(DURUM, encoding="utf-8") as f:
        d = json.load(f)
    bas = baslangic()
    sl = _kacirilani_kaydir(d["kuyruk_bekleyen"]["slotlar"], bas)
    return d, [_tarihle(s, bas) for s in sl]


def reelsler(slotlar=None):
    """Reels takvimi. Reels, kendi klasörünün gönderisiyle aynı güne
    biniyor.

    Eskiden reels'in kendi gün sırası vardı: aynı ürün bir gün reels,
    üç gün sonra gönderi olarak çıkıyordu. Listede aynı başlık üç kere
    görünüyor, takipçiye de aynı şey tekrar tekrar gidiyordu. Artık bir
    konu tek güne toplanıyor: gönderi, hikayesi ve videosu aynı gün."""
    with open(DURUM, encoding="utf-8") as f:
        d = json.load(f)
    bas = baslangic()
    gonderi_gunu = {s["klasor"]: s["tarih"] for s in (slotlar or [])}
    gunluk = sorted({s["tarih"] for s in (slotlar or [])})
    out = {}
    bekleyen = []
    for r in (_tarihle(x, bas) for x in d["kuyruk_bekleyen"].get("reels", [])):
        # Video bir klasörde, o konunun gönderisi başka klasörde
        # olabiliyor; "gun_klasor" hangi gönderiye bineceğini söylüyor.
        hedef = r.get("gun_klasor", r["klasor"])
        t = gonderi_gunu.get(hedef, r["tarih"])
        if t in out:
            bekleyen.append(r["klasor"])    # o güne zaten reels düştü
        else:
            out[t] = r["klasor"]
    # Günde tek reels var. Gönderisinin gününe sığmayan video başka bir
    # güne atılmıyor: atılırsa aynı konu iki ayrı güne yayılıyor, listede
    # de akışta da tekrar gibi duruyor. Bekliyor, gün açılınca giriyor.
    for kl in bekleyen:
        if kl not in gonderi_gunu:          # gönderisi yok, tekrar riski de yok
            for t in gunluk:
                if t not in out:
                    out[t] = kl
                    break
        else:
            print("BEKLEYEN REELS: %s — gönderi günü (%s) dolu"
                  % (kl, gonderi_gunu[kl]))
    return out


def tekrar_uyarisi(slotlar, reels):
    """Aynı klasör birden çok gönderi slotuna düşmüş mü, bakıyor."""
    sayac = {}
    for s in slotlar:
        sayac.setdefault(s["klasor"], []).append(s["tarih"])
    return {k: t for k, t in sayac.items() if len(t) > 1}


def kampanyalar():
    """Izgara dışı kampanya gönderileri — çekiliş, duyuru, kutlama."""
    with open(DURUM, encoding="utf-8") as f:
        d = json.load(f)
    bas = baslangic()
    return [_tarihle(k, bas)
            for k in d["kuyruk_bekleyen"].get("kampanya", [])]


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
    kamp = kampanyalar()
    reels = reelsler(slotlar)
    for k, t in tekrar_uyarisi(slotlar, reels).items():
        print("UYARI: %s %d kere planlanmış (%s)" % (k, len(t), ", ".join(t)))

    sat = ["# YAYIN LİSTESİ",
           "",
           "Günde **4 gönderi · 4 hikaye · 1 reels**. Hikaye, gönderiden "
           "%d dakika sonra." % HIKAYE_GECIKME,
           "",
           "Bu dosya `sira.py` tarafından üretiliyor, elle düzenleme — "
           "kuyruk `DURUM.json` içinde.",
           ""]

    yayinlanan = {(x.get("tarih"), x.get("slot")): x.get("klasor")
                  for x in d.get("gecmis", []) if x.get("klasor")}

    eksik = []
    for tarih, sl in gun.items():
        g = date.fromisoformat(tarih).weekday()
        sat += ["## %s · %s" % (tarih, GUN[g]), "",
                "| Saat | Tür | Slot | Klasör | Kare |",
                "|---|---|---|---|---|"]

        # Kuyruktaki eski slot adları (elektronik) da listelensin; yoksa
        # geçmiş günlerin gönderileri listeden düşüyor.
        slot_adlari = SLOTLAR + [a for a in sl if a not in SLOTLAR]
        satirlar = []
        for ad in slot_adlari:
            s = sl.get(ad)
            if not s:
                if tarih < date.today().isoformat():
                    continue          # geçmiş gün; boş slot aranmıyor
                # Elle paylaşılan gönderi kuyruktan düşüyor, slot da boş
                # görünüyordu: "üretilecek" diye duran satır aslında o
                # gün yayınlanmış işti.
                y = yayinlanan.get((tarih, ad))
                if y:
                    satirlar.append((saat(g, ad),
                                     "Yayınlandı | %s | `%s` | —"
                                     % (BASLIK[ad], y)))
                    continue
                eksik.append((tarih, ad))
                satirlar.append((saat(g, ad),
                                 "— | **%s** | _boş — üretilecek_ | —"
                                 % BASLIK[ad]))
                continue
            k = s["klasor"]
            n = kare_sayisi(k)
            satirlar.append((saat(g, ad),
                             "Gönderi | %s | `%s` | %d" % (BASLIK[ad], k, n)))
            satirlar.append((arti(saat(g, ad), HIKAYE_GECIKME),
                             "Hikaye | %s | `%s/hikaye.jpg` | 1"
                             % (BASLIK[ad], k)))

        # Aynı saati eski slot adı doldurduysa boş satır tekrar olmasın
        dolu = {t for t, g2 in satirlar if "boş" not in g2}
        satirlar = [(t, g2) for t, g2 in satirlar
                    if "boş" not in g2 or t not in dolu]

        for k in kamp:
            if k["tarih"] != tarih:
                continue
            tur = k.get("tur", "gonderi")
            ad = "**Kampanya**" if tur == "gonderi" else "Kampanya hikaye"
            dosya = k["klasor"] if tur == "gonderi" \
                else "%s/hikaye.jpg" % k["klasor"]
            satirlar.append((k["saat"], "%s | — | `%s` | %s"
                             % (ad, dosya, kare_sayisi(k["klasor"])
                                if tur == "gonderi" else 1)))
            if tur == "gonderi":
                satirlar.append((arti(k["saat"], HIKAYE_GECIKME),
                                 "Kampanya hikaye | — | `%s/hikaye.jpg` | 1"
                                 % k["klasor"]))

        r = reels.get(tarih)
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
    reels = reelsler(slotlar)

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
        r = reels.get(tarih)
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
    try:                                   # artifact sayfası
        import paket as _p
        _p.main()
    except Exception as _e:                # sayfa olmasa da liste üretilsin
        print("yayin-paketi.html üretilemedi:", _e)
    if "--eksik" in sys.argv:
        print("%d gün, %d boş slot" % (n, e))
    else:
        print("YAYIN-LISTESI.md yazıldı — %d gün, %d boş slot" % (n, e))
