# Django and 3rd party libs
import pytest
import os
from django.core.wsgi import get_wsgi_application
from django.test import TestCase

# Build app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()


# Then load own libs
from books.models import Author, Book, Product, Rating, Bill, FAQ, Cart, Address, User


# TODO: Make test "en cadena". If we have to test something before try one test, do it.
# Decorator to enable DB at test function
def test_user():
    # Data to test
    id = 15
    role = 'Admin'
    name = 'Josep'
    password = 'password1'
    email = 'fakemail@gmail.com'
    user_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
    fact_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
    user_address.save()
    fact_address.save()

    # Model creation
    obj = User(id=id, role=role, name=name, password=password, email=email, user_address=user_address,
               fact_address=fact_address)
    obj.save()
    # Retrieve model to check correct creation
    obj = User.objects.all().last()
    check = all([id == obj.id, role == obj.role, name == obj.name, password == obj.password, email == obj.email,
                 user_address == obj.user_address, fact_address == obj.fact_address])
    # Test sucess if check is True
    assert check


def test_author():
    # Data to test
    first_name = 'Homero'
    last_name = 'Simpson'
    # Model creation
    obj = Author(first_name=first_name, last_name=last_name)
    obj.save()
    # Retrieve model to check correct creation
    obj = Author.objects.all().last()
    check = all([first_name == obj.first_name, last_name == obj.last_name])

# Decorator to enable DB at test function
def test_address():
    # Data to test
    street = 'C/ Test, 112'
    city = 'Barcelona'
    country = 'Spain'
    zip_code = '08942'
    # Model creation
    obj = Address(city=city, street=street, country=country, zip=zip_code)
    obj.save()
    # Retrieve model to check correct creation
    obj = Address.objects.all().last()
    check = all([street == obj.street, city == obj.city, country == obj.country, zip_code == obj.zip])

    # Test sucess if check is True
    assert check

#
# def test_book():
#     # Data to test
#     isbn = '0123456789012'  # 13 digits
#
#     user_id = User.objects.all().last()#User()
#     #user_id.save()
#     title = 'THis is the TITLE'
#     description = 'This is the description of a test book'
#     saga = 'SAGA\'S NAME'
#     author = Author.objects.all().last()
#     #authors = list(author)
#     #authors = list()
#     # publication_date = default
#     price = 23.45
#     language = 'Español'
#     genre = 'Fantasy'
#     publisher = 'Alejandria'
#     num_pages = 100
#     num_sold = 0
#     recommended_age = 'Juvenile'
#     thumbnail = '/thumbnails/1234567.png'
#
#     obj = Book(ISBN=isbn, user_id=user_id, title=title, description=description,
#                saga=saga, price=price, language=language, genre=genre,
#                publisher=publisher, num_pages=num_pages, num_sold=num_sold,
#                recommended_age=recommended_age, thumbnail=thumbnail)
#
#     obj.save()
#     obj.authors.add(author)
#
#     #obj.authors.set(authors)
#     obj.save()
#
#     obj = Book.objects.all().last()
#
#     assert isbn == obj.ISBN
#     assert user_id == obj.user_id
#     assert title == obj.title
#     assert description == obj.description
#     assert saga == obj.saga
#     print(obj.authors.get(id=author.id))
#     assert author.first_name == obj.authors.get(id=author.id).first_name
#     assert author.last_name == obj.authors.get(id=author.id).last_name
#     #i = 0 #TODDO Test it properly
#     #for author in authors:
#     #     assert author.first_name == obj.authors[i].first_name
#     #     assert author.last_name == obj.authors[i].last_name
#     #     i += 1
#     assert price == float(obj.price)
#     assert language == obj.language
#     assert genre == obj.genre
#     assert publisher == obj.publisher
#     assert num_pages == obj.num_pages
#     assert num_sold == obj.num_sold
#     assert recommended_age == obj.recommended_age
#     assert thumbnail == obj.thumbnail
#
#     # TODO: TEST EVERY POSSIBLE OUTCOME


