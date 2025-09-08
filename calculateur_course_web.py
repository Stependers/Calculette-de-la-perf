
import streamlit as st

st.set_page_config(page_title="Calculette de la Perf !", layout="centered")
st.title("💪 Calculette de la Perf ! 💪")

# --- Distance totale ---
st.subheader("Distance totale")
distance = st.number_input("Entrez la distance :", min_value=0.0, value=5.0, step=0.1, key="distance_total")
unite = st.radio("Unité :", ["km", "m"], key="unite")
distance_m = distance * 1000 if unite == "km" else distance

# --- Temps total ---
st.subheader("Temps total")
col1, col2 = st.columns(2)
temps_min = col1.number_input("Minutes", min_value=0, value=0, step=1, key="temps_total_min")
temps_sec = col2.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="temps_total_sec")

# --- Allure ---
st.subheader("Allure (min/km)")
col3, col4 = st.columns(2)
allure_min = col3.number_input("Minutes", min_value=0, value=0, step=1, key="allure_min")
allure_sec = col4.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="allure_sec")

# --- Calcul automatique ---
# Convertir en secondes
temps_total_s = temps_min * 60 + temps_sec
allure_s = allure_min * 60 + allure_sec

# Si temps total > 0, calcul allure
if temps_total_s > 0 and allure_s == 0:
    allure_s = (temps_total_s / distance_m) * 1000
    allure_min = int(allure_s // 60)
    allure_sec = int(allure_s % 60)
# Si allure > 0, calcul temps total
elif allure_s > 0 and temps_total_s == 0:
    temps_total_s = (distance_m / 1000) * allure_s
    temps_min = int(temps_total_s // 60)
    temps_sec = int(temps_total_s % 60)
# Sinon si les deux sont remplis, on garde les valeurs saisies

# --- Afficher les valeurs calculées ---
st.write(f"**Allure :** {allure_min} min {allure_sec} sec / km")
st.write(f"**Temps total :** {temps_min} min {temps_sec} sec")

# --- Onglets pour intervalle ---
tab = st.radio("Type d'intervalle :", ["Distance", "Temps"], key="onglet_intervalle")
sorties = []

if tab == "Distance":
    intervalle_m = st.number_input("Intervalle distance (m)", min_value=1, value=1000, step=100, key="intervalle_distance")
    if intervalle_m > 0:
        nb_intervalles = int(distance_m // intervalle_m)
        vitesse = 1000 / allure_s
        for i in range(1, nb_intervalles + 1):
            m = i * intervalle_m
            t_s = m / vitesse
            minutes = int(t_s // 60)
            secondes = int(t_s % 60)
            sorties.append(f"{int(m)} m → {minutes:02d}:{secondes:02d}")

else:  # Temps
    col5, col6 = st.columns(2)
    intervalle_min = col5.number_input("Minutes", min_value=0, value=1, step=1, key="intervalle_temps_min")
    intervalle_sec = col6.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="intervalle_temps_sec")
    intervalle_s = intervalle_min * 60 + intervalle_sec
    if intervalle_s > 0:
        nb_intervalles = int(temps_total_s // intervalle_s)
        vitesse = 1000 / allure_s
        for i in range(1, nb_intervalles + 1):
            t = i * intervalle_s
            m = t * vitesse
            minutes = int(t // 60)
            secondes = int(t % 60)
            sorties.append(f"{minutes:02d}:{secondes:02d} → {int(m)} m")

# --- Bouton calcul ---
if st.button("🏃 En route vers la perf !", key="bouton_calcul"):
    if sorties:
        st.subheader("Résultats :")
        for s in sorties:
            st.write(s)
    else:
        st.warning("⚠ Aucun intervalle calculé. Vérifiez vos entrées.")
