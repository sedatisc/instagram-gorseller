# Yapı

Tek kaynak `icerik.json`. Her gönderi orada bir satır; gün numarası
tutulmuyor.

## icerik.json

```json
{"klasor": "2026-10-23-sekil-cark-tahtasi",
 "kategori": "baski",
 "konu": "sekil-cark-tahtasi",
 "durum": "hazir",
 "kare": 4,
 "reels": true}
```

| alan | ne işe yarıyor |
|---|---|
| `kategori` | `rehber` · `baski` · `magaza` · `proje` · `kampanya` |
| `konu` | Aynı konunun iki klasörü varsa ikisine de aynı anahtar yazılır; plan konuyu bir kere dizer |
| `durum` | `hazir` · `yayinlandi` · `beklemede` · `iptal` |
| `tarih` | Yalnız `yayinlandi` için — hangi gün çıktığı |
| `neden` | Yalnız `beklemede` / `iptal` için — niçin planda olmadığı |
| `reels` | Klasörde `reels.mp4` varsa |

## Takvim nasıl çıkıyor

Durumu `hazir` olan işler kategorisindeki sırayla günlere diziliyor:
her kategorinin birinci işi birinci güne, ikincisi ikinci güne. Tarih
içeriğin içinde yazmıyor, sırasından çıkıyor.

Bunun üç sonucu var:

- **Aksayan iş kaybolmuyor.** Yayınlanmayan iş `hazir` kaldığı için
  sıradaki güne kendiliğinden kayıyor. Eski yapıda atlanan işin ayrıca
  deftere yazılması gerekiyordu, yazılmazsa o günün içeriği düşüyordu.
- **Aynı iş iki kere planlanamıyor.** Gün numarası elle tutulmadığı için
  kayma da yok; `konu` anahtarı aynı konunun ikinci klasörünü eliyor.
- **Yayınlanmış konu plana geri girmiyor.** Kuyruk, `yayinlandi` olan
  işlerin konu listesiyle başlıyor; aynı konunun başka bir klasörü de
  olsa eleniyor. Bir işin gönderisi paylaşıldıysa videosu çekilmemiş
  olsa bile durumu `yayinlandi` olmalı — `beklemede` bırakılırsa konu
  kuyrukta kalıyor ve ikinci kez paylaşılıyor.
- **Elle paylaşılan iş kuyrukta kalmıyor.** `yayinlandi` yazıldığı anda
  plandan düşüyor, listede o slot "Yayınlandı" diye görünüyor.

Videolar: günde tek reels var, video konusunun kendi gönderisiyle aynı
güne biniyor. İki video aynı güne denk gelirse biri kendi
kategorisindeki bir sonraki videosuz işle yer değiştiriyor — konu iki
güne yayılmıyor, video da beklemiyor.

Kampanyaların iki türü var. Çekiliş gibi işler planla birlikte kayıyor
(`gun`: başlangıçtan kaç gün sonra). Bayram gibi işler kaymıyor: kaydına
`tarih` yazılıyor, o gün geçtiyse iş plandan düşüyor.

Planın birinci günü: ilk gerçek yayında takvime çivileniyor
(`otomasyon/plan-durumu.json`). O güne kadar "bugünden itibaren"
gösteriliyor; günün ilk gönderi saati geçtiyse yarından başlıyor.

## Slotlar ve bağlantılar

Günün üç gönderi slotu var: `s1` sabah, `s2` öğle, `s3` akşam. Hangi
kategorinin geleceği sabit değil. `sira.TERCIH`e göre s2 ve s3 baskı
ürününü tercih ediyor, s1 dönen kategoriyi (rehber → mağaza → proje,
`sira.DONEN`). Bir kuyruk boşalınca slot dolu olan kuyruktan besleniyor:
baskı ürünü bittiğinde gün yarım kalmıyor, plan üç gönderiyle sürüyor.

Günde tek reels var. İki video aynı güne denk gelirse biri kuyrukta bir
videosuz işle yer değiştiriyor; o da olmazsa video sonraki boş güne
kayıyor. Hiçbir video düşmüyor — reels takipçi olmayana ulaşan tek biçim.

Beş gönderiden üçe inildi: aynı gün yayımlanan gönderiler akışta
birbiriyle yarışıyor, kişi başı etkileşim düşüyor. Keşfet'e düşüren şey
gönderi sayısı değil, takipçi olmayana gösterilme sinyalleri — izlenme
süresi, gönderim (paylaş/DM) ve erişim başına beğeni.

