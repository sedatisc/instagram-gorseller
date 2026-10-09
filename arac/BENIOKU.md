# Görsel araçları

Afiş ya da sahne fotoğrafından stüdyo ürün karesi çıkarmak için.

## studyo.py — ürünü kendi zeminine oturt

Arka planı temizlenmiş PNG'leri alıp 1080 × 800 stüdyo karesi kuruyor:
degrade zemin, üstten ışık, temas gölgesi ve yere yansıma. Birden fazla
ürün verilirse boyları eşitleyip yan yana diziyor.

```
python3 arac/studyo.py <cikti.jpg> <ustHEX> <altHEX> <vurguHEX> <png...>
python3 arac/studyo.py gorsel/urun/x.jpg 2a2f3a 0c0e14 7a93b4 a.png b.png
```

Renkleri gönderinin `zemin` paletine yakın seç, kare sayfaya otursun.
Tek ürünlü karelerde `doluluk` 0,80 civarı iyi; uzun ince üründe 0,70.

## Arka planı temizleme

İki yol var, hangisinin işe yaradığı fotoğrafa bağlı:

**rembg** — karışık sahnelerde (tezgâh üstü, atölye) iyi çalışıyor.
`pip install --break-system-packages rembg onnxruntime`, model ilk
çalıştırmada GitHub'dan iniyor.

```python
from rembg import remove, new_session
remove(Image.open("x.jpg").convert("RGB"), session=new_session("u2net"))
```

**Parlaklık eşiği** — açık zeminde koyu ürün varsa rembg ürünün koyu
kısmını atabiliyor (Liber hotend'in soğutucusunda oldu). O durumda maskeyi
parlaklıktan çıkarmak daha doğru:

```python
L = 0.2126*r + 0.7152*g + 0.0722*b
mask = clip((205 - L) / 55, 0, 1)
```

Kesimden sonra alt kenardaki zemin şeridini kırp, yoksa yansımada
dikdörtgen artık kalıyor.

## hazirla.py · serit.py

`hazirla.py` konuyu zeminden ayırıp hedef tuvale oturtuyor (kapak
kadrajı için). `serit.py` birkaç kareyi ortak yükseklikte yan yana
diziyor. İkisi de arka plan temizlemeden çalışıyor; stüdyo karesi
gerekmiyorsa bunlar yeterli.
