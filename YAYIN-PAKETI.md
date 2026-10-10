# YAYIN PAKETİ · 11-18 Ekim 2026

Her gönderinin kareleri, metni ve ilk yorumu burada. Hikaye, gönderiden 40 dakika sonra, aynı klasördeki `hikaye.jpg`.

Kareler depoda: `raw.githubusercontent.com/sedatisc/instagram-gorseller/main/<klasör>/<n>.jpg`

---

# 2026-10-11 · Pazar

## 11:40 · 3D BASKI & ÜRETİM DONANIMI

**Klasör:** `2026-10-11-sunlu-pla-kartelasi` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg, 6.jpg
**Hikaye:** 12:20 · `2026-10-11-sunlu-pla-kartelasi/hikaye.jpg`

### Gönderi metni

SUNLU'nun on altı ayrı PLA serisi var ve hepsi aynı profille basılmıyor. Renge bakıp sepete atmadan önce bakılacak iki rakam: nozul sıcaklığı ve hız sınırı.

Sıcaklık → düz PLA 185-230 °C, PLA Meta 185-225 °C, Wood 190-220 °C, Glow 200-240 °C, PLA+ 2.0 ve Matte 205-245 °C, Silk PLA+ 210-230 °C. Seriyi değiştirip dilimleyicideki profili aynı bırakmak en sık yapılan hata.

Hız → PLA+ 2.0 ve Silk 50-200 mm/s, Matte 50-230 mm/s, Rainbow 100-260 mm/s. High Speed PLA+ 2.0 ise 50-600 mm/s; ama 600 mm/s yalnız 230-260 °C nozul bandında geçerli, düşük sıcaklıkta o hızı zorlarsan akış yetişmiyor.

Karışan iki isim → Matte PLA ile High Speed Matte PLA ayrı ürün. Matte 205-245 °C ve 50-230 mm/s, High Speed Matte 200-260 °C ve 450 mm/s'ye kadar. Kutuda "High Speed" yazıyorsa parametre tablosu da farklı. Mermer isteyen de dikkat: katalogda düz "Marble PLA" yok, yalnız High Speed Marble var.

Tabla → Wood PLA 40-50 °C, ailenin tek istisnası. Diğer tüm PLA serileri 50-60 °C.

Kurutma → SUNLU tek bir rakam veriyor: 50 °C. Süre vermiyor, depolamada %20 altı nem istiyor. "8 saat kurutun" diyen herkes kendi deneyimini söylüyor, üretici verisini değil.

Yanlış seriye doğru profili uygulayıp makarayı çöpe atan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #3dbaski #sunlu #filament #3dyazici #makerturkiye

### İlk yorum

Rakamlar SUNLU'nun ürün sayfalarından. Kendi wiki tablosu Matte PLA ve High Speed PLA+ 2.0'da ürün sayfasıyla çelişiyor; o tabloda bazı satırlar birden fazla seriye kopyalanmış görünüyor, ürün sayfasını esas aldım.

## 12:20 · ELEKTRONİK & IoT

**Klasör:** `2026-10-11-jetson-orin-nano` — 1.jpg, 2.jpg, 3.jpg, 4.jpg
**Hikaye:** 13:00 · `2026-10-11-jetson-orin-nano/hikaye.jpg`

### Gönderi metni

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

### İlk yorum

Güç kipini 25 W'a almadan önce soğutmaya bak; pasif soğutucuyla 25 W kipinde kart kendini kısıyor ve 15 W'tan farkı kalmıyor.

## 17:10 · ÜRÜN & MAĞAZA

**Klasör:** `2026-10-10-bambu-r1-tanitim` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 17:50 · `2026-10-10-bambu-r1-tanitim/hikaye.jpg`

### Gönderi metni

Bambu Lab 3D yazıcıdan sonra lazere girdi. R1, 55 W CO2 lazerle 600 × 300 mm tezgâh sunuyor; gövde fiyatı 2.499 dolar.

Ne kesiyor → 18 mm ceviz kontrplak, 20 mm şeffaf akrilik. Deri, kâğıt, kumaş da listede. Cam, taş ve kaplamalı metalde yalnız gravür var; çıplak metal kesmiyor. CO2 lazerin fiziği bu, marka farkı değil.

Tezgâh → 600 × 300 mm. Opsiyonel konveyörle 3 metre uzunluğunda malzeme geçirilebiliyor. Gravürde 1.000 mm/s'ye çıkıyor, güç hıza göre otomatik ayarlanıp ton eşitleniyor.

Hizalama → işin asıl zor kısmı burası ve dört ayrı sensöre dağıtılmış: kuş bakışı kamera, kafa kamerası, nokta lazeri, mesafe ölçüm lazeri. Basılı desenin üstüne 0,2 mm'de oturuyor, kesim hassasiyeti 0,2 mm'nin altında.

Güvenlik → kapalı kullanımda Class 1. Kapak açılınca lazer duruyor, alev sensörü ve acil stop var. Kaide veya konveyör takılınca Class 4'e geçiyor; o noktada gözlük ve eğitimli operatör şart.

Dikkat edilecek yer: 2.499 dolar gövdenin fiyatı. Konveyör, Vision Encoder, ayna hizalama sensörü, otomatik yangın söndürme ve E1 Pro hava temizleyici ayrı satılıyor.

Türkiye tarafı → MetaTech üç varyantı da listelemiş: standart R1, Long Material Bundle ve Long Material & Rotary Bundle. Üçü de şu an tükenmiş görünüyor ve fiyat sayfada yazmıyor. Yani makine Türkiye'ye geliyor, sırayı beklemek gerekiyor.

Atölyesine lazer almayı konuşan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #lazerkesim #bambulab #co2lazer #atolye #makerturkiye

### İlk yorum

Rakamların tamamı Bambu Lab'in lansman bülteninden. Bağımsız test sonuçları çıktıkça buraya not düşeceğim; özellikle 18 mm kesimin tek geçişte mi yoksa çok geçişte mi olduğu önemli.

## 19:50 · REELS — `2026-10-10-bambu-r1-tanitim/reels.mp4`

Açıklama gönderinin metniyle aynı; uygulamadan trend sesi eklemek istersen elle paylaş.

## 21:00 · PROJE & ATÖLYE

**Klasör:** `2026-10-11-musteriye-fiyat` — 1.jpg, 2.jpg, 3.jpg, 4.jpg
**Hikaye:** 21:40 · `2026-10-11-musteriye-fiyat/hikaye.jpg`

### Gönderi metni

Müşteriye 3D baskı fiyatı verirken altı kalem var; filament bunlardan yalnız biri ve en küçüğü.

1 · Malzeme → dilimleyicinin verdiği gram × makaranın gram fiyatı. 60 g'lık bir parça 1 kg makaranın %6'sı.
2 · Makine saati → elektrik, amortisman ve bakımın yıllık toplamı, çalışma saatine bölünüyor.
3 · Başarısız pay → her işe %10-15. Tek bir başarısız baskının bedeli tüm işlere yayılıyor.
4 · İşçilik → dosya hazırlığı, destek temizliği, zımpara, paketleme. Hepsi senin saatin.
5 · Tasarım → modelleme ayrı faturalanıyor, baskı ücretine katılmıyor.
6 · Kâr marjı → maliyetin üstüne ekleniyor. Maliyeti çıkarmak fiyat vermek demek değil.

Saat ücretini bir kez belirle ve her teklifte aynı sayıyı kullan. İş bazında pazarlık edilen saat ücreti bir süre sonra hiç uygulanmıyor.

Baskı işini gram üzerinden fiyatlayıp ay sonunda kâr edemeyen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #maker #3dbaski #fiyatlandirma #makerturkiye

### İlk yorum

Teklifi kalem kalem yazıp müşteriye göster; gram fiyatı tartışılıyor ama işçilik ve makine saati yazılı olduğunda tartışma bitiyor.

---

# 2026-10-12 · Pazartesi

## 08:12 · 3D BASKI & ÜRETİM DONANIMI

**Klasör:** `2026-10-12-yapisma-yuzeyleri` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 08:52 · `2026-10-12-yapisma-yuzeyleri/hikaye.jpg`

### Gönderi metni

3D baskı tablası yapışma yüzeyi seçimi ayar meselesi değil: PEI, garolit ve cam farklı malzemeleri tutuyor, parça kalkıyorsa önce yüzeye bakılıyor.

Pürüzlü PEI → PLA ve PETG'yi 60 °C tablada yapıştırıcısız tutuyor, parçanın altına mat doku bırakıyor.
Düz PEI → parlak taban veriyor ama PETG'ye fazla yapışıyor; ayırıcı sürülmezse yüzeyden parça kopuyor.
Garolit (G10) → 110 °C tablada ABS, ASA ve nylon burada tutuyor; aynı yüzeyde PLA zor kalkıyor.
Cam → en düz yüzey, 0,02 mm düzlemlik; ölçü hassasiyeti isteyen parçada avantajı bu, karşılığı kendi başına hiçbir şeyi tutmaması.

Düz PEI ve camda yapıştırıcı kalemi hem tutturucu hem ayırıcı görevi yapıyor. Yüzey ne olursa olsun parmak izindeki yağ ilk katmanı kaldırıyor; %90 izopropil alkolle silmek Z ofsetiyle oynamaktan önce geliyor.

İlk katman tutmuyor diye Z ofsetiyle sürekli oynayan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #3dbaski #3dprinting #pei #3dbaskiturkiye

### İlk yorum

Yüzeyi değiştirdiğinde Z ofsetini yeniden al; her plakanın kalınlığı aynı değil ve eski ofset yeni plakada ya eziyor ya havada bırakıyor.

