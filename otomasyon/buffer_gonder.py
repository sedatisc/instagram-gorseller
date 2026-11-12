#!/usr/bin/env python3
"""Günün paylaşımlarını Buffer'a planlar — GitHub Actions üzerinde çalışır.

Meta geliştirici hesabı gerektirmeyen ücretsiz yol. Instagram hesabı
Buffer'a bağlı; Buffer kendi Meta uygulamasıyla yayınlıyor. Bu betik her
gece bir kez çalışıp o günün gönderi, hikaye ve reels'lerini Buffer'a
saatleriyle birlikte gönderir. Buffer ücretsiz planı kanal başına aynı anda
10 bekleyen paylaşıma izin veriyor; günlük gönderim bu sınırın altında
kalıyor.

    python3 otomasyon/buffer_gonder.py --kuru            # hiçbir şey göndermez
    python3 otomasyon/buffer_gonder.py                   # bugünü gönderir
    python3 otomasyon/buffer_gonder.py --gun 2026-11-04  # belirli gün
    python3 otomasyon/buffer_gonder.py --kontrol         # yalnız bağlantı

Ortam değişkeni (GitHub Actions secret):
    BUFFER_TOKEN   Buffer > Settings > API altından alınan anahtar

Gönderilen klasörler icerik.json'da "yayinlandi" olarak işaretlenir; plan
ertesi gün bir sonraki işle devam eder. Aynı gün için daha önce işaretlenmiş
iş varsa (elle ya da başka araçla planlanmış) o gün atlanır, iki kez gitmez.
"""
import json
import os
import re
import sys
from datetime import date, datetime, timedelta

import requests

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
sys.path.insert(0, os.path.join(KOK, "otomasyon"))
import sira                                              # noqa: E402
import yayinla                                           # noqa: E402

UC = "https://api.buffer.com"
DEFTER = os.path.join(KOK, "otomasyon", "buffer-defter.json")
RAPOR = os.path.join(KOK, "otomasyon", "SON-BUFFER.md")
BAGLANTI = os.path.join(KOK, "baglantilar.json")
AZAMI_ETIKET = 5          # Buffer, Instagram gönderisinde en çok 5 hashtag
AZAMI_METIN = 2200
AZAMI_GUNLUK = 10         # ücretsiz planın bekleyen paylaşım sınırı


class Hata(Exception):
    pass


# ------------------------------------------------------------ Buffer API
def _sorgu(q, degisken=None):
    r = requests.post(UC, json={"query": q, "variables": degisken or {}},
                      headers={"Authorization": "Bearer %s"
                               % os.environ["BUFFER_TOKEN"]},
                      timeout=60)
    try:
        g = r.json()
    except ValueError:
        raise Hata("Buffer %s: %s" % (r.status_code, r.text[:300]))
    if g.get("errors"):
        raise Hata("Buffer: %s" % "; ".join(e.get("message", "")
                                             for e in g["errors"]))
    return g["data"]


def kanal_bul():
    """Bağlı Instagram kanalının kimliği."""
    d = _sorgu("query { account { organizations { id } } }")
    for org in d["account"]["organizations"]:
        k = _sorgu("query K($o: OrganizationId!) { channels(input: "
                   "{organizationId: $o}) { id service name isDisconnected } }",
                   {"o": org["id"]})
        for c in k["channels"]:
            if c["service"].lower() == "instagram" and not c["isDisconnected"]:
                return c["id"], c["name"]
    raise Hata("Buffer'da bağlı Instagram kanalı yok")


def _tur_adi(t):
    while t and t.get("ofType"):
        if t.get("name"):
            break
        t = t["ofType"]
    return t.get("name") if t else None


def _alanlar(ad):
    d = _sorgu("query T($n: String!) { __type(name: $n) { inputFields { "
               "name type { name kind ofType { name kind ofType { name kind "
               "} } } } enumValues { name } } }", {"n": ad})
    return d["__type"] or {}


def _zorunlu(t):
    """Alan NON_NULL mı — şema kindine bakıyor."""
    return bool(t) and t.get("kind") == "NON_NULL"


