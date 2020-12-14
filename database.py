"""
This file was used to add initial lines in the DataBase,
but might be changed for a future mor professional implementation.
"""
import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Alejandria.settings")
django.setup()

from books.models import Book, User, Address, Cart, FAQ  #  deepcode ignore C0413: <irrelevant error>

from django.core.files import File
from django.db import IntegrityError

user_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
fact_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
user_address.save()
fact_address.save()
# pylint: disable=line-too-long
thumb1 = File(open('Alejandria/static/images/cover-images/202852714dec217e579db202a977be70.jpg', 'rb'))
thumb2 = File(open('Alejandria/static/images/cover-images/book_cover.jpg', 'rb'))
thumb3 = File(open('Alejandria/static/images/cover-images/book_cover2.jpg', 'rb'))
thumb4 = File(open('Alejandria/static/images/cover-images/book_cover3.jpg', 'rb'))
thumb5 = File(open('Alejandria/static/images/cover-images/book_cover4.jpg', 'rb'))
thumb6 = File(open('Alejandria/static/images/cover-images/book_cover5.jpg', 'rb'))
thumb7 = File(open('Alejandria/static/images/cover-images/book_cover7.jpg', 'rb'))
thumb8 = File(
    open('Alejandria/static/images/cover-images/canva-white-bold-text-thriller-mystery-book-cover-CejxvxrTCyg.jpg',
         'rb'))
thumb9 = File(open('Alejandria/static/images/cover-images/Night_pb-eb-des2.jpg', 'rb'))
thumb10 = File(
    open('Alejandria/static/images/cover-images/design-for-writers-book-cover-tf-2-a-million-to-one.jpg', 'rb'))

print("ADDRESS SAVED...OK")

# Model creation
user = User(id=15, role='Admin', username=str(random.randint(0, 5156123423456015412)), name='Josep',
            password='password1', email='fakemail@gmail.com', user_address=user_address, genre_preference_1='CRIM',
            genre_preference_2='FANT', genre_preference_3='KIDS', fact_address=fact_address)
user.save()

print("USER SAVED...OK")

book = Book(ISBN="01234565", user_id=user, title="Harry", saga="Potter", description="first harry book",
            author="J.K.Rowling", price=30, language="Spanish", publisher="Alejandria", num_pages=200, num_sold=100,
            primary_genre="FANT", secondary_genre="OTHR", recommended_age="Juvenil")

book.thumbnail.save('dummy_design.jpg', thumb10)
book.save()

book1 = Book(ISBN="012389012", user_id=user, title="Potter", saga="saga", description="first harry book", author="J.ng",
             price=30, language="Spanish", publisher="Alejandria", num_pages=200, num_sold=100, primary_genre="CRIM",
             secondary_genre="OTHR", recommended_age="Juvenil")
book1.thumbnail.save('dummy_book_cover2.jpg', thumb3)
book1.save()

book2 = Book(ISBN="01234567892", user_id=user, title="Sherlock", saga="Harry Potter", description="first harry book",
             author="J.aaa", price=30, language="Spanish", publisher="Alejandria", num_pages=200, num_sold=100,
             primary_genre="HORR", secondary_genre="OTHR", recommended_age="Juvenil")
book2.thumbnail.save('dummy_Night_pb-eb-des2.jpg', thumb9)
book2.save()

book3 = Book(ISBN="01456789012", user_id=user, title="Holmes", saga="Harry Potter", description="first harry book",
             author="JUse", price=30, language="Spanish", publisher="Alejandria", num_pages=200, num_sold=100,
             primary_genre="ROMA", secondary_genre="OTHR", recommended_age="Juvenil")
book3.thumbnail.save('dummy_book_cover4.jpg', thumb5)
book3.save()

book4 = Book(ISBN="01234567852", user_id=user, title="Muerte en el Nilo", saga="Harry Potter",
             description="first harry book", author="Josama", price=30, language="Spanish", publisher="Alejandria",
             num_pages=200, num_sold=100, primary_genre="FANT", recommended_age="Juvenil")
book4.thumbnail.save('dummy_book_cover5.jpg', thumb6)
book4.save()

book5 = Book(ISBN="012349012", user_id=user, title="Hola", saga="Harry Potter", description="first harry book",
             author="Jacinto", price=30, language="Spanish", publisher="Alejandria", num_pages=200, num_sold=100,
             primary_genre="CRIM", secondary_genre="OTHR", recommended_age="Juvenil")
book5.thumbnail.save('dummy_book_cover7.jpg', thumb7)
book5.save()

book6 = Book(ISBN="012345812", user_id=user, title="Holita", saga="Harry Potter", description="first harry book",
             author="Julieta", price=30, language="Spanish", publisher="Alejandria", num_pages=200, num_sold=100,
             primary_genre="CRIM", recommended_age="Juvenil")
book6.save()

print("BOOKS SAVED...OK")
try:

    # Create Cart
    cart, created = Cart.objects.get_or_create(id=1, user_id=user)
    books = Book.objects.all()
    cart.books.add(books[0])
    cart.save()
    print("CART SAVED...OK")

except IntegrityError:
    print("Error in cart")