## 12:38 · ELEKTRONİK & IoT

**Klasör:** `2026-10-12-deep-sleep-akim` — 1.jpg, 2.jpg, 3.jpg, 4.jpg
**Hikaye:** 13:18 · `2026-10-12-deep-sleep-akim/hikaye.jpg`

### Gönderi metni

ESP32 deep sleep akım ölçümü veri sayfasındaki 10 µA'i vermiyor; ölçtüğün şey çip değil kartın tamamı.

Geliştirme kartında USB-UART çevirici, kart üstündeki LDO ve güç ledi uyurken de akım çekiyor; çıplak bir DevKit tipik olarak milliamper bandında kalıyor. Veri sayfasındaki sayıya ancak çıplak modülde yaklaşılıyor.

Ampermetre besleme hattının üstüne, kaynakla kart arasına seri bağlanıyor. Paralel bağlanan metre hiçbir şey ölçmüyor. Ölçüm noktası kartın regülatöründen önce olacak, yoksa regülatörün kendi boşta akımı sayının dışında kalıyor.

Kart uyanıp Wi-Fi'yi açtığında akım yüz milliamperlerin üstüne çıkıyor; µA kademesindeki metre ya sigortayı atıyor ya hattı kısıtlayıp kartı resetliyor. Uyku akımını µA kademesinde, uyanık akımı ayrı ölçümde al.

Pil ömrünü veri sayfasındaki 10 µA ile hesaplayıp iki günde biten bir projesi olan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #embedded #esp32 #makerturkiye

### İlk yorum

Gerçek pil ömrü ortalama akımla çıkıyor: uyku akımı ile uyanık akımı, uyanık kalınan süre oranına göre ağırlıklandırılacak; saniyede bir uyanan bir kart 10 µA'lik uykuyu anlamsız kılıyor.

## 17:24 · ÜRÜN & MAĞAZA

**Klasör:** `2026-10-14-sunlu-filadryer` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 18:04 · `2026-10-14-sunlu-filadryer/hikaye.jpg`

### Gönderi metni

SUNLU FilaDryer'ın bu üç modeli arasındaki asıl fark kapasite değil: kaç yazıcıyı besleyebildiği ve sıcaklık tavanı.

Kapasite » S2 tek makara alıyor, Ø 210 × 85 mm. S4 dört makara alıyor, 4 × 1 kg, sekiz filament çıkışı var. E2 iki 1 kg, iki 2 kg ya da tek 3 kg'lık makara alıyor.

Sıcaklık » S2 ve S4 35-70 °C. E2 ise 35-110 °C. Bu rakam sadece "daha iyi" demek değil, hangi filamenti kurutabileceğini belirliyor.

Isıtıcı gücü » S2 48 W, S4 320-350 W PTC ve üç fan, E2 500 W PTC ve çift hazne. S4'te hazne içi sıcaklık farkı ±3 °C'de tutuluyor.

PLA ve PETG 70 °C'nin altında kuruyor, o yüzden S2 çoğu kullanıcının işini görüyor. Birden çok yazıcı çalıştırıyorsan S4 dört makarayı birlikte kuru tutuyor ve dört yazıcıya kadar besliyor. Naylon ailesi daha yükseğini istiyor: E2'nin hazır profillerinde PA6-CF, PA12-CF, PC ve PPS var, diğer ikisinde yok. E2'de ayrıca tavlama modu ve tepsisi geliyor.

Bir uyarı » 70 °C üstünde kurutuyorsan makaranın kendisi de o sıcaklığa dayanmalı. Ucuz plastik makara deforme olup sarımı kilitleyebiliyor.

Nem niye önemli » nemli filament nozul içinde buharlaşıp kabarcık yapıyor. Tel tel çekme artıyor, yüzey pürüzleniyor, nozuldan çıtırtı geliyor, katman yapışması düşüyor. Bunların hiçbiri slicer ayarıyla düzelmiyor; sorun ayarda değil malzemede. En çok etkilenenler PETG, TPU ve naylon.

Retraction mesafesini her baskıda biraz daha artırmaya devam eden bir arkadaşın varsa bu gönderiyi ona yolla — sorun büyük ihtimalle nem.

#sermenkreatif #3dbaski #sunlu #filament #filamentkurutucu #makerturkiye

### İlk yorum

Rakamlar SUNLU'nun kendi S2 / S4 / E2 karşılaştırmasından. Kurutma süresini vermiyorlar, yalnız sıcaklık veriyorlar; "şu kadar saat" diyen herkes kendi deneyimini aktarıyor. Ekrandaki nem değerini izleyip düşüş durunca almak en sağlıklısı.

## 19:40 · PROJE & ATÖLYE

**Klasör:** `2026-10-12-urun-fotografi` — 1.jpg, 2.jpg, 3.jpg, 4.jpg
**Hikaye:** 20:20 · `2026-10-12-urun-fotografi/hikaye.jpg`

### Gönderi metni

Ürün fotoğrafı için stüdyo kurmak tek ışıkla oluyor; ikinci lamba parçayı düzeltmiyor, gölgeyi ikiye çıkarıyor.

Işık → 60 × 60 cm softbox parçanın 45° yanına ve göz hizasının biraz üstüne geliyor. Kaynak büyüdükçe ve yaklaştıkça gölge yumuşuyor.
Dolgu → karşı tarafa konan beyaz köpük kart ışığı geri yansıtıp karanlık yüzü açıyor; ikinci lambanın yaptığı işi o yapıyor.
Zemin → kıvrımsız tek parça beyaz kâğıt. İki yüzeyin birleştiği çizgi fotoğrafta düzeltilmesi en zor şey.
Makine → f/8 - f/11 arası diyafram parçayı baştan sona net veriyor, ISO 100 ve tripot gürültüyü sıfıra indiriyor.

Beyaz ayarı elle 5.000 - 5.500 K'ye alınıyor, otomatiğe bırakılmıyor. Softbox açıkken oda ışığı da yanıyorsa parçanın bir yanı sarı bir yanı mavi çıkıyor ve bu sonradan düzeltilemiyor.

Bastığı parçayı tezgâhta telefonla çekip satamayan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #maker #3dbaski #urunfotografi #makerturkiye

### İlk yorum

Aynı parçayı iki kez çek: biri düz önden katalog karesi, biri 45° üstten doku karesi; ürün sayfasında ilk kare satıyor, ikinci kare güven veriyor.

## 21:10 · REELS — `2026-10-14-sunlu-filadryer/reels.mp4`

Açıklama gönderinin metniyle aynı; uygulamadan trend sesi eklemek istersen elle paylaş.

---

# 2026-10-13 · Salı

## 08:12 · 3D BASKI & ÜRETİM DONANIMI

**Klasör:** `2026-10-16-sunlu-filament-pano` — 1.jpg
**Hikaye:** 08:52 · `2026-10-16-sunlu-filament-pano/hikaye.jpg`

### Gönderi metni

SUNLU'nun üç filamenti arasındaki fark renk değil. Üçü de 1,75 mm ve ±0,02 mm toleranslı; ayrım nerede kullanacağında.

PLA+ 2.0 » nozul 205-245 °C, tabla 50-60 °C, 50-200 mm/s. Çekme dayanımı 46±5 MPa, çentikli Izod darbe 10±3 kJ/m², ısı deformasyon sıcaklığı 56±3 °C, yoğunluk 1,21 g/cm³.

Üçünün en toku bu. Darbe dayanımı mat PLA'nın iki katı. Yük taşıyan aparat, fonksiyonel parça ve günlük baskının geneli buradan.

PLA Matte » nozul 205-245 °C, tabla 50-60 °C, 50-230 mm/s. Çekme 39±6 MPa, darbe 5±2 kJ/m², yoğunluk 1,31 g/cm³.

Mat yüzey katman izlerini gizliyor, parçanın plastik görünümünü azaltıyor. Vitrin, hediyelik ve dekoratif obje için. Karşılığında mukavemeti PLA+ 2.0'ın altında — görünüm parçası basıyorsan sorun değil, menteşe basıyorsan sorun.

PETG » nozul 240-260 °C, tabla 60-70 °C, 300 mm/s'ye kadar. Çekme 48±10 MPa, ısı deformasyon sıcaklığı 70±5 °C.

Asıl farkı ısı ve kimyasal direnci. 70 °C'lik ısı dayanımı iki PLA'nın da belirgin üstünde; araç içinde yazın deforme olmuyor. Suya, asit ve alkaliye dayanıklı, dış mekânda duruyor. Darbe dayanımı düşük (3±1 kJ/m²) — sert darbe alacak parça için değil.

Karar kısaca: yük taşıyacaksa PLA+ 2.0, görünecekse PLA Matte, dışarıda duracak ya da ısınacaksa PETG.

Bir isim uyarısı » SUNLU'nun kataloğunda PLA+ 2.0 ile High Speed PLA+ 2.0 ayrı iki ürün; yoğunlukları, mukavemetleri ve sıcaklık bantları farklı. Buradaki rakamlar PLA+ 2.0'ın. Aynı şekilde PLA Matte ile High Speed Matte PLA da ayrı ürünler, karıştırma.

PLA'yla menteşe basıp yazın deforme olduğuna şaşıran bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #3dbaski #sunlu #filament #makerturkiye

### İlk yorum

Rakamlar SUNLU'nun kendi ürün sayfalarındaki teknik föy tablolarından. Mağaza listelerindeki pazarlama maddeleriyle föy tablosu bazı yerlerde çelişiyor; föy esas alındı. Kurutma için SUNLU 50 °C diyor, süre vermiyor.

