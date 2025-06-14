# compta
🧾 Système d’Agents IA pour la Comptabilité et le Suivi Client

Ce système intelligent regroupe plusieurs agents autonomes, interconnectés via une interface Streamlit conviviale, pour assister les comptables dans la gestion des factures, le suivi des paiements, et l'analyse du risque client. Il repose sur des données CSV simulant un environnement de gestion client, et utilise un LLM (llama3 via Ollama) pour générer des relances automatiques, analyser les risques, et répondre aux questions via un chatbot.
🔧 Modules et fonctionnalités :

    💼 Relance des factures impayées

        Affiche les clients ayant des factures non réglées.

        Génère des emails de relance professionnels automatiquement à partir des données.

    ⚠️ Analyse du risque client

        Calcule un score de risque basé sur l’historique de paiement (retards, impayés, rappels).

        Génère une explication justifiée de chaque niveau de risque.

    💰 Paiements en temps réel

        Permet d'enregistrer de nouveaux paiements via l’interface.

        Met à jour les fichiers paiements.csv, factures.csv et historique.csv.

        Affiche l’historique des paiements par client.

    🤖 Chatbot intelligent

        Répond aux questions sur les paiements, clients, factures, ou analyse de risque.

        A accès aux données des clients pour répondre de façon contextualisée.

🛠️ Technologies utilisées :

    LangChain + Ollama (LLM llama3) : génération de textes explicatifs ou de relance.

    Pandas : traitement de données à partir de fichiers CSV.

    Streamlit : interface web interactive multi-page.

    Modularité par agents : chaque agent (relance, risque, paiement, chatbot) est un module indépendant.
