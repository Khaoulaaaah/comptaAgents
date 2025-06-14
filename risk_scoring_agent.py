from load_data import load_clients_data
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_ollama import OllamaLLM

def classify_risk(pourcentage):
    if pourcentage == 0:
        return "Très faible"
    elif pourcentage <= 15:
        return "Faible"
    elif pourcentage <= 35:
        return "Modéré"
    elif pourcentage <= 50:
        return "Élevé"
    else:
        return "Critique"

def evaluate_risk():
    data = load_clients_data()
    
    llm = OllamaLLM(model="llama3")
    
    prompt_template = PromptTemplate(
        input_variables=[
            "name", 
            "rappels", 
            "retards", 
            "impayees", 
            "total", 
            "pourcentage", 
            "niveau"
        ],
        template="""
        Le client {name} a reçu {rappels} rappels de paiement, a eu {retards} retards de paiement,
        avec {impayees} factures impayées sur un total de {total}, soit {pourcentage}% de factures impayées.
        Le niveau de risque calculé est : {niveau}.
        Rédige une explication en français, claire et professionnelle, pour justifier ce niveau de risque.
        """
    )
    
    chain: RunnableSequence = prompt_template | llm

    for _, row in data.iterrows():
        niveau = classify_risk(row["pourcentage_de_factures_impayées"])
        
        explanation = chain.invoke({
            "name": row["name"],
            "rappels": row["nombre_de_rappels_de_paiement"],
            "retards": row["nombre_de_retards_de_paiement"],
            "impayees": row["nombre_de_facture_impayées"],
            "total": row["nombre_total_de_factures"],
            "pourcentage": row["pourcentage_de_factures_impayées"],
            "niveau": niveau
        })

        print(f"Client : {row['name']}")
        print(f" - Niveau de risque : {niveau}")
        print(f" - Explication : {explanation}")
        print("-" * 60)

if __name__ == "__main__":
    evaluate_risk()