## 12:38 · ELEKTRONİK & IoT

**Klasör:** `2026-10-13-optokuplor` — 1.jpg, 2.jpg, 3.jpg, 4.jpg
**Hikaye:** 13:18 · `2026-10-13-optokuplor/hikaye.jpg`

### Gönderi metni

Optokuplör ne işe yarar sorusunun cevabı seviye çevirmek değil: iki devrenin toprağını birbirinden tamamen ayırmak.

İçinde kablo yok. Girişi bir LED, çıkışı o ışığı gören fototransistör; aralarında iletken bağlantı olmadığı için PC817 gibi yaygın bir parça 5.000 V'a kadar yalıtım veriyor.

LED akımı dışarıdan sınırlanıyor. İleri gerilimi 1,2 V civarı; 3,3 V'luk bir çıkış için 210 Ω, 5 V için 390 Ω yaklaşık 10 mA veriyor. Çıkış akımı bu akımla CTR'nin çarpımı ve PC817'de CTR %50-600 arasında değişiyor, yani çıkış tarafı geniş bir banda göre tasarlanıyor.

Şebeke tarafı, motor sürücünün gürültülü toprağı ve RS-485 hattı bu yüzden yalıtılıyor. İki tarafın toprağını bir yerde birleştirirsen parça devrede durur ama hiçbir işe yaramaz.

PC817 mikrosaniye mertebesinde yavaş; hızlı SPI için 6N137 gibi yüksek hızlı bir parça gerekiyor.

Yalıtım için optokuplör koyup iki toprağı yine birleştiren bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #embedded #optokuplor #makerturkiye

### İlk yorum

Çıkış tarafındaki pull-up direncini büyütmek hassasiyeti artırıyor ama anahtarlamayı yavaşlatıyor; 4,7 kΩ çoğu lojik hat için dengeli duruyor.

## 17:24 · ÜRÜN & MAĞAZA

**Klasör:** `2026-10-15-sunlu-ams-heater` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 18:04 · `2026-10-15-sunlu-ams-heater/hikaye.jpg`

### Gönderi metni

SUNLU AMS Heater, Bambu Lab AMS'in üst kapağının yerine takılan bir ısıtıcı kapak. Yaptığı iş tek cümlede: baskı sürerken AMS'in içindeki filamenti kuru tutuyor.

Normalde makarayı AMS'ten çıkarıp kurutucuya koyman, kuruyunca geri takman gerekiyor. Bu kapak o adımı tamamen kaldırıyor.

Rakamlar → 35-70 °C aralığı, 20 dakikada 70 °C'ye çıkıyor. Nem göstergesi gerçek ölçüm yapıyor, %10-90 arası gösteriyor. Otomatik modda %50 nemin üstünde devreye girip %20'de kesiyor; başlangıç eşiğini %25-50 arasında kendin ayarlıyorsun. Zamanlayıcı 0-99 saat.

Kurulum → AMS'in altına girmiyor, kapağının yerine geçiyor. Gevşet, çıkar, sıkıştır; üretici iki dakika diyor. Kalıcı bir değişiklik değil, orijinal kapak geri takılabiliyor.

En kritik nokta → bu ürün yalnız AMS 1. nesil için. AMS Lite'ın ayrı bir modeli var, bu değil. AMS 2 Pro ve AMS HT için SUNLU'nun şu an ürünü yok. Sipariş vermeden önce AMS'inin hangi nesil olduğuna bak; bu üründeki tek iade sebebi bu.

Bilinmesi gerekenler → makara başına ayrı sıcaklık kontrolü yok, dört makara birlikte ısınıyor, yani farklı malzemeleri aynı anda farklı sıcaklıkta kurutamıyorsun. Anma gücü 220 W, ısınma anında 390 W'a çıkıyor. Üretici 10 °C altı ortamda ekrandaki sıcaklığın gerçeğin biraz üstünde kalabileceğini kendisi yazıyor.

AMS'inden nemli filament yüzünden sürekli bozuk baskı alan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #3dbaski #bambulab #ams #sunlu #makerturkiye

### İlk yorum

Bambu Lab'in garantisi konusunda SUNLU bir açıklama yapmıyor — ne "etkilenmez" diyor ne de uyarıyor. Konu hiç ele alınmamış; garanti kaygın varsa bunu bilerek karar ver.

## 19:36 · REELS — `2026-10-15-sunlu-ams-heater/reels.mp4`

Açıklama gönderinin metniyle aynı; uygulamadan trend sesi eklemek istersen elle paylaş.

## 20:42 · PROJE & ATÖLYE

**Klasör:** `2026-10-13-olcu-dogrulama` — 1.jpg, 2.jpg, 3.jpg, 4.jpg
**Hikaye:** 21:22 · `2026-10-13-olcu-dogrulama/hikaye.jpg`

### Gönderi metni

Prototipten ürüne geçerken ölçü doğrulama adımı atlanıyor ve seri üretimde hata bütün adetlere yayılıyor. Tek parçanın çalışması tasarımın doğru olduğunu göstermiyor.

Kumpas → dijital kumpas 0,01 mm çözünürlükte okuyor; göz kararı ölçüm burada bitiyor.
Büzülme → PLA soğurken %0,2 kısalıyor, 100 mm'lik kenar 99,8 mm çıkıyor. Bu payı modelde bırakmak baskıdan sonra zımparalamaktan ucuz.
Eksen → X ve Y'deki sapma kayış gerginliğinden ve akıştan, Z'deki sapma katman yüksekliğinden geliyor. Üçü aynı sayıyı vermiyor, üçü ayrı ölçülüyor.
Örneklem → aynı dosyadan beş parça basıp beşini de ölçmek sapmanın tesadüf mü sistematik mi olduğunu ayırıyor.

Geçme boşluğu baştan yazılıyor: hareketli geçmede 0,2 mm, sıkı geçmede 0,1 mm. Bu sayı modelde duracak, baskıda telafi edilmeyecek.

Seriye başlamadan önce tek parça ölçülüp yazılı onaylanıyor. Onaysız başlayan seri ikinci kez basılıyor.

Prototipi tuttu diye on adet basıp hepsini çöpe atan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #maker #3dbaski #olcukontrol #makerturkiye

### İlk yorum

Ölçtüğün değerleri parça adı, filament ve tarihle birlikte bir tabloya yaz; ikinci siparişte aynı sapmayı baştan telafi etmeni sağlayan tek şey o kayıt oluyor.

---

# 2026-10-14 · Çarşamba

## 08:12 · 3D BASKI & ÜRETİM DONANIMI

**Klasör:** `2026-10-13-nozzle-capi` — 1.jpg, 2.jpg, 3.jpg, 4.jpg
**Hikaye:** 08:52 · `2026-10-13-nozzle-capi/hikaye.jpg`

### Gönderi metni

3D baskıda nozzle çapı seçimi 0,4 mm ile bitmiyor: 0,2 mm ve 0,6 mm uçlar aynı dosyayı bambaşka iki parçaya çeviriyor.

Katman yüksekliği → güvenli üst sınır uç çapının %75'i. 0,2 mm uçta 0,15 mm, 0,4 mm uçta 0,30 mm, 0,6 mm uçta 0,42 mm.
Duvar kalınlığı → varsayılan genişlik uç çapının 1,05 katı: 0,21 mm, 0,42 mm, 0,63 mm. Ölçüyü taşıyan sayı bu.
Akış → 0,6 mm uç, 0,4 mm uca göre üç kata kadar fazla malzeme basıyor; büyük ve basit parçada süre yarıya iniyor.
Süre → 0,2 mm uç ters yöne gidiyor, aynı parça üç katı sürede çıkıyor.

Dolgulu filament kullanacaksan karar baştan veriliyor: karbon ve ahşap katkılı filament 0,2 mm uçtan geçmiyor, 0,6 mm sertleştirilmiş uç tek seçenek.

Her baskıyı 0,4 mm uçla basıp küçük yazıların çıkmamasına şaşıran bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #3dbaski #3dprinting #nozzle #3dbaskiturkiye

### İlk yorum

Ucu değiştirdiğinde slicer profilindeki uç çapını da güncelle; profil 0,4 mm'de kalırsa akış hesabı yanlış çıkıyor ve parça ölçü tutmuyor.

## 12:38 · ELEKTRONİK & IoT

**Klasör:** `2026-10-14-lipo-bms` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 13:18 · `2026-10-14-lipo-bms/hikaye.jpg`

### Gönderi metni

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

### İlk yorum

Hücre ucuna doğrudan havya tutma — ısı ayırıcıyı bozuyor. Nokta kaynak yoksa uçları kaynaklı (tabbed) hücre al.

## 17:24 · ÜRÜN & MAĞAZA

**Klasör:** `2026-10-16-phaetus-liber-u1` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 18:04 · `2026-10-16-phaetus-liber-u1/hikaye.jpg`

### Gönderi metni

Snapmaker ile Phaetus'un U1 için birlikte çıkardığı Liber hotend geldi. Ne yaptığını ve ne YAPMADIĞINI birlikte yazıyorum, çünkü ikincisi daha çok yanlış biliniyor.

Ne yapıyor → nozul içindeki eriyiği birden fazla kanala bölüyor. Eriyiğin yüzey/hacim oranı arttığı için aynı enerjiyle birim zamanda daha fazla filament eriyor. Üreticinin eşit enerji koşulundaki testinde PLA'da %66, ABS'de %87, PETG HF'de %43 daha yüksek hacimsel akış.

