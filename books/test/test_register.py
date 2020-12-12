# Django and 3rd party libs
import json
import os
import random
import string

from django.core.wsgi import get_wsgi_application
from django.test.client import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()

# Then load own libs
from books.models import User, Guest
from books.views import register


def get_or_create_guest():
    device = '123456789'
    guest_query = Guest.objects.filter(device=device)
    if guest_query.count() == 0:
        guest = Guest(device=device)
        guest.save()
    else:
        guest = guest_query.first()
    return guest



def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


def test_register():
    email = random_char(7) + "@gmail.com"
    username = random_char(5)
    body = {
        "username": username, "firstname": "Josep",  "lastname": "Lopez",
        "email": email, "password1": "password123", "password2": "password123",
        "country1": "Spain", "city1": "Sant Adria del Besos", "street1": "c/Mare de deu del carme 116 4B",
        "zip1": "08930", "country2": "Spain", "city2": "Sant Adria del Besos",
        "street2": "c/Mare de deu del carme 116 4B", "zip2": "08930", "trigger": "register", "taste1": "Fiction",
        "taste2": "Crime & Thriller", "taste3": "Science Fiction", "tastes": True
    }

    guest = get_or_create_guest()
    req = RequestFactory().post("/register/", body)
    req.COOKIES['device'] = guest.device
    response = register(req)
    response_json = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 200 and response_json["error"] is False and User.objects.filter(email=email, username=username).exists()
