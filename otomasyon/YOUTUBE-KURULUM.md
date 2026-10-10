# YouTube Shorts — bir defalık kurulum

Hat hazır (`otomasyon/youtube.py` + `.github/workflows/youtube.yml`).
Eksik olan üç anahtar: **YT_CLIENT_ID**, **YT_CLIENT_SECRET**,
**YT_REFRESH_TOKEN**. Kanalın erişim bilgileri olduğu için bunları ancak
sen üretebilirsin.

Dikey ve 3 dakikanın altındaki video YouTube tarafından **kendiliğinden
Short sayılıyor** — ayrı bir alan, etiket ya da `#Shorts` yazmak
gerekmiyor. Bizim reels videoları 1080 × 1920 ve ~23 saniye, yani doğrudan
Short olarak çıkıyor.

## 1. Google Cloud projesi aç ve API'yi etkinleştir

console.cloud.google.com → yeni proje (`sermenkreatif yayin`)
→ **APIs & Services → Library** → **YouTube Data API v3** → **Enable**.

## 2. OAuth izin ekranı

**APIs & Services → OAuth consent screen**

- User type: **External**
- Uygulama adı, destek e-postası, geliştirici e-postası: kendi adresin
- Scopes: `https://www.googleapis.com/auth/youtube.upload` ve
  `https://www.googleapis.com/auth/youtube.force-ssl`
  (ikincisi ilk yorumu betiğin yazabilmesi için)
- Test users: kendi Google hesabın

**Sonra mutlaka "PUBLISH APP" ile yayın durumunu "In production" yap.**
Bu adım atlanırsa Google yenileme anahtarını **7 günde bir geçersiz
kılıyor** ve hat her hafta duruyor. Kendi kanalına yükleme yaptığın için
doğrulama (verification) istemesi beklenmiyor; isterse ekranda yazdığı
adımları izle.

## 3. OAuth istemcisi oluştur

**Credentials → Create credentials → OAuth client ID**
→ Application type: **Desktop app** → ad: `yayin-botu`.

Çıkan **Client ID** ve **Client secret** 1. ve 2. anahtar.

## 4. Yenileme anahtarını al

Tarayıcıda şu adresi aç (CLIENT_ID'yi kendi değerinle değiştir):

```
https://accounts.google.com/o/oauth2/v2/auth
  ?client_id=CLIENT_ID
  &redirect_uri=http://127.0.0.1:8080
  &response_type=code
  &access_type=offline
  &prompt=consent
  &scope=https://www.googleapis.com/auth/youtube.upload%20https://www.googleapis.com/auth/youtube.force-ssl
```

Kanalın hesabıyla onayla. Tarayıcı `127.0.0.1:8080/?code=...` adresine
düşüp hata verecek — **adres çubuğundaki `code=` değerini kopyala**
(sayfanın açılmaması normal).

Sonra o kodu anahtara çevir (terminalde):

```
curl -s -X POST https://oauth2.googleapis.com/token \
  -d client_id=CLIENT_ID \
  -d client_secret=CLIENT_SECRET \
  -d code=KOPYALADIGIN_KOD \
  -d grant_type=authorization_code \
  -d redirect_uri=http://127.0.0.1:8080
```

Dönen JSON'daki **`refresh_token`** 3. anahtar. Kod tek kullanımlık;
hata alırsan 4. adımı baştan yap.

## 5. Depoya yaz

github.com/sedatisc/instagram-gorseller → **Settings** →
**Secrets and variables** → **Actions**:

| İsim | Değer |
|---|---|
| `YT_CLIENT_ID` | 3. adımdaki Client ID |
| `YT_CLIENT_SECRET` | 3. adımdaki Client secret |
| `YT_REFRESH_TOKEN` | 4. adımdaki refresh_token |

Anahtarları sohbete ya da dosyaya yazma, yalnız secret alanına.

## 6. Dene

**Actions → YouTube Shorts → Run workflow**:

1. Önce `kuru` **açık**: hiçbir şey yüklenmez, iş özetinde hangi videoyu
   hangi başlık ve açıklamayla yükleyeceğini görürsün.
2. Sonra `kuru` **kapalı** + `zorla` alanına tek bir tarih, ör.
   `2026-10-12`. Tek video gider, kanala bak.
3. Doğruysa bir şey yapma; cron 20 dakikada bir bakıyor ve ızgaradaki
   reels saati gelen videoyu kendi yüklüyor.

## Nasıl çalışıyor

- Kuyruk `DURUM.json`, saatler `sira.py`. Instagram hattıyla aynı kaynak.
- Başlık kapak manşetinden, açıklama `metin.md`'den, etiketler metindeki
  `#` etiketlerinden üretiliyor. Kategori: Science & Technology.
- Yüklenenler `otomasyon/yayinlanan-youtube.json` defterine yazılıyor,
  aynı video iki kez gitmiyor.
- Kota: `videos.insert` kendi kovasında **günde 100 çağrı**; bizim yükümüz
  günde 1. (Google'ın kota sayfasının üst özeti hâlâ eski 1600 birimlik
  rakamı yazıyor, tablosu ve madde metni 100 çağrı diyor — Cloud
  konsolundaki Quotas ekranından teyit edebilirsin.)
- `selfDeclaredMadeForKids: false` gönderiliyor; bu alan boş bırakılamıyor.

## Elle kalan

- **Küçük resim (thumbnail).** Short'larda akışta videonun karesi
  kullanılıyor, ayrı küçük resim şart değil.
- **Oynatma listesi.** İstersen sonradan ekleriz, `playlistItems.insert`
  ile oluyor.
- **Ses.** Videolar sessiz AAC yoluyla gidiyor. YouTube kabul ediyor ama
  sessiz Short zayıf iş yapıyor; sesli versiyon istersen ayrıca konuşalım.