Dikkat → bu hız garantisi değil, akış kapasitesi. Snapmaker'ın kendisi de bunun doğrudan baskı süresine yansımadığını, kazancın baskının ne kadarının eritme kapasitesiyle sınırlı olduğuna bağlı olduğunu yazıyor. Uzun ve kesintisiz ekstrüzyon yollu büyük parçalarda fark açılıyor; bol kıvrımlı, sık yön değiştiren küçük modelde kayboluyor.

Ne YAPMIYOR → sertleştirilmiş çelik gövdeli diye karbon fiber çözümü sanılıyor. Üretici bu hotend'i karbon ve cam elyaf takviyeli filamentler, ahşap dolgulu filament ve TPU için ÖNERMİYOR; o malzemeler için standart hotend'e yönlendiriyor. Aşındırıcı filament basıyorsan senin alman gereken Snapmaker'ın kendi sertleştirilmiş çelik hotend seti.

Bir şey daha → maksimum sıcaklık 300 °C, yani U1'in standart hotend'iyle birebir aynı. Liber yüksek sıcaklık malzemelerinin kapısını açmıyor.

Pratik not → U1 dört başlıklı bir makine, gerçekte dört adet gerekiyor. Tek tek almak yerine dörtlü set almak hem daha ucuz hem de dört kafa aynı davranıyor. Tek çap var: 0,4 mm.

Fiyat ve stok için sermenkreatif.com.

U1'ine hotend arayan bir arkadaşın varsa bu gönderiyi ona yolla — özellikle karbon fiber basacaksa.

#sermenkreatif #3dbaski #snapmaker #phaetus #hotend #makerturkiye

### İlk yorum

Mutlak akış değerini (mm³/s) ne Snapmaker ne Phaetus yayınlamış; yalnız standart hotend'e göre yüzde artış var. Pazar yeri başlıklarında dolaşan "55 mm³/s" ifadesi resmî kaynakta yok, o yüzden burada da kullanmadım.

## 19:36 · REELS — `2026-10-16-phaetus-liber-u1/reels.mp4`

Açıklama gönderinin metniyle aynı; uygulamadan trend sesi eklemek istersen elle paylaş.

## 20:42 · PROJE & ATÖLYE

**Klasör:** `2026-10-14-siparis-sorulari` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg, 6.jpg
**Hikaye:** 21:22 · `2026-10-14-siparis-sorulari/hikaye.jpg`

### Gönderi metni

3D baskı siparişinde zarar eden işlerin ortak yanı düşük fiyat değil, bu beş sorunun sorulmamış olması.

1 · Dosya baskıya hazır mı? Dosyanın açılması işin kabul edildiği anlamına gelmiyor. Kapalı olmayan yüzey, ters normal, 0,8 mm'nin altında duvar — hepsi tamir işi. Tamir de iş; saati de ücreti de ayrı. STEP gelirse ya da fotoğraf gelirse o modelleme kalemi.

2 · Parça ne iş yapacak? Müşteri malzeme seçmiyor, kullanım seçiyor. "PLA olsun" diyen kişi parçanın araç içinde duracağını söylemezse yazın deforme olduğunda suç sende kalıyor. Araç içi ve güneş görüyorsa ASA ya da PETG, sürtünme varsa PETG ya da naylon, dış mekânsa ASA.

3 · Hangi ölçü kritik? Her ölçüyü ±0,1 mm tutmaya çalışmak maliyeti katlıyor. Tek soru yeter: hangi yüzey başka parçaya oturuyor? FDM'de tipik sapma ±0,2-0,3 mm; geçme delikler 0,2-0,4 mm büyütülür, kritik yüzeye göre baskı yönü seçilir. Tolerans teklifte yazılı geçsin.

4 · Kaç adet, ne zaman? Tek numune ile elli parça aynı iş değil. Seride %5-10 başarısızlık payı fiyata yazılır. Söylenen tarih baskı süresi değil teslim süresidir; kuyruğu hesaba kat.

5 · Olmazsa ne oluyor? Parça yetişmezse müşterinin ne kaybettiğini sor. Cevap büyükse — makine duracak, sevkiyat kaçacak — o işi almamak en kârlı karar.

Beş sorunun cevabı yazışmada kalsın. Sözlü anlaşmada en çok tartışılan konu teslim tarihi oluyor.

İlk siparişinde zarar eden bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #maker #3dbaski #3dbaskisiparisi #makerturkiye

### İlk yorum

Fiyatı dosyayı görmeden verme. "Ortalama şu kadar" demek, gelen dosya 14 saatlik çıktığında geri alınamıyor.

---

# 2026-10-15 · Perşembe

## 08:12 · 3D BASKI & ÜRETİM DONANIMI

**Klasör:** `2026-10-18-filament-kurutucu-pano` — 1.jpg
**Hikaye:** 08:52 · `2026-10-18-filament-kurutucu-pano/hikaye.jpg`

### Gönderi metni

Filament kurutucu alırken bakılan ilk şey kapasite oluyor ama asıl ayrım orada değil. SUNLU FilaDryer'ın bu üç modelinde farkı yaratan sıcaklık tavanı ve kaç yazıcıyı aynı anda besleyebildiği.

S2 » tek makara, Ø 210 × 85 mm, 35-70 °C, 48 W ısıtıcı. 265 × 274 × 118 mm, 1,19 kg. Masaüstünde tek yazıcıyla PLA, PETG, ABS basıyorsan bu yeterli. PTFE çıkışı var, baskı sürerken kurutmaya devam ediyor.

S4 » dört makara, 4 × 1 kg. 70 °C'ye kadar, 320-350 W PTC ısıtıcı ve üç fan. Sekiz filament çıkışı, dört yazıcıya kadar besliyor. Hazne içi sıcaklık farkı ±3 °C. 458 × 218 × 312 mm, 4,8-5,5 kg. Birden çok yazıcı çalıştıran atölyenin modeli.

E2 » 35-110 °C, 500 W PTC, çift hazne. 2 × 1 kg, 2 × 2 kg ya da tek 3 kg makara alıyor. PA6-CF, PA12-CF, PC ve PPS için hazır profilleri var; tavlama modu ve tepsisi geliyor. 400 × 220 × 307 mm, 6,1 kg. İçeride 110 °C dönerken dış yüzeyi 60 °C'nin altında kalıyor.

Karar şöyle veriliyor: PLA ve PETG 70 °C'nin altında kuruyor, S2 bu işi görüyor. Yazıcı sayın artmışsa S4. Naylon ailesi ve mühendislik filamentleri daha yükseğini istiyor, orada tek seçenek E2.

Bir uyarı » 70 °C üstünde kurutuyorsan makaranın kendisi de o sıcaklığa dayanmalı. Ucuz plastik makara deforme olup sarımı kilitleyebiliyor.

Nemli filament neye mal oluyor: tel tel çekme artıyor, yüzey pürüzleniyor, nozuldan çıtırtı geliyor, katman yapışması düşüyor. Hiçbiri slicer ayarıyla düzelmiyor.

Kurutucusu olmayıp sürekli baskı ayarıyla uğraşan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #3dbaski #sunlu #filamentkurutucu #filament #makerturkiye

### İlk yorum

Rakamlar SUNLU'nun kendi S2 / S4 / E2 karşılaştırmasından. Kurutma süresini vermiyorlar, yalnız sıcaklık veriyorlar; ekrandaki nem değerini izleyip düşüş durunca almak en sağlıklısı. Makaranın ne kadar nem çektiğine göre süre değişiyor.

## 12:38 · ELEKTRONİK & IoT

**Klasör:** `2026-10-15-h-koprusu` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 13:18 · `2026-10-15-h-koprusu/hikaye.jpg`

### Gönderi metni

Motor sürücü seçimi akımla başlamıyor, kaybın nerede olacağıyla başlıyor.

DRV8833 iki tam köprüyü, aşırı akım ve aşırı sıcaklık korumasını tek kılıfa koyuyor. Kanal başına 1,5 A sürekli, 2 A tepe, 2,7-10,8 V besleme. İki kanalı birleştirip tek motoru daha yüksek akımla sürebiliyorsun. Kaybı yaklaşık 0,5 V'luk düşüm — 6 V'ta bu hissediliyor, 12 V'ta önemsiz. Kılıfın altındaki bakır alan soğutucunun kendisi; o alanı kısmak entegreyi ısıtıyor.

N20, TT motor ve küçük pompa için ayrık devre kurmak zaman kaybı. Hazır entegre bu bandın işini görüyor.

Ayrık MOSFET köprüsü 10 A üstünde ya da 24 V'luk sürüşte devreye giriyor. RDS(on) 5 mΩ'a indiğinde kayıp entegreye göre onda bire düşüyor. Ama üç şey senin derdin oluyor:

Gate sürücü » üst kol MOSFET'i mikrodenetleyiciden doğrudan sürülmüyor, IR2104 gibi bootstrap'lı sürücü şart.
Ölü zaman » üst ve alt kol aynı anda açılırsa besleme kısa devre oluyor. Aralarına 1-2 µs boşluk bırakılıyor.
Snubber » motor endüktansı kapanma anında tepe gerilim üretiyor; TVS ya da RC olmadan MOSFET gidiyor.

Anahtarlama frekansını 20 kHz üstünde tut, altında motor duyulur şekilde ötüyor.

İkisinde de atlanan şey besleme tarafı. Kalkış akımı sürekli akımın 3-6 katı. Motor başına 100-470 µF besleme kondansatörü, kalın ve kısa güç kablosu, güç ve sinyal toprağının tek noktada birleşmesi. Akımı tahminle değil shunt direnciyle ölç, sonra yükte 10 dakika çalıştırıp ısınmaya bak.

