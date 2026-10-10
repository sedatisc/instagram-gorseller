#!/usr/bin/env python3
"""Yayın paketi sayfası — kuyruktan tek sayfalık HTML üretir.

Kart düzeni: solda saat ve tür, sağda başlık, klasör, metin kutusu ve
kopyalama düğmeleri. Sayfa `yayin-paketi.html` olarak yazılıyor, oradan
artifact olarak yayımlanıyor.

    python3 paket.py
"""
import html
import json
import os
import re
import sys
from datetime import date

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import sira                                              # noqa: E402

DEPO = "https://github.com/sedatisc/instagram-gorseller/tree/main/"
HAM = "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/main/"
AY = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
      "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
KISA = {"3dbaski": "3DBASKI", "elektronik": "ELEKTRONİK",
        "urun": "ÜRÜN", "proje": "PROJE"}


KISALTMA = {
    "PLA", "PETG", "ABS", "ASA", "TPU", "PVA", "PC", "PA", "CF", "GF", "PEI",
    "ESR", "CFS", "AMS", "LED", "USB", "DC", "AC", "FDM", "SLA", "MSLA", "UV",
    "RH", "3D", "PCB", "MCU", "SPI", "I2C", "PWM", "HT", "HQ", "GS", "UGV",
    "ROV", "API", "BMS", "CO2", "TPE", "MMU", "WIFI", "BLE", "OLED", "TFT",
}
_KOD = re.compile(r"^[A-Z]{1,4}[-]?\d+[A-Z]*$")   # R1, S2, H2D, ESP32, DRV8833

# Türkçe küçültme I'yı ı yapıyor; İngilizce marka adlarında bu bozuluyor.
MARKA = {"FILADRYER": "FilaDryer", "FILAMENT": "Filament",
         "IOT": "IoT", "LIBER": "Liber", "COMBO": "Combo",
         "PIXHAWK": "Pixhawk", "SPARKX": "SparkX", "SILK": "Silk",
         "ORIN": "Orin", "JETSON": "Jetson", "NANO": "Nano",
         "MATTE": "Matte", "GLOW": "Glow", "PRINT": "Print"}


def _kucuk(s):
    return s.replace("İ", "i").replace("I", "ı").lower()


def _buyuk_ilk(s):
    if not s:
        return s
    ilk = {"i": "İ", "ı": "I"}.get(s[0], s[0].upper())
    return ilk + s[1:]


def _korunur(w):
    """PLA, H2D, R1 gibi kısaltma ve model kodları olduğu gibi kalsın."""
    c = w.strip(".,;:·!?()")
    if not c:
        return False
    if _KOD.match(c):
        return True
    parca = [p for p in re.split(r"[^A-ZÇĞİÖŞÜ0-9]+", c) if p]
    return bool(parca) and all(p in KISALTMA or _KOD.match(p) for p in parca)


def baslik(klasor):
    """Kapak manşetinden okunur bir başlık çıkar (Türkçe büyük/küçük harf)."""
    yol = os.path.join(KOK, klasor, "spec.json")
    if not os.path.exists(yol):
        return klasor
    k = json.load(open(yol, encoding="utf-8"))["kapak"]
    ham = ("%s %s" % (k.get("satir1", ""), k.get("satir2", ""))).strip()
    if not ham:                                   # rakam kapağının manşeti yok
        ham = ("%s %s" % (k.get("ustbilgi", ""), k.get("rakam", ""))).strip()
    if not ham:
        return klasor
    kelime = []
    for w in ham.split():
        c = w.strip(".,;:·!?()")
        if any(ch in w for ch in "µΩ°"):          # 10 µA bozulmasın
            kelime.append(w)
        elif _korunur(w):
            kelime.append(w)
        elif c.upper() in MARKA:
            kelime.append(w.replace(c, MARKA[c.upper()]))
        else:
            kelime.append(_buyuk_ilk(_kucuk(w)))
    return " ".join(kelime)


