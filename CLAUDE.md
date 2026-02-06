# Sales Call Intelligence System

## Project Vision

This system transforms raw sales call transcripts into structured, actionable intelligence delivered via email. It uses multi-agent AI orchestration (CrewAI) and retrieval-augmented generation (RAG) to analyze calls, match technical concerns to documentation, find patterns in past calls, and produce a comprehensive email summary — all automatically.

---

## Repository Architecture

```
sales-agent-rag/
├── CLAUDE.md                    # This file - project overview and decisions
├── PRD.md                       # Product requirements document
├── PROGRESS.md                  # Development progress tracker
├── README.md                    # Setup and usage instructions (created at end)
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore rules
│
├── src/
│   ├── __init__.py
│   ├── main.py                  # CLI entry point - orchestrates the full pipeline
│   ├── config.py                # Configuration loading from .env
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── transcript_analyzer.py    # Agent 1: Extract structured data from transcript
│   │   ├── doc_researcher.py         # Agent 2: Search HashiCorp docs for concerns
│   │   ├── historical_analyst.py     # Agent 3: Search past transcripts for context
│   │   ├── email_composer.py         # Agent 4: Synthesize everything into email
│   │   └── knowledge_updater.py      # Agent 5: Store transcript in vector DB
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── doc_search.py             # Tool: Search hashicorp-docs collection
│   │   ├── transcript_search.py      # Tool: Search call-transcripts collection
│   │   └── vector_store.py           # Tool: Write to vector database
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── database.py               # ChromaDB client setup and collection management
│   │   ├── embeddings.py             # Embedding generation (OpenAI)
│   │   ├── ingest.py                 # Document ingestion pipeline
│   │   └── search.py                 # Semantic search with metadata filtering
│   │
│   ├── email/
│   │   ├── __init__.py
│   │   ├── sender.py                 # SendGrid email sending
│   │   └── templates.py              # HTML email template
│   │
│   └── crew/
│       ├── __init__.py
│       └── pipeline.py               # CrewAI crew definition and task orchestration
│
├── data/
│   ├── docs/                         # HashiCorp documentation files for ingestion
│   │   ├── vault/
│   │   └── terraform/
│   └── sample_transcripts/           # Sample transcripts for testing
│
├── chroma_db/                        # ChromaDB persistent storage (gitignored)
│
└── tests/
    ├── __init__.py
    ├── test_rag.py                   # RAG search and ingestion tests
    ├── test_agents.py                # Individual agent tests
    └── test_pipeline.py              # End-to-end pipeline tests
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `src/main.py` | CLI entry point. Accepts transcript (file path or pasted text), runs pipeline, reports results. |
| `src/config.py` | Loads `.env`, validates required keys are present, exposes config as simple variables. |
| `src/agents/` | One file per agent. Each exports a function that creates a CrewAI `Agent` instance. |
| `src/tools/` | CrewAI-compatible tools that wrap RAG operations. Agents use these to search/write data. |
| `src/rag/` | All vector database logic. ChromaDB setup, embedding, ingestion, search. No agent logic here. |
| `src/email/` | Email formatting and sending. Isolated from agent logic. |
| `src/crew/pipeline.py` | Defines the CrewAI `Crew`, creates all agents and tasks, runs the sequential pipeline. |

---

## Agent Design

### Agent 1: Transcript Analyzer
- **Role:** Senior Sales Call Analyst
- **Goal:** Extract structured intelligence from raw call transcripts
- **Tools:** None (pure LLM reasoning)
- **Why no tools?** The transcript is provided directly as input. The LLM excels at extracting structured information from unstructured text without external lookups.
- **Output:** JSON with account info, technical concerns, action items, sentiment

### Agent 2: Documentation Researcher
- **Role:** HashiCorp Technical Documentation Specialist
- **Goal:** Find the most relevant documentation for each technical concern raised in the call
- **Tools:** `doc_search` (searches `hashicorp-docs` ChromaDB collection)
- **Why this design?** Separating doc search from analysis keeps each agent focused. This agent only worries about finding the right docs, not interpreting the call.
- **Output:** JSON mapping each concern to relevant documentation with excerpts and URLs

### Agent 3: Historical Context Analyst
- **Role:** Sales Intelligence Analyst
- **Goal:** Find patterns and context from past calls that are relevant to the current situation
- **Tools:** `transcript_search` (searches `call-transcripts` ChromaDB collection)
- **Why this design?** Historical context is a distinct analytical task. When the transcript database is empty (first call), this agent gracefully returns "no prior history" — it doesn't block the pipeline.
- **Output:** JSON with similar calls, observed patterns, and suggestions from past experience

### Agent 4: Email Composer
- **Role:** Executive Communications Specialist
- **Goal:** Synthesize all analysis into a clear, actionable email
- **Tools:** None (pure LLM synthesis)
- **Why no tools?** This agent receives all data it needs from Agents 1-3 via task context. Its job is purely synthesis and formatting.
- **Output:** Formatted HTML email content

### Agent 5: Knowledge Base Updater
- **Role:** Knowledge Management Specialist
- **Goal:** Store the processed transcript and analysis for future retrieval
- **Tools:** `vector_store` (writes to `call-transcripts` ChromaDB collection)
- **Why separate agent?** Runs after email composition so that pipeline failures don't leave partial data in the knowledge base. Clean separation of "analysis" from "storage."
- **Output:** Confirmation that transcript is indexed

### Task Flow
```
Transcript Input
      │
      ▼
┌─────────────────────┐
│  Agent 1: Analyzer   │  ← Pure LLM analysis
│  (extract structure) │
└──────────┬──────────┘
           │ JSON: concerns, actions, sentiment
           ▼
