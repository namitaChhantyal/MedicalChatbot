# MedicalChatbot

[](https://github.com/namitaChhantyal/MedicalChatbot#medicalchatbot)

## Requirements

[](https://github.com/namitaChhantyal/MedicalChatbot#requirements)

* Python 3.11 (tested on 3.11.9)
* pip >= 22

# Medical Chatbot (RAG + Flask)

[](https://github.com/namitaChhantyal/MedicalChatbot#medical-chatbot-rag--flask)

A Retrieval-Augmented Generation (RAG) medical chatbot built with:

* **Flask** for the web interface
* **LangChain** for orchestration
* **Pinecone** as vector database
* **OpenAI GPT model** for language generation
* **Hugging Face embeddings** for document representation

## Architecture

[](https://github.com/namitaChhantyal/MedicalChatbot#architecture)

* **Backend** : Flask web server
* **LLM** : OpenAI GPT-4o-mini
* **Vector Database** : Pinecone
* **Embeddings** : Hugging Face sentence-transformers
* **Framework** : LangChain
* **Evaluation** : RAGAS
* **Ingestion** : MCP (Model Context Protocol)

## File Structure

[](https://github.com/namitaChhantyal/MedicalChatbot#file-structure)

### Core Application Files

[](https://github.com/namitaChhantyal/MedicalChatbot#core-application-files)

**`app.py`** - Main Flask application

* Starts web server on port 8080
* Handles `/ask` endpoint for chat queries
* Integrates MCP client for dataset ingestion via chat
* Manages session-based conversation chains
* Returns answers with source citations

**`store_index.py`** - Vector index creation

* Loads all files from `Data/` directory (PDF, JSON, CSV)
* Splits documents into chunks (500 chars, 20 overlap)
* Creates embeddings using Hugging Face model
* Creates/updates Pinecone index "medicalbot"
* Required before using the chatbot

**`ingest_dataset.py`** - CLI tool for dataset ingestion

* Ingests datasets via command line
* Lists ingested datasets
* Supports JSON, CSV, PDF formats
* Usage: `python ingest_dataset.py Data/file.json json`

### Source Code (`src/`)

[](https://github.com/namitaChhantyal/MedicalChatbot#source-code-src)

**`src/helper.py`** - Data loading utilities

* `load_pdf_file()` - Loads PDF files
* `load_json_file()` - Loads JSON files
* `load_csv_file()` - Loads CSV files
* `load_mixed_data()` - Loads all formats from directory
* `text_split()` - Splits documents into chunks
* `download_hugging_face_embeddings()` - Initializes embedding model

**`src/prompt.py`** - RAG chain builders

* `build_rag_chain()` - Single-turn RAG chain (no memory)
* `build_conversational_rag_chain()` - Multi-turn RAG chain (with memory)
* Creates `SourceAwareRetriever` wrapper for source citations
* Configures OpenAI LLM with medical-focused prompts

**`src/mcp_server.py`** - MCP server implementation

* `MedicalDatasetMCPServer` class - Manages dataset ingestion
* `ingest_dataset()` - Ingests files (JSON/CSV/PDF)
* `get_ingested_datasets()` - Lists ingested datasets
* `_save_metadata_to_disk()` - Persists metadata to `Data/.mcp_metadata.json`
* `_load_metadata_from_disk()` - Loads metadata on startup
* Supports MCP protocol functions (optional)

**`src/mcp_client.py`** - MCP client wrapper

* `MCPDatasetClient` class - Client interface for Flask app
* `ingest_dataset()` - Ingests datasets with path resolution
* `list_datasets()` - Lists ingested datasets
* `get_mcp_client()` - Singleton pattern
* `get_mcp_server_instance()` - Persistent server instance

**`src/download_qa_dataset.py`** - Evaluation dataset downloader

* Downloads MedQA, PubMedQA, HealthQA from HuggingFace
* Downloads MedQuAD (47,457 QA pairs from 12 NIH sources) from GitHub
* Creates expanded QA dataset for RAGAS evaluation
* Saves MedQuAD to `Data/medquad_dataset.json` for indexing
* Falls back to synthetic dataset if downloads fail
* Outputs: `docs/evaluation/qa_dataset_expanded.json`

### Frontend Files

[](https://github.com/namitaChhantyal/MedicalChatbot#frontend-files)

**`templates/index.html`** - Chat interface

* HTML structure for chat UI
* JavaScript for API calls and message display
* Shows source citations below answers

**`static/style.css`** - Styling for chat interface

### Evaluation Files

[](https://github.com/namitaChhantyal/MedicalChatbot#evaluation-files)

**`docs/evaluation/evaluate_ragas.py`** - RAGAS evaluation script

* Runs QA pairs through RAG chain
* Calculates faithfulness, answer relevancy, context precision, context recall
* Outputs: `docs/evaluation/ragas_results.csv`

**`docs/evaluation/qa_dataset.json`** - Original evaluation dataset (15 QA pairs)

**`docs/evaluation/qa_dataset_expanded.json`** - Expanded evaluation dataset (created by download script)

### Data Files (`Data/`)

[](https://github.com/namitaChhantyal/MedicalChatbot#data-files-data)

**`Data/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf`** - Medical encyclopedia PDF

**`Data/medical_conditions.json`** - Example JSON dataset

**`Data/medical_diseases.csv`** - Example CSV dataset

**`Data/medquad_dataset.json`** - MedQuAD dataset (created by download script)

* Contains 47,457 QA pairs from 12 NIH sources
* Created when running `python src/download_qa_dataset.py`
* Can be indexed via `store_index.py` for use as knowledge source

**`Data/.mcp_metadata.json`** - MCP metadata persistence (auto-generated)

### Configuration Files

[](https://github.com/namitaChhantyal/MedicalChatbot#configuration-files)

**`requirements.txt`** - Python dependencies

* Flask, LangChain, Pinecone, OpenAI SDK
* Sentence transformers, RAGAS
* MCP SDK for dataset ingestion

**`setup.py`** - Package configuration

**`.env`** - Environment variables (create this)

* `OPENAI_API_KEY` - OpenAI API key
* `PINECONE_API_KEY` - Pinecone API key
* `SECRET_KEY` - Flask session secret

## Setup Instructions

[](https://github.com/namitaChhantyal/MedicalChatbot#setup-instructions)

### Step 1: Prerequisites

[](https://github.com/namitaChhantyal/MedicalChatbot#step-1-prerequisites)

* Python 3.11+
* OpenAI API account
* Pinecone account

### Step 2: Create Virtual Environment

[](https://github.com/namitaChhantyal/MedicalChatbot#step-2-create-virtual-environment)

```shell
python3.11 -m venv medibot
source medibot/bin/activate  # Mac/Linux
# OR
medibot\Scripts\activate     # Windows
```

 **Why** : Isolates project dependencies from system Python.

### Step 3: Install Dependencies

[](https://github.com/namitaChhantyal/MedicalChatbot#step-3-install-dependencies)

```shell
pip install --upgrade pip
pip install -r requirements.txt
```

 **Why** : Installs all required packages (Flask, LangChain, Pinecone, OpenAI, MCP, etc.).

### Step 4: Configure Environment Variables

[](https://github.com/namitaChhantyal/MedicalChatbot#step-4-configure-environment-variables)

Create `.env` file in project root:

```dotenv
OPENAI_API_KEY=sk-your-key-here
PINECONE_API_KEY=your-pinecone-key
SECRET_KEY=random-string-for-sessions
```

 **Why** : API keys are required for LLM and vector database access. Never commit `.env` to git.

### Step 5: Verify Data Files

[](https://github.com/namitaChhantyal/MedicalChatbot#step-5-verify-data-files)

Check `Data/` directory contains files:

* PDF files (`.pdf`)
* JSON files (`.json`)
* CSV files (`.csv`)

 **Why** : These files are indexed and used as knowledge sources.

### Step 6: (Optional) Download MedQuAD Dataset

[](https://github.com/namitaChhantyal/MedicalChatbot#step-6-optional-download-medquad-dataset)

```shell
python src/download_qa_dataset.py
```

 **Why** :

* Downloads MedQuAD (47,457 QA pairs from 12 NIH sources) from GitHub
* Creates expanded evaluation dataset (`docs/evaluation/qa_dataset_expanded.json`)
* Saves full MedQuAD dataset to `Data/medquad_dataset.json` for indexing
* Adds 10,000+ QA pairs for evaluation

**Expected output:**

```
Downloading MedQuAD dataset from GitHub...
Successfully loaded 16407 QA pairs from MedQuAD
Saved 16407 QA pairs to Data/medquad_dataset.json
Total QA pairs created: 10000
```

### Step 7: Create Vector Index

[](https://github.com/namitaChhantyal/MedicalChatbot#step-7-create-vector-index)

```shell
python store_index.py
```

 **Why** :

* Converts documents to embeddings and stores in Pinecone
* Makes documents searchable
* Required before chatbot can answer questions
* Takes 5-10 minutes on first run

Expected output:

```
Loading documents from Data/ directory...
Loaded 774 documents
Splitting documents into chunks...
Created 6988 text chunks
Creating Pinecone index: medicalbot
Uploading embeddings to Pinecone...
Indexing complete!
```

### Step 8: Start Application

[](https://github.com/namitaChhantyal/MedicalChatbot#step-8-start-application)

```shell
python app.py
```

 **Why** : Starts Flask web server for chat interface.

Expected output:

```
 * Running on http://127.0.0.1:8080
```

### Step 9: Access Web Interface

[](https://github.com/namitaChhantyal/MedicalChatbot#step-9-access-web-interface)

Open browser: `http://localhost:8080`

 **Why** : Provides user interface for chat interactions.

## Usage

[](https://github.com/namitaChhantyal/MedicalChatbot#usage)

### Chat Interface

[](https://github.com/namitaChhantyal/MedicalChatbot#chat-interface)

**Ask medical questions:**

* "What are the symptoms of diabetes?"
* "How is hypertension treated?"
* "What causes asthma?"

**Response includes:**

* Answer from retrieved documents
* Source citations (filename)

### Dataset Ingestion via Chat

[](https://github.com/namitaChhantyal/MedicalChatbot#dataset-ingestion-via-chat)

**List datasets:**

```
list datasets
```

**Ingest dataset:**

```
ingest dataset medical_conditions.json
add file medical_diseases.csv
load dataset file.pdf
```

**Supported commands:**

* `list datasets` / `show datasets`
* `ingest dataset <filename>`
* `add dataset <filename>`
* `load file <filename>`
* `import data <filename>`

**After ingestion:**

* Run `python store_index.py` to update vector index
* New data becomes searchable

### Dataset Ingestion via CLI

[](https://github.com/namitaChhantyal/MedicalChatbot#dataset-ingestion-via-cli)

**Ingest:**

```shell
python ingest_dataset.py Data/medical_conditions.json json
```

**List:**

```shell
python ingest_dataset.py --list
```

 **Why** : Provides command-line interface for dataset management.

## Evaluation (Optional)

[](https://github.com/namitaChhantyal/MedicalChatbot#evaluation-optional)

### Step 1: Download Expanded QA Dataset

[](https://github.com/namitaChhantyal/MedicalChatbot#step-1-download-expanded-qa-dataset)

```shell
python src/download_qa_dataset.py
```

 **Why** : Creates larger evaluation dataset for better performance metrics.

### Step 2: Run Evaluation

[](https://github.com/namitaChhantyal/MedicalChatbot#step-2-run-evaluation)

```shell
python docs/evaluation/evaluate_ragas.py
```

 **Why** : Measures chatbot performance using RAGAS metrics:

* **Faithfulness** : Answer grounded in context?
* **Answer Relevancy** : Answer relevant to question?
* **Context Precision** : Retrieved docs relevant?
* **Context Recall** : Retrieved docs contain answer?

Output: `docs/evaluation/ragas_results.csv`

## Data Flow

[](https://github.com/namitaChhantyal/MedicalChatbot#data-flow)

1. **Indexing** : `store_index.py` → Loads files → Splits → Embeds → Uploads to Pinecone
2. **Query** : User question → Embed query → Search Pinecone → Retrieve top documents
3. **Generation** : Retrieved docs + question → LLM → Answer with citations
4. **Ingestion** : File → MCP server → Parse → Store metadata → (Run `store_index.py` to index)

## Troubleshooting

[](https://github.com/namitaChhantyal/MedicalChatbot#troubleshooting)

**"PINECONE_API_KEY is not set"**

* Check `.env` file exists and has correct key

**"ModuleNotFoundError"**

* Activate virtual environment: `source medibot/bin/activate`
* Install dependencies: `pip install -r requirements.txt`

**"Index not found"**

* Run `python store_index.py` first

**"Port 8080 already in use"**

* Change port in `app.py`: `app.run(port=5000)`

**"File not found" when ingesting**

* Place file in `Data/` directory
* Use relative path: `medical_conditions.json`

**No sources showing**

* Check Pinecone index has data: Run `store_index.py`
* Verify documents have source metadata

**MCP ingestion not persisting**

* Metadata saves to `Data/.mcp_metadata.json`
* Both CLI and Flask app read from same file

## Quick Reference

[](https://github.com/namitaChhantyal/MedicalChatbot#quick-reference)

```shell
# Setup
source medibot/bin/activate
pip install -r requirements.txt

# Index data
python store_index.py

# Start app
python app.py

# Ingest dataset
python ingest_dataset.py Data/file.json json

# List datasets
python ingest_dataset.py --list

# Evaluate
python docs/evaluation/evaluate_ragas.py
```

## File Dependencies

[](https://github.com/namitaChhantyal/MedicalChatbot#file-dependencies)

```
app.py
├── src/helper.py (embeddings, loaders)
├── src/prompt.py (RAG chains)
├── src/mcp_client.py (MCP client)
├── templates/index.html (UI)
└── static/style.css (styles)

store_index.py
├── src/helper.py (loaders, embeddings)
└── .env (API keys)

ingest_dataset.py
└── src/mcp_server.py (ingestion)

src/mcp_client.py
└── src/mcp_server.py (server)

src/mcp_server.py
└── src/helper.py (loaders)
```
