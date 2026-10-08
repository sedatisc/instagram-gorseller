## Gönderi metni

Optokuplör ne işe yarar sorusunun cevabı seviye çevirmek değil: iki devrenin toprağını birbirinden tamamen ayırmak.

İçinde kablo yok. Girişi bir LED, çıkışı o ışığı gören fototransistör; aralarında iletken bağlantı olmadığı için PC817 gibi yaygın bir parça 5.000 V'a kadar yalıtım veriyor.

LED akımı dışarıdan sınırlanıyor. İleri gerilimi 1,2 V civarı; 3,3 V'luk bir çıkış için 210 Ω, 5 V için 390 Ω yaklaşık 10 mA veriyor. Çıkış akımı bu akımla CTR'nin çarpımı ve PC817'de CTR %50-600 arasında değişiyor, yani çıkış tarafı geniş bir banda göre tasarlanıyor.

Şebeke tarafı, motor sürücünün gürültülü toprağı ve RS-485 hattı bu yüzden yalıtılıyor. İki tarafın toprağını bir yerde birleştirirsen parça devrede durur ama hiçbir işe yaramaz.

PC817 mikrosaniye mertebesinde yavaş; hızlı SPI için 6N137 gibi yüksek hızlı bir parça gerekiyor.

Yalıtım için optokuplör koyup iki toprağı yine birleştiren bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #embedded #optokuplor #makerturkiye

## İlk yorum

Çıkış tarafındaki pull-up direncini büyütmek hassasiyeti artırıyor ama anahtarlamayı yavaşlatıyor; 4,7 kΩ çoğu lojik hat için dengeli duruyor.
