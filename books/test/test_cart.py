import os
import random as rand

from django.core.wsgi import get_wsgi_application
from django.test import RequestFactory

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
        user = User(id=15, role='Admin', username=str(rand.randint(0, 5156123423456015412)), name='Josep',
                    password='password1', email='fakemail@gmail.com', user_address=user_address,
                    genre_preference_1='CRIM', genre_preference_2='FANT', genre_preference_3='KIDS',
                    fact_address=fact_address)
        user.save()
    return user


def generate_id():
    temp = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    list_id = [str(rand.randint(0, 16)) if character == 'x' else character for character in temp]
    id = "".join(list_id)
    print('ID', id)
    return id


def get_or_create_guest():
    guest = Guest.objects.all().first() or None
    if guest is None:
        guest = Guest(device=generate_id())
        guest.save()
    return guest


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


def get_or_create_guest_cart(guest):
    cart = Cart.objects.filter(guest_id=guest).first() or None
    if cart is None:
        cart = Cart(guest_id=guest)
        cart.save()
    return cart


def test_add_product():
    user = get_or_create_user()
    cart = Cart.objects.get(user_id=user)
    product = Product.objects.filter().last()

    body = {
        'user': user
    }

    req = RequestFactory().post("/cart/", body)
    guest = get_or_create_guest()
    req.COOKIES['device'] = guest.device
    req.user = user
    add_product(req, 'cart', product.ISBN.ISBN)
    assert cart.products.filter(ID=product.ID).last().ID == product.ID


def test_delete_product():
    user = get_or_create_user()
    cart = Cart.objects.get(user_id=user)
    product = cart.products.all()[0]

    body = {
        'user': user
    }

    req = RequestFactory().post("/cart/", body)
    guest = get_or_create_guest()
    req.COOKIES['device'] = guest.device
    req.user = user
    delete_product(req, product.ID)
    assert cart.products.filter(ID=product.ID).last() is None


def test_add_product_guest():
    guest = get_or_create_guest()
    cart = get_or_create_guest_cart(guest)
    product = Product.objects.filter().last()

    body = {}

    req = RequestFactory().post("/cart/", body)
    req.COOKIES['device'] = guest.device
    req.user = User()
    add_product(req, 'cart', product.ISBN.ISBN)
    assert cart.products.filter(ID=product.ID).last().ISBN.ISBN == product.ISBN.ISBN


def test_delete_product_guest():
    guest = get_or_create_guest()
    cart = get_or_create_guest_cart(guest)
    product = cart.products.all()[0]

    body = {}

    req = RequestFactory().post("/cart/", body)
    req.COOKIES['device'] = guest.device
    req.user = User()
    delete_product(req, product.ID)
    assert cart.products.filter(ID=product.ID).last() is None
