# Gemini brief — ne yaptırıyoruz, ne yaptırmıyoruz

Üretilen görsel `gorsel/` altına atılıyor, `spec.json` içinde `kapak.gorsel`
ya da slaydın `foto` alanına yazılıyor; gerisini `uret.py` yapıyor.
Prompt kuralları ve ev stili `gorsel/GEMINI-PROMPT.md` dosyasında.

## Üç kutu

| Yaptırıyoruz | Yaptırmıyoruz | Koda yaptırıyoruz |
|---|---|---|
| Kavram sahnesi: ölçüm, aşınma, arıza, atölye ortamı | Sattığımız ürünün fotoğrafı | Başlık, rakam, tablo, rozet, fiyat |
| Boş iç mekân zemini (ürün sonradan oturtuluyor) | Kendi robot/proje fotoğraflarımız | Kampanya afişi, ürün kartı, rehber tablosu |
| Mevsim/atmosfer çerçevesi | İnsan yüzü, el dışında insan | Hikaye ve reels kareleri |

**Ürün fotoğrafı neden üretilmiyor:** müşteri eline geçeni fotoğrafla
karşılaştırıyor. Üretilmiş ürün fotoğrafı sahte ürün fotoğrafıdır.
1 Ağustos 2026'da yürürlüğe giren yönetmelik değişikliği de tüketicinin
kararını etkileyebilecek yapay zekâ kullanımının açıkça belirtilmesini
istiyor. Makine, filament, reçine, hotend → üreticinin kendi fotoğrafı.

**Kendi projelerimiz neden üretilmiyor:** tavan arası robotu, RC tank,
rover — bunlar "biz yaptık" diye paylaşılıyor. Üretilmiş fotoğrafla
paylaşılırsa iddia yalan olur. Bunların fotoğrafı tezgâhtan çekilecek.

**Yazı neden yok:** harf, rakam, logo, filigran istemiyoruz. Başlığı ve
rakamları `uret.py` basıyor; üretilen yazı hem bozuk çıkıyor hem bizimkiyle
çakışıyor. Her promptun sonunda "no text, no letters, no numbers, no logos"
duruyor.

---

## 1 · Kavram kapakları — sıradaki beş gönderi

Hepsi 4:5. Hikaye sürümü için `Aspect ratio 9:16` ve "negative space in the
upper 40%" yerine "the subject sits in the lower third; the upper half is
empty background".

### 15 Ekim · 3D tarayıcı ne işe yarar
`2026-10-15-3d-tarayici` → `gorsel/kavram/tarayici.jpg`

```
Photorealistic macro product photography, 100mm macro lens at f/5.6, single
large softbox at 45 degrees with a white fill card opposite, deep shadows.
Very dark background falling to near black at the edges.

Subject: a worn metal machine part — a bracket with bolt holes and casting
texture — sitting on a matte turntable, with a faint structured-light grid
pattern of thin blue lines projected across its surface, wrapping over the
contours. The lines bend where the surface bends. Brushed metal, fine dust in
the grooves, shallow depth of field, the lit face tack sharp.

Composition: part in the lower third, turntable edge cutting across, deliberate
negative space in the upper 40%.

Color grade: deep forest green background (#0A543C falling to #03201C), with
lime-green (#BEF264) rim light along the part's top edge.

Absolutely no text, no letters, no numbers, no logos, no watermarks, no screens
anywhere in the image. Aspect ratio 4:5.
```

Sahnenin fikri: tarayıcı yüzeyi okuyor. Izgara çizgilerinin yüzeyle birlikte
bükülmesi o fikrin kendisi.

### 18 Ekim · Sertleştirilmiş nozul ne zaman şart
`2026-10-18-sert-nozul` → `gorsel/kavram/asinmis-nozul.jpg`

```
Photorealistic extreme macro photography, 100mm macro lens at f/4, single large
softbox at 45 degrees, deep shadows. Very dark background falling to near black.

Subject: two brass nozzle tips lying side by side on a dark matte steel surface,
seen from a low three-quarter angle. The left one is clean with a crisp circular
orifice; the right one is visibly eroded — the orifice widened into an irregular
oval, the tip rounded and scarred, with a few dark carbon-fibre strands clinging
to it. Warm brass against cold steel, fine scratches catching the light. Shallow
depth of field, both tips sharp, the surface falling away soft.

Composition: the two tips in the lower third, side by side, deliberate negative
space in the upper 40%.

Color grade: near-black background, warm orange (#FB923C) rim light along the
brass edges and faint orange reflections in the steel.

Absolutely no text, no letters, no numbers, no part markings, no logos, no
watermarks anywhere in the image. Aspect ratio 4:5.
```

Sahnenin fikri: aşınma gözle görülüyor. İki ucu yan yana koymak gönderinin
tek cümlesi.

### 18 Ekim · Toplulukta sorulan arıza
`2026-10-18-toplulukta-ariza` → `gorsel/kavram/bozuk-baski.jpg`

