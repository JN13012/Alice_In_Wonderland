from modules.entities import get_entities
from modules.topics import get_topics
from collections import Counter


THEME_KEYWORDS = {
    "adventure": {
        "adventure", "boat", "captain", "door", "escape", "island", "journey",
        "road", "ship", "travel", "voyage",
    },
    "animals": {
        "bird", "birds", "cat", "cats", "dog", "hare", "horse", "mouse",
        "pigeon", "rabbit", "serpent", "turtle",
    },
    "authority and society": {
        "court", "duchess", "executioner", "judge", "jury", "king", "law",
        "queen", "soldiers", "trial", "witness",
    },
    "childhood": {
        "child", "children", "dream", "girl", "nursery", "school", "sister",
        "youth",
    },
    "mystery": {
        "case", "clue", "crime", "detective", "evidence", "investigation",
        "murder", "secret", "witness",
    },
    "nature": {
        "flower", "forest", "garden", "grass", "river", "sea", "tree",
        "wood",
    },
    "science and fantasy": {
        "creature", "dream", "machine", "magic", "monster", "strange",
        "wonder",
    },
}


def get_summary(text, book_info=None, entities=None, topics=None):
    if book_info is None:
        book_info = {}

    authors = book_info.get("authors", "Unknown")
    excluded_names = []

    if authors != "Unknown":
        excluded_names.append(authors)

    if entities is None:
        entities = get_entities(text, excluded_names)

    if topics is None:
        topics = get_topics(text)

    characters = entities["characters"][:3]
    locations = entities["locations"][:2]
    topic_words = get_main_topic_words(topics, limit=8)
    themes = get_theme_labels(topic_words, limit=3)

    sentences = []
    title = book_info.get("title", "This book")
    bookshelves = book_info.get("bookshelves", "Unknown")

    if title != "Unknown" and authors != "Unknown":
        sentences.append(f"{title} is a book written by {authors}.")
    elif title != "Unknown":
        sentences.append(f"{title} is a book from Project Gutenberg.")
    else:
        sentences.append("This book is a Project Gutenberg text.")

    if bookshelves != "Unknown":
        sentences.append(f"It belongs to the {bookshelves} category.")

    if themes:
        sentences.append(f"It explores themes of {format_list(themes)}.")

    if characters and locations:
        sentences.append(
            f"The text focuses on characters such as {format_list(characters)}, "
            f"with places such as {format_list(locations)}."
        )
    elif characters:
        sentences.append(f"The text focuses on characters such as {format_list(characters)}.")
    elif locations:
        sentences.append(f"Recurring places include {format_list(locations)}.")

    if topic_words:
        sentences.append(f"Its most distinctive keywords include {format_list(topic_words[:5])}.")

    return " ".join(sentences)


def get_main_topic_words(topics, limit=5):
    word_count = Counter()

    for section_words in topics.values():
        for word in section_words:
            word_count[word] += 1

    words = []

    for word, count in word_count.most_common(limit):
        words.append(word)

    return words


def get_theme_labels(topic_words, limit=3):
    scores = Counter()

    for word in topic_words:
        for theme, keywords in THEME_KEYWORDS.items():
            if word in keywords:
                scores[theme] += 1

    themes = []

    for theme, score in scores.most_common(limit):
        themes.append(theme)

    return themes


def format_list(items):
    if len(items) == 1:
        return items[0]

    if len(items) == 2:
        return f"{items[0]} and {items[1]}"

    return f"{', '.join(items[:-1])}, and {items[-1]}"
