import streamlit as st
import pandas as pd
import requests
import json
import os

st.set_page_config(page_title="Adnotare Gold Set - DERC", layout="wide")

# ==========================================
# CONFIGURARE GOOGLE FORMS
# ==========================================
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeQ0Oltd9Kt7KJEG2tIOHN9_7vcCuzzbrlNoHMZ5fHCrsV8cA/formResponse"

ENTRY_TEXT = "entry.1940749737"
ENTRY_EXPRESIE = "entry.1582472415"
ENTRY_DA_NU = "entry.1693132331"
ENTRY_VARIATIE = "entry.1100442775"
ENTRY_USER = "entry.1260560058"

USERS = ["Adrian", "Daniel", "Petru", "Miruna", "Alin", "Robert"]

# ==========================================
# ÎNCĂRCAREA DATELOR
# ==========================================
@st.cache_data
def load_data():
    path_1 = 'rezultate_rolargesum.json'
    path_2 = 'corpus_processing/rezultate_rolargesum.json'

    fisier_bun = path_1 if os.path.exists(path_1) else path_2 if os.path.exists(path_2) else None

    if fisier_bun:
        with open(fisier_bun, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def get_chunk(rezultate, utilizator):
    """Returnează (start_idx, end_idx, bucata) pentru utilizatorul dat."""
    chunk_size = len(rezultate) // len(USERS)
    user_idx = USERS.index(utilizator)
    start_idx = user_idx * chunk_size
    end_idx = (user_idx + 1) * chunk_size if user_idx < len(USERS) - 1 else len(rezultate)
    return start_idx, end_idx, rezultate[start_idx:end_idx]


rezultate = load_data()

# ==========================================
# INTERFAȚA WEB
# ==========================================
st.title("🥇 Echipa Quality - Validare Gold Set")

if not rezultate:
    st.error("❌ Nu am găsit fișierul `rezultate_rolargesum.json`. Verifică dacă e urcat!")
    st.stop()

utilizator = st.selectbox(
    "Cine ești? (Fiecare are bucata lui de rezolvat)",
    ["Alege"] + USERS,
)

if utilizator == "Alege":
    st.stop()

start_idx, end_idx, bucata_mea = get_chunk(rezultate, utilizator)

st.info(f"Salut, **{utilizator}**! Tu ai de adnotat de la propoziția {start_idx} până la {end_idx} (total: {len(bucata_mea)}).")

# ==========================================
# SESSION STATE PER-USER (asta era bug-ul)
# ==========================================
key_idx = f'idx_{utilizator}'
if key_idx not in st.session_state:
    st.session_state[key_idx] = 0

# Buton de reset, dacă vrei să o iei de la capăt
col_a, col_b = st.columns([1, 4])
with col_a:
    if st.button("🔄 Reset progres"):
        st.session_state[key_idx] = 0
        st.rerun()

index_local = st.session_state[key_idx]

# ==========================================
# AFIȘARE / FORMULAR
# ==========================================
if index_local >= len(bucata_mea):
    st.success(f"🎉 GATA, {utilizator}! Ai terminat bucata ta ({len(bucata_mea)} propoziții). Du-te bea o bere.")
    st.balloons()
    st.stop()

item_curent = bucata_mea[index_local]

st.progress(index_local / len(bucata_mea), text=f"Progresul tău: {index_local}/{len(bucata_mea)}")

st.subheader("Analizează Candidatul:")
st.markdown(f"**Expresie găsită de program:** `{item_curent.get('expresie_gasita')}`")
st.warning(f"📄 **Text Știre:**\n\n{item_curent.get('text_original')}")

col1, col2 = st.columns(2)
with col1:
    raspuns = st.radio(
        "Este sens figurat (Expresie din DERC)?",
        ["DA (E expresia)", "NU (Sens Literal / Eroare)"],
        key=f"raspuns_{utilizator}_{index_local}",
    )
with col2:
    variatie = st.selectbox(
        "Dacă e DA, ce variație este?",
        ["Niciuna", "Flexiune", "Inserție", "Substituție", "Sens Literal (Fals Pozitiv)"],
        key=f"variatie_{utilizator}_{index_local}",
    )

if st.button("🚀 Trimite la Baza de Date Centrală", type="primary"):
    payload = {
        ENTRY_TEXT: item_curent.get('text_original'),
        ENTRY_EXPRESIE: item_curent.get('expresie_gasita'),
        ENTRY_DA_NU: raspuns,
        ENTRY_VARIATIE: variatie,
        ENTRY_USER: utilizator,
    }
    try:
        r = requests.post(FORM_URL, data=payload, timeout=10)
        if r.status_code in (200, 302):
            st.success("Salvat cu succes în Google Sheets!")
            st.session_state[key_idx] += 1
            st.rerun()
        else:
            st.error(f"Google Forms a răspuns cu status {r.status_code}. Verifică ID-urile entry.")
    except Exception as e:
        st.error(f"Eroare de conexiune la Google Forms: {e}")