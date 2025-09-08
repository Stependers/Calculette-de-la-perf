import streamlit as st

st.set_page_config(page_title="Calculette de la Perf !", layout="centered")

st.markdown("<h1 style='text-align: center;'>💪 Calculette de la Perf ! 💪</h1>", unsafe_allow_html=True)

# --- Distance ---
distance = st.number_input("Distance totale", min_value=0.0, value=5.0, step=0.1)
unite = st.selectbox("Unité :", ["km", "m"])
distance_m = distance * 1000 if unite=="km" else distance

# --- Onglets Temps visé / Allure visée ---
tab1, tab2 = st.tabs(["⏱️ Temps visé", "🏃 Allure visée (min/km)"])

# Variables initiales
temps_total_s = 0
allure_s = 0

# Onglet Temps visé
with tab1:
    # On "réinitialise" les variables de l'autre onglet
    allure_s = 0
    col1, col2 = st.columns(2)
    temps_min = col1.number_input("Minutes", min_value=0, value=25, step=1, key="temps_vise_min")
    temps_sec = col2.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="temps_vise_sec")
    temps_total_s = temps_min*60 + temps_sec
    if temps_total_s > 0 and distance_m > 0:
        allure_s = (temps_total_s / distance_m) * 1000
        st.markdown(f"**Allure :** {int(allure_s//60)} min {int(allure_s%60)} sec / km")

# Onglet Allure visée
with tab2:
    # On "réinitialise" les variables de l'autre onglet
    temps_total_s = 0
    col3, col4 = st.columns(2)
    allure_min = col3.number_input("Minutes", min_value=0, value=5, step=1, key="allure_visee_min")
    allure_sec = col4.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="allure_visee_sec")
    allure_s = allure_min*60 + allure_sec
    if allure_s > 0 and distance_m > 0:
        temps_total_s = (distance_m / 1000) * allure_s
        st.markdown(f"**Temps total :** {int(temps_total_s//60)} min {int(temps_total_s%60)} sec")
