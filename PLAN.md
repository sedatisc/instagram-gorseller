# @sermenkreatif — YAYIN PLANI

Günde **4 gönderi · 4 hikaye · 1 reels** · her gönderi en az 3 slayt

Günlük sıra ve klasörler `YAYIN-LISTESI.md` dosyasında; o dosyayı `sira.py`
üretiyor, kuyruk `DURUM.json` içinde duruyor.

---

# 1. ALGORİTMANIN BUGÜNKÜ HÂLİ

Planı doğrudan değiştiren dört bulgu:

**Hashtag sınırı 5.** Aralık 2025'te geldi, platform tarafından zorunlu tutuluyor. Fazlasını yazarsan ya paylaştırmıyor ya da kırpıyor. Açıklamaya mı yoruma mı yazdığın fark etmiyor, toplam hakkın 5. Instagram'ın kendi önerisi 3-5 arası.

**Hashtag yerine anahtar kelime.** Erişimi artık açıklamadaki aranabilir kelimeler taşıyor. "ESP32 ADC okuma hatası" diye yazmak, aynı şeyi hashtag'e gömmekten daha çok iş görüyor. Hashtag bir sınıflandırma sinyaline indi.

**En ağır sinyal gönderme (send).** Birine özelden yollanan gönderi, beğeniden de kaydetmeden de yukarıda. Sonra kaydetme, sonra izlenme süresi geliyor. Bu yüzden her gönderinin sonunda "kaydet" değil, **"bunu o arkadaşına yolla"** çağrısı olacak.

**Karusel hâlâ çalışıyor** ama şartı var: okuru kaydırmaya mecbur bırakacak. İlk slayt soruyu sormalı, cevabı vermemeli. Reels izlenme süresiyle, karusel kaydırma derinliğiyle ölçülüyor.

Ek olarak: içerik özgün ve filigransız olacak, başka platformdan devşirme kabul edilmiyor. Trial Reels ile takipçi olmayanlarda önce test etme imkânı var, ileride video tarafına geçersek işe yarar.

---

# 2. PAYLAŞIM SAATLERİ

Türkiye verisinde en yüksek etkileşim günü **çarşamba**, haftanın tek en yüksek anı **pazar 21.00**.

Saatler bilerek tam ve buçuk değil. Herkes 12.00 ve 20.30'a kurduğu için o dakikalarda kuyruk oluşuyor.

| Slot | Kategori | Hafta içi | Cumartesi | Pazar |
|---|---|---|---|---|
| Sabah | 3D BASKI & ÜRETİM DONANIMI | **08.12** | 11.10 | 11.40 |
| Öğle | ELEKTRONİK & IoT | **12.38** | 12.20 | 12.20 |
| İkindi | ÜRÜN & MAĞAZA | **17.24** | 16.50 | 17.10 |
| — | **REELS** | **19.36** | 19.20 | 19.50 |
| Akşam | PROJE & ATÖLYE | **20.42** | 20.10 | **21.00** |

**Hikaye** her gönderiden 40 dakika sonra, aynı gönderinin `hikaye.png`
dosyasından. Günde 4 gönderi = günde 4 hikaye; ayrıca hikaye üretilmiyor.

**Reels** günde bir tane, akşam gönderisinden hemen önce. Kaynağı o günün
ürün gönderisi; `reels.py` aynı spec'ten üretiyor.

Gün bazında kayma:

- **Pazartesi** sabah slotu güçlü, akşamı zayıf → akşam gönderisi 19.40, reels 21.10
- **Çarşamba** akşamı en iyi → haftanın en iddialı gönderisi çarşamba 20.42'ye
- **Cuma** akşamı düşüyor → ürün 16.40, akşam 18.10, reels 20.30
- **Pazar** 21.00 haftanın zirvesi → serinin en güçlü işi buraya

Saatlerin tamamı `sira.py` içindeki `IZGARA` tablosunda; değiştirince
`python3 sira.py` listeyi yeniden üretiyor.

## Dördüncü slot ne ile besleniyor

ÜRÜN & MAĞAZA slotu hesabın mağazaya bakan yüzü ve günlük. Üç kaynağı var:

1. **Mağaza ürünleri** — stokta olan filament, kurutucu, hotend, aksesuar
2. **Cihaz kataloğu** — `cihazlar/` içinde 37 cihaz kaydı; `cihaz.py --sira`
   markaları dönüşümlü sıraya diziyor. Her biri için kapak fotoğrafı lazım
   (`cihaz.py --foto` eksikleri listeliyor)