def silme_alani():
    """Planlanmış gönderiyi silen mutasyonun adı ve girdi tipi.

    Belgede geçmiyor, adı da kesin değil: şemadaki Mutation alanları
    arasından silme işini yapanı buluyoruz."""
    d = _sorgu("query { __schema { mutationType { fields { name args { "
               "name type { name kind ofType { name kind ofType "
               "{ name kind } } } } } } } }")
    alanlar = ((d.get("__schema") or {}).get("mutationType") or {}) \
        .get("fields") or []
    for ad in ("deletePost", "removePost", "postDelete", "deleteDraft"):
        f = next((x for x in alanlar if x["name"] == ad), None)
        if f:
            arg = f["args"][0] if f["args"] else None
            return ad, (arg["name"] if arg else "input"), \
                (_tur_adi(arg["type"]) if arg else None)
    return None, None, None


def buffer_sil(post_id):
    """Buffer'daki planlanmış gönderiyi siliyor."""
    ad, arg_ad, arg_tur = silme_alani()
    if not ad:
        raise Hata("Buffer şemasında silme mutasyonu bulunamadı")
    if arg_tur in (None, "ID", "String", "PostId"):
        q = ("mutation S($v: %s!) { %s(%s: $v) { __typename } }"
             % (arg_tur or "ID", ad, arg_ad))
        _sorgu(q, {"v": post_id})
    else:
        q = ("mutation S($v: %s!) { %s(%s: $v) { __typename } }"
             % (arg_tur, ad, arg_ad))
        _sorgu(q, {"v": {"id": post_id}})
    return ad


def ig_meta_alanlari():
    """metadata.instagram altındaki tüm girdi alanları.

    Hikayeye bağlantı etiketi koyulabiliyor mu, ücretsiz planda hangi alan
    var — belgede yazmıyor, şemaya soruyoruz."""
    giris = _alanlar("CreatePostInput")
    meta = next((f for f in giris.get("inputFields", [])
                 if f["name"] == "metadata"), None)
    if not meta:
        return []
    ig = next((f for f in _alanlar(_tur_adi(meta["type"]))
               .get("inputFields", []) if f["name"] == "instagram"), None)
    if not ig:
        return []
    return [(f["name"], _tur_adi(f["type"]), _zorunlu(f["type"]))
            for f in _alanlar(_tur_adi(ig["type"])).get("inputFields", [])]


def ig_turleri():
    """Instagram gönderi türü enum değerlerini şemadan okur.

    Belgelerde yazım biçimi geçmiyor; tahmin yerine şemaya soruyoruz."""
    giris = _alanlar("CreatePostInput")
    meta = next((f for f in giris.get("inputFields", [])
                 if f["name"] == "metadata"), None)
    if not meta:
        raise Hata("CreatePostInput.metadata bulunamadı")
    ig = next((f for f in _alanlar(_tur_adi(meta["type"]))
               .get("inputFields", []) if f["name"] == "instagram"), None)
    if not ig:
        raise Hata("metadata.instagram bulunamadı")
    tur = next((f for f in _alanlar(_tur_adi(ig["type"]))
                .get("inputFields", []) if f["name"] == "type"), None)
    if not tur:
        raise Hata("metadata.instagram.type bulunamadı")
    degerler = [e["name"] for e in
                _alanlar(_tur_adi(tur["type"])).get("enumValues") or []]
    harita = {}
    for v in degerler:
        k = v.lower()
        for ad in ("post", "story", "reel"):
            if k == ad or k == ad + "s":
                harita[ad] = v
    eksik = {"post", "story", "reel"} - set(harita)
    if eksik:
        raise Hata("Instagram tür değerleri eşleşmedi: %s (şemada: %s)"
                   % (", ".join(sorted(eksik)), ", ".join(degerler)))
    return harita


# metadata.instagram'da hikaye bağlantısını taşıyan alanın adı. Şemada
# yoksa None kalıyor ve bağlantı gönderilmiyor — uydurma alan yollamıyoruz.
HIKAYE_LINK_ALANI = None
ILK_YORUM_VAR = False
ZORUNLU_ALAN = []

# Instagram, yapay zekâ ile üretilmiş ya da belirgin değiştirilmiş içeriğin
# beyan edilmesini istiyor; Buffer bu beyanı zorunlu alan yapmış. Ürün
# görselleri Higgsfield'da üretiliyor, şablonla basılan kareler değil.
YZ_BEYANI = {"baski": True, "magaza": False, "rehber": False,
             "proje": False, "uygulama": False, "kampanya": False}
LINK_ADAYLARI = ("linkStickerUrl", "storyLinkUrl", "link", "linkUrl",
                 "swipeUpUrl")


def hikaye_link_alani(alanlar):
    for ad, _t, _z in alanlar:
        if ad in LINK_ADAYLARI:
            return ad
    return None


