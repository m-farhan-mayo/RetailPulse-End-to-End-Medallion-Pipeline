import chromadb

from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings

# ---------------- LLM ---------------- #

llm = Ollama(
    model="llama3"
)

embeddings = OllamaEmbeddings(
    model="llama3"
)

# ---------------- CHROMA ---------------- #

client = chromadb.PersistentClient(
    path="ai/chroma_db"
)

collection = client.get_collection(
    name="retailpulse_gold"
)

# ---------------- USER QUESTION ---------------- #

question = input("\nAsk Question: ")

# ---------------- SEARCH ---------------- #

query_embedding = embeddings.embed_query(question)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

context = "\n".join(results["documents"][0])

# ---------------- PROMPT ---------------- #

prompt = f"""

You are a retail analytics assistant.

Answer the user question using the context below.

Context:
{context}

Question:
{question}

"""

# ---------------- AI RESPONSE ---------------- #

response = llm.invoke(prompt)

print("\n🤖 AI Answer:\n")

print(response)