# Cihaz tanıtımları

Creality, Bambu Lab, Anycubic, Prusa ve Snapmaker'ın güncel cihazları. 37 kayıt; her biri `cihazlar/<marka>/<model>.json` dosyasında, kaynak bağlantılarıyla birlikte duruyor.

Gönderi tek komutla çıkıyor:

```
python3 cihaz.py cihazlar/bambu-lab/x2d.json 2026-10-14-bambu-x2d
python3 uret.py 2026-10-14-bambu-x2d/spec.json 2026-10-14-bambu-x2d
python3 reels.py 2026-10-14-bambu-x2d/spec.json 2026-10-14-bambu-x2d/reels.mp4
```

`cihaz.py` kapağı, dört slaydı, kapanışı ve `metin.md`'yi kayıttan kuruyor. Zemin rengi model adından türetiliyor, aynı cihaz her seferinde aynı zemini alıyor.

## Kural

- **Her cihaz tanıtımı Reels ile birlikte yayınlanıyor.** Karusel + hikaye + Reels, üçü bir arada.
- Kapak gerçek ürün fotoğrafı istiyor. Fotoğraf yoksa kareye "FOTOĞRAF YOK" basılıyor; o kare yayınlanmıyor.
- Fotoğraflar `gorsel/cihaz/` klasöründe, aşağıdaki adlarla.
- Rakamların tamamı üretici beyanı olarak etiketleniyor; doğrulanamayan alanlar kapanış karesinde açıkça yazılıyor.
- Markalar dönüşümlü diziliyor, arka arkaya aynı marka çıkmıyor.

## Yayın sırası

| # | Marka | Model | Tip | Durum | TR | Fotoğraf |
|---|---|---|---|---|---|---|
| 1 | Anycubic | Kobra X | FDM | satista | stokta | `anycubic-kobra-x.jpg` |
| 2 | Bambu Lab | H2D | FDM | satista | teyit gerek | `bambu-lab-h2d.jpg` |
| 3 | Creality | K2 Plus Combo | FDM | satista | tükendi | `creality-k2-plus-combo.jpg` |
| 4 | Prusa | CORE One+ (Gen 2) | FDM | satista | tükendi | `prusa-core-one-plus-gen-2.jpg` |
| 5 | Snapmaker | U1 | FDM | satista | stokta | `snapmaker-u1.jpg` |
| 6 | Anycubic | Photon Mono M7 Pro | Reçine | satista | stokta | `anycubic-photon-mono-m7-pro.jpg` |
| 7 | Bambu Lab | X2D | FDM | satista | teyit gerek | `bambu-lab-x2d.jpg` |
| 8 | Creality | K3 | FDM | duyuruldu | teyit gerek | `creality-k3.jpg` |
| 9 | Prusa | MK4S | FDM | satista | tükendi | `prusa-mk4s.jpg` |
| 10 | Snapmaker | Artisan | Cok islevli | satista | teyit gerek | `snapmaker-artisan.jpg` |
| 11 | Anycubic | Kobra S1 Combo | FDM | satista | stokta | `anycubic-kobra-s1-combo.jpg` |
| 12 | Bambu Lab | A1 | FDM | satista | teyit gerek | `bambu-lab-a1.jpg` |
| 13 | Creality | K2 Pro Combo | FDM | satista | stokta | `creality-k2-pro-combo.jpg` |
| 14 | Prusa | CORE One L+ | FDM | satista | tükendi | `prusa-core-one-l-plus.jpg` |
| 15 | Snapmaker | Artisan Premium | Cok islevli | satista | teyit gerek | `snapmaker-artisan-premium.jpg` |
| 16 | Anycubic | Photon P1 | Reçine | satista | teyit gerek | `anycubic-photon-p1.jpg` |
| 17 | Bambu Lab | A2L | FDM | satista | teyit gerek | `bambu-lab-a2l.jpg` |
| 18 | Creality | Hi Combo | FDM | satista | stokta | `creality-hi-combo.jpg` |
| 19 | Prusa | XL+ | FDM | satista | tükendi | `prusa-xl-plus.jpg` |
| 20 | Snapmaker | 2.0 A350T | Cok islevli | satista | tükendi | `snapmaker-2-0-a350t.jpg` |
| 21 | Anycubic | Kobra 4 | FDM | satista | stokta | `anycubic-kobra-4.jpg` |
| 22 | Bambu Lab | P2S | FDM | satista | teyit gerek | `bambu-lab-p2s.jpg` |
| 23 | Creality | K1C | FDM | satista | tükendi | `creality-k1c.jpg` |
| 24 | Prusa | CORE One+ (Gen 2) INDX | FDM | satista | tükendi | `prusa-core-one-plus-gen-2-indx.jpg` |
| 25 | Snapmaker | J1s | FDM | satista | teyit gerek | `snapmaker-j1s.jpg` |
| 26 | Anycubic | Photon Mono M7 Max | Reçine | satista | teyit gerek | `anycubic-photon-mono-m7-max.jpg` |
| 27 | Bambu Lab | A1 mini | FDM | satista | teyit gerek | `bambu-lab-a1-mini.jpg` |
| 28 | Creality | HALOT-X1 | Reçine | satista | tükendi | `creality-halot-x1.jpg` |
| 29 | Prusa | MINI+ | FDM | satista | tükendi | `prusa-mini-plus.jpg` |
| 30 | Snapmaker | Ray 40W | Lazer | satista | teyit gerek | `snapmaker-ray-40w.jpg` |
| 31 | Anycubic | Kobra S1 Max | FDM | satista | tükendi | `anycubic-kobra-s1-max.jpg` |
| 32 | Bambu Lab | H2S | FDM | satista | teyit gerek | `bambu-lab-h2s.jpg` |
| 33 | Creality | HALOT-MAGE S | Reçine | satista | tükendi | `creality-halot-mage-s.jpg` |
| 34 | Prusa | SL1S Speed | Reçine | durduruldu | tükendi | `prusa-sl1s-speed.jpg` |
| 35 | Anycubic | Photon Mono 4 Ultra | Reçine | satista | tükendi | `anycubic-photon-mono-4-ultra.jpg` |
| 36 | Bambu Lab | H2C | FDM | satista | teyit gerek | `bambu-lab-h2c.jpg` |
| 37 | Creality | Ender-3 V3 KE | FDM | satista | tükendi | `creality-ender-3-v3-ke.jpg` |

