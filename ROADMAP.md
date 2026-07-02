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

- [ ] One-command demo: bundle a realistic sample transcript fixture and a
      `demo` entrypoint that runs the full pipeline on it, so the repo shows
      what it does without the reader supplying their own call data.
- [ ] Structured outputs: Pydantic schemas for what the Transcript Analyzer
      hands downstream (concerns with severity, action items with owners),
      validated at the agent boundary so a malformed extraction fails loudly
      instead of poisoning the email.
- [ ] Extraction eval: hand-label the sample transcript (expected concerns,
      action items, sentiment), score the analyzer against it, print the
      results. Run it in CI.
- [ ] Tests for chunking and the ChromaDB metadata written by the knowledge
      base updater — fixture-based, no API calls.
- [ ] CI: lint + the no-network tests on push.
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

Nothing yet — file added 2026-07-02.
