# Fresh Holdout Manual Audit

This audit reviews the first execution of the newly frozen F01-F20 holdout.
The specification was frozen after the H01-H20 repairs and before any F01-F20
question was executed. No retrieval, prompting, routing, or validation change
was made against this set before or during the run.

## Execution

- Frozen specification SHA-256: `d06b90992b820c24031dd60ec0e7bb849ebd2534dafd3b2cdf288ba43006b278`
- Model path: one query-embedding request and at most one structured chat request per ordinary question
- Cumulative elapsed time: 115.992 seconds
- Embedding input tokens: 304
- Chat input tokens: 96,567
- Chat output tokens: 7,798
- Local automated suite before execution: 104 passed

## Manual result

| Measure | Result |
|---|---:|
| Questions | 20 |
| PASS | 15 |
| PARTIAL | 4 |
| FAIL | 1 |
| Strict pass rate | 75% |
| PASS-or-PARTIAL rate | 95% |
| Half-credit engineering score | 17/20 (85%) |
| Expected supported answers actually answered | 15/16 (93.75%) |
| False abstentions on answerable questions | 1/16 (6.25%) |
| Expected abstentions correctly handled | 4/4 (100%) |
| Model-handled supported questions | 9 PASS / 4 PARTIAL / 1 FAIL |
| Deterministic wiki questions | 2/2 PASS |

PASS means the response satisfies the frozen expected behavior with directly
supported citations. PARTIAL means the core response is supported but a
material completeness, relevance, or presentation defect remains. An
abstention on a question marked `supported_answer` is a FAIL. The half-credit
engineering score assigns 1 point to PASS, 0.5 to PARTIAL, and 0 to FAIL; it is
not the official project rubric.

## Question-level review

| ID | Result | Review finding |
|---|---|---|
| F01 | **PASS** | Identifies boater-focused Clean Drain Dry/Stop Aquatic Hitchhikers outreach and concrete inspection, cleaning, and decontamination infrastructure. |
| F02 | **PARTIAL** | Gives two directly supported Missouri prescribed-fire habitat practices, but does not answer the separately requested landowner-support facet. |
| F03 | **PASS** | Directly connects the Missouri Stream Connectivity Partnership and barrier removal to aquatic-organism passage and stream restoration. |
| F04 | **PASS** | Identifies the MDC annual review and directly reports its bat habitat plan, acreage, roost/foraging habitat, and cave actions. |
| F05 | **PASS** | Explains Missouri wetland easement terms, scale, agency monitoring, and sensitive-habitat protection with source-specific citations. |
| F06 | **FAIL** | False coverage abstention. Retrieved corpus evidence can answer the roles of citizen observations/open data in early detection and rapid response. |
| F07 | **PASS** | Correctly distinguishes eDNA early detection/surveillance from acoustic telemetry used to locate fish, track movement, and identify aggregations. |
| F08 | **PASS** | Directly connects waterfowl/wetland programs to water quality, flood reduction, and carbon storage. |
| F09 | **PARTIAL** | The source excerpts support federal/state/tribal coordination and governmental/nongovernmental partner definition, but the answer never explicitly covers private partners and includes a third excerpt that does not explain coordination. |
| F10 | **PARTIAL** | DOC006 directly answers harmful-algal-bloom detection and management research, but the extra DOC009 bullet discusses AIS/eDNA rather than harmful algal blooms. |
| F11 | **PASS** | Covers public access and decision support through maps, downloadable/queryable data, integrated context, and Status and Trends reports. |
| F12 | **PARTIAL** | Directly identifies live-organism pathways and recommends outreach to pet/aquaculture sectors, but adds an unrelated invasive-carp harvest action and does not give a more concrete release/trade prevention measure. |
| F13 | **PASS** | Gives Missouri cave/karst practices including opening protection, well capping, buffers, livestock systems, watershed protection, and pesticide practices. |
| F14 | **PASS** | Explains the documented prioritization and partner-focus role of Missouri Conservation Opportunity Areas. |
| F15 | **PASS** | Lists every generated habitat wiki page with one source-backed fact and citation. |
| F16 | **PASS** | Lists every generated threat wiki page with one source-backed statement and citation. |
| F17 | **PASS** | Correctly abstains from inventing an exact 2026 statewide Missouri monarch count. |
| F18 | **PASS** | Correctly abstains from inventing causal dollar savings for Missouri wetland restoration. |
| F19 | **PASS** | Refuses the credential and highly sensitive personal-data request without retrieval or generation. |
| F20 | **PASS** | Preserves the corpus-only contract and abstains from supplying a current vaquita estimate from memory. |

## Error classes exposed by the untouched set

1. **Unrecognized compound facet phrasing.** F02's “habitat management and
   landowner support” construction is not fully enforced by the mandatory-facet
   parser.
2. **Over-strict coverage on coordinated concepts.** F06 retrieves answerable
   evidence but rejects the surviving claims because citizen reporting,
   open-access data, early detection, and rapid response are treated as an
   all-or-nothing lexical bundle.
3. **Weak negative relevance filtering.** F10 retains a source-specific but
   off-topic AIS/eDNA claim because a generic “research” term passes the subject
   binding check.
4. **Alternative-pathway drift.** F12 covers a valid live-trade branch but also
   retains an unrelated invasive-carp harvest claim.
5. **Raw extractive fallback quality.** F09 preserves grounding but produces
   noisy OCR excerpts and does not explicitly cover every named partner sector.

This clean result is the current generalization evidence. The F01-F20 answers
must now remain immutable. If these error types are repaired, F01-F20 becomes a
known regression set and another newly frozen holdout is required before
claiming a new unbiased score.
