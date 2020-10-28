from django.shortcuts import render
from django.views import generic

from .models import Book, FAQ, Cart, Product, User, Author


# Create your views here.

class HomeView(generic.ListView):
    template_name = 'books/home.html'
    model = Book
    """
      Right now im passing all the books, but in the next iteration 
      Ill pass only those lists necessary por the Home page, like TopSellers, Genre lists, recommended, etc.
      #  TODO: Pass only necessary lists with get_queryset(self) and get_context_data()
      
      Example:
        # views.py
        from django.shortcuts import get_object_or_404
        from django.views.generic import ListView
        from books.models import Book, Publisher
        
        class PublisherBookList(ListView):
        
            template_name = 'books/books_by_publisher.html'
        
            def get_queryset(self):
                self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
                return Book.objects.filter(publisher=self.publisher)
                
            def get_context_data(self, **kwargs):
                # Call the base implementation first to get a context
                context = super().get_context_data(**kwargs)
                # Add in the publisher
                context['publisher'] = self.publisher
                return context
    
    """


class SearchView(generic.ListView):
    model = Book
    template_name = 'books/search.html'  # TODO: Provisional file

    #  TODO: Listen to Post from view, generate a response. To do that change genericView to a normal one.


class BookView(generic.DetailView):
    model = Book
    template_name = 'books/book.html'

    """
      Right now im passing all the books, but in the next iteration 
      Ill only pass the necessary book info, required by POST during the search.
      #  TODO: Pass only necessary lists with get_queryset(self) and get_context_data()

      Example:
        # views.py
        from django.shortcuts import get_object_or_404
        from django.views.generic import ListView
        from books.models import Book, Publisher

        class PublisherBookList(ListView):

            template_name = 'books/books_by_publisher.html'

            def get_queryset(self):
                self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
                return Book.objects.filter(publisher=self.publisher)

            def get_context_data(self, **kwargs):
                # Call the base implementation first to get a context
                context = super().get_context_data(**kwargs)
                # Add in the publisher
                context['publisher'] = self.publisher
                return context

    """


class CartView(generic.ListView):
    model = Book
    template_name = 'books/cart.html'  # TODO: Provisional file

    #  TODO: Listen to Post from view, generate a response. To do that change genericView to a normal one.


class FaqsView(generic.ListView):
    model = FAQ
    template_name = 'books/FAQs.html'  # TODO: Provisional file

    # TODO: In next iterations has to have the option to make POSTs by the admin.
