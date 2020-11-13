import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Alejandria.settings")
import django
django.setup()


from books.models import Book, User, Address
import random

user_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
fact_address = Address(city='Barcelona', street='C/ Test, 112', country='Spain', zip='08942')
user_address.save()
fact_address.save()

# Model creation
user = User(id=15, role='Admin',username=str(random.randint(0, 5156123423456015412)), name='Josep', password='password1', email='fakemail@gmail.com', user_address=user_address,
           fact_address=fact_address)


user.save()




book = Book(ISBN="01234565",user_id = user, title="Harry", saga="Potter",description="first harry book",author="J.K.Rowling",price=30,language="Spanish",publisher="Alejandria",num_pages=200,num_sold=100,primary_genre="FANT",secondary_genre="OTHR",recommended_age = "Juvenil",thumbnail="/thumbnails/1234567.png")

book.save()

book1 = Book(ISBN="012389012",user_id = user, title="Potter", saga="saga",description="first harry book",author="J.ng",price=30,language="Spanish",publisher="Alejandria",num_pages=200,num_sold=100,primary_genre="CRIM",secondary_genre="OTHR",recommended_age = "Juvenil",thumbnail="/thumbnails/1234567.png")

book1.save()

book2 = Book(ISBN="01234567892",user_id = user, title="Sherlock", saga="Harry Potter",description="first harry book",author="J.aaa",price=30,language="Spanish",publisher="Alejandria",num_pages=200,num_sold=100,primary_genre="HORR",secondary_genre="OTHR",recommended_age = "Juvenil",thumbnail="/thumbnails/1234567.png")

book2.save()

book3 = Book(ISBN="01456789012",user_id = user, title="Holmes", saga="Harry Potter",description="first harry book",author="JUse",price=30,language="Spanish",publisher="Alejandria",num_pages=200,num_sold=100,primary_genre="ROMA",secondary_genre="OTHR",recommended_age = "Juvenil",thumbnail="/thumbnails/1234567.png")

book3.save()

book4 = Book(ISBN="01234567852",user_id = user, title="Muerte en el Nilo", saga="Harry Potter",description="first harry book",author="Josama",price=30,language="Spanish",publisher="Alejandria",num_pages=200,num_sold=100,primary_genre="FANT",recommended_age = "Juvenil",thumbnail="/thumbnails/1234567.png")

book4.save()

book5 = Book(ISBN="012349012",user_id = user, title="Hola", saga="Harry Potter",description="first harry book",author="Jacinto",price=30,language="Spanish",publisher="Alejandria",num_pages=200,num_sold=100,primary_genre="CRIM",secondary_genre="OTHR",recommended_age = "Juvenil",thumbnail="/thumbnails/1234567.png")

book5.save()

book6 = Book(ISBN="012345812",user_id = user, title="Holita", saga="Harry Potter",description="first harry book",author="Julieta",price=30,language="Spanish",publisher="Alejandria",num_pages=200,num_sold=100,primary_genre="CRIM",recommended_age = "Juvenil",thumbnail="/thumbnails/1234567.png")

book6.save()
