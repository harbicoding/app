import streamlit as st
import pandas as pd
import requests
import json
import os

st.set_page_config(page_title="Adnotare Gold Set - DERC", layout="wide")

# ==========================================
# CONFIGURARE GOOGLE FORMS (PUNE DATELE TALE AICI)
# ==========================================
# 1. URL-ul formularului (ATENȚIE: trebuie să se termine în formResponse, nu viewform)
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeQ0Oltd9Kt7KJEG2tIOHN9_7vcCuzzbrlNoHMZ5fHCrsV8cA/formResponse"

# 2. Pune ID-urile extrase din pre-filled link
ENTRY_TEXT = "entry.1940749737"      # Câmpul pentru Textul din Știre
ENTRY_EXPRESIE = "entry.1582472415"  # Câmpul pentru Expresia Găsită
ENTRY_DA_NU = "entry.1693132331"     # Câmpul pentru DA/NU
ENTRY_VARIATIE = "entry.1100442775"  # Câmpul pentru Tip Variație
ENTRY_USER = "entry.1260560058"      # Câmpul pentru Cine a verificat

# ==========================================
# ÎNCĂRCAREA DATELOR
# ==========================================
@st.cache_data
def load_data():
    # Încearcă să găsească fișierul indiferent de folder
    path_1 = 'rezultate_rolargesum.json'
    path_2 = 'corpus_processing/rezultate_rolargesum.json'
    
    fisier_bun = path_1 if os.path.exists(path_1) else path_2 if os.path.exists(path_2) else None
    
    if fisier_bun:
        with open(fisier_bun, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

rezultate = load_data()

# ==========================================
# INTERFAȚA WEB
# ==========================================
st.title("🥇 Echipa Quality - Validare Gold Set")

if not rezultate:
    st.error("❌ Nu am găsit fișierul `rezultate_rolargesum.json` pe GitHub. Verifică dacă l-ai urcat!")
    st.stop()

# Ca să nu faceți toți aceleași propoziții, împărțim fișierul
utilizator = st.selectbox("Cine ești? (Fiecare are bucata lui de rezolvat)", 
                          ["Alege", "Adrian", "Daniel", "Petru", "Miruna", "Alin", "Robert"])

if utilizator != "Alege":
    # Calculăm câte propoziții are fiecare (ex: 600 prop / 6 oameni = 100 de căciulă)
    chunk_size = len(rezultate) // 6
    users = ["Adrian", "Daniel", "Petru", "Miruna", "Alin", "Robert"]
    user_idx = users.index(utilizator)
    
    start_idx = user_idx * chunk_size
    # Ultimul ia și restul, dacă nu se împarte exact
    end_idx = (user_idx + 1) * chunk_size if user_idx < 5 else len(rezultate)
    
    bucata_mea = rezultate[start_idx:end_idx]
    
    st.info(f"Salut, {utilizator}! Tu ai de adnotat de la propoziția {start_idx} până la {end_idx}.")
    
    # Track progresul utilizatorului in sesiune
    if 'current_idx' not in st.session_state:
        st.session_state.current_idx = 0
        
    index_local = st.session_state.current_idx
    
    if index_local < len(bucata_mea):
        item_curent = bucata_mea[index_local]
        
        st.progress(index_local / len(bucata_mea), text=f"Progresul tău: {index_local}/{len(bucata_mea)}")
        
        st.subheader("Analizează Candidatul:")
        st.markdown(f"**Expresie găsită de program:** `{item_curent.get('expresie_gasita')}`")
        st.warning(f"📄 **Text Știre:** \n\n {item_curent.get('text_original')}")
        
        # Formularul de decizie
        col1, col2 = st.columns(2)
        with col1:
            raspuns = st.radio("Este sens figurat (Expresie din DERC)?", 
                               ["DA (E expresia)", "NU (Sens Literal / Eroare)"])
        with col2:
            variatie = st.selectbox("Dacă e DA, ce variație este?", 
                                    ["Niciuna", "Flexiune", "Inserție", "Substituție", "Sens Literal (Fals Pozitiv)"])
            
        if st.button("🚀 Trimite la Baza de Date Centrală", type="primary"):
            # Trimitem invizibil pe Google Forms
            payload = {
                ENTRY_TEXT: item_curent.get('text_original'),
                ENTRY_EXPRESIE: item_curent.get('expresie_gasita'),
                ENTRY_DA_NU: raspuns,
                ENTRY_VARIATIE: variatie,
                ENTRY_USER: utilizator
            }
            try:
                requests.post(FORM_URL, data=payload)
                st.success("Salvat cu succes în Google Sheets!")
                
                # Trecem la următoarea
                st.session_state.current_idx += 1
                st.rerun()
            except Exception as e:
                st.error(f"Eroare de conexiune la Google Forms: {e}")
    else:
        st.success("🎉 GATA! Ai terminat bucata ta din Gold Set! Du-te bea o bere.")
        st.balloons()