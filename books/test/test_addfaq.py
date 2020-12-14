"""
This file is used to test the case where an admin adds a faq
"""
import json
import os
import random
import string

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()
from django.urls import reverse
# Build up
from django.test import RequestFactory

# Then load own libs
from books.models import User, FAQ, Cart
from books import views
from books.views import addfaq


def test_addfaq():
	# Admin user
	user = User(id=100, username="test_user", name="test_user", password="1234", email="test_user@mail.com", role="Admin")
	user.save()
	cart = Cart(user_id=user, guest_id=None)
	cart.save()
	
	# Assert True
	body = {'category': FAQ.FAQ_CHOICES[0][1], 'question': "Test Question", 'answer': "This is my test answer"}
	print(body)
	req = RequestFactory().post("/addfaq/", body)
	req.user = user
	
	response = addfaq(request=req)

	assert response.status_code == 200
	
	# Bad category
	body = {'category': "WRONG_CATEGORY", 'question': "Test Question", 'answer': "This is my test answer"}
	print(body)
	req = RequestFactory().post("/addfaq/", body)
	req.user = user
	
	response = addfaq(request=req)
	
	assert response.status_code == 403
	
	user.delete()
	cart.delete()
	
	# Not allowed user
	# Non Admin user
	user = User(id=100, username="test_notadmin", name="test_notadmin", password="1234", email="test_notadmin@mail.com", role="User")
	user.save()
	cart = Cart(user_id=user, guest_id=None)
	cart.save()
	
	body = {'category':FAQ.FAQ_CHOICES[0][1], 'question': "Test Question", 'answer': "This is my test answer"}
	print(body)
	req = RequestFactory().post("/addfaq/", body)
	req.user = user
	
	response = addfaq(request=req)
	
	assert response.status_code == 403
	
	user.delete()
	cart.delete()
	
	# Anonymous User: Not allowed
	user = "AnonymousUser"
	
	body = {'category': FAQ.FAQ_CHOICES[0][1], 'question': "Test Question", 'answer': "This is my test answer"}
	print(body)
	req = RequestFactory().post("/addfaq/", body)
	req.user = user
	
	response = addfaq(request=req)
	
	assert response.status_code == 403
	
