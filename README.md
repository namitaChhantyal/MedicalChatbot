# MedicalChatbot

## Requirements

* **Python 3.11** (tested on 3.11.9)
* **pip ≥ 22**

---

## Overview

**MedicalChatbot** is a Retrieval-Augmented Generation ( **RAG** )–based chatbot that provides **medical-related answers** from uploaded reference materials.

It combines  **Flask** ,  **LangChain** ,  **Pinecone** ,  **OpenAI GPT** , and **Hugging Face embeddings** to deliver accurate, context-aware responses.

---

## Tech Stack

* **Flask** – Web interface
* **LangChain** – Orchestration framework
* **Pinecone** – Vector database for embeddings
* **OpenAI GPT-4o-mini** – Language model for generation
* **Hugging Face** – Sentence-transformer embeddings (`all-MiniLM-L6-v2`)

---

## Features

* Responsive chat UI (works on both laptop & mobile)
* Retrieval-based answers (no hallucinations)
* Restricts responses to **medical topics only**
* Customizable system prompt
* Built-in evaluation using **RAGAS framework**

---

## Architecture Overview

### Workflow

1. **Data Ingestion** – Medical PDFs are chunked and embedded using Hugging Face.
2. **Vector Storage** – Embeddings are stored in  **Pinecone** .
3. **Query Processing** – User queries are embedded and matched against Pinecone.
4. **Answer Generation** – Retrieved chunks + system prompt → OpenAI GPT model.
5. **Response Filtering** – Non-medical queries → predefined polite message.

---

### Key Components and Relationships

| Component                                     | Description                                         | Relationship                                |
| --------------------------------------------- | --------------------------------------------------- | ------------------------------------------- |
| **Flask App (`app.py`)**              | Web server handling `/`(UI) and `/ask`(queries) | Integrates small talk handler and RAG chain |
| **Small Talk Handler**                  | Handles greetings & farewells                       | Runs before RAG for speed                   |
| **RAG Chain (`src/prompt.py`)**       | Core retrieval + generation pipeline                | Uses `create_retrieval_chain`and OpenAI   |
| **Retriever**                           | Queries Pinecone for top-k matches                  | Depends on embeddings                       |
| **Vector Store (Pinecone)**             | Stores vectorized chunks                            | Built via `store_index.py`                |
| **Embedding Model (`src/helper.py`)** | Loads `sentence-transformers/all-MiniLM-L6-v2`    | Used for indexing & querying                |
| **LLM (OpenAI)**                        | Generates answers                                   | Uses structured medical prompt              |

---

## Data Flow

1. User submits a question through the chat UI.
2. Flask detects small talk; if not, sends the query to the RAG chain.
3. The query is embedded → searched in Pinecone.
4. Top chunks are retrieved and inserted into a system prompt.
5. Prompt is passed to OpenAI GPT for response.
6. Final answer is displayed in the UI.

---

## Project Structure

<pre class="overflow-visible!" data-start="2997" data-end="3785"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>MedicalChatbot/
│── Data/                         </span><span># Medical PDF documents</span><span>
│── docs/                         </span><span># Documentation</span><span>
│   ├── C4_Diagrams.md            </span><span># C4 model diagrams</span><span>
│   └── diagrams/                 </span><span># Architecture visuals</span><span>
│── src/                          </span><span># Source code</span><span>
│   ├── helper.py                 </span><span># Embedding & data functions</span><span>
│   ├── prompt.py                 </span><span># RAG logic & prompt templates</span><span>
│── static/                       </span><span># CSS, JS, assets</span><span>
│   ├── style.css
│── templates/
│   ├── index.html                </span><span># Chat interface</span><span>
│── app.py                        </span><span># Flask entrypoint</span><span>
│── store_index.py                </span><span># Pinecone index creation</span><span>
│── docs/evaluation/              </span><span># RAGAS evaluation scripts</span><span>
│── requirements.txt
│── setup.py
│── README.md
│── LICENSE
</span></span></code></div></div></pre>

---

## Setup Instructions

### 1. Clone the repository

<pre class="overflow-visible!" data-start="3846" data-end="3939"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>git </span><span>clone</span><span> https://github.com/namitaChhantyal/MedicalChatbot.git
</span><span>cd</span><span> MedicalChatbot
</span></span></code></div></div></pre>

### 2. Create and activate a virtual environment

