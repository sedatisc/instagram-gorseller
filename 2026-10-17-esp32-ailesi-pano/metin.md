## Gönderi metni

"ESP32 alacağım" cümlesi eksik bir cümle. ESP32 tek bir yonga değil, bir aile — ve üçü ayrı tarafta güçlü.

**ESP32-S3** » iki Xtensa LX7 çekirdek 240 MHz'de, 512 KB dahili SRAM, 45 GPIO (14'ü dokunmatik olabiliyor). Wi-Fi 4 ve Bluetooth 5 LE. Ayıran özelliği vektör komutları: ESP-NN ve ESP-DSP kütüphaneleriyle sinir ağı ve sinyal işleme kartın üstünde dönüyor.

Nerede: kameralı robot ve görüntü aktarma, kart üstünde ses ya da görüntü tanıma, dokunmatik panel.

**ESP32-C6** » RISC-V mimarisi, 160 MHz yüksek performans çekirdeği ve 20 MHz düşük güç çekirdeği. 512 KB SRAM, 320 KB ROM. Wi-Fi 6 (2,4 GHz, 802.11ax) ve Bluetooth 5 LE — ama asıl fark 802.15.4: Thread ve Zigbee destekliyor.

Nerede: Matter uyumlu akıllı ev cihazı, kalabalık ağda Wi-Fi 6 avantajı, düşük güç çekirdeğiyle uzun bekleme. Akıllı ev tarafına girecekse aile içinde doğru seçim bu.

**ESP32-P4** » iki RISC-V çekirdek 400 MHz'de, FPU ve yapay zekâ uzantılarıyla. 768 KB dahili SRAM, harici PSRAM destekli. MIPI-CSI kamera ve MIPI-DSI ekran arabirimi, ikisi de 1080p'ye kadar. USB OTG 2.0 High Speed, H.264 ile 1080p30 kodlama.

Dikkat » P4'ün üstünde Wi-Fi ve Bluetooth **yok**. Kablosuz istiyorsan yanına ESP32-C ya da ESP32-S serisi bir yardımcı yonga koyup ESP-Hosted ya da ESP-AT ile bağlıyorsun. Bunu bilmeden alan çok oluyor.

Nerede: dokunmatik arayüzlü cihaz (HMI), kamera ve video kodlama, ağır arayüz ve kenarda işleme.

Kısaca: kamera ya da ses varsa S3. Akıllı ev, Thread ve Matter varsa C6. Büyük ekran ve işlem gücü gerekiyorsa P4 — kablosuzu ayrıca ekleyeceksin.

"ESP32 aldım ama Thread yokmuş" diyen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #esp32 #embedded #makerturkiye

## İlk yorum

Rakamlar Espressif'in kendi yonga sayfalarından. Kart görselleri Espressif'in esp-dev-kits deposundan, CC BY-SA 4.0 ile: creativecommons.org/licenses/by-sa/4.0

## Kaynak

- ESP32-S3 — https://www.espressif.com/en/products/socs/esp32-s3
- ESP32-C6 — https://www.espressif.com/en/products/socs/esp32-c6
- ESP32-P4 — https://www.espressif.com/en/products/socs/esp32-p4
- Kart görselleri — github.com/espressif/esp-dev-kits (CC BY-SA 4.0)

## Lisans notu

Görseller CC BY-SA 4.0. Atıf zorunlu, ayrıca ShareAlike şartı var —
ayrıntı ve alternatifler `2026-10-16-gelistirme-karti-pano/metin.md`
içinde yazılı. Yayına almadan önce oku.
