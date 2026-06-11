import re
from collections import Counter

import spacy


MAX_ENTITIES = 20
NLP = None

INVALID_ENTITY_WORDS = {
    "adventures",
    "chapter",
    "copyright",
    "ebook",
    "gutenberg",
    "latitude",
    "longitude",
    "project",
}

INVALID_ENTITY_NAMES = {
    "Majesty",
    "Miss",
    "Said",
}

INVALID_LOCATION_NAMES = {
    "Cat",
    "Crab",
    "Dinah",
    "Duchess",
    "Esq",
    "Latin Grammar",
    "Magpie",
    "Mouse",
    "Pigeon",
    "Tillie",
    "Tortoise",
}


def load_nlp():
    global NLP

    if NLP is not None:
        return NLP

    try:
        NLP = spacy.load("en_core_web_sm")
    except OSError:
        print("Missing SpaCy model. Run: python -m spacy download en_core_web_sm")
        return None

    return NLP


# Liste entities
def get_entities(text):
    nlp = load_nlp()

    if nlp is None:
        return {
            "characters": [],
            "locations": [],
        }

    doc = nlp(text)

    characters = Counter()
    locations = Counter()

    for ent in doc.ents:
        name = clean_entity_name(ent.text)

        if not is_valid_entity_name(name):
            continue

        if ent.label_ == "PERSON":
            characters[name] += 1

        elif ent.label_ in ["GPE", "LOC"] and is_valid_location_name(name):
            locations[name] += 1

    character_names = get_names_by_frequency(characters)
    location_names = get_names_by_frequency(locations)
    character_set = set(character_names)

    filtered_locations = []
    for name in location_names:
        if name not in character_set:
            filtered_locations.append(name)

    return {
        "characters": character_names[:MAX_ENTITIES],
        "locations": filtered_locations[:MAX_ENTITIES],
    }


def clean_entity_name(name):
    name = " ".join(name.split())
    name = name.replace("’s", "")
    name = name.replace("'s", "")
    name = name.strip(" \t\n\r,.;:!?\"'()[]{}")

    return name


def is_valid_entity_name(name):
    if len(name) < 3:
        return False

    if name in INVALID_ENTITY_NAMES:
        return False

    if "_" in name:
        return False

    if name.isdigit():
        return False

    lowered_name = name.lower()

    if lowered_name.startswith("the "):
        return False

    for invalid_word in INVALID_ENTITY_WORDS:
        if invalid_word in lowered_name:
            return False

    if not re.search(r"[A-Za-z]", name):
        return False

    if len(name.split()) > 4:
        return False

    return True


def is_valid_location_name(name):
    if name in INVALID_LOCATION_NAMES:
        return False

    if not name[0].isupper():
        return False

    return True


# Retirer les counter pour garder seulement les noms
def get_names_by_frequency(counter):
    names = []

    for name, count in counter.most_common():
        names.append(name)

    return names
