# Wiki quality audit

Requirements source: `Document_Intelligence_Project_Description.docx`, Step 8 and the LLM Wiki rubric category.

**Gate result:** PASS

This is a project self-audit, not an independent conservation-domain review. PASS means the generated wiki satisfies the document-defined structure, citation, consolidation, and navigation outcomes without publishing known extraction fragments as facts.

## Before and after

| Measure | Before Gate 3 | After Gate 3 |
|---|---:|---:|
| Generated pages | 15 | 15 |
| Required category folders represented | 5/5 | 5/5 |
| Published key facts | 60 | 44 |
| Pages whose facts cite at least two documents | 5/15 | 11/15 |
| Obvious TOC/bibliography/list fragments in key facts | 4 | 0 |
| Explicit semantic-relation entries | 0 | 5 |
| Qualified cross-document co-mention entries | 0 | 115 |
| Raw chunk-co-occurrence entries presented as relationships | 120 | 0 |
| Internal wiki links | 0 | 84 |

The lower fact count is intentional. The generator now omits incomplete or noisy evidence instead of padding a page. Four pages retain one strong fact because no second extracted sentence met the same publication threshold.

## Automated audit

- Page count and category balance: **15/15 PASS**; three pages each in species, habitats, locations, threats, and agencies.
- Required sections and entity front matter: **15/15 PASS**.
- Summary, key-fact, related-document, related-entity, and evidence attribution rules: **15/15 PASS**.
- Key facts traced to the exact normalized entity evidence, document, and page stored in SQLite: **44/44 PASS**.
- Unknown corpus citations: **0**.
- Duplicate key facts: **0**.
- TOC, bibliography, document-scaffolding, incomplete-sentence, unbalanced-parenthesis, and misleading chunk-relationship failures: **0**.
- Internal Markdown links resolving to a currently generated wiki page: **84/84 PASS**.
- Obsolete generated pages are removed during regeneration; manually authored pages without `generated: true` are preserved.
- Focused and corpus-wide wiki tests: **5/5 PASS**.
- Complete automated suite after regeneration: **70/70 PASS**.

## Page-level results

| Page | Category | Facts | Fact documents | Explicit relations | Qualified co-mentions | Internal links | Result |
|---|---|---:|---:|---:|---:|---:|---|
| Bighead carp | species | 1 | 1 | 0 | 8 | 4 | **PASS** |
| Hydrilla | species | 1 | 1 | 0 | 8 | 4 | **PASS** |
| Invasive carp | species | 1 | 1 | 1 | 7 | 6 | **PASS** |
| Forest | habitats | 4 | 4 | 0 | 8 | 6 | **PASS** |
| Marsh | habitats | 1 | 1 | 1 | 7 | 6 | **PASS** |
| Wetland | habitats | 4 | 4 | 1 | 7 | 5 | **PASS** |
| Canada | locations | 4 | 3 | 0 | 8 | 6 | **PASS** |
| North America | locations | 4 | 4 | 0 | 8 | 6 | **PASS** |
| United States | locations | 4 | 4 | 0 | 8 | 7 | **PASS** |
| Climate change | threats | 2 | 2 | 1 | 7 | 6 | **PASS** |
| Disease | threats | 3 | 3 | 0 | 8 | 5 | **PASS** |
| Invasive species | threats | 3 | 2 | 0 | 8 | 6 | **PASS** |
| Missouri Department of Conservation | agencies | 4 | 4 | 0 | 8 | 5 | **PASS** |
| U.S. Fish and Wildlife Service | agencies | 4 | 4 | 0 | 8 | 6 | **PASS** |
| U.S. Geological Survey | agencies | 4 | 4 | 1 | 7 | 6 | **PASS** |

## Manual semantic review

All 44 published facts were read in their rendered page context. Each was judged to be a coherent, entity-relevant claim or source recommendation and to retain the meaning of its cited evidence after whitespace, ligature, acronym, and line-break dehyphenation. No fact was accepted solely because it had a valid citation.

The five explicit semantic entries use only the high-precision relation types audited in `outputs/relation_quality_audit.md`. The other 115 entries require co-mention in at least two documents and are visibly labelled as corpus associations, with the statement that they are not inferred semantic relationships.

## Implemented controls

- Candidate entities remain ordered by document coverage and mention frequency, but an entity must have at least one publishable evidence sentence.
- Evidence is document-diversified, normalized for safe PDF extraction artifacts, deduplicated by content, and filtered for completeness and document scaffolding.
- Related-entity links prefer explicit evidence-backed semantic relations. Repeated co-mentions are a separately labelled fallback and carry citations to at least two documents.
- Links are emitted only when the related entity has a current generated page; all other names remain plain text.
- Regeneration removes only obsolete files explicitly marked `generated: true`, preventing stale inventory without overwriting manual notes.

## Remaining limitations

- Four pages have one retained fact because the extractive corpus evidence did not support a second clean statement; the generator does not invent or repair missing claims.
- The pages use deterministic evidence-ranked extractive synthesis rather than model-authored prose. This improves auditability but produces less fluent consolidation than a fully reviewed LLM summary.
- Repeated co-mentions are useful navigation signals, not semantic relations, and are labelled accordingly.
- Minor source-level OCR wording remains where the claim is still understandable and source-faithful.
- No conservation-domain expert has independently reviewed the pages.
