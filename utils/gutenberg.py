import requests
from pathlib import Path

def get_book(book_id):
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    
    response = requests.get(url)
    response.raise_for_status()
    
    return response.text

def save_book(book_id, text):
    path = Path("data/books") / f"{book_id}.txt"
    with open (path, "w", encoding="utf8") as file:
        file.write(text)
    
def main ():
    book_id = input("Enter book id : ")
    text = get_book(book_id)
    save_book(book_id, text)
    print (f"Book {book_id} saved.") 
    
if __name__ == "__main__":
    main()