3. **Pano gönderileri** — `PANO-SIRASI.md`'deki karşılaştırma panoları

Bu slot tek başına 37 günlük cihaz içeriği taşıyor; darboğaz konu değil,
fotoğraf.

---

# 3. HASHTAG SİSTEMİ

5 hak var, hepsi kullanılacak. Sabit iki slot, değişken üç slot.

| Slot | Ne | Kural |
|---|---|---|
| 1 | Marka | Her gönderide `#sermenkreatif` |
| 2 | Kategori | `#3dbaski` · `#lazer` · `#elektronik` · `#maker` |
| 3 | Topluluk | 50 bin – 500 bin gönderilik niş etiket |
| 4 | Konu | Gönderinin ana terimi: `#esp32`, `#petg`, `#arduino` |
| 5 | Dil/bölge | `#makerturkiye` veya `#3dbaskiturkiye` |

Kategori bazlı hazır setler:

**3D BASKI:** `#sermenkreatif` `#3dbaski` `#3dprinting` `#<malzeme veya ayar>` `#3dbaskiturkiye`

**ELEKTRONİK & IoT:** `#sermenkreatif` `#elektronik` `#embedded` `#<çip veya protokol>` `#makerturkiye`

**PROJE & ATÖLYE:** `#sermenkreatif` `#maker` `#robotik` `#<proje adı>` `#makerturkiye`

Türkçe karakterli etiket yazma: `#3dbaskı` ile `#3dbaski` ayrı etiket sayılıyor, ikincisi çok daha kalabalık. Hepsinde şapkasız ve noktasız yaz.

---

# 4. ETİKETLEME

**Marka etiketi.** Gönderide ürünü geçen markanın hesabını etiketle: `@bambulab`, `@prusa3d`, `@creality3dofficial`, `@raspberrypi`, `@arduino.cc`, `@espressif_systems`, `@nvidiaembedded`. Marka repost yaparsa gönderi kendi kitlesinin dışına çıkar; bu hesabın büyüme yolu bu.

**Konum etiketi.** Amasya. Yerel keşfet trafiği küçük ama dönüşümü yüksek — 3D baskı siparişi verecek kişi yakındaki üreticiyi arıyor.

**Ürün etiketi.** Instagram Shopping kurulduğunda sermenkreatif.com ürünleri gönderi üstünde etiketlenecek. Baskı ürünü geçen her gönderide kullanılacak.

**İş birliği (collab).** SK 3D Topluluğu'ndan biri projeye katkı verdiyse ortak gönderi aç; gönderi iki hesabın da akışında görünür.

---

# 5. YAZIM KILAVUZU

## İngilizce terimler

Marka, model, standart ve protokol adları **çevrilmez, olduğu gibi yazılır**: ESP32, Raspberry Pi, MOSFET, PETG, MQTT, I2C, GPIO, PWM, Wi-Fi, Thread, Matter, PLA, ASA, STL, 3MF, slicer, firmware.

Türkçesi gerçekten yerleşmiş terimlerde Türkçe kullanılır: direnç, kondansatör, diyot, katman, dolgu, duvar, destek, besleme, toprak, gerilim, akım.

Zorlama karşılık üretilmez. "Gömülü yazılım" olur, "sabit yazılım" olmaz. "Retraction" için "geri çekme" yazılır ama parantezle terimi verilir: geri çekme (retraction).

## Ek alırken kesme işareti

Özel ada ve kısaltmaya gelen çekim eki kesme işaretiyle ayrılır. Ek, kelimenin **okunuşuna** göre seçilir:

| Doğru | Yanlış |
|---|---|
| ESP32'ye, ESP32'nin | ESP32'e, ESP32nin |
| PLA'yı, PLA'nın | PLA'ı, PLAyı |
| PETG'yi, PETG'nin | PETG'i |
| STL'yi, 3MF'yi | STL'i |
| I2C'de | I2C de |
| Raspberry Pi'ye | Raspberry Pi'ya |
| MOSFET'in | MOSFETin |

Cins isme gelen ek ayrılmaz: dirençler, kondansatörü, katmanda.

## Sık yapılan hatalar

