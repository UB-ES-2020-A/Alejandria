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
from books.models import User, Guest, FAQ, Cart
from books import views
from books.views import addfaq, modifyfaq, deletefaq, FaqsView


class FaqsViewTest(TestCase):
        def setUp(self):
            # Every test needs a client.
            self.client = Client()
            self.user = User(id=100, username="test_user", name="test_user", password="1234", email="test_user@mail.com", role="editor")
            self.user.save()
            self.cart = Cart(user_id=self.user, guest_id=None)
            self.cart.save()
            
            
        def test_details(self):
            # Issue a GET request.
            factory = RequestFactory()
            request = factory.get('/faqs/')
            request.user = self.user
            response = FaqsView.as_view()(request)
            # Check that the response is 200 OK.
            self.assertEqual(response.status_code, 200)

            category_names = response.context_data.get('category_names')
            list_query = response.context_data.get('list_query')
            # Check that the rendered context contains 5 customers.
            self.assertEqual(list(category_names.values()), [a[1] for a in FAQ.FAQ_CHOICES])
            self.assertTrue(len(list_query) > 0)
            
            self.user.delete()
            self.cart.delete()
            