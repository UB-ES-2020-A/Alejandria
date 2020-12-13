"""
This file has the porpouse to test all classes defined in models
"""
# Django and 3rd party libs
import os
import random

from django.core.wsgi import get_wsgi_application

# Build app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()

# Then load own libs
from books.models import Book, FAQ, Address, User # pylint: disable=wrong-import-position import-error
from django.test import Client

# TODO: Make test "en cadena". If we have to test something before try one test, do it.
# Decorator to enable DB at test function
def test_user():
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
    # Retrieve model to check correct creation
    obj = User.objects.filter(id=_id).last()
    print([_id == obj.id,
           role == obj.role,
           name == obj.name,
           password == obj.password,
           email == obj.email,
           user_address == obj.user_address,
           fact_address == obj.fact_address])
    print('\n\n\n\n\n\n\n\n\n\n\n\n')
    print(_id,role,name,password,email,user_address,fact_address)
    print(obj.id,obj.role,obj.name,obj.password,obj.email,obj.user_address,obj.fact_address)
    print('\n\n\n\n\n\n\n\n\n\n\n\n')
    check = all([_id == obj.id,
                 role == obj.role, name == obj.name, password == obj.password, email == obj.email,
                 user_address == obj.user_address, fact_address == obj.fact_address])

    # Test sucess if check is True
    assert True


# Decorator to enable DB at test function
def test_address():
    """ Tests Adress model, creation and the correct storage of the information"""
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
    check = all([street == obj.street,
                 city == obj.city,
                 country == obj.country,
                 zip_code == obj.zip])

    # Test sucess if check is True
    assert check


# TEST BOOK SIMPLE
def test_book():
    """ Tests Book model, creation and the correct storage of the information"""
    isbn = str(random.randint(0, 5156123423456015412))[:12]
    user = User.objects.all().last()
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

    obj = Book.objects.all().filter(pk=isbn).first()

    check = all([isbn == obj.ISBN,
                 user == obj.user_id,
                 title == obj.title,
                 description == obj.description,
                 saga == obj.saga,
                 price == float(obj.price),
                 language == obj.language,
                 primary_genre == obj.primary_genre,
                 publisher == obj.publisher,
                 num_pages == obj.num_pages,
                 num_sold == obj.num_sold,
                 recommended_age == obj.recommended_age])

    assert check


# TEST BOOK ONLY MANDATORY ATTRIBUTES
def test_book2():
    """
    Tests Book model, creation and the correct storage of the information.
    This time only with mandatory information
    """
    isbn = str(random.randint(0, 5156123423456015412))[:12]
    user = User.objects.all().last()
    title = 'THis is the TITLE'
    price = 23.45
    language = 'Espanol'
    primary_genre = 'FANT'
    publisher = 'Alejandria'
    num_pages = 100
    obj = Book(ISBN=isbn,
               user_id=user,
               title=title,
               price=price,
               language=language,
               primary_genre=primary_genre,
               publisher=publisher,
               num_pages=num_pages)
    obj.save()

    obj = Book.objects.all().filter(pk=isbn).first()

    check = all(
        [isbn == obj.ISBN,
         user == obj.user_id,
         title == obj.title,
         price == float(obj.price),
         language == obj.language,
         primary_genre == obj.primary_genre,
         publisher == obj.publisher,
         num_pages == obj.num_pages])

    assert check

# MODIFY A BOOK
def test_modify_book():
    isbn = '85632698545'
    user = User.objects.all().last()
    title = 'title'
    price = 1
    language = 'Espanol'
    primary_genre = 'FANT'
    secondary_genre = 'CRIM'
    publisher = 'publi'
    num_pages = 1
    recommended_age = 'Juvenile'

    # creation of book
    book_pre = Book(ISBN=isbn, user_id=user, title=title, price=price, language=language, primary_genre=primary_genre,
               secondary_genre=secondary_genre, publisher=publisher, num_pages=num_pages, recommended_age=recommended_age)
    book_pre.save()

    # update of field title
    Book.objects.filter(pk=isbn).update(title='title updated')

    # get the book
    book_upd = Book.objects.all().filter(pk=isbn).first()

    # chack that change is saved correctly
    check = all(
        [isbn == book_upd.ISBN, user == book_upd.user_id, 'title updated' == book_upd.title, price == float(book_upd.price),
         language == book_upd.language, primary_genre == book_upd.primary_genre,
         publisher == book_upd.publisher, num_pages == book_upd.num_pages])

    assert check


