#!/usr/bin/env python3
"""Instagram'a otomatik yayın — GitHub Actions üzerinde çalışır.

Kuyruk `DURUM.json`, saat ızgarası `sira.py` içinde. Bu betik her çalışmada
"vakti gelmiş ve henüz yayınlanmamış" ne varsa yayınlar: karusel gönderi,
hikaye, reels. Yayınlananlar `otomasyon/yayinlanan.json` defterine yazılır,
aynı şey iki kez gitmez.

Görseller depodan servis ediliyor: Graph API `image_url`/`video_url` alanına
herkese açık adres istiyor, raw.githubusercontent.com bunu karşılıyor.
Ayrı bir barındırma gerekmiyor.

    python3 otomasyon/yayinla.py --kuru     # hiçbir şey yayınlamaz, ne
                                            # yapacağını ve adresleri yazar
    python3 otomasyon/yayinla.py            # vakti geleni yayınlar
    python3 otomasyon/yayinla.py --zorla 2026-10-11|3dbaski|gonderi

Ortam değişkenleri (GitHub Actions secret olarak):
    IG_USER_ID   Instagram işletme hesabının kimliği (sayı)
    IG_TOKEN     uzun ömürlü Facebook sayfa erişim anahtarı
    GRAPH_SURUM  isteğe bağlı, varsayılan v23.0
"""
import json
import os
import re
import sys
import time
from datetime import date, datetime, timedelta

import requests

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
import sira                                              # noqa: E402

DEFTER = os.path.join(KOK, "otomasyon", "yayinlanan.json")
RAPOR = os.path.join(KOK, "otomasyon", "SON-YAYIN.md")

DEPO = "sedatisc/instagram-gorseller"
SURUM = os.environ.get("GRAPH_SURUM", "v23.0")
UC = "https://graph.facebook.com/%s" % SURUM

# Vakti çok geçmiş işi yayınlamıyoruz: Actions cron'u aksarsa ya da bir
# çalışma atlanırsa, akşam üstü sabahın gönderisini atmak akışı bozuyor.
GECIKME_SINIRI = timedelta(hours=3)


# ----------------------------------------------------------------- yardım
def ham(yol, surum=None):
    """Depodaki dosyanın herkese açık adresi."""
    ref = surum or os.environ.get("GITHUB_SHA") or "main"
    return "https://raw.githubusercontent.com/%s/%s/%s" % (DEPO, ref, yol)


def defter_oku():
    if os.path.exists(DEFTER):
        try:
            return json.load(open(DEFTER, encoding="utf-8"))
        except Exception:
            pass
    return {"yayinlanan": []}


