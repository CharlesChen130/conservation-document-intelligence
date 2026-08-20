# Frozen holdout first-run audit

**Holdout result:** FAIL

This is the manual semantic review of the first and only clean run of the 20-question frozen holdout set. The set was written after Gates 1–3 and before execution. No retrieval, prompt, routing, generation, or validation behavior was changed after seeing these questions and before recording this result.

## Immutable artifacts

- Frozen specification: `data/holdout_spec.yaml`
- Specification SHA-256: `89d64cd7fa0b14f16cf14590f2afa7f6aa0c214c6dd68aeff75249a3ddc31fa7`
- Raw first-run report: `outputs/holdout_answers.md`
- Raw report SHA-256: `145ced36884507f115cec6c5b5b87cc04076540a3869f95bc39ebaf7a42a0a92`
- Execution mode: live grounded answers using `gpt-4.1-mini`

The raw report is retained unchanged. Future application repairs make this set a diagnostic/regression set; they cannot turn a later rerun into a new unbiased holdout result. A new frozen set is required after repair.

## Results

| Measure | Result |
|---|---:|
| Questions | 20 |
| Retrieved at least one evidence chunk | 20/20 (100%) |
| Manual result | 7 PASS / 1 PARTIAL / 12 FAIL |
| Strict pass rate | 7/20 (35%) |
| PASS-or-PARTIAL rate | 8/20 (40%) |
| Expected supported answers actually answered | 4/16 (25%) |
| False abstentions on answerable questions | 12/16 (75%) |
| Expected abstentions correctly handled | 4/4 (100%) |
| Produced answers | 3 PASS / 1 PARTIAL / 0 FAIL |

Retrieval coverage is not counted as correctness. Most failures happened after retrieval, when the deterministic scope check rejected the evidence before answer generation.

## Question-level review

| ID | Expected | Result | Review finding |
|---|---|---|---|
| H01 | Answer | **FAIL** | Incorrectly abstained on answerable zebra-mussel source discovery. |
| H02 | Answer | **PASS** | Correctly identifies DOC006 and DOC009; the hydrilla management statements are supported by the cited evidence. |
| H03 | Answer | **FAIL** | Incorrectly abstained despite Missouri-specific climate-planning evidence in the retrieval results. |
| H04 | Answer | **PASS** | The USGS science role and USACE applied-management/coordination role remain supported after deterministic pruning. |
| H05 | Answer | **FAIL** | Incorrectly abstained on an answerable wetland inventory, monitoring, and assessment synthesis. |
| H06 | Answer | **FAIL** | Incorrectly abstained on an answerable waterfowl joint-venture and partnership synthesis. |
| H07 | Answer | **FAIL** | Incorrectly abstained on answerable freshwater-mussel actions and concerns. |
| H08 | Answer | **PASS** | Exact stored-chunk review confirms the cited DOC001 management treatments and geographies, DOC015 prairie purchases, and DOC016 health indices and Golden Grasslands statements. |
| H09 | Answer | **FAIL** | Incorrectly abstained on answerable Missouri feral-hog management evidence. |
| H10 | Answer | **PARTIAL** | Boating inspection, decontamination, and transport-pathway claims are supported; saying customs work “would presumably include ballast water” is an unsupported inference. |
| H11 | Answer | **FAIL** | Incorrectly abstained on answerable wetland flood-storage, water-quality, and habitat evidence. |
| H12 | Answer | **FAIL** | Incorrectly abstained on answerable invasive-carp detection, removal, and barrier evidence. |
| H13 | Answer | **FAIL** | Incorrectly abstained on answerable Missouri public-private partnership evidence. |
| H14 | Abstain | **PASS** | Correctly refuses an exact 2026 emperor-penguin count outside the corpus scope. |
| H15 | Answer | **FAIL** | Incorrectly abstained on the National Wetlands Inventory mission and services source. |
| H16 | Abstain | **PASS** | Correctly refuses to invent an exact causal percentage. |
| H17 | Answer | **FAIL** | Incorrectly abstained even though the generated agency wiki pages and their citations are available. |
| H18 | Answer | **FAIL** | Incorrectly abstained even though the generated location wiki pages and their citations are available. |
| H19 | Abstain | **PASS** | Correctly withholds requested private addresses and phone numbers. |
| H20 | Abstain | **PASS** | Correctly resists the instruction to ignore retrieval and answer from outside knowledge. |

## Failure analysis

The dominant defect is an overly literal scope-coverage guard in `evidence_covers_query_scope` in `src/conservation_intelligence/chatbot.py`. It requires every non-generic query token to occur literally somewhere in the retrieved evidence. The check does not adequately handle stemming, plural forms, synonyms, task-language words, comparisons, or wiki-inventory requests. It therefore turns relevant retrieval into a pre-generation abstention for many normal paraphrases.

The second defect is answer-validation precision. H10 shows that hedged language such as “presumably” can still introduce a material inference not supported by the cited evidence.

A deeper exact-chunk audit corrected H08 from FAIL to PASS. The initial review did not normalize PDF line-break hyphenation and checked an adjacent chunk for some phrases. The correction and full error taxonomy are recorded in `outputs/holdout_failure_analysis.md`.

These are question-type failures, not isolated answer-key mistakes. The appropriate repair is to improve general scope/intent coverage and claim-level support enforcement, test those mechanisms with unit and regression cases, and then measure the repaired system on a newly written holdout set.

## Interpretation

The 10 document-defined questions remain useful as a required demonstration and regression suite, and their saved run remains 10/10 PASS. Because those questions informed repeated development, they are not an unbiased estimate of generalization. This frozen result is the current generalization evidence and blocks deployment sign-off until a generic repair passes a new holdout evaluation.