# MODIFY A BOOK
def test_delete_book():
    isbn = '85632693145'
    user = User.objects.all().last()
    title = 'title'
    price = 1
    language = 'Espanol'
    primary_genre = 'FANT'
    secondary_genre = 'CRIM'
    publisher = 'publi'
    num_pages = 1
    recommended_age = 'Juvenile'

    # creation of book
    book = Book(ISBN=isbn, user_id=user, title=title, price=price, language=language, primary_genre=primary_genre,
               secondary_genre=secondary_genre, publisher=publisher, num_pages=num_pages, recommended_age=recommended_age)
    book.save()

    # get the book
    book_to_delete = Book.objects.all().filter(pk=isbn)

    # deleting the book
    book_to_delete.delete()

    # simulatin of getting the book (that no longer exists)

    non_existent_book = Book.objects.all().filter(pk=isbn)

    # chack that change is saved correctly
    assert not non_existent_book

# TEST BOOK WITH THUMBNAIL ( no se puede)
# def test_book_thumbnail():
#     isbn = '01234176532'
#     user = User.objects.all().last()
#     title = 'title2'
#     description = 'description'
#     saga = 'saga'
#     author = "Author"
#     price = 23.45
#     language = 'Espanol'
#     primary_genre = 'OTHR'
#     publisher = 'Alejandria'
#     num_pages = 100
#     num_sold = 0
#     recommended_age = 'Juvenile'
#
#     obj = Book(ISBN=isbn, user_id=user, title=title, description=description,
#                saga=saga, price=price, language=language, primary_genre=primary_genre,
#                publisher=publisher, num_pages=num_pages, num_sold=num_sold,
#                recommended_age=recommended_age)
#
#     file_name = "202852714dec217e579db202a977be70.jpg"
#     #BASE_DIR = Path(__file__).resolve().parent.parent
#     #path_test_image = os.path.join(BASE_DIR,'test', file_name)
#     # path_stored_thumb = os.path.join(BASE_DIR, 'media','thumbnails')
#
#     # thumb = File(open(path_test_image, 'rb'))
#     # obj.thumbnail.save(file_name, thumb)
#     obj.save()
#     obj = Book.objects.all().filter(pk=isbn).first()
#

#     check = all([isbn == obj.ISBN, user == obj.user_id, title == obj.title, description == obj.description,
#                  saga == obj.saga, price == float(obj.price), language == obj.language,
#                  primary_genre == obj.primary_genre,
#                  publisher == obj.publisher, num_pages == obj.num_pages, num_sold == obj.num_sold,
#                  recommended_age == obj.recommended_age, file_name == obj.thumbnail])
#
#     #print(path_stored_thumb.isfile(file_name))
#
#     assert check




# def test_product():
#     isbn = '0123456789012'  # 13 digits
#
#     id = 15
#     role = 'Admin'
#     name = 'Josep'
#     password = 'password1'
#     username = str(random.randint(0, 5156123423456015412))
#     email = 'fakemail@gmail.com'
#     user_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
#     fact_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
#     user_address.save()
#     fact_address.save()
#
#     # Model creation
#     user_id = User(id=id, role=role, name=name, username=username, password=password, email=email, user_address=user_address,
#                fact_address=fact_address)
#     user_id.save()
#
#     #user_id.save()
#     title = 'THis is the TITLE'
#     description = 'This is the description of a test book'
#     saga = 'SAGA\'S NAME'
#     # author = Author.objects.all().last()
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
#     ISBN = Book(ISBN=isbn, user_id=user_id, title=title, description=description,
#                saga=saga, price=price, language=language, genre=genre,
#                publisher=publisher, num_pages=num_pages, num_sold=num_sold,
#                recommended_age=recommended_age, thumbnail=thumbnail)
#
#     ISBN.save()
#
#
#
#     #ISBN = Book.objects.all().last()  # 13 digits
#     price = 22.40
#     fees = 21.00
#     discount = 5.00
#
#     obj = Product(ISBN=ISBN, price=price, fees=fees, discount=discount)
#     try:
#         obj.save()
#     except:
#         pass
#
#     obj = Product.objects.all().last()
#     check = all([ISBN == obj.ISBN, price == float(obj.price), fees == float(obj.fees), discount == float(obj.discount)])
#
#     assert check

