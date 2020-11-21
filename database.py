import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Alejandria.settings")
import django

django.setup()

from books.models import Book, User, Address, Product, Cart, FAQ
from django.core.files import File

import random

user_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
fact_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
user_address.save()
fact_address.save()
# Pylint: disable=line-too-long
thumb1 = File(open('Alejandria/static/images/cover-images/202852714dec217e579db202a977be70.jpg', 'rb'))
thumb2 = File(open('Alejandria/static/images/cover-images/book_cover.jpg', 'rb'))
thumb3 = File(open('Alejandria/static/images/cover-images/book_cover2.jpg', 'rb'))
thumb4 = File(open('Alejandria/static/images/cover-images/book_cover3.jpg', 'rb'))
thumb5 = File(open('Alejandria/static/images/cover-images/book_cover4.jpg', 'rb'))
thumb6 = File(open('Alejandria/static/images/cover-images/book_cover5.jpg', 'rb'))
thumb7 = File(open('Alejandria/static/images/cover-images/book_cover7.jpg', 'rb'))
thumb8 = File(open('Alejandria/static/images/cover-images/canva-white-bold-text-thriller-mystery-book-cover-CejxvxrTCyg.jpg', 'rb'))
thumb9 = File(open('Alejandria/static/images/cover-images/Night_pb-eb-des2.jpg', 'rb'))
thumb10 = File(open('Alejandria/static/images/cover-images/design-for-writers-book-cover-tf-2-a-million-to-one.jpg', 'rb'))



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

# Create Products
books = Book.objects.all()
products = []  # TODO: Product.objects.all() doesn't work.
for b in books:
    product = Product(ISBN=b, price=b.price)
    products.append(product)
    product.save()

print("PRODUCTS SAVED...OK")

# Create Cart
cart = Cart(user_id=user)  # TODO: if not postgresql complains about the cart is not created in database.
cart.save()
cart = Cart(id=1, user_id=user)

for p in products:
    cart.products.add(p)

cart.save()

print("CART SAVED...OK")


## TO GENEREATE FAQS, CAN BE CREATED FROM A FILE faqs.txt OR WRITTEN IN TERMINAL. ALSO DELETE ALL OR SEE WHAT IS IN THE DATABASE

def write_some_faqs():
    while True:
        n = input("Number of faqs you whant to write:")
        if n.isdigit():
            n = int(n)
            break
        else:
            print("Introduce number")

    questions = list()
    answers = list()
    categories = list()

    for i in range(n):
        loop = True
        category = "DEFAULT"
        while loop:
            category = input("CATEGORY (DWLDBOOK, DEVOL, SELL, FACTU, CONTACT):")
            loop = False
        question = input("Question:")
        answer = input("Answer")

        categories.append(category)
        questions.append(question)
        answers.append(answer)

    faqs_list = list(zip(categories, questions, answers))
    print("Faqs:", faqs_list)
    create_faqs(faqs_list)


def read_faqs_from_file():
    # Using readlines()
    print("READING FILE...")
    filename = 'faqs.txt'
    file1 = open(filename, 'r')
    lines = file1.readlines()

    questions = list()
    answers = list()
    categories = list()

    # Strips the newline character
    for line in lines:
        print(line)
        category, question, answer = line.strip().split('///')
        questions.append(question)
        answers.append(answer)
        categories.append(category)

    print("ALL FAQS READ...OK")
    faqs_list = list(zip(categories, questions, answers))
    create_faqs(faqs_list)


def create_faqs(faqs_to_create):
    print("SAVING FAQS...OK")
    for faq_element in faqs_to_create:
        print("### FAQ ---->", faq_element)
        to_save = FAQ(question=faq_element[1], answer=faq_element[2], category=faq_element[0])
        print(to_save)
        to_save.save()
    print("ALL FAQS SAVED...OK")


what = input("Chose option, insert manually, read in file information, see whats in database or delete all FAQ"
             " (I/RF/DB/DEL) :")
while True:
    if what == 'I':
        write_some_faqs()
        break
    elif what == 'RF':
        read_faqs_from_file()
        break
    elif what == 'DB':
        faqs = FAQ.objects.all()
        print(faqs)
        for faq in faqs:
            print(faq)
        break
    elif what == 'DEL':
        FAQ.objects.all().delete()
        print(FAQ.objects.all())
        break
