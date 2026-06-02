import requests
from pathlib import Path

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
