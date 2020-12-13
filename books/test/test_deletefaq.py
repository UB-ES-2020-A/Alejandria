"""
This file is used to test the case where an admin deletes a faq
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()

# Build up
from django.test import RequestFactory

# Then load own libs
from books.models import User, FAQ, Cart
from books.views import deletefaq


def test_deletefaq():
	# Admin user
	user = User(id=100, username="test_user", name="test_user", password="1234", email="test_user@mail.com",
	            role="Admin")
	user.save()
	cart = Cart(user_id=user, guest_id=None)
	cart.save()
	original_faq = FAQ(question="Original question", category=FAQ.FAQ_CHOICES[0][0], answer="Original answer")
	original_faq.save()
	
	body = {'original': original_faq.question}
	req = RequestFactory().post("/deletefaq/", body)
	req.user = user
	
	response = deletefaq(request=req)
	
	assert response.status_code == 200
	
	original_faq_query = FAQ.objects.filter(question=original_faq.question)
	assert (len(original_faq_query) == 0)
	
	# Faq does not exist
	# After de delete should not exist
	body = {'original': original_faq.question}
	req = RequestFactory().post("/deletefaq/", body)
	req.user = user
	
	response = deletefaq(request=req)
	
	assert response.status_code == 404
	
	user.delete()
	cart.delete()
	
	# Anonymous User Forbidden
	user = "AnonymousUser"
	
	original_faq = FAQ(question="Original question", category=FAQ.FAQ_CHOICES[0][0], answer="Original answer")
	original_faq.save()
	
	body = {'original': original_faq.question}
	req = RequestFactory().post("/deletefaq/", body)
	req.user = user
	
	response = deletefaq(request=req)
	
	assert response.status_code == 403
	

