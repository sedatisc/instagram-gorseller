## Gönderi metni

Motor sürücü seçimi akımla başlamıyor, kaybın nerede olacağıyla başlıyor.

**DRV8833** iki tam köprüyü, aşırı akım ve aşırı sıcaklık korumasını tek kılıfa koyuyor. Kanal başına 1,5 A sürekli, 2 A tepe, 2,7-10,8 V besleme. İki kanalı birleştirip tek motoru daha yüksek akımla sürebiliyorsun. Kaybı yaklaşık 0,5 V'luk düşüm — 6 V'ta bu hissediliyor, 12 V'ta önemsiz. Kılıfın altındaki bakır alan soğutucunun kendisi; o alanı kısmak entegreyi ısıtıyor.

N20, TT motor ve küçük pompa için ayrık devre kurmak zaman kaybı. Hazır entegre bu bandın işini görüyor.

**Ayrık MOSFET köprüsü** 10 A üstünde ya da 24 V'luk sürüşte devreye giriyor. RDS(on) 5 mΩ'a indiğinde kayıp entegreye göre onda bire düşüyor. Ama üç şey senin derdin oluyor:

Gate sürücü » üst kol MOSFET'i mikrodenetleyiciden doğrudan sürülmüyor, IR2104 gibi bootstrap'lı sürücü şart.
Ölü zaman » üst ve alt kol aynı anda açılırsa besleme kısa devre oluyor. Aralarına 1-2 µs boşluk bırakılıyor.
Snubber » motor endüktansı kapanma anında tepe gerilim üretiyor; TVS ya da RC olmadan MOSFET gidiyor.

Anahtarlama frekansını 20 kHz üstünde tut, altında motor duyulur şekilde ötüyor.

**İkisinde de atlanan şey besleme tarafı.** Kalkış akımı sürekli akımın 3-6 katı. Motor başına 100-470 µF besleme kondansatörü, kalın ve kısa güç kablosu, güç ve sinyal toprağının tek noktada birleşmesi. Akımı tahminle değil shunt direnciyle ölç, sonra yükte 10 dakika çalıştırıp ısınmaya bak.

L298N'i listeye almadım: üstünde 2 V'luk düşüm var, 2026'da kurulacak bir devrede yeri yok.

Motoru çalıştırınca kartı resetlenen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #embedded #drv8833 #makerturkiye

## İlk yorum

Ayrık devre kuracaksan önce akımı ölç. Tahmini akıma göre seçilen MOSFET'in yarısı ilk yük testinde gidiyor.
