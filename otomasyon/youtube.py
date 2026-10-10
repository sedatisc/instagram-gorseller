#!/usr/bin/env python3
"""YouTube Shorts'a otomatik yükleme — GitHub Actions üzerinde çalışır.

Aynı kuyruktan besleniyor: her günün reels videosu aynı gün YouTube'a
Short olarak çıkıyor. Dikey ve 3 dakikanın altındaki video YouTube
tarafından kendiliğinden Short sayılıyor, ayrıca bir alan yok.

    python3 otomasyon/youtube.py --kuru     # hiçbir şey yüklemez, ne
                                            # yapacağını ve başlığı yazar
    python3 otomasyon/youtube.py            # vakti geleni yükler
    python3 otomasyon/youtube.py --zorla 2026-10-12

Ortam değişkenleri (GitHub Actions secret):
    YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN

Kurulum: otomasyon/YOUTUBE-KURULUM.md
"""
import json
import os
import sys
import time
from datetime import datetime, timedelta

import requests

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
import sira                                              # noqa: E402
import paket                                             # noqa: E402

DEFTER = os.path.join(KOK, "otomasyon", "yayinlanan-youtube.json")
RAPOR = os.path.join(KOK, "otomasyon", "SON-YOUTUBE.md")

JETON = "https://oauth2.googleapis.com/token"
YUKLE = "https://www.googleapis.com/upload/youtube/v3/videos"
API = "https://www.googleapis.com/youtube/v3"

GECIKME_SINIRI = timedelta(hours=3)
KATEGORI = "28"            # Science & Technology


class Hata(Exception):
    pass


def erisim():
    g = requests.post(JETON, data={
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"],
        "grant_type": "refresh_token"}, timeout=60)
    if g.status_code >= 400:
        raise Hata("jeton yenilenemedi: %s" % g.text[:200])
    return g.json()["access_token"]


def defter_oku():
    if os.path.exists(DEFTER):
        try:
            return json.load(open(DEFTER, encoding="utf-8"))
        except Exception:
            pass
    return {"yuklenen": []}


# ------------------------------------------------------------ metin
def baslik(klasor):
    """Kapak manşetinden YouTube başlığı — 100 karakter sınırı var."""
    b = paket.baslik(klasor)
    if len(b) > 90:
        b = b[:87].rstrip() + "…"
    return b


def aciklama(klasor):
    govde, yorum = sira.metin_oku(klasor)
    parca = [govde or ""]
    if yorum:
        parca.append(yorum)
    parca.append("sermenkreatif.com")
    return "\n\n".join(p for p in parca if p)[:4900]


def etiketler(klasor):
    """Metindeki #etiketleri YouTube etiketine çevir (# olmadan)."""
    govde, _ = sira.metin_oku(klasor)
    if not govde:
        return []
    t, uzun = [], 0
    for kelime in govde.split():
        if kelime.startswith("#") and len(kelime) > 2:
            e = kelime[1:].strip(".,;:")
            if e not in t and uzun + len(e) + 1 < 460:   # 500 karakter sınırı
                t.append(e)
                uzun += len(e) + 1
    return t


# ------------------------------------------------------------ gündem
def gundem():
    """Kuyruktaki reels'ler — tarih, saat, klasör."""
    d = json.load(open(os.path.join(KOK, "DURUM.json"), encoding="utf-8"))
    kb = d["kuyruk_bekleyen"]
    bekle = {b["klasor"] for b in kb.get("beklemede", [])}
    isler = []
    for r in kb.get("reels", []):
        if r["klasor"] in bekle:
            continue
        from datetime import date
        g = date.fromisoformat(r["tarih"]).weekday()
        isler.append({"anahtar": r["tarih"], "klasor": r["klasor"],
                      "zaman": "%sT%s" % (r["tarih"], sira.IZGARA[g]["reels"])})
    return sorted(isler, key=lambda i: i["zaman"])


def simdi():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Istanbul")).replace(tzinfo=None)
    except Exception:
        return datetime.utcnow() + timedelta(hours=3)


# ------------------------------------------------------------ yükleme
def yukle(jeton, yol, veri):
    """Devam ettirilebilir yükleme: önce oturum, sonra dosya."""
    boy = os.path.getsize(yol)
    a = requests.post(
        YUKLE, params={"uploadType": "resumable", "part": "snippet,status"},
        headers={"Authorization": "Bearer " + jeton,
                 "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Length": str(boy),
                 "X-Upload-Content-Type": "video/mp4"},
        data=json.dumps(veri).encode("utf-8"), timeout=120)
    if a.status_code >= 400 or "location" not in {k.lower() for k in a.headers}:
        raise Hata("oturum açılamadı: %s %s" % (a.status_code, a.text[:200]))
    oturum = a.headers["Location"]
    with open(yol, "rb") as f:
        b = requests.put(oturum, headers={"Content-Length": str(boy),
                                          "Content-Type": "video/mp4"},
                         data=f, timeout=900)
    if b.status_code not in (200, 201):
        raise Hata("yükleme başarısız: %s %s" % (b.status_code, b.text[:300]))
    return b.json()["id"]


