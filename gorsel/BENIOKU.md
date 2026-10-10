# Fotoğraflar

## Fotoğraf nereden geliyor — üç kaynak

**1. İlhan'ın gönderdiği kare.** En iyisi, şartı yok. Filament, kurutucu,
hotend tarafı böyle yürüyor.

**2. Üreticinin GitHub dokümantasyon deposu.** Oturumun ağ erişimi
kapalı ama GitHub'dan anonim `git clone` çalışıyor. Birçok elektronik
üreticisi ürün fotoğraflarını dokümantasyon deposunda tutuyor:

```
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 \
  https://github.com/raspberrypi/documentation /home/claude/rpi-doc
```

Doğrulanmış depolar:

| Depo | Ne var | Lisans |
|---|---|---|
| `raspberrypi/documentation` | Pi 2/3/4/5, 400/500, Pico ailesi, CM modülleri — stüdyo kareleri, 1920 px'e kadar | CC BY-SA 4.0 |
| `espressif/esp-dev-kits` | ESP32 geliştirme kartları, izometrik PNG (çoğu saydam zeminli) | kod Apache-2.0, **görseller CC BY-SA 4.0** |

Denenmemiş ama muhtemel: `arduino`, `adafruit`, `sparkfun`, `Seeed-Studio`,
`prusa3d`. Gereken kart çıkınca önce buraya bak.

**CC BY-SA 4.0 ne demek:** atıf zorunlu *ve* türetilmiş eser aynı
lisansla paylaşılmalı. İkinci şart ticari gönderide zorlayıcı. Bu
kaynaktan görsel kullanılan her gönderinin `metin.md` dosyasına
kaynak + lisans satırı yazılacak ve İlhan'a ayrıca söylenecek —
sessizce kullanılmayacak.

**3. Hiçbiri yoksa.** Kareye yer tutucu basılır, gönderi yayına
alınmaz. Vektör çizimle ürün tanıtımı yapılmıyor.

**Web'den indirme çalışmıyor:** kabuk yalnız paket deposu ve GitHub'a
çıkabiliyor, diğer host'lar 403 dönüyor; WebFetch metin döndürüyor,
ikili dosya değil. Yani bambulab.com ya da sunlu.com'dan fotoğraf
çekilemiyor — SUNLU, Bambu Lab, Creality ve Anycubic görselleri için
İlhan'ın göndermesi gerekiyor.


Bu klasör üretilen karelerde kullanılan gerçek fotoğrafları tutuyor. İki yerde kullanılıyor:

1. **`liste` kapağının sağ sütunu** — `"kapak": { "tip": "liste", "gorsel": "atolye.png", ... }`. Fotoğraf varsa kullanılıyor, yoksa izometrik kule çiziliyor.
2. **`urun` gönderileri** — fotoğraf tam kareyi kaplıyor. Burada yedek çizim **yok**: dosya yoksa kareye "FOTOĞRAF YOK" ve beklenen dosya adı basılıyor, üretici de şu uyarıyı yazdırıyor:

```
UYARI — fotoğraf yok, kareye yer tutucu basıldı: gorsel/bambu-r1.jpg
```

Ürün tanıtımı vektör çizimle yapılmıyor; eksik fotoğraf sessizce gizlenmiyor, ekranda görünüyor.

## Ürün fotoğrafı şartları

- **Ölçü:** kapak fotoğrafı dikey ya da kare, en az 1400 × 1750 px. Hikaye de aynı dosyadan üretiliyor, o yüzden dikey olan daha iyi oturuyor.
- **Kompozisyon:** makine karenin üst üçte ikisinde dursun. Alt üçte bir yazıyla kaplanıyor, oraya önemli bir detay denk gelmesin.
- **Zemin:** koyu, sade, tek renk. Beyaz stüdyo fonu da olur ama o zaman `odak` değerini düşürüp makineyi yukarı çek.
- **Işık:** sol üstten. Diğer karelerdeki çizimlerle aynı yön.
- **Kaynak:** üreticinin basın kiti ya da kendi çektiğin fotoğraf. Google görselinden indirilen fotoğraf ticari gönderide kullanılmaz.
- `odak` alanı (spec içinde, 0-1) dikey kırpmayı kaydırıyor: 0 üstten, 1 alttan. Makine çerçeveden taşıyorsa önce bunu dene.

## Kapak fotoğrafı ile bant fotoğrafı farkı

- **Kapak** (`urun` tipi): fotoğraf yazının başladığı yere kadar iniyor, alt kenarı zemine eriyor. Bu yüzden kapak dosyası **1080 × 800** olarak hazırlanıyor ve `odak` 0 veriliyor; konu karenin alt kenarına yakın dursun, üstte biraz boşluk kalsın.
- **Bant** (slayttaki `foto`): üretici orijinali kendi kırpıyor. Dosyayı olduğu gibi koy, kadrajı slayttaki `odak` (0 üstten, 1 alttan) ile ayarla. `bant` yüksekliği değiştirilebiliyor.

## Klasördeki ürün fotoğrafları

| Dosya | Nerede kullanılıyor | Kaynak |
|---|---|---|
| `bambu-r1.jpg` | 2026-10-10 · kapak + hikaye | Bambu Lab ürün çekimi, 1080 × 800 kadraja hazırlandı |
| `bambu-r1-is.jpg` | aynı gönderi · 2. kare | Bambu Lab tezgâh çekimi, orijinal 2400 × 2400 |
| `bambu-r1-aks.jpg` | aynı gönderi · 4. kare | Ayrı satılan parçaların dizilişi, orijinal |
| `ender-v3-mega.jpg` | 2026-10-11 · kapak + hikaye | Creality ürün çekimi, 1080 × 800 kadraja hazırlandı |
| `ender-v3-mega-is.jpg` | aynı gönderi · 2. kare | Creality önden çekim, orijinal; `odak` 0,74 ile tablaya bakıyor |

