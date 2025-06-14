import streamlit as st
import pandas as pd
from load_data import load_clients, load_factures, load_paiements, get_unpaid_factures, load_clients_data
from reminder_agent import generate_reminders
from risk_scoring_agent import classify_risk, evaluate_risk
from payment_tracker import update_payment_status, get_client_payment_history
from chat_agent import chat_with_agent


def dashboard():
    st.header("📊 Tableau de bord global")

    factures = load_factures()
    clients = load_clients()
    historique = load_clients_data()

    # Calcul du taux global d'impayés
    total_factures = len(factures)
    impayees = len(factures[factures["status"] == "unpaid"])
    taux_impayes = (impayees / total_factures) * 100 if total_factures > 0 else 0

    st.metric("Taux global d'impayés", f"{taux_impayes:.2f}%")
    st.write(f"Total factures : {total_factures}")
    st.write(f"Factures impayées : {impayees}")

    # Top 5 clients à risque (basé sur pourcentage de factures impayées)
    historique["niveau_risque"] = historique["pourcentage_de_factures_impayées"].apply(classify_risk)
    top_risque = historique.sort_values(by="pourcentage_de_factures_impayées", ascending=False).head(5)
    
    st.subheader("Top 5 clients à risque")
    st.table(top_risque[["name", "pourcentage_de_factures_impayées", "niveau_risque"]])

    # Répartition du risque (nombre de clients par niveau de risque)
    repartition = historique["niveau_risque"].value_counts()
    st.subheader("Répartition des clients par niveau de risque")
    st.bar_chart(repartition)

# Ensuite dans app.py tu ajoutes cette option au menu
page = st.sidebar.radio("📌 Sélectionner un service :", [
    "📊 Dashboard global",
    "📋 Factures non réglées",
    "⚠️ Analyse du risque client",
    "💰 Paiements en temps réel",
    "🤖 Chat IA"
])

if page == "📊 Dashboard global":
    dashboard()





# --- PAGE 1: FACTURES NON RÉGLÉES ---
if page == "📋 Factures non réglées":
    st.header("📋 Factures impayées")
    factures = get_unpaid_factures()
    st.dataframe(factures[["name", "amount", "date_due"]])

    if st.button("📨 Générer les relances"):
        st.write("📧 Emails de relance générés :")
        from langchain_ollama import OllamaLLM
        from langchain_core.prompts import PromptTemplate
        from langchain_core.runnables import RunnableSequence

        llm = OllamaLLM(model="llama3")
        prompt_template = PromptTemplate(
            input_variables=["name", "amount", "date_due"],
            template="""
            Rédige un email de relance poli et professionnel en français
            à un client nommé {name} concernant une facture impayée de {amount}€ échue le {date_due}.
            """
        )
        chain: RunnableSequence = prompt_template | llm

        for _, row in factures.iterrows():
            output = chain.invoke({
                "name": row["name"],
                "amount": row["amount"],
                "date_due": row["date_due"]
            })
            st.markdown(f"---\n**{row['name']}**\n\n{output}")

# --- PAGE 2: RISQUE CLIENT ---
elif page == "⚠️ Analyse du risque client":
    st.header("⚠️ Évaluation du risque client")
    data = pd.read_csv("sample_data/historique_paiement/historique.csv")
    clients = load_clients()
    noms = clients["name"].tolist()
    nom_selectionne = st.selectbox("Choisissez un client", noms)

    if nom_selectionne:
        client_data = data[data["name"] == nom_selectionne].iloc[0]
        niveau = classify_risk(client_data["pourcentage_de_factures_impayées"])

        from langchain_ollama import OllamaLLM
        from langchain_core.prompts import PromptTemplate
        from langchain_core.runnables import RunnableSequence

        llm = OllamaLLM(model="llama3")
        prompt_template = PromptTemplate(
            input_variables=[
                "name", "rappels", "retards", "impayees",
                "total", "pourcentage", "niveau"
            ],
            template="""
            Le client {name} a reçu {rappels} rappels de paiement, a eu {retards} retards de paiement,
            avec {impayees} factures impayées sur un total de {total}, soit {pourcentage}% de factures impayées.
            Le niveau de risque calculé est : {niveau}.
            Rédige une explication en français, claire et professionnelle, pour justifier ce niveau de risque.
            """
        )
        chain = prompt_template | llm
        output = chain.invoke({
            "name": client_data["name"],
            "rappels": client_data["nombre_de_rappels_de_paiement"],
            "retards": client_data["nombre_de_retards_de_paiement"],
            "impayees": client_data["nombre_de_facture_impayées"],
            "total": client_data["nombre_total_de_factures"],
            "pourcentage": client_data["pourcentage_de_factures_impayées"],
            "niveau": niveau
        })
        st.markdown(f"**Niveau de risque :** {niveau}")
        st.write(output)

# --- PAGE 3: SUIVI DES PAIEMENTS ---
elif page == "💰 Paiements en temps réel":
    st.header("💰 Paiements enregistrés")
    paiements = load_paiements()
    st.dataframe(paiements)

    st.subheader("➕ Enregistrer un nouveau paiement")
    clients = load_clients()
    client_names = clients["name"].tolist()
    selected_client_name = st.selectbox("Choisir un client", client_names)

    if selected_client_name:
        selected_client_id = clients[clients["name"] == selected_client_name]["id"].values[0]
        factures = load_factures()
        client_factures = factures[(factures["client_id"] == selected_client_id) & (factures["status"] == "unpaid")]

        if not client_factures.empty:
            facture_ids = client_factures["id"].astype(str).tolist()
            selected_facture_id = st.selectbox("Choisir une facture à régler", facture_ids)
            selected_facture = client_factures[client_factures["id"] == int(selected_facture_id)].iloc[0]
            montant = selected_facture["amount"]
            st.markdown(f"**Montant à régler :** {montant} €")

            date_paiement = st.date_input("Date du paiement")

            if st.button("✅ Enregistrer le paiement"):
                update_payment_status(str(selected_facture_id), montant, str(date_paiement))
                st.success("Paiement enregistré et suivi mis à jour.")
                st.rerun()
        else:
            st.info("✅ Ce client n’a aucune facture impayée.")

    st.subheader("📂 Historique des paiements par client")
    client_names = clients["name"].tolist()
    selected_name = st.selectbox("Afficher l’historique pour un client", client_names, key="history_select")
    if selected_name:
        selected_id = clients[clients["name"] == selected_name]["id"].values[0]
        historique = get_client_payment_history(selected_id)
        st.dataframe(historique)


# --- PAGE 4: CHATBOT ---
elif page == "🤖 Chat IA":
    st.header("🤖 Assistant IA comptable")
    user_input = st.text_area("Posez votre question ici:")
    if st.button("Envoyer"):
        if user_input.strip() != "":
            response = chat_with_agent(user_input)
            st.markdown(f"**Réponse :**\n{response}")
