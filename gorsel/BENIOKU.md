# Kapak görselleri

Bu klasöre konan görsel, `liste` kapağının sağ sütununu kaplıyor. Spec'e tek satır eklemek yeterli:

```json
"kapak": { "tip": "liste", "gorsel": "atolye.png", ... }
```

Görsel varsa çizim devre dışı kalıyor, yoksa izometrik kule çiziliyor. Başka bir şey yapmaya gerek yok.

## Üretirken

- **Ölçü:** dikey, en az 1200 × 1800 px. Kare ya da yatay görsel kırpılıyor.
- **Kompozisyon:** konu sağ tarafta dursun, sol üçte biri boş kalsın — orası zemine eritiliyor.
- **Zemin:** koyu ve sade. Kalabalık arka plan listenin okunmasını bozuyor.
- **Işık:** sol üstten. Kapaktaki çizimlerle aynı yön, yoksa yabancı duruyor.

## Üretilecek set

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

Dosya adları sabit; değiştirirsen spec'teki `gorsel` alanını da değiştir.
