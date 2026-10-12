# Kurumsal gönderiler ve içerik revizyonu

Şu ana kadarki gönderiler iki tür: ürün tanıtımı ve teknik bilgi. Eksik
olan üçüncü tür, **şirketin kendisi**: ne yapıyoruz, nasıl çalışıyoruz,
neden biz. Mağazanın menüsünde duran "3D Baskı Hizmeti" hiç anlatılmadı.

Yeni kategori: **kurumsal**. Vurgu rengi markanın kırmızısı (244, 93, 90);
teknik kategorilerden ilk bakışta ayrılıyor. Tek renk — kart içindeki
değerler de beyaz basılıyor, sarı yok (`sade` modu).

## Kurumsal gönderi dizisi

Ayda bir dönen beş gönderi. Hepsi doğrulanabilir bilgiyle kuruluyor;
makine sayısı, kapasite, "%100 kalite" gibi ölçülemeyen iddia yazılmıyor.

| # | Gönderi | Ne anlatıyor | Kaynak |
|---|---|---|---|
| 1 | **Neden Sermen Kreatif** | Malzeme ailesi, marka sayısı, yedek parça, taksit, kargo, baskı hizmeti | Katalog + site üst şeridi |
| 2 | **Baskı hizmeti nasıl işliyor** | Dosya → teklif → baskı → kontrol → kargo, beş adım | Hizmet sayfası |
| 3 | **Neler basıyoruz** | Prototip, makine parçası, jig & fikstür, aparat, dekoratif, yedek parça | Yapılan işler |
| 4 | **Hangi malzemeden basılır** | PLA · PETG · ABS · ASA · TPU · reçine — hangi iş hangi malzeme | Ürün sayfaları |
| 5 | **Atölyeden** | Gerçek tezgâh fotoğrafı, çalışan makineler | Fotoğraf çekilecek |

1 hazır (`2026-10-20-neden-sermen`), 2-4 aynı kalıptan çıkıyor. 5 için
atölyenin kendi fotoğrafı gerekiyor — üretilmiş fotoğraf kullanılmıyor,
sattığı hizmetin sahte fotoğrafı olur.

## Elektronik kategorisi — sorun ve çözüm

Sitede elektronik satılmıyor. Menü: 3D Yazıcılar, 3D Tarayıcılar,
Filamentler, Reçineler, Yedek Parça & Aksesuar, 3D Baskı Ürünleri,
3D Baskı Hizmeti. `espressif-116`, `pixhawk-65` gibi marka sayfaları
duruyor ama açınca "ÜRÜN BULUNMAMAKTADIR" diyor.

Yani optokuplör, BMS, H köprüsü gibi gönderiler satılmayan bir şeyi
anlatıyordu. İnsanların "anlamsız" demesinin sebebi tasarım değil, bu.

Kategori kalıyor ama içeriği değişiyor: **elektronik tek başına konu
olmaktan çıkıyor, basılmış parçayla birlikte anlatılıyor** ve her gönderi
satılan bir malzemede bitiyor.

| Eski | Yeni |
|---|---|
| "Optokuplör ne zaman şart" | "Elektronik kutusu basarken: hangi malzeme, hangi tolerance" |
| "BMS neyi koruyor" | "Pil kutusu tasarımı — ısıya dayanacaksa PETG, neden" |
| "Deep sleep akımı" | "Sensör muhafazası: dışarıda duracaksa ASA" |

Ortak kural: elektronik bilgisi kancayı kuruyor, **baskı tarafı gönderinin
gövdesi oluyor**, kapanış satılan malzemeye bağlanıyor.

Yazılmış olan optokuplör gönderisi silinmedi, 19 Ekim'de duruyor.

## Tasarım değişikliği

ESTA3D'nin işe yarayan tarafı şu: koyu zemin, **tek** vurgu rengi, simge
ızgarası, kısa ve kalın yazı, paragraf yok. Bizdeki dağınıklığın sebebi
kart başına ayrı renk ve slayt başına paragraf.

| | Eski | Yeni |
|---|---|---|
| Renk | Kart başına ayrı renk | Tek vurgu rengi |
| Değer rengi | Sarı | Beyaz (`sade`) |
| Metin | 4-5 satır paragraf | 1-2 satır |
| Kapak | Başlık + spot | Başlık + simge ızgarası |

`sade` modu `kategori: "kurumsal"` olunca kendiliğinden açılıyor; başka
kategoride `"sade": true` ile açılıyor.