def yt_baslik(klasor):
    """YouTube başlığı — 100 karakter sınırı var."""
    b = baslik(klasor)
    return b if len(b) <= 90 else b[:87].rstrip() + "…"


def yt_aciklama(klasor):
    govde, yorum = sira.metin_oku(klasor)
    p = [govde or ""]
    if yorum:
        p.append(yorum)
    p.append("sermenkreatif.com")
    return "\n\n".join(x for x in p if x)[:4900]


def yt_etiket(klasor):
    govde, _ = sira.metin_oku(klasor)
    t, uzun = [], 0
    for k in (govde or "").split():
        if k.startswith("#") and len(k) > 2:
            e = k[1:].strip(".,;:")
            if e not in t and uzun + len(e) + 1 < 460:
                t.append(e)
                uzun += len(e) + 1
    return t


def tt_metin(klasor):
    """TikTok metni — ilk paragraf, sonunda etiketler. Uzun metin orada
    okunmuyor, ilk iki satır dışında her şey 'daha fazla' arkasında."""
    govde, _ = sira.metin_oku(klasor)
    if not govde:
        return ""
    paragraf = [p.strip() for p in govde.split("\n") if p.strip()]
    etiket = [p for p in paragraf if p.startswith("#")]
    govde_p = [p for p in paragraf if not p.startswith("#")]
    bas = govde_p[0] if govde_p else ""
    if len(bas) > 230 and len(govde_p) > 1:
        bas = bas[:227].rstrip() + "…"
    return (bas + ("\n\n" + etiket[0] if etiket else "")).strip()


def kayitlar():
    d, slotlar = sira.kuyruk()
    gun = sira.gunler(slotlar)
    reelsler = {r["tarih"]: r["klasor"]
                for r in d["kuyruk_bekleyen"].get("reels", [])}
    cikti = []
    for tarih, sl in gun.items():
        g = date.fromisoformat(tarih).weekday()
        kayit = []
        for ad in sira.SLOTLAR:
            s = sl.get(ad)
            if not s:
                continue
            kl = s["klasor"]
            govde, yorum = sira.metin_oku(kl)
            kare = sira.kare_adlari(kl)
            t = sira.saat(g, ad)
            kayit.append({"platform": ["ig"],
                          "saat": t, "tur": "GÖNDERİ", "slot": ad,
                          "baslik": baslik(kl), "klasor": kl,
                          "dosyalar": kare, "metin": govde or "",
                          "yorum": yorum or ""})
            kayit.append({"platform": ["ig"],
                          "saat": sira.arti(t, sira.HIKAYE_GECIKME),
                          "tur": "HİKAYE", "slot": ad, "baslik": baslik(kl),
                          "klasor": kl, "dosyalar": ["hikaye.jpg"],
                          "metin": "", "yorum": ""})
        r = reelsler.get(tarih)
        if r:
            govde, _ = sira.metin_oku(r)
            kayit.append({"saat": sira.saat(g, "reels"), "tur": "REELS",
                          "slot": "", "baslik": baslik(r), "klasor": r,
                          "dosyalar": ["reels.mp4"], "metin": govde or "",
                          "yorum": "", "platform": ["ig", "yt", "tt"],
                          "yt": {"baslik": yt_baslik(r),
                                 "aciklama": yt_aciklama(r),
                                 "etiket": ", ".join(yt_etiket(r))},
                          "tt": {"metin": tt_metin(r)}})
        kayit.sort(key=lambda k: k["saat"])
        gun_ad = date.fromisoformat(tarih)
        cikti.append({"tarih": tarih,
                      "ad": "%d %s · %s" % (gun_ad.day, AY[gun_ad.month - 1],
                                            sira.GUN[g]),
                      "kayitlar": kayit})
    return cikti


