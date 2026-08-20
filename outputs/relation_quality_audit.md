# Relation quality audit

Requirements source: `Document_Intelligence_Project_Description.docx`, Step 7 and the Entity and relation extraction rubric category.

**Gate result:** PASS

This is a project self-audit, not an independent conservation-domain review. PASS means the stored evidence directly contains the related entities and expresses the named semantic relation, or directly contains the entity for a `document_mentions_*` relation.

## Before and after

| Measure | Before Gate 2 | After Gate 2 |
|---|---:|---:|
| Entity mentions | 6,982 | 6,795 |
| All relation mentions | 1,389 | 987 |
| Semantic relation mentions | 54 | 7 |
| Document-mention relations | 1,335 | 980 |
| Required relation types represented | 5/5 | 5/5 |

The reduction is intentional. The old semantic extractor linked every compatible entity pair in the same OCR sentence when any broad trigger appeared. Long PDF tables and front matter therefore produced unsupported pairs. The repaired extractor requires bounded active, passive, possessive, or explicit habitat-list grammar. It also rejects reference/table-of-contents chunks, matches short acronyms case-sensitively, excludes locations embedded in agency or longer location names, and centers evidence on the matched alias.

## Automated integrity audit

Every one of the 987 stored relation rows was checked against the rebuilt SQLite corpus.

- Valid required relation type: **987/987 PASS**
- Relation document ID matches its source chunk: **987/987 PASS**
- Source chunk is not classified as bibliography/table-of-contents noise: **987/987 PASS**
- Evidence contains the required object alias for document mentions and both aliases for semantic relations: **987/987 PASS**
- Integrity failures: **0**

## Semantic relation review

All seven semantic relation mentions were manually reviewed.

| Relation | Evidence location | Confidence | Result | Finding |
|---|---|---:|---|---|
| U.S. Geological Survey → `agency_manages_program` → Nonindigenous Aquatic Species Database | DOC011, pp. 1-2 | 0.90 | **PASS** | The title identifies the database possessively as the U.S. Geological Survey's database. |
| U.S. Geological Survey → `agency_manages_program` → Nonindigenous Aquatic Species Database | DOC011, pp. 2-3 | 0.90 | **PASS** | The relational-design caption again identifies it as the U.S. Geological Survey's database. |
| U.S. Geological Survey → `agency_manages_program` → Nonindigenous Aquatic Species Database | DOC011, pp. 4-6 | 0.90 | **PASS** | The occurrence-record caption again identifies it as the U.S. Geological Survey's database. |
| Mallard → `species_uses_habitat` → Wetland | DOC001, pp. 149-153 | 0.90 | **PASS** | Wetland systems are stated to provide habitat to a list that explicitly includes mallards. |
| Mallard → `species_uses_habitat` → Wetland | DOC014, pp. 18-20 | 0.90 | **PASS** | Wetlands are stated to support species explicitly including Mallard. |
| American black duck → `species_uses_habitat` → Marsh | DOC014, pp. 34-36 | 0.93 | **PASS** | American black duck is directly stated to occur in saltwater marshes. |
| Climate change → `threat_affects_species` → Invasive carp | DOC012, pp. 13-14 | 0.94 | **PASS** | The source directly states that climate change may affect where invasive carp can invade. |

Duplicate subject/relation/object pairs are retained only when they point to distinct evidence chunks; consumers deduplicate canonical pairs when appropriate.

## Document-mention sample

A deterministic SHA-256 ordering selected 15 `document_mentions_species` and 15 `document_mentions_location` rows. Manual review found the named species/location alias in every evidence snippet.

- Species mentions: **15/15 PASS**
- Location mentions: **15/15 PASS**
- Combined mention sample: **30/30 PASS**

## Overall sampled precision

- Semantic relations: **7/7 PASS**
- Document mentions: **30/30 PASS**
- Combined reviewed sample: **37/37 PASS (100%)**

## Remaining limitations

- The extractor deliberately favors precision over recall; only seven semantic relation mentions survive in this corpus.
- The lexicon is finite and rule-based, so unlisted species, programs, and paraphrased predicates can be missed.
- Possessive agency/program wording establishes operational ownership conservatively but is less explicit than a “manages” verb, reflected by its lower confidence.
- No conservation-domain expert has independently scored the relations.
