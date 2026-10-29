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
