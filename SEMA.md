# SPEC JSON ŞEMASI

`uret.py` bu yapıyı okur. Çizim koordinatları **1912 × 940** tuvalindedir; üretici çizimi otomatik kırpıp panele ortalar, boş kenarları kendisi ayarlar. Koordinatları kafana göre ver, ölçek derdi yok — yalnız oranları koru.

```json
{
  "kategori": "elektronik | 3dbaski | proje",
  "kapak": {
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
| `renk` | `x, y, w, h, hex, ad` | Renk kartelası karesi (filament tanıtımı) |
| `cizgi` | `x0, y0, x1, y1` | Ayraç çizgisi |

Yatay direnç 240 × 76, dikey 76 × 240. `x, y` sol üst köşedir.

## Kurallar

- Bir çizimde en fazla 9 ayrık bileşen + 1 modül. Fazlası 1080 px genişlikte okunmaz; ikiye böl, iki adıma yay.
- Karşılaştırma (yanlış/doğru) için iki devreyi yan yana çiz, aralarına `cizgi` koy, üstlerine `d` rozeti.
- Fotoğraf yok. Şemaya uymayan konularda `tablo` kullan — 3D baskı ve proje kategorilerinin çoğu böyle.
- `vurgu` dikdörtgeni anlatılan bileşeni ve etiketlerini içine alsın; dışarıda kalan her şey söner.
