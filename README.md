# Conservation Document Intelligence

A deployable research prototype that organizes 35 public conservation sources, searches page-aware evidence, extracts conservation entities and relations, presents an evidence-backed wiki, and produces citation-checked chatbot answers.

The supplied project description and deployment guide are the requirements source of truth. [ROADMAP.md](ROADMAP.md) records the implementation architecture and acceptance gates.

## Documentation

- [Technical implementation report](TECHNICAL_IMPLEMENTATION_REPORT.md)
- [User manual](USER_MANUAL.md)
- [Deployment guide](DEPLOYMENT.md)
- [Implementation roadmap](ROADMAP.md)
- [Evaluation and status reports](outputs/requirements_evaluation.md)

## Status

The runtime corpus and precomputed retrieval artifacts are implemented. The document-defined demonstration, relation, wiki, and known-set chatbot regression gates pass. The final fresh J01-J20 holdout scored 11 PASS / 4 PARTIAL / 5 FAIL, so the deployed system must remain labelled as a research prototype and must not be represented as production-ready:

- 35/35 catalog sources acquired and extracted
- 724 deterministic, page-aware chunks in SQLite/FTS5
- 6,795 entity mentions and 987 high-precision, evidence-linked relations
- 15 validated wiki pages across species, habitats, locations, threats, and agencies; 44/44 facts trace to stored evidence and 84/84 internal links resolve
- five working Streamlit tabs: Corpus, Search, Wiki, Chatbot, and Evaluation
- a current 724-vector, 1,536-dimensional FAISS semantic index
- 139 automated tests passing
- all 10 document-defined questions plus 5 engineering checks in the saved live evaluation
- a completed five-answer manual citation audit and document-rubric report
- full official-answer audit: 10 PASS, 0 PARTIAL, 0 FAIL
- relation-quality audit: 987/987 integrity checks and 37/37 manually reviewed rows passing
- wiki-quality audit: 15/15 pages and 44/44 manually reviewed facts passing
- post-repair H, F, and G 20-question regression sets: 16/16 supported answers and 4/4 intended abstentions on each set
- provisional document-rubric self-score: 95/100 (internal deployment threshold: 90/100)

`OPENAI_API_KEY` is optional for corpus, keyword-search, wiki, and saved-evaluation browsing. It is required for live query embeddings, chatbot answers, and rebuilding the FAISS index. Publication to Streamlit Community Cloud requires the owner's GitHub and Streamlit accounts.

See [outputs/status_report.md](outputs/status_report.md) for readiness, [outputs/demo_answers.md](outputs/demo_answers.md) for the document-defined live evaluation, [outputs/full_demo_correctness_audit.md](outputs/full_demo_correctness_audit.md) for its complete answer audit, [outputs/scope_repair_regression_audit.md](outputs/scope_repair_regression_audit.md) for the H/F/G repair evidence, [outputs/holdout_v4_first_run_audit.md](outputs/holdout_v4_first_run_audit.md) for the latest immutable untouched-holdout result, [outputs/holdout_first_run_audit.md](outputs/holdout_first_run_audit.md) for the original first-run history, [outputs/relation_quality_audit.md](outputs/relation_quality_audit.md) for Gate 2 evidence, [outputs/wiki_quality_audit.md](outputs/wiki_quality_audit.md) for Gate 3 evidence, and [outputs/requirements_evaluation.md](outputs/requirements_evaluation.md) for the rubric score.

## Quick start