<pre class="overflow-visible!" data-start="3990" data-end="4122"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span># Create</span><span>
py -3.11 -m venv medibot

</span><span># Activate</span><span>
</span><span># Windows</span><span>
medibot\Scripts\activate
</span><span># Mac/Linux</span><span>
</span><span>source</span><span> medibot/bin/activate
</span></span></code></div></div></pre>

### 3. Install dependencies

<pre class="overflow-visible!" data-start="4152" data-end="4195"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install -r requirements.txt
</span></span></code></div></div></pre>

### 4. Configure environment variables

Create a `.env` file in the root directory:

<pre class="overflow-visible!" data-start="4281" data-end="4398"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>OPENAI_API_KEY</span><span>=your_openai_api_key
</span><span>OPENAI_PROJECT_KEY</span><span>=your_project_key
</span><span>PINECONE_API_KEY</span><span>=your_pinecone_api_key
</span></span></code></div></div></pre>

> Make sure your Pinecone project has a **serverless environment** in  **AWS us-east-1** .

---

## Run Guide

### Setup Once

```
git clone https://github.com/namitaChhantyal/MedicalChatbot
cd MedicalChatbot

### 2. Create & activate virtual environment
Create Virtual environment
py -3.11 -m venv medibot
# Windows
medibot\Scripts\activate
# Mac/Linux
source medibot/bin/activate
```

Ensure `.env` is set up with:

<pre class="overflow-visible!" data-start="4693" data-end="4751"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>OPENAI_API_KEY</span><span>
OPENAI_PROJECT_KEY
PINECONE_API_KEY
</span></span></code></div></div></pre>

---

### store_index.py

**Command:**

<pre class="overflow-visible!" data-start="4793" data-end="4826"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python store_index.py
</span></span></code></div></div></pre>

**What it does:**

* Loads PDFs from `Data/`
* Splits them into chunks
* Creates embeddings using `sentence-transformers/all-MiniLM-L6-v2`
* Builds or updates Pinecone index `medicalbot` under `namespace='default'`
* Uploads all chunks to Pinecone

After it completes, confirm the index in your **Pinecone Console** before proceeding.

---

### app.py

**Command:**

<pre class="overflow-visible!" data-start="5194" data-end="5219"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python app.py
</span></span></code></div></div></pre>

**What it does:**

* Starts Flask web app
* Loads retriever and LLM
* Serves the chatbot at: **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

Visit the URL in your browser to chat — responses come directly from your Pinecone database.

---

### docs/evaluation/evaluate_ragas.py

**Command:**

<pre class="overflow-visible!" data-start="5499" data-end="5551"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python docs/evaluation/evaluate_ragas.py
</span></span></code></div></div></pre>

**What it does:**

* Runs the RAG pipeline over `docs/evaluation/qa_dataset.json`
* Evaluates using **RAGAS metrics**
* Prints aggregate scores
* Exports detailed results to `docs/evaluation/ragas_results.csv`

Use the CSV to inspect per-question performance or compare runs after tuning prompts/embeddings.

---

### test_embeddings.py

**Command:**

<pre class="overflow-visible!" data-start="5904" data-end="5941"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python test_embeddings.py
</span></span></code></div></div></pre>

**What it does:**

* Iterates through all models in:
  <pre class="overflow-visible!" data-start="5996" data-end="6173"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>MODELS = [
      </span><span>'sentence-transformers/all-MiniLM-L6-v2'</span><span>,
      </span><span>'sentence-transformers/all-MiniLM-L12-v2'</span><span>,
      </span><span>'sentence-transformers/all-mpnet-base-v2'</span><span>
  ]
  </span></span></code></div></div></pre>
* Creates a temporary Pinecone index (`medicalbot-test-*`)
* Uploads test chunks and retrieves top matches
* Prints retrieved snippets for comparison

Use this to decide whether to switch embedding models before reindexing.

---

### After Any Change

* Update data or prompt templates
* Change embedding models
* Modify the retriever or parameters

Run these in order:

<pre class="overflow-visible!" data-start="6566" data-end="6654"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python store_index.py
python docs/evaluation/evaluate_ragas.py
python app.py
</span></span></code></div></div></pre>

Then test chatbot behavior in the UI.

---

## Evaluation

The chatbot can be quantitatively evaluated using **RAGAS metrics** for faithfulness, relevancy, and answer correctness.

Results and scripts are located in `docs/evaluation/`.

---
