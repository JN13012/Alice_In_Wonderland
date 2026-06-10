from modules.entities import get_entities
from modules.topics import get_topics
from collections import Counter


def get_summary(text):
    entities = get_entities(text)
    topics = get_topics(text)

    characters = entities["characters"][:3]
    locations = entities["locations"][:3]
    topic_words = get_main_topic_words(topics, limit=5)

    sentences = []

    if characters:
        sentences.append(f"This book focuses on {format_list(characters)}.")

    if locations:
        sentences.append(f"Important locations include {format_list(locations)}.")

    if topic_words:
        sentences.append(f"Main topics include {format_list(topic_words)}.")

    if not sentences:
        return "This book does not contain enough extracted information to build a summary."

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


def format_list(items):
    if len(items) == 1:
        return items[0]

    if len(items) == 2:
        return f"{items[0]} and {items[1]}"

    return f"{', '.join(items[:-1])}, and {items[-1]}"
