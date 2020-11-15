import os
import django
import json
import requests
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Alejandria.settings")
django.setup()

from books.models import *


def isbn_10__to__isbn_13(isbn_10):
    str_isbn_12 = "978" + str(isbn_10[0][:-1])
    list_isbn_12 = [int(digit) for digit in str_isbn_12]
    sum = 0
    for i, str_num in zip(range(0, 12), list_isbn_12):
        number = int(str_num)
        prod = number * 1 if (i % 2 == 1) else number * 3
        sum += prod
    residual = sum % 10
    last_digit = 0 if residual == 0 else 10 - residual

    return str_isbn_12 + str(last_digit)


responses = list()

for _, genre in Book.GENRE_CHOICES:
    print("GENRE: ", genre)
    for word in genre.split(" "):
        params = {'query': '{"type":"\/type\/edition", "genres":' + "\"{}\"".format(word) + '}'}
        responses.append(requests.get('http://openlibrary.org/api/things', params=params))
    print("RESPONSES: ", responses)
    for response in responses:
        json = response.json()
        for book in json["result"]:
            time.sleep(0.5)
            print(book)
            params = {"key": book, "prettyprint": "true"}
            request = requests.get('http://openlibrary.org/api/get', params=params)
            json = request.json()["result"]
            print(json)
            try:
                isbn = json["isbn_13"] if "isbn_13" in json else isbn_10__to__isbn_13(json["isbn_10"])
                title = json["title"] or "Unknown Title"
                description = json["description"] if "description" in json else None
                saga = json['series'][0] if 'series' in json else None
                publication_date = json["publish_date"]

                authors = json['authors'][0] if 'authors' in json else None

                book = Book(ISBN=isbn, num_pages=json["number_of_pages"], title=title, desctiption = description,
                            saga = saga, publication_date = publication_date)

                print("BOOK: ", book)
            except:
                print("This book does not have ISBN")

    # Reset list for the next genre
    responses = list()
