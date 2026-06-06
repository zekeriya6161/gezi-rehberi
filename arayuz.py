import streamlit as st
import requests

STRAPI_URL = "https://lilly-starlet-dreamy.ngrok-free.dev"

st.set_page_config(page_title="Çok Dilli Gezi Rehberi", page_icon="🌍", layout="wide")

st.title("🌍 Çok Dilli Gezi Rehberi")

st.divider()


col1, col2 = st.columns(2)

with col1:
    dil_secimi = st.radio("Dil Seçin / Select Language:", ["Türkçe (TR)", "English (EN)"])
    locale = "tr" if dil_secimi == "Türkçe (TR)" else "en"

with col2:
    sehirler_istek = requests.get(f"{STRAPI_URL}/api/cities?locale={locale}")
    sehir_listesi = ["Tümü"] 
    
    if sehirler_istek.status_code == 200:
        sehir_datalari = sehirler_istek.json().get('data', [])
        for s in sehir_datalari:
            sehir_listesi.append(s['Ad'])
            
    secilen_sehir = st.selectbox("Şehir Seçin / Select City:", sehir_listesi)

st.divider()


if secilen_sehir == "Tümü":
    api_url = f"{STRAPI_URL}/api/places?populate=*&locale={locale}"
else:
    
    api_url = f"{STRAPI_URL}/api/places?filters[city][Ad][$eq]={secilen_sehir}&populate=*&locale={locale}"

cevap = requests.get(api_url)

if cevap.status_code == 200:
    mekanlar = cevap.json().get('data', [])
    
    if not mekanlar:
        st.warning("Bu şehirde henüz bir mekan bulunmamaktadır." if locale == "tr" else "No places found in this city yet.")
        
    for mekan in mekanlar:
        ad = mekan.get('Mekan_Adi', 'İsimsiz Mekan')
        aciklama = mekan.get('Aciklama', 'Açıklama bulunamadı.')
        puan = mekan.get('Puan', 0)
        
        gorsel_url = None
        kapak_resmi_data = mekan.get('Kapak_Resmi')
        
        
        if kapak_resmi_data:
            if isinstance(kapak_resmi_data, list) and len(kapak_resmi_data) > 0:
                gorsel_url = STRAPI_URL + kapak_resmi_data[0].get('url', '')
            elif isinstance(kapak_resmi_data, dict):
                gorsel_url = STRAPI_URL + kapak_resmi_data.get('url', '')


        c1, c2 = st.columns([1, 2])
        with c1:
            if gorsel_url:

                try:
                    resim_verisi = requests.get(gorsel_url).content
                    st.image(resim_verisi, use_container_width=True)
                except Exception:
                    st.info("Bu mekan için görsel yüklenemedi." if locale == "tr" else "Image could not be loaded.")
            else:
                st.info("Bu mekan için görsel bulunamadı." if locale == "tr" else "No image found for this place.")
        
        with c2:
            st.subheader(ad)
            st.write(aciklama)
            st.write(f"⭐ **Puan:** {puan} / 5")
            
        st.divider()
