import os
import traceback

import django
import json
import requests
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Alejandria.settings")
django.setup()

from books.models import *
from random import randint

try:
    adress = Address(street="anonimous", city="Terraplana", country="Illuminados", zip=12345)
    adress.save()
    user = User(role="Admin", name="admin", password="admin", email="admin@mail.com", user_address=adress,
                fact_address=adress)
    user.save()
except:
    user = User.objects.filter(name="admin").first()


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

for _, genre in GENRE_CHOICES:
    print("GENRE: ", genre)
    for word in genre.split(" "):
        params = {'query': '{"type":"\/type\/edition", "genres":' + "\"{}\"".format(word) + '}'}
        responses.append(requests.get('http://openlibrary.org/api/things', params=params))
    print("RESPONSES: ", responses)
    for response in responses:
        json = response.json()
        for book in json["result"]:
            time.sleep(0.5)
            params = {"key": book, "prettyprint": "true"}
            request = requests.get('http://openlibrary.org/api/get', params=params)
            json = request.json()["result"]
            try:
                isbn = json["isbn_13"][0] if "isbn_13" in json else isbn_10__to__isbn_13(json["isbn_10"])
                print('ISBN: ', isbn)
                title = json["title"] or "Unknown Title"
                print('title: ', title)
                description = json["description"]if "description" in json else None
                if type(description) != str and not description == None:
                    description = description["value"]
                print('dessc: ', description)
                saga = json['series'][0] if 'series' in json else None
                print('saga: ', saga)
                # publication_date = json["publish_date"] TODO, modify incomming format to YYY-MM-DD or accept multiple formats
                # print('publication date: ', publication_date)
                publisher = json["publishers"][0] if "publishers" in json else None
                print('publisher: ', publisher)

                # authors = json['authors'][0] if 'authors' in json else None #TODO

                book = Book(ISBN=isbn, num_pages=json["number_of_pages"], title=title, description=description,
                            saga=saga, publication_date=None, primary_genre=_, price=randint(5, 75),
                            publisher=publisher, user_id=user)
                print('BOOK: ', book)
                book.save()
            except:
                traceback.print_exc()

    # Reset list for the next genre
    responses = list()
