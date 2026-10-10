# youtube/

YouTube'un kendi yapısı. Instagram kuyruğundan ayrı duruyor; ortak olan
tek şey video dosyası.

| Dosya | Ne |
|---|---|
| `DURUM.json` | Kuyruk: hangi gün hangi video, başlık, kanca, maddeler, etiketler |
| `PLAN.md` | Başlık ve açıklama kuralları, sıradaki konular |

Hat ve kurulum `otomasyon/` altında:

- `otomasyon/youtube.py` — bu kuyruğu okuyup Shorts olarak yüklüyor
- `otomasyon/YOUTUBE-KURULUM.md` — bir defalık Google kurulumu
- `.github/workflows/youtube.yml` — 20 dakikada bir bakıyor

## Akış

1. Gönderi klasöründe `spec.json` ve `reels.mp4` zaten var (Instagram
   hattından çıkıyor, video 1080 × 1920 ve ~23 sn).
2. `youtube/DURUM.json` kuyruğuna tarih, klasör, başlık, kanca, maddeler
   ve etiketler yazılıyor — metin YouTube'a göre, Instagram metninin
   kopyası değil.
3. `python3 paket.py` çalıştırılıyor; Yayın Paketi sayfasının YouTube
   sekmesi yenileniyor.
4. Saat gelince `otomasyon/youtube.py` videoyu yüklüyor, yüklenenler
   `otomasyon/yayinlanan-youtube.json` defterine yazılıyor.

Denemek için yükleme yapmadan:

```
python3 otomasyon/youtube.py --kuru
python3 otomasyon/youtube.py --kuru --zorla 2026-10-12
```
