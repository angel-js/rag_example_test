# RAG Example (Local) – Ollama + Qdrant + LangChain

### Este proyecto implementa un sistema RAG (Retrieval Augmented Generation) completamente local, utilizando:

Ollama → para ejecutar el modelo LLM y generar embeddings

Qdrant → para almacenar embeddings vectoriales

LangChain → para orquestar el pipeline RAG

Python → implementación del pipeline

El sistema permite consultar información contenida en un PDF mediante preguntas en lenguaje natural.

## Arquitectura

### El flujo del sistema es el siguiente:

```
PDF
 ↓
Document Loader
 ↓
Text Splitter
 ↓
Embeddings (Ollama)
 ↓
Vector Database (Qdrant)
 ↓
Retriever
 ↓
LLM (Ollama - Llama3)
 ↓
Respuesta al usuario
```

```
Pipeline:

User Question
      ↓
Retriever (Qdrant)
      ↓
Relevant Chunks
      ↓
Prompt + Context
      ↓
LLM (Ollama)
      ↓
Answer
```

### Paso 1 — Crear entorno virtual
```
python3 -m venv venv
source venv/bin/activate
```

### Paso 2 — Instalar dependencias
Instalar todas las dependencias necesarias:
```
pip install -r requirements.txt
```

Principales librerías utilizadas:

```
langchain
langchain-community
langchain-ollama
qdrant-client
pypdf
```

### Paso 3 — Levantar la base vectorial (Qdrant)

Se utiliza Docker Compose para ejecutar Qdrant.
```
docker-compose up -d
```

Esto levanta Qdrant en:
```
http://localhost:6333
```
### Paso 4 — Instalar Ollama

Instalar Ollama en el sistema.

Mac / Linux:
```
brew install ollama
```
Luego iniciar el servidor:
```
ollama serve
```
Ollama corre por defecto en:
```
http://localhost:11434
```
### Paso 5 — Descargar los modelos

Modelo de embeddings:
```
ollama pull nomic-embed-text
```
Modelo LLM:
```
ollama pull llama3
```
Ver modelos instalados:
```
ollama list
```
### Paso 6 — Ingestar el documento

Este script:

carga el PDF

lo divide en chunks

genera embeddings

guarda los vectores en Qdrant

Ejecutar:
```
python src/ingest_pdf.py
```
Pipeline del script:
```
PDF
 ↓
Load
 ↓
Split
 ↓
Embeddings
 ↓
Qdrant Collection
```
Colección creada:
```
pdf_docs
```
### Paso 7 — Consultar el RAG

Ejecutar el sistema de preguntas:
```
python src/query_rag.py
```
Luego ingresar una pregunta:

Pregunta: ¿De qué trata el documento?

El sistema:

busca los fragmentos relevantes en Qdrant

construye un prompt con contexto

envía el prompt al LLM

devuelve la respuesta

Ejemplo de Prompt

El LLM responde usando solo el contexto recuperado:
```
Responde usando solo el contexto.
Sé conciso y directo al punto.
Si no sabes la respuesta, di que no lo sabes.
No inventes información.

Contexto:
{context}

Pregunta:
{query}
```

### Estructura del proyecto
```
rag_example_test
│
├── data
│   └── document.pdf
│
├── src
│   ├── ingest_pdf.py
│   └── query_rag.py
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```
Comandos principales

Levantar vector DB
```
docker-compose up -d
```
Activar entorno
```
source venv/bin/activate
```
Ingestar documento
```
python src/ingest_pdf.py
```
Consultar el sistema
```
python src/query_rag.py
```