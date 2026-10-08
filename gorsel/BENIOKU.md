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

## Bekleyen dosyalar

Üretici bunları arıyor, henüz klasörde yok:

| Dosya | Nerede kullanılıyor | Ne olmalı |
|---|---|---|
| `bambu-r1.jpg` | 2026-10-10-bambu-r1-tanitim · kapak + hikaye | R1'in tam gövdesi, kapağı kapalı, önden-yandan |
| `bambu-r1-is.jpg` | aynı gönderi · 2. kare | Kesilmiş/gravürlenmiş ahşap ya da akrilik iş, yakın plan |
| `ender-v3-mega.jpg` | 2026-10-11-ender-v3-mega-tanitim · kapak + hikaye | Yazıcının tam gövdesi, tabla görünür |
| `ender-v3-mega-is.jpg` | aynı gönderi · 2. kare | Tabladan çıkmış büyük parça ya da baskı anı |

Dosyayı klasöre koyup gönderiyi yeniden üret:

```
python3 uret.py 2026-10-10-bambu-r1-tanitim/spec.json 2026-10-10-bambu-r1-tanitim
```

Uyarı satırı kaybolduysa fotoğraf yerine oturmuş demektir.

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