L298N'i listeye almadım: üstünde 2 V'luk düşüm var, 2026'da kurulacak bir devrede yeri yok.

Motoru çalıştırınca kartı resetlenen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #embedded #drv8833 #makerturkiye

### İlk yorum

Ayrık devre kuracaksan önce akımı ölç. Tahmini akıma göre seçilen MOSFET'in yarısı ilk yük testinde gidiyor.

## 17:24 · ÜRÜN & MAĞAZA

**Klasör:** `2026-10-17-polymaker-ht-pla` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 18:04 · `2026-10-17-polymaker-ht-pla/hikaye.jpg`

### Gönderi metni

Polymaker HT-PLA serisi yüksek sıcaklığa dayanıklı PLA diye satılıyor ve bu doğru — ama bir şartı var, onu söylemeyen satıcıdan almayın.

Isı dayanımı kutudan çıkmıyor, tavlamayla geliyor.

Rakamlar, Polymaker'ın kendi teknik veri sayfasından, tavlama öncesi → sonrası:

HT-PLA, 0,45 MPa yük altında 61,4 → 107,2 °C. Aynı malzeme 1,8 MPa altında 58,6 → 71,7 °C.
HT-PLA-GF, 0,45 MPa altında 75,5 → 114,7 °C. 1,8 MPa altında 59,7 → 84 °C.

Tavlamadan basarsan elinde normal PLA'dan belirgin farkı olmayan, daha pahalı bir makara kalıyor. 58 °C ile 61 °C arasındaki fark için para vermeye değmez.

İyi haber → tavlama zor değil. 80-90 °C'de 3 dakika. Fırın, kurutucu ya da ısıtmalı tabla yeter. İnce cidarlı parçalarda aralığın alt ucunu kullanın, yoksa çarpılıyor.

Üç çeşit, üç ayrı iş → HT-PLA düz sürüm, fonksiyonel parçanın geneli için. HT-PLA Gradient aynı ısı dayanımını renk geçişiyle veriyor, dekoratif iş için. HT-PLA-GF cam elyaf takviyeli; ailenin en yüksek HDT'si ve en rijit olanı, araç içinde kalacak parça varsa bu.

Baskı ayarı üçünde de aynı: nozul 230 °C, tabla 50 °C.

Yazın araçta bıraktığı telefon tutucusu eğilen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #3dbaski #polymaker #htpla #filament #makerturkiye

### İlk yorum

Teknik veri sayfası tavlama için 80-90 °C ve 3 dakika veriyor ama parça kalınlığına göre değişiyor; ince cidarda alt uç, kalın parçada üst uç. Polymaker ayrıca bu değerlerin karşılaştırma amaçlı olduğunu, tasarım hesabında kullanılmaması gerektiğini not düşüyor.

## 19:36 · REELS — `2026-10-17-polymaker-ht-pla/reels.mp4`

Açıklama gönderinin metniyle aynı; uygulamadan trend sesi eklemek istersen elle paylaş.

## 20:42 · PROJE & ATÖLYE

**Klasör:** `2026-10-15-3d-tarayici` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 21:22 · `2026-10-15-3d-tarayici/hikaye.jpg`

### Gönderi metni

3D tarayıcı ölçülü model vermiyor, yüzey veriyor. Aradaki farkı bilmeyen tarama dosyasını doğrudan baskıya gönderip parçayı çöpe atıyor.

Taramadan çıkan şey mesh: milyonlarca üçgen. Üstünde "çap 20 mm" diye bir bilgi yok, bir yüzeyi 0,5 mm kaydıramıyorsun. Kopyalanacak parça için mesh referans alınıyor, model CAD'de yeniden çiziliyor. İşin %80'i burada; tarama kısmı on dakika.

Taramadan önce parçayı hazırla. Parlak ya da şeffaf yüzey taranmıyor — mat sprey ya da talk gerekiyor, ama sprey de 0,01-0,02 mm kalınlık ekliyor; geçme ölçüde bu fark önemli. Derin delik ve vida dişi taramada çıkmıyor, kumpasla ölçülüyor.

Doğruluk rakamına dikkat. Masaüstü yapısal ışık tarayıcıda iyi koşulda 0,05 mm civarı. "İyi koşul" demek: sabit ışık, hareketsiz parça, yeterli örtüşme. Elde gezdirilen taramada bu rakam birkaç katına çıkıyor.

Kritik ölçüyü kumpasla doğrula. Taramadaki sapma geniş yüzeye dağılıyor ve göze batmıyor, ama montaj deliklerinde toplanıyor. Geçme yapacak her ölçü ayrıca ölçülüyor; dişli ve vida dişi zaten standart tablodan çiziliyor.

Ne zaman tarama gereksiz: düz yüzey, delik ve pahtan ibaret bir parçayı kumpasla ölçüp çizmek taramadan hızlı. Tarama serbest form yüzeyde — kalıp, gövde, organik şekil — kazanıyor.

Bir uyarı » taranan parça başkasının ürünüyse kopyalamadan önce tasarım hakkına bak. Birebir kopya satışa çıkmıyor.

Tarama dosyasını doğrudan slicer'a atıp sonucu beğenmeyen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #maker #3dtarayici #3dbaski #makerturkiye

### İlk yorum

Tarama için ayrı tarayıcı almadan önce fotogrametriyi dene: 60-80 fotoğraf ve açık kaynak bir yazılım, büyük ve dokulu parçalarda şaşırtıcı iş görüyor. Küçük ve parlak parçada çalışmıyor.

---

# 2026-10-16 · Cuma

## 08:12 · 3D BASKI & ÜRETİM DONANIMI

**Klasör:** `2026-10-18-bambu-h-serisi-pano` — 1.jpg
**Hikaye:** 08:52 · `2026-10-18-bambu-h-serisi-pano/hikaye.jpg`

### Gönderi metni

Bambu'nun H serisinde üç makine var ve adları birbirine çok benziyor. Şunu baştan söyleyeyim: sıcaklık ve hız üçünde de aynı. 350 °C nozul, 120 °C tabla, 65 °C'ye kadar aktif ısıtmalı kapalı kabin, 1.000 mm/s kafa hızı, 20.000 mm/s² ivme. Yani "hangisi daha güçlü" diye bakmak yanlış soru.

Gerçek ayrım kafa mimarisi ile baskı alanı arasındaki takasta.

H2S » tek nozul, en büyük hacim. 340 × 320 × 340 mm — serinin en büyüğü. Tek nozul, hızlı değişen uç. Bambu bunu "daha büyük bir X1C" diye konumluyor: H2D'nin çift nozul karmaşıklığı olmadan daha çok hacim. Lazer tarafında sınırı var, yalnız 10 W destekliyor; 40 W lazer takılmıyor. Serinin en uygun fiyatlısı.

Kime: tek malzemeyle büyük parça basan.

H2C » Vortek, atıksız çok malzeme. Sağ kafasında 6 hotend'li otomatik değiştirici karusel var. Combo kutusunda 8 hotend geliyor, önerilen kurulumla tek işte 7 malzemeye kadar purge atığı olmadan basıyor. Çok renkli baskıda çöpe giden malzeme derdini ortadan kaldıran kısım burası. AMS ile 24 filamente kadar çıkıyor.

Karşılığı: serinin en küçük baskı alanı (330 × 320 × 325 mm, iki nozul toplamı) ve en yüksek fiyatı.

Kime: çok renkli/çok malzemeli iş yapan ve atıktan rahatsız olan.

H2D » çift nozul, lazer ve kesim. 350 × 320 × 325 mm, çift nozul, 600 mm/s sürekli baskı. Tek farkı baskı değil: 10 W ya da 40 W lazer modülü takılıyor, 40 W ile 15 mm kontrplak kesiyor. Üstüne dijital kesim ve kalem çizim modülleri var. 12 AMS ünitesine, 25 renge kadar çıkıyor.

Kime: masasına baskı + lazer + kesim atölyesini birlikte kuracak olan.

Karar kısaca: tek malzemeyle büyük parça basıyorsan H2S. Çok renkte atık istemiyorsan H2C. Lazer ve kesim de lazımsa H2D.

Bir not » H2D Pro adında kurumsal bir model daha var; tungsten karbür nozullar ve kurumsal ağ desteğiyle ayrı bir sınıf, bu karşılaştırmaya girmiyor.

H serisinde hangisini alacağına karar veremeyen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #3dbaski #bambulab #3dyazici #makerturkiye

### İlk yorum

Rakamlar Bambu Lab'in kendi sayfalarından: ürün ve spec sayfaları, blog lansman yazıları ve wiki FAQ'leri. H2D'nin azami tabla sıcaklığı Bambu'nun okunabilen sayfalarında yazmıyor; H2S'in 120 °C değerini oraya taşımadım.

## 12:38 · ELEKTRONİK & IoT

**Klasör:** `2026-10-16-gelistirme-karti-pano` — 1.jpg
**Hikaye:** 13:18 · `2026-10-16-gelistirme-karti-pano/hikaye.jpg`

### Gönderi metni

"Hangi kartı alayım" sorusunun cevabı güçte değil, işin ne olduğunda. Üçü de geliştirme kartı ama üçü ayrı sınıf.

Raspberry Pi Pico 2 W » RP2350, iki Cortex-M33 çekirdek 150 MHz'de (istersen aynı yongadaki RISC-V çekirdekleri de seçebiliyorsun). 520 KB SRAM, 4 MB flash. Wi-Fi 4 ve Bluetooth LE var. 26 GPIO, 4 ADC, 1,8-5,5 V ile besleniyor.

