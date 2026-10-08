## Gönderi metni

TP4056 şarj modülü üç liraya geliyor ve çalışıyor gibi görünüyor. Hücreyi bitiren üç hata hep aynı yerden çıkıyor.

Şarj akımı → karttan çıkan hazır 1,2 kΩ R_PROG direnci 1 A demek. 500 mAh'lik bir hücrede bu 2C yükleme; hücre ısınıyor, ömrü kısalıyor. Güvenli sınır 0,5C, yani o hücre için 250 mA.

Koruma → TP4056 yalnız şarj kontrolcüsü. Aşırı boşalmaya ve kısa devreye karşı hiçbir şey yapmıyor. Koruma istiyorsan kartta DW01 ve FS8205 ikilisinin bulunduğu sürümü al.

Bağlantı → yükü doğrudan BAT bacağına bağlarsan yükün çektiği akım şarj akımına karışıyor ve modül şarjın bittiğini anlayamıyor. Korumalı kartta yük OUT bacağından alınıyor.

Modül lineer şarj ediyor: giriş gerilimi ile hücre arasındaki fark tamamen ısıya dönüyor. 1 A şarjda kart 1,3 W ısı atıyor.

Li-ion hücreyi TP4056 ile şişiren bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #embedded #liion #makerturkiye

## İlk yorum

R_PROG direncini değiştirmeden önce hücrenin kapasitesini yaz: 0,5C kuralı 1000 mAh'de 500 mA, 2000 mAh'de 1 A demek.
