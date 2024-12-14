# Data Engineering Project: Graph Processing

## Description
This project implements a data engineering pipeline for processing a graph dataset using cutting-edge technologies like FastAPI, Apache Kafka, Apache Spark GraphX, Neo4j, Streamlit, and Apache Airflow. The goal is to enable automated graph data processing and analysis with interactive visualizations.

---

## Technologies Used
- **FastAPI**: Provides an API to stream data from a Parquet file into Kafka.
- **Apache Kafka**: For streaming and consuming data.
- **Apache Spark GraphX**: For graph computation and analysis.
- **Neo4j**: To store and query graph results.
- **Streamlit**: To visualize data interactively.
- **Apache Airflow**: To orchestrate and schedule the pipeline tasks.
- **Docker & Docker Compose**: For containerization and simplified deployment.

---

## Architecture
### Workflow Steps:
1. **Docker**:  
   - All services are containerized using Docker Compose.
   - Independent containers ensure service isolation and easy portability.
   
2. **Kafka**:  
   - Data is streamed into Kafka using a FastAPI service.
   - The FastAPI endpoint reads data from a Parquet file and streams it into a Kafka topic.
   - A Kafka consumer retrieves the data for further processing.

3. **Spark GraphX**:  
   - Processes graph data retrieved from Kafka.
   - Executes algorithms such as:
     - PageRank
     - Connected Components
     - Triangle Counting.

4. **Neo4j**:  
   - Processed data is stored in Neo4j using Cypher queries for further analysis.

5. **Streamlit**:  
   - Displays an interactive dashboard for visualizing results from Neo4j.

6. **Airflow**:  
   - Manages and orchestrates the pipeline for automated task execution.
  
![workflow](https://github.com/user-attachments/assets/1b8ad346-f873-4b2f-b009-73ae2ab80823)

---

## Prerequisites
Before running the project, ensure you have:
- **Docker** and **Docker Compose** installed.
- **Python 3.8+** installed on your system.
- Required Python libraries:
  ```bash
  pip install pandas kafka-python pyspark fastapi uvicorn

---

## How to run
 - Clone the repository:
    ```bash
    git clone https://github.com/nada-han/Graph-Pipeline-Project.git
    cd Graph-Pipeline-Project

 - Start the services:
    ```bash
    docker-compose up --build

 - Access the tools:
   
   **Airflow UI:** Access at http://localhost:8080 to monitor and trigger pipeline workflows.
   
   **Kafka API:** Verify data streaming by accessing FastAPI at http://localhost:8000/graph.
   
   **Neo4j Dashboard:** Access Neo4j at http://localhost:7474 to explore stored graph data.
   
   **Streamlit Dashboard:** View results interactively at http://localhost:8501.

--- 

## Video tutorial
For a step-by-step walkthrough of the project setup and usage, watch the tutorial video here:

https://github.com/user-attachments/assets/d6f69757-1b88-4b6d-9d0b-c7abfba4f3e9
