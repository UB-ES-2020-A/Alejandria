import os
from random import random

from django.core.wsgi import get_wsgi_application
from django.test import RequestFactory

import json

# Build up
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()

from books.models import User, Address, Cart, Book, Product, Guest
from books.test.test_register import random_char
from books.views import delete_product, add_product



def get_or_create_user():
    user = User.objects.all().last() or None
    if user is None:
        user_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
        fact_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
        user = User(id=15, role='Admin', username=str(random.randint(0, 5156123423456015412)), name='Josep',
                    password='password1', email='fakemail@gmail.com', user_address=user_address,
                    genre_preference_1='CRIM', genre_preference_2='FANT', genre_preference_3='KIDS',
                    fact_address=fact_address)
        user.save()
    return user


def get_or_create_books(user, n):
    books = Book.objects.all() or None
    if books is None:
        books = []
        ISBNs = [str(i) for i in range(n)]
        titles = [random_char(5) for i in range(n)]
        for i in range(len(titles)):
            book = Book(ISBN=ISBNs[i], user_id=user, title=titles[i], descritpion='', author='', price=30,
                        language='Spanish', publisher='', num_pages=200, num_sold=100, primary_genre="FANT",
                        secondary_genre="OTHR", recommended_age="Juvenil")
            books.append(book)
            book.save()
    return books


def get_or_create_products(books):
    products = []
    for b in books:
        product = Product(ISBN=b, price=b.price)
        products.append(product)
        product.save()
    return products


def test_add_product():
    user = get_or_create_user()
    cart = Cart.objects.get(user_id=user)
    product = Product.objects.filter().last()

    body = {
        'user': user
    }
    print('PRODUCT', product)
    req = RequestFactory().post("/cart/", body)
    guest = Guest.objects.all().first()
    req.COOKIES['device'] = guest.device
    req.user = user
    add_product(req, 'cart', product.ID)
    assert cart.products.filter(ID=product.ID).last().ID == product.ID


def test_delete_product():
    user = get_or_create_user()
    cart = Cart.objects.get(user_id=user)
    product = cart.products.all()[0]

    body = {
        'user': user
    }

    req = RequestFactory().post("/cart/", body)
    guest = Guest.objects.all().first()
    req.COOKIES['device'] = guest.device
    req.user = user
    delete_product(req, product.ID)
    assert cart.products.filter(ID=product.ID).last() is None


def test_add_product_guest():
    guest = Guest.objects.all().first()
    cart = Cart.objects.get(guest_id=guest)
    product = Product.objects.filter().last()

    body = {}

    print('product', product.ISBN.ISBN)
    print('cart test', cart)
    req = RequestFactory().post("/cart/", body)
    req.COOKIES['device'] = guest.device
    req.user = User()
    add_product(req, 'cart', product.ISBN.ISBN)
    assert cart.products.filter(ID=product.ID).last().ISBN.ISBN == product.ISBN.ISBN


def test_delete_product_guest():
    guest = Guest.objects.all().first()
    cart = Cart.objects.get(guest_id=guest)
    product = cart.products.all()[0]

    body = {}

    req = RequestFactory().post("/cart/", body)
    req.COOKIES['device'] = guest.device
    req.user = User()
    delete_product(req, product.ID)
    assert cart.products.filter(ID=product.ID).last() is None
