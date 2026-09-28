# ÇALIŞMA TALİMATI

Bu depo @sermenkreatif Instagram hesabının içerik üretim hattıdır. Bu dosyayı okuyan oturumun önceki konuşmalardan haberi yoktur; ihtiyacı olan her şey bu depodadır.

## Görev

Metricool kuyruğunda **her zaman 5 günlük gönderi** bulunacak şekilde eksikleri tamamla. Her gün 3 gönderi: sabah 3D baskı, öğle elektronik, akşam proje.

## Sabitler

- Metricool blogId: `7137084`
- Zaman dilimi: `Europe/Istanbul`
- Instagram: `@sermenkreatif` (işletme hesabı, Facebook sayfasına bağlı)
- Görsel barındırma: bu depo. Adres kalıbı:
  `https://raw.githubusercontent.com/sedatisc/instagram-gorseller/main/<klasör>/<n>.png`

## Adımlar

**1. Kuyruğu oku.** `getScheduledPosts` ile bugünden 6 gün sonrasına kadar bak. Hangi gün hangi slotun boş olduğunu çıkar.

**2. Eksikleri belirle.** Bugün dahil 5 gün içinde boş olan her slot doldurulacak. Geçmiş saatler doldurulmaz. Bir çalışmada en fazla 9 gönderi üret; kalanı ertesi günün çalışması tamamlar.

**3. Konu seç.** `DURUM.json` içindeki `kullanilan` listesine bak. `PLAN.md` içindeki ilgili kategori tablosundan **kullanılmamış en küçük numaralı** konuyu al.

**4. Slayt üret.** Konuya göre bir spec JSON yaz (şema: `SEMA.md`), sonra:
```
python3 uret.py <spec.json> <YYYY-AA-GG-slug>/
```
Slaytlar `1.png`, `2.png` … diye çıkar. Slayt sayısı `PLAN.md`'deki tür sütununa uyacak: rehber 4, liste ise başlıktaki sayı + kapak + kapanış.

**5. Depoya yükle.** Klasörü commit edip push et. Sonra her adresi `curl -sI` ile doğrula, hepsi 200 dönmeli.

**6. Kuyruğa ekle.** `createScheduledPost` ile:
- `media`: raw adresler, slayt sırasıyla
- `mediaAltText`: her slayt için ayrı alt metin, aynı sırada
- `providers`: `[{"network": "instagram"}]`
- `instagramData`: `{"type": "POST", "showReelOnFeed": true}`
- `autoPublish`: `true`
- `publicationDate`: `{"dateTime": "...", "timezone": "Europe/Istanbul"}`
- `firstCommentText`: konuyu bir adım ileri taşıyan tek cümle

**7. Durumu güncelle.** `DURUM.json` içindeki `kullanilan` listesine konu numarasını ekle, commit ve push et. Bu adım atlanırsa ertesi gün aynı konu tekrar üretilir.

## Paylaşım saatleri

| Slot | Kategori | Hafta içi | Cumartesi | Pazar |
|---|---|---|---|---|
| Sabah | 3dbaski | 08.12 | 11.10 | 11.40 |
| Öğle | elektronik | 12.38 | 12.20 | 12.20 |
| Akşam | proje | 20.42 | 20.10 | 21.00 |

Gün bazlı kaymalar: pazartesi akşamı 19.40 · cuma akşamı 18.10 · çarşamba akşamı haftanın en iyi slotu, oraya listenin en iddialı konusu gelsin.

## Metin kuralları

**Hashtag tam 5 tane.** Instagram sınırı bu, fazlası kırpılıyor. Dizilim:
`#sermenkreatif` + kategori + topluluk + konu + `#makerturkiye`
Kategori etiketi: `#3dbaski` · `#elektronik` · `#maker`
Türkçe karakter kullanma: `#3dbaski`, `#3dbaskı` değil.

**Açıklama metni.** İlk cümlede aranabilir terim birebir geçsin ("ESP32 deep sleep akım ölçümü" gibi) — erişimi hashtag değil bu taşıyor. 4-8 satır. Sonunda çağrı: "kaydet" değil, **"bu … olan bir arkadaşın varsa ona yolla"**. Gönderme sinyali algoritmada en ağır basan şey.

**Yazım.** Marka, model ve protokol adları çevrilmez ve olduğu gibi yazılır: ESP32, Raspberry Pi, PETG, MOSFET, MQTT, I2C, PLA, STL, slicer, firmware. Türkçesi yerleşmiş terimlerde Türkçe kullanılır: direnç, kondansatör, katman, dolgu, duvar.

Kesme işareti okunuşa göre: ESP32'ye, PLA'yı, PETG'yi, STL'yi, I2C'de, MOSFET'in. Cins isimde ek ayrılmaz: dirençler, katmanda.

Sayı ve birim arasında boşluk, ondalıkta virgül: `100 kΩ`, `0,2 mm`, `210 °C`, `%15`.

Slayt başlıklarında yalnız ilk kelime ve özel adlar büyük.

## Ürün gönderileri

`PLAN.md`'de **Ürün:** ile başlayan konularda, yazmadan önce web'de ara ve doğrula. Model adları ve ürün gamları hızlı değişiyor.

- Fiyat yazma. Konumlandırma yaz ("giriş seviyesi", "kapalı kabinli orta sınıf"), fiyat için sermenkreatif.com'a yönlendir.
- Ürünün durumunu ayır: **duyuruldu** (özellik yok), **fuarda gösterildi** (özellik açık, satış yok), **satışta**. Duyuru aşamasındakini karşılaştırmaya sokma; fuar aşamasındakini sok ama "şu an alınamıyor, tarih şu" diye yaz.
- Üretici basın görseli kullanma, telifli. `tablo` paneli veya `renk` öğesi kullan.
- Geçen markanın hesabını açıklamada etiketle: `@bambulab`, `@sunlu3d`, `@snapmaker`, `@creality3dofficial`.

## Sınırlar

- Konu listesi bittiğinde yeni gönderi üretme. Çalışmayı bitir ve listenin tükendiğini bildir.
- Bir slotu asla iki kez doldurma; önce `getScheduledPosts` ile kontrol et.
- Görsel adresi 200 dönmüyorsa o gönderiyi kuyruğa ekleme, sonraki çalışmaya bırak.
- Yayınlanmış gönderiyi silme veya değiştirme.
