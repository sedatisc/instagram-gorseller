#!/usr/bin/env python3
"""Yayın sırası — icerik.json'dan takvim türetiyor.

Eski yapıda her gönderinin elle tutulan bir gün numarası vardı. Numara
kaydıkça aynı iş iki kere planlanıyor, elle paylaşılan iş kuyrukta
kalıyor, yayıncı aksayınca o günün işi sessizce düşüyordu. Burada
gönderinin tarihi yok: durumu "hazir" olan işler kategorisindeki
sırayla günlere diziliyor, tarih konumdan çıkıyor. Bir gün kaçarsa
içerik kaybolmuyor, bir gün kayıyor.

    python3 sira.py                      # listeyi ve paketi üret
    python3 sira.py --eksik              # yalnız boş slotları say
    python3 sira.py yayinlandi <klasor> [gg.aa.yyyy]
    python3 sira.py beklet <klasor> <neden>
    python3 sira.py geri <klasor>
"""
import json
import os
import sys
from datetime import date, datetime, timedelta

GUN = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma",
       "Cumartesi", "Pazar"]

KATEGORILER = ["rehber", "baski", "magaza", "proje"]

# Günde üç gönderi var. Beş gönderi aynı gün akışta birbiriyle yarışıyordu;
# Instagram'ın kendi ölçümünde gönderiler birbirini bastırıyor ve kişi başı
# etkileşim düşüyor. İkisi baskı ürünü — satılan şey o. Üçüncü slot her gün
# sırayla rehber, mağaza ve projeye geçiyor.
GUNLUK = {"baski": 2}
DONEN = ["rehber", "magaza", "proje"]


# Günün üç gönderi slotu. Hangi kategorinin geleceği sabit değil:
# s2 ve s3 baskı ürününü tercih ediyor, s1 dönen kategoriyi; bir kuyruk
# boşalınca slot dolu kuyruktan besleniyor, gün yarım kalmıyor.
SLOTLAR = ["s1", "s2", "s3"]
TERCIH = {"s1": None, "s2": "baski", "s3": "baski"}

BASLIK = {"rehber": "AYAR & REHBER",
          "baski": "BASKI ÜRÜNLERİ",
          "baski2": "BASKI ÜRÜNLERİ",
          "magaza": "ÜRÜN & MAĞAZA",
          "proje": "PROJE & ATÖLYE",
          "kampanya": "KAMPANYA"}

# gün indeksi -> {slot: "SS:DD"}
IZGARA = {
    0: {"s1": "09:10", "s2": "12:38", "s3": "17:24", "reels": "19:40"},
    1: {"s1": "09:10", "s2": "12:38", "s3": "17:24", "reels": "19:40"},
    2: {"s1": "09:10", "s2": "12:10", "s3": "17:24", "reels": "19:40"},
    3: {"s1": "09:05", "s2": "12:38", "s3": "17:24", "reels": "19:40"},
    4: {"s1": "09:10", "s2": "12:38", "s3": "16:40", "reels": "19:20"},
    5: {"s1": "11:10", "s2": "13:20", "s3": "17:10", "reels": "19:20"},
    6: {"s1": "11:10", "s2": "13:20", "s3": "17:10", "reels": "19:50"},
}

HIKAYE_GECIKME = 40      # gönderiden kaç dakika sonra

KOK = os.path.dirname(os.path.abspath(__file__))
ICERIK = os.path.join(KOK, "icerik.json")
PLAN_DURUM = os.path.join(KOK, "otomasyon", "plan-durumu.json")
DEPO = "https://github.com/sedatisc/instagram-gorseller/tree/main/"
HAM = ("https://raw.githubusercontent.com/sedatisc/"
       "instagram-gorseller/main/")


# --------------------------------------------------------------- veri
BAGLANTI = os.path.join(KOK, "baglantilar.json")


