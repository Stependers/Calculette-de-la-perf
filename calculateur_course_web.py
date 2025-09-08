import streamlit as st

st.set_page_config(page_title="Calculette de la Perf !", layout="centered")

# --- Titre centré ---
st.markdown("<h1 style='text-align: center;'>💪 Calculette de la Perf ! 💪</h1>", unsafe_allow_html=True)

# --- Distance ---
st.subheader("Distance totale")
col_dist1, col_dist2 = st.columns([2,1])
distance = col_dist1.number_input("Entrez la distance :", min_value=0.0, value=5.0, step=0.1)
unite = col_dist2.selectbox("Unité :", ["km", "m"])
distance_m = distance * 1000 if unite == "km" else distance

# --- Onglets simulés pour mode de calcul ---
st.markdown("### Mode de calcul")
mode_calc = st.radio(
    "",
    ["Temps visé", "Allure visée"],
    index=0,
    horizontal=True
)

# --- CSS pour rendre les radios comme des onglets ---
st.markdown("""
<style>
[data-baseweb="radio"] > div {
    display: flex;
}
[data-baseweb="radio"] label {
    background-color: #f0f0f0;
    padding: 8px 16px;
    margin-right: 2px;
    border-radius: 8px 8px 0 0;
    font-weight: bold;
    cursor: pointer;
}
[data-baseweb="radio"] input:checked + label {
    background-color: #4CAF50 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# --- Calcul allure/temps ---
allure_s = 0
temps_total_s = 0

if mode_calc == "Temps visé":
    col1, col2 = st.columns(2)
    temps_min = col1.number_input("Minutes", min_value=0, value=25, step=1, key="t_min")
    temps_sec = col2.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="t_sec")
    temps_total_s = temps_min*60 + temps_sec
    if distance_m > 0 and temps_total_s > 0:
        allure_s = (temps_total_s / distance_m) * 1000
        st.markdown(f"**Allure :** {int(allure_s//60)} min {int(allure_s%60)} sec / km")
else:
    col3, col4 = st.columns(2)
    allure_min = col3.number_input("Minutes", min_value=0, value=5, step=1, key="a_min")
    allure_sec = col4.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="a_sec")
    allure_s = allure_min*60 + allure_sec
    if distance_m > 0 and allure_s > 0:
        temps_total_s = (distance_m / 1000) * allure_s
        st.markdown(f"**Temps visé :** {int(temps_total_s//60)} min {int(temps_total_s%60)} sec")

# --- Onglets simulés pour intervalle ---
st.markdown("### Intervalle")
intervalle_type = st.radio("", ["Distance", "Temps"], index=0, horizontal=True)

intervalle_m = intervalle_s = 0
if intervalle_type == "Distance":
    intervalle_m = st.number_input("Intervalle distance (m)", min_value=1, value=1000, step=100)
else:
    col5, col6 = st.columns(2)
    intervalle_min = col5.number_input("Minutes", min_value=0, value=1, step=1)
    intervalle_sec = col6.number_input("Secondes", min_value=0, max_value=59, value=0, step=1)
    intervalle_s = intervalle_min*60 + intervalle_sec

# --- Bouton central ---
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

if st.button("🏃 En route pour la perf !"):
    if allure_s <= 0:
        st.warning("⚠ Veuillez saisir un temps visé ou une allure visée valide.")
    else:
        vitesse = 1000 / allure_s
        st.subheader("Résultats :")

        if intervalle_m > 0:
            nb = int(distance_m // intervalle_m)
            st.markdown(f"**Intervalle distance : {intervalle_m} m**")
            for i in range(1, nb+1):
                m = i * intervalle_m
                t_s = m / vitesse
                st.write(f"{int(m)} m → {int(t_s//60):02d}:{int(t_s%60):02d} sec")
        elif intervalle_s > 0:
            nb = int(temps_total_s // intervalle_s)
            st.markdown(f"**Intervalle temps : {intervalle_min} min {intervalle_sec} sec**")
            for i in range(1, nb+1):
                t = i * intervalle_s
                m = t * vitesse
                st.write(f"{int(t//60):02d}:{int(t%60):02d} → {int(m)} m")
