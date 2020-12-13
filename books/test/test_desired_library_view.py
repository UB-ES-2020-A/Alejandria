import random
from books.models import Guest, Book, User, Address, BookProperties
from django.test import TestCase, Client, RequestFactory

from books.views import BookView, EditorLibrary, DesiredLibrary


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


class DesiredLibraryViewTest(TestCase):
    def test_desired_library(self):

        previously_added_book = create_book()
        user = previously_added_book.user_id

        book_properties = BookProperties(book=previously_added_book,user=user,desired=True,readed=True)
        book_properties.save()

        request = RequestFactory().get('/desiredLibrary/')
        request.user = user
        response = DesiredLibrary.as_view()(request)

        desired_books = response.context_data.get('desired_books')
        print("desired", desired_books)


        find=False
        for book, price in desired_books:
            if(book.ISBN==previously_added_book.ISBN):
                find=True
        if find:
            assert True
        else:
            assert False



