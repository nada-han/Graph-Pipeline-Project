from fastapi import FastAPI
from kafka import KafkaProducer
import pandas as pd
import numpy as np
import json
from kafka.errors import KafkaError

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    acks='all',
    retries=5,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON serialization
)

@app.get("/graph")
async def send_graph_data():
    try:
        # Lecture du fichier Parquet
        df = pd.read_parquet("proteins.parquet")
        
        # Conversion des colonnes contenant des objets numpy en types natifs Python
        for col in df.columns:
            if df[col].dtype == object or isinstance(df[col].iloc[0], np.ndarray):
                df[col] = df[col].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)

        # Fonction de sérialisation pour convertir les ndarrays en listes avant envoi
        def serialize_record(record):
            def convert(value):
                # Si la valeur est un ndarray, la convertir en liste
                if isinstance(value, np.ndarray):
                    return value.tolist()
                # Si la valeur est une liste contenant des ndarray, convertir chaque élément
                elif isinstance(value, list):
                    return [convert(item) if isinstance(item, np.ndarray) else item for item in value]
                return value

            return {key: convert(value) for key, value in record.items()}

        # Conversion du DataFrame en liste de dictionnaires
        graph_data = df.to_dict(orient="records")

        # Envoi des données au topic Kafka
        for record in graph_data:
            serialized_record = serialize_record(record)
            future = producer.send("graph_data", value=serialized_record)
            future.get(timeout=10)  # Gestion des erreurs

        producer.flush()  # S'assurer que les messages sont envoyés
        return {"message": "Graph data sent to Kafka"}
    
    except Exception as e:
        print(f"Erreur : {e}")
        return {"error": str(e)}