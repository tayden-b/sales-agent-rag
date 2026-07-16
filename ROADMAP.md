# Roadmap

Where this project is headed and what to pick up next. Work the top unchecked
item first. When something ships, check it off and move it to Done with the date.
Keep items small enough to land as one focused PR.

## Goal

Take this from a script that works on my machine to a pipeline someone else
can run and trust: a bundled sample transcript that demos end-to-end with one
command, schema-validated agent outputs instead of free prose between agents,
and an eval that measures extraction accuracy. Scope stays distinct from
hashi-agent-rag — this repo is call-transcript intelligence; that one is the
docs knowledge agent.

## Next up

- [ ] Tests for chunking and the ChromaDB metadata written by the knowledge
      base updater — fixture-based, no API calls.
- [ ] CI: lint + the no-network tests on push. (Partly done: the extraction
      eval already runs in its own `extraction-eval` workflow. This item is now
      about a lint step and running the rest of the no-network suite.)
- [ ] README trim: it currently reads like a product page. Cut it to what it
      does, how to run the demo, the architecture in ~10 lines, and what I
      learned about multi-agent orchestration. Keep the "why I built this."

## Later

- [ ] Deal-health scoring made explicit: a visible rubric (config or prompt
      section) instead of vibes inside a prompt.
- [ ] Batch mode: point it at a folder of transcripts, get a digest.
- [ ] Revisit whether CrewAI is earning its weight here vs. plain function
      calls — measure, don't guess.

## Done

- [x] Extraction eval: hand-labeled the sample transcript in
      `data/eval/gold_labels.json` (expected concerns, action items, sentiment
      as keyword rubrics), and `src/eval.py` scores an analyzer extraction
      against it — recall/precision/F1 per field plus sentiment accuracy — and
      prints a scorecard. `python -m src.eval` runs the analyzer live when
      `OPENAI_API_KEY` is set, otherwise scores a recorded prediction fixture so
      it works offline. Runs in CI via the `extraction-eval` workflow and a
      no-network test (`tests/test_eval.py`). Factored a `run_analyzer` helper
      out of the pipeline so the eval can score extraction without running the
      email agents. On the current fixture: concerns 6/7 recall, actions 3/4,
      sentiment correct. (2026-07-14)
- [x] Structured outputs: Pydantic schemas (`src/schemas.py`) for what the
      Transcript Analyzer hands downstream — concerns with severity, action
      items with owners — wired into the analyze task via `output_pydantic` so
      a malformed extraction fails at the boundary instead of poisoning the
      email. Downstream account/date now read off the validated model instead
      of a hand-rolled `json.loads`. (2026-07-10)
- [x] One-command demo: bundled a realistic sample transcript at
      `data/sample_transcript.txt` and a `python -m src.demo` entrypoint that
      runs the full pipeline on it. (2026-07-07)
