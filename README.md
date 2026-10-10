# instagram-gorseller

@sermenkreatif Instagram hesabının içerik üretim hattı.

- `CALISMA.md` — otomatik oturumun izlediği talimat
- `PLAN.md` — 90 gönderilik konu listesi, saatler, hashtag sistemi, yazım kuralları
- `SEMA.md` — spec JSON şeması ve çizim öğeleri
- `uret.py` — slayt üreticisi
- `DURUM.json` — hangi konuların kullanıldığı
- `sira.py` — saat ızgarası, `YAYIN-LISTESI.md` üreticisi
- `otomasyon/yayinla.py` — Instagram'a otomatik yayın (kurulum:
  `otomasyon/YAYIN-KURULUM.md`)
- `otomasyon/cek.py` — satıcı sayfalarından ürün görseli çekici
- `ornek/` — örnek spec
- `fonts/`, `marka/` — yazı tipleri ve logo

Tarih klasörleri (`2026-09-29-voltaj-bolucu/`) gönderilerin slaytlarını
tutar: `1.jpg`, `2.jpg` … karusel sırası, `hikaye.jpg` hikaye,
`reels.mp4` video, `metin.md` açıklama ve ilk yorum, `spec.json` kaynak.

Çıktı **JPEG**: Instagram Graph API'si PNG kabul etmiyor. Reels'te sessiz
AAC ses yolu var, kap bunu şart koşuyor.
