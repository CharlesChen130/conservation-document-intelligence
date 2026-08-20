# Deployment guide

The primary deployment target is Streamlit Community Cloud. It runs `app.py` from the repository root and reads the precomputed `db/conservation.db`; normal startup does not download, extract, or re-index the corpus.

## 1. Pre-deployment verification

From a clean Python 3.12 environment:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/08_validate_project.py
```

Expected core counts are 35 documents, 724 chunks, 6,795 entity mentions, 987 relations, and 15 wiki pages. A warning that DOC007 and DOC008 are byte-identical is expected and documented.

Run the exact cloud entrypoint locally:

```bash
streamlit run app.py
```

Open <http://localhost:8501> and confirm that `/_stcore/health` returns a healthy response.

Docker remains available as an optional second packaging check:

```bash
docker build -t conservation-intelligence .
docker run --rm -p 7860:7860 --env-file .env conservation-intelligence
```

## 2. Publish to the private GitHub repository

The configured repository is `https://github.com/CharlesChen130/conservation-document-intelligence`.

```bash
git add .
git commit -m "Build conservation document intelligence prototype"
git branch -M main
git remote add origin https://github.com/CharlesChen130/conservation-document-intelligence.git
git push -u origin main
```

Sign in at <https://share.streamlit.io/> and connect the GitHub account that administers the repository.
Grant Streamlit access to private repositories. When creating the app, use:

- Repository: `CharlesChen130/conservation-document-intelligence`
- Branch: `main`
- Main file path: `app.py`
- Python version: `3.12`
- App URL: choose an available `*.streamlit.app` subdomain

## 3. Configure runtime settings

In Streamlit Community Cloud, open **Advanced settings**, then paste root-level TOML into **Secrets**:

```toml
OPENAI_API_KEY = "your-project-api-key"
# Optional overrides:
# OPENAI_CHAT_MODEL = "gpt-4.1-mini"
# OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
# FEEDBACK_FORM_URL = "https://example.com/feedback"
```

Keep these values at the TOML root so the current application can read them as environment variables.
Do not put credentials in the Dockerfile, README, `.env.example`, `.streamlit/secrets.toml`, or repository history.

## 4. Semantic search choice

Keyword retrieval and the chatbot's evidence retrieval work from bundled SQLite without an embedding index. To enable the app's **Semantic** search mode, build and commit the FAISS artifacts before deployment:

```bash
export OPENAI_API_KEY=...
python scripts/04_build_vector_index.py
git add vector_index/chunks.faiss vector_index/manifest.json
git commit -m "Build semantic corpus index"
git push origin main
```

The manifest hashes the corpus and records the embedding model; stale indexes are disabled automatically.

## 5. Acceptance test after deployment

- Corpus tab shows 35 records and working public-source links.
- Keyword search returns cited, page-aware evidence for `wetland restoration` and `invasive carp`.
- All 15 wiki pages render and citations use known document IDs.
- Without `OPENAI_API_KEY`, Chatbot clearly reports reduced mode and all other tabs still work.
- With the secret, ask at least five questions and inspect every claim/citation against the evidence expander and source.
- An out-of-corpus question produces the explicit insufficient-evidence response rather than an unsupported answer.
- Evaluation report downloads and the feedback link opens if configured.
- Restarting the cloud app retains the same corpus counts without rebuilding.

## 6. Operations and rollback

- The application writes only transient Streamlit/session state at runtime. Feedback is external because Community Cloud instance storage is not durable.
- The versioned database makes a restart deterministic. If a release fails, revert the GitHub repository to the prior known-good commit.
- Re-run the audit whenever metadata, chunks, entities, relations, or wiki pages change.
- Keep model choice and answer-token limits conservative; `config.yaml` caps retrieval and output size.

## Remaining owner actions

External publication requires the owner's GitHub and Streamlit Community Cloud authentication. The OpenAI key must be entered directly in Streamlit's Secrets console and must never be committed. A feedback survey URL remains optional.
