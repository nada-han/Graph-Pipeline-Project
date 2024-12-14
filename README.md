# **Projet Data Engineering : Traitement de graphe**

## **Description**
Ce projet implémente un pipeline de data engineering pour traiter un dataset de graphe. Il utilise les technologies suivantes :
- **Apache Kafka** : Pour la diffusion et la consommation des données.
- **Apache Spark GraphX** : Pour le traitement et l'analyse des graphes.
- **Neo4j** : Pour le stockage des résultats du traitement.
- **Streamlit** : Pour visualiser les résultats de manière interactive.
- **Apache Airflow** : Pour orchestrer l'ensemble du pipeline.

## **Architecture**
1. **Docker** :
   - L'ensemble des services nécessaires (Kafka, Spark, Neo4j, Airflow) est conteneurisé avec Docker Compose pour simplifier le déploiement.
   - Chaque service s'exécute dans son propre conteneur, assurant l'isolation et la portabilité.
     
2. **Kafka** :
   - Un producteur diffuse les données depuis un fichier Parquet dans un topic Kafka.
   - Un consommateur Kafka consomme ces données.

3. **Spark GraphX** :
   - Les données sont récupérées depuis Kafka et traitées dans Spark GraphX.
   - Les algorithmes de traitement sont : PageRank, Connected Components, Triangle Counting.

4. **Neo4j** :
   - Les résultats des traitements sont stockés dans Neo4j via des requêtes Cypher.

5. **Streamlit** :
   - Une interface interactive permet de visualiser les résultats depuis Neo4j.

6. **Airflow** :
   - Orchestration complète du pipeline pour une exécution automatisée.
  
![workflow](https://github.com/user-attachments/assets/1b8ad346-f873-4b2f-b009-73ae2ab80823)

## **Prérequis**
- Docker et Docker Compose
- Python 3.8+
- Bibliothèques Python :
  - `pandas`, `kafka-python`, `pyspark`


