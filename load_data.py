from database import read_table

def load_clients():
    return read_table("clients")

def load_factures():
    return read_table("factures")

def load_paiements():
    return read_table("paiements")

def load_clients_data():
    return read_table("historique")

def get_unpaid_factures():
    factures = load_factures()
    clients = load_clients()
    merged = factures.merge(clients, left_on='client_id', right_on='id', suffixes=('_facture', '_client'))
    return merged[merged['status'] == 'unpaid']
