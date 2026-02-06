# Quick Start Guide

## Step 1: Set Up Your Environment

```bash
# Activate virtual environment
source venv/bin/activate

# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Or add it to .env
echo "OPENAI_API_KEY=your-key-here" >> .env
```

## Step 2: Load Documentation

You have three options:

### Option A: Use the Pre-Included Sample Docs (5 files)

```bash
python -m src.rag.ingest
```

Fast and simple — good for initial testing.

### Option B: Scrape a Few Key Pages

```bash
# Edit the URL file to include just the pages you want
nano data/vault_urls.txt

# Scrape and auto-ingest
python -m src.rag.scrape --product vault --urls data/vault_urls.txt
```

This fetches live documentation from HashiCorp's website.

### Option C: Scrape Everything (Recommended for Production Use)

```bash
# Scrape all Vault docs (currently 17 URLs in vault_urls.txt)
python -m src.rag.scrape --product vault --urls data/vault_urls.txt

# Scrape all Terraform docs (currently 11 URLs in terraform_urls.txt)
python -m src.rag.scrape --product terraform --urls data/terraform_urls.txt
```

**To add more documentation URLs:**
1. Open `data/vault_urls.txt` or `data/terraform_urls.txt`
2. Add one URL per line (lines starting with `#` are ignored)
3. Run the scraper again

The scraper will automatically skip URLs that have already been scraped (based on filename).

## Step 3: Process a Call Transcript

### Test with the Sample Transcript

```bash
python -m src.main --file data/sample_transcripts/acme-corp-evaluation.txt
```

This will:
1. Analyze the transcript (extract account info, concerns, action items, sentiment)
2. Search the documentation for relevant information
3. Search past transcripts for similar situations (empty on first run)
4. Compose a formatted email
5. Print the email to your console (EMAIL_PREVIEW_MODE=true by default)
6. Store the transcript in the knowledge base for future reference

Expected processing time: **1-3 minutes** for a typical transcript.

### Process Your Own Transcript

```bash
# From a file
python -m src.main --file /path/to/your/transcript.txt

# Or paste interactively
python -m src.main --paste
# (Paste your transcript, then press Ctrl+D on Mac/Linux or Ctrl+Z on Windows)
```

## Step 4: Review the Email

By default, `EMAIL_PREVIEW_MODE=true`, so the email will be printed to your console.

Example output:
```
======================================================================
EMAIL PREVIEW (not sent)
======================================================================
From: noreply@yourdomain.com
To:   you@yourdomain.com
Subject: Call Summary: Acme Corp - 2026-02-04
----------------------------------------------------------------------

## Executive Summary
- Acme Corp is evaluating Vault and Terraform...
- Key concerns: secrets management for 200 microservices...
- Decision timeline: End of Q1, implementation in Q2

## Technical Concerns & Documentation
...

======================================================================
```

## Step 5: Send Real Emails (Optional)

Once you're happy with the output:

1. Get a SendGrid API key (free tier: 100 emails/day)
2. Add to `.env`:
   ```
   SENDGRID_API_KEY=your-sendgrid-key
   EMAIL_FROM=noreply@yourdomain.com
   EMAIL_TO=you@yourdomain.com
   EMAIL_PREVIEW_MODE=false
   ```
3. Run the pipeline — emails will now be sent via SendGrid

## Next Steps

### Add More Documentation

The more documentation you load, the better the system gets at finding relevant information.

```bash
# Find documentation URLs from HashiCorp's website
# Add them to data/vault_urls.txt or data/terraform_urls.txt
# Run the scraper

python -m src.rag.scrape --product vault --urls data/vault_urls.txt
```

### Process More Transcripts

Each processed transcript:
- Gets stored in the knowledge base
- Becomes searchable for future calls
- Helps the Historical Context Analyst find patterns

The system gets smarter with every call you process.

### Customize Agent Behavior

Edit the agent definitions in `src/agents/` to adjust:
- The analysis depth
- The email format
- The documentation search strategy

## Troubleshooting

### "No documentation found" in the email

The `hashicorp-docs` collection is empty. Run:
```bash
python -m src.rag.ingest
```

### "No past transcripts found" in Historical Context section

This is normal for the first few calls. The knowledge base grows as you process more transcripts.

### Scraper fails to extract content

Some pages may have unusual HTML structures. Check the logs and add site-specific extraction rules in `src/rag/scrape.py` if needed.

### Python version error

CrewAI requires Python 3.10-3.13. If you have Python 3.14, create the venv with 3.12:
```bash
/opt/homebrew/bin/python3.12 -m venv venv
```

## Performance Notes

- **First run**: Slower because it needs to embed the transcript and search (cold start)
- **Subsequent runs**: Faster due to ChromaDB's persistent storage and LLM warm-up
- **Typical transcript (2000-5000 words)**: 1-3 minutes end-to-end
- **Very long transcripts (>10,000 words)**: 3-5 minutes

The bottleneck is LLM API calls, not the RAG system.
