from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en.stop_words import STOP_WORDS
from utils.text_processing import split_sections


CUSTOM_STOP_WORDS = {
    "answered",
    "asked",
    "book",
    "came",
    "chapter",
    "copyright",
    "couldn",
    "cried",
    "didn",
    "doesn",
    "don",
    "ebook",
    "gutenberg",
    "http",
    "https",
    "isn",
    "license",
    "ll",
    "looked",
    "project",
    "re",
    "replied",
    "said",
    "say",
    "says",
    "shouldn",
    "thing",
    "things",
    "thought",
    "time",
    "ve",
    "wasn",
    "way",
    "went",
    "weren",
    "wouldn",
    "www",
}


def get_topics(text, words_per_section=10):
    raw_sections = split_sections(text)
    chapters = []

    for section in raw_sections:
        if len(section.split()) >= 80:
            chapters.append(section)

    if not chapters:
        return {}

    stop_words = list(STOP_WORDS.union(CUSTOM_STOP_WORDS))

    vectorizer = TfidfVectorizer(
        lowercase=True,
        max_df=0.9,
        stop_words=stop_words,
        token_pattern=r"(?u)\b[a-zA-Z]{3,}\b",
    ) #Crée objet sans les mots inutiles anglais
    matrix = vectorizer.fit_transform(chapters) # fit => apprend le vocabulaire et transform => matrice tableau

    words = vectorizer.get_feature_names_out()

    topics = {}

    for  chapter_index in range(matrix.shape[0]): # matrix.shape = nombre de raw => nombre de chapitre
        scores = matrix[chapter_index].toarray()[0] # récupere les scores du chapitre actuel
        best_indexes = scores.argsort()[::-1] #Tri les scores des mots du plus haut au plus bas.

        top_words = []

        for index in best_indexes:
            if scores[index] == 0:
                continue

            top_words.append(words[index])

            if len(top_words) == words_per_section:
                break

        topics[chapter_index + 1] = top_words

    return topics
