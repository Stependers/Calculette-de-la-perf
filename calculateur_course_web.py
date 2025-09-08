import streamlit as st

st.set_page_config(page_title="Calculette de la Perf !", layout="centered")

# --- Choix couleur titre ---
couleur_titre = st.selectbox("🎨 Choisis la couleur du titre :", 
                             ["Vert", "Bleu", "Orange", "Rouge", "Noir"], index=0)

couleurs_map = {
    "Vert": "#4CAF50",
    "Bleu": "#2196F3",
    "Orange": "#FF9800",
    "Rouge": "#F44336",
    "Noir": "#000000"
}
couleur = couleurs_map[couleur_titre]

# --- Titre stylisé centré ---
st.markdown(
    f"""
    <h1 style='text-align: center; color: {couleur}; font-size: 40px;'>
    💪 Calculette de la Perf ! 💪
    </h1>
    """,
    unsafe_allow_html=True
)

# --- Exemple bouton centré avec couleur variable ---
couleur_bouton = st.selectbox("🎨 Choisis la couleur du bouton :", 
                              ["Vert", "Bleu", "Orange", "Rouge", "Noir"], index=0)
couleur_btn = couleurs_map[couleur_bouton]

st.markdown(
    f"""
    <style>
    div.stButton > button:first-child {{
        font-size: 22px;
        background-color: {couleur_btn};
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        display: block;
        margin: 0 auto; /* centre horizontal */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("🏃 En route vers la perf !"):
    st.success("C'est parti 🚀")
