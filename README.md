# Candidate Finder

Candidate Finder is an AI-powered candidate discovery application built using **Retrieval-Augmented Generation (RAG)**.

The application allows recruiters or hiring teams to search across candidate resumes using natural language instead of relying only on keyword matching.

For example, you can ask:

* Who has experience with Java and Spring Boot?
* Find candidates with engineering management experience.
* Which candidates have worked with AWS and microservices?
* Find someone with both backend development and AI experience.
* Who would be suitable for a Senior Backend Engineer position?

Candidate Finder retrieves the most relevant information from candidate resumes and uses an LLM to generate an answer based on the retrieved context.

---

## How It Works

The application uses a RAG pipeline:

```text
Candidate Resumes
      ↓
LLM-based Chunking
      ↓
OpenAI Embeddings
      ↓
ChromaDB Vector Store
      ↓
User Question
      ↓
Question Embedding
      ↓
Vector Search
      ↓
Top 5 Resume Chunks
      ↓
LLM Re-ranking
      ↓
Top 3 Chunks
      ↓
LLM + Retrieved Context
      ↓
Final Answer
```

### 1. Resume Ingestion

Candidate resumes are stored as Markdown files inside the `knowledge-base` directory.

During ingestion, the application:

1. Reads the resume files.
2. Uses an LLM to split each resume into meaningful overlapping chunks.
3. Creates a headline and summary for each chunk.
4. Generates vector embeddings using OpenAI.
5. Stores the embeddings and resume content in ChromaDB.

This creates the searchable candidate knowledge base.

---

### 2. Candidate Retrieval

When a user asks a question:

```text
"Find a candidate with Java, Spring Boot and AWS experience"
```

Candidate Finder:

1. Converts the question into an embedding.
2. Searches ChromaDB for semantically similar resume sections.
3. Retrieves the top matching chunks.

The application currently retrieves the **top 5 candidate chunks**.

---

### 3. LLM Re-ranking

Vector similarity alone does not always provide the best ordering.

Candidate Finder therefore sends the retrieved chunks to an LLM, which reranks them according to how relevant they are to the user's question.

The **top 3 reranked chunks** are then used as context for the final answer.

---

### 4. Answer Generation

The selected resume information is passed to the LLM together with the user's question.

The model generates an answer grounded in the retrieved candidate information rather than answering only from its general knowledge.

The UI also displays the retrieved context so that users can see which resume information contributed to the response.

---

## Tech Stack

| Technology            | Purpose                                      |
| --------------------- | -------------------------------------------- |
| Python                | Application development                      |
| OpenAI                | Embeddings                                   |
| LiteLLM               | Unified LLM interface                        |
| GPT-4.1 Nano          | Resume chunking during ingestion             |
| GPT-OSS 120B via Groq | Reranking and answer generation              |
| ChromaDB              | Vector database                              |
| Gradio                | Chat interface                               |
| Pydantic              | Structured LLM responses                     |
| python-dotenv         | Environment configuration                    |
| uv                    | Python dependency and environment management |

---

## Project Structure

```text
candidate-finder/
│
├── knowledge-base/
│   └── *.md
│       Candidate resumes used as the knowledge base
│
├── vector_db/
│   └── ChromaDB persistent vector database
│
├── src/
│   └── candidate_finder/
│       ├── ingest.py
│       ├── answer.py
│       └── ui.py
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

### `ingest.py`

Responsible for building the candidate knowledge base.

It:

* Reads resumes from `knowledge-base`
* Uses an LLM to create semantic chunks
* Generates OpenAI embeddings
* Creates the ChromaDB collection
* Stores candidate resume chunks in the vector database

### `answer.py`

Contains the RAG pipeline.

It:

* Generates an embedding for the user question
* Searches ChromaDB
* Retrieves relevant resume chunks
* Reranks retrieved chunks
* Builds the RAG prompt
* Calls the answer model
* Returns the generated answer and supporting context

### `ui.py`

Provides the Gradio-based user interface.

Users can:

* Ask natural-language questions about candidates
* Continue a conversation
* View the generated answer
* Inspect the resume context retrieved by the RAG pipeline

---

## Getting Started

### Prerequisites

Make sure you have:

* Python 3.14+
* `uv`
* OpenAI API key
* Groq API key

---

## Clone the Repository

```bash
git clone https://github.com/khushboo13gupta/candidate-finder.git
cd candidate-finder
```

---

## Install Dependencies

This project uses `uv` for dependency management.

```bash
uv sync
```

If `uv` is not installed:

```bash
pip install uv
```

Then run:

```bash
uv sync
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

Do not commit your `.env` file to GitHub.

---

## Add Candidate Resumes

Add candidate information as Markdown files inside:

```text
knowledge-base/
```

For example:

```text
knowledge-base/
├── candidate_1.md
├── candidate_2.md
├── candidate_3.md
└── candidate_4.md
```

Each Markdown file represents a candidate resume or profile.

---

## Build the Vector Database

Before starting the application, run the ingestion pipeline:

