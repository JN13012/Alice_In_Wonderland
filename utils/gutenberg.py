import requests

book_id = "",

    def get_book(book_id):
        url = "https://www.gutenberg.org/cache/epub/78785/pg78785-images.html"
        query_parameters = { "download format" : "txt"}
        response = requests.get(url, params=query_parameters)

        return response.text

    text = get_book()

    def save_book(book_id, text):
        with open ("data/books/{book_id}.txt", "w", encoding="utf8") as file:
            file.write(response.content)
            return