- **de/da:** "Ben de yaptım" ayrı, "evde yaptım" bitişik. Ayırma testi: cümleden çıkarınca anlam bozuluyorsa bitişiktir.
- **ki:** bağlaç olarak ayrı — "gördüm ki". Ek olarak bitişik — "masadaki".
- **-cek/-cak:** "yapacak", "yapıcak" değil.
- **Soru eki ayrı:** "çalışıyor mu", "çalışıyormu" değil.
- Şapka işareti yalnız anlam ayırıyorsa: kâr/kar, hâlâ.

## Sayı ve birim

- Sayı ile birim arasında boşluk: `100 kΩ`, `5 V`, `0,2 mm`, `210 °C`
- Ondalık ayırıcı **virgül**: `0,2 mm` — nokta değil
- Binlik ayırıcı **nokta**: `1.000 saat`
- Yüzde işareti önde: `%20`
- Bir cümlede rakamla başlanmaz

## Başlık ve cümle

- Slayt başlıklarında yalnız ilk kelime ve özel adlar büyük: "Katman yüksekliği neyi değiştirir" — "Katman Yüksekliği Neyi Değiştirir" değil. Büyük harfli kapak başlıkları bu kuralın dışında.
- Üç noktadan sonra boşluk yok, virgülden sonra var
- Türkçe tırnak kullan: "böyle"

---

# 6. GÖNDERİ KURGUSU

Her gönderi aynı iskelet:

**Slayt 1 — kanca.** Soru sorar, cevabı vermez. Okur cevabı merak etmezse kaydırmaz.
**Ara slaytlar — adımlar.** Rehber gönderide 3 adım, liste gönderide her madde ayrı slayt.
**Son slayt — çağrı.** "Kaydet" değil: "bu tuzağa düşen bir arkadaşın varsa yolla."

Açıklama metni kısa ve anahtar kelime yüklü olacak. İlk cümlede aranabilir terim geçsin: gönderi "ESP32 deep sleep akım ölçümü" hakkındaysa bu ifade birebir açıklamada yer alsın.

Erişilebilirlik metni (alt text) her slayta yazılacak — hem görme engelli okur için hem de arama için okunuyor.

---

# 7. KONU LİSTESİ

Aşağıdaki üç liste ilk üç slotun konu havuzu. Dördüncü slot (ÜRÜN & MAĞAZA)
sabit konu listesi tutmuyor; `cihazlar/`, `PANO-SIRASI.md` ve mağaza
stoğundan besleniyor (bkz. bölüm 2).

## SLOT 1 · SABAH — 3D BASKI & ÜRETİM DONANIMI

Slot yalnız 3D baskıyı değil üretim donanımının tamamını kapsıyor: yazıcı, filament ve lazer. Beş günde bir ürün gönderisi geliyor (3, 8, 13, 18, 23, 28) — bunlar mağazaya en yakın içerik, ürün ve marka etiketi zorunlu.

| # | Konu | Tür · Slayt |
|---|---|---|
| 1 | PLA, PETG, ABS, ASA: hangi parçada hangisi | Liste · 6 |
| 2 | Katman yüksekliği görünümü mü hızı mı belirler | Rehber · 4 |
| 3 | **Ürün:** Bambu Lab A2L Combo — kime göre, kime değil | Ürün · 5 |
| 4 | Dolgu oranı gerçekte neyi değiştirir | Rehber · 4 |
| 5 | Duvar sayısı dolgudan neden daha önemli | Rehber · 4 |
| 6 | Parça yönü mukavemeti nasıl değiştirir | Rehber · 4 |
| 7 | Destek yapısı: ağaç mı normal mi | Rehber · 4 |
| 8 | **Ürün:** Bambu Lab R1 — 55 W CO₂ lazer ne yapar | Ürün · 5 |
| 9 | Stringing: retraction mı sıcaklık mı | Rehber · 4 |
| 10 | Warping ve kapalı kabin meselesi | Rehber · 4 |
| 11 | Elephant foot: ilk katman değil ilk beş katman | Rehber · 4 |
| 12 | Filament kurutma: hangisi kaç saat | Liste · 6 |
| 13 | **Ürün:** Sunlu PLA renk kartelası ve gerçek özellikleri | Ürün · 6 |
| 14 | Yapışma yüzeyleri: PEI, garolit, cam | Liste · 5 |
| 15 | 0,4 dışına çıkmak: 0,2 ve 0,6 nozzle | Rehber · 4 |
| 16 | Yüzey işlemi: zımpara, astar, boya | Liste · 5 |
| 17 | Geçme parçalarda tolerans: kaç mm boşluk | Rehber · 4 |
| 18 | **Ürün:** Diyot mu CO₂ mü — Falcon2 Pro ve R1 karşılaştırması | Ürün · 5 |
| 19 | Hızı artırınca ilk bozulan şey | Rehber · 4 |
| 20 | Sertleştirilmiş nozzle ne zaman şart | Rehber · 4 |
| 21 | Heat-set insert ile vidalı birleşim | Rehber · 4 |
| 22 | AMS ve MMU: renk değişiminin israf maliyeti | Rehber · 4 |
| 23 | **Ürün:** Snapmaker U1 mi Creality K3 mü — biri rafta, biri ekimde | Ürün · 5 |
| 24 | Yüksek akışlı nozzle gerçekten hızlandırıyor mu | Rehber · 4 |
| 25 | Slicer profilini sıfırdan kurmak | Rehber · 4 |
| 26 | Input shaping ve pressure advance | Rehber · 4 |
| 27 | Baskı sonrası ölçü sapması ve büzülme payı | Rehber · 4 |
| 28 | **Ürün:** Filament sınıfları — PLA, PLA+, Silk, Matte | Ürün · 6 |
| 29 | Reçine ne zaman FDM'den iyi | Rehber · 4 |
| 30 | 3D baskı gıdayla temasta güvenli mi | Rehber · 4 |

