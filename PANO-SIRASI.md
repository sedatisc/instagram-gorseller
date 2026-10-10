# Pano gönderi sırası

Her biri tek kare `pano`, üç sütun. İçerik araştırması bende, fotoğraf
sende. Fotoğraf gelmezse sütunda simge çıkıyor — çalışıyor ama zayıf
duruyor, ürün karesi her zaman daha iyi.

## Filament ve malzeme

| # | Konu | Sütunlar | Gereken fotoğraf |
|---|---|---|---|
| ✓ | Filament kurutucu | S2 · S4 · E2 | tamam |
| ✓ | HT-PLA serisi | HT-PLA · Gradient · GF | tamam |
| 1 | Temel üçlü | PLA · PETG · ABS | 3 makara |
| 2 | ASA ne zaman tercih edilir | UV · dış mekân · sıcaklık | 1 makara + 2 basılmış parça |
| 3 | Elyaf takviyeliler | PLA-CF · PETG-CF · PA-CF | 3 makara |
| 4 | TPU sertlikleri | 95A · 85A · yumuşak | 3 makara ya da 3 esnek parça |
| 5 | Çözünür destek | PVA · BVOH · breakaway | 3 makara |
| 6 | Yüksek sıcaklık | ABS · ASA · PC | 3 makara |
| 7 | Görünüm serileri | Matte · Silk · Wood | 3 makara ya da 3 basılmış parça |
| 8 | Nozul seçimi | 0,2 · 0,4 · 0,8 mm | 3 nozul yakın plan |

Sütun başına bir fotoğraf yeterli. Basılmış parça fotoğrafı makara
fotoğrafından daha iyi çalışıyor — izleyici sonucu görüyor.

Fotoğraf şartları `gorsel/BENIOKU.md` içinde. Bir konunun üç
fotoğrafı gelince o gönderiyi üretip pushluyorum.

## Elektronik kart ve modül

"Bu kart ne işe yarar" sorusu pano formatına birebir oturuyor: üstte
künye, altta kullanım alanları. Rakamlar üreticinin kendi ürün
sayfasından alınacak, hafızadan yazılmayacak. Kart fotoğrafları için
önce üreticinin GitHub dokümantasyon deposuna bak (`gorsel/BENIOKU.md`).

| # | Konu | Sütunlar | Gereken fotoğraf |
|---|---|---|---|
| ✓ | Projeye hangi kart girer | Pico 2 W · ESP32-S3 · Pi 5 | tamam — üretici GitHub deposundan |
| ✓ | Hangi ESP32 | S3 · C6 · P4 | tamam — esp-dev-kits deposundan |
| 1 | Kablosuz seçimi | Wi-Fi · BLE · LoRa | 3 modül |
| 2 | Motor sürücü sınıfı | DRV8833 · BTS7960 · ayrık MOSFET | 3 modül/kart |
| 3 | Güç kaynağı | lineer · buck · buck-boost | 3 modül |
| 4 | Sensör ailesi | DHT22 · BME280 · SHT41 | 3 sensör |
| ✓ | Uçuş kontrol kartı | Pixhawk 6C · 6C mini · 6X | tamam — PX4 deposundan (CC BY 4.0) |
| ✓ | Raspberry Pi kamerası | Module 3 · HQ · GS | tamam — rpi deposundan |
| 6 | Ekran seçimi | OLED · TFT · e-ink | 3 ekran |

## Pano ne değildir

Pano **tek bir seçim sorusunun** formatı: "bunlardan hangisi benim
işime?" Üç sütun, aynı türden üç seçenek, aralarından biri seçiliyor.

Pano **vitrin değildir.** Birbiriyle yarışmayan ürünleri yan yana
dizmek karşılaştırma gibi görünüyor ama değil; okur "hangisini
alayım" diye bakıyor, cevap çıkmıyor.

Yapılan hata (10 Ekim 2026): iki SUNLU kurutucunun yanına Phaetus
hotend konup "baskıyı bozan üç sorun" denildi. Kurutucuyla hotend
birbirinin alternatifi değil. Gönderi kaldırıldı.