Nerede kullanılır: sensör okuyup veri yollayan düğüm, pille aylarca çalışması gereken iş, röle/motor/şerit LED sürme. İşletim sistemi yok, kod doğrudan donanımda koşuyor — açılış anında hazır.

ESP32-S3 » iki Xtensa LX7 çekirdek 240 MHz'de, 512 KB dahili SRAM, 45 GPIO (14'ü dokunmatik olabiliyor). Wi-Fi 4 ve Bluetooth 5 LE. Farkı yaratan şey vektör komutları: ESP-NN ve ESP-DSP ile sinir ağı ve sinyal işleme kart üstünde dönüyor.

Nerede kullanılır: kameralı robot ve görüntü aktarma, Wi-Fi'li ev otomasyonu ve MQTT, kart üstünde ses ya da görüntü tanıma. Pico'nun yapamadığı yer burası; Pi'nin fazla geldiği yer de.

Raspberry Pi 5 » BCM2712, dört Cortex-A76 çekirdek 2,4 GHz'de. 1'den 16 GB'a kadar LPDDR4X. Çift bant Wi-Fi 5, Bluetooth 5.0, Gigabit Ethernet, iki USB 3.0, PCIe 2.0. Çift 4K çıkış.

Nerede kullanılır: kiosk ve medya kutusu, NVMe diskli yerel sunucu (PCIe için ayrı HAT gerekiyor), kamera + yapay zekâ, ROS çalıştıran robot. Bu bir bilgisayar, mikrodenetleyici değil.

Dikkat » Pi 5 5 V / 5 A USB-C istiyor. Telefon şarj cihazıyla çalıştırmaya kalkarsan yük bindiğinde kapanıyor. Pille taşınabilir iş kuracaksan Pi 5 yanlış kart.

Karar kısaca: sensör okuyup veri yolluyorsan Pico 2 W. Kablosuzun üstüne kamera ya da ses biniyorsa ESP32-S3. İşletim sistemi gerekiyorsa Pi 5.

Projesine Pi 5 koyup pille çalıştırmaya uğraşan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #raspberrypi #esp32 #makerturkiye

### İlk yorum

Rakamlar üreticilerin kendi ürün sayfalarından. Fiyat yazmadım, en hızlı eskiyen bilgi o. Kart görselleri Raspberry Pi ve Espressif'in kendi dokümantasyonundan, CC BY-SA 4.0 ile: creativecommons.org/licenses/by-sa/4.0

## 16:40 · ÜRÜN & MAĞAZA

**Klasör:** `2026-10-21-u1-k3-pano` — 1.jpg
**Hikaye:** 17:20 · `2026-10-21-u1-k3-pano/hikaye.jpg`

### Gönderi metni

Çok renkli baskıda asıl maliyet filament değil, her renk değişiminde boşa akıtılan malzeme. AMS ve CFS tipi sistemler nozulu temizlemek için filamenti atıyor; uzun bir çok renkli baskıda çöpe giden miktar parçanın kendisini geçebiliyor.

İki üretici bunu aynı mantıkla çözüyor — temizleme yerine değiştirme — ama farklı seviyede.

Snapmaker U1 » araç kafasının tamamını değiştiriyor. Dört bağımsız kafa var, her birinde kendi 0,4 mm nozulu; değişim yaklaşık 5 saniye. Renk geçişinde filament boşa akmıyor çünkü ortak bir eriyik kanalı yok. 270 × 270 × 270 mm, 500 mm/s, 20.000 mm/s², 32 mm³/s akış. Nozul 300 °C, tabla 100 °C. Pogo pin kontakları bir milyon değişim için derecelendirilmiş. 2 MP kabin kamerası spagetti ve filament bitti algılıyor.

Dikkat » kabin standart değil. ABS, ASA, PET, PA ve PC basacaksan ayrıca satılan üst kapak şart, üstüne karbon/cam elyaflı malzeme için sertleştirilmiş nozul gerekiyor. Üst kapakla bile kabin ancak 50 °C civarına çıkıyor, aktif ısıtma yok. Dört renkten fazlası için baskıyı durdurup filamenti elle değiştirmek gerekiyor.

Creality K3 » yalnız nozul grubunu değiştiriyor. KliTek sistemi tam kafayı değil, nozul grubunu değiştiriyor — ağırlığın yaklaşık beşte biri — ve bunu 4,8 saniyede yapıyor. Creality'nin öne sürdüğü avantaj yedek parça maliyeti: nozul grubu yaklaşık 14 dolar, rakip sistemlerde tam kafa 67 dolar. Gövdesine gömülü 4 makara yuvası var, TPU odaklı; 80A'ya kadar yumuşak filament basıyor.

Ama şunu net söyleyeyim: K3 henüz satılmıyor. Creality baskı alanını, hızını, ivmesini ve sıcaklıklarını yayınlamadı. Kendi blogunda "ön siparişler ekim ortasında açılıyor" yazıyor, kampanya sayfasında tek buton abone ol. Fiyat için söylediği "900 doların altında olması bekleniyor" — resmi fiyat değil.

Karar: bugün alınabilen tek seçenek U1. K3'ün yaklaşımı yedek parça tarafında daha ucuz görünüyor ama ortada henüz makine yok; teknik verisi yayınlanınca yeniden bakmak gerekiyor.

Çok renkli baskıda çöpe giden filamente üzülen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #3dbaski #snapmaker #cokrenklibaski #makerturkiye

### İlk yorum

U1 verileri Snapmaker'ın kendi sayfalarından, K3 verileri Creality'nin kendi blog ve kampanya sayfalarından. K3 görseli Creality'nin kendi tanıtım karesi; makine henüz satışta değil.

## 18:10 · PROJE & ATÖLYE

**Klasör:** `2026-10-20-pixhawk-pano` — 1.jpg
**Hikaye:** 18:50 · `2026-10-20-pixhawk-pano/hikaye.jpg`

### Gönderi metni

Uçuş kontrol kartı seçerken bakılan şey işlemci değil. Üç Pixhawk'ta da aynı H7 var; ayrım yedeklilikte ve gövde ölçüsünde.

Pixhawk 6C » STM32H743, Cortex-M7 480 MHz, 2 MB flash, 1 MB RAM. Yanında STM32F103 IO işlemcisi. Sensörler: ICM-42688-P ve BMI055 ivme/jiroskop, IST8310 manyetometre, MS5611 barometre. 84,8 × 44 × 12,4 mm, 59,3 g. 16 PWM çıkış (8'i IO'dan, 8'i FMU'dan), 3 seri port, 2 GPS, 2 CAN, I2C.

Nerede: çoklu rotor, sabit kanat, rover. Hobi ve öğrenme tarafının standart kartı.

Pixhawk 6C mini » aynı işlemci, aynı sensör seti, aynı bellek. Değişen gövde: 53,3 × 39 × 16,2 mm, 39,2 g — 6C'den 20 gram hafif. 14 PWM çıkış (8 IO + 6 FMU).

Dikkat » port akım sınırı 1 A; 6C'de bu 1,5 A. Telemetri modülü ve çevre birimlerini aynı anda besleyeceksen bu farkı hesaba kat.

Nerede: dar gövdeli araç, küçük dron, ağırlığın sayıldığı her yer.

Pixhawk 6X » STM32H753 ve FMUv6X açık standardı. Asıl fark burada: üç IMU ve iki BMP388 barometre, ayrı veri yollarında ve ayrı güç kontrolüyle. Sensör arızası algılandığında sistem kendiliğinden diğerine geçiyor. Titreşim yalıtım sistemi ve sıcaklık kontrollü IMU kartı var. Güç tarafı da üçlü yedekli: POWER1, POWER2 ve USB.

Nerede: ticari uçuş, kritik görev, arıza toleransının pazarlık konusu olmadığı işler.

Karar kısaca: hobi ve öğrenme için 6C. Gövdede yer darsa 6C mini. Arıza toleransı gerekiyorsa 6X.

Bir not » üçü de hem PX4 hem ArduPilot çalıştırıyor. Kart seçimi yazılım seçimini kilitlemiyor.

İlk dronunda hangi kartı alacağına karar veremeyen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #maker #pixhawk #dron #makerturkiye

### İlk yorum

Rakamlar ve görseller PX4 kullanıcı kılavuzundan (PX4 Autopilot), CC BY 4.0 ile: creativecommons.org/licenses/by/4.0

## 20:30 · REELS — `2026-10-18-bambu-h-serisi-pano/reels.mp4`

Açıklama gönderinin metniyle aynı; uygulamadan trend sesi eklemek istersen elle paylaş.

---

# 2026-10-17 · Cumartesi

## 11:10 · 3D BASKI & ÜRETİM DONANIMI

**Klasör:** `2026-10-19-bambu-a-serisi-pano` — 1.jpg
**Hikaye:** 11:50 · `2026-10-19-bambu-a-serisi-pano/hikaye.jpg`

### Gönderi metni

A serisinde üç makine var ve üçü de aynı temeli paylaşıyor: açık gövdeli bed-slinger, 300 °C nozul, Combo paketinde AMS Lite ile dört renk. Karar iki şeye iniyor — ne kadar hacim istediğin ve tablanın kaç dereceye çıktığı.

A1 mini » 180 × 180 × 180 mm. Nozul 300 °C, tabla 80 °C. Tek AMS Lite alıyor, dört renkle sınırlı ve genişlemiyor. Otomatik tabla tesviyesi var, elle ayar gerekmiyor.

Kime: minyatür ve küçük parça basan, masasında yer kısıtlı olan.

