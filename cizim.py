# -*- coding: utf-8 -*-
"""İzometrik çizim kitaplığı.

Serbest çizilen çokgen yerine tek bir projeksiyon ve tek bir ışık yönü
kullanılıyor. Bütün hacimler buradaki `kutu` ile çiziliyor; yüzeylerin
parlaklığı ışığa göre otomatik hesaplanıyor, böylece farklı parçalar
birbirine oturuyor.

Projeksiyon: 2:1 izometrik. x sağa-aşağı, y sola-aşağı, z yukarı.
Işık: sol üstten. Üst yüzey en parlak, sol yüz orta, sağ yüz en koyu.
"""
from PIL import Image, ImageDraw, ImageFilter

# 2:1 izometrik birim vektörler
EX = (0.866, 0.5)
EY = (-0.866, 0.5)
EZ = (0.0, -1.0)

# yüzey parlaklıkları — ışık sol üstten
UST, SOL, SAG = 1.0, 0.74, 0.52


def yans(ox, oy, x, y, z, s=1.0):
    """3B noktayı 2B tuvale yansıt."""
    return (ox + (x * EX[0] + y * EY[0]) * s,
            oy + (x * EX[1] + y * EY[1] + z * EZ[1]) * s)


def ton(c, k):
    """Rengi k katsayısıyla aydınlat/karart (k=1 kendisi)."""
    if k <= 1:
        return tuple(max(0, min(255, int(v * k))) for v in c[:3])
    t = min(1.0, k - 1)
    return tuple(max(0, min(255, int(v + (255 - v) * t))) for v in c[:3])


def kutu(d, ox, oy, x, y, z, gx, gy, gz, renk, s=1.0, ust=True):
    """Köşesi (x,y,z) olan gx×gy×gz kutuyu üç yüzüyle çiz."""
    P = lambda a, b, c: yans(ox, oy, a, b, c, s)
    x1, y1, z1 = x + gx, y + gy, z + gz
    if ust:
        d.polygon([P(x, y, z1), P(x1, y, z1), P(x1, y1, z1), P(x, y1, z1)],
                  fill=ton(renk, UST))
    # sol yüz (y = y1 düzlemi, izleyiciye sol)
    d.polygon([P(x, y1, z1), P(x1, y1, z1), P(x1, y1, z), P(x, y1, z)],
              fill=ton(renk, SOL))
    # sağ yüz (x = x1 düzlemi)
    d.polygon([P(x1, y, z1), P(x1, y1, z1), P(x1, y1, z), P(x1, y, z)],
              fill=ton(renk, SAG))


def yuzey(d, ox, oy, kose, renk, s=1.0, k=1.0):
    """Serbest düzlem — kose: [(x,y,z), ...]."""
    d.polygon([yans(ox, oy, *p, s=s) for p in kose], fill=ton(renk, k))


def golge(boy, ox, oy, x, y, gx, gy, s=1.0, op=0.38, bulanik=18):
    """Zemine düşen yumuşak gölge katmanı döndürür."""
    lay = Image.new("RGBA", boy, (0, 0, 0, 0))
    g = ImageDraw.Draw(lay)
    kay = gy * 0.55
    g.polygon([yans(ox, oy, x - kay, y, 0, s),
               yans(ox, oy, x + gx - kay, y, 0, s),
               yans(ox, oy, x + gx - kay, y + gy, 0, s),
               yans(ox, oy, x - kay, y + gy, 0, s)],
              fill=(0, 0, 0, int(255 * op)))
    return lay.filter(ImageFilter.GaussianBlur(bulanik))
