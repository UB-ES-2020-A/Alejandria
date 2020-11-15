from datetime import datetime, timedelta

from django.contrib.auth import login
from django.contrib.auth import logout
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic

from .forms import RegisterForm, LoginForm

from .models import Book, FAQ, Cart, Product, User, Address


# Create your views here.

"""
This is my custom response to get to a book by it's ISBN. The ISBN is passed by the front in an AJAX
"""

NUM_COINCIDENT = 10
NUM_RELATED = 5
MONTHS_TO_CONSIDER_TOP_SELLER = 6


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

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs['pk']
        context['review_list'] = Rating.objects.filter(product_id=book_id).all()[:5]
        if self.request.user.id == Book.objects.filter(ISBN=book_id).first().user_id:
            context['book_owner'] = True


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
        # context['novels'] = Book.objects.filter(genre__contains="Novel")

        return context


class SearchView(generic.ListView):
    model = Book
    template_name = 'search.html'  # TODO: Provisional file
    context_object_name = 'coincident'

    def __init__(self):
        super().__init__()
        self.coincident = None
        self.related = None
        self.searchBook = None
        self.genres = []

    def get(self, request, *args, **kwargs):
        print(request.GET)
        if 'search_book' in request.GET:
            self.searchBook = request.GET['search_book']
            print("esta es gucci", self.searchBook)
        else:
            keys = request.GET.keys()
            for key in keys:
                self.genres.append(request.GET[key])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):  # TODO: Test
        context = super().get_context_data(**kwargs)

        # Filtering by title or author
        if self.searchBook:
            filtered =  Book.objects.filter(Q(title__icontains=self.searchBook) | Q(author__icontains=self.searchBook))
            context['book_list'] = filtered
            return context
        # Filtering by genre (primary and secondary) using checkbox from frontend
        if self.genres:
            filtered = Book.objects.filter(Q(primary_genre__in=self.genres )| Q(secondary_genre__in=self.genres))
            context['book_list'] = filtered
            return context
        # TODO: Filtering by topseller and On Sale

        context['book_list'] = Book.objects.all()


        return context


class CartView(generic.ListView):
    model = Cart
    template_name = 'cart.html'  # TODO: Provisional file
    context_object_name = 'cart_list'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None

    def get_queryset(self):
        request = self.request
        print(request.GET)
        self.user_id = request.user.id or None
        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
            return cart.products.all()
        return None


def delete_product(request, product_id):
    user_id = request.user.id or None
    print(request.GET)
    if user_id:
        cart = Cart.objects.get(user_id=user_id)
        product = cart.products.get(ID=product_id)
        print("Delete Product ", product)
        cart.products.remove(product)
    return HttpResponseRedirect('/cart')


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

        return render(request,"login.html", {"form":form})


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
          

# TODO: Not implemented yet
class PaymentView(generic.TemplateView):
    model = Book
    template_name = 'payment.html'
    queryset = Product.objects.all()