SAYFA = """<title>Yayın Paketi</title>
<style>
/* Düzen: solda saat rayı, sağda kart içeriği; günler üst üste dizili. */
:root {
  --kagit: #f7f6f3; --kart: #ffffff; --murekkep: #1c1a17;
  --soluk: #6b6560; --cizgi: #e2ded7; --kutu: #faf9f6;
  --dugme: #1c1a17; --dugme-yazi: #ffffff;
  --3dbaski: #c2410c; --elektronik: #0e7490; --urun: #15803d;
  --proje: #6d28d9; --reels: #be185d;
  --ana: "Inter", ui-sans-serif, system-ui, -apple-system, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --kagit: #16150f; --kart: #201e18; --murekkep: #f0ece3;
    --soluk: #a09a8f; --cizgi: #342f26; --kutu: #1a1813;
    --dugme: #f0ece3; --dugme-yazi: #16150f;
    --3dbaski: #fb923c; --elektronik: #22d3ee; --urun: #4ade80;
    --proje: #a78bfa; --reels: #f472b6;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --kagit: #16150f; --kart: #201e18; --murekkep: #f0ece3;
  --soluk: #a09a8f; --cizgi: #342f26; --kutu: #1a1813;
  --dugme: #f0ece3; --dugme-yazi: #16150f;
  --3dbaski: #fb923c; --elektronik: #22d3ee; --urun: #4ade80;
  --proje: #a78bfa; --reels: #f472b6;
  color-scheme: dark;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--kagit); color: var(--murekkep);
  font-family: var(--ana); font-size: 15px; line-height: 1.5;
  -webkit-text-size-adjust: 100%;
}
.sayfa { max-width: 980px; margin: 0 auto; padding-block: 28px 64px;
         padding-left: 16px; padding-right: 16px; }
header h1 { font-size: 24px; margin: 0 0 4px; letter-spacing: -0.015em;
            text-wrap: balance; }
header p { margin: 0; color: var(--soluk); font-size: 14px; max-width: 62ch; }
.ozet { display: flex; flex-wrap: wrap; gap: 8px 18px; margin: 14px 0 0;
        font-family: var(--mono); font-size: 12px; color: var(--soluk); }
.sekmeler { display: flex; gap: 6px; margin: 18px 0 2px; flex-wrap: wrap; }
.sekme { font-family: var(--mono); font-size: 12px; letter-spacing: 0.06em;
         padding: 8px 14px; border: 1px solid var(--cizgi); border-radius: 999px;
         background: var(--kart); color: var(--soluk); cursor: pointer; }
.sekme[aria-pressed="true"] { background: var(--dugme); color: var(--dugme-yazi);
                              border-color: var(--dugme); }
.durum { margin: 12px 0 0; padding: 11px 13px; border: 1px solid var(--cizgi);
         border-left: 3px solid var(--proje); border-radius: 7px;
         background: var(--kutu); font-size: 13.5px; color: var(--soluk); }
.durum b { color: var(--murekkep); font-weight: 600; }
.gun { margin-top: 38px; }
.gun h2 { font-size: 17px; margin: 0 0 12px; display: flex;
          align-items: baseline; gap: 10px; flex-wrap: wrap; }
.gun h2 span { font-family: var(--mono); font-size: 12px; color: var(--soluk);
               font-weight: 400; }
.kart { display: grid; grid-template-columns: 92px 1fr; background: var(--kart);
        border: 1px solid var(--cizgi); border-radius: 10px; overflow: hidden;
        margin-bottom: 12px; }
.ray { border-right: 1px solid var(--cizgi); padding: 16px 12px;
       display: flex; flex-direction: column; gap: 4px; align-items: flex-start; }
.ray b { font-family: var(--mono); font-size: 19px; font-weight: 500;
         font-variant-numeric: tabular-nums; letter-spacing: -0.02em; }
.ray i { font-family: var(--mono); font-size: 10px; font-style: normal;
         letter-spacing: 0.1em; color: var(--soluk); }
.govde { padding: 14px 16px 16px; min-width: 0; }
.ust { display: flex; align-items: center; gap: 9px; flex-wrap: wrap; }
.ust h3 { font-size: 16px; margin: 0; font-weight: 600; letter-spacing: -0.01em; }
.rozet { font-family: var(--mono); font-size: 10px; letter-spacing: 0.08em;
         border: 1px solid currentColor; border-radius: 4px; padding: 2px 6px; }
.yol { font-family: var(--mono); font-size: 12px; color: var(--soluk);
       margin: 7px 0 0; word-break: break-word; }
.yol b { font-weight: 500; color: var(--murekkep); }
.etiket { font-family: var(--mono); font-size: 10px; letter-spacing: 0.1em;
          color: var(--soluk); margin: 13px 0 5px; }
.metin { background: var(--kutu); border: 1px solid var(--cizgi);
         border-radius: 7px; padding: 11px 13px; max-height: 148px;
         overflow-y: auto; white-space: pre-wrap; font-size: 14px;
         line-height: 1.55; }
.metin.acik { max-height: none; }
.dugmeler { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 11px; }
button, .bag {
  font: inherit; font-size: 13px; padding: 7px 13px; border-radius: 7px;
  border: 1px solid var(--cizgi); background: var(--kart);
  color: var(--murekkep); cursor: pointer; text-decoration: none;
  display: inline-block;
}
button.ana { background: var(--dugme); color: var(--dugme-yazi);
             border-color: var(--dugme); }
button:hover, .bag:hover { border-color: var(--soluk); }
button:focus-visible, .bag:focus-visible { outline: 2px solid var(--proje);
                                           outline-offset: 2px; }
button.oldu { background: var(--urun); border-color: var(--urun);
              color: var(--kart); }
.kart[data-slot="3dbaski"] .rozet { color: var(--3dbaski); }
.kart[data-slot="elektronik"] .rozet { color: var(--elektronik); }
.kart[data-slot="urun"] .rozet { color: var(--urun); }
.kart[data-slot="proje"] .rozet { color: var(--proje); }
.kart[data-tur="REELS"] .rozet { color: var(--reels); }
.kart[data-tur="HİKAYE"] { opacity: 0.86; }
footer { margin-top: 44px; color: var(--soluk); font-size: 13px;
         border-top: 1px solid var(--cizgi); padding-top: 14px; }
@media (max-width: 520px) {
  .kart { grid-template-columns: 1fr; }
  .ray { flex-direction: row; align-items: baseline; gap: 10px;
         border-right: 0; border-bottom: 1px solid var(--cizgi);
         padding: 10px 14px; }
  .govde { padding: 12px 14px 14px; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>

<div class="sayfa">
  <header>
    <h1>Yayın Paketi</h1>
    <p>Kuyruktaki her gönderi, hikaye ve reels yayın sırasına dizili.
       Metni kopyala, klasörü aç, kareleri sırayla yükle.</p>
    <div class="ozet">__OZET__</div>
  </header>
  <div class="sekmeler" id="sekmeler"></div>
  <p class="durum" id="durum"></p>
  <main id="gunler"></main>
  <footer>
    Bu sayfa <b>sira.py</b> ve <b>paket.py</b> ile kuyruktan üretiliyor —
    kuyruk değişince yeniden yayımlanıyor. Kareler depoda:
    sedatisc/instagram-gorseller.
  </footer>
</div>

<script>
const VERI = __VERI__;
const DEPO = "__DEPO__", HAM = "__HAM__";
const KISA = __KISA__;

function kopyala(dugme, metin) {
  const bitti = () => {
    const eski = dugme.textContent;
    dugme.textContent = "Kopyalandı";
    dugme.classList.add("oldu");
    setTimeout(() => { dugme.textContent = eski;
                       dugme.classList.remove("oldu"); }, 1400);
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(metin).then(bitti, () => sec(metin));
  } else { sec(metin); }
}

function sec(metin) {
  const t = document.createElement("textarea");
  t.value = metin; t.style.position = "fixed"; t.style.opacity = "0";
  document.body.appendChild(t); t.select();
  try { document.execCommand("copy"); } catch (e) { t.focus(); return; }
  document.body.removeChild(t);
}

function dugme(yazi, ana, islev) {
  const b = document.createElement("button");
  b.textContent = yazi;
  if (ana) b.className = "ana";
  b.addEventListener("click", () => islev(b));
  return b;
}

function kartCiz(k) {
  const kart = document.createElement("article");
  kart.className = "kart";
  kart.dataset.slot = k.slot; kart.dataset.tur = k.tur;

  const ray = document.createElement("div");
  ray.className = "ray";
  ray.innerHTML = "<b>" + k.saat.replace(":", ".") + "</b><i>" + k.tur + "</i>";
  kart.appendChild(ray);

  const govde = document.createElement("div");
  govde.className = "govde";

  const ust = document.createElement("div");
  ust.className = "ust";
  const h3 = document.createElement("h3");
  h3.textContent = k.baslik;
  ust.appendChild(h3);
  const etiket = k.tur === "REELS" ? "REELS" : (KISA[k.slot] || "");
  if (etiket) {
    const r = document.createElement("span");
    r.className = "rozet"; r.textContent = etiket;
    ust.appendChild(r);
  }
  govde.appendChild(ust);

  const yol = document.createElement("p");
  yol.className = "yol";
  const d = k.dosyalar;
  const liste = d.length > 2 ? d[0] + " – " + d[d.length - 1] : d.join(" · ");
  yol.innerHTML = "klasör <b>" + k.klasor + "</b> · " + liste;
  govde.appendChild(yol);

  const yt = secili === "yt" && k.yt, tt = secili === "tt" && k.tt;
  const anaMetin = yt ? k.yt.aciklama : (tt ? k.tt.metin : k.metin);

  if (yt) {
    const e = document.createElement("div");
    e.className = "etiket"; e.textContent = "BAŞLIK";
    govde.appendChild(e);
    const b = document.createElement("div");
    b.className = "metin"; b.style.maxHeight = "none";
    b.textContent = k.yt.baslik;
    govde.appendChild(b);
  }

  let kutu = null;
  if (anaMetin) {
    const e = document.createElement("div");
    e.className = "etiket";
    e.textContent = yt ? "AÇIKLAMA"
                  : tt ? "TIKTOK METNİ"
                  : (k.tur === "REELS" ? "REELS AÇIKLAMASI" : "GÖNDERİ METNİ");
    govde.appendChild(e);
    kutu = document.createElement("div");
    kutu.className = "metin";
    kutu.textContent = anaMetin;
    govde.appendChild(kutu);
  }

  const sira_ = document.createElement("div");
  sira_.className = "dugmeler";
  if (yt) {
    sira_.appendChild(dugme("Başlığı kopyala", true,
                            b => kopyala(b, k.yt.baslik)));
    sira_.appendChild(dugme("Açıklamayı kopyala", false,
                            b => kopyala(b, k.yt.aciklama)));
    if (k.yt.etiket) {
      sira_.appendChild(dugme("Etiketleri kopyala", false,
                              b => kopyala(b, k.yt.etiket)));
    }
  } else if (anaMetin) {
    sira_.appendChild(dugme("Metni kopyala", true, b => kopyala(b, anaMetin)));
  }
  if (!yt && !tt && k.yorum) {
    sira_.appendChild(dugme("İlk yorumu kopyala", false,
                            b => kopyala(b, k.yorum)));
  }
  if (kutu) {
    sira_.appendChild(dugme("Tamamını göster", false, b => {
      kutu.classList.toggle("acik");
      b.textContent = kutu.classList.contains("acik") ? "Kısalt"
                                                      : "Tamamını göster";
    }));
  }
  sira_.appendChild(dugme("Görsel adreslerini kopyala", false, b =>
    kopyala(b, k.dosyalar.map(f => HAM + k.klasor + "/" + f).join("\\n"))));
  const bag = document.createElement("a");
  bag.className = "bag"; bag.href = DEPO + k.klasor;
  bag.target = "_blank"; bag.rel = "noopener";
  bag.textContent = "Klasörü aç";
  sira_.appendChild(bag);
  govde.appendChild(sira_);

  kart.appendChild(govde);
  return kart;
}

const PLATFORM = [
  ["ig", "INSTAGRAM", "Gönderi, hikaye ve reels. Meta anahtarları depoya " +
   "girene kadar elle paylaşılıyor."],
  ["yt", "YOUTUBE", "Günün reels videosu Short olarak çıkıyor. " +
   "<b>YT_* secret'ları girilince otomatik</b> — kurulum " +
   "otomasyon/YOUTUBE-KURULUM.md."],
  ["tt", "TIKTOK", "<b>Elle paylaşılıyor.</b> TikTok, kendi hesabına yükleyen " +
   "araçlara denetim vermiyor; otomatik hat kurulsa gizli paylaşımda kalırdı. " +
   "Sesi uygulamadan ekle."]
];
let secili = "ig";

const kap = document.getElementById("gunler");
const serit = document.getElementById("sekmeler");
const durum = document.getElementById("durum");

PLATFORM.forEach(([kod, ad]) => {
  const b = document.createElement("button");
  b.className = "sekme"; b.textContent = ad;
  b.setAttribute("aria-pressed", kod === secili);
  b.addEventListener("click", () => { secili = kod; ciz(); });
  serit.appendChild(b);
});

function ciz() {
  [...serit.children].forEach((b, i) =>
    b.setAttribute("aria-pressed", PLATFORM[i][0] === secili));
  durum.innerHTML = PLATFORM.find(p => p[0] === secili)[2];
  kap.textContent = "";
  VERI.forEach(g => {
    const kayit = g.kayitlar.filter(
      k => (k.platform || ["ig"]).indexOf(secili) >= 0);
    if (!kayit.length) return;
    const bol = document.createElement("section");
    bol.className = "gun";
    const h2 = document.createElement("h2");
    h2.innerHTML = g.ad + " <span>" + kayit.length + " kayıt</span>";
    bol.appendChild(h2);
    kayit.forEach(k => bol.appendChild(kartCiz(k)));
    kap.appendChild(bol);
  });
}
ciz();
</script>
"""


