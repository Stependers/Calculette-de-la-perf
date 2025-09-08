import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculette de la Perf !", layout="centered")

# --- CSS pour responsive ---
st.markdown("""
<style>
/* Titre centré et adapté */
h1 {
    text-align: center;
    font-size: 28px;
}

/* Boutons centrés et plus gros */
div.stButton > button:first-child {
    font-size: 22px;
    background-color: #4CAF50;
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
    display: block;
    margin: 20px auto;
}

/* Encadrés VMA responsive */
.vma-result {
    border:2px solid #4CAF50;
    padding:15px;
    border-radius:10px;
    background-color:#e6f9e6;
    text-align:center;
    font-size:20px;
    font-weight:bold;
    margin-bottom:15px;
}

/* Colonnes empilées sur petit écran */
@media only screen and (max-width: 600px) {
    div[data-baseweb="column"] {
        flex-direction: column;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Titre global ---
st.markdown("<h1>💪 Calculette de la Perf ! 💪</h1>", unsafe_allow_html=True)

# --- Onglets pour sélectionner l'outil ---
onglets_outils = st.tabs(["📊 Calcul d'intervalles", "⚡ VMAïe !"])

# =========================
# --- Onglet 1 : Calcul d'intervalles ---
# =========================
with onglets_outils[0]:
    st.subheader("📏 Calcul d'intervalles")
    distance = st.number_input("Distance totale (km)", min_value=0.0, value=5.0, step=0.1)
    distance_m = distance * 1000

    mode_calc = st.radio("Sélectionner la méthode", ["Temps visé", "Allure visée"], horizontal=True)
    allure_s = 0
    temps_total_s = 0

    if mode_calc == "Temps visé":
        col1, col2 = st.columns(2)
        temps_min = col1.number_input("Minutes", min_value=0, value=25, step=1, key="t_min")
        temps_sec = col2.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="t_sec")
        temps_total_s = temps_min*60 + temps_sec
        if distance_m > 0 and temps_total_s > 0:
            allure_s = (temps_total_s / distance_m) * 1000
            st.markdown(f"**Allure :** {int(allure_s//60)} min {int(allure_s%60)} / km")
    else:
        col3, col4 = st.columns(2)
        allure_min = col3.number_input("Minutes", min_value=0, value=5, step=1, key="a_min")
        allure_sec = col4.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="a_sec")
        allure_s = allure_min*60 + allure_sec
        if distance_m > 0 and allure_s > 0:
            temps_total_s = (distance_m / 1000) * allure_s
            st.markdown(f"**Temps visé :** {int(temps_total_s//60)} min {int(temps_total_s%60)}")

    intervalle_type = st.radio("Type d'intervalle", ["Distance", "Temps"], horizontal=True)
    intervalle_m = intervalle_s = 0
    if intervalle_type == "Distance":
        intervalle_m = st.number_input("Intervalle choisi (m)", min_value=1, value=1000, step=100)
    else:
        col5, col6 = st.columns(2)
        intervalle_min = col5.number_input("Minutes", min_value=0, value=1, step=1)
        intervalle_sec = col6.number_input("Secondes", min_value=0, max_value=59, value=0, step=1)
        intervalle_s = intervalle_min*60 + intervalle_sec

    if st.button("🏃 En route pour la perf !"):
        if allure_s <= 0:
            st.warning("⚠ Veuillez saisir un temps visé ou une allure visée valide.")
        else:
            vitesse = 1000 / allure_s
            st.subheader("Résultats :")

            if intervalle_m > 0:
                nb = int(distance_m // intervalle_m)
                st.markdown(f"**Intervalle choisi : {intervalle_m} m**")
                for i in range(1, nb+1):
                    m = i * intervalle_m
                    t_s = m / vitesse
                    st.write(f"{int(m)} m → {int(t_s//60):02d}:{int(t_s%60):02d}")

            elif intervalle_s > 0:
                nb = int(temps_total_s // intervalle_s)
                st.markdown(f"**Intervalle temps : {intervalle_min} min {intervalle_sec} sec**")
                for i in range(1, nb+1):
                    t = i * intervalle_s
                    m = t * vitesse
                    st.write(f"{int(t//60):02d}:{int(t%60):02d} → {int(m)} m")

# =========================
# --- Onglet 2 : VMAïe ! ---
# =========================
with onglets_outils[1]:
    st.subheader("⚡ VMAïe ! - Outil de séances VMA")
    col_vma1, col_vma2 = st.columns(2)
    vma = col_vma1.number_input("VMA (km/h)", min_value=0.0, value=15.0, step=0.1)
    pct_vma_user = col_vma2.number_input("%VMA visé", min_value=50, max_value=120, value=100, step=5)

    mode_vma = st.radio("Mode de calcul", ["Distance connue", "Temps connu"], horizontal=True)

    if mode_vma == "Distance connue":
        dist = st.number_input("Distance à parcourir (m)", min_value=1, value=200, step=50)
        temps_s = dist / (vma * pct_vma_user / 100 * 1000 / 3600)
        st.markdown(f"<div class='vma-result'>Temps à réaliser : {int(temps_s//60)} min {int(temps_s%60)}</div>", unsafe_allow_html=True)
    else:
        col_t1, col_t2 = st.columns(2)
        t_min = col_t1.number_input("Minutes", min_value=0, value=1, step=1)
        t_sec = col_t2.number_input("Secondes", min_value=0, max_value=59, value=0, step=1)
        temps_s = t_min*60 + t_sec
        dist = temps_s * (vma * pct_vma_user / 100 * 1000 / 3600)
        st.markdown(f"<div class='vma-result'>Distance parcourue : {int(dist)} m</div>", unsafe_allow_html=True)

    st.subheader("Tableau des temps pour différentes distances et %VMA")
    distances_tab = [100, 200, 300, 400, 500, 600, 800, 1000]
    pct_tab = list(range(80, 125, 5))

    tableau = []
    for p in pct_tab:
        ligne = []
        for d in distances_tab:
            t_s = d / (vma * p / 100 * 1000 / 3600)
            ligne.append(f"{int(t_s//60):02d}:{int(t_s%60):02d}")
        tableau.append(ligne)

    df_tableau = pd.DataFrame(tableau, index=[f"{p}%" for p in pct_tab], columns=[f"{d} m" for d in distances_tab])
    st.dataframe(df_tableau)

# --- Copyright ---
st.markdown("<p style='text-align: center;'>© by Coach Antoine</p>", unsafe_allow_html=True)
