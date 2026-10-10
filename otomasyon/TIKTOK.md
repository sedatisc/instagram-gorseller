# TikTok — neden otomatik değil

Araştırıldı (10 Ekim 2026, kaynak yalnız developers.tiktok.com). Sonuç:
**TikTok'a otomatik yayın yapılamıyor.** Teknik bir eksiklik değil,
TikTok'un kendi kuralı. Hat kurmadım; kurup çalışmayacağını sonradan
görmek daha pahalı.

## Engel 1 — denetimden geçmeyen istemci yalnız gizli paylaşır

Content Posting API ile doğrudan paylaşım yapmak için uygulamanın
**audit**'ten geçmesi gerekiyor. Geçmeyen istemci için TikTok'un kendi
ifadesi: paylaşılan içerik gizli görünürlükle sınırlı (`SELF_ONLY`) ve
paylaşan hesabın da gizli olması gerekiyor. Hata kodu
`unaudited_client_can_only_post_to_private_accounts`. Yani denetimsiz hat
kurulabilir ama kimse göremez.

## Engel 2 — bizim kullanımımız denetim kurallarında açıkça yasak

TikTok'un İçerik Paylaşım Kılavuzu'nda kabul edilmeyenler arasında
birebir şu madde var: **"Sizin ya da ekibinizin yönettiği hesaplara
içerik yüklemeye yarayan bir araç."** Ayrıca istemcinin "geniş bir
kitleye yönelik olması, iç kullanımla sınırlı olmaması" isteniyor.
Bizim yapacağımız şey tam olarak yasaklanan madde.

Buna ek olarak denetim, her paylaşımda kullanıcıya gösterilmesi gereken
bir arayüz şart koşuyor: gizlilik seçimi açılır menüden **elle**
seçilecek (varsayılan değer olmayacak), yorum/düet/dikiş anahtarları
kapalı başlayacak, paylaş düğmesinin üstünde müzik kullanım onayı
yazacak, önizleme olacak. Bunların hepsi ekranın başında bir insan
olduğunu varsayıyor. Koşucuda çalışan bir betik bu şartları sağlayamaz.

## Engel 3 — görselin adresi bizim değil

`PULL_FROM_URL` ile video çektirmek için adresin alan adının **DNS
kaydıyla doğrulanmış** olması gerekiyor. Videolarımız
`raw.githubusercontent.com` üzerinde duruyor; o alan adı bizim değil,
doğrulayamayız (403 `url_ownership_unverified`). Bu engel aşılabilir —
dosyayı koşucudan `FILE_UPLOAD` ile yollamak ya da videoları
sermenkreatif.com üzerinden servis etmek yeter — ama ilk iki engel
durduğu sürece anlamı yok.

## Pratikte ne yapıyoruz

TikTok elle paylaşılıyor, ama elle iş en aza indirildi:

- Aynı reels videosu üç platformda da kullanılıyor (1080 × 1920, ~23 sn).
- Yayın Paketi sayfasında TikTok sekmesi var: videonun adresi ve
  TikTok'a göre kısaltılmış metin, kopyala düğmesiyle.
- Ses uygulamadan ekleniyor. TikTok'ta trend sesi hem kolay hem erişime
  yarıyor; API'nin ses kütüphanesine erişimi zaten yok, yani otomatik
  hat kurulsa bile bu adım elle kalacaktı.

## Başka rakamlar (gerektiğinde)

- Erişim anahtarı 24 saat, yenileme anahtarı 365 gün. Yenileme anahtarı
  her tazelemede değişebiliyor; otomatik hatta yeni değeri bir yere
  yazmak gerekiyor.
- Doğrudan paylaşım başlatma: dakikada 6 istek. Hesap başına günlük üst
  sınır yaklaşık 15 paylaşım.
- Video: MP4/WebM/MOV, H.264 önerilen, 23-60 FPS, 360-4096 piksel,
  en çok 4 GB, API üzerinden en fazla 10 dakika.
- Ses akışı zorunlu mu — TikTok belgelerinde geçmiyor, doğrulanmadı.

Kurallar değişirse yeniden bakılır; o zaman `FILE_UPLOAD` yolu ve
sermenkreatif.com üzerinden servis hazır seçenekler.
