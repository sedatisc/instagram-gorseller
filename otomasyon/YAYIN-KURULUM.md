# Otomatik yayın — bir defalık kurulum

Yayın hattı hazır (`otomasyon/yayinla.py` + `.github/workflows/yayin.yml`).
Eksik olan tek şey iki anahtar: **IG_USER_ID** ve **IG_TOKEN**. Bunlar
hesabın kendi erişim bilgileri, benim üretemeyeceğim tek parça. Aşağıdaki
adımlar bir kez yapılıyor, sonra anahtar süresiz çalışıyor.

Ön koşul: `@sermenkreatif` **işletme hesabı** olacak ve bir **Facebook
sayfasına bağlı** olacak. İkisi de var.

## 1. Uygulama aç

developers.facebook.com → **My Apps** → **Create App**
→ tür: **Business** → ad: `sermenkreatif yayin`.

Sonra uygulamanın panelinde **Add Product** → **Instagram** ekle.

Buradaki uygulama yalnız kendi hesabına yazacağı için **App Review
gerekmiyor** — Standard Access kendi varlıklarını kapsıyor.

## 2. Kısa ömürlü anahtar al

Uygulama panelinde **Tools → Graph API Explorer**:

- Sağ üstte uygulamayı seç
- **User or Page**: `User Token`
- **Add a Permission** ile şunları işaretle:
  `instagram_basic`, `instagram_content_publish`, `pages_show_list`,
  `pages_read_engagement`, `instagram_manage_comments`
- **Generate Access Token** → Facebook izin ekranında sayfayı seç

Çıkan anahtar 1–2 saatlik. Bir sonraki adımda kalıcıya çeviriyoruz.

## 3. Uzun ömürlüye çevir

Tarayıcıda (App ID ve App Secret, panelde **Settings → Basic** altında):

```
https://graph.facebook.com/v23.0/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id=APP_ID
  &client_secret=APP_SECRET
  &fb_exchange_token=2._ADIMDAKI_ANAHTAR
```

Dönen `access_token` 60 günlük **kullanıcı** anahtarı.

## 4. Sayfa anahtarını al — bu süresiz

```
https://graph.facebook.com/v23.0/me/accounts?access_token=3._ADIMDAKI_ANAHTAR
```

Listede `@sermenkreatif`in bağlı olduğu sayfayı bul, onun `access_token`
alanını al. **Sayfa anahtarının süresi dolmuyor** — 60 günde bir
yenileme derdi yok. `id` alanını da not et, bir sonraki adımda gerekiyor.

## 5. Instagram hesap kimliğini al

```
https://graph.facebook.com/v23.0/SAYFA_ID
  ?fields=instagram_business_account&access_token=SAYFA_ANAHTARI
```

Dönen `instagram_business_account.id` → **IG_USER_ID**.

## 6. Depoya yaz

github.com/sedatisc/instagram-gorseller → **Settings** →
**Secrets and variables** → **Actions** → **New repository secret**:

| İsim | Değer |
|---|---|
| `IG_USER_ID` | 5. adımdaki kimlik |
| `IG_TOKEN` | 4. adımdaki sayfa anahtarı |

Anahtarı buraya, sohbete ya da herhangi bir dosyaya yazma — secret
alanı dışında hiçbir yerde durmasın.

## 7. Dene

Depoda **Actions** → **Instagram yayını** → **Run workflow**:

1. Önce `kuru` **açık** çalıştır. Hiçbir şey yayınlanmaz; iş özetinde
   hangi işi hangi adresle yayınlayacağını görürsün.
2. Sonra `kuru` **kapalı** + `zorla` alanına tek bir iş yaz, ör.
   `2026-10-11|3dbaski|gonderi`. Tek gönderi gider, hesaba bak.
3. Doğruysa bir şey yapma — cron zaten 20 dakikada bir bakıyor ve
   ızgaradaki saati gelen her işi kendi yayınlıyor.

## Nasıl çalışıyor

- Kuyruk `DURUM.json`, saatler `sira.py` içindeki ızgara.
- Her çalışmada "vakti gelmiş ve `otomasyon/yayinlanan.json` defterinde
  olmayan" işler yayınlanıyor. Defter her yayından sonra depoya işleniyor,
  aynı gönderi iki kez gitmiyor.
- Görseller depodan servis ediliyor
  (`raw.githubusercontent.com/...`), Graph API herkese açık adres
  istediği için ayrı barındırma gerekmiyor.
- Kota: Meta 24 saatte ~50 yayın veriyor, bizim yükümüz günde 9.
  Her çalışmada kota okunuyor, doluysa atlanıyor.
- Cron 5–30 dakika kayabiliyor. `yayinla.py` vakti 3 saatten fazla
  geçmiş işi yayınlamıyor — akşam sabahın gönderisi düşmesin.

## Reels takılırsa

Görseller `raw.githubusercontent` üzerinden `image/jpeg` olarak gidiyor,
sorun çıkarmıyor. Video aynı yerden `application/octet-stream` olarak
geliyor; Meta kabı bunu reddederse `MEDYA_KOK` secret'ı eklenip başka bir
kök adres (CDN ya da release varlığı) verilebilir, kod değişmiyor. Hata
iş özetinde `kap ... ERROR` satırı olarak görünür.

## Elle kalan işler

API bunları yapmıyor, uygulamadan yapılacak:

- **Hikaye etiketleri** — anket, link, geri sayım, soru kutusu. API
  hikayeyi düz kare olarak atıyor, etiket koyamıyor.
- **Reels'e trend sesi** — API'nin ses kütüphanesine erişimi yok. Video
  sessiz AAC yoluyla gidiyor; sesi uygulamadan eklemek istersen reels'i
  elle paylaş.
- **İlk yorum** — `instagram_manage_comments` izni verilmişse betik
  kendi yazıyor, izin yoksa sessizce geçiyor ve `metin.md` içindeki
  metni elle yapıştırmak gerekiyor.
