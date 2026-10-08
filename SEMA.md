# SPEC JSON ŞEMASI

`uret.py` bu yapıyı okur. Çizim koordinatları **1912 × 940** tuvalindedir; üretici çizimi otomatik kırpıp panele ortalar, boş kenarları kendisi ayarlar. Koordinatları kafana göre ver, ölçek derdi yok — yalnız oranları koru.

```json
{
  "kategori": "elektronik | 3dbaski | proje",
  "zemin": "koyu | acik | indigo | kobalt | okyanus | orman | mor | kiraz",
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

Slaytta `foto` alanı varsa o slayt fotoğraflı dizilir: üstte banda oturan fotoğraf (alt kenarı zemine eriyor), altında başlık, açıklama ve `satirlar` künyesi (`[["ETİKET","değer"], ...]`, en çok 6). `bant` ile fotoğrafın yüksekliği değişiyor (varsayılan 628). Fotoğraf yoksa yine yer tutucu basılıyor.

Slaytta `foto`, `cizim` veya `tablo` yoksa kapaktaki görsel kullanılır, yalnız `vurgu` değişir. Rehber gönderilerde doğru kullanım budur: tek çizim, üç farklı vurgu.

`kapanis` yalnız liste gönderilerinde bulunur.

## Kapak tipleri

- **`klasik`** — başlık üstte, panel altta. `satir1`, `satir2`, `spot`.
- **`rakam`** — dev sayı kapağı. `ustbilgi` (küçük üst etiket), `rakam` (dev metin: `%15`, `4,7 kΩ`, `0,2 mm`), `rakam_alt` (ne anlama geldiği), `spot`.
- **`carpisma`** — çapraz bölünmüş karşılaştırma. `satir1`, `satir2`, `sol_etiket`, `sag_etiket`, `sol_metin`, `sag_metin`, `spot`.
- **`yakin`** — çizim büyütülüp kenarlardan taşırılır. `satir1`, `satir2`, `spot`, ayrıca `cizim`/`tablo` ve `vurgu`.
- **`liste`** — sıralı liste. `satir1`, `satir2`, `spot`, `satirlar`, isteğe bağlı `gorsel`. Her satır: `etiket`, `deger`, `ikon`, `renk`. Solda ikonlu satırlar, sağda görsel. `gorsel` alanı `gorsel/` klasöründeki bir dosyayı gösteriyorsa o görsel kullanılıyor (bkz. `gorsel/BENIOKU.md`); yoksa her satır için bir blok barındıran izometrik kule çiziliyor. 5-10 satır. "N tane şey" gönderilerinin kapağı bu.
- **`urun`** — gerçek ürün fotoğrafı tam kareyi kaplıyor, yazı fotoğrafın üstünde duruyor. `gorsel` (zorunlu, `gorsel/` içindeki dosya adı), `ustbilgi`, `satir1`, `satir2`, `spot`, `ozet` (2-3 gözlü künye şeridi: `[["ALAN","600×300 mm"], ...]`), isteğe bağlı `odak` (0-1, dikey kırpma noktası; 0 üst, 1 alt, varsayılan 0,38). Hikaye de aynı fotoğraftan tam boy üretiliyor. **Fotoğraf yoksa vektör çizime düşmüyor:** kareye "FOTOĞRAF YOK" ve beklenen dosya adı basılıyor, üretici de uyarı yazdırıyor. Yalnız ürün tanıtımlarında kullan.
- **`izgara`** — kopya kâğıdı. `satir1`, `satir2`, `spot`, `kartlar`. Her kart: `etiket` (küçük başlık), `deger` (dev sarı rakam), `alt` (bir iki satır açıklama), `renk`, `ikon`, isteğe bağlı `durum` (`dogru` / `yanlis` rozeti) ve `genis` (tam satır kaplar).

Simge listesi: `katman` (katman yığını) · `nozzle` · `makara` (filament makarası) · `kup` (dolgulu küp) · `isi` (ısı dalgaları) · `hiz` · `duvar` (iç içe duvarlar) · `tabla` (ısıtıcı tabla) · `uyari` · `zaman` · `cip` (IC) · `pil` · `dalga` (sinyal) · `damla` · `terazi` (karşılaştırma) · `dis` (dişli) · `olcu` (cetvel) · `soru`

Renkler: `tema` · `turuncu` · `kirmizi` · `mavi` · `yesil` · `mor` · `sari` · `gri` · `beyaz`. Her kart farklı renkte olsun. 5-7 kart ideal; ara slaytlar kart listesinden otomatik tablo üretir.

Arka arkaya aynı tipi kullanma.

## Zemin

`zemin` tüm slaytları ve hikayeyi birlikte değiştirir:

- `koyu` — varsayılan. Siyaha yakın zemin, neon huzmeler.
- `acik` — aydınlık zemin, koyu yazı. Panel beyaza döner, şema koyu mürekkeple çizilir, kart rakamları kartın kendi rengini alır.
- `indigo` · `kobalt` · `okyanus` · `orman` · `mor` · `kiraz` — doygun renk zemin. Her biri kendi vurgu rengini getirir; kategori rengi yalnız logo şeridinde kalır.

Renk uyumu otomatik: kart renkleri, iletkenler ve panel zemine göre açılıp koyulaşıyor. Spec'te renk ayarı yapmaya gerek yok.

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