┌─────────────────────┐
│  Agent 2: Doc Search │  ← RAG over hashicorp-docs
│  (find relevant docs)│
└──────────┬──────────┘
           │ JSON: docs per concern
           ▼
┌─────────────────────┐
│  Agent 3: History    │  ← RAG over call-transcripts
│  (find past context) │
└──────────┬──────────┘
           │ JSON: similar calls, patterns
           ▼
┌─────────────────────┐
│  Agent 4: Email      │  ← Pure LLM synthesis
│  (compose email)     │
└──────────┬──────────┘
           │ HTML email content
           ▼
┌─────────────────────┐
│  Agent 5: KB Update  │  ← Vector DB write
│  (store for future)  │
└──────────┬──────────┘
           │ Confirmation
           ▼
    Send Email via SendGrid
```

---

## Key Technical Choices

### CrewAI for Agent Orchestration
**Choice:** CrewAI with sequential process
**Rationale:** CrewAI provides the simplest abstraction for multi-agent coordination in Python. Sequential processing (vs. hierarchical) is easier to debug and reason about. Each agent's output feeds cleanly into the next.

### ChromaDB for Vector Storage
**Choice:** ChromaDB (local persistent storage)
**Rationale:** Free, open-source, runs locally with zero cloud setup. The Python API is minimal — create collection, add documents, query. For a portfolio project, this avoids cloud vendor accounts and API keys beyond what's already needed. Persistent storage means data survives between runs.
**Trade-off:** Not production-scale, but appropriate for this use case (hundreds to low thousands of documents).

### OpenAI for LLM and Embeddings
**Choice:** OpenAI GPT-4o-mini for agents, `text-embedding-3-small` for embeddings
**Rationale:** Cost-efficient while capable. GPT-4o-mini handles structured extraction and synthesis well at a fraction of the cost of larger models. Using the same provider for LLM and embeddings keeps the dependency footprint small.

### SendGrid for Email
**Choice:** SendGrid API with SMTP fallback
**Rationale:** Generous free tier (100 emails/day). Well-documented Python SDK. SMTP fallback allows use with any email provider if SendGrid isn't available.

### Structured JSON Between Agents
**Choice:** Agents output JSON, not free-form text
**Rationale:** JSON output is parseable and validatable. If an agent produces malformed output, we can detect and handle it. Free-form text between agents leads to cascading interpretation errors.

---

## Data Flow

```
User provides transcript (file or paste)
         │
         ▼
┌──────────────────┐     ┌──────────────────┐
│   Input Module   │────▶│  Validation &    │
│  (main.py CLI)   │     │  Preprocessing   │
└──────────────────┘     └────────┬─────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │    CrewAI Pipeline       │
                    │  (pipeline.py)           │
                    │                          │
                    │  Task 1: Analyze         │
                    │      │                   │
                    │      ▼                   │
                    │  Task 2: Search Docs ◄───┼──── ChromaDB: hashicorp-docs
                    │      │                   │
                    │      ▼                   │
                    │  Task 3: Search History◄─┼──── ChromaDB: call-transcripts
                    │      │                   │
                    │      ▼                   │
                    │  Task 4: Compose Email   │
                    │      │                   │
                    │      ▼                   │
                    │  Task 5: Update KB ──────┼────▶ ChromaDB: call-transcripts
                    │                          │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Email Delivery     │
                    │  (SendGrid / SMTP)   │
                    └──────────────────────┘
```

---

## Configuration

All configuration lives in a `.env` file. Required variables:

```
# LLM
OPENAI_API_KEY=your-openai-api-key

# Email
SENDGRID_API_KEY=your-sendgrid-api-key
EMAIL_FROM=noreply@yourdomain.com
EMAIL_TO=you@yourdomain.com

# Optional
EMAIL_PREVIEW_MODE=true          # Print email to console instead of sending
CHROMA_DB_PATH=./chroma_db       # ChromaDB storage location
LOG_LEVEL=INFO                   # DEBUG, INFO, WARNING, ERROR
```

---

## Future Enhancements

These are not in v1.0 but are natural extensions:

1. **Web UI** — Streamlit or FastAPI frontend for transcript upload and email preview
2. **CRM Integration** — Push deal health and action items to Salesforce/HubSpot
3. **Competitive Intelligence** — Dedicated database and analysis for competitor mentions
4. **Call Recording Ingestion** — Whisper API integration for audio-to-text
5. **Automated Scheduling** — Watch a folder or inbox for new transcripts
6. **Team Analytics** — Aggregate insights across all calls (common concerns, win/loss patterns)
7. **Custom Email Templates** — User-configurable email sections and formatting
8. **Slack/Teams Integration** — Post summaries to channels instead of (or in addition to) email

---

## Known Limitations

- **English only** — No multi-language transcript support
- **Text input only** — Cannot process audio recordings directly
- **Single user** — No authentication or multi-tenancy
- **Local vector DB** — ChromaDB is not suitable for production-scale deployments
- **No real-time processing** — Batch processing of completed transcripts only
- **Documentation coverage** — Limited to HashiCorp Vault and Terraform docs provided during setup
- **No CI/CD** — Manual testing and deployment
- **LLM accuracy** — Analysis quality depends on transcript clarity and LLM capabilities; no human-in-the-loop verification

---

## Development Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Then fill in API keys

# Ingest documentation into ChromaDB
python -m src.rag.ingest

# Process a transcript
python -m src.main --file path/to/transcript.txt
python -m src.main --paste  # Interactive paste mode

# Run tests
pytest tests/ -v
```
