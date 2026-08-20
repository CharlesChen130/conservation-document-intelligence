# Balanced Scope Repair Regression Audit

## Outcome

The generalized scope, comparison, pathway-relation, exact-span, and guarded-
fallback repairs pass the document-defined demo and all three known 20-question
regression sets. These sets now informed development, so their post-repair
scores are breadth/regression evidence rather than an unbiased generalization
estimate.

## Automated verification

- Local automated suite: **131 passed**
- Paired positive/near-miss tests cover comparison subjects, live-trade versus
  pet-food context, single-facet fallback scope, title binding, OCR-split words,
  invalid ellipses, and internal source-label cleanup.
- Ordinary supported-question path: one embedding request and at most one
  structured chat request; no model verifier or retry loop.
- Structured output cap: 1,000 tokens.
- Immutable first-run holdout specifications and reports retain their recorded
  SHA-256 hashes.

## Known-set regression results

| Set | Current manual result | Supported questions answered | Required abstentions |
|---|---:|---:|---:|
| H01-H20 | **20 PASS** | 16/16 | 4/4 correct |
| F01-F20 | **20 PASS** | 16/16 | 4/4 correct |
| G01-G20 | **20 PASS** | 16/16 | 4/4 correct |

Final full-replay artifacts:

- H: `outputs/holdout_regression_balanced_final_answers.md`
- F: `outputs/holdout_v2_regression_balanced_final_3_answers.md`
- G: `outputs/holdout_v3_regression_final_answers.md`

The final F replay used 304 embedding input tokens, 96,834 chat input tokens,
7,243 chat output tokens, and 141.141 cumulative seconds. The final H and G
replays also completed with the intended 16 answers and four abstentions.

## Repairs and trade-off checks

- Explicit comparison sides remain subject-binding even when a technique, such
  as eDNA, is also an action alias.
- `How do A compare with B?` now retrieves and requires evidence for both sides.
- Bare `What actions ... through A, B, or C?` questions treat alternatives as OR
  branches and require a genuine prevention/control/outreach/planning action.
- `pet food` no longer satisfies the `aquarium pets` introduction pathway.
- Exact cross-agency corroboration is answered deterministically from a
  relation repeated in documents from distinct source agencies.
- Single-facet extractive fallback must cover the distinctive question scope;
  deictic words such as “this” cannot admit an unrelated result.
- Invalid compound quotes are narrowed only to exact source fragments; dangling
  OCR page cutoffs and internal `Source S1` prose are not published.

The breadth replay caught H15, F07, F12, Q11, Q12, and Q15 regressions during
the loop. They were repaired as question-type mechanisms, then protected by
paired tests and replayed on unrelated cases. This is the primary evidence that
the final rules did not merely hard-code the failing IDs.

## Document-defined evaluation

The final saved report contains substantive, cited answers for all 10 official
questions. Manual review scored **10 PASS / 0 PARTIAL / 0 FAIL**. The five
additional engineering controls also behave as intended: four supported
answers and one privacy abstention, with no failed or safety-abstention status
and no raw internal source labels.

Artifact: `outputs/demo_answers.md`

## Integrity

The immutable first-run artifacts remain unchanged:

- `data/holdout_spec.yaml`: `89d64cd7fa0b14f16cf14590f2afa7f6aa0c214c6dd68aeff75249a3ddc31fa7`
- `outputs/holdout_answers.md`: `145ced36884507f115cec6c5b5b87cc04076540a3869f95bc39ebaf7a42a0a92`
- `data/holdout_v2_spec.yaml`: `d06b90992b820c24031dd60ec0e7bb849ebd2534dafd3b2cdf288ba43006b278`
- `outputs/holdout_v2_answers.md`: `368f5cf639944679e0511bbd269ac58d2609e8704db2955820ccbded8794b5cf`
- `data/holdout_v3_spec.yaml`: `e02672aa02315ed3bce74d9cae24186c2a03d7695dc11618b61e199305870400`
- `outputs/holdout_v3_answers.md`: `7af001f8e2a426d9cf6803d997e3c9330897a241165e1eace52ccb59a85038b0`
- `outputs/holdout_v3_metrics.json`: `bb393e67ccb820476816f8b98587d701174cd021d2d77eaee05a90aa2a99345e`

## Conclusion

The implementation now meets the document-defined functional evaluation and
the known-set breadth checks. Before publication, freeze and run a new
untouched holdout and complete the Docker/Hugging Face Space smoke test.
Independent conservation-domain review remains recommended;
post-repair regression scores alone are not independent validation.
