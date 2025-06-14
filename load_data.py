
import pandas as pd
import os

BASE_PATH = os.path.join(os.path.dirname(__file__), 'sample_data')

def load_clients():
    return pd.read_csv(os.path.join(BASE_PATH, 'clients', 'clients.csv'))

def load_factures():
    return pd.read_csv(os.path.join(BASE_PATH, 'factures', 'factures.csv'))

def load_paiements():
    return pd.read_csv(os.path.join(BASE_PATH, 'paiements', 'paiements.csv'))

def load_clients_data():
    return pd.read_csv(os.path.join(BASE_PATH, 'historique_paiement', 'historique.csv'))

def get_unpaid_factures():
    factures = load_factures()
    clients = load_clients()
    merged = factures.merge(clients, left_on='client_id', right_on='id', suffixes=('_facture', '_client'))
    return merged[merged['status'] == 'unpaid']
