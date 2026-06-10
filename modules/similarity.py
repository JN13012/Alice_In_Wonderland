from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.gutenberg import load_book
from utils.text_processing import remove_header_footer


BOOK_COLLECTION = {
    "11": {
        "title": "Alice's Adventures in Wonderland",
        "authors": "Lewis Carroll",
        "bookshelves": "Children / Young Adult",
    },
    "12": {
        "title": "Through the Looking-Glass",
        "authors": "Lewis Carroll",
        "bookshelves": "Children / Young Adult",
    },
    "16": {
        "title": "Peter Pan",
        "authors": "J. M. Barrie",
        "bookshelves": "Children / Young Adult",
    },
    "55": {
        "title": "The Wonderful Wizard of Oz",
        "authors": "L. Frank Baum",
        "bookshelves": "Children / Young Adult",
    },
    "113": {
        "title": "The Secret Garden",
        "authors": "Frances Hodgson Burnett",
        "bookshelves": "Children / Young Adult",
    },
    "120": {
        "title": "Treasure Island",
        "authors": "Robert Louis Stevenson",
        "bookshelves": "Children / Young Adult",
    },
    "236": {
        "title": "The Jungle Book",
        "authors": "Rudyard Kipling",
        "bookshelves": "Children / Young Adult",
    },
    "108": {
        "title": "The Return of Sherlock Holmes",
        "authors": "Arthur Conan Doyle",
        "bookshelves": "Crime, Mystery & Thriller",
    },
    "834": {
        "title": "The Memoirs of Sherlock Holmes",
        "authors": "Arthur Conan Doyle",
        "bookshelves": "Crime, Mystery & Thriller",
    },
    "863": {
        "title": "The Mysterious Affair at Styles",
        "authors": "Agatha Christie",
        "bookshelves": "Crime, Mystery & Thriller",
    },
    "1661": {
        "title": "The Adventures of Sherlock Holmes",
        "authors": "Arthur Conan Doyle",
        "bookshelves": "Crime, Mystery & Thriller",
    },
    "61262": {
        "title": "Poirot Investigates",
        "authors": "Agatha Christie",
        "bookshelves": "Crime, Mystery & Thriller",
    },
    "69087": {
        "title": "The Murder of Roger Ackroyd",
        "authors": "Agatha Christie",
        "bookshelves": "Crime, Mystery & Thriller",
    },
    "70114": {
        "title": "The Big Four",
        "authors": "Agatha Christie",
        "bookshelves": "Crime, Mystery & Thriller",
    },
    "35": {
        "title": "The Time Machine",
        "authors": "H. G. Wells",
        "bookshelves": "Science-Fiction & Fantasy",
    },
    "36": {
        "title": "The War of the Worlds",
        "authors": "H. G. Wells",
        "bookshelves": "Science-Fiction & Fantasy",
    },
    "84": {
        "title": "Frankenstein; Or, The Modern Prometheus",
        "authors": "Mary Wollstonecraft Shelley",
        "bookshelves": "Science-Fiction & Fantasy",
    },
    "159": {
        "title": "The Island of Doctor Moreau",
        "authors": "H. G. Wells",
        "bookshelves": "Science-Fiction & Fantasy",
    },
    "164": {
        "title": "Twenty Thousand Leagues under the Sea",
        "authors": "Jules Verne",
        "bookshelves": "Science-Fiction & Fantasy",
    },
    "345": {
        "title": "Dracula",
        "authors": "Bram Stoker",
        "bookshelves": "Science-Fiction & Fantasy",
    },
    "68283": {
        "title": "The Call of Cthulhu",
        "authors": "H. P. Lovecraft",
        "bookshelves": "Science-Fiction & Fantasy",
    },
}


def get_book_info(book_id):
    book_id = str(book_id)

    if book_id in BOOK_COLLECTION:
        info = BOOK_COLLECTION[book_id]
        return {
            "id": book_id,
            "authors": info["authors"],
            "bookshelves": info["bookshelves"],
        }

    return {
        "id": book_id,
        "authors": "Unknown",
        "bookshelves": "Unknown",
    }


def get_similar_books(book_id, limit=5):
    book_id = str(book_id)
    ids = list(BOOK_COLLECTION.keys())

    if book_id not in BOOK_COLLECTION:
        ids.append(book_id)

    documents = []

    for current_id in ids:
        text = load_book(current_id)
        clean_text = remove_header_footer(text)
        documents.append(clean_text)

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    matrix = vectorizer.fit_transform(documents)

    target_index = ids.index(book_id)
    similarities = cosine_similarity(matrix[target_index], matrix)[0]

    scored_books = []

    for index, score in enumerate(similarities):
        current_id = ids[index]

        if current_id == book_id:
            continue

        if current_id not in BOOK_COLLECTION:
            continue

        title = BOOK_COLLECTION[current_id]["title"]
        scored_books.append((title, score))

    scored_books.sort(key=lambda item: item[1], reverse=True)

    similar_titles = []

    for title, score in scored_books[:limit]:
        similar_titles.append(title)

    return similar_titles
