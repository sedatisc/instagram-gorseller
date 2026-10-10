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
| 1 | Kablosuz seçimi | Wi-Fi · BLE · LoRa | 3 modül |
| 2 | Motor sürücü sınıfı | DRV8833 · BTS7960 · ayrık MOSFET | 3 modül/kart |
| 3 | Güç kaynağı | lineer · buck · buck-boost | 3 modül |
| 4 | Sensör ailesi | DHT22 · BME280 · SHT41 | 3 sensör |
| 5 | Uçuş/sürüş kontrol | Pixhawk 6C · SpeedyBee F405 · Arduino | 3 kart |
| 6 | Ekran seçimi | OLED · TFT · e-ink | 3 ekran |
