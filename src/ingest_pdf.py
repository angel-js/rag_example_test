from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient

# cargar pdf
loader = PyPDFLoader("data/document.pdf")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = text_splitter.split_documents(docs)

embeddings = OllamaEmbeddings(model="nomic-embed-text")

Qdrant.from_documents(
    docs,
    embeddings,
    url="http://localhost:6333",
    collection_name="pdf_docs"
)