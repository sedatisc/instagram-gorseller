# Görsel araçları

## Tasarım sistemi — `arac/html/sistem.py`

Kare üretimi iki motorda yapılıyor: eski rehber/teknik gönderileri
Pillow'da (`uret.py`), ürün ve kampanya kareleri tarayıcıda. Renk, font
ve ortak parçalar `arac/html/sistem.py` içinde tek yerde duruyor; renk
adları `uret.py`deki palette birebir aynı, yani `spec.json` içinde
`"renk": "yesil"` yazınca iki motor da aynı yeşili veriyor.

| Jeton | Değer | Nerede |
|---|---|---|
| `KAGIT` | `#eef2f8` | açık karelerin zemini |
| `ZEMIN` | `#ffffff` | ürün kesimlerinin ortak zemini |
| `LACI` | `#121a30` | koyu kare, bant ve cip |
| `MUREKKEP` / `SOLUK` | `#101626` / `#68748b` | ana ve ikincil yazı |
| `RENK[...]` | 9 vurgu rengi | kategori, şerit, rozet |

Fontlar (`Anton`, `Pop`, `Mono`) base64 ile HTML'in içine gömülüyor:
hem Chromium sistem fontuna düşmüyor, hem de aynı HTML Adobe Express'e
aktarıldığında yazı bozulmuyor. Baskı `sistem.bas()` ile yapılıyor,
çıktı her zaman JPEG — Instagram Graph API'si `/media` ucunda PNG
kabul etmiyor.

Neden tarayıcı: yazı bloğunun kaç satır tuttuğunu, kalan yeri kimin
dolduracağını Pillow'da piksel sayarak hesaplıyorduk; bir cümle uzayınca
altta avuç içi kadar boşluk kalıyor ya da yazı taşıyordu. Yerleşim
motoru bunu kendisi yapıyor.

## kart_html.py — ürün kartı şablonu

```
python3 arac/kart_html.py <spec.json> <cikti-klasoru>
```

`spec.json` içinde ürünün yalnız `slug`ı ve bir cümlesi yazılıyor; ad,
fiyat, fotoğraf ve özellikler `otomasyon/urun-bilgi.json`dan geliyor.
Çıkan kareler: kapak (`1.jpg`), her ürün için bir kare, kapanış listesi
ve `hikaye.jpg`.

- Ürün fotoğrafları `rembg` ile kesilip tek zemine oturuyor; kesim
  `gorsel/urun/kesik/` altında saklanıyor, iki motor aynı PNG'yi
  paylaşıyor. Kesim istenmiyorsa spec'e `"kesim": false`.
- Kapak ızgarası ürünlerin ortanca en/boy oranına göre seçiliyor:
  yatık ürünler (yazıcı, makara) az sütunlu geniş hücreye, dik ürünler
  (saksı, vazo) üç sütuna gidiyor.
- Fiyat varsayılan olarak **yazılmıyor**. Gönderide fiyat donup kalıyor,
  mağazada değişince kare yanlış kalıyor. Açmak için spec'e
  `"fiyat": true`.
- Stok ve sevkiyat bilgisi şablonda hiç yok, eklenmeyecek.

## afis_html.py — kampanya afişi

```
python3 arac/afis_html.py <spec.json> <cikti.jpg> [--html <dosya>]
```

Üç kategorili bayi afişi düzeni: üstte konturlu başlık ve eğik kurdele,
ortada üç renkli panel, altta teklif ve güven şeritleri. Örnek spec
`ornek/afis-ornek.json`.

`teklif` boşsa şerit boş bırakılmıyor, yerine mağaza şeridi geçiyor —
afişin ortasında delik kalmasın diye. İndirim yazılacaksa indirimden
önceki en düşük fiyatın da gösterilmesi gerekiyor.

`--html` ile üretilen dosya kendi kendine yeten tek sayfa: font ve
görseller içine gömülü, dışarıya bağlanmıyor.

---

Aşağıdakiler afiş ya da sahne fotoğrafından stüdyo ürün karesi çıkarmak
için.

## studyo.py — ürünü kendi zeminine oturt

Arka planı temizlenmiş PNG'leri alıp 1080 × 800 stüdyo karesi kuruyor:
degrade zemin, üstten ışık, temas gölgesi ve yere yansıma. Birden fazla
ürün verilirse boyları eşitleyip yan yana diziyor.

```
python3 arac/studyo.py <cikti.jpg> <ustHEX> <altHEX> <vurguHEX> <png...>
python3 arac/studyo.py gorsel/urun/x.jpg 2a2f3a 0c0e14 7a93b4 a.png b.png
```

Renkleri gönderinin `zemin` paletine yakın seç, kare sayfaya otursun.
Tek ürünlü karelerde `doluluk` 0,80 civarı iyi; uzun ince üründe 0,70.

## Arka planı temizleme

İki yol var, hangisinin işe yaradığı fotoğrafa bağlı:

**rembg** — karışık sahnelerde (tezgâh üstü, atölye) iyi çalışıyor.
`pip install --break-system-packages rembg onnxruntime`, model ilk
çalıştırmada GitHub'dan iniyor.

```python
from rembg import remove, new_session
remove(Image.open("x.jpg").convert("RGB"), session=new_session("u2net"))
```

**Parlaklık eşiği** — açık zeminde koyu ürün varsa rembg ürünün koyu
kısmını atabiliyor (Liber hotend'in soğutucusunda oldu). O durumda maskeyi
parlaklıktan çıkarmak daha doğru:

```python
L = 0.2126*r + 0.7152*g + 0.0722*b
mask = clip((205 - L) / 55, 0, 1)
```

Kesimden sonra alt kenardaki zemin şeridini kırp, yoksa yansımada
dikdörtgen artık kalıyor.

## hazirla.py · serit.py

`hazirla.py` konuyu zeminden ayırıp hedef tuvale oturtuyor (kapak
kadrajı için). `serit.py` birkaç kareyi ortak yükseklikte yan yana
diziyor. İkisi de arka plan temizlemeden çalışıyor; stüdyo karesi
gerekmiyorsa bunlar yeterli.
