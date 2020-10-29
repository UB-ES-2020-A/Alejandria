# Django and 3rd party libs
import pytest
import os
from django.core.wsgi import get_wsgi_application

# Build app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()

# Then load own libs
from books.models import Address, User


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
    obj = Address.objects.all().first()
    check = all([street == obj.street, city == obj.city, country == obj.country, zip_code == obj.zip])
    # Test sucess if check is True
    assert check


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
    obj = User.objects.all().first()
    check = all([id == obj.id, role == obj.role, name == obj.name, password == obj.password, email == obj.email,
                 user_address == obj.user_address, fact_address == obj.fact_address])
    # Test sucess if check is True
    assert check
