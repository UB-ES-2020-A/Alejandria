# Django and 3rd party libs
import pytest
from django.core.wsgi import get_wsgi_application
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile

import json
import string
import random
import os


# Build app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()

# Then load own libs
from books.models import User, Guest
from books.views import login_user, register, post_avatar


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

def setup_request(request):
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
    return request

@override_settings(AUTHENTICATION_BACKENDS=
                       ('books.backend.EmailAuthBackend',))
def test_update_avatar_register():
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


    body2 = {
        'mail': email, 'password': 'password123', 'trigger': 'login'
    }

    req = RequestFactory().post("/login/", body2)
    req.user = User.objects.filter(username=username).first()
    req = setup_request(req)
    response = login_user(request=req)
    response_json = json.loads(response.content.decode("utf-8"))


    image = SimpleUploadedFile(name='test_image.jpg', content=open(r"C:\Users\Yusepp\PycharmProjects\Alejandria\media\thumbnails\dummy_book_cover2.jpg", 'rb').read(), content_type='image/jpeg')

    body3 = {
        'avatar': image, 'trigger': 'avatar'
    }

    req = RequestFactory().post("/avatar/", body3)
    req.user = User.objects.filter(username=username).first()
    req = setup_request(req)
    response = post_avatar(request=req)
    response_json = json.loads(response.content.decode("utf-8"))

    refresh_user = User.objects.filter(username=username).first()

    validation = not response_json['error'] and response.status_code == 200 and bool(refresh_user.avatar)
    User.objects.filter(username=username).delete()

    assert validation



@override_settings(AUTHENTICATION_BACKENDS=
                       ('books.backend.EmailAuthBackend',))
def test_update_avatar_edit():
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

    body2 = {
        'trigger': 'logout'
    }

    req = RequestFactory().post("/login/", body2)
    req.user = User.objects.filter(username=username).first()
    req = setup_request(req)
    response = login_user(request=req)
    response_json = json.loads(response.content.decode("utf-8"))

    image = SimpleUploadedFile(name='test_image.jpg', content=open(r"C:\Users\Yusepp\PycharmProjects\Alejandria\media\thumbnails\dummy_book_cover2.jpg", 'rb').read(), content_type='image/jpeg')

    body3 = {
        'avatar': image, 'trigger': 'avatar', 'username': username,
    }

    logout_user = req.user
    req = RequestFactory().post("/avatar/", body3)
    req.user = logout_user
    #req = setup_request(req)
    response = post_avatar(request=req)
    response_json = json.loads(response.content.decode("utf-8"))

    refresh_user = User.objects.filter(username=username).first()

    validation = not response_json['error'] and response.status_code == 200 and bool(refresh_user.avatar)
    User.objects.filter(username=username).delete()

    assert validation