A1 » 256 × 256 × 256 mm. Nozul 300 °C, tabla 100 °C — serinin tek 100 °C'lik tablası, asıl fark burada. Bambu A1 için TPU ve PVA'yı ideal malzeme sayıyor; diğer ikisi 80 °C'de kalıyor. 500 mm/s, 10.000 mm/s². Her baskı öncesi otomatik titreşim kompanzasyonu yapıyor, kayış gerginliğini titreşim frekansından denetleyip gevşekse uyarıyor. Akış ve basınç kalibrasyonu da otomatik.

Kime: esnek (TPU) ya da suda çözünen (PVA) filamentle çalışacak olan.

A2L » 330 × 320 × 325 mm. Serinin en büyüğü, Haziran 2026'da çıktı. 500 mm/s, 10.000 mm/s², tabla 80 °C. Gövdesinde iki granül damper ve çok noktalı uyarlanabilir titreşim telafisi var; Bambu bunu "aslında bir H2S Lite" diye tanımlıyor. Genişlemede önde: 4 AMS + 1 AMS Lite ile 19 renge kadar çıkıyor.

Dikkat » A2L açık gövdeli ve Bambu onu "PLA, PETG ve diğer mühendislik dışı filamentler" için konumluyor. Güvenlik gerekçesiyle lazer modülü desteklemiyor. Büyük hacmi 80 °C tablayı kabul ederek alıyorsun.

A2L, A1'in yerine geçmedi — seriye eklenen büyük formatlı model, diğer ikisi satışta.

Karar kısaca: masada yer yoksa A1 mini. Esnek ya da çözünür filament basacaksan A1. Büyük parça basacaksan A2L.

Hangi Bambu'yu alacağına karar veremeyen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #3dbaski #bambulab #3dyazici #makerturkiye

### İlk yorum

Rakamlar Bambu Lab'in kendi spec, FAQ ve blog sayfalarından. A1 mini'nin azami hız ve ivme değerleri için resmi tech-specs sayfası açılamadı, o yüzden panoya koymadım — A1'in değerlerini oraya taşımak yanlış olurdu.

## 12:20 · ELEKTRONİK & IoT

**Klasör:** `2026-10-17-esp32-ailesi-pano` — 1.jpg
**Hikaye:** 13:00 · `2026-10-17-esp32-ailesi-pano/hikaye.jpg`

### Gönderi metni

"ESP32 alacağım" cümlesi eksik bir cümle. ESP32 tek bir yonga değil, bir aile — ve üçü ayrı tarafta güçlü.

ESP32-S3 » iki Xtensa LX7 çekirdek 240 MHz'de, 512 KB dahili SRAM, 45 GPIO (14'ü dokunmatik olabiliyor). Wi-Fi 4 ve Bluetooth 5 LE. Ayıran özelliği vektör komutları: ESP-NN ve ESP-DSP kütüphaneleriyle sinir ağı ve sinyal işleme kartın üstünde dönüyor.

Nerede: kameralı robot ve görüntü aktarma, kart üstünde ses ya da görüntü tanıma, dokunmatik panel.

ESP32-C6 » RISC-V mimarisi, 160 MHz yüksek performans çekirdeği ve 20 MHz düşük güç çekirdeği. 512 KB SRAM, 320 KB ROM. Wi-Fi 6 (2,4 GHz, 802.11ax) ve Bluetooth 5 LE — ama asıl fark 802.15.4: Thread ve Zigbee destekliyor.

Nerede: Matter uyumlu akıllı ev cihazı, kalabalık ağda Wi-Fi 6 avantajı, düşük güç çekirdeğiyle uzun bekleme. Akıllı ev tarafına girecekse aile içinde doğru seçim bu.

ESP32-P4 » iki RISC-V çekirdek 400 MHz'de, FPU ve yapay zekâ uzantılarıyla. 768 KB dahili SRAM, harici PSRAM destekli. MIPI-CSI kamera ve MIPI-DSI ekran arabirimi, ikisi de 1080p'ye kadar. USB OTG 2.0 High Speed, H.264 ile 1080p30 kodlama.

Dikkat » P4'ün üstünde Wi-Fi ve Bluetooth yok. Kablosuz istiyorsan yanına ESP32-C ya da ESP32-S serisi bir yardımcı yonga koyup ESP-Hosted ya da ESP-AT ile bağlıyorsun. Bunu bilmeden alan çok oluyor.

Nerede: dokunmatik arayüzlü cihaz (HMI), kamera ve video kodlama, ağır arayüz ve kenarda işleme.

Kısaca: kamera ya da ses varsa S3. Akıllı ev, Thread ve Matter varsa C6. Büyük ekran ve işlem gücü gerekiyorsa P4 — kablosuzu ayrıca ekleyeceksin.

"ESP32 aldım ama Thread yokmuş" diyen bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #elektronik #esp32 #embedded #makerturkiye

### İlk yorum

Rakamlar Espressif'in kendi yonga sayfalarından. Kart görselleri Espressif'in esp-dev-kits deposundan, CC BY-SA 4.0 ile: creativecommons.org/licenses/by-sa/4.0

## 16:50 · ÜRÜN & MAĞAZA

**Klasör:** `2026-10-20-sparkx-i7-i8-pano` — 1.jpg
**Hikaye:** 17:30 · `2026-10-20-sparkx-i7-i8-pano/hikaye.jpg`

### Gönderi metni

Creality tarafında üç isim aynı haberlerde dolaşıyor ama yalnız biri bugün satın alınabiliyor. Aradaki farkı bilmeden sipariş vermeye kalkan zaman kaybediyor.

SPARKX i7 » satışta. 260 × 260 × 255 mm, 500 mm/s, 10.000 mm/s², nozul 300 °C, tabla 100 °C. Çok renk için yanına harici CFS Lite ünitesi geliyor: 4 slot, nem alıcıyla kurutma, RFID tanıma. 720p AI kamerası spagetti ve dolaşma algılıyor. Açık gövde, kabin ısıtması yok. Desteklediği filament PLA, PETG, PLA-CF ve TPU ile sınırlı.

SPARKX i8 » Indiegogo'da, rafta değil. Teknik verisi yayınlandı: aynı 260 × 260 × 255 mm alan, 500 mm/s, 10.000 mm/s², 81 noktadan otomatik kalibrasyon. Çok renk sistemi QuarTeks — CFS değil, nozula gömülü 4 kanallı bir yapı; purge kulesi olmadan 4 renk basıyor ve kanal değişimi bir saniyenin altında.

Ama bu bir kitlesel fonlama kampanyası, normal perakende satış değil. Creality'nin kendi sayfasında fiyat hâlâ "3XX" yer tutucu olarak duruyor ve sevkiyat tarihi açıklanmamış. Kitlesel fonlamada teslim gecikmesi riski ve tüketici hakları ayrı bir konu — Türkiye'den alacaksan hesaba kat.

K3 bu karşılaştırmaya girmiyor: farklı sınıf, farklı mekanizma. Onu Snapmaker U1 ile karşılaştırdığım ayrı bir gönderide ele aldım.

Kısaca: bugün alınabilen i7. i8'in mekanizması daha iyi ama makine kitlesel fonlamada ve teslim tarihi yok.

"Yeni çıkan şu makineyi alayım" diyen bir arkadaşın varsa bu gönderiyi ona yolla — önce rafta mı diye baksın.

#sermenkreatif #3dbaski #creality #3dyazici #makerturkiye

### İlk yorum

Durum 10 Ekim 2026 itibarıyla, Creality'nin kendi sayfalarından. i8'in ürün fotoğrafı yok çünkü ortada henüz satılan bir ürün yok — panodaki boşluk kasıtlı.

## 19:20 · REELS — `2026-10-16-sunlu-filament-pano/reels.mp4`

Açıklama gönderinin metniyle aynı; uygulamadan trend sesi eklemek istersen elle paylaş.

## 20:10 · PROJE & ATÖLYE

**Klasör:** `2026-10-21-pi-kamera-pano` — 1.jpg
**Hikaye:** 20:50 · `2026-10-21-pi-kamera-pano/hikaye.jpg`

### Gönderi metni

Raspberry Pi kamerası seçerken megapiksele bakılmıyor. Üçü de aynı şerit kabloya takılıyor ama üçü ayrı işin kamerası.

Camera Module 3 » Sony IMX708, 11,9 MP, 4608 × 2592. 1/2,43" sensör, F1.8. Video 2304 × 1296p56, HDR'de 30 fps. 25 × 24 × 11,5 mm, 4 gram.

Ayıran özelliği motorlu otofokus: 10 cm'den sonsuza kendi odaklanıyor. 4 gram olduğu için dronda ve robot kolunda yük yapmıyor. Geniş açı sürümünde yatay görüş 66°'den 102°'ye çıkıyor, yakın çekimde 5 cm'ye kadar iniyor.

HQ Camera » Sony IMX477, 12,3 MP, 4056 × 3040. 1/2,3" sensör, 1,55 µm piksel — Module 3'ten büyük piksel, düşük ışıkta avantaj. 38 × 38 × 18,4 mm (lenssiz), 30,4 gram.

Buradaki fark lens: C/CS yuvası var, lensi sen seçiyorsun. Makro, telefoto, geniş açı. Karşılığında odak mesafesi ve görüş açısı artık kameranın değil lensin özelliği — ve ağırlık 30 grama çıkıyor. Sabit kurulum ve kalite öncelikli işin kamerası.

GS Camera » Sony IMX296, 1,58 MP, 1456 × 1088 ve 60 fps. 3,45 µm piksel — üçünün en büyüğü. 38 × 38 × 19,8 mm, 34 gram.

