import os
import pandas as pd
import chromadb

from langchain_community.embeddings import OllamaEmbeddings

# ---------------- CHROMA ---------------- #

client = chromadb.PersistentClient(
    path="ai/chroma_db"
)

collection = client.get_or_create_collection(
    name="retailpulse_gold"
)

# ---------------- EMBEDDINGS ---------------- #

embeddings = OllamaEmbeddings(
    model="llama3"
)

# ---------------- LOAD FILES ---------------- #

data_path = "ai/data/exports"

files = os.listdir(data_path)

for file in files:

    if file.endswith(".csv"):

        df = pd.read_csv(f"{data_path}/{file}")

        for idx, row in df.iterrows():

            text = row.to_json()

            embedding = embeddings.embed_query(text)

            collection.add(
                documents=[text],
                embeddings=[embedding],
                ids=[f"{file}_{idx}"]
            )

print("✅ ChromaDB ingestion complete.")