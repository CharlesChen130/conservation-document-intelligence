# Manual citation audit

Audited artifact: `outputs/demo_answers.md` (final live API-backed run)

Reviewer: implementation self-audit. This is not a substitute for independent conservation-domain review.

## Result

Five representative official answers were checked from question to retrieved chunk to cited document/page. All five passed the four checks required by the project description.

| Official question | Retrieval relevance | Claim support | IDs/pages | Unsupported claims | Result |
|---:|---|---|---|---|---|
| 1. Documents discussing aquatic invasive species | PASS | PASS | PASS | PASS | **PASS** |
| 2. Agencies appearing most often | PASS | PASS | PASS | PASS | **PASS** |
| 5. Public documents mentioning waterfowl conservation | PASS | PASS | PASS | PASS | **PASS** |
| 6. Invasive carp and aquatic habitat management | PASS | PASS | PASS | PASS | **PASS** |
| 8. Short wetland-conservation summary | PASS | PASS | PASS | PASS | **PASS** |

## Audit notes

### Question 1

- Each of the five cited chunks explicitly contains aquatic-invasive, aquatic-nuisance, or nonindigenous-aquatic evidence.
- The returned items use exact catalog titles and application-owned citations.
- Nonmatching and negative-search-result items are removed by the document-list relevance filter.

### Question 2

- Counts were independently recomputed from the `entities` table, grouped by normalized agency name and ranked by distinct-document coverage followed by mention count.
- The recomputed top eight exactly match the answer: USFWS 133/19, USGS 84/13, MDC 115/11, Ducks Unlimited 50/11, EPA 34/11, USACE 39/9, DOI 37/9, and Convention on Wetlands 67/5 (mentions/documents).

### Question 5

- A corpus-wide SQL check found 15 documents where `waterfowl` and `conservation` occur in the same stored chunk; the answer lists those same 15 documents.
- Citations without page numbers correspond to HTML-derived records and correctly use document-only citation form.

### Question 6

- `DOC012, pp. 13-14` directly supports invasive-carp management, habitat/hydrologic conditions, and coordinated management.
- `DOC012, pp. 17-20` directly supports habitat variables, removal, monitoring, and decision support.
- `DOC006, pp. 3-4` supports the broader ecological impact and control context.

### Question 8

- The answer is a deterministic evidence brief tied to six canonical chunks.
- The Missouri SWAP chunks support the Community Health Index metrics; Ramsar supports wetland types, productivity, biodiversity, wise use, and ecological character; USGS WARC supports research/management/restoration; and the Missouri Wetland Program Plan supports inventories, indices, hydrologic monitoring, research, and restoration planning.

## Mechanical integrity checks

- Unresolved model-facing labels such as `[S1]`: **0**
- `failed` evaluation statuses: **0**
- `safety_abstention` statuses: **0**
- Official questions with substantive answers: **10/10**
- Intended out-of-scope engineering questions 14 and 15: retrieval abstention before generation

## Scope limitation

This audit samples five of the ten official answers, as required. It verifies the frozen report and the stored corpus; it does not assert that every possible future model response is domain-perfect.