Çözünürlüğü en düşük olan bu, ama işi farklı: global shutter. Diğer ikisi rolling shutter, yani kareyi satır satır okuyorlar; hızlı hareket eden cisim eğilerek çıkıyor, titreşimli platformda görüntü dalgalanıyor. Global shutter tüm pikselleri aynı anda okuyor, bu bozulma olmuyor.

Nerede: hızlı hareket, titreşimli platform, makine görüşü, ölçüm, kod okuma. Fotoğraf çekmek için değil.

Karar kısaca: günlük kullanım ve dron için Module 3. Sabit kurulum ve lens özgürlüğü için HQ. Hızlı hareket ve makine görüşü için GS.

Dronuna taktığı kameranın görüntüsü neden eğri çıkıyor anlamayan bir arkadaşın varsa bu gönderiyi ona yolla — cevap rolling shutter.

#sermenkreatif #maker #raspberrypi #makinegörüşü #makerturkiye

### İlk yorum

Rakamlar Raspberry Pi'nin kendi donanım karşılaştırma tablosundan. Görseller de aynı dokümantasyondan, CC BY-SA 4.0 ile: creativecommons.org/licenses/by-sa/4.0

---

# 2026-10-18 · Pazar

## 11:40 · 3D BASKI & ÜRETİM DONANIMI

**Klasör:** `2026-10-18-sert-nozul` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 12:20 · `2026-10-18-sert-nozul/hikaye.jpg`

### Gönderi metni

Karbon elyaflı filamente geçtikten sonra baskıların bozulmaya başladıysa önce ayarları kurcalama, nozula bak.

Pirinç yumuşak bir malzeme. Isıyı çok iyi ilettiği için standart uç pirinçten yapılıyor, PLA ve PETG'de yıllarca sorun çıkarmıyor. Ama içinden karbon elyaf, cam elyaf, ahşap tozu, metal tozu ya da karanlıkta parlayan filamentin fosfor taneleri geçmeye başladığında delik yavaşça büyüyor.

Sorun şu: dilimleyici hâlâ 0,4 mm varsayıp malzeme hesaplıyor. Delik 0,45 olduğunda duvar inceliyor, köşelerde boşluk açılıyor, üst yüzey kapanmıyor. Sen sıcaklıkla, akışla, retraction'la uğraşıyorsun; sebep eline aldığın parçada değil, ucun içinde.

Aşındıranlar: karbon elyaf, cam elyaf, ahşap dolgulu, metal dolgulu, karanlıkta parlayan filamentler.
Aşındırmayanlar: düz PLA, PETG, ABS, ASA, TPU. Bunlarda pirinç uç yeterli.

Sert uca geçerken bilmen gereken bir ayrıntı var: sertleştirilmiş çelik pirinç kadar iyi ısı iletmiyor. Aynı sıcaklık ayarıyla basınca malzeme yeterince erimeyebiliyor. Nozul sıcaklığını 5-10 °C yükselt, ilk baskıda akışı gözle. Pirinç kadar iyi ileten sert seçenek arıyorsan tungsten karbür ya da yakut uçlu modellere bakacaksın.

Elyaflı filamente geçmeyi düşünüyorsan ucu önceden değiştir. Uç ucuz, bozuk baskı pahalı.

#sermenkreatif #3dbaski #nozzle #karbonfiber #filament #makerturkiye

### İlk yorum

Aşınmayı anlamanın kolay yolu: aynı kalibrasyon küpünü ayda bir bas ve duvar kalınlığını kumpasla ölç. İncelmeye başladıysa uç gitmiş demektir.

## 12:20 · ELEKTRONİK & IoT

**Klasör:** `2026-10-18-kondansator-esr` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 13:00 · `2026-10-18-kondansator-esr/hikaye.jpg`

### Gönderi metni

Kart yük bindiğinde resetleniyor, güç kaynağı ısınıyor, çıkışta dalgalanma var. Kondansatörleri ölçüyorsun, multimetre etiket değerini gösteriyor. "Sağlam" diyip başka yere bakıyorsun. Çoğu zaman hata tam orada.

Kondansatörün kendi iç direnci var: ESR. Elektrolitli kondansatörlerde elektrolit zamanla kuruyor, iç bağlantılar bozuluyor ve bu direnç katlanıyor. Kapasite ise az düşüyor — multimetrenin kapasite kademesi hâlâ makul bir sayı gösteriyor. Ölçüm seni yanıltıyor.

ESR yükselince kondansatör işini yapamıyor: anahtarlamalı güç kaynağının çıkışındaki dalgalanmayı bastıramıyor, kendisi ısınıyor, kart ani akım çektiğinde besleme çöküyor.

Üstü kabarmış ya da altından sızmış kondansatör zaten bellidir. Asıl sinsi olan dışarıdan kusursuz görünendir.

Nasıl bakılır: ESR metre devrede ölçebiliyor, söküp denemeye göre çok daha hızlı. Osiloskopun varsa çıkıştaki dalgalanmanın tepeden tepeye değerine bak.

Değiştirirken düşük ESR serisinden, 105 °C sınıfı ve en az aynı gerilim değerinde bir parça seç. Kapasiteyi büyütmek ESR'yi düzeltmiyor — farklı bir problemi çözmeye çalışmış olursun.

#sermenkreatif #elektronik #kondansator #esr #tamir #makerturkiye

### İlk yorum

Elinde ESR metre yoksa bir ipucu: aynı karttaki aynı değerdeki kondansatörleri karşılaştır. Biri diğerlerinden belirgin farklı davranıyorsa şüpheli odur.

## 17:10 · ÜRÜN & MAĞAZA

**Klasör:** `2026-10-18-ender-3-v4-combo` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 17:50 · `2026-10-18-ender-3-v4-combo/hikaye.jpg`

### Gönderi metni

Ender serisi, hobi masasındaki en bilinen isim. Bu kuşakta artık rakamlar da ona göre: 500 mm/s azami hız, 12.000 mm/s² ivme, 300 °C nozul.

Baskı alanı 220 × 220 × 235 mm. Bu sınıf, ilk ciddi makine arayan için doğru yer: küçük parça, fonksiyonel parça, oyuncak, aparat, yedek parça. 220 mm küpü aşan işler basıyorsan bu makine dar gelir, onu baştan söyleyelim.

Combo adı CFS'li paketi anlatıyor. CFS dört makara taşıyor, dört CFS'e kadar bağlanabiliyor — Creality üst sınırı 16 renk diye veriyor. Makara bitince sıradakine kendisi geçiyor, dolaşma algılaması CFS ile birlikte çalışıyor.

Zamanı yiyen iki işi de kısaltmışlar: tabla ayarı tam otomatik, nozul kapağı mıknatıslı — elle çekip alıyorsun. Titreşim tarafında input shaping var, hızı yükseltince köşelerde iz bırakmasın diye.

Bağlantı: USB bellek, Wi-Fi ve Creality Cloud. Birden fazla makineyi Creality Print üzerinden aynı ağdan yönetebiliyorsun.

Kapalı kabini yok. PLA, PETG ve TPU tarafında rahat; ABS ve ASA basacaksan bu makine o iş için değil.

Ender-3 V4 Combo sermenkreatif.com'da.

#sermenkreatif #3dbaski #creality #ender3 #cokrenklibaski #makerturkiye

### İlk yorum

Rakamların hepsi Creality'nin kendi ürün sayfasındaki tablodan. Combo'nun CFS'li paket olduğunu üretici ölçü tablosu da doğruluyor: tek makine 396 mm genişlikte, Combo 838 mm.

## 19:50 · REELS — `2026-10-18-ender-3-v4-combo/reels.mp4`

Açıklama gönderinin metniyle aynı; uygulamadan trend sesi eklemek istersen elle paylaş.

## 21:00 · PROJE & ATÖLYE

**Klasör:** `2026-10-18-toplulukta-ariza` — 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
**Hikaye:** 21:40 · `2026-10-18-toplulukta-ariza/hikaye.jpg`

### Gönderi metni

Baskı bozuk çıktığında çoğu kişi saatlerce tek başına ayar kurcalıyor. Oysa aynı arıza o gün başka birinin de başına gelmiş ve çözülmüş oluyor.

SK 3D Topluluğu bunun için var: ücretsiz, herkese açık bir WhatsApp grubu.

Grupta işleyiş basit. "Baskım bozuk çıkıyor" cümlesi kimseye bir şey anlatmıyor; parçanın fotoğrafını atıyorsun. Fotoğraf bir bakışta söylüyor — stringing mi, katman ayrışması mı, ilk katman mı.

En çok gelen beş arıza hep aynı: ilk katmanın tutmaması, stringing, katmanların ayrışması, ölçünün tutmaması, ortada tıkanma. İlk üçünün cevabı belli. Son ikisi daha sinsi: sebep çoğu zaman ayar değil, büzülme payı, aşınmış nozul ya da nem çekmiş filament oluyor. Bunlar deneyimle ayıklanıyor.

Arıza dışında da işliyor: çizdiğin parçayı paylaşıyorsun, başkasının denediği ayarı öğreniyorsun, yazıcı ya da filament lazımsa aynı yerden hallediliyor.

Katılmak için profildeki linke dokunman yeterli. Ücretsiz, istediğin an çıkabilirsin.

#sermenkreatif #3dbaski #3dbaskiturkiye #makerturkiye #topluluk

### İlk yorum

Fotoğrafı çekerken parçayı yan ışıkta çek — katman izleri ve yüzey hataları düz ışıkta kaybolup gidiyor.

