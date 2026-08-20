# Conservation Document Intelligence Project — Meeting Brief

**Current status:** The functional and document-defined requirements are implemented, but the system is **not ready for deployment** because the latest untouched holdout failed the internal quality gate.

## 1. How I used Codex

I used Codex as an end-to-end engineering and evaluation partner rather than only as a code generator. Codex:

- read the two requirement documents and converted them into a staged roadmap and acceptance gates;
- implemented the 35-source ingestion pipeline, metadata catalog, SQLite/FAISS retrieval, entity/relation layer, generated wiki, citation-grounded chatbot, tests, and Hugging Face/Docker packaging;
- configured the application to use the OpenAI API key from local `.env` without exposing it in code or reports;
- ran an iterative loop of **generic repair → automated tests → live API evaluation → manual answer/citation audit → error classification → next repair**;
- preserved each fresh holdout specification and first-run output with hashes so later tuning could not be represented as an unbiased result; and
- maintained status, rubric, audit, and deployment-readiness reports throughout the work.

The design rule was that repairs must address question types, not hard-code evaluation IDs, phrases, or document IDs. Potential deviations from the requirement documents were reserved for discussion rather than silently introduced.

## 2. How the system is evaluated

Evaluation uses several complementary layers:

1. **Document-defined evaluation:** the 10 required demo questions are manually reviewed for correctness, completeness, source/page accuracy, and unsupported claims.
2. **Automated regression testing:** 131 local tests cover retrieval, scope logic, comparison handling, citation validation, privacy, unsupported exact values, instruction resistance, and positive/near-miss cases.
3. **Artifact quality gates:** the corpus, relation layer, wiki pages, citations, internal links, database, and semantic index are validated separately.
4. **Fresh holdouts:** each round contains 20 previously unseen questions—normally 16 answerable and four that should abstain. The questions and hashes are frozen before the first execution, the set is run once without tuning, and the first-run artifacts remain immutable.
5. **Manual semantic audit:** PASS requires the correct answer/abstention behavior, complete question coverage, support for every material claim, correct source/page attribution, and no unsafe or out-of-scope content. PARTIAL indicates a grounded core answer with a material completeness or relevance defect.
6. **Post-repair replay:** old holdouts become known regression sets. They demonstrate that repairs did not re-break known behavior, but they are not treated as new blind evidence.

## 3. Evaluation rounds, errors, and repairs

| Round | First-run result | Core error classes | Repair or disposition |
|---|---:|---|---|
| Required 10-question demo | **10 PASS / 0 PARTIAL / 0 FAIL** | The questions informed development, so this is a requirements demonstration rather than an unbiased generalization estimate. | Retained as the official acceptance and regression suite. |
| H01–H20, first fresh holdout | **7 PASS / 1 PARTIAL / 12 FAIL**; 37.5% half-credit | Literal token-based scope checking caused 12 false abstentions; one answer included an unsupported inference. Retrieval returned evidence for 20/20. | Added semantic scope aliases, normalization, safer wiki-inventory routing, exact claim-span checks, and more efficient guarded fallbacks. |
| F01–F20, second fresh holdout | **15 PASS / 4 PARTIAL / 1 FAIL**; 85% half-credit | Compound facets were missed; coordinated concepts were judged too strictly; some off-topic claims and pathway drift survived; raw fallback text was noisy. | Improved facet parsing, subject binding, live-trade/pathway filters, exact extractive fallback, and claim selection by required obligation. |
| G01–G20, third fresh holdout | **13 PASS / 3 PARTIAL / 4 FAIL**; 72.5% half-credit | Literal coverage false negatives remained; one two-sided comparison missed a source; valid answers covered required facets unevenly. | Added named-side query decomposition and balanced retrieval, OR handling for genuine alternatives, grouped-phrase coverage, per-obligation selection, and paired positive/near-miss tests. |
| H/F/G after repair | **20/20 expected behavior on each set**; 131 automated tests pass | Replays caught several trade-off regressions while rules were adjusted. | Confirms breadth on known cases, but these scores are post-tuning regression evidence, not independent validation. |
| J01–J20, latest untouched holdout | **11 PASS / 4 PARTIAL / 5 FAIL**; 65% half-credit | Five answerable questions falsely abstained after valid evidence was retrieved. Four answers retained correctly cited but semantically adjacent, out-of-scope bullets. | No repair or rerun has been performed against J. J is now frozen as a known regression set and currently blocks deployment. |

The round scores should not be read as a simple performance trend because every fresh set has different questions. The repeated finding is more important: **retrieval usually finds the expected source, but the post-generation scope validator sometimes rejects valid paraphrases, while the pruning layer sometimes retains a generic neighboring detail.**

## 4. Important conclusions and current risks

- The prototype meets the document-defined functional evaluation and has a provisional internal rubric score of **95/100**.
- Current artifacts include **35 sources, 724 searchable chunks, 6,795 entity mentions, 987 relations, and 15 generated wiki pages**.
- Safety behavior is stable: all four unsupported/privacy/instruction-resistance questions in every fresh round abstained correctly.
- In the latest J holdout, usable expected evidence was retrieved for **16/16 answerable questions**. Therefore, the present bottleneck is primarily answer validation and relevance pruning—not corpus coverage or citation provenance.
- The substantive J answers used valid document/page citations, and no fabricated citation, exact statistic, causal result, credential, or live-web answer was found.
- The 10/10 demo and repaired 20/20 regression scores are valuable but must not be presented as proof of generalization. The untouched holdout is the stronger deployment signal.
- The current ordinary path uses one embedding request and at most one structured chat request. The J run completed in about **164 seconds for 20 questions**, so the present issue is quality rather than the earlier experimental latency.

## Recommended next step

Repair the two generic J error classes while protecting the current safety behavior: use semantic/evidence-based acceptance for normal paraphrases, reserve hard rejection for high-risk constraints, and strengthen relation-to-question pruning for generic neighboring claims. Then replay the official/H/F/G/J suites, run all automated tests, freeze a completely new untouched holdout, and require that set to pass before the Docker/Hugging Face smoke test and deployment.

**Meeting takeaway:** the system is a strong, traceable prototype with reliable retrieval, citations, and safety boundaries. Its remaining deployment blocker is the recall-versus-scope trade-off in answer validation, now demonstrated by a genuinely untouched test rather than the required demo questions.
