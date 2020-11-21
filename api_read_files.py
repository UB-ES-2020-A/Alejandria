"""
This file reads information fron OpenLibrary API, and saves in the database
all those books that fit on our book model definition.
"""
import os
import time
import traceback
from random import randint

import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Alejandria.settings")
django.setup()

from django.db.utils import IntegrityError

# pylint: disable=import-error
from books.models import Address, User, Book, GENRE_CHOICES

try:
    adress = Address(street="anonimous", city="Terraplana", country="Illuminados", zip=12345)
    adress.save()
    user = User(role="Admin", name="admin", password="admin", email="admin@mail.com",
                user_address=adress, fact_address=adress)
    user.save()
except IntegrityError:
    user = User.objects.filter(name="admin").first()


def _isbn10_to_isbn13(isbn_10):
    str_isbn_12 = "978" + str(isbn_10[0][:-1])
    list_isbn_12 = [int(digit) for digit in str_isbn_12]
    _sum = 0
    for i, str_num in zip(range(0, 12), list_isbn_12):
        number = int(str_num)
        prod = number * 1 if (i % 2 == 1) else number * 3
        _sum += prod
    residual = _sum % 10
    last_digit = 0 if residual == 0 else 10 - residual

    return str_isbn_12 + str(last_digit)


verbose = False
verboseprint = print if verbose else lambda *a, **k: None

responses = list()
i = 0
for _, genre in GENRE_CHOICES:
    verboseprint("GENRE: ", genre)
    for word in genre.split(" "):
        params = {'query': r'{"type":"\/type\/edition", "genres":' + "\"{}\"".format(word) + '}'}
        responses.append(requests.get('http://openlibrary.org/api/things', params=params))
    verboseprint("RESPONSES: ", responses)

    for response in responses:
        j = 0
        i += 1
        json = response.json()
        num_books = len(json["result"])
        for book in json["result"]:
            j += 1
            print("Genre {}    Book {}/{}".format(i, j, num_books))
            time.sleep(0.1)
            params = {"key": book, "prettyprint": "true"}
            request = requests.get('http://openlibrary.org/api/get', params=params)
            json = request.json()["result"]
            try:
                # ISBN
                isbn = json["isbn_13"][0] if "isbn_13" in json \
                    else _isbn10_to_isbn13(json["isbn_10"])
                verboseprint('ISBN: ', isbn)
                # In case isbn does not have the exact necessary length, the book is expeled
                if len(isbn) != 13:
                    continue
                # TITLE
                title = json["title"] or "Unknown Title"
                verboseprint('title: ', title)
                # DESCRIPTION
                description = json["description"] if "description" in json else None
                if not isinstance(description, str) and description is not None:
                    description = description["value"]
                verboseprint('dessc: ', description)
                # SAGA
                saga = json['series'][0] if 'series' in json else None
                verboseprint('saga: ', saga)
                # PUBLICATION DATE
                # publication_date = json["publish_date"]
                # TODO, modify incomming format to YYY-MM-DD or accept multiple formats
                # print('publication date: ', publication_date)
                # PUBLISHER
                publisher = json["publishers"][0] if "publishers" in json else None
                verboseprint('publisher: ', publisher)

                # #TODO authors = json['authors'][0] if 'authors' in json else None

                book = Book(ISBN=isbn,
                            num_pages=json["number_of_pages"],
                            title=title,
                            description=description,
                            saga=saga,
                            publication_date=None,
                            primary_genre=_,
                            price=randint(5, 75),
                            publisher=publisher[:50],
                            user_id=user)

                verboseprint('BOOK: ', book)
                book.save()

            except KeyError:
                print("One of the keys is not in this Book.")
                traceback.print_exc()

    # Reset list for the next genre
    responses = list()
