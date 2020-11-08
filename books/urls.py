from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('book/<slug:pk>/', views.BookView.as_view(), name='book'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('faqs/', views.FaqsView.as_view(), name='faqs'),
    path('register/', views.RegisterView.register, name='register'),
    path('login/', views.login_user, name='login'),

]