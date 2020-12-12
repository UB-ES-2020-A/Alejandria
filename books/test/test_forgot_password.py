# Django and 3rd party libs
import json
import os
import random
import string

from django.core.wsgi import get_wsgi_application
from django.test.client import RequestFactory
from django.http import HttpResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()

# Then load own libs
from books.models import User, Guest
from books.views import register, forgot


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

    user = User.objects.filter(username=username).first()

    body2 = {
            "trigger": "forgot", "mail": email
    }

    req = RequestFactory().post("/forgot/", body2)
    response = forgot(req)
    response_json = json.loads(response.content.decode("utf-8"))
    validation1 = not response_json["error"] and response.status_code == 200
    reset_id = response_json["id"]

    req = RequestFactory().get("/forgot/", data={"id": reset_id})
    response = forgot(req)
    validation2 = type(response) == HttpResponse

    new_password = 'newpass'
    body3 = {
        "trigger": "reset", "id": reset_id, 'new_pass': new_password
    }

    req = RequestFactory().post("/forgot/", body3)
    response = forgot(req)
    response_json = json.loads(response.content.decode("utf-8"))
    validation3 = not response_json["error"] and response.status_code == 200 and User.objects.filter(username=username).first().password == new_password

    User.objects.filter(username=username).delete()

    req = RequestFactory().post("/forgot/",body2)
    response = forgot(req)
    response_json = json.loads(response.content.decode("utf-8"))
    validation4 = response_json["error"] and response.status_code == 200


    assert validation1 and validation2 and validation3 and validation4