Sütunlar şu testi geçmeli: **hepsi aynı soruya verilen farklı
cevaplar mı?** Değilse pano değil, ya ayrı ayrı ürün gönderisi ya da
karusel rehber olur.

**Sütun sayısı üç olmak zorunda değil.** İki sütun da düzgün
çıkıyor ve bazen doğrusu o: aynı sınıftan olmayan bir ürünü üçüncü
sütuna doldurmak karşılaştırmayı bozuyor. 10 Ekim 2026'da SPARKX i7/i8
panosuna Creality K3 konulmuştu — K3 nozul değiştirici bir üst sınıf
makine, SparkX'lerle aynı soruyu cevaplamıyor. Çıkarıldı ve kendi
mekanizma eşleşmesiyle (Snapmaker U1) ayrı panoya alındı.

Mağaza ürünlerinin tanıtımı zaten `urun` tipli karusel gönderilerle
yapılıyor (10-14 … 10-17). ÜRÜN & MAĞAZA slotu için ayrıca pano
gerekmiyor.

## Yazıcı ve makine

| # | Konu | Sütunlar | Durum |
|---|---|---|---|
| ✓ | Çok renge nasıl geçilir | AD5X · SPARKX i7 · H2D | tamam |
| ✓ | Bambu H serisi | H2S · H2C · H2D | tamam |
| ✓ | Bambu A serisi | A1 mini · A1 · A2L | tamam |
| ✓ | SPARKX i7 mi i8 mi | i7 · i8 | tamam — iki sütun; i8 fotoğrafı İlhan'dan |
| ✓ | Purge atmadan çok renk | Snapmaker U1 · Creality K3 | tamam — iki sütun; K3 fotoğrafı İlhan'dan, makine hâlâ sevkiyatta değil |
| 1 | Reçine yazıcılar | Mono M7 Pro · M7 Max · Mars 5 Ultra | görseller hazır |
| 2 | Creality K2 ailesi | K2 · K2 Pro · K2 Plus | görsel gerek |

## Doğrulamada elenen konular

- **Ender-3 V3 Mega** — Creality'nin hiçbir kendi kaynağında yok;
  kendi karşılaştırma sayfasında V3 serisi Plus / V3 / KE / SE'den
  ibaret. Dolaşan 420 mm küp / 1.150 W değerleri yalnız üçüncü taraf
  SEO sitelerinde. 10 Ekim 2026'da gönderi iptal edildi, yerine
  **Ender-3 V4 Combo** yapıldı (220 × 220 × 235 mm, 500 mm/s,
  12.000 mm/s², CFS 4 slot — rakamlar üreticinin kendi sayfasından,
  makine mağazada satılıyor).
- **K3 Combo** — Creality'de böyle bir paket adı yok; K3'ün kendisi de
  sevkiyatta değil ve teknik verisi yayınlanmadı.
- **SparkX i8** — gerçek ama Indiegogo kampanyası, perakende satışta
  değil. "Alınabilir" diye sunulmayacak.

## Denenip çıkmayanlar

Fotoğraf aramak için boşuna tekrar bakma:

- **Bambu Lab** (`bambulab/BambuStudio`) — yazıcı görselleri var ama
  dilimleyici arayüzü için, 104 × 104 piksel. Panoda kullanılamaz.
- **Prusa** (`prusa3d/Prusa-Firmware-Buddy`) — yalnız doküman ekran
  görüntüleri, ürün fotoğrafı yok.
- **Voron** (`VoronDesign/Voron-Documentation`) — tek bir yazıcı
  fotoğrafı var, üçlü pano çıkmıyor; ayrıca depo GPL-3.0.

Yani **yazıcı ve filament tarafının fotoğrafı İlhan'dan gelecek.**
Elektronik tarafı (Raspberry Pi, Espressif, PX4/Pixhawk) kendi
depolarından çıkıyor.
