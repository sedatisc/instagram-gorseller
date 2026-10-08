## Gönderi metni

ESP32 deep sleep akım ölçümü veri sayfasındaki 10 µA'i vermiyor; ölçtüğün şey çip değil kartın tamamı.

Geliştirme kartında USB-UART çevirici, kart üstündeki LDO ve güç ledi uyurken de akım çekiyor; çıplak bir DevKit tipik olarak milliamper bandında kalıyor. Veri sayfasındaki sayıya ancak çıplak modülde yaklaşılıyor.

Ampermetre besleme hattının üstüne, kaynakla kart arasına seri bağlanıyor. Paralel bağlanan metre hiçbir şey ölçmüyor. Ölçüm noktası kartın regülatöründen önce olacak, yoksa regülatörün kendi boşta akımı sayının dışında kalıyor.

Kart uyanıp Wi-Fi'yi açtığında akım yüz milliamperlerin üstüne çıkıyor; µA kademesindeki metre ya sigortayı atıyor ya hattı kısıtlayıp kartı resetliyor. Uyku akımını µA kademesinde, uyanık akımı ayrı ölçümde al.

Pil ömrünü veri sayfasındaki 10 µA ile hesaplayıp iki günde biten bir projesi olan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #embedded #esp32 #makerturkiye

## İlk yorum

Gerçek pil ömrü ortalama akımla çıkıyor: uyku akımı ile uyanık akımı, uyanık kalınan süre oranına göre ağırlıklandırılacak; saniyede bir uyanan bir kart 10 µA'lik uykuyu anlamsız kılıyor.