## SLOT 2 · ÖĞLE — ELEKTRONİK & IoT

Eleme ve güncelleme yapılmış liste. Tarihler yeni takvime göre kaydırıldı.

| # | Konu | Tür · Slayt |
|---|---|---|
| 1 | 2026'nın en iyi 8 IoT geliştirme kartı | Liste · 10 |
| 2 | Röle mi MOSFET mi: hangi yükte hangisi | Rehber · 4 |
| 3 | Pull-up direnci: dahili mi harici mi | Rehber · 4 |
| 4 | I2C çalışmıyor: 5 sebep | Liste · 7 |
| 5 | MOSFET mükemmel anahtar değil: RDS(on) ve ısınma | Rehber · 4 |
| 6 | Debounce: donanımla mı yazılımla mı | Rehber · 4 |
| 7 | IoT projesine başlamadan bilmen gereken 6 kavram | Liste · 8 |
| 8 | Voltaj bölücü ile sensör okumak neden yanıltır | Rehber · 4 |
| 9 | USB-C'den 5 V almak: CC direnci | Rehber · 4 |
| 10 | Bypass kondansatörü neden her IC'nin yanında | Rehber · 4 |
| 11 | 5 V sensörü 3,3 V karta bağlamak | Rehber · 4 |
| 12 | Motor açılınca kart resetleniyor | Rehber · 4 |
| 13 | Buck dönüştürücü ısınıyorsa 4 sebep | Liste · 6 |
| 14 | TP4056 ile Li-ion şarj: 3 yaygın hata | Liste · 5 |
| 15 | Kart tanıtımı: Jetson Orin Nano Super | Tanıtım · 4 |
| 16 | ESP32 deep sleep: gerçek akım ölçümü | Rehber · 4 |
| 17 | Optokuplör ne işe yarar, ne zaman şart | Rehber · 4 |
| 18 | Li-Po koruma devresi (BMS) nasıl çalışır | Rehber · 4 |
| 19 | Ayrık H köprüsü mü, DRV8833 mü | Rehber · 4 |
| 20 | Sigorta, PTC ve TVS: devre koruma üçlüsü | Rehber · 4 |
| 21 | Kart tanıtımı: Pixhawk 6C mi SpeedyBee F405 mi | Tanıtım · 4 |
| 22 | Kondansatör sağlam mı bozuk mu: ESR meselesi | Rehber · 4 |
| 23 | Ground loop gürültüsü nasıl biter | Rehber · 4 |
| 24 | ESP32 antenini öldüren 4 yerleşim hatası | Liste · 6 |
| 25 | Zener yerine TL431 | Rehber · 4 |
| 26 | ArduRover: uçuş kontrol kartı yerde | Rehber · 4 |
| 27 | AHT20 verisini MQTT ile buluta gönderme | Rehber · 4 |
| 28 | ESP32'ye kablosuz OTA güncelleme | Rehber · 4 |
| 29 | BME280 + Raspberry Pi Pico 2 W | Rehber · 4 |
| 30 | Kart tanıtımı: ESP32-P4 | Tanıtım · 4 |

