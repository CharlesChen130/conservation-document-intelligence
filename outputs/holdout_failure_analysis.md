# Frozen holdout failure analysis

This analysis uses the immutable first-run answers in `outputs/holdout_answers.md`, the exact stored chunks in `db/conservation.db`, and a retrieval-only replay with answer generation disabled. No retrieval, routing, prompting, generation, or validation behavior was tuned during this analysis.

## Executive finding

The low score was caused primarily by **false abstention after successful retrieval**, not by an inability to retrieve any evidence and not primarily by the OpenAI answer model.

- The system returned an abstention for 12 of 16 answerable questions.
- All 12 false abstentions stopped at the deterministic scope gate before the answer model was called.
- For 9 of those 12, the top-six evidence already contained a direct expected supporting citation.
- H01 retrieved relevant source families but missed the strongest method-specific chunks.
- H17 and H18 missed the required wiki-inventory route and did not retrieve the complete expected wiki evidence.
- Of the four answers that reached generation, three pass after exact chunk review and one is partial.

Corrected semantic result: **7 PASS / 1 PARTIAL / 12 FAIL**.

## Error taxonomy

### E1 — Literal scope-gate false abstention

Affected: **H01, H03, H05, H06, H07, H09, H11, H12, H13, H15**

The scope gate calculates all non-generic query terms and requires every term to occur as an exact substring somewhere in the retrieved evidence. One absent surface form rejects the whole answer. It does not stem words, normalize hyphens, understand synonyms, or reliably distinguish topical terms from question phrasing.

| Question | Literal term(s) that rejected the evidence | Why that is invalid |
|---|---|---|
| H01 | `methods` | Evidence can describe methods without using the word “methods.” |
| H03 | `missouri-focused` | The evidence says “Missouri” but not the user’s compound adjective. |
| H05 | `inventories` | The evidence uses singular `inventory`. |
| H06 | `roles` | The sources describe what partnerships do without using the word `roles`. |
| H07 | `concerns`, `describe` | The evidence says mussel numbers diminished and populations are threatened; `describe` is question syntax. |
| H09 | `say` | `say` is question syntax, not required subject matter. |
| H11 | `connects` | The evidence directly lists benefits without the verb `connects`. |
| H12 | `early-detection` | The source uses `Early Detection` with a space rather than a hyphen. |
| H13 | `public-private` | The source uses `public and private` and `private landowners`. |
| H15 | `explains` | `explains` is question syntax, not required subject matter. |

This error class accounts for 10 questions. Nine already had direct answer-supporting evidence; H01 also had a retrieval-ranking problem.

### E2 — Wiki intent-routing failure

Affected: **H17, H18**

The deterministic wiki-inventory route only activates when the exact phrase `wiki pages` is combined with `generated` or `created`. H17 says `each generated agency wiki page` (singular), and H18 says `location wiki pages exist` without `generated` or `created`. Both therefore fell into ordinary semantic document retrieval.

The ordinary wiki search is limited and relevance-ranked, so it cannot guarantee a complete category inventory. H17 selected only two of the three agency pages in wiki context and H18 selected only one of the three location pages. Both then failed the same literal scope gate.

### E3 — Retrieval ranking/chunk-boundary miss

Affected: **H01**

H01 retrieved the correct source families—DOC006, DOC007/DOC008, DOC009, and DOC005—but not their strongest zebra-mussel method chunks. For example, direct method evidence exists in:

- DOC006, pp. 6–7: zebra-mussel antifouling research;
- DOC007/DOC008, pp. 16–22: watercraft inspection, decontamination, monitoring, containment, control, research, and education;
- DOC009, pp. 7–8: genetic sterilization and eDNA detection work;
- DOC013, pp. 19–20: monitoring and inspection systems plus coordinated containment.

The selected DOC007/DOC008 pp. 13–17 chunks end immediately after the `ZEBRA/QUAGGA MUSSELS` heading, before the associated solution text in the overlapping next chunk. Document diversification and the six-chunk limit then kept the stronger chunks out of the final evidence set.

### E4 — Claim-to-citation entailment failure

Affected: **H10**

H10 retrieved the correct citations for watercraft inspection/decontamination and ballast-water regulation. Most of the answer is supported, but it says customs-inspector biosecurity training “would presumably include ballast water and boating.” The cited customs chunks do not establish that connection. A separate retrieved DOC009 chunk supports Coast Guard enforcement of ballast-water regulations, so the model had adequate evidence but combined it incorrectly.

