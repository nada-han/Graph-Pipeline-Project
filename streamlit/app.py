import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Configurer le titre de l'application Streamlit
st.title("Analyse de Graphes depuis Neo4j")
st.write("Explorez différents algorithmes appliqués sur les graphes.")

# Configuration de la connexion à Neo4j
NEO4J_URI = "bolt://neo4j:7687"
NEO4J_USER = "neo4j"  # Remplacez par votre nom d'utilisateur
NEO4J_PASSWORD = "password"  # Remplacez par votre mot de passe
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Fonction pour exécuter une requête dans Neo4j
def query_neo4j(query):
    with driver.session() as session:
        result = session.run(query)
        return [dict(record) for record in result]

# Visualiser le graphe
def visualize_graph(df, algorithm_name=None):
    if 'source' not in df.columns:
        st.error("Le graphe ne contient pas de données valides pour la visualisation.")
        return

    G = nx.DiGraph()
    for _, row in df.iterrows():
        node_attrs = {
            'pagerank': row.get('pagerank', 'N/A'),
            'component': row.get('component', 'N/A'),
            'triangle_count': row.get('triangle_count', 'N/A')
        }
        G.add_node(row['source'], **node_attrs)
        if pd.notna(row.get('target', None)):
            G.add_edge(row['source'], row['target'])

    pos = nx.spring_layout(G)
    labels = {
        node: f"{node}\nPR: {float(data['pagerank']):.2f}" if isinstance(data.get('pagerank'), (int, float)) else node
        for node, data in G.nodes(data=True)
    }

    plt.figure(figsize=(12, 8))
    nx.draw(
        G, pos, with_labels=True, node_size=700, node_color='lightblue',
        labels=labels, font_size=10, font_color='black'
    )
    title = f"Visualisation du graphe - {algorithm_name}" if algorithm_name else "Visualisation du graphe"
    plt.title(title)
    st.pyplot(plt)

# Requête basée sur l'algorithme sélectionné
def query_graph_data(algorithm):
    if algorithm == "PageRank":
        query = "MATCH (n:GraphData) RETURN n.id AS source, n.rank AS pagerank"
    elif algorithm == "Connected Components":
        query = "MATCH (n:GraphData) RETURN n.id AS source, n.component AS component"
    elif algorithm == "Triangle Count":
        query = "MATCH (n:GraphData) RETURN n.id AS source, n.triangle_count AS triangle_count"
    else:
        st.error("Algorithme non reconnu.")
        return pd.DataFrame()

    df = pd.DataFrame(query_neo4j(query))
    return df.dropna(how='any')

# Interface Streamlit
st.subheader("Sélectionner un algorithme")
algorithm = st.selectbox(
    "Choisissez un algorithme à appliquer",
    ("PageRank", "Connected Components", "Triangle Count")
)

df = query_graph_data(algorithm)

if not df.empty:
    if algorithm == "PageRank":
        st.subheader("Résultats de PageRank")
        st.write(df[["source", "pagerank"]])
    elif algorithm == "Connected Components":
        st.subheader("Composantes connexes")
        st.write(df[["source", "component"]])
    elif algorithm == "Triangle Count":
        st.subheader("Nombre de triangles")
        st.write(df[["source", "triangle_count"]])

    visualize_graph(df, algorithm_name=algorithm)
else:
    st.warning("Aucune donnée trouvée pour l'algorithme sélectionné.")

driver.close()