Python 3.12 is the tested Streamlit Community Cloud deployment target.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
cp .env.example .env
python scripts/00_initialize.py
python -m pytest -q
streamlit run app.py
```

The versioned `db/conservation.db` is the complete runtime corpus, so the app does not download or process documents at startup. Open <http://localhost:8501> for local Streamlit or use Docker port 7860.

## Capabilities

| Area | Implementation | Credential-free |
|---|---|---|
| Corpus | searchable/filterable 35-source catalog with public links and provenance | Yes |
| Keyword retrieval | SQLite FTS5 with page-aware evidence snippets | Yes |
| Semantic retrieval | current persisted FAISS index using OpenAI embeddings | Live query/rebuild requires API key |
| Structured knowledge | rule-based typed entities and five required relation types, each tied to evidence | Yes |
| Wiki | 15 evidence-ranked Markdown pages with cited facts, qualified relationships, and validated internal links | Yes |
| Chatbot | Responses API answer generation, retrieved-context-only prompt, citation allow-list validation, and abstention | Requires API key |
| Evaluation | 15 saved document/engineering cases, three 20-question known regression sets, reviewer rubrics, artifact audits, and feedback link | Yes |

## Rebuild pipeline

Normal app startup reads precomputed artifacts. To rebuild from the public sources:

```bash
python scripts/00_initialize.py
python scripts/00_apply_source_replacements.py
python scripts/01_download_sources.py
python scripts/02_extract_text.py
python scripts/03_build_chunks.py
python scripts/05_extract_entities.py
python scripts/06_generate_wiki.py --per-category 3
python scripts/07_evaluate.py
python scripts/08_validate_project.py
```

Rebuild the semantic index after setting `OPENAI_API_KEY`:

```bash
python scripts/04_build_vector_index.py
```

Generate live model answers in the evaluation report with:

```bash
python scripts/07_evaluate.py --with-openai
```

Acquisition and processing steps are resumable. Use each command's `--help` option for document-specific or forced rebuild options.

## Configuration and secrets

Copy `.env.example` for local development. On Streamlit Community Cloud, add root-level TOML values in the app's **Secrets** settings. Root-level secrets are exposed to the application as environment variables.

- `OPENAI_API_KEY`: enables chatbot answers and index construction
- `OPENAI_CHAT_MODEL`: optional override; default is `gpt-4.1-mini`
- `OPENAI_EMBEDDING_MODEL`: optional override; default is `text-embedding-3-small`
- `VECTOR_STORE_ID`: reserved for the optional hosted retrieval adapter
- `FEEDBACK_FORM_URL`: public external survey URL shown in the Evaluation tab

Never commit `.env` or `.streamlit/secrets.toml`.

## Source provenance

The canonical record is [data/metadata.csv](data/metadata.csv). Original URLs are retained even when a broken source required an official replacement, archived official copy, or representative public DocumentCloud record. All substitutions and verification links are explicit in [data/source_replacements.csv](data/source_replacements.csv).

DOC007 and DOC008 intentionally resolve to byte-identical copies of the same DOI report because the required source list includes both its landing-page and direct-PDF entries. The audit surfaces this instead of silently removing a required ID.

Raw downloads and extracted page files are rebuildable and excluded from the deployment image. Their checksums, resolved URLs, extraction counts, and status remain in the catalog; the compact derived SQLite corpus is versioned for deterministic startup.

## Project layout

```text
app.py                         Streamlit entry point
config.yaml                    Pipeline and runtime defaults
data/metadata.csv              35-source catalog and processing provenance
db/conservation.db             Precomputed runtime corpus and FTS index
scripts/                       Reproducible pipeline and audit commands
src/conservation_intelligence/ Testable application and pipeline modules
vector_index/                  Persisted FAISS index and current-corpus manifest
wiki/                          Generated, reviewable Markdown knowledge pages
outputs/                       Structured exports, evaluation, and status report
tests/                         Unit/integration/app smoke tests and questions
```

## Deployment

The primary deployment target is Streamlit Community Cloud. Use `app.py` as the entrypoint and Python 3.12; dependencies, the SQLite corpus, FAISS index, and wiki are versioned in the repository so startup performs no downloads or indexing. Detailed GitHub, secrets, deployment, smoke-test, and rollback instructions are in [DEPLOYMENT.md](DEPLOYMENT.md). The Dockerfile remains available for optional container hosting.

The official-answer, relation-quality, wiki-quality, and known-set chatbot regression gates are complete, and the provisional document-rubric score exceeds the internal threshold. The final fresh holdout did not pass: five answerable questions falsely abstained even though usable expected evidence was retrieved. The app may be published for transparent research demonstration with this limitation disclosed. Independent conservation-domain review remains recommended before any consequential or production use.

## Limitations

- The rule-based entity layer favors auditability over exhaustive recall and has not received domain-expert validation.
- Four wiki pages retain one publishable fact rather than padding them with noisy extraction fragments; repeated co-mentions are explicitly labelled as non-semantic corpus associations.
- The saved live evaluation is a self-evaluation, not an independent domain-expert assessment; the five-answer citation audit is recorded in `outputs/manual_citation_audit.md`.
- The first frozen holdout found a high false-abstention rate on answerable paraphrases and one materially unsupported generated answer. Its immutable first-run record is in `outputs/holdout_first_run_audit.md`.
- Live semantic queries and answers depend on the configured OpenAI API and can be affected by model/service changes; citation and abstention checks remain deterministic.
- The prototype is not an authoritative conservation decision system. Verify consequential claims against the linked source and cited pages.

## Research prototype notice

This system uses public documents and AI-assisted answering. Generated content can contain errors. Verify important conclusions against the linked source documents and inspect the cited evidence.
