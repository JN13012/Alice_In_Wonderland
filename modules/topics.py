from sklearn.feature_extraction.text import TfidfVectorizer
from utils.text_processing import split_sections

def get_topics(text, words_per_section=10):
    chapters = split_sections(text)

    vectorizer = TfidfVectorizer(stop_words="english") #Crée objet sans les mots inutiles anglais
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
