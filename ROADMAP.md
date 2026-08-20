# Conservation Document Intelligence Prototype — Implementation Roadmap

## Goal

Build a reproducible Streamlit research prototype that organizes the 35 required public conservation sources, extracts page-aware text and structured conservation knowledge, generates evidence-backed wiki pages, and answers natural-language questions using inspectable source citations. Package the completed application for later deployment as a Docker-based Hugging Face Space.

The two supplied DOCX files are the source of truth. Where they allow alternatives, the defaults below keep the system small, testable, and deployable.

## Implementation snapshot

Phases 0–6 are implemented for the full 35-source corpus. The document-defined live evaluation and full official-answer self-audit are complete, and the relation-quality and wiki-quality repair gates pass. Phase 7 quality hardening is reopened because the corrected exact-chunk review of the first frozen 20-question holdout scored 7 PASS, 1 PARTIAL, and 12 FAIL, dominated by false abstentions on answerable paraphrases. The next work is a generic scope/claim-validation repair followed by a newly frozen holdout. Phase 8 packaging is present, but deployment remains gated on that quality repair, locally unavailable Docker, and the owner's Hugging Face credentials. Current evidence is recorded in `outputs/status_report.md`, `outputs/holdout_first_run_audit.md`, and `outputs/holdout_failure_analysis.md`.

## Definition of done

The project is complete when all of the following are true:

- `metadata.csv` contains traceable records for `DOC001` through `DOC035`, including documented failures and substitutions.
- Available documents have page-aware extracted text and reproducible chunks.
- Keyword and semantic search return snippets with document IDs, source URLs, and pages where available.
- Entity and relationship outputs link every result to supporting chunks.
- At least 10 useful wiki pages contain source-backed facts, related entities/documents, evidence, and open questions.
- The Streamlit app provides Corpus, Search, Wiki, Chatbot, and Evaluation tabs.
- Chatbot answers are restricted to retrieved evidence, use citations such as `[DOC012, p. 5]`, and explicitly abstain when evidence is insufficient.
- The required demo questions have recorded results and manually checked citations.
- Tests, setup documentation, Docker packaging, secret handling, and Hugging Face Space metadata are complete.
- The app runs after a clean install and survives a container restart without rebuilding its corpus at startup.

## Architecture and default choices

### Offline build pipeline

`source catalog -> acquisition -> text extraction -> chunks -> SQLite/search index -> entities/relations -> wiki pages -> evaluation artifacts`

The expensive and potentially fragile processing steps run through scripts and produce versioned artifacts. The deployed application reads those artifacts instead of downloading or rebuilding the corpus during startup.

### Runtime application

`Streamlit UI -> retrieval service -> cited evidence -> answer service`

The UI will not contain core data-processing logic. Search, citation formatting, wiki access, and answering will be implemented in testable modules.

### Technology defaults

- Python 3.11
- Streamlit for the user interface
- SQLite plus FTS5 for documents, chunks, structured outputs, and keyword search
- A small local persisted semantic index as the reproducible default
- Provider adapters for embeddings and answer generation, configured through environment variables
- OpenAI File Search as an optional hosted retrieval backend, not a hard dependency on day one
- `pypdf` for PDF extraction and BeautifulSoup for HTML extraction
- Pydantic-style schemas or equivalent validation for LLM structured output
- Pytest for unit, integration, and smoke tests
- Docker on port 7860 for Hugging Face Spaces

Exact dependency versions and the local vector implementation will be selected during scaffolding after compatibility checks. All provider-dependent features must fail clearly when credentials are absent; corpus browsing, wiki browsing, and keyword search should remain usable where practical.

## Execution phases

### Phase 0 — Repository foundation

Deliverables:

- Initialize the repository and prescribed directory layout.
- Add `README.md`, `requirements.txt` or equivalent lockable dependency specification, `.gitignore`, `.env.example`, `config.yaml`, and `Dockerfile` placeholder.
- Add a `src/` package for reusable logic and keep numbered scripts as thin entry points.
- Add project-root-relative path handling, structured logging, and configuration validation.
- Create an idempotent SQLite schema initializer implementing the required tables and useful indexes.
- Create a minimal Streamlit shell with the five required tabs.
- Establish a test suite and a single command for local checks.

