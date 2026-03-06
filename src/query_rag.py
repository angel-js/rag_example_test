from langchain_community.vectorstores import Qdrant
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from qdrant_client import QdrantClient

# -----------------------------
# Embeddings
# -----------------------------
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# -----------------------------
# Qdrant connection
# -----------------------------
client = QdrantClient(
    url="http://localhost:6333"
)

vector_db = Qdrant(
    client=client,
    collection_name="pdf_docs",
    embeddings=embeddings
)

# -----------------------------
# Retriever
# -----------------------------
retriever = vector_db.as_retriever(
    search_kwargs={"k": 3}
)

# -----------------------------
# LLM
# -----------------------------
llm = OllamaLLM(
    model="llama3"
)

# -----------------------------
# User Query
# -----------------------------
query = input("Pregunta: ")

# Buscar documentos relevantes
docs = retriever.invoke(query)

# Construir contexto
context = "\n\n".join([doc.page_content for doc in docs])

# -----------------------------
# Prompt
# -----------------------------
prompt = f"""
Responde usando SOLO la información del contexto.

Reglas:
- Si la respuesta no está en el contexto, responde: "No lo sé con la información disponible".
- No inventes información.
- Mantén un tono profesional y objetivo.

Contexto:
{context}

Pregunta:
{query}
"""

# -----------------------------
# LLM Response
# -----------------------------
response = llm.invoke(prompt)

print("\nRespuesta:\n")
print(response)