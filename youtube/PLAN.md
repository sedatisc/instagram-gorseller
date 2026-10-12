# YouTube — kendi yapısı

Kanal: **SermenLab** (@sermenlab). Günde **1 Shorts**, saat **18:20**.

Video **ayrı bir kurgudan** çıkıyor: `python3 shorts.py <klasor>` →
`<klasor>/shorts.mp4`. Tamamı için `python3 shorts.py --tumu`.
Yükleyici `shorts.mp4` varsa onu, yoksa `reels.mp4` dosyasını atıyor.

Neden ayrı: Instagram'da insan akışta gezerken denk geliyor, YouTube'da
**arayarak** buluyor. Aynı metin iki yerde aynı işi yapmıyor. Kurgu da
aynı işi yapmıyor — bir ara shorts dosyası reels'in sonuna abone kartı
eklenmiş hâliydi, ekranda hiçbir farkı yoktu ve zayıf iş yapıyordu.

## Kurgu — reels'ten farkı

| | reels.py (Instagram) | shorts.py (YouTube) |
|---|---|---|
| Sahne | ~4 sn, yavaş açılan panel | 1,9 sn, vuruş ızgarasında |
| Ürün | beyaz zeminli kare fotoğraf | arka planı kesilmiş, kadraja taşan |
| Rakam | cümlenin içinde | ekranı dolduruyor, sıfırdan yukarı sayıyor |
| Ses | sessiz | kendi ürettiğimiz ritim (96 BPM) |
| Süre | ~23 sn | 10-13 sn |

Ayrıntılar:

- **Ürün kesiliyor.** `gorsel/urun/kesik-*.png` varsa o kullanılıyor, yoksa
  rembg ile kesilip oraya kaydediliyor. Koyu zeminde beyaz zeminli
  fotoğraf beyaz bir kutu gibi duruyordu.
- **Rakam metinden ayrılıyor.** "55 W CO2 lazer, 600 × 300 mm tezgâh" →
  ekranda dev "55 W", altında cümlenin kalanı. Rakam, modelin adından
  gelmiyorsa (R1, S2, i8) ve bir birimi varsa ayrılıyor; yoksa cümle
  olduğu gibi kelime kelime vuruyor.
- **Kesimler 96 BPM ızgarasında.** Kanca 5 vuruş, her madde 3, kapanış 3.
  Altındaki ritim de aynı tempoda üretiliyor, kesim sese denk geliyor.
- **Ses telifsiz**, çünkü kick/hi-hat/trampet/bas numpy ile burada
  üretiliyor. YouTube'un ses kütüphanesine ya da başkasının parçasına
  ihtiyaç yok. `--sessiz` ile kapatılıyor.
- **Üstte ilerleme çubuğu** var: izleyici videonun kısa olduğunu görüyor.
- Her sahnede ürünün ölçeği ve yeri değişiyor; kadraj baştan sona aynı
  kalırsa video tek kare gibi görünüyor.

## Başlık kuralı

Başlık bir **soru ya da net bir vaat** olacak, arandığı gibi yazılacak.

- 70 karakteri geçmeyecek (telefonda gerisi kesiliyor; API sınırı 100).
- Marka ve model adı başta ya da başa yakın: "Bambu H2S, H2C ve H2D farkı ne?"
- Tıklama tuzağı yok. Videoda olmayan şey başlıkta olmayacak.
- `#Shorts` yazmaya gerek yok — dikey ve 3 dakikanın altındaki video
  YouTube tarafından kendiliğinden Short sayılıyor.
- Büyük harfle bağırma yok. Kısaltmalar olduğu gibi: PLA, CFS, ESR.

## Açıklama kuralı

Sıra sabit:

1. **Kanca** — tek cümle, videonun cevapladığı soru.
2. **Maddeler** — 3-4 satır, videodaki rakamlar.
3. **Kaynak satırı** — rakamlar nereden alındı (üreticinin kendi sayfası).
4. **sermenkreatif.com**
5. En çok **3 hashtag**. Fazlası YouTube'da işe yaramıyor.

Instagram metni buraya olduğu gibi kopyalanmıyor: oradaki metin uzun ve
sohbet dilinde, burada aranan bilgi önce geliyor.

## Etiketler

5 etiket yetiyor: marka, ürün/konu, kategori, `3dbaski` ya da
`elektronik`, `makerturkiye`. Etiketler aramayı belirlemiyor ama yanlış
yazımları yakalıyor.

## Sabit kurallar

- **Stok durumu ve sevkiyat tarihi yazılmıyor.** Instagram'daki kural
  burada da geçerli; video aylarca izleniyor, o bilgi en hızlı bayatlayan
  şey.
- Doğrulanmamış rakam yok. Üreticinin kendi sayfası yoksa o satır yazılmaz.
- **`satirlar` videonun kendisi.** Açıklamaya yazılan o üç dört satır
  aynı zamanda ekrandaki vuruşlar. Rakamla başlayan satır daha iyi iş
  çıkarıyor: "55 W CO2 lazer…" ekranda dev "55 W" oluyor.

## Kuyruğa video ekleme

`youtube/DURUM.json` → `kuyruk` listesine bir kayıt:

```json
{ "tarih": "2026-10-19",
  "klasor": "2026-10-19-bambu-a-serisi-pano",
  "baslik": "A1 mini, A1 ve A2L farkı ne?",
  "kanca": "Üçü de aynı aileden ama aynı işe göre değil.",
  "satirlar": ["Baskı alanı ve hız farkı", "AMS uyumu", "Hangisi kime"],
  "etiket": ["bambulab", "a1mini", "3dyazici", "3dbaski", "makerturkiye"] }
```

`klasor` içinde `spec.json` olmak zorunda; video oradan üretiliyor:

```
python3 shorts.py 2026-10-19-bambu-a-serisi-pano
```

`python3 paket.py` çalıştırınca Yayın Paketi sayfasının YouTube sekmesi
de yenileniyor.

## Sıradaki konular

Instagram planından bağımsız, arama niyetine göre sıralandı. Her biri için
`uret.py` + `reels.py` ile video çıkarılacak.

| # | Başlık adayı | Kaynak klasör |
|---|---|---|
| 1 | A1 mini, A1 ve A2L farkı ne? | 2026-10-19-bambu-a-serisi-pano |
| 2 | Pixhawk 6C mi 6X mi? | 2026-10-20-pixhawk-pano |
| 3 | SparkX i7 mi i8 mi? | 2026-10-20-sparkx-i7-i8-pano |
| 4 | Raspberry Pi kamerası: Module 3, HQ, GS | 2026-10-21-pi-kamera-pano |
| 5 | Purge atmadan çok renk: U1 ve K3 | 2026-10-21-u1-k3-pano |
| 6 | Hangi ESP32: S3, C6, P4 | 2026-10-17-esp32-ailesi-pano |
| 7 | Projeye hangi kart girer? | 2026-10-16-gelistirme-karti-pano |
| 8 | Sertleştirilmiş nozul ne zaman şart? | 2026-10-18-sert-nozul |
| 9 | Kondansatör sağlam görünüp bozuk olur mu? | 2026-10-18-kondansator-esr |
| 10 | Çok renge nasıl geçilir? | 2026-10-17-cok-renkli-yazici-pano |

Bu listeden alınan konu `kullanilan` listesine ekleniyor, tekrar
yayımlanmıyor.