def baglantilar():
    try:
        with open(BAGLANTI, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _konu(klasor, d=None):
    for i in (d or oku())["icerik"]:
        if i["klasor"] == klasor:
            return i.get("konu") or klasor
    return klasor


def urun_kaydi(klasor, d=None):
    b = baglantilar()
    return (b.get("urun") or {}).get(_konu(klasor, d)) or {}


def urun_gorselleri(klasor, d=None):
    """Ürünün site görselleri.

    Baskı ürünü gönderilerinde yalnız sitenin kendi görselleri
    kullanılıyor. Liste boşsa ürün yayına girmiyor; depodaki kareyle
    ya da başka bir görselle yayımlanmıyor."""
    return list(urun_kaydi(klasor, d).get("gorsel") or [])


def urun_sayfasi(klasor, d=None):
    b = baglantilar()
    return (urun_kaydi(klasor, d).get("sayfa")
            or b.get("varsayilan") or "")


def oku():
    with open(ICERIK, encoding="utf-8") as f:
        return json.load(f)


def yaz(d):
    with open(ICERIK, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)


def plan_durumu():
    try:
        with open(PLAN_DURUM, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def baslangic():
    """Planın birinci günü.

    İlk gerçek yayında takvime çivileniyor; o güne kadar "bugünden
    itibaren" gösteriliyor, böylece yayıncı kapalıyken gün kaybı olmuyor.
    Çivilenmiş tarih geçmişte kaldıysa bugüne çekiliyor: plan geriye
    doğru uzayıp boş günler üretmesin."""
    s = plan_durumu().get("baslangic")
    bug = date.today()
    if s:
        t = date.fromisoformat(s)
        if t >= bug:
            return t
    # Günün ilk gönderi saati geçtiyse plan yarından başlıyor: yarım
    # günle başlayıp o günün işlerinin çoğunu yayınlanmadan geçirmesin.
    ilk = min(IZGARA[bug.weekday()].values())
    return bug if datetime.now().strftime("%H:%M") < ilk else bug + timedelta(1)


# ------------------------------------------------------------ takvim
def hazirlar(d=None):
    """Kategorisine göre, sırasıyla, plana girecek işler.

    Aynı konunun ikinci klasörü atlanıyor: aynı ürün iki ayrı gönderi
    olarak kuyrukta durabiliyordu. Yayınlanmış bir konu da plana
    girmiyor; aynı iş ikinci kez paylaşılmasın diye kuyruk, yayınlanan
    konuların listesiyle başlıyor."""
    d = d or oku()
    out = {k: [] for k in KATEGORILER}
    gorulen = {i.get("konu") or i["klasor"] for i in d["icerik"]
               if i.get("durum") == "yayinlandi"}
    for i in d["icerik"]:
        if i.get("durum") != "hazir" or i.get("kategori") not in out:
            continue
        konu = i.get("konu") or i["klasor"]
        if i["kategori"] == "baski" and not urun_gorselleri(i["klasor"], d):
            print("SİTE GÖRSELİ YOK: %s — plana girmiyor" % i["klasor"])
            continue
        if konu in gorulen:
            print("ATLANDI (aynı konu): %s" % i["klasor"])
            continue
        gorulen.add(konu)
        out[i["kategori"]].append(i)
    return out


def kuyruk():
    """(uyumluluk sözlüğü, slot listesi).

    yayinla.py bu biçimi bekliyor: her kayıtta klasor, slot, tarih."""
    d = oku()
    bas = baslangic()
    kuy = {k: list(v) for k, v in hazirlar(d).items()}
    slotlar, g, don = [], 0, 0

    def cek(kat, video_dolu):
        """Kuyruğun başı. Günde tek reels var: o gün video dolduysa
        kuyruktaki ilk videosuz iş öne alınıyor, video kaybolmuyor."""
        lst = kuy.get(kat)
        if not lst:
            return None
        n = 0
        if video_dolu and lst[0].get("reels"):
            n = next((j for j, x in enumerate(lst)
                      if not x.get("reels")), 0)
        return lst.pop(n)

    def sirayla():
        """Dönen kategorilerden sırası gelen ve dolu olan."""
        nonlocal don
        for _ in range(len(DONEN)):
            kat = DONEN[don % len(DONEN)]
            don += 1
            if kuy.get(kat):
                return kat
        return None

    while any(kuy.values()) and g < 400:
        video_dolu = False
        for slot in SLOTLAR:
            kat = TERCIH[slot]
            if not kat or not kuy.get(kat):
                kat = sirayla()
                if kat is None and kuy.get("baski"):
                    kat = "baski"
            if kat is None:
                continue
            kayit = cek(kat, video_dolu)
            if kayit is None:
                continue
            if kayit.get("reels"):
                video_dolu = True
            slotlar.append({"klasor": kayit["klasor"], "slot": slot,
                            "kategori": kat, "gun": g,
                            "tarih": (bas + timedelta(days=g)).isoformat()})
        g += 1
    uyum = {"kuyruk_bekleyen": {"beklemede": [
        {"klasor": i["klasor"]} for i in d["icerik"]
        if i.get("durum") in ("beklemede", "iptal")]}}
    return uyum, sorted(slotlar, key=lambda s: (s["tarih"], s["slot"]))


def kampanyalar():
    """Kampanya takvimi.

    İki tür var. Çekiliş gibi işler plana göre kayıyor: "gun" alanı
    başlangıçtan kaç gün sonra olduğunu söylüyor. Bayram gibi işler
    kaymıyor; onların "tarih" alanı var ve o gün geçtiyse iş plandan
    düşüyor — 29 Ekim 30 Ekim'de yayımlanmaz."""
    d = oku()
    bas = baslangic()
    bug = date.today().isoformat()
    hazir = {i["klasor"] for i in d["icerik"] if i.get("durum") == "hazir"}
    out = []
    for k in d.get("kampanya", []):
        if k["klasor"] not in hazir:
            continue
        x = dict(k)
        if k.get("tarih"):
            if k["tarih"] < bug:
                continue
            x["tarih"] = k["tarih"]
        else:
            x["tarih"] = (bas + timedelta(days=int(k.get("gun", 0)))).isoformat()
        out.append(x)
    return out


def reelsler(slotlar=None):
    """Reels takvimi; video konusunun gönderisiyle aynı güne biniyor.

    Ayrı güne atılsa aynı konu iki güne yayılıyor, listede de akışta da
    tekrar gibi duruyordu. Gönderisinin günü başka bir videoyla doluysa
    video sonraki boş güne kayıyor: günde tek reels var ama video da
    kaybolmuyor. Reels, takipçi olmayana ulaşan tek biçim — birini
    boşa harcamıyoruz."""
    d = oku()
    if slotlar is None:
        _, slotlar = kuyruk()
    gun = {s["klasor"]: s["tarih"] for s in slotlar}
    out = {}
    for i in d["icerik"]:
        if not i.get("reels") or i.get("durum") != "hazir":
            continue
        t = gun.get(i["klasor"])
        if t is None:
            continue
        if t in out:
            gun_t = date.fromisoformat(t)
            for k in range(1, 15):
                yeni = (gun_t + timedelta(days=k)).isoformat()
                if yeni not in out:
                    print("REELS KAYDI: %s — %s dolu, %s gününe"
                          % (i["klasor"], t, yeni))
                    out[yeni] = i["klasor"]
                    break
            else:
                print("BEKLEYEN REELS: %s — boş gün bulunamadı" % i["klasor"])
            continue
        out[t] = i["klasor"]
    return out


def gunler(slotlar):
    out = {}
    for s in slotlar:
        out.setdefault(s["tarih"], {})[s["slot"]] = s
    return dict(sorted(out.items()))


def saat(g, slot):
    return IZGARA[g][slot]


def arti(hhmm, dk):
    t = datetime.strptime(hhmm, "%H:%M") + timedelta(minutes=dk)
    return t.strftime("%H:%M")


# ------------------------------------------------------------ yardımcı
def kare_adlari(klasor):
    yol = os.path.join(KOK, klasor)
    if not os.path.isdir(yol):
        return []
    return sorted((f for f in os.listdir(yol)
                   if f[:-4].isdigit() and f.endswith(".jpg")),
                  key=lambda f: int(f[:-4]))


def metin_oku(klasor):
    """(gönderi metni, ilk yorum)."""
    yol = os.path.join(KOK, klasor, "metin.md")
    if not os.path.exists(yol):
        return "", ""
    ham = open(yol, encoding="utf-8").read()
    govde, yorum, hedef = [], [], None
    for satir in ham.splitlines():
        if satir.startswith("## "):
            b = satir[3:].strip().lower()
            hedef = govde if b.startswith("gönderi") else (
                yorum if b.startswith("ilk yorum") else None)
            continue
        if hedef is not None:
            hedef.append(satir)
    return "\n".join(govde).strip(), "\n".join(yorum).strip()


# ------------------------------------------------------------- liste
def liste():
    d = oku()
    _, slotlar = kuyruk()
    gun = gunler(slotlar)
    kamp = kampanyalar()
    reels = reelsler(slotlar)
    yayinlanan = {}
    for i in d["icerik"]:
        if i.get("durum") == "yayinlandi" and i.get("tarih"):
            yayinlanan.setdefault(i["tarih"], []).append(i)

    sat = ["# YAYIN LİSTESİ", "",
           "Günde **3 gönderi · 3 hikaye · 1 reels**. Hikaye, gönderiden "
           "%d dakika sonra." % HIKAYE_GECIKME, "",
           "Bu dosya `sira.py` tarafından üretiliyor, elle düzenleme — "
           "içerik `icerik.json` içinde.", ""]

    eksik = []
    for tarih, sl in gun.items():
        g = date.fromisoformat(tarih).weekday()
        sat += ["## %s · %s" % (tarih, GUN[g]), "",
                "| Saat | Tür | Slot | Klasör | Kare |", "|---|---|---|---|---|"]
        satirlar = []
        for ad in SLOTLAR:
            s = sl.get(ad)
            if not s:
                y = yayinlanan.get(tarih, [])
                if y:
                    satirlar.append((saat(g, ad), "Yayınlandı | %s | `%s` | —"
                                     % (BASLIK.get(y[0].get("kategori"), "—"),
                                        y[0]["klasor"])))
                    continue
                eksik.append((tarih, ad))
                satirlar.append((saat(g, ad),
                                 "— | **boş** | _boş — üretilecek_ | —"))
                continue
            kare = len(kare_adlari(s["klasor"]))
            satirlar.append((saat(g, ad), "Gönderi | %s | `%s` | %d"
                             % (BASLIK[s["kategori"]], s["klasor"], kare)))
            satirlar.append((arti(saat(g, ad), HIKAYE_GECIKME),
                             "Hikaye | %s | `%s/hikaye.jpg` | 1"
                             % (BASLIK[s["kategori"]], s["klasor"])))
        for k in kamp:
            if k["tarih"] != tarih:
                continue
            tur = k.get("tur", "gonderi")
            ad = "**Kampanya**" if tur == "gonderi" else "Kampanya hikaye"
            dosya = (k["klasor"] if tur == "gonderi"
                     else "%s/hikaye.jpg" % k["klasor"])
            satirlar.append((k["saat"], "%s | — | `%s` | %s"
                             % (ad, dosya, len(kare_adlari(k["klasor"]))
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
        sat += ["| %s | %s |" % (t, g2) for t, g2 in sorted(satirlar)] + [""]

    if eksik:
        sat += ["## Boş slotlar", "",
                "Bu slotlar için içerik henüz üretilmedi:", ""]
        sat += ["- %s · %s" % (t, BASLIK.get(a, a.upper())) for t, a in eksik]
        sat += [""]

    with open(os.path.join(KOK, "YAYIN-LISTESI.md"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(sat) + "\n")
    return len(gun), len(eksik)


# ------------------------------------------------------------- paket
def paket():
    """Tek sayfa yayın paketi: kapak küçük resmi, klasör linki, metin."""
    _, slotlar = kuyruk()
    gun = gunler(slotlar)
    reels = reelsler(slotlar)

    sat = ["# YAYIN PAKETİ", "",
           "Her gönderinin kapağı, klasörü ve metni burada. Metin kutusunun "
           "sağ üstündeki kopyala düğmesine basıp Instagram'a yapıştır; "
           "başlığa dokununca klasör açılıyor.", "",
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
                sira_.append((saat(g, ad), "gonderi", s["klasor"],
                              s["kategori"]))
        r = reels.get(tarih)
        if r:
            sira_.append((saat(g, "reels"), "reels", r, None))
        for t, tur, kl, ad in sorted(sira_):
            if tur == "reels":
                sat += ["## %s · REELS — [%s](%s)"
                        % (t, kl + "/reels.mp4", DEPO + kl), "",
                        "Açıklama gönderi metniyle aynı.", ""]
                continue
            govde, yorum = metin_oku(kl)
            kare = kare_adlari(kl)
            sat += ["## %s · %s" % (t, BASLIK.get(ad, ad)), "",
                    '<a href="%s%s"><img src="%s%s/1.jpg" width="240"></a>'
                    % (DEPO, kl, HAM, kl), "",
                    "**[%s](%s)** · %d kare · hikaye %s"
                    % (kl, DEPO + kl, len(kare), arti(t, HIKAYE_GECIKME)), ""]
            sat += (["```", govde, "```", ""] if govde
                    else ["_metin.md yok_", ""])
            if yorum:
                sat += ["İlk yorum:", "", "```", yorum, "```", ""]

    with open(os.path.join(KOK, "YAYIN-PAKETI.md"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(sat) + "\n")
    return sum(len(v) for v in gun.values())


# ------------------------------------------------------------ komutlar
def _bul(d, klasor):
    for i in d["icerik"]:
        if i["klasor"] == klasor:
            return i
    raise SystemExit("icerik.json'da yok: %s" % klasor)


def komut_yayinlandi(klasor, tarih=None):
    d = oku()
    i = _bul(d, klasor)
    i["durum"] = "yayinlandi"
    i["tarih"] = tarih or date.today().isoformat()
    i.pop("neden", None)
    yaz(d)
    print("yayınlandı: %s · %s" % (klasor, i["tarih"]))


def komut_beklet(klasor, neden):
    d = oku()
    i = _bul(d, klasor)
    i["durum"] = "beklemede"
    i["neden"] = neden
    yaz(d)
    print("beklemede: %s — %s" % (klasor, neden))


def komut_geri(klasor):
    d = oku()
    i = _bul(d, klasor)
    i["durum"] = "hazir"
    i.pop("neden", None)
    i.pop("tarih", None)
    yaz(d)
    print("plana alındı: %s" % klasor)


def main():
    a = sys.argv[1:]
    if a and a[0] == "yayinlandi":
        return komut_yayinlandi(*a[1:3])
    if a and a[0] == "beklet":
        return komut_beklet(a[1], " ".join(a[2:]) or "—")
    if a and a[0] == "geri":
        return komut_geri(a[1])

    n, e = liste()
    paket()
    try:
        import paket as _p
        _p.main()
    except Exception as _e:
        print("yayin-paketi.html üretilemedi:", _e)
    print("YAYIN-LISTESI.md yazıldı — %d gün, %d boş slot" % (n, e))


if __name__ == "__main__":
    main()
