import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Adnotare pt Goldset", layout="wide")

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeQ0Oltd9Kt7KJEG2tIOHN9_7vcCuzzbrlNoHMZ5fHCrsV8cA/formResponse"

ENTRY_TEXT = "entry.1940749737"
ENTRY_EXPRESIE = "entry.1582472415"
ENTRY_DA_NU = "entry.1693132331"
ENTRY_VARIATIE = "entry.1100442775"
ENTRY_USER = "entry.1260560058"

USERS = ["Adrian", "Daniel", "Petru", "Miruna", "Alin", "Robert"]

# Mutează sau activează debug pentru diagnostic
DEBUG = True

@st.cache_data
def load_data():
    """
    incarcarea fisierului json de adnotat cel cu candidatii
    """
    paths= [
        'generate_rolargesum.json',
        'rezultate_rolargesum.json',
        'corpus_processing/rezultate_rolargesum.json',
        'data/rezultate_rolargesum.json',
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f), p
    return [], None


def split_evenly(n_items, n_users, user_idx):
    """
    impartim n_items pe n_users cat mai uniform 
    primii (n_items % n_users) users primesc cate un item in plus
    """
    base = n_items // n_users
    rest = n_items % n_users
    if user_idx < rest:
        start = user_idx * (base + 1)
        end = start + (base + 1)
    else:
        start = rest * (base + 1) + (user_idx - rest) * base
        end = start + base
    return start, end


def get_chunk(rezultate, utilizator):
    user_idx = USERS.index(utilizator)
    start_idx, end_idx = split_evenly(len(rezultate), len(USERS), user_idx)
    return start_idx, end_idx, rezultate[start_idx:end_idx]


rezultate, fisier_incarcat = load_data()

#INTERFATA
st.title("Adnotare candidati pentru GoldSET")

if not rezultate:
    st.error("!!!Nu am gasit inputul de candidati!!!")
    st.stop()

utilizator = st.selectbox(
    "Utilizatori",
    ["Alege"] + USERS,
)

if utilizator == "Alege":
    st.stop()

index_start, index_sf, bucata_mea = get_chunk(rezultate, utilizator)


if len(bucata_mea) == 0:
    st.warning(
        f"!!{utilizator}, nu ai itemi de adnotat;"
        f"sunt {len(rezultate)} itemi pentru {len(USERS)} adnotatori "
        f"deci nu mai ramane nimic pentru tine. "
    )
    st.stop()

st.info(
    f"Salut, **{utilizator}**! Ai de adnotat itemii {index_start} -> {index_sf - 1} "
    f"(total:**{len(bucata_mea)}**)."
)

key = f'idx_{utilizator}'
if key not in st.session_state:
    st.session_state[key] = 0

col_a, col_b = st.columns([1, 4])
with col_a:
    if st.button("Reset progres"):
        st.session_state[key] = 0
        st.rerun()

index_local = st.session_state[key]

# flag pentru a evita trimiterea multipla a aceluiasi item
submit_flag = f"submitting_{utilizator}_{index_local}"
if submit_flag not in st.session_state:
    st.session_state[submit_flag] = False


if index_local >= len(bucata_mea):
    st.success(f"GATA, {utilizator}! Ai terminat bucata ta ({len(bucata_mea)} prop).")
    st.stop()

item_curent = bucata_mea[index_local]

st.progress(index_local / len(bucata_mea), text=f"Progresul tau: {index_local}/{len(bucata_mea)}")

st.markdown(f"Expresie gasita de program: `{item_curent.get('expresie_gasita')}`")
st.warning(f"**Text Stire:**\n\n{item_curent.get('text_original')}")

col1, col2 = st.columns(2)
with col1:
    raspuns = st.radio(
        "Este sens figurat (Expresie din DERC)?",
        ["DA (E expresia)", "NU (Sens Literal / Eroare)"],
        key=f"raspuns_{utilizator}_{index_local}",
    )
with col2:
    variatie = st.selectbox(
        "Daca e DA, ce variatie este?",
        ["Niciuna", "Flexiune", "Insertie", "Substitutie", "Sens Literal (Fals Pozitiv)"],
        key=f"variatie_{utilizator}_{index_local}",
    )

if st.session_state.get(submit_flag):
    st.info("Se trimite... asteapta putin.")
else:
    if st.button("Trimite", type="primary", key=f"submit_{utilizator}_{index_local}"):
        # marcheaza ca trimitem pentru a evita click-uri duplicate
        st.session_state[submit_flag] = True
        payload = {
            ENTRY_TEXT: item_curent.get('text_original'),
            ENTRY_EXPRESIE: item_curent.get('expresie_gasita'),
            ENTRY_DA_NU: raspuns,
            ENTRY_VARIATIE: variatie,
            ENTRY_USER: utilizator,
        }
        try:
            # Folosim un header simplu ca unele endpoint-uri pot filtra cererile "ne-browser"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT; Streamlit)',
                'Referer': FORM_URL,
            }
            r = requests.post(FORM_URL, data=payload, timeout=15, headers=headers)
            # Debug: arătăm status și un fragment din răspuns pentru diagnostic
            if DEBUG:
                st.write("DEBUG: status_code", r.status_code)
                try:
                    st.write("DEBUG: response snippet:\n", r.text[:1000])
                except Exception:
                    st.write("DEBUG: response not text-displayable")

            if r.status_code in (200, 302):
                st.success("Salvat")
                st.session_state[key] += 1
                # resetam flagul inainte de rerun pentru a evita blocarea ulterioara
                st.session_state[submit_flag] = False
                st.rerun()
            else:
                st.error(f"Google Forms a raspuns cu status {r.status_code}. Verifica ID-urile entry.")
                st.session_state[submit_flag] = False
        except Exception as e:
            st.error(f"Eroare de conexiune la Google Forms: {e}")
            if DEBUG:
                import traceback
                st.text(traceback.format_exc())
            st.session_state[submit_flag] = False