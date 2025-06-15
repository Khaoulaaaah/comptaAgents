from sqlalchemy import create_engine
import pandas as pd

# Connexion SQLite
engine = create_engine('sqlite:///sample_data/database.db', echo=False)

def read_table(table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, con=engine)

def write_table(df, table_name):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
