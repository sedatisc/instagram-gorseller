# Dört Makara — 12-15 Ekim 2026

Dört Creality filament, dört ayrı kazanan. Duyuru 12 Ekim, son gün
15 Ekim 23.59, sonuç 16 Ekim.

| Ödül | Ürün | Kime yarar |
|---|---|---|
| 1 | Creality CR-PLA Silk · Mavi | parlak yüzey, dekoratif baskı |
| 2 | Creality CR-TPU · Siyah | esnek parça: conta, tampon, kılıf |
| 3 | Creality CR-PETG · Mavi | dayanıklı, dış mekâna uygun |
| 4 | Creality CR-ABS · Mavi | ısıya dayanıklı, kabin isteyen işler |

Hepsi 1,75 mm · 1 kg. Kişi başı bir makara, kargo bizden, Türkiye içi.

## Kura yok — sebebi

Rastgele kura ile yapılan ödüllü kampanya, mevzuatta **"karşılığı nakit
olmayan piyango"** sayılıyor. Yönetmeliğe göre ticari firmaların böyle bir
çekiliş düzenlemesi için **önceden izin alması** gerekiyor (md. 7, 8/a);
başvuru kampanya başlamadan **en az 15 gün önce** yapılıyor (md. 12) ve
ikramiye toplamının **%10 fazlası teminat** isteniyor (md. 11). İzinsiz
düzenlenen çekilişte İdare, mülki amirden faaliyetin durdurulmasını ve
tanıtımların kaldırılmasını isteyebiliyor (md. 5). Bugün başlayıp dört gün
sürecek bir kampanyada bu izni almaya vakit yok.

Bu yüzden kurgu **kurasız**: kazananlar yorumların içeriğine göre
seçiliyor. Rastgelelik olmayınca iş piyango değil, değerlendirmeye dayalı
bir seçim oluyor. Gönderi metninde de bu açıkça yazıyor: "Kura çekmiyoruz,
cevaplara bakıyoruz."

Avukat değilim; kesin konuşmak istersen mali müşavirine ya da avukatına
sor. Mevzuat: Millî Piyango İdaresi Genel Müdürlüğü Karşılığı Nakit
Olmayan Piyangolar ve Çekilişler Hakkında Yönetmelik.

## Katılım kuralları (gönderide yazan hâli)

1. @sermenkreatif hesabını takip et
2. Duyuru gönderisini beğen
3. Yoruma hangi filamenti neden istediğini yaz — ne basacağını anlat

Arkadaş etiketlemek isteğe bağlı. Katılım ücretsiz; link, form, ödeme yok.
Türkiye içinden, 18 yaş ve üstü. Aynı kişi birden fazla makara alamıyor.
Değerlendirmeyi sermenkreatif yapıyor, Instagram'ın seçimle ilgisi yok.

## Dolandırıcılık uyarısı

Kazananlara **yalnız @sermenkreatif hesabından** DM atılıyor. Ödül için
ödeme, kart bilgisi ya da kargo ücreti isteyen her mesaj sahtedir. Bu
uyarı hem kapanış slaydında hem gönderi metninde duruyor — ödüllü
kampanyaların ardından taklit hesaplar her seferinde yazıyor.

## Takvim

| Tarih | Saat | Ne |
|---|---|---|
| 12 Ekim Pzt | 13:30 | Duyuru gönderisi (4 kare) + 14:10 hikaye |
| 13 Ekim Salı | 19:10 | Hatırlatma hikayesi |
| 14 Ekim Çar | 19:10 | Hatırlatma hikayesi |
| 15 Ekim Per | 18:40 | Son gün gönderisi + 19:20 hikaye |
| 15 Ekim Per | 23:59 | Yorumlar kapanıyor |
| 16 Ekim Cum | — | Sonuç gönderisi |

Kampanya kayıtları `DURUM.json` → `kuyruk_bekleyen.kampanya` içinde,
dört slotluk günlük ızgaranın dışında duruyor.

## Sonuç gönderisi

**Henüz üretilmedi.** Kazananlar belli olmadan üretilmiyor; 16 Ekim'de
yorumlar değerlendirilince dört kazananın kullanıcı adı ve hangi makarayı
aldığı yazılarak çıkarılacak. O gün yapılacak:

1. Yorumları oku, dört kazananı seç (ne basacağını en net anlatanlar).
2. `2026-10-16-cekilis-sonuc` klasörünü üret — kapakta dört kazanan.
3. Kuyruğa `kampanya` kaydı olarak ekle, `python3 sira.py` ve
   `python3 paket.py` çalıştır.
4. Kazananlara @sermenkreatif hesabından DM at, adres ve kargo bilgisi
   iste.