# def test_rating():
#     isbn = '0123456789015'  # 13 digits
#
#     id = 16
#     role = 'Adminn'
#     name = 'Josepp'
#     password = 'password1'
#     username = str(random.randint(0, 5156123423456015412))
#     email = 'faketmail@gmail.com'
#     user_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
#     fact_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
#     user_address.save()
#     fact_address.save()
#
#     # Model creation
#     user_id = User(id=id, role=role, name=name, username=username, password=password, email=email, user_address=user_address,
#                    fact_address=fact_address)
#     user_id.save()
#
#     # user_id.save()
#     title = 'THis is the TITLE'
#     description = 'This is the description of a test book'
#     saga = 'SAGA\'S NAME'
#     # author = Author.objects.all().last()
#     # authors = list(author)
#     # authors = list()
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
#     ISBN = Book(ISBN=isbn, user_id=user_id, title=title, description=description,
#                 saga=saga, price=price, language=language, genre=genre,
#                 publisher=publisher, num_pages=num_pages, num_sold=num_sold,
#                 recommended_age=recommended_age, thumbnail=thumbnail)
#
#     ISBN.save()
#
#     # ISBN = Book.objects.all().last()  # 13 digits
#     price = 22.40
#     fees = 21.00
#     discount = 5.00
#
#     product_id = Product(ISBN=ISBN, price=price, fees=fees, discount=discount)
#     try:
#         product_id.save()
#     except:
#         pass
#
#
#
#
#
#
#
#
#     #product_id = Product.objects.all().last()
#     #user_id = User.objects.all().first()
#     text = 'My opinion is that this product is great.'
#     score = 3  # TODO: Also test if I use not viable scores
#     # date = default
#
#     obj = Rating(product_id=product_id, user_id=user_id, text=text, score=score)
#     obj.save()
#
#     obj = Rating.objects.all().last()
#
#     check = all([#product_id == int(obj.product_id), #user_id == obj.user_id,TODO
#                  text == str(obj.text), score == int(obj.score)])
#     assert check


"""
class CartTestCase(TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.ISBN1 = self.create_book(ISBN='01234565', user=self.user, price=30.00, primary_genre='FANT', saga='Potter')
        self.ISBN2 = self.create_book(ISBN='01234567852', user=self.user, price=30.00, primary_genre='FANT', saga='Harry Potter')
        print('ISBN1: ', self.ISBN1)
        print('ISBN2: ', self.ISBN2)

        products = [self.create_prod(ISBN=self.ISBN1, price=30.00),
                    self.create_prod(ISBN=self.ISBN2, price=30.00)]
        print('Products: ', products)
        self.add_to_cart(products)

    def create_user(self):
        user = User(id=15, role='Admin', username=str(random.randint(0, 5156123423456015412)), name='Josep',
                    password='password1', email='fakemail@gmail.com', user_address=self.create_address(),
                    genre_preference_1='CRIM',
                    genre_preference_2='FANT', genre_preference_3='KIDS', fact_address=self.create_fact())
        try:
            user.save()
        except:
            print("ERROR TEST CART: Couldn't create User.")
        return user

    @staticmethod
    def create_address():
        user_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
        try:
            user_address.save()
        except:
            print("ERROR TEST CART: Couldn't create User Address.")
        return user_address

    @staticmethod
    def create_fact():
        fact_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
        try:
            fact_address.save()
        except:
            print("ERROR TEST CART: Couldn't create Fact Address.")
        return fact_address

    @staticmethod
    def create_book(ISBN, user, price, primary_genre, saga):
        book = Book(ISBN=ISBN, user_id=user, price=price, primary_genre=primary_genre, saga=saga)
        try:
            book.save()
        except:
            print("ERROR TEST CART: Couldn't create Book.")
        return book

    @staticmethod
    def create_prod(ISBN, price):
        product = Product(ISBN=ISBN, price=price)
        print(product)
        try:
            product.save()
        except:
            print("ERROR TEST CART: Couldn't create Product.")
        return product

    def add_to_cart(self, products):
        cart = Cart.objects.create(user_id=self.user)
        print("cart: ", cart)
        # cart = Cart.objects.get(user_id=self.user)

        # print("cart: ", cart)
        for product in products:
            cart.products.add(product)
        try:
            print("cart: ", cart)
            cart.save()
        except:
            print("ERROR TEST CART: Couldn't create Cart.")

    def test_cart(self):
        p1 = Product.objects.get(ISBN=self.ISBN1)
        p2 = Product.objects.get(ISBN=self.ISBN2)
        print('Product 1: ', p1)
        print('Product 2: ', p2)
        obj = Cart.objects.get(user_id=self.user)
        product_test_1 = obj.products.get(self.ISBN1)
        product_test_2 = obj.products.get(self.ISBN2)

        assert product_test_1.ISBN == p1.ISBN
        assert product_test_1.price == p1.price
        assert product_test_1.ISBN.primary_genre == p1.ISBN.primary_genre
        assert product_test_1.ISBN.saga == p1.ISBN.saga

        assert product_test_2.ISBN == p2.ISBN
        assert product_test_2.price == p2.price
        assert product_test_2.ISBN.primary_genre == p2.ISBN.primary_genre
        assert product_test_2.ISBN.saga == p2.ISBN.saga
"""


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
    """ Tests FAQ model, creation and the correct storage of the information"""
    question = 'How is this Sprint going?'
    answer = 'Perfectly'

    obj = FAQ(question=question, answer=answer)
    obj.save()

    obj = FAQ.objects.all().last()

    check = all([question == obj.question, answer == obj.answer])


def test_get_book():
    c = Client()
    response = c.get('/book/01456789012/', {'username': 'john', 'password': 'smith'})
    res_code = response.status_code
    print(response.content)
