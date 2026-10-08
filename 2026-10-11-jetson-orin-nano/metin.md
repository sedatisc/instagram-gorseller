## Gönderi metni

Jetson Orin Nano Super'da süper olan donanım değil, yazılım. Ayrı bir kart çıkmadı; var olan kartın saatleri yükseltildi ve fiyatı düştü.

Yapay zeka → 67 TOPS seyrek kipte, yoğun kipte 33 TOPS
GPU → 1024 Ampere çekirdeği, 32 tensor çekirdeği, 1.020 MHz
İşlemci → 6 çekirdek Arm Cortex-A78AE, 1,7 GHz
Bellek → 8 GB LPDDR5, 102 GB/s
Güç → 7, 15 ya da 25 W kipi

Fark şurada: GPU 635 MHz'den 1.020 MHz'e, işlemci 1,5'ten 1,7 GHz'e, bellek bant genişliği 68'den 102 GB/s'ye çıkıyor. Toplamda 1,7 kat.

8 GB belleği işlemci ile GPU paylaşıyor; modelin tamamı o 8 GB'a sığacak. Küçük dil modelleri ve görüntü işleme rahat çalışıyor, büyük modeller sığmıyor.

Raspberry Pi ne zaman yetmez: tek kamera ve klasik görüntü işlemede Pi yeterli. Birden çok kamera akışı, gerçek zamanlı nesne takibi ya da yerel dil modeli istiyorsan CUDA ve tensor çekirdeği gerekiyor.

Pi'ye model sığdırmaya çalışan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #embedded #jetson #makerturkiye

## İlk yorum

Güç kipini 25 W'a almadan önce soğutmaya bak; pasif soğutucuyla 25 W kipinde kart kendini kısıyor ve 15 W'tan farkı kalmıyor.
