from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'books'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('book/<slug:pk>/', views.BookView.as_view(), name='book'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('delete/<product_id>/', views.delete_product, name='delete_product'),
    path('add/<view>/<book>/', views.add_product, name='add_product'),
    path('faqs/', views.FaqsView.as_view(), name='faqs'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('upload/', views.AddView.as_view(), name='add'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('sell/', views.SellView.add_book, name='sell'),
    path('forgot/', views.forgot, name='forgot'),
    path('forgot/<id>/', views.forgot, name='reset'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
