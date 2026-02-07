# Sales Call Intelligence System

An AI-powered system that automatically analyzes sales call transcripts and generates actionable email summaries. Built with multi-agent orchestration and retrieval-augmented generation (RAG) to turn unstructured conversations into structured insights.

## What It Does

Upload a sales call transcript, and the system will:
- **Extract key information** (account details, technical concerns, action items, sentiment)
- **Search documentation** to match concerns with relevant resources
- **Find similar past calls** to identify patterns and proven strategies
- **Generate a professional email** with executive summary, prioritized actions, and deal health assessment
- **Store the transcript** in a searchable knowledge base that gets smarter over time

## Why I Built This

After seeing how much time sales engineers spend manually summarizing calls and digging through documentation, I wanted to automate the entire workflow. The challenge was making the system intelligent enough to understand technical conversations and self-improving through accumulated call history.

## Technical Architecture

### Multi-Agent System (CrewAI)

I designed five specialized AI agents that work sequentially, each with a focused responsibility:

1. **Transcript Analyzer** - Parses raw call text and extracts structured data (account stage, products discussed, technical concerns with severity levels, action items with ownership)
2. **Documentation Researcher** - Searches the documentation knowledge base to find relevant resources for each technical concern
3. **Historical Context Analyst** - Queries past transcripts to surface similar situations and what worked before
4. **Email Composer** - Synthesizes all information into a clear, actionable email format
5. **Knowledge Base Updater** - Indexes the current transcript with metadata for future retrieval

Each agent uses GPT-4o-mini for cost-efficient reasoning and is equipped with only the tools it needs to accomplish its specific task.

### RAG Knowledge Base

The system maintains two ChromaDB vector collections:

**hashicorp-docs** - Product documentation indexed and searchable
- Ingests markdown files from HashiCorp Vault and Terraform documentation
- Chunks documents intelligently (800 words with 100-word overlap to preserve context)
- Stores metadata: product, source file, chunk index
- Enables semantic search: "kubernetes authentication" finds relevant auth methods even if the exact phrase isn't in the docs

**call-transcripts** - Historical call data that grows over time
- Each processed call gets stored with rich metadata (account name, date, stage, products, sentiment)
- Becomes searchable by future calls: "Show me similar POC deals with Vault concerns"
- Creates organizational memory: patterns, successful strategies, common objections
- Enables context-aware analysis: "We've seen this concern 3 times before, here's what worked"

### Web Scraper for Documentation

Built a custom scraper that:
- Fetches documentation pages from URLs
- Extracts main content (strips navigation, footers, ads)
- Converts HTML to clean markdown
- Automatically ingests into the vector database
- Makes it easy to keep documentation up-to-date

You can scrape entire documentation sites by providing a URL list.

### Self-Improving System

The key innovation: **every processed transcript becomes training data for future calls**. The system literally gets smarter with each call you analyze:
- Call #1: Pure documentation search
- Call #10: Can reference 9 similar past situations
- Call #100: Has seen nearly every common objection and knows what works

## Tech Stack

- **Python 3.12** (CrewAI requires <3.14)
- **CrewAI** - Multi-agent orchestration framework
- **OpenAI GPT-4o-mini** - Fast, cost-efficient LLM
- **ChromaDB** - Local vector database with persistent storage
- **OpenAI text-embedding-3-small** - Semantic embeddings for RAG
- **SendGrid** - Email delivery (with console preview mode for development)
- **BeautifulSoup + Markdownify** - Web scraping pipeline

## Installation

```bash
# Clone the repo
git clone https://github.com/tayden-b/sales-agent-rag.git
cd sales-agent-rag

# Create virtual environment (must use Python 3.12)
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### 1. Load Documentation

**Option A:** Use the pre-included sample docs
```bash
python -m src.rag.ingest
```

**Option B:** Scrape live documentation from URLs
```bash
# Edit data/vault_urls.txt or data/terraform_urls.txt with documentation URLs
python -m src.rag.scrape --product vault --urls data/vault_urls.txt
python -m src.rag.scrape --product terraform --urls data/terraform_urls.txt
```

The scraper handles everything: fetch → extract → convert → ingest.

### 2. Process a Transcript

```bash
# From a file
python -m src.main --file path/to/transcript.txt

