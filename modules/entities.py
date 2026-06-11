import re
from collections import Counter

import spacy


MAX_ENTITIES = 20
NLP = None

INVALID_ENTITY_WORDS = {
    "chapter",
    "copyright",
    "ebook",
    "gutenberg",
    "latitude",
    "license",
    "longitude",
    "project",
}

INVALID_STANDALONE_NAMES = {
    "Madam",
    "Majesty",
    "Miss",
    "Mister",
    "Mr",
    "Mrs",
    "Said",
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
def get_entities(text, excluded_names=None):
    if excluded_names is None:
        excluded_names = []

    excluded_names = set(excluded_names)
    nlp = load_nlp()

    if nlp is None:
        return {
            "characters": [],
            "locations": [],
        }

    text = remove_heading_lines(text)
    doc = nlp(text)

    characters = Counter()
    locations = Counter()

    for ent in doc.ents:
        name = clean_entity_name(ent.text)

        if not is_valid_entity_name(name):
            continue

        if name in excluded_names:
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


def remove_heading_lines(text):
    cleaned_lines = []

    for line in text.splitlines():
        stripped_line = line.strip()

        if is_probable_heading(stripped_line):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def is_probable_heading(line):
    if not line:
        return False

    lowered_line = line.lower()

    if re.match(r"^chapter\s+[ivxlcdm\d]+", lowered_line):
        return True

    if len(line.split()) <= 6 and line == line.upper():
        return True

    return False


def clean_entity_name(name):
    name = " ".join(name.split())
    name = name.replace("’s", "")
    name = name.replace("'s", "")
    name = name.strip(" \t\n\r,.;:!?\"'()[]{}")

    return name


def is_valid_entity_name(name):
    if len(name) < 3:
        return False

    if name in INVALID_STANDALONE_NAMES:
        return False

    if not name[0].isupper():
        return False

    if "_" in name:
        return False

    if name.isdigit():
        return False

    lowered_name = name.lower()

    for invalid_word in INVALID_ENTITY_WORDS:
        if invalid_word in lowered_name:
            return False

    if not re.search(r"[A-Za-z]", name):
        return False

    if len(name.split()) > 4:
        return False

    return True


def is_valid_location_name(name):
    if not name[0].isupper():
        return False

    return True


# Retirer les counter pour garder seulement les noms
def get_names_by_frequency(counter):
    names = []

    for name, count in counter.most_common():
        names.append(name)

    return names
