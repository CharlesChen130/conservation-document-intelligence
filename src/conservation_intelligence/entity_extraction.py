from __future__ import annotations

import csv
import hashlib
import re
import sqlite3
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import yaml

from .database import connect_database
from .paths import DATABASE_PATH, OUTPUTS_DIR, PROJECT_ROOT
from .repository import evidence_quality_issues


ENTITY_TYPES = {
    "species",
    "habitat",
    "river",
    "wetland",
    "agency",
    "location",
    "threat",
    "program",
    "policy",
    "date",
}
RELATION_TYPES = {
    "species_uses_habitat",
    "threat_affects_species",
    "agency_manages_program",
    "document_mentions_location",
    "document_mentions_species",
}
LEXICON_PATH = PROJECT_ROOT / "data" / "entity_lexicon.yaml"
SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
RIVER_PATTERN = re.compile(r"\b((?:[A-Z][A-Za-z'’-]+\s+){1,3}River)\b")
DATE_PATTERN = re.compile(
    r"\b(?:19|20)\d{2}(?:\s*[-–]\s*(?:(?:19|20)?\d{2}))?\b"
)
RELATION_GAP = r"(?:(?![.!?•])[\s\S]){0,80}?"
HABITAT_TARGET_LINK = (
    r"(?:\s+(?:the|a|an|available|suitable|critical|seasonal|breeding|"
    r"nesting|foraging|nursery|saltwater|brackish|freshwater|riverine|"
    r"estuarine|coastal|shallow))*\s*"
)
SPECIES_TARGET_LINK = (
    r"(?:\s+(?:the|breeding|nesting|foraging|wintering|migrating|"
    r"populations?|individuals|colonies|species|of|such|as))*\s*"
)
THREAT_TARGET_LINK = (
    r"(?:\s+(?:the|where|populations?|distribution|range|survival|"
    r"mortality|abundance|of|for|to|in))*\s*"
)
PROGRAM_TARGET_LINK = r"(?:\s+(?:the|its|a|an))*\s*"
ORGANIZATION_AFTER_LOCATION = re.compile(
    r"^\s+(?:department|agency|bureau|service|survey|army|corps|administration|"
    r"commission|office|secretariat|ministry)\b",
    flags=re.IGNORECASE,
)
SPECIES_HABITAT_ACTIVE = (
    r"\b(?:uses?|utili[sz]es?|inhabits?|occup(?:y|ies)|depends?\s+on|"
    r"(?:is|are|was|were)\s+(?:found|present)\s+in|occurs?\s+in|"
    r"can\s+be\s+found\s+in|"
    r"spawns?\s+in|nests?\s+in|forages?\s+in)\b"
)
SPECIES_HABITAT_REVERSE = (
    r"(?:\b(?:provides?|offers?)\b"
    + RELATION_GAP
    + r"\bhabitats?\s+(?:for|to)\b|"
    r"\b(?:is|are|was|were)\s+used\s+by\b)"
)
THREAT_ACTIVE = r"\b(?:threatens?|affects?|impacts?|harms?|endangers?)\b"
THREAT_PASSIVE = (
    r"\b(?:(?:is|are|was|were)\s+)?"
    r"(?:threatened|affected|impacted|harmed|endangered|at\s+risk)\s+(?:by|from)\b"
)
AGENCY_ACTIVE = (
    r"\b(?:manages?|administers?|leads?|coordinates?|implements?|operates?|"
    r"oversees?|runs?|delivers?)\b"
)
AGENCY_PASSIVE = (
    r"\b(?:is|are|was|were)\s+"
    r"(?:managed|administered|led|coordinated|implemented|operated|overseen|run|delivered)\s+by\b"
)


@dataclass(frozen=True)
class EntityMention:
    entity_id: str
    name: str
    normalized_name: str
    entity_type: str
    doc_id: str
    chunk_id: str
    confidence: float
    evidence: str


@dataclass(frozen=True)
class RelationMention:
    relation_id: str
    subject: str
    relation: str
    object: str
    doc_id: str
    chunk_id: str
    evidence: str
    confidence: float


