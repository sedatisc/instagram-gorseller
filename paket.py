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


def baslik(klasor):
    """Kapak manşetinden okunur bir başlık çıkar."""
    yol = os.path.join(KOK, klasor, "spec.json")
    if not os.path.exists(yol):
        return klasor
    k = json.load(open(yol, encoding="utf-8"))["kapak"]
    ham = ("%s %s" % (k.get("satir1", ""), k.get("satir2", ""))).strip()
    if not ham:
        return klasor
    kelime = []
    for i, w in enumerate(ham.split()):
        # PLA, ESR, H2D, i7 gibi kısaltmalar olduğu gibi kalsın
        if len(w) <= 4 or any(c.isdigit() for c in w):
            kelime.append(w)
        elif i == 0:
            kelime.append(w[0] + w[1:].lower())
        else:
            kelime.append(w.lower())
    s = " ".join(kelime)
    return s[0].upper() + s[1:]


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
            kayit.append({"saat": t, "tur": "GÖNDERİ", "slot": ad,
                          "baslik": baslik(kl), "klasor": kl,
                          "dosyalar": kare, "metin": govde or "",
                          "yorum": yorum or ""})
            kayit.append({"saat": sira.arti(t, sira.HIKAYE_GECIKME),
                          "tur": "HİKAYE", "slot": ad, "baslik": baslik(kl),
                          "klasor": kl, "dosyalar": ["hikaye.jpg"],
                          "metin": "", "yorum": ""})
        r = reelsler.get(tarih)
        if r:
            govde, _ = sira.metin_oku(r)
            kayit.append({"saat": sira.saat(g, "reels"), "tur": "REELS",
                          "slot": "", "baslik": baslik(r), "klasor": r,
                          "dosyalar": ["reels.mp4"], "metin": govde or "",
                          "yorum": ""})
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

  let kutu = null;
  if (k.metin) {
    const e = document.createElement("div");
    e.className = "etiket";
    e.textContent = k.tur === "REELS" ? "REELS AÇIKLAMASI" : "GÖNDERİ METNİ";
    govde.appendChild(e);
    kutu = document.createElement("div");
    kutu.className = "metin";
    kutu.textContent = k.metin;
    govde.appendChild(kutu);
  }

  const sira_ = document.createElement("div");
  sira_.className = "dugmeler";
  if (k.metin) {
    sira_.appendChild(dugme("Metni kopyala", true, b => kopyala(b, k.metin)));
  }
  if (k.yorum) {
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

const kap = document.getElementById("gunler");
VERI.forEach(g => {
  const bol = document.createElement("section");
  bol.className = "gun";
  const h2 = document.createElement("h2");
  h2.innerHTML = g.ad + " <span>" + g.kayitlar.length + " kayıt</span>";
  bol.appendChild(h2);
  g.kayitlar.forEach(k => bol.appendChild(kartCiz(k)));
  kap.appendChild(bol);
});
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
