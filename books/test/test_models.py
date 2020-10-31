# Django and 3rd party libs
import pytest
import os
from django.core.wsgi import get_wsgi_application
from django.test import TestCase

# Build app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()

from books.models import Author, UserDummy, Book, Product, Rating, Bill, FAQ, Cart


# TODO: Make test "en cadena". If we have to test something before try one test, do it.

def test_author():
    # Data to test
    first_name = 'Homero'
    last_name = 'Simpson'
    # Model creation
    obj = Author(first_name=first_name, last_name=last_name)
    obj.save()
    # Retrieve model to check correct creation
    obj = Author.objects.all().first()
    check = all([first_name == obj.first_name, last_name == obj.last_name])
    # Test sucess if check is True
    assert check


def test_book():
    # Data to test
    isbn = '0123456789012'  # 13 digits
    user_id = UserDummy()
    user_id.save()
    title = 'THis is the TITLE'
    description = 'This is the description of a test book'
    saga = 'SAGA\'S NAME'
    authors = list(Author.objects.all()[:10])
    # publication_date = default
    price = 23.45
    language = 'Español'
    genre = 'Fantasy'
    publisher = 'Alejandria'
    num_pages = 100
    num_sold = 0
    recommended_age = 'Juvenile'
    thumbnail = '/thumbnails/1234567.png'

    obj = Book(ISBN=isbn, user_id=user_id, title=title, description=description,
               saga=saga, price=price, language=language, genre=genre,
               publisher=publisher, num_pages=num_pages, num_sold=num_sold,
               recommended_age=recommended_age, thumbnail=thumbnail)
    obj.authors.set(authors)
    obj.save()

    obj = Book.objects.all().first()

    assert isbn == obj.ISBN
    assert user_id == obj.user_id
    assert title == obj.title
    assert description == obj.description
    assert saga == obj.saga
    # i = 0 TODDO Test it properly
    # for author in authors:
    #     assert author.first_name == obj.authors[i].first_name
    #     assert author.last_name == obj.authors[i].last_name
    #     i += 1
    assert price == float(obj.price)
    assert language == obj.language
    assert genre == obj.genre
    assert publisher == obj.publisher
    assert num_pages == obj.num_pages
    assert num_sold == obj.num_sold
    assert recommended_age == obj.recommended_age
    assert thumbnail == obj.thumbnail

    # TODO: TEST EVERY POSSIBLE OUTCOME


def test_product():
    ISBN = Book.objects.all().first()  # 13 digits
    price = 22.40
    fees = 21.00
    discount = 5.00

    obj = Product(ISBN=ISBN, price=price, fees=fees, discount=discount)
    try:
        obj.save()
    except:
        pass

    obj = Product.objects.all().first()
    check = all([ISBN == obj.ISBN, price == float(obj.price), fees == float(obj.fees), discount == float(obj.discount)])

    assert check


def test_rating():
    product_id = Product.objects.all().first()
    user_id = UserDummy.objects.all().first()
    text = 'My opinion is that this product is great.'
    score = 3  # TODO: Also test if I use not viable scores
    # date = default

    obj = Rating(product_id=product_id, user_id=user_id, text=text, score=score)
    obj.save()

    obj = Rating.objects.all().first()

    check = all([#product_id == int(obj.product_id), #user_id == obj.user_id,TODO
                 text == str(obj.text), score == int(obj.score)])
    assert check


def test_cart():
    # TODO
    # ISBN1 = Book.objects.filter(ISBN='0123456789012')  # 13 digits
    # price1 = 22.40
    # fees1 = 21.00
    # discount1 = 5.00
    # prod_1 = Product(ISBN=ISBN1, price=price1, fees=fees1, discount=discount1)
    # prod_1.save()
    #
    # ISBN2 = Book.objects.filter(ISBN='0123456789012')  # 13 digits
    # price2 = 23.40
    # fees2 = 0.00
    # discount2 = 0.00
    # prod_2 = Product(ISBN=ISBN2, price=price2, fees=fees2, discount=discount2)
    # prod_2.save()
    #
    # products = Product.objects.all()[:3]
    #
    # obj = Cart(products=products)
    #
    # assert products == obj.products
    assert True


def test_bill():
    # TODO
    # ISBN1 = Book.objects.filter(ISBN='0123456789012')  # 13 digits
    # price1 = 22.40
    # fees1 = 21.00
    # discount1 = 5.00
    # prod_1 = Product(ISBN=ISBN1, price=price1, fees=fees1, discount=discount1)
    # prod_1.save()
    #
    # ISBN2 = Book.objects.filter(ISBN='0123456789012')  # 13 digits
    # price2 = 23.40
    # fees2 = 0.00
    # discount2 = 0.00
    # prod_2 = Product(ISBN=ISBN2, price=price2, fees=fees2, discount=discount2)
    # prod_2.save()
    #
    # cart = Cart(products=Product.objects.all()[:3])
    # cart.save()
    # cart = Cart.objects.all().first()
    #
    # user_id = UserDummy.objects.all().first()
    # # date = default
    # seller_info = ' This is the information of the Seller'
    # payment_method = 'PayPal'
    #
    # obj = Bill(cart=cart, user_id=user_id,
    #            seller_info=seller_info, payment_method=payment_method)
    # obj.save()
    #
    # obj = Bill.objects.all().first()
    #
    # check = all([cart == obj.cart, user_id == obj.user_id,
    #              seller_info == obj.seller_info, payment_method == obj.payment_method])
    # assert check

    assert True


def test_faq():
    question = 'How is this Sprint going?'
    answer = 'Perfectly'

    obj = FAQ(question=question, answer=answer)
    obj.save()

    obj = FAQ.objects.all().first()

    check = all([question == obj.question, answer == obj.answer])

    assert check
