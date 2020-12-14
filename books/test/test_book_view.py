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
from books.views import BookView, SearchView, SellView




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

    isbn = str(random.randint(0, 5156123423456015412))[:12]
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
    return obj




class BookViewTest(TestCase):
    def test_get_book(self):



        previously_added_book = create_book()

        # request = client.get(reverse('books:book', kwargs={'pk': previously_added_book.ISBN}))
        request = RequestFactory().get('/book/', kwargs={'pk': previously_added_book.ISBN})
        request.user = create_user(random_user=True)
        response = BookView.as_view()(request, pk=previously_added_book.ISBN)

        # request.render()
        # request.COOKIES['device'] = guest.device
        print(type(response))
        print(response.context_data)

        book_obteined = response.context_data.get('book')

        return self.assertEqual(book_obteined, previously_added_book)

    def test_post_book(self):

        user = create_user(random_user=True)
        previously_added_book = create_book()

        book_properties = {
            "readed": ['on'],
        }

        request = RequestFactory().post('/book/' + previously_added_book.ISBN, book_properties)
        request.user = user
        BookView.as_view()(request, kwargs=previously_added_book.ISBN)

        request_get = RequestFactory().get('/book/', kwargs={'pk': previously_added_book.ISBN})
        request_get.user = user
        response = BookView.as_view()(request_get, pk=previously_added_book.ISBN)


        form = response.context_data.get('form')
        desired = form.desired
        readed = form.readed

        assert not desired and readed



