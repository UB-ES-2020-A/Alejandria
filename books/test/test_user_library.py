import json
import os
import random
import string

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()
from django.urls import reverse
# Build up
from django.test import TestCase, Client, RequestFactory

# Then load own libs
from books.models import User, FAQ, Cart
from books import views
from books.views import UserLibrary


class UserLibraryTest(TestCase):
	def setUp(self):
		# Every test needs a client.
		self.client = Client()
		self.user = User(id=100, username="test_user", name="test_user", password="1234", email="test_user@mail.com",
		                 role="editor")
		self.user.save()
		self.cart = Cart(user_id=self.user, guest_id=None)
		self.cart.save()
	
	def test_details(self):
		# Issue a GET request.
		factory = RequestFactory()
		request = factory.get('/library/')
		request.user = self.user
		response = UserLibrary.as_view()(request)
		# Check that the response is 200 OK.
		self.assertEqual(response.status_code, 200)
		try:
			coincident = response.context_data.get('coincident')
		except:
			assert False
		
		self.user.delete()
		self.cart.delete()
