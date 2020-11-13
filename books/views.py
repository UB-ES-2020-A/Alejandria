from django.views import generic

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegisterForm, LoginForm

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta

from .models import Book, FAQ, Cart, Product, User, Author

# Create your views here.

"""
This is my custom response to get to a book by it's ISBN. The ISBN is passed by the front in an AJAX
"""

NUM_COINCIDENT = 10
NUM_RELATED = 5
MONTHS_TO_CONSIDER_TOP_SELLER = 6

# Method decorators TODO: NOT TESTED, I don't know how we should test if the user is logged in etc.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
decorators = [login_required]


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

    # TODO: Treat POST to add a book


class HomeView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'book_list'
    model = Book

    # queryset = Book.objects.all()
    def get_queryset(self):  # TODO: Return list requested by the front end, TOP SELLERS, etc.
        today = datetime.today()
        return Book.objects.all()  ## TODO: Replace with the one below when ready to test with a full database.
        # return Book.objects.order_by('-num_sold')[:10].filter(
        #     publication_date__range=[str(today)[:10],
        #                              str(today - timedelta(days=30 * MONTHS_TO_CONSIDER_TOP_SELLER))[:10]])[:10]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today()
        context['new_books'] = Book.objects.filter(
            publication_date__range=[str(today)[:10], str(today - timedelta(days=10))[:10]])[:10]
        context['novels'] = Book.objects.filter(genre__contains="Novel")

        return context


class SearchView(generic.ListView):
    model = Book
    template_name = 'search.html'  # TODO: Provisional file
    context_object_name = 'coincident'

    def __init__(self):
        super().__init__()
        self.coincident = None
        self.related = None

    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)

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
        return context


class CartView(generic.ListView):
    model = Book
    template_name = 'cart.html'  # TODO: Provisional file

    ## TODO: This is m aproach to Cart post method, but it shouldn't be done in this branch.
    # def get_queryset(self):
    #     if self.logged_in():
    #         user = User.objects.get(username=super().request.POST['username'], password=super().request.POST['password'])
    #         return User.objects.filter(username=user).products.all()
    #     else:
    #         ## TODO: What to do when visitant whants to see it's Cart @method_decorator??
    #         return None ## TODO and error_message
    #
    # def post(self, request, *args, **kwargs):
    #     ## TODO: Make form to check if the request for CartView is good.
    #     auth = super().request.auth
    #     print(auth)
    #     if auth: ## https://www.django-rest-framework.org/api-guide/authentication/
    #         user = super().request.user
    #         if user: ## TODO User and auth is linked somehow? or request.user?
    #             pass
    #
    #
    #     #return render(request, self.template_name, {'form': form})
    #
    # ## TODO Check if the user is logged in. With tocken or userneme password or auth or user
    # def logged_in(self):
    #     return True


class FaqsView(generic.ListView):
    model = FAQ
    template_name = 'FAQs.html'  # TODO: Provisional file

    # TODO: In next iterations has to have the option to make POSTs by the admin.


class RegisterView(generic.TemplateView):

    @staticmethod
    def register(request):
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect("/")
        else:
            form = RegisterForm()

        return render(request, "register.html", {"form": form})


class LoginView(generic.TemplateView):

    @staticmethod
    def login(request):
        form = LoginForm(request.POST)
        if request.method == 'POST':
            # user = authenticate(
            #    username=request.POST['username'],
            #    password=request.POST['password'],backend='books.backend.EmailAuthBackend'
            # )
            user = User.objects.get(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user, backend='books.backend.EmailAuthBackend')
                return redirect("/")

        return render(request, "login.html", {"form": form})
