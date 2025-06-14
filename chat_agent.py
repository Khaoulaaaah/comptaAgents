from langchain_ollama import OllamaLLM
from load_data import load_clients, load_factures, load_paiements, load_clients_data

llm = OllamaLLM(model="llama3")

def summarize_data():
    clients = load_clients()
    factures = load_factures()
    paiements = load_paiements()
    historique = load_clients_data()

    client_summary = "\n".join([
        f"- {row['id']} | {row['name']} | {row['email']}" for _, row in clients.iterrows()
    ])

    facture_summary = "\n".join([
        f"- Facture {row['id']} | Client {row['client_id']} | Montant {row['amount']}€ | Échéance {row['date_due']} | Statut {row['status']}"
        for _, row in factures.iterrows()
    ])

    paiement_summary = "\n".join([
        f"- Paiement {row['id']} | Facture {row['facture_id']} | Montant {row['amount']}€ | Date {row['date']}"
        for _, row in paiements.iterrows()
    ])

    risque_summary = "\n".join([
        f"- {row['name']} : {row['nombre_de_facture_impayées']} impayées sur {row['nombre_total_de_factures']} ({row['pourcentage_de_factures_impayées']}%)"
        for _, row in historique.iterrows()
    ])

    return client_summary, facture_summary, paiement_summary, risque_summary


def chat_with_agent(message: str) -> str:
    clients, factures, paiements, risques = summarize_data()

    prompt = f"""
Tu es un assistant comptable intelligent. Utilise les données suivantes pour répondre aux questions posées.

📋 Clients :
{clients}

📄 Factures :
{factures}

💰 Paiements :
{paiements}

📊 Risques :
{risques}

Maintenant, réponds à cette question de manière claire, concise et professionnelle :
\"{message}\"
"""
    return llm.invoke(prompt)