```bash
uv run src/candidate_finder/ingest.py
```

The ingestion process will:

```text
Load resumes
    ↓
Create semantic chunks
    ↓
Generate embeddings
    ↓
Store vectors in ChromaDB
```

When ingestion completes, you should see output similar to:

```text
Loaded 10 documents
Vectorstore created with 150 documents
Ingestion complete
```

The generated vector database will be stored in:

```text
vector_db/
```

You normally only need to rerun ingestion when resumes are added or changed.

---

## Run the Application

Start the Gradio UI:

```bash
uv run src/candidate_finder/ui.py
```

The application will start locally and open in your browser.

You can then ask questions such as:

```text
Find candidates with Java microservices experience.
```

```text
Who has experience leading engineering teams?
```

```text
Which candidates have worked with AWS?
```

```text
Find someone with both backend engineering and generative AI experience.
```

---

## RAG Pipeline

The complete request flow looks like this:

```text
                        ┌────────────────────┐
                        │   Candidate CVs    │
                        │    Markdown        │
                        └─────────┬──────────┘
                                  │
                                  ▼
                        ┌────────────────────┐
                        │   LLM Chunking     │
                        │   GPT-4.1 Nano     │
                        └─────────┬──────────┘
                                  │
                                  ▼
                        ┌────────────────────┐
                        │ OpenAI Embeddings  │
                        │ text-embedding-    │
                        │     3-large        │
                        └─────────┬──────────┘
                                  │
                                  ▼
                        ┌────────────────────┐
                        │      ChromaDB      │
                        │   Vector Store     │
                        └─────────┬──────────┘
                                  │
                           Vector Search
                                  │
                                  ▼
┌──────────────┐        ┌────────────────────┐
│ User Question│───────▶│ Top 5 Resume       │
└──────────────┘        │ Chunks             │
                        └─────────┬──────────┘
                                  │
                                  ▼
                        ┌────────────────────┐
                        │    LLM Reranker    │
                        └─────────┬──────────┘
                                  │
                                  ▼
                        ┌────────────────────┐
                        │ Top 3 Resume       │
                        │ Chunks             │
                        └─────────┬──────────┘
                                  │
                                  ▼
                        ┌────────────────────┐
                        │   RAG Generation   │
                        │                    │
                        │ Question + Context │
                        └─────────┬──────────┘
                                  │
                                  ▼
                        ┌────────────────────┐
                        │       Answer       │
                        └────────────────────┘
```

---

## Why RAG?

Traditional candidate search systems often depend heavily on exact keyword matching.

For example, searching for:

```text
"backend engineer with distributed systems experience"
```

may miss candidates whose resumes describe:

```text
"built highly scalable event-driven microservices using Kafka"
```

even though the experience is relevant.

Using vector embeddings allows Candidate Finder to search based on **semantic meaning**, not just exact words.

RAG then gives the LLM relevant information from the candidate database before asking it to answer the question.

This helps make the response:

* More relevant
* Grounded in candidate data
* Easier to verify
* Less dependent on the LLM's general knowledge

---

## Current Features

* Natural-language candidate search
* Resume ingestion
* LLM-based semantic chunking
* Vector embeddings
* Persistent ChromaDB storage
* Semantic similarity search
* LLM-based reranking
* Retrieval-Augmented Generation
* Conversational search
* Retrieved-context visualization
* Multiple LLM providers through LiteLLM

---

## Future Improvements

Some possible next steps for the project:

* Upload resumes directly through the UI
* Support PDF and DOCX resumes
* Extract structured candidate information
* Add job-description matching
* Generate candidate match scores
* Rank candidates for a particular role
* Add candidate filters such as location, experience and skills
* Display candidate cards instead of only chat responses
* Add citations linking answers to individual resumes
* Add hybrid keyword + vector search
* Add candidate comparison
* Add evaluation metrics for retrieval quality
* Containerize the application with Docker
* Deploy the application to the cloud

---

## Example Use Cases

Candidate Finder can be extended to support workflows such as:

### Candidate Discovery

```text
Find backend engineers with more than five years of Java experience.
```

### Skill Search

```text
Who has experience with Kafka, Spring Boot and AWS?
```

### Leadership Search

```text
Find candidates who have managed engineering teams.
```

### Candidate Comparison

```text
Compare the experience of candidates who have worked with distributed systems.
```

### Job Matching

```text
Which candidate would be relevant for a Senior Java Backend Engineer role requiring
Spring Boot, Kafka, AWS and microservices?
```

---

## Disclaimer

Candidate Finder is an experimental AI project intended to demonstrate RAG, semantic search and LLM-based information retrieval.

AI-generated responses should be treated as decision-support information rather than as automated hiring decisions. Candidate evaluation should include appropriate human review and should not rely on protected personal characteristics.

---

## Author

**Khushboo Gupta**

GitHub: [khushboo13gupta](https://github.com/khushboo13gupta)

---

## License

This project is currently intended for learning and portfolio purposes.
