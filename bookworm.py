from utils.text_processing import remove_header_footer
from utils.gutenberg import get_book
from utils.gutenberg import save_book

# Main logic
def main ():
    book_id = input("Enter book id : ")
    full_text = get_book(book_id)
    cut_text = remove_header_footer(full_text)
    save_book(book_id, cut_text)
    print (f"Book {book_id} saved.") 
    
if __name__ == "__main__":
    main()