import numpy as np
import random


def hesapla_cekicilik(mesafe):             #mesafe ne kadar kucukse, o yol karinca icin o kadar cekicidir
    cekicilik = np.zeros_like(mesafe)
    with np.errstate(divide='ignore'):
        cekicilik = 1 / mesafe             #mesafenin tersi alinir
        cekicilik[mesafe == np.inf] = 0
    return cekicilik


def olasilik_hesapla(mevcut, ziyaret_edilmemisler, feromon, cekicilik, alpha, beta):
    #Karınca bir sonraki durağa gitmek için feromon ve çekicilik değerlerini çarpar.
    toplam = 0
    olasiliklar = {}
    for j in ziyaret_edilmemisler:
        # Pheromone ^ alpha * Visibility ^ beta
        deger = (feromon[mevcut][j] ** alpha) * (cekicilik[mevcut][j] ** beta)
        olasiliklar[j] = deger
        toplam += deger

    for j in olasiliklar:
        olasiliklar[j] /= toplam if toplam > 0 else 1
    return olasiliklar


def rulet_tekerlegi_secimi(olasilik_dict):
    """Olasılıklara göre rastgele bir sonraki durağı seçer"""
    r = random.random()
    toplam = 0
    for sehir, olasilik in olasilik_dict.items():
        toplam += olasilik
        if r <= toplam:
            return sehir


def karinca_gezi(baslangic, mesafe, feromon, alpha, beta):
    """Tek bir karıncanın tüm şehirleri dolaşması"""
    n = len(mesafe)
    yol = [baslangic]
    toplam_uzunluk = 0
    cekicilik = hesapla_cekicilik(mesafe)

    while len(yol) < n:
        mevcut = yol[-1]
        ziyaret_edilmemisler = list(set(range(n)) - set(yol))
        olasiliklar = olasilik_hesapla(mevcut, ziyaret_edilmemisler, feromon, cekicilik, alpha, beta)
        secilen = rulet_tekerlegi_secimi(olasiliklar)
        yol.append(secilen)
        toplam_uzunluk += mesafe[mevcut][secilen]

    # Başlangıç noktasına geri dön (Döngüyü tamamla)
    toplam_uzunluk += mesafe[yol[-1]][yol[0]]
    yol.append(yol[0])
    return yol, toplam_uzunluk


def feromon_guncelle(feromon, yollar, buharlasma_orani, Q=1.0):
    """Feromon miktarını buharlaştırır ve yeni yollara göre günceller"""
    # Buharlaşma
    feromon = (1 - buharlasma_orani) * feromon
    # Karıncaların bıraktığı yeni feromon
    for yol, uzunluk in yollar:
        for i in range(len(yol) - 1):
            a, b = yol[i], yol[i + 1]
            katki = Q / uzunluk
            feromon[a][b] += katki
            feromon[b][a] += katki
    return feromon


def run_aco(mesafe, karinca_sayisi=15, iterasyon_sayisi=30, alpha=1, beta=2,
            buharlasma_orani=0.5, feromon_katkisi=1):
    """Algoritmayı ana başlatan fonksiyon"""
    sehir_sayisi = len(mesafe)
    feromon = np.ones_like(mesafe) * 0.1
    en_iyi_yol = None
    en_kisa_mesafe = float("inf")
    iterasyon_en_iyiler = []

    for it in range(iterasyon_sayisi):
        yollar = []
        for _ in range(karinca_sayisi):
            # Karıncaları her zaman 0. noktadan (Milli Eğitim Müdürlüğü) başlatıyoruz
            yol, uzunluk = karinca_gezi(0, mesafe, feromon, alpha, beta)
            yollar.append((yol, uzunluk))

            if uzunluk < en_kisa_mesafe:
                en_kisa_mesafe = uzunluk
                en_iyi_yol = yol

        feromon = feromon_guncelle(feromon, yollar, buharlasma_orani, feromon_katkisi)
        iterasyon_en_iyiler.append(en_kisa_mesafe)

    return en_iyi_yol, en_kisa_mesafe, iterasyon_en_iyiler