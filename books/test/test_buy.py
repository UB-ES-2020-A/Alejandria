import random as rand
import os
import string
import unittest

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()
from django.test import RequestFactory
from books.models import User, Address, Cart, Book, Guest, BankAccount, Bill
import random
from books.views import delete_product, add_product, complete_purchase, generate_pdf, PaymentView



def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


def create_user(random_user=False):
    """ Test if creation of Users has any error, creating or storing the information"""
    # Data to test
    if random_user:
        _id = random.randint(0, 654891898)
    else:
        _id = 1
    role = 'Admin'
    name = 'Josep'
    if random_user:
        username = str(random.randint(0, 5156123423456015412))[:12]
    else:
        username = 'user'

    password = 'password1'
    email = 'fakemail@gmail.com'
    user_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
    fact_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
    user_address.save()
    fact_address.save()

    # Model creation
    obj = User(id=_id, role=role,
               username=username,
               name=name,
               password=password,
               email=email,
               user_address=user_address,
               fact_address=fact_address)
    obj.save()

    cart = Cart(user_id=obj)
    cart.save()

    return obj

def get_or_create_user():
    user_query = User.objects.filter(id=1000)
    if user_query.count() == 0:
        user_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
        fact_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
        user = User(id=1000, role='Admin', username='Test User Cart', name='Test',
                    password='password1', email='fakemail@gmail.com', user_address=user_address,
                    genre_preference_1='CRIM', genre_preference_2='FANT', genre_preference_3='KIDS',
                    fact_address=fact_address)
        user_address.save()
        fact_address.save()
        user.save()
    else:
        user = user_query.first()
    return user

  
def get_or_create_guest():
    device = '123456789'
    guest_query = Guest.objects.filter(device=device)
    if guest_query.count() == 0:
        guest = Guest(device=device)
        guest.save()
    else:
        guest = guest_query.first()
    return guest


def get_or_create_books(user, n):
    books_query = Book.objects.filter()
    books = []
    if books_query.count() < 3:
        ISBNs = [str(i) for i in range(n)]
        titles = [random_char(5) for i in range(n)]
        for i in range(len(titles)):
            book = Book(ISBN=ISBNs[i], user_id=user, title=titles[i], description='', author='', price=30,
                        language='Spanish', publisher='', num_pages=200, num_sold=100, primary_genre="FANT",
                        secondary_genre="OTHR", recommended_age="Juvenil")
            books.append(book)
            book.save()
    else:
        for b in books_query:
            books.append(b)
    return books


def get_or_create_guest_cart(guest):
    cart_query = Cart.objects.filter(guest_id=guest)
    if cart_query.count() == 0:
        cart = Cart(guest_id=guest)
        cart.save()
    else:
        cart = cart_query.first()
    return cart


def get_or_create_user_cart(user):
    cart_query = Cart.objects.filter(user_id=user)
    if cart_query.count() == 0:
        cart = Cart(user_id=user)
        cart.save()
    else:
        cart = cart_query.first()
    return cart


def test_add_product():
    user = get_or_create_user()
    cart = get_or_create_user_cart(user)
    books = get_or_create_books(user, 5)

    book = books[0]

    body = {
        'user': user
    }

    req = RequestFactory().post("/cart/", body)
    guest = get_or_create_guest()
    req.COOKIES['device'] = guest.device
    req.user = user
    add_product(req, 'cart', book.ISBN)
    assert cart.books.filter(ISBN=book.ISBN).last().ISBN == book.ISBN


def test_delete_product():
    user = get_or_create_user()
    cart = get_or_create_user_cart(user)
    books = get_or_create_books(user, 5)

    book = books[0]

    body = {
        'user': user
    }

    req = RequestFactory().post("/cart/", body)
    guest = get_or_create_guest()
    req.COOKIES['device'] = guest.device
    req.user = user
    delete_product(req, book)
    assert cart.books.filter(ISBN=book.ISBN).last() is None


def test_add_product_guest():
    guest = get_or_create_guest()
    cart = get_or_create_guest_cart(guest)
    user = get_or_create_user()
    books = get_or_create_books(user, 5)

    book = books[0]

    body = {}

    req = RequestFactory().post("/cart/", body)
    req.COOKIES['device'] = guest.device
    req.user = None
    add_product(req, 'cart', book.ISBN)
    assert cart.books.filter(ISBN=book.ISBN).last().ISBN == book.ISBN


def test_delete_product_guest():
    guest = get_or_create_guest()
    cart = get_or_create_guest_cart(guest)
    user = User()
    books = get_or_create_books(user, 5)

    book = books[0]

    body = {}

    req = RequestFactory().post("/cart/", body)
    req.COOKIES['device'] = guest.device
    req.user = None
    delete_product(req, book)
    assert cart.books.filter(ISBN=book.ISBN).last() is None


def push_some_products(user):
    cart = Cart.objects.get(user_id=user)
    books = Book.objects.all()
    cart.books.add(books[0])
    cart.books.add(books[1])
    cart.save()
    return books[0].price + books[1].price


def get_or_create_user_bank_account(user):
    bank_query = BankAccount.objects.filter(user=user)
    if bank_query.count() == 0:
        user_bank_account = BankAccount(user=user)
        user_bank_account.save()
    else:
        user_bank_account = bank_query.first()
    return user_bank_account


def test_complete_purchase():
    user = create_user(random_user=True)
    total_price = push_some_products(user)
    user_bank_account = get_or_create_user_bank_account(user)
    user_bank_account.save()

    body = {
        'user': user, 'username': 'User Name Test', 'month_exp': 11, 'year_exp': 2021, 'cardNumber': '1234567890123456',
        'cvv': 111, 'redeemed_codes': 0
    }

    req = RequestFactory().post("/payment/", body)
    req.test = True
    # La Request Factory no pilla el middleware, s'ha d'afegir manualment
    # (es necessita pel complete_purchase)
    middleware = SessionMiddleware()
    middleware.process_request(req)
    req.session.save()
    req.user = user
    cart = Cart.objects.get(user_id=user)
    complete_purchase(request=req, kwarg=True)
    bill = Bill.objects.filter(user_id=user).last()

    req2 = RequestFactory().post("/pdf/")
    req2.user = user
    generate_pdf(req2)
    user_bank_account = get_or_create_user_bank_account(user)
    assert cart.books.count() == 0 and user_bank_account.cvv == 111 and bill.total_money_spent == total_price


class SimpleTest(unittest.TestCase):
    def test_context(self):
        factory = RequestFactory()
        request = factory.get('/payment')
        request.user = create_user(random_user=True)
        response = PaymentView.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertEqual(response.context_data['total_items'], 0)
