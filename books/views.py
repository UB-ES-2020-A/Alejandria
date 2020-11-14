from django.shortcuts import render

from django.views import generic

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth import authenticate, login

from .models import Book, FAQ, Cart, Product, User, Author, Address, Rating

# Create your views here.

"""
This is my custom response to get to a book by it's ISBN. The ISBN is passed by the front in an AJAX
"""

NUM_COINCIDENT = 10
NUM_RELATED = 5


def book(request):  # TODO: this function is not linked to the frontend
    if request.method == 'GET' and request['']:
        try:
            req_book = get_object_or_404(Book, pk=request.GET['ISBN'])  # I get ISBN set in frontend form ajax
        except(KeyError, Book.DoesNotExist):
            return render(request, 'search.html', {  # TODO: Provisional
                'error_message': 'Alejandria can not find this book.'
            })
        else:
            return render(request, 'details.html', {'book': req_book})

    elif request.method == 'POST':
        """
        Here we can treat different situations,
            Is it an admin, who wants to add a book?
            Is it an editor?
            What information do we need?
        """
        # TODO: Treat POST methods to save new Books
        return render(request, 'search.html', {'error_message': 'Not Implemented Yet'})  # TODO: Provisional


# This one works in thory when using the url with the pk inside # TODO: The idea is to use something like that
def book_pk(request, pk):
    req_book = get_object_or_404(Book, pk=pk)
    return render(request, 'details.html', {'book': req_book})


# This one is the same but uses a generic Model, lso should work with the primary key
class BookView(generic.DetailView):
    model = Book
    template_name = 'details.html'

    # TODO: Treat POST methods to add to cart, etc.
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs['pk']
        context['review_list'] = Rating.objects.filter(product_id=book_id).all()[:5]


    """
      Right now im passing all the books, but in the next iteration
      Ill only pass the necessary book info, required by POST during the search.
      #  TODO: Pass only necessary lists with get_queryset(self) and get_context_data()
      In this case I might use get_object().

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


class HomeView(generic.ListView):
    template_name = 'home.html'
    model = Book

    def get_queryset(self):  # TODO: Return list requested by the front end, TOP SELLERS, etc.
        return Book.objects.order_by('-num_sold')[:10]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtered_list'] = Book.objects.filter(title__contains='Red')  # Example

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


# TODO: Not being used
def search(request):  # TODO: Delete if SearchView is working as expected
    pass


class SearchView(generic.ListView):
    model = Book
    template_name = 'search.html'  # TODO: Provisional file

    def __init__(self):
        super().__init__()
        self.coincident = None
        self.related = None

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):  # TODO: This is a rather simple method, can be improved # TODO: TEST
        try:
            srch = self.kwargs['search']
        except:
            srch = None

        if srch != None:
            vector = SearchVector('title', 'saga', 'authors', 'description')
            query = SearchQuery(srch)
            self.coincident = Book.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')[:NUM_COINCIDENT]
            vector_related = SearchVector('saga', 'genre', 'authors')
            query_related = SearchQuery(" ".join((self.coincident[0].saga, self.coincident[0].genre,
                                                  self.coincident[
                                                      0].saga.authors)))  # TODO: Right now uses info of the first coincidende
            self.related = Book.objects.annotate(
                rel_rank=SearchRank(vector_related, query_related)).order_by('-rel_rank')[:NUM_RELATED]
            if len(self.coincident) > 0:
                context = super().get_context_data()
                context['error_message'] = 'No coincidences'
            return self.coincident

    def get_context_data(self, *, object_list=None, **kwargs):  # TODO: Test
        context = super().get_context_data(**kwargs)
        if not self.related or len(self.related) == 0:
            context['related_error_message'] = 'No Books Related Found'
        context['related'] = self.related


class CartView(generic.ListView):
    model = Book
    template_name = 'cart.html'  # TODO: Provisional file
    queryset = Product.objects.all()  # TODO: Right now im giving all the Products created to the Cart.
    # TODO: Should get books in User.Cart

    # TODO: Manage POST METHODS URGENT *****************************************

    #  TODO: Listen to Post from view, generate a response. To do that change genericView to a normal one.

    """
    Example:
    
    from django.http import HttpResponseRedirect
    from django.shortcuts import render
    from django.views import View
    
    from .forms import MyForm
    
    class MyFormView(View):
        form_class = MyForm
        initial = {'key': 'value'}
        template_name = 'form_template.html'
    
        def get(self, request, *args, **kwargs):
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})
    
        def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST)
            if form.is_valid():
                # <process form cleaned data>
                return HttpResponseRedirect('/success/')
    
            return render(request, self.template_name, {'form': form})
    """


class FaqsView(generic.ListView):
    model = FAQ
    template_name = 'FAQs.html'  # TODO: Provisional file

    # TODO: In next iterations has to have the option to make POSTs by the admin.


def register(request):
    def validate_register(data):
        # No Blank Data
        data_answered = all([len(data[key]) > 0 for key in data])
        exists = User.objects.filter(email=request.POST["email"]).exists()
        validation = data and not exists
        return validation

    if request.method == 'POST':
        if 'trigger' in request.POST and 'register' in request.POST['trigger']:
            if validate_register(request.POST):
                query = Address.objects.filter(city=request.POST['city1'], street=request.POST['street1'],
                                       country=request.POST['country1'], zip=request.POST['zip1'])
                if query.exists():
                    user_address = query.first()
                else:
                    user_address = Address.objects.filter(city=request.POST['city1'], street=request.POST['street1'],
                                           country=request.POST['country1'], zip=request.POST['zip1'])
                    user_address.save()

                if request.POST['city1'] == request.POST['city2'] and request.POST['street1'] == request.POST['street2'] and request.POST['country1'] == request.POST["country2"] and request.POST['zip1'] == request.POST["zip2"]:
                    fact_address = user_address
                else:
                    fact_address = Address(city=request.POST['city2'], street=request.POST['street2'],
                                           country=request.POST['country2'], zip=request.POST['zip2'])
                    fact_address.save()

                # Model creation
                user = User(role="user", username=request.POST['username'], name=request.POST['firstname'],
                            last_name=request.POST['lastname'], password=request.POST['password1'],
                            email=request.POST['email'], user_address=user_address,
                            fact_address=fact_address)
                user.save()

                return JsonResponse({"error": False})

            else:
                return JsonResponse({"error": True})


def login_user(request):
    if request.method == 'POST':
        if 'trigger' in request.POST and 'login' in request.POST['trigger']:
            user = User.objects.filter(email=request.POST['mail'], password=request.POST['password'])
            if user:
                user = user.first()
                login(request, user, backend='books.backend.EmailAuthBackend')
                return JsonResponse({"name": user.name, "error": False})
            else:
                return JsonResponse({"error": True})

        elif 'trigger' in request.POST and 'logout' in request.POST['trigger']:
            error = False
            try:
                logout(request)
            except:
                error = True

            return JsonResponse({"error": error})
