# Plan Structuré pour la Veille Technologique et RAG (avec Phi3)
Plan pour mettre en place un système de veille technologique récurrente, qui collecte des documents périodiquement sur un sujet donné, les intègre dans une base de données vectorielle, et permet de les interroger via un système RAG (Retrieval-Augmented Generation) utilisant le modèle Phi3.

## 1. Collecte Récurrente de Données (Veille Technologique)
Objectif :
Mettre en place un processus automatisé pour collecter régulièrement des articles, des papiers de recherche, ou des actualités sur un sujet spécifique (par exemple, Automatic Speech Recognition) depuis des sources fiables comme Google Scholar, ArXiv, ou d'autres API.

**Étapes :**
Définir les Sources :

Google Scholar pour les articles académiques.
ArXiv pour les prépublications.
D'autres sources pertinentes comme PubMed, IEEE, ou Springer.
Planifier des Collectes Récurrentes :

Utiliser un scheduler (par exemple, cron ou Airflow) pour lancer périodiquement la collecte de documents (exemple : une fois par semaine).
Extraire les Informations Nécessaires :

Titre, résumé (abstract), lien vers l'article complet, auteurs, et mots-clés.
Filtrage et Préprocessing :

Filtrer les articles pour ne garder que ceux pertinents à ASR (par exemple, avec des mots-clés spécifiques).
Nettoyer les données textuelles (supprimer les caractères inutiles, homogénéiser le texte, etc.).
Stockage Initial :

Stocker les données collectées dans une base structurée (par exemple, au format JSON ou dans une base relationnelle comme PostgreSQL).

## 2. Intégration dans une Base Vectorielle
Objectif :
Transformer les documents collectés en vecteurs d'embeddings et les intégrer dans une base vectorielle pour permettre une recherche efficace.

Étapes :
Générer des Embeddings :

Utiliser un modèle comme SentenceTransformers (all-mpnet-base-v2 ou un modèle spécialisé dans les articles scientifiques).
Transformer chaque résumé ou document en vecteurs d'embeddings.
Stocker dans une Base Vectorielle :

Utiliser une base vectorielle comme ChromaDB, FAISS, ou Pinecone pour stocker les embeddings et leurs métadonnées (titre, résumé, lien, etc.).
Gestion des Mises à Jour :

Lors de chaque collecte récurrente, vérifier les articles déjà présents (via leurs DOI, titres ou hashes) pour éviter les doublons.
Mettre à jour la base vectorielle avec les nouveaux articles.

## 3. Conception du Système RAG
Objectif :
Construire un système de RAG (Retrieval-Augmented Generation) permettant d’interroger la base vectorielle pour répondre aux questions en s’appuyant sur les documents collectés.

Étapes :
Recherche dans la Base Vectorielle :

Utiliser LangChain ou une bibliothèque similaire pour interroger la base vectorielle.
Récupérer les documents les plus pertinents en fonction de la requête de l'utilisateur.
Construction d’un Contexte :

Construire un contexte textuel en combinant les résumés ou les parties pertinentes des documents récupérés.
Limiter la taille du contexte pour rester dans les limites du modèle (ex. : 4 000 tokens).
Génération de Réponse :

Construire un prompt comprenant la requête utilisateur et le contexte extrait.
Appeler le modèle Phi3 (via Ollama) pour générer une réponse basée sur ce prompt.
Validation de la Réponse :

Optionnel : valider ou enrichir la réponse générée par Phi3 à l’aide des métadonnées associées aux documents.

## 4. Interface Utilisateur
Objectif :
Offrir une interface interactive pour :

Visualiser les articles collectés.
Poser des questions à la base de données.
Obtenir des réponses pertinentes basées sur le système RAG.
Étapes :
Interface Streamlit :

Un champ pour entrer le sujet de la veille technologique.
Un bouton pour déclencher la collecte manuelle des articles.
Un champ pour poser des questions à la base.
Visualisation des Documents :

Afficher les titres des articles récupérés, les résumés, et les liens vers les documents complets.
Affichage des Réponses :

Afficher les réponses générées par Phi3.
Afficher les documents utilisés pour répondre (métadonnées ou extraits).

## 5. Automatisation et Maintenance
**Objectif** :
Garantir que le système fonctionne de manière autonome et est facile à maintenir.

**Étapes** :
Planification des Collectes :

Automatiser les collectes avec un scheduler comme cron ou Airflow.
**Monitoring** :

Mettre en place des logs pour surveiller les collectes et identifier d’éventuelles erreurs (exemple : échec d'accès à Google Scholar).
**Nettoyage Régulier** :

Supprimer les articles obsolètes ou non pertinents de la base vectorielle pour garder un système optimisé.


download chromedriver
```
    !wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
```
After that
```
!unzip chromedriver_linux64.zip
!sudo mv chromedriver /usr/bin/chromedriver
!sudo chown root:root /usr/bin/chromedriver
!sudo chmod +x /usr/bin/chromedriver
```

### !pip install pdfplumber