## SLOT 4 · AKŞAM — PROJE & ATÖLYE

Kendi projelerinden besleniyor. Bu slot hesabın kimliği: diğer ikisi bilgi verir, bu slot "bunu gerçekten yapan adam" olduğunu gösterir.

10, 20 ve 30. günler topluluk gönderisi — WhatsApp grubuna çağrı. Her seferinde aynı gönderi değil, aynı çağrının farklı açısı (soru sorma, arıza çözme, model paylaşımı).

| # | Konu | Tür · Slayt |
|---|---|---|
| 1 | ATLAS: bilgisayarı kullanan sesli asistan | Proje · 5 |
| 2 | Atölye düzeni: tezgâh, depolama, ışık | Liste · 5 |
| 3 | SIPA/KATIR: 4x4 yük taşıyıcı UGV | Proje · 6 |
| 4 | 3D yazıcı bakım takvimi | Liste · 5 |
| 5 | Arama kurtarma roveri: gece devriyesi | Proje · 6 |
| 6 | Maliyet hesabı: gram ve saat | Rehber · 4 |
| 7 | Rover V2: Arduino Mega ve NRF24 | Proje · 5 |
| 8 | Model nereden bulunur: Printables, MakerWorld | Liste · 5 |
| 9 | Atölyede olması gereken 10 alet | Liste · 12 |
| 10 | **Topluluk:** SK 3D Topluluğu — takıldığın yerde soracak biri var | Topluluk · 5 |
| 11 | Başarısız baskı arşivi: 6 ders | Liste · 8 |
| 12 | Fusion mı Onshape mi | Rehber · 4 |
| 13 | Müşteriye fiyat vermek | Rehber · 4 |
| 14 | Ürün fotoğrafı: tek ışıkla stüdyo | Rehber · 4 |
| 15 | Prototipten ürüne: ölçü doğrulama | Rehber · 4 |
| 16 | Siparişi kabul etmeden önce sorulacak 5 soru | Liste · 7 |
| 17 | 3D tarayıcı ile var olan parçayı kopyalamak | Rehber · 4 |
| 18 | Vida sayım sistemi DİRHEM | Proje · 5 |
| 19 | NFC ile demirbaş takibi | Proje · 5 |
| 20 | **Topluluk:** SK 3D Topluluğu — arıza çözme açısı | Topluluk · 5 |
| 21 | Tavan arası kamera robotu | Proje · 5 |
| 22 | RC tank: büyük baskı projesi | Proje · 6 |
| 23 | Oyuncak yol seti: modüler parça tasarımı | Proje · 5 |
| 24 | FPV drone: Cinelog20 kurulumu | Proje · 5 |
| 25 | Pi 5 ekran standı | Proje · 4 |
| 26 | Cam sehpa küre ayak üretimi | Proje · 4 |
| 27 | Anatomi maketleri: 15 parçalık iş | Proje · 5 |
| 28 | Cephe yıkama dronu | Proje · 6 |
| 29 | Yeşilay astronot maskotu | Proje · 4 |
| 30 | **Topluluk:** SK 3D Topluluğu — model paylaşımı açısı | Topluluk · 5 |

---

# 8. SIRALAMA MANTIĞI

İlk üç günün verisi: en geniş ve en acemi dostu konu (dört filament karşılaştırması) diğerlerinin üç katı erişim aldı, en dar ve en kişisel olan (atölye düzeni) en dibe düştü. Paylaşım ve yeni takipçi her gönderide sıfır.

Kalan konular bu yüzden zorluk sırasına göre yeniden dizildi: önce herkesin karşılaştığı sorunlar (stringing, warping, elephant foot), derin teknik konular ve proje anlatıları sona bırakıldı. Takipçi tabanı oluştukça o konular da karşılığını bulur.

Proje slotunda da aynı mantık: "benim projem" içeriği henüz kimse hesabı tanımadığı için tutmuyor. Önce işe yarayan şeyler (model kaynakları, alet listesi, fiyatlama), projeler sonra.

Kullanılmış konuların numaraları değişmedi; `DURUM.json` ile uyum korunuyor.

# 9. KAPSAM DIŞI

Bu hesap **Sermen Kreatif**'in hesabı. AR-GE biriminin kurumsal projeleri buraya girmez.

