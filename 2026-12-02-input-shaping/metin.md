## Gönderi metni

Input shaping ve pressure advance ikisi de köşeyi düzeltiyor ama aynı kusura bakmıyorlar. Hangisinin gerektiğini kusurun yerinden anlıyorsun: köşeden sonra tekrar eden dalga titreşim, köşenin tam kendisinde şişme basınç.

Input shaping titreşimi söndürüyor. Gövde her yön değişiminde kendi frekansında salınıyor ve bu salınım duvara hayalet dalga olarak basılıyor. Frekans ADXL345 ivmeölçerle ölçülüyor; çoğu makinede 30-60 Hz çıkıyor. Hareket komutu o frekansı söndürecek şekilde bölünüyor.

Pressure advance basınç gecikmesini kapatıyor. Eriyik basıncı ekstruder adımını gecikmeli izliyor: köşeye girerken fazla, çıkarken eksik malzeme geliyor. Değer direct tahrikte 0,02-0,05, bowden'da 0,40-0,80 aralığında; test deseni basıp köşeye bakarak seçiliyor.

İkisi birlikte hızın kapısını açıyor. Titreşim sönünce ivmeyi 3.000 mm/s²'de tutma zorunluluğu kalkıyor, 10.000 mm/s² üstü kullanılabilir hale geliyor.

Klipper ikisini de taşıyor. Marlin tarafında pressure advance karşılığı Linear Advance, input shaping 2.1 sürümlerinde geldi.

Köşelerdeki dalgayı yazıcının kaderi sanan bir arkadaşın varsa bu gönderiyi ona yolla.

#sermenkreatif #3dbaski #3dprinting #klipper #3dbaskiturkiye

## İlk yorum

İkisini aynı baskıda ayarlamaya çalışma: önce input shaping'i kur, sonra pressure advance test desenini bas — titreşim varken köşedeki şişmeyi doğru okumak mümkün değil.
