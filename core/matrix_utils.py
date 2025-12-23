import googlemaps
import numpy as np
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def verileri_api_ile_getir(okullar):
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        st.error("❌ API Anahtarı bulunamadı! .env dosyasını kontrol edin.")
        return None, None

    gmaps = googlemaps.Client(key=api_key)
    n = len(okullar)
    koordinatlar = {}

    # 1. Koordinatları Çek (Geocoding)
    for i, okul in enumerate(okullar):
        try:
            res = gmaps.geocode(okul)
            if res:
                loc = res[0]['geometry']['location']
                # ÖDEV ŞARTI: Virgülden sonra 4 basamak
                koordinatlar[i] = (okul, (round(loc['lat'], 4), round(loc['lng'], 4)))
            else:
                st.warning(f"⚠️ {okul} adresi bulunamadı!")
        except Exception as e:
            st.error(f"❌ Geocoding hatası: {str(e)}")
            return None, None

    # 2. Mesafe Matrisi (Satır satır çekerek limiti aşmıyoruz)
    mesafe_matrisi = np.zeros((n, n))
    progress_bar = st.progress(0)
    st.write("🛣️ Yol mesafeleri hesaplanıyor...")

    for i in range(n):
        try:
            # Her okulu diğer tüm okullarla kıyasla (Satır bazlı istek)
            matrix_res = gmaps.distance_matrix(okullar[i], okullar, mode="driving")

            for j in range(n):
                if i == j:
                    mesafe_matrisi[i][j] = np.inf
                else:
                    element = matrix_res['rows'][0]['elements'][j]
                    if element['status'] == 'OK':
                        # Metreyi KM'ye çevir
                        mesafe_matrisi[i][j] = element['distance']['value'] / 1000.0
                    else:
                        mesafe_matrisi[i][j] = 999.0

                        # İlerleme çubuğunu güncelle
            progress_bar.progress((i + 1) / n)

        except Exception as e:
            st.error(f"❌ {okullar[i]} için mesafe çekilemedi: {str(e)}")
            return None, None

    progress_bar.empty()
    return koordinatlar, mesafe_matrisi