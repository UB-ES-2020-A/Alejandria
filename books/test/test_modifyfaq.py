"""
This file is used to test the case where an admin modifies a faq
"""
import os


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alejandria.settings')
app = get_wsgi_application()

# Build up
from django.test import RequestFactory

# Then load own libs
from books.models import User, FAQ, Cart
from books.views import modifyfaq


def test_modifyfaq():
	# Admin user
	user = User(id=100, username="test_user", name="test_user", password="1234", email="test_user@mail.com",
	            role="Admin")
	user.save()
	cart = Cart(user_id=user, guest_id=None)
	cart.save()
	original_faq = FAQ(question="Original question", category=FAQ.FAQ_CHOICES[0][0], answer="Original answer")
	original_faq.save()
	
	body = {'original': original_faq.question,
	       'category': FAQ.FAQ_CHOICES[1][1],
           'question': "Test Question",
			'answer': "This is my test answer"}
	req = RequestFactory().post("/modifyfaq/", body)
	req.user = user
	
	response = modifyfaq(request=req)
	
	assert response.status_code == 200
	
	original_faq = FAQ.objects.filter(question=original_faq.question)
	assert(len(original_faq) == 0)
	modified_faq = FAQ.objects.filter(question="Test Question")
	assert(len(modified_faq) > 0)
	
	
	# Bad original
	body = {'original': "This question does not exist",
	        'category': FAQ.FAQ_CHOICES[1][1],
	        'question': "Test Question",
	        'answer': "This is my test answer"}
	print(body)
	req = RequestFactory().post("/modifyfaq/", body)
	req.user = user
	
	response = modifyfaq(request=req)
	
	assert response.status_code == 403
	
	# Bad category
	body = {'original': modified_faq.first().question,
	        'category': "Bad category",
	        'question': "Test Question",
	        'answer': "This is my test answer"}
	print(body)
	req = RequestFactory().post("/modifyfaq/", body)
	req.user = user
	
	response = modifyfaq(request=req)
	
	assert response.status_code == 403
	
	user.delete()
	cart.delete()
	
	# Not allowed user
	# Non Admin user
	user = User(id=100, username="test_notadmin", name="test_notadmin", password="1234",
	            email="test_notadmin@mail.com",
	            role="User")
	user.save()
	cart = Cart(user_id=user, guest_id=None)
	cart.save()
	
	body = {'original': modified_faq.first().question,
	        'category': FAQ.FAQ_CHOICES[0][1],
	        'question': "Test Question",
	        'answer': "This is my test answer"}
	print(body)
	req = RequestFactory().post("/modifyfaq/", body)
	req.user = user
	
	response = modifyfaq(request=req)
	
	assert response.status_code == 403
	
	user.delete()
	cart.delete()
	
	# Anonymous User: Not allowed
	user = "AnonymousUser"
	
	body = {'original': modified_faq.first().question,
	        'category': FAQ.FAQ_CHOICES[0][1],
	        'question': "Test Question",
	        'answer': "This is my test answer"}
	print(body)
	req = RequestFactory().post("/modifyfaq/", body)
	req.user = user
	
	response = modifyfaq(request=req)
	
	assert response.status_code == 403
	
	modified_faq.delete()

