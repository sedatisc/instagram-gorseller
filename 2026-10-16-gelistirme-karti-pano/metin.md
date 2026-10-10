## Gönderi metni

"Hangi kartı alayım" sorusunun cevabı güçte değil, işin ne olduğunda. Üçü de geliştirme kartı ama üçü ayrı sınıf.

**Raspberry Pi Pico 2 W** » RP2350, iki Cortex-M33 çekirdek 150 MHz'de (istersen aynı yongadaki RISC-V çekirdekleri de seçebiliyorsun). 520 KB SRAM, 4 MB flash. Wi-Fi 4 ve Bluetooth LE var. 26 GPIO, 4 ADC, 1,8-5,5 V ile besleniyor.

Nerede kullanılır: sensör okuyup veri yollayan düğüm, pille aylarca çalışması gereken iş, röle/motor/şerit LED sürme. İşletim sistemi yok, kod doğrudan donanımda koşuyor — açılış anında hazır.

**ESP32-S3** » iki Xtensa LX7 çekirdek 240 MHz'de, 512 KB dahili SRAM, 45 GPIO (14'ü dokunmatik olabiliyor). Wi-Fi 4 ve Bluetooth 5 LE. Farkı yaratan şey vektör komutları: ESP-NN ve ESP-DSP ile sinir ağı ve sinyal işleme kart üstünde dönüyor.

Nerede kullanılır: kameralı robot ve görüntü aktarma, Wi-Fi'li ev otomasyonu ve MQTT, kart üstünde ses ya da görüntü tanıma. Pico'nun yapamadığı yer burası; Pi'nin fazla geldiği yer de.

**Raspberry Pi 5** » BCM2712, dört Cortex-A76 çekirdek 2,4 GHz'de. 1'den 16 GB'a kadar LPDDR4X. Çift bant Wi-Fi 5, Bluetooth 5.0, Gigabit Ethernet, iki USB 3.0, PCIe 2.0. Çift 4K çıkış.

Nerede kullanılır: kiosk ve medya kutusu, NVMe diskli yerel sunucu (PCIe için ayrı HAT gerekiyor), kamera + yapay zekâ, ROS çalıştıran robot. Bu bir bilgisayar, mikrodenetleyici değil.

Dikkat » Pi 5 5 V / 5 A USB-C istiyor. Telefon şarj cihazıyla çalıştırmaya kalkarsan yük bindiğinde kapanıyor. Pille taşınabilir iş kuracaksan Pi 5 yanlış kart.

Karar kısaca: sensör okuyup veri yolluyorsan Pico 2 W. Kablosuzun üstüne kamera ya da ses biniyorsa ESP32-S3. İşletim sistemi gerekiyorsa Pi 5.

Projesine Pi 5 koyup pille çalıştırmaya uğraşan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #raspberrypi #esp32 #makerturkiye

## İlk yorum

Rakamlar üreticilerin kendi ürün sayfalarından. Fiyat yazmadım, en hızlı eskiyen bilgi o. Kart görselleri Raspberry Pi ve Espressif'in kendi dokümantasyonundan, CC BY-SA 4.0 ile: creativecommons.org/licenses/by-sa/4.0

## Kaynak

Rakamlar:
- Raspberry Pi Pico 2 W — https://www.adafruit.com/product/6087
- ESP32-S3 — https://www.espressif.com/en/products/socs/esp32-s3
- Raspberry Pi 5 — https://www.raspberrypi.com/products/raspberry-pi-5/

Görseller (ikisi de CC BY-SA 4.0, atıf zorunlu):
- Pico 2 W ve Raspberry Pi 5 — github.com/raspberrypi/documentation
- ESP32-S3-DevKitC-1 — github.com/espressif/esp-dev-kits

## Lisans uyarısı — paylaşmadan önce oku

Bu iki fotoğraf telifsiz değil, **CC BY-SA 4.0**. İki şart var:

1. **Atıf** — kaynağı ve lisansı belirtmek zorunlu. İlk yoruma koydum.
2. **Aynı lisansla paylaşma (ShareAlike)** — fotoğrafı işleyip ürettiğim bu pano "türetilmiş eser" sayılıyor; harfiyen uygulanırsa panonun kendisinin de CC BY-SA 4.0 ile paylaşılması gerekiyor. Ticari bir mağaza gönderisinde bu zorlayıcı bir şart.

Pratikte sektörde bu fotoğraflar atıfla yaygın kullanılıyor ama risk sıfır değil. Üç temiz yol var:

- Kartlar stokta ya da elinde varsa kendi fotoğrafını çek — en temizi.
- Raspberry Pi ve Espressif'in basın (press kit) birimlerinden görsel iste; basın görselleri genelde daha serbest şartlarla veriliyor.
- Gönderiyi atıfla yayınla, kararı sen ver.

Ayrıca Raspberry Pi ve Espressif'in marka (logo/isim) kullanım kuralları ayrı bir konu; ürünü tanıtan içerikte isim kullanmak sorun değil, logolarını öne çıkarmamak gerekiyor.