```
Photorealistic macro product photography, 100mm macro lens at f/5.6, single
large softbox at 45 degrees, deep shadows. Very dark background falling to near
black at the edges.

Subject: a failed 3D print lying on a dark textured print bed — a tall thin
object whose upper half has collapsed into a tangled bird's nest of thin
extruded strands, the lower half still clean with even layer lines. The break
between the good part and the failure is clearly visible. Matte grey plastic,
fine stringing between the strands, shallow depth of field, the transition zone
tack sharp.

Composition: the part in the lower third lying diagonally, deliberate negative
space in the upper 40%.

Color grade: deep forest green background (#0A543C falling to #03201C), with
lime-green (#BEF264) rim light along the top of the part.

Absolutely no text, no letters, no numbers, no logos, no watermarks anywhere in
the image. Aspect ratio 4:5.
```

Sahnenin fikri: alt yarısı düzgün, üst yarısı çöpe gitmiş. Arızanın nerede
başladığı tek bakışta görülüyor.

### Atölye ortamı — yedekte dursun
`gorsel/kavram/atolye-gece.jpg` · kurumsal ve hizmet gönderileri için

```
Photorealistic interior photography, 35mm lens at f/2.8, available light.
A small workshop bench at night: three enclosed 3D printers of no identifiable
brand running side by side on a steel rack, their chamber lights glowing warm
through the glass doors, casting light pools on a concrete floor. Spools of
filament stacked on a shelf behind, out of focus. Cables routed neatly along
the rack. No people. Deep shadows, warm interior light against cool darkness.

Composition: the rack in the lower two thirds, deliberate negative space in the
upper 40% where the ceiling falls into darkness.

Color grade: near-black background, warm orange (#FB923C) light from the
chambers, cool blue-grey fill from a window out of frame.

Absolutely no text, no letters, no numbers, no brand logos, no screens with
visible content, no watermarks anywhere in the image. Aspect ratio 4:5.
```

Dikkat: makineler **markasız** istensin. Tanınır bir makine çizdirip
"bizim atölye" demek olmaz.

### Mevsim çerçevesi — ekim sonu
`gorsel/kavram/sonbahar-zemin.jpg` · hediyelik ve mumluk gönderilerinin zemini

```
Photorealistic still life background plate, 50mm lens at f/4, soft window light
from the left. An empty light oak table surface seen from a low three-quarter
angle, with a few dry autumn leaves and two small pumpkins pushed to the far
left and the back right corner, leaving the entire centre of the table empty
and unobstructed. Soft shadows, warm late afternoon light, shallow depth of
field falling off behind the table.

Composition: the centre and lower middle of the frame must stay completely
empty — a product will be composited there later.

Color grade: warm neutral, cream and amber, no heavy colour cast.

Absolutely no text, no letters, no numbers, no logos, no watermarks, no products
of any kind anywhere in the image. Aspect ratio 4:5.
```

Bu kareye ürün **sonradan** oturtuluyor: `gorsel/urun/kesik/` altındaki gerçek
kesilmiş ürün fotoğrafı üstüne biniyor. Böylece sahne üretilmiş, ürün gerçek
oluyor. Zeminin ortası boş kalmalı, yoksa ürün bir şeyin üstüne oturuyor.

---

## 2 · Kampanya afişi — koda yaptırılıyor

Gösterdiğin bayi afişi düzeni (üstte bağıran başlık, üç renkli kategori
paneli, altta büyük teklif şeridi, en altta güven şeridi) `arac/kampanya.py`
ile çıkıyor. Gemini'ye gerek yok; metin ve fiyat yazısının birebir doğru
olması gerekiyor, üretilen görselde harf bozuluyor.

```
python3 arac/kampanya.py <spec.json> <cikti.jpg> [<hikaye.jpg>]
```

spec alanları:

| Alan | Ne yazıyor |
|---|---|
| `baslik` | İki satır, büyük punto. İkincisi vurgu renginde. |
| `alt` | Tek cümle açıklama |
| `paneller` | Üç kategori: `ad`, `renk`, `gorsel`, üç `maddeler` satırı |
| `teklif` | Ortadaki büyük şerit — kampanya cümlesi buraya |
| `guven` | Alt şeritte dört kısa ibare |

Panel fotoğrafları `gorsel/urun/ham/` altındaki gerçek ürün fotoğrafından
geliyor, arka planı otomatik kesiliyor.

**Teklif şeridine yazılacak cümle sende.** Gerçekten uygulanacak bir kampanya
değilse o şeridi boş bırak (`"teklif": ""`), afiş kategori tanıtımı olarak
çalışır. İndirim yazacaksan indirimden önceki en düşük fiyatın gösterilmesi
gerekiyor — o bilgi afişte yoksa indirim ibaresi yazılmıyor.

---

## 3 · Üretilen görsel geldikten sonra

1. Dosyayı `gorsel/kavram/` altına koy, adı promptun yanındaki ad olsun.
2. İlgili `spec.json` içinde `kapak.gorsel` ya da slaydın `foto` alanına yaz.
3. `python3 uret.py <klasör>/spec.json <klasör>`
4. Kareye bak. Ürün kesiliyorsa `uret.py` artık kendisi sığdırıyor, ama
   kadraj yanlışsa `odak` değeriyle oynanıyor: 0.0 üst, 0.5 orta, 1.0 alt.
