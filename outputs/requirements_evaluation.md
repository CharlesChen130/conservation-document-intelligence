# Document-defined requirements evaluation

Requirements source: `Document_Intelligence_Project_Description.docx`

## Outcome

Provisional implementation self-score: **95/100**. This exceeds the internal
90/100 deployment threshold. It is not an independent or
conservation-domain-expert score.

| Document rubric category | Weight | Score | Evidence and deductions |
|---|---:|---:|---|
| Corpus and metadata | 20% | **20/20** | 35/35 public sources; organized metadata; original/resolved URLs and checksums retained; every source has a raw artifact and database record. |
| Search/retrieval | 20% | **19/20** | SQLite FTS5 plus a current 724-vector FAISS index returns relevant, traceable chunks. Facet-balanced retrieval, comparison-side probes, bibliography filtering, and explicit gap handling are implemented. Deduction: long-chunk previews can begin before the exact supporting sentence. |
| Entity/relation extraction | 20% | **18/20** | All five required relation types remain represented. All 987 rows pass provenance/alias/noisy-source integrity checks; all 7 semantic relations and a deterministic 30-row mention sample pass manual review. Exact cross-agency corroboration can be queried. Deduction: the finite rule-based lexicon favors precision over recall and lacks independent domain review. |
| LLM Wiki | 20% | **18/20** | 15 category-balanced pages consolidate 44 citation-backed facts; 44/44 facts trace to exact stored evidence and 84/84 internal links resolve. Deduction: four pages retain only one publishable fact, generation is deterministic/extractive, and no domain expert has independently reviewed it. |
| Chatbot and demo | 20% | **20/20** | Final official evaluation: 10 PASS / 0 PARTIAL / 0 FAIL. H, F, and G regression sets each have 16/16 supported answers and 4/4 intended abstentions. Claim-level citations, exact support spans, logical-facet coverage, policy abstention, and local safety pruning remain enforced without a model retry loop. |
| **Total** | **100%** | **95/100** | Provisional self-evaluation; the document-defined implementation threshold is met. |

## Required question report

Questions 1-10 in `outputs/demo_answers.md` reproduce the document-defined
evaluation questions exactly. Questions 11-15 are additional engineering
checks and do not replace the required set.

- Official questions with substantive answers: **10/10**
- Full correctness review: **10 PASS / 0 PARTIAL / 0 FAIL**
- Evaluation failures: **0**
- Safety-abstention failures: **0**
- Raw internal source labels exposed: **0**
- Additional engineering controls: **5/5 expected behavior**
- Full official-answer audit: `outputs/full_demo_correctness_audit.md`

## Additional engineering evidence

- Automated suite: **139 passed**
- Known H regression replay: **20/20 expected behavior**
- Known F regression replay: **20/20 expected behavior**
- Known G regression replay: **20/20 expected behavior**
- Fresh untouched J holdout: **11 PASS / 4 PARTIAL / 5 FAIL**; **13/20
  half-credit score (65%)**; all 16 answerable questions retrieved usable expected
  evidence, but five were rejected by post-generation coverage validation
- Corpus: **35 documents / 724 chunks**
- Knowledge layer: **6,795 entity mentions / 987 high-precision relations**
- Relation quality: **987/987 integrity checks, 37/37 manually reviewed rows PASS** (`outputs/relation_quality_audit.md`)
- Wiki: **15 canonical pages / 44 traceable facts / 84 valid internal links** (`outputs/wiki_quality_audit.md`)
- Semantic index: **current for the corpus, 724 vectors, 1,536 dimensions**
- Ordinary supported query: **one embedding call plus at most one structured chat call**

The original frozen first-run reports remain immutable and continue to record
the defects that motivated the repairs. Post-repair H/F/G results are regression
evidence because those questions informed development; they are not represented
as a new blind estimate.

## Remaining external gates

- Run the app locally and in Streamlit Community Cloud, then complete the browser
  acceptance checklist.
- Configure `OPENAI_API_KEY` as a root-level Streamlit Community Cloud secret,
  never in a committed file.
- Optionally configure `FEEDBACK_FORM_URL`.
- Obtain independent rubric scoring and conservation-domain review before
  treating the prototype as authoritative decision support.
- The final J01-J20 result remains disclosed as a failed internal generalization
  gate; publication is for research demonstration rather than production use.

The project owner selected Streamlit Community Cloud instead of the deployment
guide's Hugging Face target because Docker Spaces require paid hosting. This
changes the hosting adapter, not the documented system capabilities. The final
J holdout remains disclosed as a failed internal generalization gate; publication
is therefore for research demonstration rather than production readiness. The
remaining external gates are the Streamlit cloud smoke test and owner-authenticated
deployment from the private GitHub repository.