- **BİLGE** kurumun yüzü, bu hesapta anlatılmaz. Sesli asistan konusu işlenecekse **ATLAS** üzerinden işlenir.
- Kurumsal bir işten söz edilecekse ürüne ya da yönteme odaklanılır, kurumun adı öne çıkarılmaz.

# 10. TOPLULUK GÖNDERİLERİ

WhatsApp grubu hesabın en değerli çıktısı: takipçi akışta kaybolur, gruba giren kalır.

**Link bio'da.** Instagram açıklama metninde link tıklanmıyor. Grup bağlantısı profildeki bio alanında duracak, gönderiler oraya yönlendirecek ("profildeki linkten katıl"). Gönderi metnine ham WhatsApp adresi yazma, tıklanmadığı için sadece kalabalık yapar.

**Hikayeye link çıkartması ekle.** Hikayede link çalışıyor. Topluluk hikayesi yayınlandıktan sonra Instagram'dan link çıkartması eklenip öne çıkanlara kaydedilirse kalıcı bir giriş kapısı oluyor. Bu adım elle yapılıyor, otomatik değil.

**Vaat abartılmaz.** Grupta gerçekten ne varsa o yazılır. "Binlerce model" gibi doğrulanamayan sayı kullanılmaz.

# 11. ÜRÜN TANITIMI KURALLARI

Ürün gönderileri hesabın mağazaya bakan yüzü. Üçü birden zorunlu:

**Doğrula, hatırlama.** Her ürün gönderisinden önce web'de ara. Model adları, fiyatlar ve ürün gamları hızlı değişiyor; hafızadan yazılan özellik yanlış çıkıyor.

**Çıkmamış ürünü çıkmış gibi anlatma.** Duyurulmuş ama raflarda olmayan ürün karşılaştırmaya sokulmaz. Konu buysa açıkça "henüz çıkmadı" denir — bu zaten kendi başına haberdir.

**Fiyat yazma.** Fiyat en hızlı eskiyen bilgi. Gönderide fiyat yerine konumlandırma yazılır ("giriş seviyesi", "kapalı kabinli orta sınıf"). Fiyat sermenkreatif.com'da, gönderi oraya yönlendirir.

**Görsel gerçek fotoğraf olacak, vektör çizim değil.** Fotoğrafı İlhan veriyor; ham kareden arka planı kesilip `arac/studyo.py` ile stüdyo karesine çevriliyor (bkz. `gorsel/BENIOKU.md`). Fotoğraf yoksa gönderi üretilmiyor — kareye "FOTOĞRAF YOK" basılıyor ve üretici uyarı veriyor. Google görselinden indirilen kare ticari gönderide kullanılmıyor.

Gelen fotoğrafın anlatılan ürün olduğu doğrulanmadan klasöre konmuyor. Bu sette iki kere lazım oldu: R1 gönderisi için gelen kare aslında açık gövdeli bir diyot lazerdi, kurutucu setindeki "SP2" aslında S4'tü.

Etiketler: `@bambulab`, `@sunlu3d`, `@snapmaker`, `@creality3dofficial`, `@crealityfalcon` — hangi marka geçiyorsa. Ürün etiketi ve konum etiketi eklenir.

# 12. HAFTALIK İŞ DÜZENİ

Günde 4 gönderi + 4 hikaye + 1 reels = haftada 28 gönderi, 28 hikaye, 7 reels. Her gün tek tek üretmek sürdürülemez.

**Pazar günü toplu üretim.** Haftanın 28 gönderisinin görselleri tek oturumda üretilir, metinleri yazılır, reels'ler render edilir, Metricool'a yüklenip zamanlanır. Hafta içi sadece yorum yanıtlamak kalır.

**Metricool kotası.** Ücretsiz planda aylık 20 planlama hakkı var; 28'lik haftaya yetmiyor. Kota dolunca gönderiler `ERROR: You have reached your Metricool account limit` ile düşüyor ve sessizce yayınlanmıyor. İki yol var: plan yükseltilecek ya da günlük yayın Meta Business Suite üzerinden elle yapılacak. `YAYIN-LISTESI.md` her iki durumda da sıranın tek kaynağı.

**Yorumlara ilk bir saat içinde dön.** Gönderi sonrası ilk saatteki etkileşim dağılımı belirliyor.

**Haftada bir ölçüm.** Metricool'dan gönderme (send) ve kaydetme sayılarına bak; beğeniye bakma. En çok yollanan üç gönderinin ortak yanı neyse sonraki haftanın konuları oraya kayar.
