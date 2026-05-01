import streamlit as st
import pandas as pd
import os

# Setăm fișierul unde salvăm baza de date a echipei
DB_FILE = 'baza_de_date_goldset.csv'

# Încărcăm datele (fie fisierul JSON de la engine, fie CSV-ul)
@st.cache_data
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        # Aici citești rezultate_rolargesum.json la prima rulare
        df = pd.read_json('rezultate_rolargesum.json')
        df['Este_Expresie'] = "Necompletat" # Aici ar veni sugestia automată a AI-ului
        df['Tip_Variatie'] = "Necompletat"
        df['Verificat_De'] = ""
        return df

df = load_data()

st.set_page_config(page_title="Adnotare DERC", layout="wide")
st.title("🥇 Echipa Quality - Validare Gold Set")

# Colegul își alege numele ca să știm cine a adnotat
utilizator = st.selectbox("Cine ești?", ["Alege", "Adrian", "Daniel", "Petru", "Miruna", "Alin", "Robert"])

if utilizator != "Alege":
    # Găsim prima propoziție necompletată
    de_rezolvat = df[df['Este_Expresie'] == "Necompletat"]
    
    if not de_rezolvat.empty:
        idx = de_rezolvat.index[0]
        rand_curent = de_rezolvat.iloc[0]
        
        st.write(f"### Progrese Echipă: {len(df) - len(de_rezolvat)} din {len(df)} completate!")
        st.progress((len(df) - len(de_rezolvat)) / len(df))
        
        st.info(f"**Expresie suspectată de cod:** {rand_curent['expresie_gasita']}")
        st.markdown(f"### Text extras din știri:\n> *{rand_curent['text_original']}*")
        
        # Partea de butoane
        col1, col2 = st.columns(2)
        with col1:
            raspuns = st.radio("Este sens figurat (Expresie din DERC)?", ["DA (Sens Figurat)", "NU (Sens Literal - Fals Pozitiv)"])
        with col2:
            variatie = st.selectbox("Dacă e DA, ce variație are?", ["Niciuna (Exact ca în DERC)", "Flexiune (ex: a tăiat)", "Inserție (cuvinte în plus)", "Substituție (sinonim)"])
            
        if st.button("✅ Salvează și treci mai departe", type="primary"):
            # Salvăm răspunsul
            df.at[idx, 'Este_Expresie'] = raspuns
            df.at[idx, 'Tip_Variatie'] = variatie
            df.at[idx, 'Verificat_De'] = utilizator
            
            # Salvăm baza de date
            df.to_csv(DB_FILE, index=False)
            
            # --- FIX-UL AICI ---
            # Ștergem memoria cache ca la următorul refresh să citească noul CSV
            st.cache_data.clear() 
            
            # Dăm refresh la pagină pentru a trece la următoarea propoziție
            st.rerun()