# Kanal kurulumu

**Kanal:** Sermen Kreatif Teknolojileri
**Kimlik:** `UCEwu_2EOMmS5AuRRulxVnag`
**Kullanıcı adı:** @SermenKreatifTeknolojileri
**Adres:** https://www.youtube.com/channel/UCEwu_2EOMmS5AuRRulxVnag

Görseller `youtube/gorsel/` altında, `arac/youtube_kanal.py` üretiyor.
Metinler aşağıda olduğu gibi yapıştırılacak.

| Dosya | Nereye | Ölçü |
|---|---|---|
| `banner.png` | Kanalı özelleştir → Marka → Banner | 2048 × 1152 |
| `profil.png` | Marka → Profil fotoğrafı | 800 × 800 |
| `filigran.png` | Marka → Video filigranı | 150 × 150 |

Banner'da yazı ve logo ortadaki 1235 × 338'lik alanda; televizyonda
kenarlar kırpılıyor, telefonda yalnız o alan görünüyor.

## Hangisini ben yapabiliyorum

Anahtarlar depoya girdikten sonra API ile **ben** yapabiliyorum:

| İş | Uç | Kota |
|---|---|---|
| Hakkında metni | `channels.update` → `brandingSettings.channel.description` | 50 |
| Anahtar kelimeler | `channels.update` → `brandingSettings.channel.keywords` | 50 |
| Banner | `channelBanners.insert` sonra `channels.update` → `bannerExternalUrl` | 50 + 50 |

**Elle yapılacaklar — API'de yok:**

- **Kanal adı.** `channels.update` adı değiştirmeyi reddediyor
  (`channelTitleUpdateForbidden`); YouTube Studio'dan değişiyor.
- **Kullanıcı adı (@handle).** API'de yok.
- **Profil fotoğrafı.** API'de yok.
- **Oynatma listeleri ve bölümler.** API'de var ama elle yapmak daha hızlı.

## Künye

**Kanal adı:** "Sermen Kreatif Teknolojileri" duruyor. Önerim
**"Sermen Kreatif"** — mağaza ve Instagram'la aynı, videoda söylerken
kısa. Ar-Ge/yazılım tarafı için yeni bir firma adı arıyorsun; o iş
netleşince ayrı kanal açılır, bu kanal mağazanın kanalı olarak kalır.

**Kullanıcı adı:** @SermenKreatifTeknolojileri uzun. Boşsa
**@sermenkreatif** alınsın — Instagram'la aynı olması hem akılda kalıyor
hem videoda "sermenkreatif" demek yetiyor. YouTube kullanıcı adı
değişikliğinde sınır koyuyor, bir kerede doğrusunu al.

**Hakkında** (Kanalı özelleştir → Temel bilgiler → Açıklama):

```
3D baskı, filament ve elektronik tarafında işe yarayan kısa videolar.

Burada her rakam üreticinin kendi sayfasından geliyor: baskı alanı, hız,
sıcaklık, akım. Tahmin, "bence" ve kulaktan dolma yok; bir bilgi
doğrulanamıyorsa videoda "açıklanmadı" diye geçiyor.

Ne bulursun:
· Makine karşılaştırmaları — hangisi hangi işe, nerede yetmiyor
· Filament rehberleri — hangi seri kaç derecede, neyi basar
· Elektronik — kart seçimi, besleme, sensör, arıza çözme
· Atölyeden işler ve bozulan baskıların sebebi

Her gün yeni bir Short. Ürünler: sermenkreatif.com
```

**Kanal anahtar kelimeleri** (Ayarlar → Kanal → Temel bilgiler):

```
3d baskı, 3d yazıcı, filament, pla, petg, abs, tpu, creality, bambu lab,
sunlu, polymaker, elektronik, esp32, raspberry pi, arduino, maker,
türkçe 3d baskı, 3d baskı türkiye
```

**Ülke:** Türkiye · **Dil:** Türkçe