def ilk_yorum(jeton, kanal, video, metin):
    """youtube.force-ssl kapsamı gerekiyor; yoksa sessizce geçiyoruz."""
    try:
        g = requests.post(API + "/commentThreads", params={"part": "snippet"},
                          headers={"Authorization": "Bearer " + jeton,
                                   "Content-Type": "application/json"},
                          data=json.dumps({"snippet": {
                              "channelId": kanal, "videoId": video,
                              "topLevelComment": {"snippet": {
                                  "textOriginal": metin}}}}).encode("utf-8"),
                          timeout=60)
        if g.status_code >= 400:
            print("   ilk yorum yazılamadı: %s" % g.text[:160])
            return False
        return True
    except Exception as e:
        print("   ilk yorum yazılamadı: %s" % e)
        return False


def kanal_kimligi(jeton):
    g = requests.get(API + "/channels", params={"part": "id", "mine": "true"},
                     headers={"Authorization": "Bearer " + jeton}, timeout=60)
    try:
        return g.json()["items"][0]["id"]
    except Exception:
        return None


# ------------------------------------------------------------ ana akış
def main():
    kuru = "--kuru" in sys.argv
    zorla = sys.argv[sys.argv.index("--zorla") + 1] if "--zorla" in sys.argv \
        else None

    if not kuru and not all(os.environ.get(k) for k in
                            ("YT_CLIENT_ID", "YT_CLIENT_SECRET",
                             "YT_REFRESH_TOKEN")):
        print("YT_* secret'ları yok — yükleme yapılamaz. "
              "Deneme için: python3 otomasyon/youtube.py --kuru")
        return 1

    d = defter_oku()
    yapilan = {y["anahtar"] for y in d["yuklenen"]}
    an = simdi()
    satir, basari, hata = [], 0, 0
    jeton = kanal = None

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
        kl = is_["klasor"]
        yol = os.path.join(KOK, kl, "reels.mp4")
        print("→ %s · %s" % (ad, kl))
        try:
            if not os.path.exists(yol):
                raise Hata("%s/reels.mp4 yok" % kl)
            bas, acik = baslik(kl), aciklama(kl)
            if kuru:
                print("   başlık: %s" % bas)
                print("   açıklama %d karakter · etiket: %s"
                      % (len(acik), ", ".join(etiketler(kl)) or "yok"))
                print("   dosya %.1f MB" % (os.path.getsize(yol) / 1048576.0))
                satir.append("| %s | kuru | %s |" % (ad, bas))
                continue
            if jeton is None:
                jeton = erisim()
                kanal = kanal_kimligi(jeton)
            vid = yukle(jeton, yol, {
                "snippet": {"title": bas, "description": acik,
                            "tags": etiketler(kl), "categoryId": KATEGORI,
                            "defaultLanguage": "tr"},
                "status": {"privacyStatus": "public",
                           "selfDeclaredMadeForKids": False}})
            _, yorum = sira.metin_oku(kl)
            if yorum and kanal:
                ilk_yorum(jeton, kanal, vid, yorum)
            d["yuklenen"].append({"anahtar": ad, "video": vid, "klasor": kl,
                                  "zaman": an.strftime("%Y-%m-%d %H:%M")})
            json.dump(d, open(DEFTER, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            satir.append("| %s | tamam | youtu.be/%s |" % (ad, vid))
            basari += 1
        except Hata as e:
            print("   HATA: %s" % e)
            satir.append("| %s | HATA | %s |" % (ad, str(e)[:160]))
            hata += 1

    if not satir:
        satir.append("| — | boş | vakti gelmiş yeni video yok |")
    with open(RAPOR, "w", encoding="utf-8") as f:
        f.write("# Son YouTube yüklemesi\n\n%s%s · %d video · %d hata\n\n"
                % (an.strftime("%Y-%m-%d %H:%M"), " (kuru)" if kuru else "",
                   basari, hata))
        f.write("| İş | Durum | Not |\n|---|---|---|\n")
        f.write("\n".join(satir) + "\n")
    print("\n".join(satir))
    print("---- %d video, %d hata" % (basari, hata))
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