## Fotoğraf çekim notu

Her cihaz için **bir** fotoğraf yeterli: makinenin tam gövdesi, üç çeyrek açı ya da önden. Kaynak üreticinin basın kiti ya da yetkili satıcının ürün sayfası olsun; arama sonucundan indirilen görsel kullanılmıyor.

Dosya `gorsel/cihaz/` içine yukarıdaki adla konuyor. Üretici kadrajı kendi ayarlıyor, hazırlık gerekmiyor — dikey ya da kare tercih edilir, en az 1200 px genişlik.

Fotoğrafı koymadan önce makinenin gerçekten o model olduğunu doğrula. Arama sonuçlarında benzer makineler dolaşıyor; yanlış makineyi tanıtmak vektör çizimden kötü.

## Veri hakkında

Araştırma 9 Ekim 2026'da yapıldı. Her kayıtta `kaynak` listesi ve `dogrulanmadi` alanı var. Üç şey özellikle not edilmeli:

- **Bambu Lab serisi yenilendi:** X1 Carbon ve X1E üretimden kalktı (Mart 2026), yerine X2D geldi. A1 yerine A2L, P1S yerine P2S. Eski model adlarını güncel diye yazma.
- **Prusa hız rakamı yayınlamıyor.** Hiçbir modeli için resmî maksimum baskı hızı veya ivme yok; gönderide hız sayısı verilmiyor.
- **Türk satıcı sayfalarında stok durumu güvenilir okunmuyor.** Çoğu sayfada "Sepete Ekle" ile "Tükendi" aynı anda görünüyor. "Stokta" demeden önce satıcıyı ara.
