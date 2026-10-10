## Gönderi metni

Uçuş kontrol kartı seçerken bakılan şey işlemci değil. Üç Pixhawk'ta da aynı H7 var; ayrım yedeklilikte ve gövde ölçüsünde.

**Pixhawk 6C** » STM32H743, Cortex-M7 480 MHz, 2 MB flash, 1 MB RAM. Yanında STM32F103 IO işlemcisi. Sensörler: ICM-42688-P ve BMI055 ivme/jiroskop, IST8310 manyetometre, MS5611 barometre. 84,8 × 44 × 12,4 mm, 59,3 g. 16 PWM çıkış (8'i IO'dan, 8'i FMU'dan), 3 seri port, 2 GPS, 2 CAN, I2C.

Nerede: çoklu rotor, sabit kanat, rover. Hobi ve öğrenme tarafının standart kartı.

**Pixhawk 6C mini** » aynı işlemci, aynı sensör seti, aynı bellek. Değişen gövde: 53,3 × 39 × 16,2 mm, 39,2 g — 6C'den 20 gram hafif. 14 PWM çıkış (8 IO + 6 FMU).

Dikkat » port akım sınırı 1 A; 6C'de bu 1,5 A. Telemetri modülü ve çevre birimlerini aynı anda besleyeceksen bu farkı hesaba kat.

Nerede: dar gövdeli araç, küçük dron, ağırlığın sayıldığı her yer.

**Pixhawk 6X** » STM32H753 ve FMUv6X açık standardı. Asıl fark burada: **üç IMU ve iki BMP388 barometre, ayrı veri yollarında ve ayrı güç kontrolüyle**. Sensör arızası algılandığında sistem kendiliğinden diğerine geçiyor. Titreşim yalıtım sistemi ve sıcaklık kontrollü IMU kartı var. Güç tarafı da üçlü yedekli: POWER1, POWER2 ve USB.

Nerede: ticari uçuş, kritik görev, arıza toleransının pazarlık konusu olmadığı işler.

Karar kısaca: hobi ve öğrenme için 6C. Gövdede yer darsa 6C mini. Arıza toleransı gerekiyorsa 6X.

Bir not » üçü de hem PX4 hem ArduPilot çalıştırıyor. Kart seçimi yazılım seçimini kilitlemiyor.

İlk dronunda hangi kartı alacağına karar veremeyen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #maker #pixhawk #dron #makerturkiye

## İlk yorum

Rakamlar ve görseller PX4 kullanıcı kılavuzundan (PX4 Autopilot), CC BY 4.0 ile: creativecommons.org/licenses/by/4.0

## Kaynak

- Pixhawk 6C / 6C mini / 6X — github.com/PX4/PX4-user_guide, `en/flight_controller/`
- Görseller — aynı depo, `assets/flight_controller/`

## Lisans notu

Bu kaynak **CC BY 4.0** — yalnız atıf şartı var, ShareAlike yok.
Espressif ve Raspberry Pi görsellerinden farklı olarak ticari gönderide
rahat kullanılıyor; atıf ilk yorumda duruyor.