Metin kuralları buradan çıkıyor: her gönderide en çok 5 etiket (etiket
erişime katkı vermiyor, Instagram da 5'te sınırlıyor) ve metnin sonunda
"bunu şuna yolla" cümlesi — gönderim, takipçi olmayana ulaşmada en ağır
sinyal.

Baskı ürününün görselleri sitenin kendisinden geliyor. Başka görsel
kullanılmıyor: `baglantilar.json`'da ürünün `gorsel` listesi boşsa o ürün
plana hiç girmiyor (`SİTE GÖRSELİ YOK` uyarısı) ve Buffer'a gitmiyor —
depodaki kareye düşülmüyor. Liste dolunca gönderi o görsellerle, hikaye
listenin ilkiyle gidiyor.

## Oyun ve uygulama gönderileri

`uygulama` kategorisi Google Play'deki kendi oyun ve uygulamalarımız
için. Klasörü `uygulama/<slug>`; içinde akış kareleri (`1.jpg`…),
`hikaye.jpg` ve `metin.md` var. Kareler uygulamanın kendi mağaza
tasarımından ve Play'deki gerçek ekran görüntülerinden geliyor —
yapay zekâ beyanı bu yüzden kapalı.

Play adresi `baglantilar.json`'daki `uygulama` eşlemesinde, anahtar
klasörün son parçası. Hikaye bağlantı etiketi ve metindeki "Uygulama
sayfası" satırı oradan geliyor.

Slot sırasında `uygulama`, s1'in dönen kategorilerine katıldı
(rehber → mağaza → proje → uygulama). Üç uygulama olduğu için aynı
uygulama on iki günde bir dönüyor.

Ürün bağlantıları aynı dosyada. Anahtar, icerik.json'daki `konu`.
Gönderi metninde `{urun_linki}` ürünün `sayfa` adresine dönüyor; boşsa
`varsayilan` (site adresi) yazılıyor. Baskı ürünü ve mağaza
gönderilerinin hikayesi de aynı bağlantıyı taşıyor. Buffer şemasında
`link` alanı var: hikayeye bağlantı etiketi olarak gidiyor. Şemada `firstComment` alanı
görünüyor ama ücretsiz planda dolu gönderilince istek
"First comment requires a paid plan" diye reddediliyor — 6 Kasım'da bir
gönderi ve bir reels bu yüzden düştü. Artık o hata gelince ilk yorum
metnin sonuna indirilip gönderi bir kez daha deneniyor; iş düşmüyor.
`buffer_gonder.py --kontrol` ikisini de yazdırıyor.

Gün ortasında plana iş eklenirse `otomasyon/TETIK` dosyası değiştirilip
itiliyor: `buffer.yml` bu yola gelen itmede `--zorla` ile çalışıyor,
deftere girmiş ve saati geçmiş işleri atlayıp yalnız yenileri
gönderiyor.

Buffer'a gönderilen her Instagram işinde `shouldShareToFeed` zorunlu —
yalnız reels'e konduğu için gönderi ve hikaye "required field" hatasıyla
düşüyordu. Şemada zorunlu görünen başka alan varsa türüne uygun değerle
dolduruluyor. `otomasyon/buffer_deneme.py`, Buffer'ın doğrulamasını
taklit eden bir sunucuya karşı günün işlerini gönderip yükün şeklini
anahtar olmadan sınıyor.

Buffer ücretsiz planında günde en çok 10 bekleyen paylaşım var. Sınır
aşılırsa hikayeler şu sırayla düşüyor: kampanya, proje, rehber, mağaza.
Baskı ürününün hikayesi düşmüyor — ürün bağlantısı oradan veriliyor.

## Ürün gönderileri katalogdan geliyor

Baskı ürünü gönderilerinin klasörü yok. `icerik.json`'da `klasor` alanı
`urun/<site-slug>` biçiminde; ad, açıklama, fiyat ve görseller
`urunler.json`'dan, o da sermenkreatif.com ürün sayfalarındaki Product
verisinden geliyor. Gönderi metnini `arac/urun_katalog.py` üretiyor:
ürün adı, site açıklaması, baskı notu, fiyat, ürün sayfası bağlantısı,
"şuna yolla" cümlesi ve kategoriye göre 5 etiket.

Sonucu: ürün sayfası değişince gönderi de değişiyor, elle yazılmış metin
ve elle basılmış kare yok. Görsel yalnız siteden geliyor.

`arac/katalog_cek.py` siteyi tarayıp katalogu yeniliyor,
`arac/katalog_plan.py` yeni ürünü plana alıyor ve satıştan kalkanı
plandan düşürüyor. İkisini `.github/workflows/katalog.yml` her gece
23.40'ta çalıştırıyor — yeni ürün siteye girdiği gün yayın sırasına
katılıyor.

## Komutlar

```
python3 sira.py                              # liste + paket üret
python3 sira.py yayinlandi <klasor> [tarih]  # yayınlandı işaretle
python3 sira.py beklet <klasor> <neden>      # plandan çıkar
python3 sira.py geri <klasor>                # plana geri al
python3 uret_hepsi.py [klasor...]            # kareleri bas
```

Üretilen dosyalar — elle düzenlenmiyor: `YAYIN-LISTESI.md`,
`YAYIN-PAKETI.md`, `yayin-paketi.html`.
