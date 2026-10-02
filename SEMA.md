# SPEC JSON ŞEMASI

`uret.py` bu yapıyı okur. Çizim koordinatları **1912 × 940** tuvalindedir; üretici çizimi otomatik kırpıp panele ortalar, boş kenarları kendisi ayarlar. Koordinatları kafana göre ver, ölçek derdi yok — yalnız oranları koru.

```json
{
  "kategori": "elektronik | 3dbaski | proje",
  "kapak": {
    "tip": "klasik | rakam | carpisma | yakin | izgara",
    "satir1": "BEYAZ SATIR",
    "satir2": "RENKLİ SATIR",
    "spot": "Bir iki cümlelik kanca.",
    "rozetler": [["metin", "tema"], ["metin", "turuncu"], ["metin", "yesil"]],
    "cizim": [ ... ],
    "tablo": [["ETİKET", "değer"], ...]
  },
  "slaytlar": [
    {
      "baslik": "Adım başlığı",
      "aciklama": "İki cümle.",
      "vurgu": [x0, y0, x1, y1],
      "cizim": [ ... ]
    }
  ],
  "kapanis": {
    "satir1": "HANGİSİNİ",
    "satir2": "ALMALISIN?",
    "kriterler": [["KRİTER", "cevap"], ...],
    "not": "Tek cümle."
  }
}
```

Slaytta `cizim` veya `tablo` yoksa kapaktaki görsel kullanılır, yalnız `vurgu` değişir. Rehber gönderilerde doğru kullanım budur: tek çizim, üç farklı vurgu.

`kapanis` yalnız liste gönderilerinde bulunur.

## Kapak tipleri

- **`klasik`** — başlık üstte, panel altta. `satir1`, `satir2`, `spot`.
- **`rakam`** — dev sayı kapağı. `ustbilgi` (küçük üst etiket), `rakam` (dev metin: `%15`, `4,7 kΩ`, `0,2 mm`), `rakam_alt` (ne anlama geldiği), `spot`.
- **`carpisma`** — çapraz bölünmüş karşılaştırma. `satir1`, `satir2`, `sol_etiket`, `sag_etiket`, `sol_metin`, `sag_metin`, `spot`.
- **`yakin`** — çizim büyütülüp kenarlardan taşırılır. `satir1`, `satir2`, `spot`, ayrıca `cizim`/`tablo` ve `vurgu`.
- **`izgara`** — kopya kâğıdı. `satir1`, `satir2`, `spot`, `kartlar`. Her kart: `etiket` (küçük başlık), `deger` (dev sarı rakam), `alt` (bir iki satır açıklama), `renk`, isteğe bağlı `durum` (`dogru` / `yanlis` rozeti) ve `genis` (tam satır kaplar). 5-7 kart ideal; ara slaytlar kart listesinden otomatik tablo üretir.

Arka arkaya aynı tipi kullanma.

Rozet rengi: `tema` (kategori rengi), `turuncu`, `yesil`, `sari`, `kirmizi`, `gri`, `mavi`, `beyaz`.

## Çizim öğeleri

| Tip | Alanlar | Ne çizer |
|---|---|---|
| `w` | `p: [[x,y],[x,y],...]` | İletken (dik açı kullan, çapraz kaçın) |
| `n` | `x, y` | Düğüm noktası |
| `r` | `x, y, yon: h\|v, ad, deger, etiket: ust\|alt\|sol\|sag` | Direnç (turuncu) |
| `c` | `x, y, yon: v\|h, ad, deger` | Kondansatör (yeşil) |
| `g` | `x, y, b` | Toprak |
| `t` | `x, y, metin` | Besleme ucu (`+12V`) |
| `k` | `x0, y0, x1, y1, metin` | IC / modül kutusu (mavi) |
| `d` | `x, y, metin, renk` | Rozet (`YANLIŞ` / `DOĞRU`) |
| `y` | `x, y, metin, boy, renk, hiza` | Serbest yazı |
| `s` | `x, y, yon: v\|h, h\|w, ad, deger` | Anahtar / buton (açık konumda) |
| `renk` | `x, y, w, h, hex, ad` | Renk kartelası karesi (filament tanıtımı) |
| `cizgi` | `x0, y0, x1, y1` | Ayraç çizgisi |

Yatay direnç 240 × 76, dikey 76 × 240. `x, y` sol üst köşedir.

## Kurallar

- Bir çizimde en fazla 9 ayrık bileşen + 1 modül. Fazlası 1080 px genişlikte okunmaz; ikiye böl, iki adıma yay.
- Karşılaştırma (yanlış/doğru) için iki devreyi yan yana çiz, aralarına `cizgi` koy, üstlerine `d` rozeti.
- Fotoğraf yok. Şemaya uymayan konularda `tablo` kullan — 3D baskı ve proje kategorilerinin çoğu böyle.
- `vurgu` dikdörtgeni anlatılan bileşeni ve etiketlerini içine alsın; dışarıda kalan her şey söner.
