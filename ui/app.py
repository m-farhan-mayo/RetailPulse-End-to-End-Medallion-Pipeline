import chainlit as cl
import chromadb

from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings

# ---------------- OLLAMA ---------------- #

llm = Ollama(
    model="llama3"
)

embeddings = OllamaEmbeddings(
    model="llama3"
)

# ---------------- CHROMADB ---------------- #

client = chromadb.PersistentClient(
    path="ai/chroma_db"
)

collection = client.get_collection(
    name="retailpulse_gold"
)

# ---------------- CHAT START ---------------- #

@cl.on_chat_start
async def start():

    await cl.Message(
        content="""
# 🤖 RetailPulse AI Assistant

Ask anything about:
- revenue
- products
- stores
- sales trends
"""
    ).send()

# ---------------- MESSAGE HANDLER ---------------- #

@cl.on_message
async def main(message: cl.Message):

    question = message.content

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

    await cl.Message(
        content=response
    ).send()