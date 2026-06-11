import sys
from utils.gutenberg import load_book
from utils.gutenberg import save_book
from utils.text_processing import remove_header_footer
from utils.text_processing import tokenize_words
from modules.lexdiv import get_lexdiv_metrics
from modules.topics import get_topics
from modules.entities import get_entities
from modules.summarize import get_summary
from modules.similarity import get_book_info, get_similar_books
from modules.card import build_card
from utils.cache import load_cache, save_cache


LEXDIV_CACHE = "lexdiv"
TOPICS_CACHE = "topics_v5"
ENTITIES_CACHE = "entities_v11"
SUMMARY_CACHE = "summary_hybrid_v7"
SIMILAR_CACHE = "similar_v2"
CARD_CACHE = "card_v18"


def main ():
    if len(sys.argv) < 2:
        help()
        return

    option = sys.argv[1]

    if option == "--help":
        help()

    elif option == "--lexdiv":
        if len(sys.argv) < 3:
            print("Usage: python bookworm.py --lexdiv <book_id>")
            return

        book_id = sys.argv[2]
        lexdiv(book_id)

    elif option == "--topics":
        if len(sys.argv) < 3:
            print("Usage: python bookworm.py --topics <book_id>")
            return
        book_id = sys.argv[2]
        topics(book_id)

    elif option == "--entities":
        if len(sys.argv) < 3:
            print("Usage: python bookworm.py --entities <book_id>")
            return

        book_id = sys.argv[2]
        entities(book_id)

    elif option == "--summarize":
        if len(sys.argv) < 3:
            print("Usage: python bookworm.py --summarize <book_id>")
            return

        book_id = sys.argv[2]
        summarize(book_id)

    elif option == "--similar":
        if len(sys.argv) < 3:
            print("Usage: python bookworm.py --similar <book_id>")
            return

        book_id = sys.argv[2]
        similar(book_id)

    elif option == "--card":
        if len(sys.argv) < 3:
            print("Usage: python bookworm.py --card <book_id>")
            return

        book_id = sys.argv[2]
        card(book_id)

    else:
        print(f"Unknown option: {option}. Type --help")
    
def help ():
    print("\n Usage: python bookworm.py --option <book_id>.\n Avaible options : --lexdiv ; --topics ; --entities ; --summarize ; --similar ; --card \n")

def get_clean_book(book_id):
    full_text = load_book(book_id)
    cut_text = remove_header_footer(full_text)
    save_book(book_id, cut_text)
    return cut_text
    
def lexdiv (book_id):
    cached = load_cache(book_id, LEXDIV_CACHE)
    if cached is not None:
        print(cached)
        return

    cut_text = get_clean_book(book_id)
    words = tokenize_words(cut_text)
    metrics = get_lexdiv_metrics(words)
    save_cache(book_id, LEXDIV_CACHE, metrics)
    print (metrics)

def topics (book_id):
    cached = load_cache(book_id, TOPICS_CACHE)
    if cached is not None:
        cached = {int(section): words for section, words in cached.items()}
        print(cached)
        return
    
    cut_text = get_clean_book(book_id)
    result = get_topics(cut_text)
    save_cache(book_id, TOPICS_CACHE, result)
    print (result)

def entities(book_id):
    cached = load_cache(book_id, ENTITIES_CACHE)
    if cached is not None:
        print(cached)
        return

    cut_text = get_clean_book(book_id)
    info = get_book_info(book_id)
    result = get_entities(cut_text, [info["authors"]])
    save_cache(book_id, ENTITIES_CACHE, result)

    print(result)

def summarize(book_id):
    cached = load_cache(book_id, SUMMARY_CACHE)
    if cached is not None:
        print(cached)
        return

    cut_text = get_clean_book(book_id)
    info = get_book_info(book_id)
    result = get_summary(cut_text, info)
    save_cache(book_id, SUMMARY_CACHE, result)

    print(result)

def similar(book_id):
    cached = load_cache(book_id, SIMILAR_CACHE)
    if cached is not None:
        print(cached)
        return

    result = get_similar_books(book_id)
    save_cache(book_id, SIMILAR_CACHE, result)
    print(result)

def card(book_id):
    cached = load_cache(book_id, CARD_CACHE)
    if cached is not None:
        if "topics" in cached:
            cached["topics"] = {int(section): words for section, words in cached["topics"].items()}
        print_card(cached)
        return

    cut_text = get_clean_book(book_id)
    words = tokenize_words(cut_text)

    lexdiv_result = load_cache(book_id, LEXDIV_CACHE)
    if lexdiv_result is None:
        lexdiv_result = get_lexdiv_metrics(words)
        save_cache(book_id, LEXDIV_CACHE, lexdiv_result)

    topics_result = load_cache(book_id, TOPICS_CACHE)
    if topics_result is None:
        topics_result = get_topics(cut_text)
        save_cache(book_id, TOPICS_CACHE, topics_result)
    else:
        topics_result = {int(section): words for section, words in topics_result.items()}

    info = get_book_info(book_id)

    entities_result = load_cache(book_id, ENTITIES_CACHE)
    if entities_result is None:
        entities_result = get_entities(cut_text, [info["authors"]])
        save_cache(book_id, ENTITIES_CACHE, entities_result)

    summary_result = load_cache(book_id, SUMMARY_CACHE)
    if summary_result is None:
        summary_result = get_summary(cut_text, info, entities_result, topics_result)
        save_cache(book_id, SUMMARY_CACHE, summary_result)

    similar_result = load_cache(book_id, SIMILAR_CACHE)
    if similar_result is None:
        similar_result = get_similar_books(book_id)
        save_cache(book_id, SIMILAR_CACHE, similar_result)

    result = build_card(
        info,
        lexdiv_result,
        topics_result,
        entities_result,
        summary_result,
        similar_result,
    )
    save_cache(book_id, CARD_CACHE, result)
    print_card(result)


def print_card(card_result):
    keys = ["info", "lexdiv", "topics", "entities", "summary", "similar"]

    print("{")

    for index, key in enumerate(keys):
        value = card_result[key]
        comma = "," if index < len(keys) - 1 else ""
        print(f'  "{key}": {repr(value)}{comma}')

    print("}")

    
if __name__ == "__main__":
    main()
