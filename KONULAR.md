# Konu planı

Elektronik kategorisi kapandı: sitede elektronik satılmıyor (menü 3D
Yazıcılar, 3D Tarayıcılar, Filamentler, Reçineler, Yedek Parça &
Aksesuar, 3D Baskı Ürünleri, 3D Baskı Hizmeti). Marka sayfaları duruyor
ama "ÜRÜN BULUNMAMAKTADIR" diyor. Satılmayan şeyi anlatmak hem ilgi
çekmiyor hem satmıyor.

Yeni dört hat. Hepsi satılan bir şeye bağlanıyor.

| Hat | Ne satıyor | Biçim |
|---|---|---|
| **Ayar & Rehber** | Filament, nozul, tabla — sarf | Referans tablosu |
| **Ürün** | Makine, tarayıcı, aksesuar | Ürün tanıtımı |
| **Baskı Ürünleri** | Kendi bastığımız ürünler | Ürün kartı |
| **Atölye & Hizmet** | 3D baskı hizmeti | Proje anlatımı |

Kapanan elektronik slotunun yerine **Baskı Ürünleri** geçiyor. Sebebi:
sitede 160 civarı basılı ürün var ve bugüne kadar tek gönderi
yapılmadı.

---

## 1 · Ayar & Rehber — referans tablosu

Ekran görüntüsü alınıp saklanan kare. Rakamların hepsi ürün
sayfalarından çekiliyor, uydurma yok.

| # | Konu | Veri |
|---|---|---|
| 1 | Filament ayar rehberi — 8 malzeme | ✅ hazır, 13 Ekim |
| 2 | Katman yüksekliği × nozul çapı | Hesapla çıkıyor |
| 3 | Hangi nozul hangi makineye | Phaetus sayfaları |
| 4 | Tabla ve yüzey kaplaması uyumluluğu | Yedek parça kategorisi |
| 5 | Reçine ayar rehberi — pozlama, katman | Anycubic sayfaları |
| 6 | Kurutma rehberi — hangi filament kaç derece | Sunlu + Polymaker |
| 7 | Baskı sorunu → sebep tablosu | Katalog gerekmiyor |
| 8 | Dolgu oranı × dayanım × süre | Hesapla çıkıyor |
| 9 | Destek ayarları: ne zaman, hangi açı | Hesapla çıkıyor |
| 10 | Filament markaları toleransa göre | Ürün sayfaları |

## 2 · Ürün — gerçek ürün tanıtımı

Fotoğraf kendi ürün sayfasından, rakamlar iki kaynaktan doğrulanıyor.

| # | Konu | Durum |
|---|---|---|
| 1 | Phaetus Conch M4 EndCoat nozul | ✅ hazır, 13 Ekim |
| 2 | Creality CR-Scan ailesi: Raptor · Otter · Ferret | Tarayıcı kategorisi hiç anlatılmadı |
| 3 | Bambu Lab A2L | Yeni makine |
| 4 | Phaetus Conweb cool plate tablalar | K1C, H2D, P2S, Qidi |
| 5 | Anycubic Photon Mono M7 serisi | Reçine yazıcı |
| 6 | Sunlu FilaDryer S2 · S4 · E2 | ✅ yazılmış |
| 7 | Sunlu AMS Heater | ✅ yazılmış |
| 8 | Polymaker PolyDryer | Modüller kategorisi |
| 9 | Creality Space Pi kurutucu | Modüller |
| 10 | Bambu Lab AMS 2 Pro | Modüller |

## 3 · Baskı Ürünleri — kendi bastıklarımız

Kategori sayfasında 108 ürün sayıldı, bugüne kadar hiçbiri
paylaşılmadı. En kolay içerik burası: ürün zaten basılmış, fotoğrafı
zaten çekilmiş. Şablon `arac/urun_karti.py`; ürünün slug'ı yazılınca
ad, fiyat ve fotoğraf ürün sayfasından geliyor.

| Tarih | Grup | Durum |
|---|---|---|
| 14 Ekim | Atölyeden çıkanlar — altı ayrı grup | ✅ hazır |
| 15 Ekim | Saksı koleksiyonu — 6 saksı | ✅ hazır |
| 16 Ekim | Vazo koleksiyonu — 6 vazo | ✅ hazır |
| 17 Ekim | Masa düzeni — 6 düzenleyici | ✅ hazır |
| 18 Ekim | Basılmış ışık — 5 lamba | ✅ hazır |
| 19 Ekim | Banyo düzeni — 6 parça | ✅ hazır |
| 20 Ekim | Makyaj & takı — 6 parça | ✅ hazır |
| 21 Ekim | Küçük hediyelikler — 6 parça | ✅ hazır |

Sırada bekleyen gruplar: mutfak & servis (dalga formlu tepsi, modern
kâse, yaprak kâse), duvar saatleri, oyun & maket (cribbage seti,
dondurma kulesi, mini yol maketi, kafatası maketi), eğitim (ayak
kemikleri modelleri).

Sezon bağlantısı: balkabağı mumluk → ekim sonu (21 Ekim gönderisinde),
noel çorabı ve şapkası anahtarlıkları → aralık.

**Kullanılmayan iki ürün:** TNT blok anahtarlık ve Mustang anahtarlık
askısı gönderiye konmadı — ikisi de başkasının markası, paylaşımda
sorun çıkarabilir.

## 4 · Atölye & Hizmet — baskı hizmeti

Menüde "3D Baskı Hizmeti" var, hiç anlatılmadı. Sitede "dosyanı yükle,
anında fiyat al" sayfası bile duruyor.

| # | Konu |
|---|---|
| 1 | Dosyanı yükle, fiyatını gör — hizmet nasıl işliyor |
| 2 | Hangi dosya formatı, hangi ölçü sınırı |
| 3 | Prototipten seri üretime: aynı parçanın yolculuğu |
| 4 | Yazıcın yoksa ne yapıyorsun — hizmetin kime lazım olduğu |
| 5 | Ölçü doğrulama: seriye başlamadan önce | ✅ yazılmış |
| 6 | Müşteriye fiyat vermek, altı kalem | ✅ yazılmış |
| 7 | Atölyeden: çalışan makineler (fotoğraf senden) |
| 8 | Bozulan baskının sebebi — gerçek örnekler |

---

## Haftalık düzen

| Saat | Hat |
|---|---|
| 08:12 | Ayar & Rehber |
| 12:38 | Baskı Ürünleri |
| 17:24 | Ürün |
| 20:42 | Atölye & Hizmet |

Reels akşam, kuyruktaki ürün gönderisinden.

## Elektronikten arta kalanlar

Yazılmış ama yayımlanmamış elektronik gönderileri siliniyor değil,
kuyruktan çıkarılıyor: optokuplör, BMS, H köprüsü, kondansatör ESR,
deep sleep. Bir gün elektronik satılırsa hazır duruyorlar.

Pano gönderileri (ESP32 ailesi, geliştirme kartı, Pixhawk, Pi kamera)
gerçek ürün fotoğrafı taşıyor ama o ürünler de satılmıyor; onlar da
kuyruktan çıkıyor.