def gonder(kanal, metin, varliklar, zaman, tur, turler, baglanti=None,
           yorum=None, yz=False):
    """Tek paylaşımı Buffer'a belirli saatte planlar."""
    global ILK_YORUM_VAR
    utc = (zaman - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:00.000Z")
    q = """mutation P($i: CreatePostInput!) {
      createPost(input: $i) {
        ... on PostActionSuccess { post { id dueAt } }
        ... on MutationError { message }
      }
    }"""
    girdi = {"text": metin, "channelId": kanal,
             "schedulingType": "automatic", "mode": "customScheduled",
             "dueAt": utc, "assets": varliklar,
             "metadata": {"instagram": {"type": turler[tur]}}}
    ig = girdi["metadata"]["instagram"]
    # shouldShareToFeed her Instagram gönderi türünde zorunlu. Yalnız
    # reels'e koyduğumuz için gönderi ve hikaye "required field" hatasıyla
    # geri dönüyordu; artık hepsine giriyor.
    ig["shouldShareToFeed"] = True
    # Şemanın zorunlu tuttuğu başka alan varsa türüne uygun değerle
    # dolduruluyor; boş kalan alan isteğin tamamını düşürüyor.
    for a, t in ZORUNLU_ALAN:
        if a in ig:
            continue
        if a == "isAiGenerated":
            ig[a] = bool(yz)
        elif a == "firstComment":
            ig[a] = yorum or ""
        elif a == "link":
            ig[a] = baglanti or ""
        elif t == "Boolean":
            ig[a] = False
        elif t in ("String", "ID"):
            ig[a] = ""
        else:
            print("ZORUNLU ALAN BİLİNMİYOR: %s (%s)" % (a, t))
    if tur == "story" and baglanti and HIKAYE_LINK_ALANI:
        girdi["metadata"]["instagram"][HIKAYE_LINK_ALANI] = baglanti
    if tur != "story" and yorum and ILK_YORUM_VAR:
        girdi["metadata"]["instagram"]["firstComment"] = yorum[:2200]
    try:
        d = _sorgu(q, {"i": girdi})["createPost"]
        if "post" not in d:
            raise Hata(d.get("message", "bilinmeyen hata"))
    except Hata as e:
        # firstComment şemada görünüyor ama ücretsiz planda reddediliyor:
        # "First comment requires a paid plan". İlk yorumu metnin sonuna
        # indirip bir kez daha deniyoruz — gönderi düşmesin.
        if "paid plan" not in str(e).lower():
            raise
        ILK_YORUM_VAR = False
        ig.pop("firstComment", None)
        if yorum:
            girdi["text"] = (metin.rstrip() + "\n\n" + yorum.strip())[:2200]
        print("İlk yorum ücretli planda — metnin sonuna eklendi.")
        d = _sorgu(q, {"i": girdi})["createPost"]
        if "post" not in d:
            raise Hata(d.get("message", "bilinmeyen hata"))
    return d["post"]["id"]


# ------------------------------------------------------------ bağlantı
def urun_linki(klasor):
    """Ürünün site sayfası; yoksa site adresi."""
    return sira.urun_sayfasi(klasor)


def _magaza_satiri(klasor, kategori=""):
    u = urun_linki(klasor)
    if not u:
        return ""
    etiket = "Uygulama sayfası: " if kategori == "uygulama" \
        else "Ürün sayfası: "
    return etiket + re.sub(r"^https?://", "", u).rstrip("/")


# ------------------------------------------------------------ metin
def metin_kur(klasor, ayri_yorum=False, kategori=""):
    """Gönderi metni.

    İlk yorum Buffer şemasında varsa (firstComment) ayrı gidiyor, yoksa
    metnin sonuna iniyor."""
    govde, yorum = yayinla.metin_oku(klasor)
    govde = govde or ""
    MAGAZA = _magaza_satiri(klasor, kategori)
    yorum = re.sub(r"\*\*(.+?)\*\*", r"\1", yorum or "")
    for yer in ("Bağlantı: {urun_linki}", "{urun_linki}",
                "Bağlantı: {trendyol_linki}", "{trendyol_linki}"):
        yorum = yorum.replace(yer, MAGAZA)
    if yorum:
        govde = govde.replace("Bağlantı ilk yorumda.", MAGAZA
                              if MAGAZA in yorum else "")
    elif MAGAZA:
        govde = govde.replace("Bağlantı ilk yorumda.", MAGAZA)
    satirlar = govde.rstrip().split("\n")
    etiket = []
    if satirlar and satirlar[-1].lstrip().startswith("#"):
        etiket = satirlar.pop().split()[:AZAMI_ETIKET]
    govde = "\n".join(satirlar).rstrip()
    if ayri_yorum:
        pass
    elif yorum and yorum != MAGAZA:
        govde += "\n\n" + yorum
    elif yorum == MAGAZA and MAGAZA not in govde:
        govde += "\n\n" + MAGAZA
    govde = re.sub(r"\n{3,}", "\n\n", govde)
    son = (govde + ("\n\n" + " ".join(etiket) if etiket else "")).strip()
    if len(son) > AZAMI_METIN:
        kes = AZAMI_METIN - len(" ".join(etiket)) - 4
        son = govde[:kes].rstrip() + "…\n\n" + " ".join(etiket)
    return son


def varlik(is_, sha):
    """Gönderinin medyası.

    Baskı ürününde yalnız sitenin kendi görselleri kullanılıyor; site
    görseli yoksa iş gönderilmiyor, depodaki kareye düşülmüyor."""
    k = is_["klasor"]
    # icerik.json'daki işte "gorsel" / "gorsel_hikaye" adresleri varsa
    # medya depodan değil o adreslerden gidiyor. Depoya konamayan
    # (dışarıda üretilmiş) kareler için.
    dis = sira.dis_gorsel(k)
    if dis:
        if is_["tur"] == "hikaye":
            return [{"image": {"url": dis.get("hikaye") or dis["kare"][0]}}]
        if is_["tur"] == "gonderi":
            return [{"image": {"url": u}} for u in dis["kare"][:10]]
    if is_.get("kategori") == "baski":
        g = sira.urun_gorselleri(k)
        if not g:
            raise Hata("%s — site görseli yok, gönderilmedi" % k)
        if is_["tur"] == "hikaye":
            return [{"image": {"url": g[0]}}]
        if is_["tur"] == "gonderi":
            return [{"image": {"url": u}} for u in g[:10]]
    if is_["tur"] == "gonderi":
        yollar = yayinla.kareler(k)
        if not yollar:
            raise Hata("%s içinde kare yok" % k)
        return [{"image": {"url": yayinla.ham(y, sha)}} for y in yollar[:10]]
    if is_["tur"] == "hikaye":
        return [{"image": {"url": yayinla.ham("%s/hikaye.jpg" % k, sha)}}]
    return [{"video": {"url": yayinla.ham("%s/reels.mp4" % k, sha)}}]


# ------------------------------------------------------------ ana akış
def defter_oku():
    try:
        return json.load(open(DEFTER, encoding="utf-8"))
    except Exception:
        return {"gonderilen": []}


def mutasyon_listesi():
    d = _sorgu("query { __schema { mutationType { fields { name } } } }")
    f = ((d.get("__schema") or {}).get("mutationType") or {}).get("fields")
    return [x["name"] for x in (f or [])]


def geri_al(onek):
    """Deftere girmiş işleri Buffer'dan silip defterden düşürüyor.

    Böylece aynı iş yeni görseliyle tekrar gönderilebiliyor."""
    defter = defter_oku()
    kalan, silinen, notlar = [], 0, []
    for g in defter["gonderilen"]:
        if not g["anahtar"].startswith(onek):
            kalan.append(g)
            continue
        try:
            ad = buffer_sil(g["buffer"])
            print("Silindi (%s): %s" % (ad, g["anahtar"]))
            silinen += 1
        except Exception as e:                               # noqa: BLE001
            print("SİLİNEMEDİ: %s — %s" % (g["anahtar"], str(e)[:300]))
            notlar.append("%s: %s" % (g["anahtar"], str(e)[:300]))
            kalan.append(g)
    defter["gonderilen"] = kalan
    with open(DEFTER, "w", encoding="utf-8") as f:
        json.dump(defter, f, ensure_ascii=False, indent=1)
    print("Toplam silinen: %d" % silinen)
    try:
        mut = mutasyon_listesi()
    except Exception as e:                                   # noqa: BLE001
        mut = ["şema okunamadı: %s" % str(e)[:200]]
    with open(RAPOR, "w", encoding="utf-8") as f:
        f.write("# Geri alma\n\nSilinen: %d\n\nNot: %s\n\n"
                "## Mutation alanları\n\n%s\n"
                % (silinen, "; ".join(notlar) or "-", ", ".join(mut)))
    return silinen


def main():
    kuru = "--kuru" in sys.argv
    if "--geri-al" in sys.argv:
        geri_al(sys.argv[sys.argv.index("--geri-al") + 1])
    if "--kontrol" in sys.argv:
        kanal, ad = kanal_bul()
        print("Kanal bağlı: %s (%s)" % (ad, kanal))
        print("Instagram türleri: %s" % ig_turleri())
        alanlar = ig_meta_alanlari()
        print("metadata.instagram alanları: %s"
              % ", ".join("%s: %s%s" % (a, t, " (ZORUNLU)" if z else "")
                          for a, t, z in alanlar))
        link = hikaye_link_alani(alanlar)
        print("Hikaye bağlantı alanı: %s"
              % (link or "YOK — hikayeye bağlantı etiketi konulamıyor"))
        with open(RAPOR, "w", encoding="utf-8") as f:
            f.write("# Buffer kontrolü\n\nKanal: %s\n" % ad)
        return 0
    gun = yayinla.simdi().date()
    if "--gun" in sys.argv:
        gun = date.fromisoformat(sys.argv[sys.argv.index("--gun") + 1])
    gun_s = gun.isoformat()
    sha = os.environ.get("GITHUB_SHA") or "main"

    if not kuru and not os.environ.get("BUFFER_TOKEN"):
        print("BUFFER_TOKEN yok — gönderim yapılamaz. "
              "Deneme için: python3 otomasyon/buffer_gonder.py --kuru")
        return 1

    d = sira.oku()
    once = [i["klasor"] for i in d["icerik"]
            if i.get("durum") == "yayinlandi" and i.get("tarih") == gun_s]
    if once and "--zorla" in sys.argv:
        print("%s günü planlanmış ama --zorla verildi; yalnız deftere "
              "girmemiş ve saati geçmemiş işler gönderilecek." % gun_s)
        once = []
    if once:
        print("%s günü zaten planlanmış (%s) — atlanıyor."
              % (gun_s, ", ".join(once)))
        return 0

    defter = defter_oku()
    yapilan = {g["anahtar"] for g in defter["gonderilen"]}
    simdi = yayinla.simdi().replace(tzinfo=None)
    isler = []
    for i in yayinla.gundem():
        if not i["zaman"].startswith(gun_s) or i["anahtar"] in yapilan:
            continue
        # Saati geçmiş iş Buffer'a planlanamıyor; sessizce atlanıyor ki
        # gün ortasında çalıştırılan gönderim hataya düşmesin.
        if datetime.fromisoformat(i["zaman"]) <= simdi:
            print("Saati geçti, atlandı: %s (%s)" % (i["anahtar"],
                                                     i["zaman"]))
            continue
        # Gün içinde elle tetiklenen gönderimde yalnız tarihi elle
        # yazılmış (kampanya) işler gidiyor. Plan gün ortasında yeniden
        # türetilince o günün dolmuş slotlarına yeni iş düşüyordu;
        # bu, aynı saate ikinci bir gönderi çıkmasını engelliyor.
        if "--sadece-kampanya" in sys.argv and i.get("slot") != "kampanya":
            continue
        # Gün içinde tek bir işi düzeltip yeniden göndermek için:
        # --yalniz <önek>[,<önek>...]. Yalnız anahtarı bu öneklerden
        # biriyle başlayan işler gidiyor, gün içinde yeniden türeyen
        # başka hiçbir iş karışmıyor.
        if "--yalniz" in sys.argv:
            onekler = [o.strip() for o
                       in sys.argv[sys.argv.index("--yalniz") + 1].split(",")
                       if o.strip()]
            if not any(i["anahtar"].startswith(o) for o in onekler):
                continue
        isler.append(i)
    # Ücretsiz plan: kanal başına aynı anda en çok 10 bekleyen paylaşım.
    # Fazlası varsa önce kampanya hikayesi, sonra sondan hikayeler düşüyor.
    # Sınırı aşan hikayeler bu sırayla düşüyor. Baskı ürününün hikayesi
    # hiç düşmüyor: ürün bağlantısı oradan veriliyor.
    DUSME_SIRASI = ["kampanya", "proje", "rehber", "magaza"]
    while len(isler) > AZAMI_GUNLUK:
        hik = [i for i in isler if i["tur"] == "hikaye"]
        dus = None
        for slot in DUSME_SIRASI:
            aday = [i for i in hik
                    if (i.get("kategori") or i["slot"]) == slot]
            if aday:
                dus = aday[-1]
                break
        if dus is None:
            print("Sınır %d — düşürülecek hikaye kalmadı, %d iş gidiyor."
                  % (AZAMI_GUNLUK, len(isler)))
            break
        print("Sınır %d — düşen: %s" % (AZAMI_GUNLUK, dus["anahtar"]))
        isler.remove(dus)
    tur_ad = {"gonderi": "post", "hikaye": "story", "reels": "reel"}
    satir, klasorler, hata = [], set(), 0

    kanal, turler = None, None
    if not kuru:
        global HIKAYE_LINK_ALANI
        kanal, ad = kanal_bul()
        turler = ig_turleri()
        global ILK_YORUM_VAR
        alanlar = ig_meta_alanlari()
        HIKAYE_LINK_ALANI = hikaye_link_alani(alanlar)
        ILK_YORUM_VAR = any(a == "firstComment" for a, _t, _z in alanlar)
        global ZORUNLU_ALAN
        ZORUNLU_ALAN = [(a, t) for a, t, z in alanlar if z and a != "type"]
        if ZORUNLU_ALAN:
            print("metadata.instagram zorunlu alanları: %s"
                  % ", ".join("%s: %s" % x for x in ZORUNLU_ALAN))
        print("Kanal: %s · türler: %s" % (ad, turler))
        print("Hikaye bağlantı alanı: %s"
              % (HIKAYE_LINK_ALANI or "şemada yok — hikayeye bağlantı "
                 "eklenemiyor, bağlantı metne yazılıyor"))
        print("İlk yorum alanı: %s"
              % ("firstComment" if ILK_YORUM_VAR
                 else "şemada yok — ilk yorum metnin sonuna ekleniyor"))

    for is_ in isler:
        anahtar = is_["anahtar"]
        if anahtar in yapilan:
            continue
        zaman = datetime.fromisoformat(is_["zaman"])
        try:
            v = varlik(is_, sha)
            link = (urun_linki(is_["klasor"])
                    if is_.get("kategori") in ("baski", "magaza",
                                               "uygulama") else "")
            if is_["tur"] == "hikaye":
                # Hikayeye bağlantı etiketi konabiliyorsa oradan, konamıyorsa
                # hikaye metnine yazılıyor; ürün sayfası her iki durumda da
                # hikayede görünüyor.
                metin = "" if HIKAYE_LINK_ALANI or not link else \
                    re.sub(r"^https?://", "", link).rstrip("/")
            else:
                metin = metin_kur(is_["klasor"], ILK_YORUM_VAR,
                                  is_.get("kategori", ""))
            _g, ilk = yayinla.metin_oku(is_["klasor"])
            ilk = ilk if (ILK_YORUM_VAR and is_["tur"] != "hikaye") else None
            if kuru:
                print("→ %s · %s · %d medya · metin %d kr%s"
                      % (is_["zaman"], anahtar, len(v), len(metin),
                         " · bağlantı " + link if link else ""))
                satir.append("| %s | %s | kuru |" % (is_["zaman"], anahtar))
                continue
            pid = gonder(kanal, metin, v, zaman, tur_ad[is_["tur"]], turler,
                         link, ilk,
                         YZ_BEYANI.get(is_.get("kategori"), False))
            defter["gonderilen"].append({"anahtar": anahtar, "buffer": pid,
                                         "zaman": is_["zaman"]})
            json.dump(defter, open(DEFTER, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            klasorler.add(is_["klasor"])
            satir.append("| %s | %s | planlandı |" % (is_["zaman"], anahtar))
        except Hata as e:
            hata += 1
            satir.append("| %s | %s | HATA: %s |"
                         % (is_["zaman"], anahtar, str(e)[:600]))

    if not kuru:
        if klasorler:
            yayinla.plan_oturt()
        for k in sorted(klasorler):
            sira.komut_yayinlandi(k, gun_s)

    if not satir:
        satir.append("| — | — | bu gün için iş yok |")
    with open(RAPOR, "w", encoding="utf-8") as f:
        f.write("# Son Buffer gönderimi\n\n%s%s · %d hata\n\n"
                % (gun_s, " (kuru)" if kuru else "", hata))
        f.write("| Saat | İş | Durum |\n|---|---|---|\n")
        f.write("\n".join(satir) + "\n")
    print("\n".join(satir))
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
