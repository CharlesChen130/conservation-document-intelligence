# Full official demo correctness audit

Audited artifact: `outputs/demo_answers.md`

Artifact SHA-256:
`6d5b93eafbec629dad0c3094998f2836115ccfaec56c43e93fa14ccd15c6d54e`

Scoring rule: **PASS** = relevant and supported with usable presentation;
**PARTIAL** = the core content is supported but a material quality defect
remains; **FAIL** = a material claim is not established by its cited evidence.

## Result

| Question | Result | Findings |
|---:|---|---|
| 1. Aquatic-invasive-species documents | **PASS** | Three matching public documents with exact titles; every description directly discusses aquatic invasive species and has an application-owned citation. |
| 2. Most frequent agencies | **PASS** | Deterministic corpus-wide entity counts, ranked by document coverage then mention count. |
| 3. Main conservation threats | **PASS** | Deterministic aggregation reports eight threat entities with corpus-wide document and mention counts. |
| 4. Wetland documents | **PASS** | Four directly relevant sources cover restoration, wetland action, wetland damage/management, and inventory mapping/monitoring. |
| 5. Waterfowl-conservation documents | **PASS** | Deterministic same-chunk scan lists documents containing both required terms and cites each result. |
| 6. Invasive carp and habitat management | **PASS** | Cited evidence directly covers invasive-carp removal and selective control research in aquatic habitats. |
| 7. Missouri conservation-planning documents | **PASS** | Three relevant Missouri planning/management sources describe statewide actions, goals, and Conservation Opportunity Areas. |
| 8. Wetland-conservation summary | **PASS** | Deterministic brief; claims cover condition assessment, wise use, research/monitoring, and restoration planning with citations. |
| 9. Generated wiki inventory | **PASS** | Deterministic inventory matches the canonical wiki categories and cites a source for each page. |
| 10. Unanswered corpus questions | **PASS** | Six statements are explicit source uncertainties or information needs; the system does not infer gaps from missing retrieval results. |

**Total: 10 PASS, 0 PARTIAL, 0 FAIL.**

## Additional engineering controls

- Cross-location comparison covers both Missouri and Chesapeake Bay threats.
- Cross-agency corroboration uses one exact relation independently supported by
  Environment and Climate Change Canada and the Missouri Department of
  Conservation.
- Missing-page citations are reported deterministically.
- The private-personnel request abstains.
- Amazon deforestation evidence is returned as an exact cited corpus span.

All 15 report entries avoid failed and safety-abstention statuses. The one
intended privacy abstention is a sufficiency abstention. No raw internal source
label appears in answer text.

Automated checks verify citation syntax, authorization, retrieval membership,
formatting, and abstention behavior. The PASS judgments additionally reflect
manual semantic review and remain a project self-audit rather than independent
conservation-domain validation.
