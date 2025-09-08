import streamlit as st

# --- Configuration de la page ---
st.set_page_config(page_title="Calculette de la Perf !", layout="centered")

# --- Titre centré ---
st.markdown("<h1 style='text-align: center;'>💪 Calculette de la Perf ! 💪</h1>", unsafe_allow_html=True)

# --- Distance totale ---
st.subheader("Distance totale")
col_dist1, col_dist2 = st.columns([2,1])
distance = col_dist1.number_input("Entrez la distance :", min_value=0.0, value=5.0, step=0.1)
unite = col_dist2.selectbox("Unité :", ["km", "m"])
distance_m = distance * 1000 if unite == "km" else distance

# --- Onglets Temps visé / Allure visée ---
tab1, tab2 = st.tabs(["⏱️ Temps visé", "🏃 Allure visée (min/km)"])

# Variables locales
temps_total_s_tab1 = 0
allure_s_tab1 = 0
temps_total_s_tab2 = 0
allure_s_tab2 = 0

# --- Onglet Temps visé ---
with tab1:
    col1, col2 = st.columns(2)
    temps_min = col1.number_input("Minutes", min_value=0, value=25, step=1, key="t_min_tab1")
    temps_sec = col2.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="t_sec_tab1")
    if st.button("Calculer allure", key="btn_temps_tab1"):
        temps_total_s_tab1 = temps_min*60 + temps_sec
        if temps_total_s_tab1 > 0 and distance_m > 0:
            allure_s_tab1 = (temps_total_s_tab1 / distance_m) * 1000
            st.success(f"Allure visée : {int(allure_s_tab1//60)} min {int(allure_s_tab1%60)} sec / km")

# --- Onglet Allure visée ---
with tab2:
    col3, col4 = st.columns(2)
    allure_min = col3.number_input("Minutes", min_value=0, value=5, step=1, key="a_min_tab2")
    allure_sec = col4.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="a_sec_tab2")
    if st.button("Calculer temps", key="btn_allure_tab2"):
        allure_s_tab2 = allure_min*60 + allure_sec
        if allure_s_tab2 > 0 and distance_m > 0:
            temps_total_s_tab2 = (distance_m / 1000) * allure_s_tab2
            st.success(f"Temps visé : {int(temps_total_s_tab2//60)} min {int(temps_total_s_tab2%60)} sec")

# --- Onglets Intervalle ---
tab3, tab4 = st.tabs(["📏 Intervalle par distance", "⏳ Intervalle par temps"])

# --- Intervalle par distance ---
with tab3:
    intervalle_m = st.number_input("Intervalle distance (m)", min_value=1, value=1000, step=100, key="intervalle_distance_tab3")
    sorties_distance = []
    if st.button("Calculer intervalle (Distance)", key="btn_intervalle_distance"):
        # On choisit quelle allure utiliser selon onglet actif
        allure_s = allure_s_tab1 if allure_s_tab1 > 0 else allure_s_tab2
        if intervalle_m > 0 and allure_s > 0:
            vitesse = 1000 / allure_s
            nb_intervalles = int(distance_m // intervalle_m)
            for i in range(1, nb_intervalles + 1):
                m = i * intervalle_m
                t_s = m / vitesse
                sorties_distance.append(f"{int(m)} m → {int(t_s//60):02d}:{int(t_s%60):02d} sec")
            st.subheader("Résultats Intervalle Distance :")
            for s in sorties_distance:
                st.write(s)

# --- Intervalle par temps ---
with tab4:
    col5, col6 = st.columns(2)
    intervalle_min = col5.number_input("Minutes", min_value=0, value=1, step=1, key="intervalle_temps_min_tab4")
    intervalle_sec = col6.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="intervalle_temps_sec_tab4")
    sorties_temps = []
    if st.button("Calculer intervalle (Temps)", key="btn_intervalle_temps"):
        allure_s = allure_s_tab1 if allure_s_tab1 > 0 else allure_s_tab2
        intervalle_s = intervalle_min*60 + intervalle_sec
        if intervalle_s > 0 and allure_s > 0:
            vitesse = 1000 / allure_s
            # temps_total_s dépend de l’onglet actif
            temps_total_s = temps_total_s_tab1 if temps_total_s_tab1 > 0 else temps_total_s_tab2
            nb_intervalles = int(temps_total_s // intervalle_s)
            for i in range(1, nb_intervalles + 1):
                t = i * intervalle_s
                m = t * vitesse
                sorties_temps.append(f"{int(t//60):02d}:{int(t%60):02d} → {int(m)} m")
            st.subheader("Résultats Intervalle Temps :")
            for s in sorties_temps:
                st.write(s)

# --- Bouton central général (optionnel) ---
st.markdown("""
<style>
div.stButton > button:first-child {
    font-size: 22px;
    background-color: #4CAF50;
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
    display: block;
    margin: 20px auto;
}
</style>
""", unsafe_allow_html=True)
