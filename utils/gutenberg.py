import requests
from pathlib import Path
from text_processing import remove_header

# Download full book.txt
def get_book(book_id):
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    
    response = requests.get(url)
    response.raise_for_status()
    
    return response.text

# Save book in data/books
def save_book(book_id, text):
    path = Path("data/books") / f"{book_id}.txt"
    with open (path, "w", encoding="utf8") as file:
        file.write(text)

# Main logic
def main ():
    book_id = input("Enter book id : ")
    full_text = get_book(book_id)
    cut_text = remove_header(full_text)
    save_book(book_id, cut_text)
    print (f"Book {book_id} saved.") 
    
if __name__ == "__main__":
    main()