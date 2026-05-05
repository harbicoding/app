import streamlit as st
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
    """
    Încarcă candidații de adnotat. ATENȚIE: trebuie rezultate_rolargesum.json
    (candidații propuși de program), NU generate_rolargesum.json (gold setul OUTPUT).
    """
    paths_to_try = [
        'generate_rolargesum.json',
        'rezultate_rolargesum.json',
        'corpus_processing/rezultate_rolargesum.json',
        'data/rezultate_rolargesum.json',
    ]
    for p in paths_to_try:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f), p
    return [], None


def split_evenly(n_items, n_users, user_idx):
    """
    Împarte n_items pe n_users cât mai uniform posibil.
    Primii (n_items % n_users) users primesc câte un item în plus.

    Ex: 7 itemi, 6 users -> primul ia 2, restul câte 1 each.
    Ex: 5 itemi, 6 users -> primii 5 iau câte 1, ultimul primește 0.
    """
    base = n_items // n_users
    remainder = n_items % n_users
    if user_idx < remainder:
        start = user_idx * (base + 1)
        end = start + (base + 1)
    else:
        start = remainder * (base + 1) + (user_idx - remainder) * base
        end = start + base
    return start, end


def get_chunk(rezultate, utilizator):
    user_idx = USERS.index(utilizator)
    start_idx, end_idx = split_evenly(len(rezultate), len(USERS), user_idx)
    return start_idx, end_idx, rezultate[start_idx:end_idx]


rezultate, fisier_incarcat = load_data()

# ==========================================
# INTERFAȚA WEB
# ==========================================
st.title("🥇 Echipa Quality - Validare Gold Set")

if not rezultate:
    st.error("❌ Nu am găsit `rezultate_rolargesum.json` în repo. Verifică dacă e urcat la rădăcina proiectului.")
    st.stop()

# Sidebar cu info de debug - util pe Streamlit Cloud
with st.sidebar:
    st.caption(f"📁 Fișier încărcat: `{fisier_incarcat}`")
    st.caption(f"📊 Total itemi: **{len(rezultate)}**")
    if st.button("🔄 Reîncarcă din fișier (clear cache)"):
        st.cache_data.clear()
        st.rerun()

utilizator = st.selectbox(
    "Cine ești? (Fiecare are bucata lui de rezolvat)",
    ["Alege"] + USERS,
)

if utilizator == "Alege":
    st.stop()

start_idx, end_idx, bucata_mea = get_chunk(rezultate, utilizator)

# Dacă chunk-ul e gol (mai puțini itemi decât users), nu mai poți face nimic
if len(bucata_mea) == 0:
    st.warning(
        f"⚠️ {utilizator}, nu ai itemi de adnotat — sunt doar {len(rezultate)} itemi pentru "
        f"{len(USERS)} adnotatori, deci nu mai rămâne nimic pentru tine. "
        f"Mai urcă date în `rezultate_rolargesum.json` sau lasă pe ceilalți să termine primii."
    )
    st.stop()

st.info(
    f"Salut, **{utilizator}**! Ai de adnotat itemii {start_idx} → {end_idx - 1} "
    f"(total: **{len(bucata_mea)}** propoziții)."
)

# ==========================================
# SESSION STATE PER-USER
# ==========================================
key_idx = f'idx_{utilizator}'
if key_idx not in st.session_state:
    st.session_state[key_idx] = 0

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