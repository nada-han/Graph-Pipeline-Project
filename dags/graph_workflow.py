from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 1),
    'retries': 1,
}

# Création du DAG
dag = DAG(
    'graph_workflow',
    default_args=default_args,
    schedule_interval='*/15 * * * *',  # Toutes les 15 minutes
)

# Étape 1 : Récupérer des données depuis FastAPI
fetch_data = BashOperator(
    task_id='fetch_data',
    bash_command='curl -X GET http://fastapi_kafka:8000/graph',
    dag=dag,
)

# Étape 2 : Exécuter Spark avec GraphX et stocker les résultats dans Neo4j
run_spark_store_neo4j = BashOperator(
    task_id='run_spark_store_neo4j',
    bash_command=(
        'docker exec spark-master2 bash -c '
        '"spark-submit --class GraphXApp --master local[*] '
        '--packages com.typesafe.play:play-json_2.12:2.9.4,'
        'org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.0,'
        'org.neo4j:neo4j-connector-apache-spark_2.12:5.3.2_for_spark_3 '
        '/app/spark/GraphX.jar"'
    ),
    dag=dag,
)

# Définir les dépendances des tâches
fetch_data >> run_spark_store_neo4j
