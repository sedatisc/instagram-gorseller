## Gönderi metni

Li-Po koruma devresi (BMS) pili şarj etmiyor. Yaptığı tek iş, seri bağlı iki MOSFET'i dört eşikte açıp kapatmak.

Aşırı şarj » hücre 4,25-4,30 V'a çıkınca şarj yolunu kesiyor.
Aşırı deşarj » 2,50-3,00 V'a inince yük yolunu kesiyor. Li-Po 2,5 V'un altına indiğinde kapasitesinin bir kısmını kalıcı kaybediyor; kartın asıl koruduğu sınır bu.
Aşırı akım » karta göre 3-10 A bandında kesiyor.
Kısa devre » birkaç yüz mikrosaniye içinde kapatıyor.

Korumadığı şey sıcaklık. Üstünde NTC ucu yoksa hücre ısınırken kart bunu görmüyor.

PCM ile BMS farkı » PCM yalnız koruma yapıyor, tek hücrede (1S) yeterli. 2S ve üstünde hücreler zamanla ayrışıyor; dengeleme yoksa biri dolarken diğeri boşta kalıyor. Kartta hücre sayısı kadar algılama ucu yoksa dengeleme de yoktur.

Kart seçerken bakılan rakam sürekli akım, ama motor kalkışında çekilen tepe akım sürekli akımın birkaç katına çıkıyor. Kart orada kesiyor, sistem resetleniyor ve "kart bozuk" sanılıyor. Sürekli akımı yükün tepe akımının 1,5 katı seç.

Bir not » korumalı hücrenin üstündeki ince kart zaten PCM'dir. Üstüne ikinci koruma takmak kesme eşiğini öne çekiyor.

Pili bir kez tamamen boşaltıp bir daha şarj edemeyen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #embedded #lipo #makerturkiye

## İlk yorum

Hücre ucuna doğrudan havya tutma — ısı ayırıcıyı bozuyor. Nokta kaynak yoksa uçları kaynaklı (tabbed) hücre al.
