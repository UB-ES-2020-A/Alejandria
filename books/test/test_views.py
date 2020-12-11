import os
from random import random

from django.core.wsgi import get_wsgi_application
from django.urls import reverse

# Build up
from django.test import TestCase, Client, RequestFactory

from books import views
# from books.views import BookView
from books.models import Guest, Book, User, Address
from books.views import BookView, SearchView

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()

def create_user():
    """ Test if creation of Users has any error, creating or storing the information"""
    # Data to test
    _id = 30
    role = 'Admin'
    name = 'Josep'
    username = 'Test User'
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

    return obj



def get_or_create_guest():
    device = '123456789'
    guest_query = Guest.objects.filter(device=device)
    if guest_query.count() == 0:
        guest = Guest(device=device)
        guest.save()
    else:
        guest = guest_query.first()
    return guest



def create_book():
    """ Tests Book model, creation and the correct storage of the information"""
    isbn = '121651'#str(random.randint(0, 5156123423456015412))[:12]
    user = create_user()
    title = 'THis is the TITLE'
    description = 'This is the description of a test book'
    saga = 'SAGA\'S NAME'
    author = "Author"
    price = 23.45
    language = 'Espanol'
    primary_genre = 'FANT'
    publisher = 'Alejandria'
    num_pages = 100
    num_sold = 0
    recommended_age = 'Juvenile'

    obj = Book(ISBN=isbn,
               user_id=user,
               title=title,
               description=description,
               saga=saga,
               price=price,
               language=language,
               primary_genre=primary_genre,
               publisher=publisher,
               num_pages=num_pages,
               num_sold=num_sold,
               recommended_age=recommended_age)
    obj.save()
    return obj.ISBN


# class FaqsViewTest(TestCase):
#     def test_environment_set_in_context(self):
#         #request = RequestFactory().get('/book/01456789012/')
#         #request = RequestFactory().get('book/01456789012',)
#         client = Client()
#         request = client.get(reverse('books:faqs'))
#
#         print(request.context)
#         print(request.content)




# class BookViewTest(TestCase):
#     def test_environment_set_in_context(self):
#         #request = RequestFactory().get('/book/01456789012/')
#         #request = RequestFactory().get('book/01456789012',)
#         guest = get_or_create_guest()
#         isbn = create_book()
#         # req = RequestFactory().post("/register/")
#         # req.COOKIES['device'] = guest.device
#
#
#
#         client = Client()
#         request = client.get(reverse('books:book', kwargs={'pk': isbn}))

        # request.COOKIES['device'] = guest.device

        # book = request.context.get('book')

        # view = BookView()
        # view.setup(request)

        # context = view.get_context_data()
        # self.assertIn('environment', context)

# class SearchViewTest(TestCase):
#     def test_environment_set_in_context(self):
#         #request = RequestFactory().get('/book/01456789012/')
#         #request = RequestFactory().get('book/01456789012',)
#
#         guest = get_or_create_guest()
#
#         req = RequestFactory().post("/register/", body)
#         req.COOKIES['device'] = guest.device
#
#
#
#
#         client = Client()
#         request = client.get(reverse('books:search'))
#
#         print(request)
        # view = SearchView()
        # view.setup(request)


        #
        # context = view.get_context_data()
        # self.assertIn('environment', context)





"""
import random as rand
from django.test import RequestFactory
from books.models import User, Address, Cart, Book, Product, Guest, BankAccount, Bill
from books.test.test_register import random_char
from books.views import delete_product, add_product, complete_purchase


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


def generate_id():
    temp = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    list_id = [str(rand.randint(0, 16)) if character == 'x' else character for character in temp]
    id = "".join(list_id)
    return id


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


def get_or_create_products(books):
    products_query = Product.objects.filter()
    products = []
    if products_query.count() < 3:
        for b in books:
            product = Product(ISBN=b, price=b.price)
            products.append(product)
            product.save()
    else:
        for p in products_query:
            products.append(p)
    return products


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
    products = get_or_create_products(books)

    product = products[0]

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
    cart = get_or_create_user_cart(user)
    books = get_or_create_books(user, 5)
    products = get_or_create_products(books)

    product = products[0]

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
    user = get_or_create_user()
    books = get_or_create_books(user, 5)
    products = get_or_create_products(books)

    product = products[0]

    body = {}

    req = RequestFactory().post("/cart/", body)
    req.COOKIES['device'] = guest.device
    req.user = None
    add_product(req, 'cart', product.ISBN.ISBN)
    assert cart.products.filter(ID=product.ID).last().ISBN.ISBN == product.ISBN.ISBN


def test_delete_product_guest():
    guest = get_or_create_guest()
    cart = get_or_create_guest_cart(guest)
    user = User()
    books = get_or_create_books(user, 5)
    products = get_or_create_products(books)

    product = products[0]

    body = {}

    req = RequestFactory().post("/cart/", body)
    req.COOKIES['device'] = guest.device
    req.user = None
    delete_product(req, product.ID)
    assert cart.products.filter(ID=product.ID).last() is None


def push_some_products(user):
    cart = Cart.objects.get(user_id=user)
    products = Product.objects.all()
    cart.products.add(products[0])
    cart.products.add(products[1])
    cart.save()
    return products[0].price + products[1].price


def get_or_create_user_bank_account(user):
    bank_query = BankAccount.objects.filter(user=user)
    if bank_query.count() == 0:
        user_bank_account = BankAccount(user=user)
        user_bank_account.save()
    else:
        user_bank_account = bank_query.first()
    return user_bank_account


def test_complete_purchase():
    user = get_or_create_user()
    total_price = push_some_products(user)
    user_bank_account = get_or_create_user_bank_account(user)
    user_bank_account.save()

    body = {
        'user': user, 'username': 'User Name Test', 'month_exp': 11, 'year_exp': 2021, 'cardNumber': '1234567890123456',
        'cvv': 111
    }

    req = RequestFactory().post("/payment/", body)
    req.user = user
    cart = Cart.objects.get(user_id=user.id)
    complete_purchase(request=req)
    bill = Bill.objects.filter(user_id=user).last()
    user_bank_account = get_or_create_user_bank_account(user)
    assert cart.products.count() == 0 and user_bank_account.cvv == 111 and bill.total_money_spent == total_price

"""