**Bağlantılar** (Temel bilgiler → Bağlantılar):
1. sermenkreatif.com — Mağaza
2. instagram.com/sermenkreatif — Instagram

İlk bağlantı banner'ın üstünde görünüyor; mağaza ilk sırada olsun.

## Yükleme varsayılanları

Ayarlar → Yükleme varsayılanları. Betik de aynısını gönderiyor; elle
yüklediğin videoda da aynı olsun diye buraya yazılıyor:

| Alan | Değer |
|---|---|
| Kategori | Bilim ve Teknoloji |
| Dil | Türkçe |
| Çocuklara yönelik | Hayır |
| Yorumlar | Açık, uygunsuz olanları beklet |
| Lisans | Standart YouTube lisansı |
| Görünürlük | Herkese açık |

## Oynatma listeleri

Shorts tek tek izleniyor ama oynatma listesi aramada ve kanal sayfasında
işe yarıyor. Beşi yeter:

| Liste | Ne girer |
|---|---|
| Hangisini almalı? | Makine ve ekipman karşılaştırmaları |
| Filament rehberi | PLA, PETG, ABS, TPU, kurutma, seri farkları |
| Elektronik ve IoT | Kart seçimi, besleme, sensör, arıza |
| Baskı sorunları | Stringing, warping, ölçü tutmaması, tıkanma |
| Atölyeden | Kendi projeleri ve üretim işleri |

Açıklamaları tek cümle, aramada çıkan kısım orası.

## Kanal bölümleri (ana sayfa sırası)

1. Öne çıkan video (fragman)
2. Shorts
3. Hangisini almalı?
4. Filament rehberi
5. Elektronik ve IoT
6. Baskı sorunları
7. Atölyeden

## Kanal fragmanı

30 saniye, kanalı ilk kez görene "burada ne var" diyen video. Üretim
hattımızdan çıkabilir; senaryo:

| Saniye | Ekranda | Söylenen (altyazı) |
|---|---|---|
| 0-4 | Bozuk baskı yakın plan | "Baskı bozuk çıkıyor ve sebebi ayar değil." |
| 4-10 | Nozul / filament kartları | "Burada her rakam üreticinin kendi sayfasından." |
| 10-18 | Makine karşılaştırma panosu | "Hangi makine hangi işe yetiyor, nerede yetmiyor." |
| 18-24 | Elektronik kart panosu | "Kart seçimi, besleme, arıza çözme." |
| 24-30 | Logo + abone işareti | "Her gün yeni bir Short. Abone ol." |

Fragman henüz üretilmedi; kanal açılıp görseller yerine konduktan sonra
yapılacak.

## Uzun video meselesi

Şu an üretebildiğimiz şey Shorts: 1080 × 1920, ~23 saniye, sessiz. Uzun
video (5-10 dakika) için ya kamera karşısına geçmek ya da seslendirme
gerekiyor — ikisi de elle iş. Kanalı Shorts'la açmak doğru; uzun videoya
geçilecekse ayrı karar.

Şu anki videolar **sessiz**. YouTube kabul ediyor ama sessiz Short zayıf
iş yapıyor. Seçenekler: (a) böyle devam, (b) YouTube'un kendi ses
kütüphanesinden müzik eklemek (elle, yükleme sonrası), (c) seslendirme.

## Sıra

1. **Sende:** kanal adını kısalt, kullanıcı adını al, profil fotoğrafını
   yükle (`youtube/gorsel/profil.png`).
2. **Sende:** yükleme varsayılanlarını ayarla, beş oynatma listesini aç.
3. **Sende:** `otomasyon/YOUTUBE-KURULUM.md` adımlarıyla üç anahtarı
   depoya koy.
4. **Bende:** anahtarlar girince hakkında metnini, anahtar kelimeleri ve
   banner'ı API ile yazarım; günün videosu da 18:20'de kendiliğinden
   yüklenmeye başlar.
5. **Bende:** ilk hafta dolunca fragmanı üretirim, sen öne çıkan video
   yaparsın.
