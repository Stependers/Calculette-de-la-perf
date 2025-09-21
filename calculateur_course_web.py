# =========================
# Onglet 1 : Calcul d'intervalles
# =========================
with onglets_outils[0]:
    st.subheader("📏 Calcul d'intervalles")

    # --- Choix distance prédéfinie ---
    choix_distance = st.radio(
        "Choisir une distance prédéfinie :",
        ("Saisie manuelle", "5 km", "10 km", "Semi-marathon (21.1 km)", "Marathon (42.195 km)"),
        horizontal=True
    )

    # --- Distance en km en fonction du choix ---
    if choix_distance == "5 km":
        distance_km = 5.0
    elif choix_distance == "10 km":
        distance_km = 10.0
    elif choix_distance == "Semi-marathon (21.1 km)":
        distance_km = 21.1
    elif choix_distance == "Marathon (42.195 km)":
        distance_km = 42.195
    else:
        distance_km = st.number_input("Distance totale (km)", min_value=0.0, value=5.0, step=0.1)

    distance_m = distance_km * 1000

    # --- Suite de ton code ---
    mode_calc = st.radio("Sélectionner la méthode", ["Temps visé", "Allure visée"], horizontal=True)
    allure_s = 0
    temps_total_s = 0

    if mode_calc == "Temps visé":
        col_h, col_m, col_s = st.columns(3)
        temps_h = col_h.number_input("Heures", min_value=0, value=0, step=1, key="t_h")
        temps_min = col_m.number_input("Minutes", min_value=0, value=25, step=1, key="t_min")
        temps_sec = col_s.number_input("Secondes", min_value=0, max_value=59, value=0, step=1, key="t_sec")
        temps_total_s = temps_h*3600 + temps_min*60 + temps_sec
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

    # ici ton code d’intervalles …
