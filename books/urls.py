from django.contrib.auth.decorators import permission_required
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
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('sell/', views.SellView.as_view(), name='sell'),
    path('forgot/', views.forgot, name='forgot'),
    path('forgot/<id>/', views.forgot, name='reset'),
    path('review/<slug:pk>/', views.BookView.as_view(), name='post_review'),
    path('review/', views.leave_review, name='leave_review'),
    path('editor/', views.EditorLibrary.as_view(), name='editor_library'),
    path('profile/', views.view_profile, name="view_profile"),
    path('purchase/', views.complete_purchase, name='purchase'),
    path('editBook/<slug:pk>/', views.EditBookView.as_view(), name='edit_book'),
    path('deleteBook/<slug:pk>/', views.DeleteBookView.as_view(), name='delete_book'),
    path('pdf/', views.generate_pdf, name='generate_bill'),
    path('library/', views.UserLibrary.as_view(), name='user_library'),
    path('bills/', views.UserBills.as_view(), name='user_bills')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
