import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

# Liste entities
def get_entities(text):
    doc = nlp(text)

    characters = Counter()
    locations = Counter()

    for ent in doc.ents:
        name = " ".join(ent.text.split())

        if ent.label_ == "PERSON":
            characters[name] += 1

        elif ent.label_ in ["GPE", "LOC"]:
            locations[name] += 1

    return {
        "characters": get_names_by_frequency(characters),
        "locations": get_names_by_frequency(locations)
    }

# Retirer les counter pour garder seulement les noms
def get_names_by_frequency(counter):
    names = []

    for name, count in counter.most_common():
        names.append(name)

    return names