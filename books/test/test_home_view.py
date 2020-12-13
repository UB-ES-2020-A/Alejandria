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
from books.models import Guest, Book, User, Address, Cart
from books.views import BookView, SearchView, SellView, HomeView


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


class HomeViewTest(TestCase):
    def test_get_home(self):

        # context['fantasy'] = Book.objects.filter(primary_genre__contains="FANT")[:20]
        # context['crime'] = Book.objects.filter(primary_genre__contains="CRIM")[:20]
        # context['anime'] = Book.objects.filter(primary_genre__contains="ANIM")[:20]
        # context['fiction'] = Book.objects.filter(primary_genre__contains="FICT")[:20]
        # context['romance'] = Book.objects.filter(primary_genre__contains="ROMA")[:20]
        # context['horror'] = Book.objects.filter(primary_genre__contains="HORR")[:20]

        fant_book = create_book('FANT')
        crim_book = create_book('CRIM')
        anim_book = create_book('ANIM')
        fict_book = create_book('FICT')
        roma_book = create_book('ROMA')
        horr_book = create_book('HORR')

        biog_book = create_book('BIOG')
        humo_book = create_book('HUMO')
        kids_book = create_book('KIDS')


        user = create_user(random_user=True)

        request_get = RequestFactory().get('/')
        request_get.user = user

        response = HomeView.as_view()(request_get)
        fant_books = response.context_data.get('fantasy')
        crim_books = response.context_data.get('crime')
        anim_books = response.context_data.get('anime')
        fict_books = response.context_data.get('fiction')
        roma_books = response.context_data.get('romance')
        horr_books = response.context_data.get('horror')


        added_in_fant = False
        added_in_crim = False
        added_in_anim = False
        added_in_fict = False
        added_in_roma = False
        added_in_horr = False

        error_in_fant_books = False
        error_in_crim_books = False
        error_in_anim_books = False
        error_in_fict_books = False
        error_in_roma_books = False
        error_in_horr_books = False

        for book in fant_books:
            if book.primary_genre != "FANT" and book.secondary_genre != "FANT":
                print(book.primary_genre, book.secondary_genre)
                error_in_fant_books = True

        for book in crim_books:
            if book.primary_genre != "CRIM" and book.secondary_genre != "CRIM":
                error_in_crim_books = True

        for book in anim_books:
            if book.primary_genre != "ANIM" and book.secondary_genre != "ANIM":
                error_in_anim_books = True

        for book in fict_books:
            if book.primary_genre != "FICT" and book.secondary_genre != "FICT":
                error_in_fict_books = True

        for book in roma_books:
            if book.primary_genre != "ROMA" and book.secondary_genre != "ROMA":
                error_in_roma_books = True

        for book in horr_books:
            if book.primary_genre != "HORR" and book.secondary_genre != "HORR":
                error_in_horr_books = True

        if fant_book in fant_books:
            added_in_fant = True
        if crim_book in crim_books:
            added_in_crim = True
        if anim_book in anim_books:
            added_in_anim = True
        if fict_book in fict_books:
            added_in_fict = True
        if roma_book in roma_books:
            added_in_roma = True
        if horr_book in horr_books:
            added_in_horr = True

        books_added_in_context = added_in_fant and added_in_crim and added_in_anim and added_in_fict and added_in_roma and added_in_horr
        errors_in_genres = error_in_fant_books or error_in_crim_books or error_in_anim_books or error_in_fict_books or error_in_roma_books or error_in_horr_books

        assert books_added_in_context and not errors_in_genres