Acceptance gate:

- Clean environment installation succeeds.
- Database initialization is repeatable.
- Unit tests pass.
- Streamlit starts and renders all five placeholder tabs.

### Phase 1 — Corpus catalog and acquisition

Deliverables:

- Transcribe the complete 35-row dataset into `data/metadata.csv`.
- Add fields needed for provenance: original URL, resolved/final URL, retrieval date, checksum, HTTP status, status, and substitution notes while retaining all required columns.
- Implement resumable acquisition with timeouts, retries, descriptive user agent, content-type checks, and deterministic filenames.
- Save direct PDFs and useful HTML/text snapshots under `data/raw/`.
- For collection/search pages, select one representative public document and record the choice.
- Produce an acquisition report without hiding unavailable or replaced sources.

Acceptance gate:

- Exactly 35 unique IDs exist.
- At least 25 sources are acquired or validly represented, matching the Week 1 requirement.
- Every unsuccessful source has a recorded reason; every replacement preserves the same agency/topic intent and both URLs.
- Re-running acquisition does not redownload unchanged files unnecessarily.

### Phase 2 — Text extraction and normalization

Deliverables:

- Extract text from PDFs page by page with visible page separators.
- Extract meaningful content from saved HTML/text while removing navigation boilerplate where possible.
- Record page count, character count, extraction method, warnings, and failures.
- Detect nearly empty/scanned PDFs and expose an optional OCR path if needed.
- Save normalized UTF-8 text under `data/processed/DOCxxx.txt`.

Acceptance gate:

- Text extraction works for at least 15 documents first, then all usable acquired sources.
- Extracted pages retain stable source-page identifiers.
- Empty, corrupt, or suspicious extraction results are reported instead of silently indexed.

### Phase 3 — Chunking, database, and retrieval

Deliverables:

- Create deterministic 600–900-word chunks with approximately 100-word overlap without crossing document boundaries.
- Store document and chunk records in SQLite with `doc_id`, `chunk_id`, page/page range, text, title, topic, agency, and source URL.
- Implement SQLite FTS5 keyword search.
- Build a persisted semantic index and an embedding manifest that records model and content hashes.
- Implement a common retrieval interface supporting keyword, semantic, and later hosted backends.
- Add metadata filters and hybrid ranking if it materially improves the required questions.

Acceptance gate:

- Every indexed chunk maps to exactly one document and inspectable source location.
- Index creation is incremental or safely repeatable.
- Search returns title, document ID, URL, page, score, and snippet.
- A fixed retrieval test set produces relevant evidence for the core wetland, invasive-species, waterfowl, and Missouri-planning questions.

### Phase 4 — Entity and relationship extraction

Deliverables:

- Define validated entity types: species, habitat, river, wetland, agency, location, threat, program, policy, and date.
- Define the required relationship types and a small extension policy if useful relations are discovered.
- Combine deterministic extraction for simple cases with schema-constrained LLM extraction for ambiguous cases.
- Normalize aliases, capitalization, abbreviations, and duplicate entities while preserving the original mention.
- Store confidence, evidence, document ID, and chunk ID for every extracted item.
- Export `outputs/entities.csv` and `outputs/relations.csv` from canonical database records.

Acceptance gate:

- CSV schemas are stable and validated.
- Every relation includes inspectable supporting evidence.
- A manually reviewed sample across several documents shows understandable, useful results with duplicates controlled.
- Pipeline behavior is documented when no LLM key is configured.

### Phase 5 — Evidence-backed LLM Wiki

Deliverables:

- Rank candidate entities by frequency, source diversity, and relevance to required demo questions.
- Generate 10–20 Markdown pages across the required category folders.
- Include summary, key facts, related documents, related entities, evidence snippets, open questions, and citations on every factual statement.
- Add reproducible slugs, front matter, and database records for wiki pages.
- Implement link validation and citation validation.
- Build the Streamlit Wiki browser.

Acceptance gate:

- At least 10 pages pass structural and citation checks.
- Wiki facts can be traced to stored chunks.
- Related-document and related-entity navigation works.
- Regeneration is safe and produces a reviewable change rather than silently overwriting curated content.

