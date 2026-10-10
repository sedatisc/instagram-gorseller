# Otomasyon — ürün görselleri

Claude'un çalıştığı kutu `sermenkreatif.com`, `filamentdepom.com` ve
görsellerin durduğu `static.ticimax.cloud` adreslerine çıkamıyor; üçü de
403 veriyor (organizasyonun çıkış politikası). GitHub Actions koşucusunun
tam internet erişimi var. Bu yüzden görselleri koşucu indiriyor, depoya
işliyor; Claude depodan okuyor. **Elle fotoğraf göndermek gerekmiyor.**

## Çalıştırma

- **Elle:** GitHub → Actions → "Ürün görsellerini çek" → Run workflow.
  "Var olan görselleri de yeniden çek" kutusu işaretlenirse eldekiler de
  yenilenir.
- **Kendiliğinden:** her pazartesi 03.17 UTC.

Sonuç `otomasyon/SON-CALISMA.md` dosyasına ve iş özetine yazılıyor:
hangi ürün geldi, hangisi gelmedi, neden.

## Ürün ekleme

`otomasyon/urunler.json` içine bir satır:

```json
{ "slug": "sunlu-pla-plus-2", "ara": "SUNLU PLA+ 2.0" }
```

- **`ara`** — ürün adı. Betik site haritasından eşleştirip ürün sayfasını
  buluyor. Çoğu durumda bu yeterli.
- **`sayfa`** — tam adres. Ad eşleşmesi yanlış ürünü bulursa bunu ver.
- **`kes`** — varsayılan `true`. `false` dersen arka plan kesilmez.

Çıktı: ham kare `gorsel/urun/ham/<slug>.jpg`, kesilmiş `gorsel/urun/kesik-<slug>.png`.

## Neden Google görsel araması değil

Google'dan ada göre görsel çekmek kolay görünüyor ama iki sorunu var:

1. **Hangi ürün olduğu garanti değil.** Bu projede bir kere yaşandı:
   Bambu Lab R1 diye gelen kare açık gövdeli bir diyot lazerdi. Arama
   sonucunda benzer makineler karışıyor ve yanlış makineyi tanıtmak
   vektör çizimden kötü.
2. **Telif belirsiz.** Çıkan karenin kime ait olduğu ve ticari gönderide
   kullanılıp kullanılamayacağı bilinmiyor.

Site haritası eşleşmesi aynı kolaylığı veriyor — ürün adını yazıyorsun —
ama görsel satıcının kendi ürün sayfasından geliyor: doğru ürün, belli
kaynak.

## Elektronik tarafı

Raspberry Pi, Espressif ve PX4/Pixhawk görselleri bu iş akışına gerek
kalmadan alınıyor; üreticilerin dokümantasyon depoları GitHub'da ve
oradan doğrudan klonlanıyor. Ayrıntı ve lisans şartları
`gorsel/BENIOKU.md` içinde.
