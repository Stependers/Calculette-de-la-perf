import streamlit as st

st.set_page_config(page_title="Calculette de la Perf !", layout="centered")

# Titre centré
st.markdown("<h1 style='text-align: center;'>💪 Calculette de la Perf ! 💪</h1>", unsafe_allow_html=True)

# Distance totale
distance = st.number_input("Distance totale (km)", min_value=0.0, value=5.0, step=0.1)
distance_m = distance * 1000

# Onglets pour Temps / Allure
tab_time, tab_pace = st.tabs(["⏱️ Temps visé", "🏃 Allure visée (min/km)"])
allure_s = 0
temps_total_s = 0

with tab_time:
    col1, col2 = st.columns(2)
    temps_min = col1.number_input("Minutes", min_value=0, value=25, step=1, key="t_min")
    temps_sec = col2.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="t_sec")
    temps_total_s = temps_min*60 + temps_sec
    if distance_m > 0:
        allure_s = temps_total_s / distance_m * 1000
        st.markdown(f"**Allure visée :** {int(allure_s//60)} min {int(allure_s%60)} sec / km")

with tab_pace:
    col3, col4 = st.columns(2)
    allure_min = col3.number_input("Minutes", min_value=0, value=5, step=1, key="a_min")
    allure_sec = col4.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="a_sec")
    allure_s = allure_min*60 + allure_sec
    if distance_m > 0:
        temps_total_s = distance_m / 1000 * allure_s
        st.markdown(f"**Temps visé :** {int(temps_total_s//60)} min {int(temps_total_s%60)} sec")

# Onglets pour Intervalle
st.subheader("Intervalle")
# Simule un bouton radio via radio + onglets
interval_type = st.radio("Sélectionnez le type d'intervalle :", ["Distance", "Temps"], horizontal=True)

tab_dist, tab_time_interval = st.tabs(["📏 Distance", "⏳ Temps"])

intervalle_m = intervalle_s = 0

with tab_dist:
    if interval_type == "Distance":
        intervalle_m = st.number_input("Intervalle distance (m)", min_value=1, value=1000, step=100)

with tab_time_interval:
    if interval_type == "Temps":
        col5, col6 = st.columns(2)
        intervalle_min = col5.number_input("Minutes", min_value=0, value=1, step=1)
        intervalle_sec = col6.number_input("Secondes", min_value=0, max_value=59, value=0, step=1)
        intervalle_s = intervalle_min*60 + intervalle_sec

# Bouton central
if st.button("🏃 En route pour la perf !"):
    if allure_s <= 0:
        st.warning("⚠ Veuillez saisir un temps ou une allure valide.")
    else:
        vitesse = 1000 / allure_s
        st.subheader("Résultats :")
        if interval_type == "Distance" and intervalle_m > 0:
            nb = int(distance_m // intervalle_m)
            st.markdown(f"**Intervalle distance : {intervalle_m} m**")
            for i in range(1, nb+1):
                m = i * intervalle_m
                t_s = m / vitesse
                st.write(f"{int(m)} m → {int(t_s//60):02d}:{int(t_s%60):02d} sec")
        elif interval_type == "Temps" and intervalle_s > 0:
            nb = int(temps_total_s // intervalle_s)
            st.markdown(f"**Intervalle temps : {intervalle_min} min {intervalle_sec} sec**")
            for i in range(1, nb+1):
                t = i * intervalle_s
                m = t * vitesse
                st.write(f"{int(t//60):02d}:{int(t%60):02d} → {int(m)} m")
