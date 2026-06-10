import requests
from pathlib import Path

BOOKS_DIR = Path("data/books")

# Download full book.txt
def get_book(book_id):
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    
    # getter url renvoie un objet request et vérifie le statut de la réponse.
    response = requests.get(url)
    response.raise_for_status()
    
    #response.text (récupere la partie text de la requête)
    return response.text

# Save book in data/books
def save_book(book_id, text):
    path = BOOKS_DIR / f"{book_id}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open (path, "w", encoding="utf8") as file:
        file.write(text)

# Load book from data/books if exist sinon download
def load_book(book_id):
    path = BOOKS_DIR / f"{book_id}.txt"

    if path.exists():
        with open(path, "r", encoding="utf8") as file:
            return file.read()

    text = get_book(book_id)
    save_book(book_id, text)
    return text
