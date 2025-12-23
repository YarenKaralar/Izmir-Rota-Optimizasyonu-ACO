İzmir İl Milli Eğitim Müdürlüğü Rota Optimizasyonu (ACO)
Bu proje, İzmir'deki 15 farklı okulun en verimli şekilde ziyaret edilebilmesi için Karınca Kolonisi Algoritması (Ant Colony Optimization - ACO) kullanılarak geliştirilmiş bir rota optimizasyon sistemidir.

Projenin Amacı
İzmir İl Milli Eğitim Müdürlüğü'nden yola çıkan bir yetkilinin, belirlenen 15 okulu en kısa mesafeyi kat ederek ziyaret etmesini ve başlangıç noktasına geri dönmesini sağlamaktır. Projede kuş uçuşu mesafe yerine, Google Maps API kullanılarak gerçek zamanlı sürüş mesafeleri baz alınmıştır.

Kullanılan Teknolojiler ve Kütüphaneler
Python 3.9+: Ana programlama dili.

Streamlit: Web tabanlı kullanıcı arayüzü.

Google Maps API (Distance Matrix & Geocoding): Okul koordinatlarını çekmek ve gerçek yol mesafelerini hesaplamak için.

Folium & Streamlit-Folium: İnteraktif harita görselleştirmesi.

Numpy & Pandas: Veri işleme ve matris hesaplamaları.

Algoritma Detayları: Karınca Kolonisi (ACO)
Algoritma, karıncaların yiyecek ararken bıraktıkları feromon izlerini simüle eder. Her iterasyonda karıncalar bir sonraki okulu şu formüle göre seçer:

P 
ij
​	
 = 
∑(τ 
ik
α
​	
 )(η 
ik
β
​	
 )
(τ 
ij
α
​	
 )(η 
ij
β
​	
 )
​	
 
τ (Feromon): Önceki karıncaların deneyimini temsil eder.

η (Sezgisel Bilgi): Mesafenin tersidir (1/d), yani yakın olan yer daha çekicidir.

Alpha & Beta: Bu iki parametre arasındaki dengeyi ayarlar.

Öne Çıkan Özellikler
Gerçek Veri Hassasiyeti: Koordinat hesaplamaları ödev şartlarına uygun olarak virgülden sonra 4 basamak hassasiyetle yapılmaktadır.

Görsel Analiz: Her iterasyondaki en kısa mesafe değişimi grafik üzerinde canlı olarak takip edilebilir.

İnteraktif Harita: Hesaplanan en kısa rota, Folium üzerinden interaktif bir harita üzerinde kırmızı çizgi ile gösterilir.

Güvenlik Notu

Ödev kuralları gereği, kişisel API anahtarını içeren .env dosyası repoya dahil edilmemiştir. Lütfen kendi anahtarınızla test ediniz.
