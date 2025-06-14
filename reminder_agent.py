from load_data import get_unpaid_factures
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_ollama import OllamaLLM

def generate_reminders():
    factures = get_unpaid_factures()
    llm = OllamaLLM(model="llama3")

    prompt_template = PromptTemplate(
        input_variables=["name", "amount", "date_due"],
        template="""
        Rédige un email de relance court, poli et professionnel en français
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
        print(f"--- Relance pour {row['name']} ---\n{output}\n")

if __name__ == "__main__":
    generate_reminders()