def test_product():
    ISBN = Book.objects.all().last()  # 13 digits
    price = 22.40
    fees = 21.00
    discount = 5.00

    obj = Product(ISBN=ISBN, price=price, fees=fees, discount=discount)
    try:
        obj.save()
    except:
        pass

    obj = Product.objects.all().last()
    check = all([ISBN == obj.ISBN, price == float(obj.price), fees == float(obj.fees), discount == float(obj.discount)])

    assert check

def test_rating():
    product_id = Product.objects.all().last()
    user_id = User.objects.all().first()
    text = 'My opinion is that this product is great.'
    score = 3  # TODO: Also test if I use not viable scores
    # date = default

    obj = Rating(product_id=product_id, user_id=user_id, text=text, score=score)
    obj.save()

    obj = Rating.objects.all().last()

    check = all([#product_id == int(obj.product_id), #user_id == obj.user_id,TODO
                 text == str(obj.text), score == int(obj.score)])
    assert check



# def test_cart():
#     # TODO
#     ISBN1 = Book.objects.filter(ISBN='0123456789012').last()  # 13 digits
#     price1 = 22.40
#     fees1 = 21.00
#     discount1 = 5.00
#     prod_1 = Product(ISBN=ISBN1, price=price1, fees=fees1, discount=discount1)
#
#     try:
#         prod_1.save()
#     except:
#         pass
    """
    ISBN2 = Book.objects.filter(ISBN='0123456789012').last()  # 13 digits
    price2 = 23.40
    fees2 = 0.00
    discount2 = 0.00
    prod_2 = Product(ISBN=ISBN2, price=price2, fees=fees2, discount=discount2)
    prod_2.save()
    try:
        prod_2.save()
    except:
        pass
    """
#     product = Product.objects.all().last()
#     #print(products[0])
#     obj = Cart()
#     obj.save()
#     obj.products.add(product)
#     obj.save()
#     obj = Cart.objects.all().last()
#     assert obj.products.last().ISBN == product.ISBN
#     assert obj.products.last().price== product.price
#     assert obj.products.last().fees == product.fees
#     assert obj.products.last().discount == product.discount
#
#
#
# def test_bill():
#     # TODO
#     ISBN1 = Book.objects.filter(ISBN='0123456789012').last()  # 13 digits
#     price1 = 22.40
#     fees1 = 21.00
#     discount1 = 5.00
#     prod_1 = Product(ISBN=ISBN1, price=price1, fees=fees1, discount=discount1)
#
#     try:
#         prod_1.save()
#     except:
#         pass
#
#     # ISBN2 = Book.objects.filter(ISBN='0123456789012')  # 13 digits
#     # price2 = 23.40
#     # fees2 = 0.00
#     # discount2 = 0.00
#     # prod_2 = Product(ISBN=ISBN2, price=price2, fees=fees2, discount=discount2)
#     # prod_2.save()
#     #
#     # cart = Cart(products=Product.objects.all()[:3])
#     # cart.save()
#     # cart = Cart.objects.all().first()
#     try:
#         product = Product.objects.all().last()
#         obj = Cart()
#         obj.save()
#         obj.products.add(product)
#         obj.save()
#
#     finally:
#         cart = Cart.objects.all().first()
#
#     user_id = User.objects.all().last()
#     # date = default
#     seller_info = ' This is the information of the Seller'
#     payment_method = 'PayPal'
#
#     obj = Bill(user_id=user_id,
#                seller_info=seller_info, payment_method=payment_method)
#     obj.save()
#     obj.cart.add(cart)
#     obj.save()
#
#     obj = Bill.objects.all().last()
#
#     check = all([seller_info == obj.seller_info, payment_method == obj.payment_method])
#     assert check
#     #assert True TODO: COMPROVAR EL CART Y USER


def test_faq():
    question = 'How is this Sprint going?'
    answer = 'Perfectly'

    obj = FAQ(question=question, answer=answer)
    obj.save()

    obj = FAQ.objects.all().last()

    check = all([question == obj.question, answer == obj.answer])