def main():
    veri = kayitlar()
    gonderi = sum(1 for g in veri for k in g["kayitlar"] if k["tur"] == "GÖNDERİ")
    hikaye = sum(1 for g in veri for k in g["kayitlar"] if k["tur"] == "HİKAYE")
    reels = sum(1 for g in veri for k in g["kayitlar"] if k["tur"] == "REELS")
    ozet = "".join(
        "<span>%s</span>" % html.escape(x) for x in
        ("%d gün" % len(veri), "%d gönderi" % gonderi, "%d hikaye" % hikaye,
         "%d reels" % reels,
         "%s – %s" % (veri[0]["tarih"], veri[-1]["tarih"]) if veri else ""))
    s = (SAYFA.replace("__VERI__", json.dumps(veri, ensure_ascii=False))
              .replace("__OZET__", ozet)
              .replace("__KISA__", json.dumps(KISA, ensure_ascii=False))
              .replace("__DEPO__", DEPO).replace("__HAM__", HAM))
    yol = os.path.join(KOK, "yayin-paketi.html")
    open(yol, "w", encoding="utf-8").write(s)
    print("%s · %d gün, %d gönderi, %d hikaye, %d reels"
          % (yol, len(veri), gonderi, hikaye, reels))


if __name__ == "__main__":
    main()
