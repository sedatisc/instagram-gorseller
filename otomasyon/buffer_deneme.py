#!/usr/bin/env python3
"""Buffer gönderimini taklit Buffer'a karşı deniyor.

Gerçek anahtar burada yok; _sorgu yerine Buffer'ın doğrulamasını taklit
eden bir işlev konuyor. Taklit, Buffer'ın bugün döndürdüğü hatanın
kuralını uyguluyor: metadata.instagram'da shouldShareToFeed yoksa istek
"required field" diye düşüyor. Böylece göndereceğimiz yükün şekli
gerçek gönderime çıkmadan doğrulanıyor.
"""
import os
import sys

KOK = "/home/claude/instagram-gorseller"
sys.path.insert(0, KOK)
sys.path.insert(0, os.path.join(KOK, "otomasyon"))
os.environ["BUFFER_TOKEN"] = "deneme"

import buffer_gonder as B                                    # noqa: E402
import yayinla                                               # noqa: E402

GONDERILEN = []
SEMA = [("firstComment", "String", False),
        ("geolocation", "InstagramGeolocationInput", False),
        ("isAiGenerated", "Boolean", False),
        ("link", "String", False),
        ("shouldShareToFeed", "Boolean", True),
        ("stickerFields", "InstagramStickerFieldsInput", False),
        ("type", "PostType", True)]


def taklit_sorgu(q, degisken=None):
    if "createPost" not in q:
        raise AssertionError("beklenmeyen sorgu")
    ig = degisken["i"]["metadata"]["instagram"]
    # Ücretsiz planın gerçek davranışı: dolu firstComment reddediliyor.
    if ig.get("firstComment"):
        raise B.Hata("Invalid post: First comment requires a paid plan. "
                     "Please upgrade to use this feature.")
    for ad, _t, zorunlu in SEMA:
        if zorunlu and ad not in ig:
            raise B.Hata('Buffer: Variable "$i" got invalid value ... '
                         'Expected value of type '
                         '"InstagramPostMetadataInput" to include required '
                         'field "%s".' % ad)
    GONDERILEN.append(dict(degisken["i"]))
    return {"createPost": {"post": {"id": "deneme-%d" % len(GONDERILEN),
                                    "dueAt": degisken["i"]["dueAt"]}}}


B._sorgu = taklit_sorgu
B.kanal_bul = lambda: ("deneme-kanal", "sermenkreatif")
B.ig_turleri = lambda: {"post": "post", "story": "story", "reel": "reel"}
B.ig_meta_alanlari = lambda: SEMA

gun = sys.argv[1] if len(sys.argv) > 1 else "2026-11-04"
ek = sys.argv[2:]
B.DEFTER = "/tmp/claude-0/-home-claude/" \
    "ef2140ec-8608-5339-9ace-73c3ed35e2e5/scratchpad/deneme-defter.json"
B.RAPOR = "/tmp/claude-0/-home-claude/" \
    "ef2140ec-8608-5339-9ace-73c3ed35e2e5/scratchpad/deneme-rapor.md"
if os.path.exists(B.DEFTER):
    os.remove(B.DEFTER)

# icerik.json'a dokunmasın: işaretleme işlevini sustur
import sira                                                  # noqa: E402
sira.komut_yayinlandi = lambda *a, **k: None

sys.argv = ["buffer_gonder.py", "--gun", gun] + ek
cikis = B.main()

print("\n--- DENEME SONUCU ---")
print("çıkış kodu:", cikis, "· gönderilen:", len(GONDERILEN))
hata = 0
for g in GONDERILEN:
    ig = g["metadata"]["instagram"]
    eksik = [a for a, _t, z in SEMA if z and a not in ig]
    if eksik:
        hata += 1
        print("  EKSİK ALAN:", eksik)
for g in GONDERILEN[:3]:
    ig = g["metadata"]["instagram"]
    print("  %s · %s · %s · medya %d · metin %d kr"
          % (g["dueAt"], ig["type"],
             " ".join("%s=%s" % (k, v) for k, v in sorted(ig.items())
                      if k != "type")[:90],
             len(g["assets"]), len(g["text"])))
print("zorunlu alan eksiği olan iş:", hata)
raise SystemExit(1 if (hata or cikis) else 0)
