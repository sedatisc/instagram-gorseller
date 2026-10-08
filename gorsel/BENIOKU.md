# Fotoğraflar

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

Fotoğrafı değiştirince gönderiyi yeniden üret:

```
python3 uret.py 2026-10-10-bambu-r1-tanitim/spec.json 2026-10-10-bambu-r1-tanitim
```

Uyarı satırı çıkmıyorsa bütün fotoğraflar yerine oturmuş demektir.

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