def defter_yaz(d):
    json.dump(d, open(DEFTER, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


def metin_oku(klasor):
    """metin.md'den gönderi metnini ve ilk yorumu ayır."""
    yol = os.path.join(KOK, klasor, "metin.md")
    if not os.path.exists(yol):
        return None, None
    s = open(yol, encoding="utf-8").read()
    parca = re.split(r"^##\s+", s, flags=re.M)
    govde, yorum = None, None
    for p in parca:
        if p.lower().startswith("gönderi metni"):
            govde = p.split("\n", 1)[1].strip()
        elif p.lower().startswith("i̇lk yorum") or p.lower().startswith("ilk yorum"):
            yorum = p.split("\n", 1)[1].strip()
    # Markdown kalınlığı Instagram'da yıldız olarak görünüyor, temizle.
    if govde:
        govde = re.sub(r"\*\*(.+?)\*\*", r"\1", govde)
    return govde, yorum


def kareler(klasor):
    d = os.path.join(KOK, klasor)
    if not os.path.isdir(d):
        return []
    n = sorted(f for f in os.listdir(d)
               if f.endswith(".jpg") and f[:-4].isdigit())
    return ["%s/%s" % (klasor, f) for f in sorted(n, key=lambda f: int(f[:-4]))]


# ----------------------------------------------------------------- gündem
def gundem():
    """Kuyruktan (tarih, saat, tür, klasör) listesi çıkar."""
    d = json.load(open(os.path.join(KOK, "DURUM.json"), encoding="utf-8"))
    kb = d["kuyruk_bekleyen"]
    bekle = {b["klasor"] for b in kb.get("beklemede", [])}
    reelsler = {r["tarih"]: r["klasor"] for r in kb.get("reels", [])}
    isler = []
    for s in kb.get("slotlar", []):
        if s["klasor"] in bekle:
            continue
        g = date.fromisoformat(s["tarih"]).weekday()
        hhmm = sira.IZGARA[g][s["slot"]]
        isler.append({"anahtar": "%s|%s|gonderi" % (s["tarih"], s["slot"]),
                      "zaman": "%sT%s" % (s["tarih"], hhmm),
                      "tur": "gonderi", "klasor": s["klasor"]})
        isler.append({"anahtar": "%s|%s|hikaye" % (s["tarih"], s["slot"]),
                      "zaman": "%sT%s" % (s["tarih"],
                                          sira.arti(hhmm, sira.HIKAYE_GECIKME)),
                      "tur": "hikaye", "klasor": s["klasor"]})
    for tarih, klasor in reelsler.items():
        if klasor in bekle:
            continue
        g = date.fromisoformat(tarih).weekday()
        isler.append({"anahtar": "%s|reels" % tarih,
                      "zaman": "%sT%s" % (tarih, sira.IZGARA[g]["reels"]),
                      "tur": "reels", "klasor": klasor})
    return sorted(isler, key=lambda i: i["zaman"])


def simdi():
    """Europe/Istanbul yerel saati. Koşucu UTC çalışıyor."""
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Istanbul")).replace(tzinfo=None)
    except Exception:
        return datetime.utcnow() + timedelta(hours=3)


# -------------------------------------------------------------- Graph API
class Hata(Exception):
    pass


def _cagir(yol, veri=None, al=False):
    kimlik = os.environ["IG_USER_ID"]
    anahtar = os.environ["IG_TOKEN"]
    url = "%s/%s" % (UC, yol.replace("<ig>", kimlik))
    for deneme in range(3):
        try:
            if al:
                r = requests.get(url, params=dict(veri or {},
                                                  access_token=anahtar),
                                 timeout=60)
            else:
                r = requests.post(url, data=dict(veri or {},
                                                 access_token=anahtar),
                                  timeout=120)
            g = r.json()
            if r.status_code >= 400:
                m = g.get("error", {})
                # Geçici hatada tekrar dene; kalıcı hatada hemen bırak.
                if m.get("is_transient") and deneme < 2:
                    time.sleep(5 + 10 * deneme)
                    continue
                raise Hata("%s · %s (kod %s/%s)"
                           % (yol, m.get("message", g), m.get("code"),
                              m.get("error_subcode")))
            return g
        except requests.RequestException as e:
            if deneme == 2:
                raise Hata("%s · ağ: %s" % (yol, e))
            time.sleep(5 + 10 * deneme)


def kota():
    g = _cagir("<ig>/content_publishing_limit",
               {"fields": "quota_usage,config"}, al=True)
    v = (g.get("data") or [{}])[0]
    return v.get("quota_usage", 0), (v.get("config") or {}).get("quota_total", 50)


def kap_bekle(kap, azami=300):
    """Reels kabı işlenene kadar bekle. Video hemen hazır olmuyor."""
    gecen = 0
    while gecen < azami:
        g = _cagir(kap, {"fields": "status_code,status"}, al=True)
        kod = g.get("status_code")
        if kod == "FINISHED":
            return
        if kod in ("ERROR", "EXPIRED"):
            raise Hata("kap %s: %s · %s" % (kap, kod, g.get("status")))
        time.sleep(10)
        gecen += 10
    raise Hata("kap %s 5 dakikada hazır olmadı" % kap)


def yayinla_kap(kap):
    g = _cagir("<ig>/media_publish", {"creation_id": kap})
    return g["id"]


def ilk_yorum(medya, metin):
    """İzin yoksa sessizce geç — gönderi yayınlandı, yorum ikincil."""
    try:
        _cagir("%s/comments" % medya, {"message": metin})
        return True
    except Hata as e:
        print("   ilk yorum yazılamadı (izin gerekebilir): %s" % e)
        return False


# ------------------------------------------------------------------ işler
def is_gonderi(is_, kuru):
    kare = kareler(is_["klasor"])
    if not kare:
        raise Hata("%s içinde .jpg kare yok" % is_["klasor"])
    govde, yorum = metin_oku(is_["klasor"])
    if not govde:
        raise Hata("%s/metin.md yok ya da 'Gönderi metni' bölümü boş"
                   % is_["klasor"])
    adres = [ham(k) for k in kare]
    if kuru:
        print("   %d kare · metin %d karakter · ilk yorum %s"
              % (len(adres), len(govde), "var" if yorum else "yok"))
        for a in adres:
            print("     " + a)
        return None
    if len(adres) == 1:
        kap = _cagir("<ig>/media", {"image_url": adres[0], "caption": govde})["id"]
    else:
        cocuk = []
        for a in adres:
            cocuk.append(_cagir("<ig>/media",
                                {"image_url": a, "is_carousel_item": "true"})["id"])
        kap = _cagir("<ig>/media", {"media_type": "CAROUSEL",
                                    "children": ",".join(cocuk),
                                    "caption": govde})["id"]
    medya = yayinla_kap(kap)
    if yorum:
        ilk_yorum(medya, yorum)
    return medya


def is_hikaye(is_, kuru):
    yol = "%s/hikaye.jpg" % is_["klasor"]
    if not os.path.exists(os.path.join(KOK, yol)):
        raise Hata("%s yok" % yol)
    if kuru:
        print("   " + ham(yol))
        return None
    kap = _cagir("<ig>/media", {"image_url": ham(yol),
                                "media_type": "STORIES"})["id"]
    return yayinla_kap(kap)


def is_reels(is_, kuru):
    yol = "%s/reels.mp4" % is_["klasor"]
    tam = os.path.join(KOK, yol)
    if not os.path.exists(tam):
        raise Hata("%s yok" % yol)
    govde, _ = metin_oku(is_["klasor"])
    if kuru:
        print("   %s · %.1f MB" % (ham(yol), os.path.getsize(tam) / 1048576.0))
        return None
    kap = _cagir("<ig>/media", {"media_type": "REELS", "video_url": ham(yol),
                                "caption": (govde or "")[:2200],
                                "share_to_feed": "true"})["id"]
    kap_bekle(kap)
    return yayinla_kap(kap)


YAPICI = {"gonderi": is_gonderi, "hikaye": is_hikaye, "reels": is_reels}


# --------------------------------------------------------------- ana akış
def main():
    kuru = "--kuru" in sys.argv
    zorla = None
    if "--zorla" in sys.argv:
        zorla = sys.argv[sys.argv.index("--zorla") + 1]

    if not kuru and not (os.environ.get("IG_USER_ID")
                         and os.environ.get("IG_TOKEN")):
        print("IG_USER_ID / IG_TOKEN yok — yayın yapılamaz. "
              "Deneme için: python3 otomasyon/yayinla.py --kuru")
        return 1

    d = defter_oku()
    yapilan = {y["anahtar"] for y in d["yayinlanan"]}
    an = simdi()
    satir, basari, hata = [], 0, 0

    if not kuru:
        try:
            kullanim, toplam = kota()
            print("Meta kotası: %s/%s (24 saat)" % (kullanim, toplam))
            if kullanim >= toplam:
                print("Kota dolu, bu çalışma atlanıyor.")
                return 0
        except Hata as e:
            print("kota okunamadı: %s" % e)

    for is_ in gundem():
        ad = is_["anahtar"]
        if ad in yapilan:
            continue
        if zorla:
            if ad != zorla:
                continue
        else:
            t = datetime.fromisoformat(is_["zaman"])
            if t > an:
                continue
            if an - t > GECIKME_SINIRI:
                satir.append("| %s | atlandı | vakti %s, %s geçmiş |"
                             % (ad, is_["zaman"], str(an - t).split(".")[0]))
                continue
        print("→ %s · %s · %s" % (ad, is_["tur"], is_["klasor"]))
        try:
            medya = YAPICI[is_["tur"]](is_, kuru)
            if kuru:
                satir.append("| %s | kuru | %s |" % (ad, is_["klasor"]))
                continue
            d["yayinlanan"].append({"anahtar": ad, "medya": medya,
                                    "klasor": is_["klasor"],
                                    "zaman": an.strftime("%Y-%m-%d %H:%M")})
            defter_yaz(d)                      # her adımda yaz, çakılırsa kalsın
            satir.append("| %s | tamam | medya %s |" % (ad, medya))
            basari += 1
        except Hata as e:
            print("   HATA: %s" % e)
            satir.append("| %s | HATA | %s |" % (ad, str(e)[:160]))
            hata += 1

    if not satir:
        satir.append("| — | boş | vakti gelmiş yeni iş yok |")
    with open(RAPOR, "w", encoding="utf-8") as f:
        f.write("# Son yayın\n\n%s%s · %d yayın · %d hata\n\n"
                % (an.strftime("%Y-%m-%d %H:%M"), " (kuru)" if kuru else "",
                   basari, hata))
        f.write("| İş | Durum | Not |\n|---|---|---|\n")
        f.write("\n".join(satir) + "\n")
    print("\n".join(satir))
    print("---- %d yayın, %d hata" % (basari, hata))
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
