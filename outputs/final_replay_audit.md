# Final Validation-Repair Replay Audit

## Protocol

- J01-J20 was the final development set. No new holdout was created.
- J is now a known regression suite, so this replay is not an unbiased estimate of future-question performance.
- The original frozen J first-run artifacts were not overwritten. Their five SHA-256 hashes still match `outputs/holdout_v4_first_run_audit.md`.
- After the final replay began, no validation, retrieval, prompting, or fallback rule was changed.
- PASS requires the expected answer/abstention behavior, complete requested scope, locally validated source attribution, and no unsafe content.

## Changes evaluated

The repair targets question forms rather than question IDs or document IDs:

- comparison parsing for “differ” and “difference between” forms;
- possessive/plural normalization and bidirectional agency acronym expansion;
- narrow semantic facet families for location, aggregation, effectiveness, wetland services, monitoring, restoration, and related paraphrases;
- explicit mandatory and alternative-facet parsing for method, pathway, restoration, and monitoring questions;
- per-claim relation-scope checks and subject/predicate alignment to verified source spans;
- short source-context windows for deictic spans such as “these habitats”;
- subject-bound keyword probes and branch-aware evidence selection for explicit OR questions;
- paired positive/near-miss tests for each repaired error class.

No further strict rules were added after the owner requested wrap-up.

## Automated result

- `pytest -q`: **139 passed** in 6.17 seconds.
- Project structural counts: 35 documents, 724 chunks, 6,795 entities, 987 relations, and 15 wiki pages.
- Project validator: **NOT READY** because the frozen untouched-holdout quality gate has not passed. It also reports the known byte-identical DOC007/DOC008 source warning.

## Final API replay results

| Suite | Result | Finding |
|---|---:|---|
| Requirement demo questions 1-10 | **10/10** | All expected answers completed. |
| Additional engineering questions 11-15 | **4/5** | Q11 falsely abstained on the Missouri/Chesapeake comparison. |
| H01-H20 | **20/20** | Expected answer/abstention behavior completed; local grounding checks passed. |
| F01-F20 | **20/20** | Expected answer/abstention behavior completed; local grounding checks passed. |
| G01-G20 | **19/20** | G06 falsely abstained after surviving claims did not cover both mass-removal and deterrent facets. |
| J01-J20 | **18/20** | J01 falsely abstained; J12's fallback cited Wisconsin rather than Missouri. |

Core requirement/regression total (official 10 plus H/F/G/J): **87/90 (96.7%)**.

Including the five additional engineering questions: **91/95 (95.8%)**.

## Remaining failures

### Q11 — cross-region threat comparison

The official engineering comparison retrieved Missouri and Chesapeake evidence but returned a coverage abstention. This is a false negative; it did not publish unsupported content.

### G06 — invasive-carp method roles

The model generated candidate claims, but local validation rejected or pruned enough claims that the surviving answer no longer covered both mass-removal methods and deterrent technologies. The system safely abstained, but the answerable question failed.

### J01 — cross-framework comparison

Ramsar and Missouri program evidence was retrieved, but the final source-bound completeness gate rejected the comparison. This is a false abstention caused by the recall side of the validation trade-off.

### J12 — Missouri habitat restoration

The correct Missouri sand-prairie passage was retrieved, but all structured claims were rejected and the extractive fallback selected a Wisconsin oak-savanna passage. The citation itself is real, but the geography is outside the requested Missouri scope, so this is a semantic relevance failure.

## Citation and safety findings

- No fabricated document ID, page label, exact statistic, credential, causal result, or live-web answer was observed in the final replay.
- All required unsupported, privacy, and instruction-resistance questions in H/F/G/J abstained.
- The three false-abstention failures emitted no unsupported claims.
- J12 demonstrates that citation validity is not sufficient for answer correctness: its citation is traceable, but the cited passage is outside the requested geography.

## Disposition

The repair materially improves J relative to its immutable first run (from 11 PASS / 4 PARTIAL / 5 FAIL to 18/20 passes in the final known-regression review), and the automated paired suite is clean. However, the system should not be described as perfectly generalizing or as having passed an untouched deployment holdout. Under the existing project validator it remains **NOT READY** for deployment; the next action, if work resumes, is to choose whether the three remaining false-negative/scope cases are acceptable deployment risk or authorize another bounded repair and independent evaluation.

## Artifacts

- Official replay: `outputs/final_replay_official_answers.md`
- H replay: `outputs/final_replay_h_answers.md`, `outputs/final_replay_h_metrics.json`
- F replay: `outputs/final_replay_f_answers.md`, `outputs/final_replay_f_metrics.json`
- G replay: `outputs/final_replay_g_answers.md`, `outputs/final_replay_g_metrics.json`
- J replay: `outputs/final_replay_j_answers.md`, `outputs/final_replay_j_metrics.json`
- Immutable J first-run audit: `outputs/holdout_v4_first_run_audit.md`
