import os
import traceback
import urllib

import django
import json
import requests
import time
import datetime
from django.core.files import File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Alejandria.settings")
django.setup()

from books.models import *
from random import randint

if not os.path.exists('./temp'):
    os.mkdir('./temp')


try:
    adress = Address(street="anonimous", city="Terraplana", country="Illuminados", zip=12345)
    adress.save()
    user = User(role="Admin", name="admin", password="admin", email="admin@mail.com", user_address=adress,
                fact_address=adress)
    user.save()
    
    book = Book(ISBN="123455556345", user_id=user, title="Harry", saga="Potter", description="first harry book",
                author="J.K.Rowling", price=30, language="Spanish", publisher="Alejandria", num_pages=200, num_sold=100,
                primary_genre="FANT", secondary_genre="OTHR", recommended_age="Juvenil")
    thumb10 = File(
        open('Alejandria/static/images/cover-images/design-for-writers-book-cover-tf-2-a-million-to-one.jpg', 'rb'))
    book.thumbnail.save('dummy_design.jpg', thumb10) # TODO TESTING
    book.save()
    print("Done")
    
except:
    user = User.objects.filter(name="admin").first()
    print("Except")


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
                # publication_date = json["publish_date"]
                # print('publication date: ', publication_date)
                publication_date = datetime.time
                publisher = json["publishers"][0] if "publishers" in json else None
                print('publisher: ', publisher)

                # Author request
                author_json = json['authors'][0] if 'authors' in json else None
                if author_json:
                    print(author_json)
                    author = requests.get('http://openlibrary.org' + author_json['key'] + '.json')
                    author = author.json()['name']
                else:
                    author = 'Unknown'

                from django.core.files.base import ContentFile

                urllib.request.urlretrieve('https://covers.openlibrary.org/b/isbn/' + isbn + '-M.jpg', './temp/'+isbn+'.jpg')
                myfile = ContentFile(open('./temp/'+isbn+'.jpg', 'rb').read())
                book = Book(ISBN=isbn, num_pages=json["number_of_pages"], title=title, description=description,
                            saga=saga, publication_date=publication_date, primary_genre=_, price=randint(5, 75),
                            publisher=publisher, user_id=user, author=author)
                path = str(isbn)+'.jpg'
                print(path)
                book.thumbnail.save('dummy_design.jpg', myfile)
                #book.thumbnail.save(path, file_image)
                print('BOOK: ', book)
                book.save()
            except:
                traceback.print_exc()

    # Reset list for the next genre
    responses = list()
