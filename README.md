# Sales Call Intelligence System

An AI-powered system that transforms raw sales call transcripts into actionable intelligence using multi-agent orchestration (CrewAI) and retrieval-augmented generation (RAG).

## What It Does

1. **Upload a call transcript** (text file or paste)
2. **AI agents analyze it:**
   - Extract structured data (account stage, products, concerns, action items)
   - Search HashiCorp documentation for relevant solutions
   - Find similar past calls for context
   - Compose a professional email summary
   - Store the transcript for future reference
3. **Receive a formatted email** with:
   - Executive summary
   - Technical concerns matched to documentation
   - Prioritized action items
   - Resources to share with the customer
   - Internal deal health assessment

## Setup

### 1. Prerequisites

- **Python 3.12** (CrewAI requires `>=3.10, <3.14`)
- OpenAI API key
- (Optional) SendGrid API key for email delivery

### 2. Installation

```bash
# Clone the repo
git clone <repo-url>
cd sales-agent-rag

# Create virtual environment with Python 3.12
/opt/homebrew/bin/python3.12 -m venv venv  # macOS with Homebrew
# OR: python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy example config
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

Required:
```
OPENAI_API_KEY=your-openai-api-key-here
```

Optional (for email sending):
```
SENDGRID_API_KEY=your-sendgrid-api-key
EMAIL_FROM=noreply@yourdomain.com
EMAIL_TO=you@yourdomain.com
EMAIL_PREVIEW_MODE=true  # Set to false to actually send emails
```

### 4. Ingest Documentation

#### Option A: Use Pre-Included Sample Docs

```bash
python -m src.rag.ingest
```

This will index the 5 sample documentation files in `data/docs/`.

#### Option B: Scrape Live HashiCorp Documentation

```bash
# Scrape Vault documentation
python -m src.rag.scrape --product vault --urls data/vault_urls.txt

# Scrape Terraform documentation
python -m src.rag.scrape --product terraform --urls data/terraform_urls.txt
```

The scraper will:
- Fetch each URL
- Extract the main content
- Convert to markdown
- Save to `data/docs/{product}/`
- Automatically ingest into ChromaDB

**Add your own URLs:**
Edit `data/vault_urls.txt` or `data/terraform_urls.txt` and add one URL per line.

## Usage

### Process a Transcript from a File

```bash
python -m src.main --file data/sample_transcripts/acme-corp-evaluation.txt
```

### Paste a Transcript Interactively

```bash
python -m src.main --paste
# Paste your transcript, then press Ctrl+D (Unix) or Ctrl+Z (Windows)
```

### Output

With `EMAIL_PREVIEW_MODE=true` (default), the email will be printed to the console.

With `EMAIL_PREVIEW_MODE=false`, the email will be sent via SendGrid to `EMAIL_TO`.

## Project Structure

```
sales-agent-rag/
├── src/
│   ├── main.py              # CLI entry point
│   ├── config.py            # Configuration management
│   ├── agents/              # 5 CrewAI agents
│   │   ├── transcript_analyzer.py
│   │   ├── doc_researcher.py
│   │   ├── historical_analyst.py
│   │   ├── email_composer.py
│   │   └── knowledge_updater.py
│   ├── tools/               # CrewAI tools for RAG operations
│   │   ├── doc_search.py
│   │   ├── transcript_search.py
│   │   └── vector_store.py
│   ├── rag/                 # RAG infrastructure
│   │   ├── database.py      # ChromaDB client
│   │   ├── ingest.py        # Document ingestion
│   │   ├── search.py        # Semantic search
│   │   └── scrape.py        # Web scraper
│   ├── email/               # Email generation
│   │   ├── templates.py
│   │   └── sender.py
│   └── crew/
│       └── pipeline.py      # Multi-agent orchestration
├── data/
│   ├── docs/                # Documentation for RAG
│   │   ├── vault/
│   │   └── terraform/
│   ├── sample_transcripts/  # Sample call transcripts
│   ├── vault_urls.txt       # URLs to scrape for Vault docs
│   └── terraform_urls.txt   # URLs to scrape for Terraform docs
├── tests/                   # Unit tests
├── PRD.md                   # Product requirements
├── CLAUDE.md                # Architecture & decisions
└── PROGRESS.md              # Development progress

```

## Architecture

### Multi-Agent Pipeline

Five specialized agents work sequentially:

1. **Transcript Analyzer**: Extracts structured data (account stage, products, concerns, action items, sentiment)
2. **Documentation Researcher**: Searches HashiCorp docs for relevant information
3. **Historical Context Analyst**: Finds similar past calls and patterns
4. **Email Composer**: Synthesizes everything into a professional email
5. **Knowledge Base Updater**: Stores the transcript for future reference

### RAG System

- **Vector Database**: ChromaDB (local, persistent)
- **Collections**:
  - `hashicorp-docs`: Pre-populated documentation
  - `call-transcripts`: Grows with each processed call
- **Embeddings**: OpenAI `text-embedding-3-small`
- **Search**: Semantic similarity + metadata filtering

### LLM

- **Model**: OpenAI `gpt-4o-mini` (cost-efficient, fast)
- **Framework**: CrewAI for agent orchestration

## Testing

```bash
# Run unit tests
pytest tests/ -v

# Test document ingestion
python -m src.rag.ingest

# Process the sample transcript
python -m src.main --file data/sample_transcripts/acme-corp-evaluation.txt
```

## Development

See `PROGRESS.md` for development status and `CLAUDE.md` for detailed architecture decisions.

## Troubleshooting

### Python Version Issues

CrewAI requires Python `>=3.10, <3.14`. If you have Python 3.14 (default on some systems), explicitly use 3.12:

```bash
# Find Python 3.12
which python3.12

# Create venv with Python 3.12
/opt/homebrew/bin/python3.12 -m venv venv
```

### Dependency Conflicts

CrewAI pins specific versions of its dependencies. Let it manage them — don't pin `chromadb`, `openai`, `pydantic`, or `python-dotenv` separately.

### Empty ChromaDB

If searches return no results, you may need to ingest documentation:

```bash
python -m src.rag.ingest
```

### Scraper Errors

If the scraper fails to extract content, the page structure may have changed. Check:
- Is the URL accessible?
- Does the page load in a browser?
- Try adding site-specific extraction rules in `src/rag/scrape.py`

## Future Enhancements

- Web UI (Streamlit/FastAPI)
- CRM integration (Salesforce, HubSpot)
- Call recording ingestion (Whisper API)
- Competitive intelligence database
- Team analytics dashboard
- Slack/Teams integration

## License

MIT
