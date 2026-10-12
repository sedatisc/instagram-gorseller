# Gemini görsel promptları

Üretilen görsel `gorsel/` altına atılıyor, `spec.json` içinde `kapak.gorsel`
ya da kartın `gorsel` alanına yazılıyor, `uret.py` gerisini yapıyor.

## Kurallar

- **Yazı yok.** Harf, rakam, logo, filigran istemiyoruz — başlığı, rakamları
  ve rozetleri `uret.py` kendisi basıyor. Üretilen yazı hem bozuk çıkıyor
  hem de bizim yazımızla çakışıyor.
- **Üst %40 boş kalacak.** Başlık oraya geliyor. Prompt'ta "negative space
  in the upper 40%" diye geçiyor.
- **Sattığımız ürünün fotoğrafı üretilmiyor.** Makine, filament, hotend,
  kart — bunların görseli üreticinin kendi fotoğrafı olacak
  (`otomasyon/cek.py` siteden çekiyor). Üretilmiş ürün fotoğrafı sahte ürün
  fotoğrafıdır; bir müşteri eline geçeni fotoğrafla karşılaştırır.
  Üretilen görsel yalnız **kavram** gönderilerinde: ölçüm, arıza, yöntem,
  atölye ortamı.
- **Ölçü.** Gönderi 4:5, hikaye 9:16, reels karesi 9:16.
- **İngilizce yazılıyor.** Aynı tarifi Türkçe verince sonuç belirgin
  biçimde zayıflıyor.
- Prompt İngilizce olsa da sahnede **yazılı hiçbir şey** olmayacak; yabancı
  dilde yazı çıkması da aynı sorun.

## Ev stili — her promptun başına

```
Photorealistic macro product photography, shot on a 100mm macro lens at f/4,
single large softbox at 45 degrees with a white fill card opposite, deep
shadows, no harsh specular blowouts. Very dark background that falls off to
near black at the edges. Clean, technical, workshop-grade. Composition leaves
deliberate negative space in the upper 40% of the frame. Absolutely no text,
no letters, no numbers, no logos, no watermarks, no UI overlays anywhere in
the image. Aspect ratio 4:5.
```

Kategori rengi sonuna ekleniyor:

| Kategori | Zemin | Renk cümlesi |
|---|---|---|
| Elektronik & IoT | kobalt | `Color grade: deep cobalt blue background (#123A92 falling to #051442), with teal-cyan (#5EEAD4) rim light and reflections.` |
| Proje & Atölye | orman | `Color grade: deep forest green background (#0A543C falling to #03201C), with lime-green (#BEF264) rim light and reflections.` |
| 3D Baskı & Üretim | — | `Color grade: near-black background, warm orange (#FB923C) rim light and reflections.` |
| Ürün & Mağaza | — | Üretilmiyor, üreticinin fotoğrafı kullanılıyor. |

---

# 13 Ekim

## 12:38 · Optokuplör Ne Zaman Şart
`2026-10-13-optokuplor` · kapak görseli · 4:5

```
Photorealistic macro product photography, shot on a 100mm macro lens at f/4,
single large softbox at 45 degrees with a white fill card opposite, deep
shadows. Very dark background that falls off to near black at the edges.

Subject: an extreme close-up of a small black 4-pin DIP optocoupler chip
standing alone on a dark green printed circuit board, seen at a low three-
quarter angle so the chip reads as a solid block. The board is cut through by
a wide empty channel of bare substrate running right under the chip, splitting
the board into two separate copper regions — one on each side of the chip,
clearly not touching. Fine solder joints and a few passive components sit on
each side, slightly out of focus. Shallow depth of field, the chip body tack
sharp, the board falling away soft.

Composition: the chip sits in the lower third, the channel runs horizontally
across the frame, deliberate negative space in the upper 40%.

Color grade: deep cobalt blue background (#123A92 falling to #051442), with
teal-cyan (#5EEAD4) rim light along the top edge of the chip and faint cyan
reflections in the solder.

Absolutely no text, no letters, no numbers, no part markings, no logos, no
watermarks anywhere in the image. Aspect ratio 4:5.
```

Neden bu sahne: gönderinin tek cümlelik fikri "iki toprak birbirine
değmiyor". Kartı ikiye bölen boş kanal o fikrin kendisi. Çip üstündeki
yazıyı istemiyoruz — zaten PC817 yazısını biz basıyoruz.

## 20:42 · Prototip Çalıştı, Ürün Tutmuyor
`2026-10-13-olcu-dogrulama` · kapak görseli · 4:5

```
Photorealistic macro product photography, shot on a 100mm macro lens at f/5.6,
single large softbox at 45 degrees with a white fill card opposite, deep
shadows. Very dark background that falls off to near black at the edges.

Subject: a stainless steel digital caliper closed around the wall of a small
matte 3D-printed plastic part, jaws gripping it precisely, seen at a low
three-quarter angle. The printed part shows fine horizontal layer lines
catching the light. Four more identical printed parts sit in a loose row
behind it, progressively out of focus. Brushed steel, matte plastic, visible
tool marks. Shallow depth of field, the caliper jaws tack sharp.

Composition: caliper and part in the lower third, the row of parts receding to
the right, deliberate negative space in the upper 40%.

Color grade: deep forest green background (#0A543C falling to #03201C), with
lime-green (#BEF264) rim light along the caliper's steel edge and faint lime
reflections on the plastic.

Absolutely no text, no letters, no numbers, no digits on the caliper display
(show the screen dark and empty), no logos, no watermarks anywhere in the
image. Aspect ratio 4:5.
```

Neden bu sahne: gönderinin fikri "tek parça yetmiyor, beş parça ölçülüyor".
Arkadaki sıra o. Kumpas ekranı **karanlık** isteniyor, çünkü üretilen rakam
uydurma rakamdır; ölçüyü biz yazıyoruz.

## Hikaye sürümü

Aynı iki prompt, iki değişiklikle:

- `Aspect ratio 4:5` → `Aspect ratio 9:16`
- `negative space in the upper 40%` → `the subject sits in the lower third;
  the upper half is empty background`

## Yaptırmayacaklarımız

| Saat | Gönderi | Neden |
|---|---|---|
| 08:12 | Hangi Sunlu Filament | Üç makaranın gerçek fotoğrafı kesilmiş hâlde hazır |
| 17:24 | Sunlu AMS Heater | Sattığımız ürün; üreticinin fotoğrafı var |
