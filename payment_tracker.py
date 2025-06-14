import pandas as pd
from datetime import datetime

# Chemins des fichiers CSV
FACTURES_PATH = "sample_data/factures/factures.csv"
PAIEMENTS_PATH = "sample_data/paiements/paiements.csv"
HISTORIQUE_PATH = "sample_data/historique_paiement/historique.csv"

def update_payment_status(facture_id, amount, date_str):
    # Charger les données
    factures = pd.read_csv(FACTURES_PATH)
    paiements = pd.read_csv(PAIEMENTS_PATH)
    historique = pd.read_csv(HISTORIQUE_PATH)

    facture_id = int(facture_id)
    amount = float(amount)
    date = pd.to_datetime(date_str).strftime("%Y-%m-%d")

    # Vérifier si la facture existe
    facture_index = factures[factures["id"] == facture_id].index
    if facture_index.empty:
        print("❌ Facture introuvable.")
        return

    idx = facture_index[0]
    facture = factures.loc[idx]

    # Ajouter le paiement au fichier paiements.csv
    new_id = paiements["id"].max() + 1 if not paiements.empty else 1
    new_payment = {
        "id": new_id,
        "facture_id": facture_id,
        "amount": amount,
        "date": date
    }
    paiements = pd.concat([paiements, pd.DataFrame([new_payment])], ignore_index=True)

    # Mettre à jour le statut de la facture
    if facture["status"] == "unpaid" and amount >= facture["amount"]:
        factures.at[idx, "status"] = "paid"

        # Mettre à jour l'historique du client
        client_id = facture["client_id"]
        hist_index = historique[historique["client_id"] == client_id].index
        if not hist_index.empty:
            hidx = hist_index[0]
            historique.at[hidx, "nombre_de_facture_impayées"] -= 1
            total = historique.at[hidx, "nombre_total_de_factures"]
            impayees = historique.at[hidx, "nombre_de_facture_impayées"]
            pourcentage = round((impayees / total) * 100, 2)
            historique.at[hidx, "pourcentage_de_factures_impayées"] = pourcentage

    # Sauvegarder les fichiers
    paiements.to_csv(PAIEMENTS_PATH, index=False)
    factures.to_csv(FACTURES_PATH, index=False)
    historique.to_csv(HISTORIQUE_PATH, index=False)

    print("✅ Paiement ajouté et suivi mis à jour.")

def get_client_payment_history(client_id):
    client_id = int(client_id)
    factures = pd.read_csv(FACTURES_PATH)
    paiements = pd.read_csv(PAIEMENTS_PATH)

    # Obtenir les factures du client
    client_factures = factures[factures["client_id"] == client_id]
    facture_ids = client_factures["id"].tolist()

    # Filtrer les paiements liés aux factures de ce client
    client_paiements = paiements[paiements["facture_id"].isin(facture_ids)]

    return client_paiements