# Or paste interactively
python -m src.main --paste
```

The system will:
- Analyze the call (~20-30 seconds)
- Search documentation (~10-15 seconds)
- Check historical context (~5-10 seconds)
- Generate email (~15-20 seconds)
- Store transcript for future use (~5 seconds)

**Total time:** ~60-90 seconds for a typical transcript.

### 3. Review the Email

By default, `EMAIL_PREVIEW_MODE=true` prints the email to your console. To send real emails via SendGrid, set it to `false` in your `.env` file.

## Project Structure

```
sales-agent-rag/
├── src/
│   ├── main.py              # CLI entry point
│   ├── config.py            # Environment configuration
│   ├── agents/              # 5 specialized CrewAI agents
│   ├── tools/               # RAG search and storage tools
│   ├── rag/                 # Vector database infrastructure
│   │   ├── database.py      # ChromaDB client
│   │   ├── ingest.py        # Document ingestion pipeline
│   │   ├── search.py        # Semantic search
│   │   └── scrape.py        # Web scraper
│   ├── email/               # Email generation and sending
│   └── crew/
│       └── pipeline.py      # Multi-agent orchestration
├── data/
│   ├── docs/                # Documentation files for RAG
│   │   ├── vault/           # HashiCorp Vault docs
│   │   └── terraform/       # Terraform docs
│   ├── vault_urls.txt       # URLs to scrape (Vault)
│   └── terraform_urls.txt   # URLs to scrape (Terraform)
└── tests/                   # Unit tests
```

## Key Features

### Intelligent Document Chunking
- 800-word chunks with 100-word overlap preserve context across boundaries
- Never cuts mid-sentence
- Maintains semantic coherence for better retrieval

### Metadata-Rich Indexing
- Every document chunk: product, source file, chunk index
- Every transcript: account, date, stage, products, sentiment
- Enables filtered searches: "Find Vault docs about Kubernetes auth"

### Context-Aware Analysis
- Searches past calls by stage: "Show me other POC deals"
- Filters by product: "Find calls where Terraform was discussed"
- Sentiment matching: "Any cautious/at-risk deals we turned around?"

### Structured Output Format
The generated email follows a consistent template:
- Executive Summary (3-4 key takeaways)
- Technical Concerns & Documentation (each concern with context, docs, recommendations)
- Recommended Next Steps (prioritized with ownership)
- Resources to Share with Customer
- Internal Notes (deal health, risks, patterns)

### Extensible Design
- Add new agents by creating a new file in `src/agents/`
- Add new tools by implementing the CrewAI tool interface
- Expand documentation sources by adding URLs to the scraper
- Customize email format in `src/email/templates.py`

## Testing

```bash
# Run unit tests
pytest tests/ -v

# Test document ingestion
python -m src.rag.ingest

# Test with a sample transcript (create your own in data/)
python -m src.main --file data/your_transcript.txt
```

## How the RAG System Works

### Ingestion Pipeline
1. Read documentation files (markdown/text)
2. Split into overlapping chunks for context preservation
3. Generate embeddings using OpenAI's text-embedding-3-small
4. Store in ChromaDB with metadata

### Search Pipeline
1. User query: "secrets management for kubernetes"
2. Generate query embedding
3. Semantic similarity search across vector space
4. Filter by metadata (product, stage, etc.)
5. Return top-k results with relevance scores

### Self-Improvement Loop
1. Process call → Generate analysis
2. Store analysis with metadata
3. Future calls query past transcripts
4. System learns patterns over time
5. Better recommendations with each iteration

## Future Enhancements

- **Web UI** - Streamlit dashboard for transcript upload and analysis
- **Real-time transcription** - Integrate Whisper API for audio → text
- **CRM integration** - Push deal health and actions to Salesforce
- **Team analytics** - Aggregate insights across all calls
- **Competitive intelligence** - Dedicated analysis for competitor mentions
- **Slack/Teams bots** - Post summaries to channels automatically

## Why This Approach Works

**Multi-agent > single LLM**: Breaking the task into specialized agents produces higher-quality output than asking one LLM to "do everything." Each agent has focused instructions and only the tools it needs.

**RAG > fine-tuning**: Fine-tuning is expensive and becomes stale. RAG stays current — just update the documentation and it immediately improves responses.

**ChromaDB > cloud vector DB**: For a portfolio project, local storage is simpler, free, and sufficient. Production scale would use Pinecone or Weaviate.

**Sequential > parallel**: While parallel agents are faster, sequential processing is more reliable when tasks depend on previous outputs (email composition needs the research results).

## License

MIT

---

Built to demonstrate AI engineering: multi-agent systems, RAG architecture, and practical automation of real business workflows.
