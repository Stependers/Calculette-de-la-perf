import streamlit as st

st.set_page_config(page_title="Calculette de la Perf !", layout="centered")

st.markdown("<h1 style='text-align: center;'>💪 Calculette de la Perf ! 💪</h1>", unsafe_allow_html=True)

# Distance
distance = st.number_input("Distance totale", min_value=0.0, value=5.0, step=0.1)
unite = st.selectbox("Unité", ["km", "m"])
distance_m = distance*1000 if unite=="km" else distance

# Onglets
tab1, tab2 = st.tabs(["⏱️ Temps visé", "🏃 Allure visée"])

with tab1:  # Temps visé
    col1, col2 = st.columns(2)
    temps_min = col1.number_input("Minutes", min_value=0, value=25, key="t_min")
    temps_sec = col2.number_input("Secondes", min_value=0, max_value=59, value=0, key="t_sec")
    if st.button("Calculer allure", key="btn_temps"):
        temps_total_s = temps_min*60 + temps_sec
        if temps_total_s > 0 and distance_m > 0:
            allure_s = (temps_total_s / distance_m) * 1000
            st.success(f"Allure visée : {int(allure_s//60)} min {int(allure_s%60)} sec / km")

with tab2:  # Allure visée
    col3, col4 = st.columns(2)
    allure_min = col3.number_input("Minutes", min_value=0, value=5, key="a_min")
    allure_sec = col4.number_input("Secondes", min_value=0, max_value=59, value=0, key="a_sec")
    if st.button("Calculer temps", key="btn_allure"):
        allure_s = allure_min*60 + allure_sec
        if allure_s > 0 and distance_m > 0:
            temps_total_s = (distance_m / 1000) * allure_s
            st.success(f"Temps visé : {int(temps_total_s//60)} min {int(temps_total_s%60)} sec")

# --- Onglets Intervalle ---
tab3, tab4 = st.tabs(["📏 Intervalle par distance", "⏳ Intervalle par temps"])

# --- Intervalle par distance ---
with tab3:
    intervalle_m = st.number_input("Intervalle distance (m)", min_value=1, value=1000, step=100, key="intervalle_distance_tab3")
    sorties_distance = []
    if intervalle_m > 0 and 'allure_s' in locals() and allure_s > 0:
        vitesse = 1000 / allure_s
        nb_intervalles = int(distance_m // intervalle_m)
        for i in range(1, nb_intervalles + 1):
            m = i * intervalle_m
            t_s = m / vitesse
            sorties_distance.append(f"{int(m)} m → {int(t_s//60):02d}:{int(t_s%60):02d} sec")
        if st.button("🏃 En route vers la perf ! (Distance)"):
            st.subheader("Résultats Intervalle Distance :")
            for s in sorties_distance:
                st.write(s)

# --- Intervalle par temps ---
with tab4:
    col5, col6 = st.columns(2)
    intervalle_min = col5.number_input("Minutes", min_value=0, value=1, step=1, key="intervalle_temps_min_tab4")
    intervalle_sec = col6.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="intervalle_temps_sec_tab4")
    intervalle_s = intervalle_min*60 + intervalle_sec
    sorties_temps = []
    if intervalle_s > 0 and 'temps_total_s' in locals() and temps_total_s > 0:
        vitesse = 1000 / allure_s
        nb_intervalles = int(temps_total_s // intervalle_s)
        for i in range(1, nb_intervalles + 1):
            t = i * intervalle_s
            m = t * vitesse
            sorties_temps.append(f"{int(t//60):02d}:{int(t%60):02d} → {int(m)} m")
        if st.button("🏃 En route vers la perf ! (Temps)"):
            st.subheader("Résultats Intervalle Temps :")
            for s in sorties_temps:
                st.write(s)