The current validator verifies citation syntax, allowed document IDs, citation placement, and some unsupported tails. It does not perform full semantic entailment between every claim and its attached chunk, so the unsupported inference survived.

### E5 — Manual audit normalization error, now corrected

Affected: **H08**, which is now **PASS**

The initial manual audit incorrectly marked H08 as unsupported because exact string searches did not account for PDF line-break hyphenation and the audit checked the wrong adjacent chunk for some phrases. Exact stored-chunk review confirms:

- DOC001, pp. 61–63 supports prescribed burning, mechanical tree and brush removal, mowing, haying, herbicide treatment, grazing, the named grassland geographies, landowner cooperation, and monitoring.
- DOC015, pp. 5–6 supports Missouri Prairie Foundation prairie purchases and MDC grassland acquisition/management.
- DOC016 supports the community health index, landscape health index, Golden Grasslands, priority geographies, partners, and private landowners.

This was an evaluation-process error rather than an application error.

## Expected-citation matrix for non-passing questions

`Yes` means at least one exact top-six retrieved chunk directly supported the requested answer. `Partial` means the correct document family was retrieved but the strongest answer-supporting chunk was not. `No` means the required inventory/citation set was not retrieved.

| ID | Result | Expected citation found? | Direct evidence or expected evidence | Primary error |
|---|---|---|---|---|
| H01 | FAIL | **Partial** | Retrieved DOC006/DOC007/DOC008/DOC009 families; stronger method chunks such as DOC006 pp. 6–7 and DOC007/DOC008 pp. 16–22 were outside the selected set. | E1 + E3 |
| H03 | FAIL | **Yes** | DOC018 directly describes Missouri’s climate adaptation/resilience plan and climate-smart planning. | E1 |
| H05 | FAIL | **Yes** | DOC027 pp. 49–52 directly connects wetland inventory, monitoring, detecting/responding to change, and management planning; DOC002 adds Missouri inventory data. | E1 |
| H06 | FAIL | **Yes** | DOC003 pp. 40–42 and DOC004 pp. 1–4 directly describe joint ventures and coordinated partnership functions. | E1 |
| H07 | FAIL | **Yes** | DOC001 pp. 176–180 says freshwater mussel numbers diminished greatly and identifies habitat loss, sedimentation, and invasive-species threats. | E1 |
| H09 | FAIL | **Yes** | DOC017, DOC018, and DOC016 directly report Missouri feral-hog removals, acreage, aerial operations, baiting/scouting, landowner assistance, and partnership structure. | E1 |
| H10 | PARTIAL | **Yes** | DOC009 pp. 1–3 and 9–11 plus DOC006/DOC007/DOC008 directly support ballast regulation, watercraft inspection, decontamination, and pathway controls. | E4 |
| H11 | FAIL | **Yes** | DOC014 pp. 4–7 directly says wetlands help clean/maintain water supplies, reduce flood risk, and provide habitat carrying capacity for waterfowl and other wildlife. | E1 |
| H12 | FAIL | **Yes** | DOC012 pp. 17–20 directly covers early detection, surveillance, removal, herding, and barriers; DOC006 pp. 6–7 covers electric barriers. | E1 |
| H13 | FAIL | **Yes** | DOC001 pp. 36–37 directly describes cost sharing, private-landowner partnerships, Farm Bill programs, restoration, invasive control, outreach, and monitoring. | E1 |
| H15 | FAIL | **Yes** | DOC022 directly states the National Wetlands Inventory mission and lists maps, geospatial data, monitoring, datasets, status/trends reports, and decision support. | E1 |
| H17 | FAIL | **No** | Expected complete agency-page facts include citations from the USFWS, USGS, and MDC wiki pages; the generic route did not load the complete agency inventory. | E2 |
| H18 | FAIL | **No** | Expected location pages are Canada, United States, and North America with their page citations; the generic route selected only one location page. | E2 |

Among the 12 failed answerable questions, the expected direct citation was found for **9**, partially found for **1**, and missed for **2**. Including the partial H10 answer, **10 of the 13 non-passing cases had direct expected evidence available to the answer pipeline**.

## Why the numerical result became so low

Each incorrect abstention is a full failed answer even when retrieval was good. The all-terms scope gate allowed only 4 of 16 answerable questions to reach generation. After corrected semantic review, those four produced three supported answers and one partial answer. Thus the headline score mostly measures an over-conservative deterministic gate, while H10 demonstrates a separate overclaim problem that still requires repair.

The four intended abstentions all pass. This means the system currently has high refusal behavior but poor recall: it is safe in unsupported scenarios, yet rejects too many supported questions.