## urun/ klasörü — stüdyo kompozitleri

Bu dosyalar ham fotoğraftan türetiliyor: arka plan `rembg` ile kesiliyor
(`kesik-*.png`), sonra `arac/studyo.py` zemini, gölgeyi ve yansımayı
çiziyor. Ham fotoğraf değişirse kesimi ve kompoziti yeniden üret.

| Dosya | Nerede kullanılıyor | Kaynak |
|---|---|---|
| `filadryer.jpg` | 10-14 · kapak, 2. kare bandı | SUNLU FilaDryer S2, tek ürün stüdyo |
| `filadryer-uclu.jpg` | 10-14 · kapak | S2 · S4 · E2 üçlü dizilim |
| `filadryer-e2.jpg` | yedek | E2 tek ürün |
| `ams-heater.jpg` | 10-15 · kapak + hikaye | SUNLU AMS Heater, tek ürün stüdyo |
| `liber.jpg` | 10-16 · kapak + hikaye | Phaetus × Snapmaker Liber dörtlü set (U1'in dört kafası için) |
| `ht-pla.jpg` · `htpla-uclu.jpg` | 10-17 | Polymaker HT-PLA |
| `kesik-s2.png` · `kesik-s4.png` · `kesik-e2.png` | 10-18 pano sütunları | arka planı kesilmiş PNG |
| `kesik-htpla*.png` | 10-19 pano sütunları | arka planı kesilmiş PNG |

**Orta kurutucu S4'tür, SP2 değil.** Gelen fotoğraf SP2 diye
adlandırılmıştı; dört dikey makara yuvası ve sekiz çıkışıyla SUNLU'nun
S4'ü olduğu doğrulandı. SP2 gerekirse ayrı fotoğraf lazım.

Fotoğrafı değiştirince gönderiyi yeniden üret:

```
python3 uret.py 2026-10-10-bambu-r1-tanitim/spec.json 2026-10-10-bambu-r1-tanitim
```

Uyarı satırı çıkmıyorsa bütün fotoğraflar yerine oturmuş demektir.

## cihaz/ klasörü

`gorsel/cihaz/` cihaz tanıtımlarının kapak fotoğraflarını tutuyor. Dosya adı `<marka>-<model>.jpg` kalıbında ve `cihazlar/<marka>/<model>.json` içindeki `gorsel` alanıyla birebir eşleşiyor. Hangi cihazın hangi dosyayı beklediği `cihazlar/BENIOKU.md` tablosunda yazıyor.

Burada kadraj hazırlığı gerekmiyor — üretici `odak` ile kendi kırpıyor. Dikey ya da kare, en az 1200 px genişlik yeterli.

## Pano sütun görseli

`pano` gönderisinde her sütunda bir ürün duruyor. Arka planı ben
temizliyorum (`arac/BENIOKU.md`), senin göndermen gereken sadece ham
fotoğraf.

**İyi kaynak:**
- Tek ürün, tek kare. Üç ürünü tek afişte değil, ayrı ayrı gönder.
- Sade zemin: beyaz, açık gri ya da düz renk. Tezgâh/atölye fonu da
  olur ama arka planda yazı, logo ya da başka ürün olmasın.
- En az 600 px genişlik. Küçük kare büyütünce bulanıklaşıyor,
  kullanamıyorum.
- Ürün kadrajın içinde tam dursun, kenarından kesilmiş olmasın.
- Üstünde "ŞİMDİ STOKTA", fiyat etiketi gibi yazı olmasın — kesince
  o yazı da geliyor.

**Olmaz:**
- Afiş/banner kırpıntısı (yazı ve diyagonal ayraçlar geliyor)
- Ekran görüntüsü (düşük çözünürlük)
- Birden çok ürünün aynı karede olduğu tanıtım görseli

**Dosya adı:** `gorsel/urun/<marka>-<model>.jpg`. Gönderirken sadece
hangisi olduğunu yaz, adlandırmayı ben yaparım.

## Fotoğrafı koymadan önce kontrol et

Gönderilen her görsel anlatılan ürünün kendisi olmayabilir. Arama sonuçlarında ve stok görsel sitelerinde benzer makineler dolaşıyor. **Makineyi tanımadan dosyayı klasöre koyma** — yanlış makineyi tanıtmak vektör çizimden daha kötü. Bu sette bir kare bu yüzden elendi: R1 gönderisi için gelen açık gövdeli diyot lazer karesi kullanılmadı.

## liste kapağı seti

Bir görsel defalarca kullanılıyor; her gönderiye ayrı görsel gerekmiyor. Bu sekizi kategorilerin tamamını karşılıyor:

| Dosya | Konu |
|---|---|
| `atolye.png` | Tezgâh üstü: yazıcı, el aletleri, ölçü aleti |
| `yazici.png` | Çalışan FDM yazıcı, yakın plan nozzle |
| `filament.png` | Raf dolusu makara, renkli |
| `lazer.png` | Lazer kesim tezgâhı, ahşap üstünde iz |
| `kart.png` | Breadboard, ESP32, jumper kablolar |
| `lehim.png` | Havya, duman, kart üstünde çalışma |
| `robot.png` | Paletli rover, saha zemini |
| `depo.png` | Kutular, raflar, düzenli stok |

Bunlarda konu sağ tarafta dursun, sol üçte biri boş kalsın — orası zemine eritiliyor.

Dosya adları sabit; değiştirirsen spec'teki `gorsel` alanını da değiştir.
