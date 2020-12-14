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