### Phase 6 — Streamlit product and grounded chatbot

Deliverables:

- Corpus tab with filters, source links, and processing status.
- Search tab with keyword/semantic modes, metadata filters, snippets, scores, and citation details.
- Wiki tab with category navigation and rendered Markdown.
- Chatbot tab with conversation state, retrieval inspection, source links, and cited answers.
- Evaluation tab with required questions, saved evaluation artifacts, and an external-feedback link placeholder.
- Research prototype disclaimer and visible configuration diagnostics.
- Prompt and post-generation checks that require supported citations and explicit insufficient-evidence responses.
- Sensible limits for query and response length, retrieval size, retries, and provider errors.

Acceptance gate:

- All five tabs work with project-relative paths.
- Every factual chatbot answer contains valid corpus citations.
- Invalid or invented document IDs are rejected or surfaced as an error.
- Evidence-poor questions trigger an abstention rather than unsupported prose.
- The app remains useful in a reduced mode when optional API configuration is absent.

### Phase 7 — Evaluation and quality hardening

Deliverables:

- Add the 10 required demo questions and 5 useful edge/adversarial questions.
- Capture retrieved chunks, generated answers, latency, citations, and reviewer notes in `outputs/demo_answers.md` or a generated equivalent.
- Add automated checks for metadata integrity, database references, index freshness, wiki structure, citation syntax, cited-document existence, and app startup.
- Manually verify the chain `claim -> citation -> source evidence` for the final demonstration set.
- Document limitations, failed sources, substitutions, known weak answers, and reproducibility steps.

Acceptance gate:

- All required questions have recorded pass/fail outcomes.
- At least five representative chatbot answers are fully citation-audited for the demo.
- Critical tests pass from a clean checkout/build.
- No secret, local absolute path, or private document is present.

### Phase 8 — Hugging Face packaging and handoff

Deliverables:

- Finalize the Python 3.11 slim Docker image and Streamlit port 7860 configuration.
- Add Hugging Face Space front matter to the README.
- Prepackage metadata, database/index artifacts as appropriate, wiki pages, entities, relations, and evaluation material.
- Configure `OPENAI_API_KEY`, optional `VECTOR_STORE_ID`, model selection, and feedback URL through environment variables only.
- Test container build, startup, health, all tabs, citation links, missing-secret behavior, and restart behavior.
- Add deployment steps, testing instructions, known limitations, and cost-control guidance.

Acceptance gate before external deployment:

- Docker image builds and runs locally.
- The app does not download or rebuild the corpus at normal startup.
- API credentials exist only in deployment secrets.
- Basic CPU hosting is sufficient.
- The deployment acceptance checklist from the supplied guide is satisfied except for items requiring the owner's accounts or external reviewers.

## Autonomous working rules

During implementation I can independently:

- choose small internal libraries and module boundaries;
- repair or replace broken public-source URLs while documenting provenance;
- improve schemas without removing required fields;
- add tests, fixtures, caches, validation, and developer documentation;
- use a small corpus subset to prove each vertical slice, then scale it;
- change a recommended implementation detail when compatibility or reliability requires it, while preserving the stated outcomes.

I will stop and request input only when progress requires authority or information I cannot safely infer, principally:

- an OpenAI API key or approval of another paid model/embedding provider;
- a Hugging Face account/Space and permission to publish or push;
- a GitHub destination and permission to push, if remote publication is desired;
- selection or access to an external survey service;
- acceptance of material ongoing API cost or public exposure.

The system will be designed and tested locally before any of those external actions are required.

## Progress tracking

At the end of each phase:

1. Run the phase's automated and smoke tests.
2. Record completed deliverables and known issues in the README or a generated status report.
3. Keep generated-data provenance visible.
4. Move forward only after the acceptance gate is met, or document why a noncritical exception is safe.

## Recommended implementation order

The first end-to-end slice will use 3–5 diverse documents and exercise acquisition, page extraction, chunking, search, one extraction pass, one wiki page, and one cited answer. Once that slice is reliable, the corpus will scale to all 35 records. This exposes integration and citation problems early while keeping the final pipeline identical to the full build.
