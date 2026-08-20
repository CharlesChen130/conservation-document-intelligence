from __future__ import annotations

from src.conservation_intelligence.entity_extraction import (
    extract_chunk_entities,
    extract_chunk_relations,
    load_lexicon,
)


def test_rule_extraction_produces_evidence_backed_entities_and_relations():
    text = (
        "The U.S. Fish and Wildlife Service manages the North American Waterfowl "
        "Management Plan. Silver carp use aquatic habitat in the Missouri River. "
        "Pollution threatens silver carp populations in Missouri."
    )
    lexicon = load_lexicon()

    entities = extract_chunk_entities("DOC999", "DOC999-C0001", text, lexicon)
    relations = extract_chunk_relations(
        "DOC999", "DOC999-C0001", text, entities, lexicon
    )

    entity_pairs = {(item.entity_type, item.name) for item in entities}
    relation_triples = {(item.subject, item.relation, item.object) for item in relations}
    assert ("species", "Silver carp") in entity_pairs
    assert ("habitat", "Aquatic habitat") in entity_pairs
    assert (
        "U.S. Fish and Wildlife Service",
        "agency_manages_program",
        "North American Waterfowl Management Plan",
    ) in relation_triples
    assert ("Silver carp", "species_uses_habitat", "Aquatic habitat") in relation_triples
    assert ("DOC999", "document_mentions_location", "Missouri") in relation_triples
    assert all(item.evidence for item in relations)


def _relations_for(text: str):
    lexicon = load_lexicon()
    entities = extract_chunk_entities("DOC999", "DOC999-C0001", text, lexicon)
    return extract_chunk_relations(
        "DOC999",
        "DOC999-C0001",
        text,
        entities,
        lexicon,
    )


def test_semantic_relations_require_direct_predicates_not_long_range_cooccurrence():
    text = (
        "Wetlands provide habitat for amphibians while lake sturgeon are discussed in a table. • "
        "Forest and wetland planning table. • "
        "The agency uses monitoring results to support conservation. "
        "U.S. Fish and Wildlife Service contributors include program reviewers. "
        "The North American Waterfowl Management Plan appears in the bibliography."
    )

    semantic = {
        item.relation
        for item in _relations_for(text)
        if not item.relation.startswith("document_mentions_")
    }

    assert semantic == set()


def test_semantic_relations_support_active_passive_and_possessive_wording():
    text = (
        "Silver carp inhabit aquatic habitat. "
        "Wetlands provide seasonal habitat for mallards. "
        "Coastal wetlands support species such as frogs, zebra mussels. "
        "The American black duck can be found in saltwater marshes. "
        "Zebra mussels are threatened by pollution. "
        "USGS's Nonindigenous Aquatic Species Database tracks introduced species."
    )

    triples = {(item.subject, item.relation, item.object) for item in _relations_for(text)}

    assert ("Silver carp", "species_uses_habitat", "Aquatic habitat") in triples
    assert ("Mallard", "species_uses_habitat", "Wetland") in triples
    assert ("Zebra mussel", "species_uses_habitat", "Wetland") in triples
    assert ("American black duck", "species_uses_habitat", "Marsh") in triples
    assert ("Pollution", "threat_affects_species", "Zebra mussel") in triples
    assert (
        "U.S. Geological Survey",
        "agency_manages_program",
        "Nonindigenous Aquatic Species Database",
    ) in triples


def test_lowercase_us_does_not_create_united_states_location():
    lexicon = load_lexicon()

    lowercase = extract_chunk_entities(
        "DOC999",
        "DOC999-C0001",
        "This report helps us understand wetlands.",
        lexicon,
    )
    uppercase = extract_chunk_entities(
        "DOC999",
        "DOC999-C0002",
        "US agencies monitor wetlands.",
        lexicon,
    )

    assert not any(item.name == "United States" for item in lowercase)
    assert any(item.name == "United States" for item in uppercase)


def test_location_aliases_exclude_organizations_and_prefer_longer_places():
    lexicon = load_lexicon()
    text = (
        "U.S. Fish and Wildlife Service and Missouri Department of Natural Resources "
        "worked outside the US near the Missouri River."
    )

    entities = extract_chunk_entities(
        "DOC999",
        "DOC999-C0001",
        text,
        lexicon,
    )
    locations = {item.name for item in entities if item.entity_type == "location"}

    assert "United States" in locations
    assert "Missouri River" in locations
    assert "Missouri" not in locations


def test_entity_evidence_is_centered_on_alias_in_long_ocr_units():
    lexicon = load_lexicon()
    text = ("front matter without punctuation " * 40) + "Missouri conservation planning"

    entities = extract_chunk_entities(
        "DOC999",
        "DOC999-C0001",
        text,
        lexicon,
    )
    missouri = next(item for item in entities if item.name == "Missouri")

    assert "Missouri" in missouri.evidence
    assert len(missouri.evidence) <= 500


def test_reference_chunks_do_not_emit_relations():
    text = (
        "References. Silver carp use aquatic habitat. "
        "Smith 2018 doi:1; Jones 2019 doi:2; Lee 2020 doi:3; Patel 2021 doi:4; "
        "Garcia 2022; Brown 2023; White 2024; Green 2025."
    )

    assert _relations_for(text) == []
