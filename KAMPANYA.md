# Dört Makara — 12-15 Ekim 2026

Dört Creality filament, **hepsi tek kazanana**. Duyuru 12 Ekim, son
gün 15 Ekim 23.59, sonuç 16 Ekim.

| Ödül | Ürün | Kime yarar |
|---|---|---|
| 1 | Creality CR-PLA Silk · Mavi | parlak yüzey, dekoratif baskı |
| 2 | Creality CR-TPU · Siyah | esnek parça: conta, tampon, kılıf |
| 3 | Creality CR-PETG · Mavi | dayanıklı, dış mekâna uygun |
| 4 | Creality CR-ABS · Mavi | ısıya dayanıklı, kabin isteyen işler |

Hepsi 1,75 mm · 1 kg. Dördü tek kutuda tek kişiye, kargo bizden, Türkiye içi.

## Kazananı takipçi anketi seçiyor

İki sorun aynı anda çözülüyor:

**Güven.** Jüri kararıyla seçilen kazanana kimse inanmıyor, "tanıdığına
verdi" deniyor. Bu yüzden son kararı biz vermiyoruz: üç finalistin yorumu
olduğu gibi hikayeye konuyor — kim yazmış, ne yazmış açık — ve kazananı
takipçi anketi belirliyor. Oylama bitince anketin ekran görüntüsü de
paylaşılıyor.

**Eleme öznel değil, kurallı.** Finalistlere kalmanın tek şartı yorumun
soruyu cevaplaması: ne basacağını yazan kalır, "katıldım" yazan elenir.
Bu kural duyuru gönderisinde yazıyor.

## Kura yok — sebebi

Rastgele kura ile yapılan ödüllü kampanya, mevzuatta **"karşılığı nakit
olmayan piyango"** sayılıyor. Yönetmeliğe göre ticari firmaların böyle bir
çekiliş düzenlemesi için **önceden izin alması** gerekiyor (md. 7, 8/a);
başvuru kampanya başlamadan **en az 15 gün önce** yapılıyor (md. 12) ve
ikramiye toplamının **%10 fazlası teminat** isteniyor (md. 11). İzinsiz
düzenlenen çekilişte İdare, mülki amirden faaliyetin durdurulmasını ve
tanıtımların kaldırılmasını isteyebiliyor (md. 5). Bugün başlayıp dört gün
sürecek bir kampanyada bu izni almaya vakit yok.

Bu yüzden kurgu **kurasız**: finalistler yorumun içeriğine göre, kazanan
takipçi oyuyla belirleniyor. Rastgelelik olmayınca iş piyango değil,
oylamaya dayalı bir seçim oluyor.

Avukat değilim; kesin konuşmak istersen mali müşavirine ya da avukatına
sor. Mevzuat: Millî Piyango İdaresi Genel Müdürlüğü Karşılığı Nakit
Olmayan Piyangolar ve Çekilişler Hakkında Yönetmelik.

## Katılım kuralları (gönderide yazan hâli)

1. @sermenkreatif hesabını takip et
2. Duyuru gönderisini beğen
3. Yoruma ne basacağını tek cümleyle yaz

Soruyu cevaplamayan yorum elenir. Üç finalist 16 Ekim'de hikayede
oylanır, en çok oyu alan kazanır.

Arkadaş etiketlemek isteğe bağlı. Katılım ücretsiz; link, form, ödeme yok.
Türkiye içinden, 18 yaş ve üstü. Dört makaranın hepsi tek kazanana gidiyor.
Değerlendirmeyi sermenkreatif yapıyor, Instagram'ın seçimle ilgisi yok.

## Afiş nasıl üretiliyor

Kampanya kapağı normal gönderi kapaklarından ayrı: dev başlık, konfeti,
podyumda dört ürün, kural kutusu ve alt şerit.

```
python3 uret.py 2026-10-12-cekilis-duyuru/spec.json 2026-10-12-cekilis-duyuru
python3 arac/cekilis_afis.py 2026-10-12-cekilis-duyuru
python3 arac/cekilis_afis.py 2026-10-15-cekilis-son-gun --son
```

**Sıra önemli:** `uret.py` 2-5. slaytları üretiyor, `cekilis_afis.py`
sonra çalışıp `1.jpg` ve `hikaye.jpg` dosyalarının üzerine afişi yazıyor.
Ters sırada çalıştırılırsa afiş silinir, normal kapak geri gelir.

Ürün kareleri `gorsel/urun/kesik-cekilis-*.png` — satıcı sayfalarından
otomasyonla çekildi.

## Dolandırıcılık uyarısı

Kazanana **yalnız @sermenkreatif hesabından** DM atılıyor. Ödül için
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
| 16 Ekim Cum | 11:00 | Üç finalistin yorumu hikayede, anket açılıyor |
| 16 Ekim Cum | 20:00 | Anket kapanıyor |
| 16 Ekim Cum | 21:00 | Sonuç gönderisi + anket ekran görüntüsü |

Kampanya kayıtları `DURUM.json` → `kuyruk_bekleyen.kampanya` içinde,
dört slotluk günlük ızgaranın dışında duruyor.

## Sonuç gönderisi

**Henüz üretilmedi.** İkisi de 16 Ekim'de, yorumlar geldikten sonra
üretiliyor:

1. Yorumları oku. Soruyu cevaplamayanları ele, kalanlardan üç finalist
   seç. Finalistlerin kullanıcı adını ve yorumunu bana yolla.
2. Finalist hikayesini üretirim — üç yorum olduğu gibi, altında anket.
   Anketi Instagram uygulamasından koyuyorsun; API anket çıkartamıyor.
3. Akşam anket sonucunu yolla. `2026-10-16-cekilis-sonuc` gönderisini
   üretirim: kazanan, yorumu ve oy dağılımı.
4. Kazanana @sermenkreatif hesabından DM at, adres ve kargo bilgisi iste.

Hikaye anketi elle konuyor: Instagram Graph API hikayeye anket, link ya
da geri sayım etiketi ekleyemiyor (bkz. `otomasyon/YAYIN-KURULUM.md`).
