from utils.gutenberg import get_book
from utils.gutenberg import save_book

from utils.text_processing import remove_header_footer
from utils.text_processing import tokenize_words

from modules.lexdiv import get_lexdiv_metrics




# Main logic
def main ():
    book_id = input("Enter book id : ")
    full_text = get_book(book_id)
    cut_text = remove_header_footer(full_text)
    save_book(book_id, cut_text)
    words = tokenize_words(cut_text)
    lexdiv = get_lexdiv_metrics(words)
    print (f"Book {book_id} saved.")
    print (lexdiv)
    
if __name__ == "__main__":
    main()