# Motion brief

Video üretimi bu sayfaya göre yapılıyor. Yeni bir video istenince bu sayfa
başa yapıştırılıyor, en alta tek satır sahne yazılıyor. Tarif burada
bitiyor; `reels.py` ve `shorts.py` bunu uyguluyor.

Rakamlar uydurma değil, kodda duran değerlerin kendisi. Biri değişirse
burası da değişiyor.

---

Bana bir video yap. Bu brief'e birebir uy:

| | |
|---|---|
| **ÇITA** | Telefonda sesi kapalı, ilk saniyede ne anlattığı anlaşılacak. Anlaşılmıyorsa bitmemiştir. |
| **ÖLÇÜ** | 1080 × 1920, 30 kare/sn, H.264 + AAC. Shorts 10-13 sn, reels ~23 sn. Son kare ilk kareyle aynı değil; son kare abone kartı. |
| **TEK KURAL** | Her sahnede **tek** bir şey büyük: ya bir rakam ya bir cümle. İkisi birden büyük olursa ikisi de kaybolur. |
| **IZGARA** | Kesimler 96 BPM'de, vuruş 0,625 sn. Kanca 5 vuruş, her madde 3, kapanış 3. Kesim sese denk gelecek. |
| **ÜRÜN** | Arka planı kesilmiş, kadrajın içinde **bütün**. Kenardan 36 piksel içeri sabit. Hiçbir karede kırpılmayacak — kırpılmışsa o video çıkmaz. |
| **GÖRÜNÜM** | Koyu zemin, arkadan kategori renginde ışık, altında yumuşak gölge. Beyaz kutu yok, çerçeve yok, yuvarlak köşeli kart yok. |
| **YAZI** | Başlık ve rakam Anton, 150-300 punto. Destek satırı Poppins SemiBold 40-62. Sayaç JetBrains Mono 36. Metnin tamamı sığacak; punto küçülür, satır düşmez. |
| **RAKAM** | Rakam cümleden ayrılıp ekranı dolduruyor ve sıfırdan yukarı sayıyor. Model adındaki rakam ayrılmaz (R1, S2, i8). |
| **HAREKET** | Her kesimde ölçek 1,08'e taşıp yerine oturuyor. Ürün 0,955'ten 1,0'a nefes alıyor — büyüterek değil küçülterek, yoksa kadrajı aşıyor. Yazı 0,2 sn'de giriyor. |
| **SES** | Kendi ürettiğimiz ritim, kurguyla aynı tempoda. Başkasının parçası yok, kütüphane müziği yok. |
| **ASLA** | Stok durumu. Sevkiyat tarihi. Doğrulanmamış rakam. Üretilmiş ürün fotoğrafı. Boş kalan alt yarı. Python'un `.upper()`'ı — Türkçede "kesmiyor" → "KESMİYOR". |
| **SAHNE** | *(tek satır, aşağıya)* |

---

## Sahne satırı nasıl yazılıyor

Tek cümle, ürün ve asıl fikir. Örnekler:

- `Bambu Lab R1 lazer — ne kesiyor, ne kesmiyor`
- `Sunlu FilaDryer S2, S4 ve E2 arasındaki fark`
- `Purge atmadan çok renk: Snapmaker U1 ve Creality K3`

Metin `youtube/DURUM.json` içindeki `baslik`, `kanca` ve `satirlar`
alanlarından geliyor. `satirlar` aynı anda ekrandaki vuruşlar: rakamla
başlayan satır daha iyi iş çıkarıyor, çünkü ekranda dev rakam oluyor.

## Neden bu brief başkasınınkinden farklı

Bu sayfanın şekli dolaşan bir "motion brief" şablonundan alındı, değerleri
alınmadı. Oradaki brief parlak zemin, 1080 × 960 ve 6 saniye istiyor; o
format sunum ekranı için. Bizimki telefonda dikey akışta, koyu zeminde ve
ürün fotoğrafıyla çalışıyor:

| | Şablon | Biz |
|---|---|---|
| Zemin | Parlak, koyu zemin yasak | Koyu — markanın kendisi |
| Ölçü | 1080 × 960, 6 sn | 1080 × 1920, 10-23 sn |
| Kahraman | Tek soyut nesne | Gerçek ürün fotoğrafı, kesilmiş |
| Son kare | İlk kareyle aynı | Abone kartı |
| Ölçüt | "Apple keynote'ta durur mu" | "Sesi kapalı, ilk saniyede anlaşılıyor mu" |

Ortak olan tek şey işe yarayan kısım: tarifin tek sayfada, kesin ve
tartışmasız durması.
