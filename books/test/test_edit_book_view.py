import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
from django.urls import reverse

# Build up
from django.test import TestCase, Client, RequestFactory

from books import views
# from books.views import BookView
from books.models import Guest, Book, User, Address, Cart, Cupon
from books.views import BookView, SearchView, SellView, HomeView, EditBookView
from django.contrib.auth.models import Group, Permission


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
               fact_address=fact_address,
               genre_preference_1='BIOG',
               genre_preference_2='FOOD',
               genre_preference_3='KIDS')
    obj.save()

    cart = Cart(user_id=obj)
    cart.save()

    group = Group.objects.get(name='editor') # create?
    perm = Permission.objects.get(codename='add_book')
    group.permissions.add(perm)
    obj.groups.add(group)
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

def create_book(genre):
    """ Tests Book model, creation and the correct storage of the information"""

    isbn = str(random.randint(0, 5156123423456015412))[:12]
    user = create_user()
    title = 'THis is the TITLE'
    description = 'This is the description of a test book'
    saga = 'SAGA\'S NAME'
    author = "Author"
    price = 23.45
    language = 'Espanol'
    primary_genre = genre
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
    return obj


class EditBookViewTest(TestCase):
    def test_post_edit_book(self):
        isbn = str(random.randint(0, 5156123423456015412))[:12]
        user = create_user(random_user=True)

        dict_book = {
            'ISBN': isbn,
            'user': user,
            'title': 'THis is the TITLE',
            'description': 'This is the description of a test book',
            'saga': 'SAGA\'S NAME',
            'author': "Author",
            'price': 23.45,
            'language': 'Espanol',
            'primary_genre': 'FANT',
            'publisher': 'Alejandria',
            'num_pages': 100,
            'num_sold': 0,
            'recommended_age': 'Juvenile',
            'terms': True,
        }

        book = Book(ISBN=dict_book['ISBN'],
                    user_id=dict_book['user'],
                    title=dict_book['title'],
                    saga=dict_book['saga'],
                    description=dict_book['description'],
                    author=dict_book['author'],
                    price=dict_book['price'],
                    language=dict_book['language'],
                    publisher=dict_book['publisher'],
                    num_pages=dict_book['num_pages'],
                    num_sold=dict_book['num_sold'],
                    primary_genre=dict_book['primary_genre'],
                    recommended_age=dict_book['recommended_age'])
        book.save()

        new_dict_book = {
            'ISBN': isbn,
            'user': user,
            'title': 'new title',
            'description': 'new description',
            'saga': 'new saga',
            'author': "new author",
            'price': 123,
            'language': 'new language',
            'primary_genre': 'HORR',
            'publisher': 'new publisher',
            'num_pages': 321,
            'num_sold': 0,
            'recommended_age': 'new age',
            'terms': True,
        }

        request = RequestFactory().post('/editBook/' + isbn, new_dict_book)
        request.user = user
        EditBookView.as_view()(request, pk=isbn, testing=True)

        request_get = RequestFactory().get('/editBook/', kwargs={'pk': isbn})
        request_get.user = user
        response = EditBookView.as_view()(request_get, pk=isbn)
        modified_book = response.context_data.get('book')


        check = all([new_dict_book['ISBN'] == modified_book.ISBN,
                     new_dict_book['user'] == modified_book.user_id,
                     new_dict_book['title'] == modified_book.title,
                     new_dict_book['description'] == modified_book.description,
                     new_dict_book['saga'] == modified_book.saga,
                     new_dict_book['price'] == float(modified_book.price),
                     new_dict_book['language'] == modified_book.language,
                     new_dict_book['primary_genre'] == modified_book.primary_genre,
                     new_dict_book['publisher'] == modified_book.publisher,
                     new_dict_book['num_pages'] == modified_book.num_pages,
                     new_dict_book['num_sold'] == modified_book.num_sold,
                     new_dict_book['recommended_age'] == modified_book.recommended_age])

        assert check



    def test_delete_promo_book(self):
        isbn = str(random.randint(0, 5156123423456015412))[:12]
        user = create_user(random_user=True)

        dict_book = {
            'ISBN': isbn,
            'user': user,
            'title': 'THis is the TITLE',
            'description': 'This is the description of a test book',
            'saga': 'SAGA\'S NAME',
            'author': "Author",
            'price': 23.45,
            'language': 'Espanol',
            'primary_genre': 'FANT',
            'publisher': 'Alejandria',
            'num_pages': 100,
            'num_sold': 0,
            'recommended_age': 'Juvenile',
            'terms': True,
        }

        book = Book(ISBN=dict_book['ISBN'],
                    user_id=dict_book['user'],
                    title=dict_book['title'],
                    saga=dict_book['saga'],
                    description=dict_book['description'],
                    author=dict_book['author'],
                    price=dict_book['price'],
                    language=dict_book['language'],
                    publisher=dict_book['publisher'],
                    num_pages=dict_book['num_pages'],
                    num_sold=dict_book['num_sold'],
                    primary_genre=dict_book['primary_genre'],
                    recommended_age=dict_book['recommended_age'])
        book.save()

        cupon = Cupon(code = str(random.randint(0, 5156123423456015412))[:5], book = book, percentage = 10,
                      max_limit = 1000, redeemed = 1)
        cupon.save()

        cupon1 = Cupon(code=str(random.randint(0, 5156123423456015412))[:5], book=book, percentage=10,
                      max_limit=1000, redeemed=1)
        cupon1.save()

        request = RequestFactory().post('/editBook/' + isbn, data={'delete_promo':cupon.code})
        request.user = user
        EditBookView.as_view()(request, pk=isbn)

        request_get = RequestFactory().get('/editBook/', kwargs={'pk': isbn})
        request_get.user = user
        response = EditBookView.as_view()(request_get, pk=isbn)

        response_book = response.context_data.get('book')
        response_promos = response.context_data.get('promos')

        val = response_book.ISBN == book.ISBN
        val2 = False

        if cupon not in response_promos:
            val2 = True

        assert val and val2


