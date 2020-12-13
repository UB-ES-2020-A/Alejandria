# Django and 3rd party libs
import pytest
import os
from django.core.wsgi import get_wsgi_application
from django.test.client import RequestFactory
import json
import string
import random

# Build app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()

# Then load own libs
from books.models import User, Guest
from books.views import view_profile, register


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
    body1 = {
        "username": username, "firstname": "Josep", "lastname": "Lopez",
        "email": email, "password1": "password123", "password2": "password123",
        "country1": "España", "city1": "Sant Adria del Besos", "street1": "c/Mare de deu del carme 116 4B",
        "zip1": "08930",
        "country2": "España", "city2": "Sant Adria del Besos", "street2": "c/Mare de deu del carme 116 4B",
        "zip2": "08930",
        "trigger": "register", "taste1": "Fiction", "taste2": "Crime & Thriller", "taste3": "Science Fiction",
        "tastes": True
    }

    guest = get_or_create_guest()
    req = RequestFactory().post("/register/", body1)
    req.COOKIES['device'] = guest.device
    response = register(req)

    email2 = random_char(7) + "@gmail.com"
    username2 = random_char(5)
    body2 = {
             "username": username2, "full_name": body1["firstname"]+" "+body1["lastname"], "email": email2,
             "street1": body1["street1"], "city1": body1["city1"], "country1": body1["country1"], "zip1": body1["zip1"],
             "street2": body1["street2"], "city2": body1["city2"], "country2": body1["country2"], "zip2": body1["zip2"],
             "taste1": body1["taste1"], "taste2": body1["taste2"], "taste3": body1["taste3"]
    }

    req = RequestFactory().post("/profile/", body2)
    req.user = User.objects.filter(username=username).first()
    response = view_profile(req)
    response_json = json.loads(response.content.decode("utf-8"))

    validation = not User.objects.filter(username=username).exists() and User.objects.filter(username=username2, email=email2).exists() and response.status_code == 200 and not response_json["error"]
    User.objects.filter(username=username2, email=email2).delete()

    assert validation