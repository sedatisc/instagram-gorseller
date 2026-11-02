# Buffer ile ücretsiz otomatik yayın — bir defalık kurulum

Facebook geliştirici hesabı gerekmiyor. Buffer ücretsiz planı: 3 kanal,
kanal başına aynı anda 10 bekleyen paylaşım, API anahtarı dahil.
Her gece 00.30'da `buffer.yml` o günün paylaşımlarını Buffer'a saatleriyle
gönderiyor, Buffer vakti gelince Instagram'a yayınlıyor.

## 1. Buffer hesabı
buffer.com → **Get started for free** → e-posta ile kayıt.

## 2. Instagram'ı bağla
Buffer → **Channels → Connect a channel → Instagram**.
@sermenkreatif ile giriş yap. Hesap işletme hesabı olduğu için paylaşımlar
otomatik yayınlanır.

## 3. API anahtarı
Buffer → **Settings → API** → anahtar oluştur ve kopyala.

## 4. GitHub'a yaz
github.com/sedatisc/instagram-gorseller → **Settings → Secrets and variables
→ Actions → New repository secret**

| İsim | Değer |
|---|---|
| `BUFFER_TOKEN` | 3. adımdaki anahtar |

Anahtar yalnız bu alanda dursun; sohbete ya da dosyaya yazılmasın.

## Ücretsiz planın sınırları
- İlk yorum ücretli özellik: ilk yorum metni gönderi metninin sonuna ekleniyor.
- Gönderi başına en çok 5 hashtag: fazlası kırpılıyor.
- Günde en çok 10 paylaşım planlanabiliyor: fazlası olursa önce kampanya
  hikayesi düşüyor.