def _stable_id(prefix: str, *values: str) -> str:
    value = "\0".join(values).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(value).hexdigest()[:20]}"


def load_lexicon(path: Path = LEXICON_PATH) -> dict[str, dict[str, list[str]]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    unexpected = set(data) - ENTITY_TYPES
    if unexpected:
        raise ValueError(f"Unknown entity types in lexicon: {', '.join(sorted(unexpected))}")
    return data


def _sentences(text: str) -> list[str]:
    protected = re.sub(
        r"(?<!w)(?:[A-Z].){2,}",
        lambda match: match.group(0).replace(".", "<PERIOD>"),
        text,
    )
    return [
        sentence.replace("<PERIOD>", ".").strip()
        for sentence in SENTENCE_PATTERN.split(protected)
        if sentence.strip()
    ]


def _case_sensitive_alias(alias: str) -> bool:
    letters = re.sub(r"[^A-Za-z]", "", alias)
    return 1 < len(letters) <= 6 and letters.isupper()


@lru_cache(maxsize=512)
def _alias_expression(aliases: tuple[str, ...]) -> str:
    alternatives: list[str] = []
    for alias in sorted(set(aliases), key=len, reverse=True):
        escaped = re.escape(alias)
        alternatives.append(escaped if _case_sensitive_alias(alias) else f"(?i:{escaped})")
    return rf"(?<!\w)(?:{'|'.join(alternatives)})(?!\w)"


def _contains_alias(sentence: str, alias: str) -> bool:
    return bool(re.search(_alias_expression((alias,)), sentence))


def _first_alias_match(sentence: str, aliases: Iterable[str]) -> re.Match[str] | None:
    matches = _alias_matches(sentence, aliases)
    return matches[0] if matches else None


def _alias_matches(sentence: str, aliases: Iterable[str]) -> list[re.Match[str]]:
    matches = [
        match
        for alias in aliases
        for match in re.finditer(_alias_expression((alias,)), sentence)
    ]
    return sorted(matches, key=lambda item: (item.start(), -len(item.group(0))))


def _location_match_allowed(
    sentence: str,
    match: re.Match[str],
    lexicon: dict[str, dict[str, list[str]]],
) -> bool:
    start, end = match.span()
    for entity_type in ("agency", "location"):
        for aliases in lexicon.get(entity_type, {}).values():
            for outer in _alias_matches(sentence, aliases):
                outer_start, outer_end = outer.span()
                if outer_start <= start and end <= outer_end and (outer_end - outer_start) > (end - start):
                    return False
    return not ORGANIZATION_AFTER_LOCATION.match(sentence[end : end + 80])


def _first_location_match(
    sentence: str,
    aliases: Iterable[str],
    lexicon: dict[str, dict[str, list[str]]],
) -> re.Match[str] | None:
    return next(
        (
            match
            for match in _alias_matches(sentence, aliases)
            if _location_match_allowed(sentence, match, lexicon)
        ),
        None,
    )


def _evidence(sentence: str, limit: int = 500) -> str:
    compact = re.sub(r"\s+", " ", sentence).strip()
    return compact if len(compact) <= limit else compact[: limit - 1].rstrip() + "…"


def _canonical_expression(
    entity_type: str,
    canonical_name: str,
    lexicon: dict[str, dict[str, list[str]]],
) -> str:
    aliases = lexicon.get(entity_type, {}).get(canonical_name, [])
    return _alias_expression(tuple(dict.fromkeys([canonical_name, *aliases])))


def _first_match(text: str, patterns: Iterable[str]) -> re.Match[str] | None:
    matches = [match for pattern in patterns if (match := re.search(pattern, text))]
    return min(matches, key=lambda item: item.start()) if matches else None


def _relation_evidence(text: str, start: int, end: int) -> str:
    window_start = max(0, start - 160)
    prefix = text[window_start:start]
    boundaries = [prefix.rfind(value) for value in ("\n", "•", ". ", "? ", "! ")]
    boundary = max(boundaries)
    if boundary >= 0:
        window_start += boundary + 1
    else:
        window_start = start

    window_end = min(len(text), end + 220)
    suffix = text[end:window_end]
    endings = [position for value in ("\n", "•", ". ", "? ", "! ") if (position := suffix.find(value)) >= 0]
    if endings:
        window_end = end + min(endings) + 1
    return _evidence(text[window_start:window_end])


def _add_explicit_relation(
    relations: dict[tuple[str, str, str], RelationMention],
    *,
    subject: str,
    relation: str,
    object_value: str,
    doc_id: str,
    chunk_id: str,
    text: str,
    patterns: Iterable[str],
    confidence: float,
) -> None:
    match = _first_match(text, patterns)
    if match is None:
        return
    item = _relation(
        subject,
        relation,
        object_value,
        doc_id,
        chunk_id,
        _relation_evidence(text, match.start(), match.end()),
        confidence,
    )
    relations[(item.subject, item.relation, item.object)] = item


def extract_chunk_entities(
    doc_id: str,
    chunk_id: str,
    text: str,
    lexicon: dict[str, dict[str, list[str]]],
) -> list[EntityMention]:
    mentions: dict[tuple[str, str], EntityMention] = {}
    sentences = _sentences(text)

    for sentence in sentences:
        for entity_type, named_entities in lexicon.items():
            for canonical_name, aliases in named_entities.items():
                alias_match = (
                    _first_location_match(sentence, aliases, lexicon)
                    if entity_type == "location"
                    else _first_alias_match(sentence, aliases)
                )
                if alias_match is not None:
                    key = (entity_type, canonical_name.casefold())
                    mentions.setdefault(
                        key,
                        EntityMention(
                            entity_id=_stable_id("ENT", doc_id, chunk_id, entity_type, canonical_name.casefold()),
                            name=canonical_name,
                            normalized_name=canonical_name.casefold(),
                            entity_type=entity_type,
                            doc_id=doc_id,
                            chunk_id=chunk_id,
                            confidence=0.92,
                            evidence=_relation_evidence(
                                sentence,
                                alias_match.start(),
                                alias_match.end(),
                            ),
                        ),
                    )

        for river_match in RIVER_PATTERN.finditer(sentence):
            name = re.sub(r"^The\s+", "", river_match.group(1)).strip()
            key = ("river", name.casefold())
            mentions.setdefault(
                key,
                EntityMention(
                    entity_id=_stable_id("ENT", doc_id, chunk_id, "river", name.casefold()),
                    name=name,
                    normalized_name=name.casefold(),
                    entity_type="river",
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    confidence=0.8,
                    evidence=_relation_evidence(
                        sentence,
                        river_match.start(),
                        river_match.end(),
                    ),
                ),
            )

        for date_match in DATE_PATTERN.finditer(sentence):
            name = re.sub(r"\s+", "", date_match.group(0).replace("–", "-"))
            key = ("date", name.casefold())
            mentions.setdefault(
                key,
                EntityMention(
                    entity_id=_stable_id("ENT", doc_id, chunk_id, "date", name.casefold()),
                    name=name,
                    normalized_name=name.casefold(),
                    entity_type="date",
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    confidence=0.98,
                    evidence=_relation_evidence(
                        sentence,
                        date_match.start(),
                        date_match.end(),
                    ),
                ),
            )

    return sorted(mentions.values(), key=lambda item: (item.entity_type, item.normalized_name))


def _relation(
    subject: str,
    relation: str,
    object_value: str,
    doc_id: str,
    chunk_id: str,
    evidence: str,
    confidence: float,
) -> RelationMention:
    if relation not in RELATION_TYPES:
        raise ValueError(f"Unsupported relationship type: {relation}")
    return RelationMention(
        relation_id=_stable_id(
            "REL", doc_id, chunk_id, subject.casefold(), relation, object_value.casefold()
        ),
        subject=subject,
        relation=relation,
        object=object_value,
        doc_id=doc_id,
        chunk_id=chunk_id,
        evidence=evidence,
        confidence=confidence,
    )


def extract_chunk_relations(
    doc_id: str,
    chunk_id: str,
    text: str,
    entities: Iterable[EntityMention],
    lexicon: dict[str, dict[str, list[str]]],
) -> list[RelationMention]:
    entity_list = list(entities)
    relations: dict[tuple[str, str, str], RelationMention] = {}

    if evidence_quality_issues(text):
        return []

    for entity in entity_list:
        if entity.entity_type == "species":
            item = _relation(
                doc_id,
                "document_mentions_species",
                entity.name,
                doc_id,
                chunk_id,
                entity.evidence,
                0.98,
            )
            relations[(item.subject, item.relation, item.object)] = item
        elif entity.entity_type == "location":
            item = _relation(
                doc_id,
                "document_mentions_location",
                entity.name,
                doc_id,
                chunk_id,
                entity.evidence,
                0.98,
            )
            relations[(item.subject, item.relation, item.object)] = item

    species = [entity for entity in entity_list if entity.entity_type == "species"]
    habitats = [entity for entity in entity_list if entity.entity_type in {"habitat", "wetland"}]
    threats = [entity for entity in entity_list if entity.entity_type == "threat"]
    agencies = [entity for entity in entity_list if entity.entity_type == "agency"]
    programs = [entity for entity in entity_list if entity.entity_type == "program"]

    for species_entity in species:
        species_expression = _canonical_expression("species", species_entity.name, lexicon)
        for habitat_entity in habitats:
            habitat_expression = _canonical_expression(
                habitat_entity.entity_type,
                habitat_entity.name,
                lexicon,
            )
            _add_explicit_relation(
                relations,
                subject=species_entity.name,
                relation="species_uses_habitat",
                object_value=habitat_entity.name,
                doc_id=doc_id,
                chunk_id=chunk_id,
                text=text,
                patterns=(
                    habitat_expression
                    + RELATION_GAP
                    + r"\b(?:supports?|provides?)\b"
                    + RELATION_GAP
                    + r"\bspecies\s+such\s+as\b"
                    + RELATION_GAP
                    + species_expression,
                ),
                confidence=0.90,
            )
            _add_explicit_relation(
                relations,
                subject=species_entity.name,
                relation="species_uses_habitat",
                object_value=habitat_entity.name,
                doc_id=doc_id,
                chunk_id=chunk_id,
                text=text,
                patterns=(
                    species_expression + RELATION_GAP + SPECIES_HABITAT_ACTIVE + HABITAT_TARGET_LINK + habitat_expression,
                    habitat_expression + RELATION_GAP + SPECIES_HABITAT_REVERSE + SPECIES_TARGET_LINK + species_expression,
                ),
                confidence=0.93,
            )

    for threat_entity in threats:
        threat_expression = _canonical_expression("threat", threat_entity.name, lexicon)
        for species_entity in species:
            species_expression = _canonical_expression("species", species_entity.name, lexicon)
            _add_explicit_relation(
                relations,
                subject=threat_entity.name,
                relation="threat_affects_species",
                object_value=species_entity.name,
                doc_id=doc_id,
                chunk_id=chunk_id,
                text=text,
                patterns=(
                    threat_expression + RELATION_GAP + THREAT_ACTIVE + THREAT_TARGET_LINK + species_expression,
                    species_expression + RELATION_GAP + THREAT_PASSIVE + RELATION_GAP + threat_expression,
                ),
                confidence=0.94,
            )

    for agency_entity in agencies:
        agency_expression = _canonical_expression("agency", agency_entity.name, lexicon)
        for program_entity in programs:
            program_expression = _canonical_expression("program", program_entity.name, lexicon)
            _add_explicit_relation(
                relations,
                subject=agency_entity.name,
                relation="agency_manages_program",
                object_value=program_entity.name,
                doc_id=doc_id,
                chunk_id=chunk_id,
                text=text,
                patterns=(
                    agency_expression + r"(?:'s|’s)" + RELATION_GAP + program_expression,
                ),
                confidence=0.90,
            )
            _add_explicit_relation(
                relations,
                subject=agency_entity.name,
                relation="agency_manages_program",
                object_value=program_entity.name,
                doc_id=doc_id,
                chunk_id=chunk_id,
                text=text,
                patterns=(
                    agency_expression + RELATION_GAP + AGENCY_ACTIVE + PROGRAM_TARGET_LINK + program_expression,
                    program_expression + RELATION_GAP + AGENCY_PASSIVE + RELATION_GAP + agency_expression,
                ),
                confidence=0.95,
            )

    return sorted(relations.values(), key=lambda item: (item.relation, item.subject, item.object))


def replace_extractions(
    connection: sqlite3.Connection,
    doc_ids: Iterable[str],
    entities: Iterable[EntityMention],
    relations: Iterable[RelationMention],
) -> None:
    selected_ids = sorted(set(doc_ids))
    if selected_ids:
        placeholders = ",".join("?" for _ in selected_ids)
        connection.execute(f"DELETE FROM relations WHERE doc_id IN ({placeholders})", selected_ids)
        connection.execute(f"DELETE FROM entities WHERE doc_id IN ({placeholders})", selected_ids)

    connection.executemany(
        """
        INSERT INTO entities (
            entity_id, name, normalized_name, entity_type, doc_id, chunk_id, confidence, evidence
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            (
                item.entity_id,
                item.name,
                item.normalized_name,
                item.entity_type,
                item.doc_id,
                item.chunk_id,
                item.confidence,
                item.evidence,
            )
            for item in entities
        ),
    )
    connection.executemany(
        """
        INSERT INTO relations (
            relation_id, subject, relation, object, doc_id, chunk_id, evidence, confidence
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            (
                item.relation_id,
                item.subject,
                item.relation,
                item.object,
                item.doc_id,
                item.chunk_id,
                item.evidence,
                item.confidence,
            )
            for item in relations
        ),
    )


def extract_database(
    *,
    database_path: Path = DATABASE_PATH,
    selected_ids: Iterable[str] | None = None,
    lexicon_path: Path = LEXICON_PATH,
) -> tuple[list[EntityMention], list[RelationMention]]:
    lexicon = load_lexicon(lexicon_path)
    selected = set(selected_ids) if selected_ids is not None else None
    with connect_database(database_path) as connection:
        rows = connection.execute(
            "SELECT chunk_id, doc_id, chunk_text FROM chunks ORDER BY chunk_id"
        ).fetchall()
        if selected is not None:
            rows = [row for row in rows if row["doc_id"] in selected]

        entities: list[EntityMention] = []
        relations: list[RelationMention] = []
        for row in rows:
            chunk_entities = extract_chunk_entities(
                row["doc_id"], row["chunk_id"], row["chunk_text"], lexicon
            )
            entities.extend(chunk_entities)
            relations.extend(
                extract_chunk_relations(
                    row["doc_id"], row["chunk_id"], row["chunk_text"], chunk_entities, lexicon
                )
            )
        doc_ids = selected or {row["doc_id"] for row in rows}
        replace_extractions(connection, doc_ids, entities, relations)
    return entities, relations


def export_extractions(
    *,
    database_path: Path = DATABASE_PATH,
    output_dir: Path = OUTPUTS_DIR,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    entities_path = output_dir / "entities.csv"
    relations_path = output_dir / "relations.csv"
    with connect_database(database_path) as connection:
        entity_rows = connection.execute(
            """
            SELECT entity_id, name, normalized_name, entity_type, doc_id, chunk_id,
                   confidence, evidence
            FROM entities ORDER BY entity_type, normalized_name, doc_id, chunk_id
            """
        ).fetchall()
        relation_rows = connection.execute(
            """
            SELECT relation_id, subject, relation, object, doc_id, chunk_id,
                   evidence, confidence
            FROM relations ORDER BY relation, subject, object, doc_id, chunk_id
            """
        ).fetchall()

    with entities_path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=list(asdict(EntityMention("", "", "", "", "", "", 0, "")).keys()),
        )
        writer.writeheader()
        writer.writerows(dict(row) for row in entity_rows)
    with relations_path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=list(
                asdict(RelationMention("", "", "", "", "", "", "", 0)).keys()
            ),
        )
        writer.writeheader()
        writer.writerows(dict(row) for row in relation_rows)
    return entities_path, relations_path
