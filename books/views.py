import random
import re
from datetime import datetime, timedelta
from io import BytesIO

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from reportlab.pdfgen import canvas

from Alejandria.settings import EMAIL_HOST_USER

from .utils import *
from .forms import BookForm, UpdateBookForm
from .models import Book, FAQ, Cart, Product, User, Address, ResetMails, Guest, BankAccount, Bill, LibraryBills, Rating

# Create your views here.

"""
This is my custom response to get to a book by it's ISBN. The ISBN is passed by the front in an AJAX
"""

NUM_COINCIDENT = 10
NUM_RELATED = 5
MONTHS_TO_CONSIDER_TOP_SELLER = 6


# This one is the same but uses a generic Model, lso should work with the primary key
class BookView(generic.DetailView):
    model = Book
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        relation_book = Book.objects.filter(primary_genre=context['object'].primary_genre)[:20]
        context['isbn'] = str(context['object'].ISBN)
        review_list = Rating.objects.filter(ISBN=context['object'])
        if self.request.user.id != None:
            owned = Product.objects.filter(bill__in=Bill.objects.filter(user_id=self.request.user)).filter(ISBN=context['book']).first()
            if owned:
                context['owned'] = "true"

        if relation_book:
            context['book_relation'] = relation_book
        else:
            context['book_relation'] = Book.objects.all()[:20]

        if review_list:
            context['review_list'] = review_list

        if 'owned' not in context.keys():
            context['owned'] = 'false'

        return context


class HomeView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'book_list'
    model = Book

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None

    # queryset = Book.objects.all()
    def get_queryset(self):  # TODO: Return list requested by the front end, TOP SELLERS, etc.

        today = datetime.today()
        self.user_id = self.request.user.id or None
        # return Book.objects.all() # TODO: Replace with the one below when ready to test with a full database.
        return Book.objects.order_by('-num_sold')[:20]
        # .filter(publication_date__range=[str(today)[:10],str(today - timedelta(days=30 * MONTHS_TO_CONSIDER_TOP_SELLER))[:10]])[:10]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today().strftime("%Y-%m-%d")
        last_day = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")

        context['recent'] = Book.objects.filter(publication_date__range=[last_day, today])
        context['fantasy'] = Book.objects.filter(primary_genre__contains="FANT")
        context['crime'] = Book.objects.filter(primary_genre__contains="CRIM")
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(HomeView, self).render_to_response(context, **response_kwargs)

        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
        else:
            device = self.request.COOKIES.get('device')
            if not device:
                device = self.generate_id()
                response.set_cookie('device', device)

            user, created = Guest.objects.get_or_create(device=device)
            cart, created = Cart.objects.get_or_create(guest_id=user)
        if cart:
            products = cart.products.all()
            items = len(products)
            context['total_items'] = items

        return response


    @staticmethod
    def generate_id():
        temp = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
        list_id = [str(random.randint(0, 16)) if character == 'x' else character for character in temp]
        id = "".join(list_id)
        return id


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
        self.user_id = None
        self.genres_preferences = []

    def get(self, request, *args, **kwargs):
        self.user_id = self.request.user.id or None
        if self.user_id:
            self.genres_preferences.append(request.user.genre_preference_1)
            self.genres_preferences.append(request.user.genre_preference_2)
            self.genres_preferences.append(request.user.genre_preference_3)
        if 'search_book' in request.GET:
            self.searchBook = request.GET['search_book']
        else:
            keys = request.GET.keys()
            for key in keys:
                self.genres.append(request.GET[key])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):  # TODO: Test
        context = super().get_context_data(**kwargs)

        # Get number of cart products
        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
        else:
            device = self.request.COOKIES['device']
            user, created = Guest.objects.get_or_create(device=device)
            cart, created = Cart.objects.get_or_create(guest_id=user)

        products = cart.products.all()
        items = len(products)
        context['total_items'] = items

        # Filtering by title or author
        if self.searchBook:
            filtered = Book.objects.filter(Q(title__icontains=self.searchBook) | Q(author__icontains=self.searchBook))[
                       :20]
            context['book_list'] = filtered
            genres_relation = []
            for book in filtered:
                if book.primary_genre not in genres_relation:
                    genres_relation.append(book.primary_genre)

            relation_book = Book.objects.filter(primary_genre__in=genres_relation)[:20]
            if relation_book:
                context['book_relation'] = relation_book
                return context

        if self.genres:
            filtered = Book.objects.filter(Q(primary_genre__in=self.genres) | Q(secondary_genre__in=self.genres))[:20]
            context['book_list'] = filtered
        if self.user_id:
            recommended_books = Book.objects.filter(
                (Q(primary_genre__in=self.genres_preferences)
                 | Q(secondary_genre__in=self.genres_preferences)))

            recommended_books_list = list(recommended_books)
            recommended_books_list = random.sample(recommended_books_list, min(len(recommended_books_list), 20))
            context['recommended_books'] = recommended_books_list

        return context


class SellView(PermissionRequiredMixin, generic.ListView):
    model = Book
    template_name = 'sell.html'
    permission_required = ('books.add_book',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # post (update) of book
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                book = form.save(commit=False)
                # intern fields (not showed to user)
                book.user_id = request.user
                book.num_sold = 0

                messages.info(request, 'Your book has been created successfully!')

                book.save()
            else:
                messages.info(request, 'Oops.. something is wrong')

        else:
            form = BookForm()

        return render(request, "sell.html", {"form": form})


class EditBookView(PermissionRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'edit_book.html'
    permission_required = ('books.add_book',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # format data to suit frontend requirements
        context['date'] = context['book'].publication_date.strftime("%Y-%m-%d")
        return context

    # post (update) of book
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # get the instance to modify
            s = get_object_or_404(Book, pk=self.kwargs['pk'])
            form = UpdateBookForm(request.POST, instance=s)
            if form.is_valid():
                book = form.save(commit=False)
                # intern field (not shown to user)
                book.user_id = request.user
                messages.info(request, 'Your book has been updated successfully!')
                book.save()
            else:
                messages.info(request, 'Oops.. something is wrong')
        else:
            form = UpdateBookForm()
        return render(request, "edit_book.html", {"form": form})


class DeleteBookView(PermissionRequiredMixin, generic.DeleteView):
    model = Book
    template_name = 'delete_book.html'
    permission_required = ('books.delete_book',)
    success_url = '/editor'

    # this is a push test

    def get_object(self, queryset=None):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        if self.request.user == book.user_id:
            return book
        else:
            print('Are you trying to delete a book that is not yours?')
            return HttpResponseForbidden()


class CartView(generic.ListView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'cart_list'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None

    def get_queryset(self):
        request = self.request
        self.user_id = request.user.id or None
        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
        else:
            device = request.COOKIES['device']
            user, created = Guest.objects.get_or_create(device=device)
            cart, created = Cart.objects.get_or_create(guest_id=user)

        return cart.products.all()

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['books_from_cart_view'] = Book.objects.all()[:6]
        context['books_from_cart_view_1'] = Book.objects.all()[:3]
        context['books_from_cart_view_2'] = Book.objects.all()[3:6]
        context['books_from_cart_view_3'] = Book.objects.all()[6:9]
        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
        else:
            device = self.request.COOKIES['device']
            user, created = Guest.objects.get_or_create(device=device)
            cart, created = Cart.objects.get_or_create(guest_id=user)

        products = cart.products.all()
        total_price = 0
        items = len(products)
        for prod in products:
            total_price += prod.price
        context['total_price'] = total_price
        context['total_items'] = items

        return context


def delete_product(request, product_id):
    user = request.user or None
    print(request.GET)
    if user:
        user_id = user.id
        if user_id:
            cart = Cart.objects.get(user_id=user_id)
        else:
            device = request.COOKIES['device']
            user = Guest.objects.get(device=device)
            cart = Cart.objects.get(guest_id=user)
    else:
        device = request.COOKIES['device']
        user = Guest.objects.get(device=device)
        cart = Cart.objects.get(guest_id=user)

    product = cart.products.get(ID=product_id)
    print("DELETE BOOK ", product)
    cart.products.remove(product)
    cart.save()
    return HttpResponseRedirect('/cart')


def add_product(request, view, book):
    user = request.user or None
    print(request.POST)
    if user:
        user_id = user.id
        if user_id:
            cart = Cart.objects.get(user_id=user_id)
        else:
            device = request.COOKIES['device']
            user, created = Guest.objects.get_or_create(device=device)
            cart, created = Cart.objects.get_or_create(guest_id=user)

    else:
        device = request.COOKIES['device']
        user, created = Guest.objects.get_or_create(device=device)
        cart, created = Cart.objects.get_or_create(guest_id=user)

    products = Product.objects.all()
    for product in products:
        if product.ISBN.ISBN == book:
            print("ADD BOOK ", book)
            cart.products.add(product)
            cart.save()

    if view == 'home':
        return HttpResponseRedirect('/')
    if view == 'cart':
        return HttpResponseRedirect('/cart')


class FaqsView(generic.ListView):
    model = FAQ
    template_name = 'faqs.html'  # TODO: Provisional file
    context_object_name = 'faqs'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None

    def get_queryset(self):
        self.user_id = self.request.user.id or None
        return FAQ.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        _range = list(range(len(FAQ.FAQ_CHOICES)))
        context['category_names'] = dict(zip(_range, [a[1] for a in FAQ.FAQ_CHOICES]))
        context['list_query'] = dict(zip(_range, [FAQ.objects.filter(category='DWL'),
                                                  FAQ.objects.filter(category='REF'),
                                                  FAQ.objects.filter(category='SEL'),
                                                  FAQ.objects.filter(category='FAC'),
                                                  FAQ.objects.filter(category='CON')]))
        print(context)

        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
        else:
            device = self.request.COOKIES['device']
            user, created = Guest.objects.get_or_create(device=device)
            cart, created = Cart.objects.get_or_create(guest_id=user)

        products = cart.products.all()
        items = len(products)
        context['total_items'] = items

        return context

    # TODO: In next iterations has to have the option to make POSTs by the admin.
    def post(self):
        pass


class AddView(generic.ListView):
    model = Book
    template_name = 'createbook.html'

    def post(self, request, *args, **kwargs):
        book = Book.objects.filter(ISBN=request.POST['isbn']).first()

        if book:

            if book.user_id != request.user.id:
                return JsonResponse({'message': 'The book does not belong to you'}, status=401)

            else:
                print('The book exists')
                book.title = request.POST['title']
                book.user_id = request.user.id
                book.authors = request.POST['author']
                book.description = request.POST['description']
                book.saga = request.POST['saga']
                book.price = float(request.POST['price'])
                book.language = request.POST['language']
                # book.genre = request.POST['genre']
                book.publisher = request.POST['publisher']
                book.num_pages = request.POST['numpages']
                book.recommended_age = request.POST['recommendedage']
                book.thumbnail = request.POST['thumbnail']
                book.ebook = request.POST['ebook']

                book.save()

                return JsonResponse({'message': 'The book was modified successfully'}, status=200)

        else:
            print('The book does not exist')
            newbook = Book(ISBN=request.POST['isbn'],
                           user_id=User.objects.filter(username="franchito55").first(),
                           title=request.POST['title'],
                           # authors=request.POST['author'],
                           description=request.POST['description'],
                           saga=request.POST['saga'],
                           price=float(request.POST['price']),
                           language=request.POST['language'],
                           genre=request.POST['genre'],
                           publisher=request.POST['publisher'],
                           num_pages=request.POST['numpages'],
                           recommended_age=request.POST['recommendedage'],
                           thumbnail=request.POST['thumbnail'],
                           ebook=request.POST['ebook'])

            newbook.save()

            return JsonResponse({'message': 'The book was added successfully'}, status=200)


def register(request):
    if request.method == 'POST':
        if 'trigger' in request.POST and 'register' in request.POST['trigger']:
            if validate_register(request):
                query = Address.objects.filter(city=request.POST['city1'], street=request.POST['street1'],
                                               country=request.POST['country1'], zip=request.POST['zip1'])
                if query.exists():
                    user_address = query.first()
                else:
                    user_address = Address(city=request.POST['city1'], street=request.POST['street1'],
                                           country=request.POST['country1'], zip=request.POST['zip1'])
                    user_address.save()

                if request.POST['city1'] == request.POST['city2'] and request.POST['street1'] == request.POST[
                    'street2'] and request.POST['country1'] == request.POST["country2"] and request.POST['zip1'] == \
                        request.POST["zip2"]:
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

                if request.POST['tastes']:
                    if request.POST["taste1"] != "Choose":
                        user.genre_preference_1 = encode_genre(request.POST["taste1"])

                    if request.POST["taste2"] != "Choose":
                        user.genre_preference_2 = encode_genre(request.POST["taste2"])

                    if request.POST["taste3"] != "Choose":
                        user.genre_preference_3 = encode_genre(request.POST["taste3"])

                user.save()

                # Create user's cart
                device = request.COOKIES.get('device')
                guest, created = Guest.objects.get_or_create(device=device)
                cart_user, created = Cart.objects.get_or_create(user_id=user)
                if device:
                    cart_guest_query = Cart.objects.filter(guest_id=guest)
                    if cart_guest_query.count() != 0:
                        cart_guest = cart_guest_query.first()
                        for product in cart_guest.products.all():
                            cart_user.products.add(product)
                        cart_guest.products.clear()
                        cart_guest.save()
                        cart_user.save()

                return JsonResponse({"error": False})

            else:
                return JsonResponse({"error": True})

        return JsonResponse({"error": True})


def forgot(request, **kwargs):
    if request.method == 'POST':
        if 'trigger' in request.POST and request.POST['trigger'] == 'forgot':
            recipient = request.POST['mail']
            query = User.objects.filter(email=recipient)
            if query.exists():
                try:
                    last = ResetMails.objects.latest('id')
                    last = last.id + 1
                except:
                    last = 0

                subject = 'Alejandria Password Reset'
                host = request.get_raw_uri()
                matches = re.finditer('/', host)
                idx = [match.start() for match in matches][2]
                link = host[:idx] + "/forgot/" + str(last) + "/"
                msg = 'Dear, ' + query.first().username + '\n\n Confirm your new password using this link: ' + link + "\n Remember that once you complete the change this link will be disabled.\n\n Alejandria Team."

                try:
                    ResetMails(id=last, user=query.first()).save()
                    send_mail(subject, msg, EMAIL_HOST_USER, [recipient], fail_silently=True)
                    return JsonResponse({"error": False,
                                         "msg": "Reset mail was sent to " + recipient + " successfully. Please check your inbox."})
                except:
                    return JsonResponse({"error": True, "msg": "Your request failed, please try it again."})

            return JsonResponse({"error": True,
                                 "msg": "Invalid mail address"})


        elif 'trigger' in request.POST and request.POST['trigger'] == 'reset':
            try:
                reset_id = kwargs['id']
                new_pass = request.POST['new_pass']
                user = ResetMails.objects.filter(id=int(reset_id)).first().user
                user.password = new_pass
                user.save()
                return JsonResponse({"error": False})
            except:
                return JsonResponse({"error": True})

    elif request.method == 'GET':
        reset_id = kwargs['id']
        query = ResetMails.objects.filter(id=reset_id)

        if query.exists() and query.first().activated:
            return render(request, "reset.html")
        else:
            return render(request, "not_found.html")


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


class PaymentView(generic.ListView):
    # model = Account
    template_name = 'payment.html'
    queryset = Product.objects.all()
    context_object_name = 'cart_list'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None
        self.username = ''
        self.card_number = ''
        self.total = 0
        self.products = None
        self.year = None
        self.month = None
        self.cvv = None

    def get_queryset(self):
        request = self.request
        print(request.GET)
        self.user_id = request.user.id or None
        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
            if cart:
                return cart.products.all()
        return None

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
            user_bank_account = BankAccount.objects.filter(user_id=self.user_id).first() or None
            products = cart.products.all()
            total_price = 0
            items = len(products)
            for prod in products:
                total_price += prod.price
            context['total_price'] = total_price
            context['total_items'] = items
            if user_bank_account is not None:
                context['card_owner'] = self.username
                context['card_number'] = self.card_number
                context['month'] = self.month
                context['year'] = self.year
                context['cvv'] = self.cvv
        else:
            context['total_items'] = 0

        return context


class EditorLibrary(PermissionRequiredMixin, generic.ListView):
    model = Book
    template_name = 'editor_library.html'  # TODO: Provisional file
    context_object_name = 'coincident'
    permission_required = ('books.add_book',)

    # permission_required = 'Alejandria.view_book'

    def __init__(self):
        super().__init__()
        self.editorBooks = None
        self.user_id = None

    def get(self, request, *args, **kwargs):
        print(request.GET)
        self.user_id = self.request.user.id or None

        # if 'search_book' in request.GET:
        #     self.searchBook = request.GET['search_book']
        # else:
        #     keys = request.GET.keys()
        #     for key in keys:
        #         self.genres.append(request.GET[key])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):  # TODO: Test
        context = super().get_context_data(**kwargs)

        # Filtering by title or author
        print(self.user_id)
        editor_books = Book.objects.filter(user_id=self.user_id)
        print("editor books", editor_books)
        context['editor_books'] = editor_books

        return context


def leave_review(request, **kwargs):
    if request.method == 'POST':
        if 'deleting' in request.POST:
            review = Rating.objects.filter(ID=request.POST['review_id']).first()
            if review:
                review.delete()
                return JsonResponse({"message": "Your review was deleted successfully!"})
            else:
                return JsonResponse({"error": "The provided review doesn't exist."})

        elif 'modifying' in request.POST:
            print("Your request is being modified...")
            review = Rating.objects.filter(ID=request.POST['review_id']).first()
            if review:
                review.score = request.POST['score']
                review.text = request.POST['text']
                review.save()
                return JsonResponse({"message": "Your review was modified successfully!"})
            return JsonResponse({"error": "The provided review doesn't exist"})

        elif 'adding' in request.POST:
            if int(request.POST['score']) < 0 or int(request.POST['score']) > 5:
                return JsonResponse({"error": "You must provide a valid score (between 0 and 5)."})
            if len(request.POST['text']) > 500:
                return JsonResponse({"error": "The maximum text length is 500 characters."})

            book = Book.objects.filter(ISBN=request.POST['book']).first()
            review = Rating(ISBN=book,
                            user_id=request.user,
                            text=request.POST['text'],
                            score=request.POST['score'])

            review.save()
            print("Your review was added successfully!")
            return JsonResponse({"message": "Your review was added successfully!"})


def view_profile(request):
    if request.method == "POST":
        if validate_data(request):
            try:
                user = request.user

                # Let's process modified data
                # User Address
                query = Address.objects.filter(street=request.POST["street1"], city=request.POST["city1"],
                                               country=request.POST["country1"], zip=request.POST['zip1'])
                if query.exists():
                    user_address = query.first()
                else:
                    user_address = Address(street=request.POST["street1"], city=request.POST["city1"],
                                           country=request.POST["country1"], zip=request.POST['zip1'])
                    user_address.save()

                # Facturation address
                query = Address.objects.filter(street=request.POST["street2"], city=request.POST["city2"],
                                               country=request.POST["country2"], zip=request.POST['zip2'])
                if query.exists():
                    fact_address = query.first()
                else:
                    fact_address = Address(street=request.POST["street2"], city=request.POST["city2"],
                                           country=request.POST["country2"], zip=request.POST['zip2'])
                    fact_address.save()

                # Process full name
                tokens = tokenize(request.POST["full_name"])
                first_name = " ".join(tokens[:-1])
                last_name = " ".join(tokens[-1:])

                # Process tastes
                if request.POST["taste1"]:
                    genre_preference_1 = encode_genre(request.POST["taste1"])

                if request.POST["taste2"]:
                    genre_preference_2 = encode_genre(request.POST["taste2"])

                if request.POST["taste3"]:
                    genre_preference_3 = encode_genre(request.POST["taste3"])

                # Apply changes
                user.username = request.POST["username"]
                user.email = request.POST["email"]
                user.user_address = user_address
                user.fact_address = fact_address
                user.name = first_name
                user.first_name = first_name
                user.last_name = last_name
                user.genre_preference_1 = genre_preference_1
                user.genre_preference_2 = genre_preference_2
                user.genre_preference_3 = genre_preference_3

                user.save()

                return JsonResponse({"error": False})

            except Exception as err:
                return JsonResponse({"error": True, "msg": "Unexpected error, please try it again"})

        return JsonResponse({"error": True, "msg": "Invalid data!"})

    elif request.method == "GET":
        user = request.user.id
        if user:
            cart = Cart.objects.get(user_id=user)
            products = cart.products.all()
            items = len(products)
            context = {
                'total_items': items
            }
        return render(request, "view_profile.html", context)


def complete_purchase(request):
    print(request.POST)

    user = request.user.id or None

    if user:

        user_bank_account, created = BankAccount.objects.get_or_create(user_id=user)
        current_money = float(user_bank_account.money)

        cart = Cart.objects.get(user_id=user)
        products = cart.products.all()
        total = 0
        for p in products:
            total += p.price
        total = float(total)

        if current_money - total >= 0:

            user_bank_account.money = str(round(current_money - total, 2))
            user_bank_account.name = request.POST.get('username')
            user_bank_account.month_exp = request.POST.get('month_exp')
            user_bank_account.year_exp = request.POST.get('year_exp')
            user_bank_account.card_number = request.POST.get('cardNumber')
            user_bank_account.cvv = request.POST.get('cvv')

            try:
                user_bank_account.full_clean()

            except ValidationError:
                # Do something when validation is not passing
                print("ERROR VALIDATION")
                user_bank_account.delete()
                messages.error(request, "An error has occurred, check that all data is in the correct format.")

            else:
                # Validation is ok we will save the instance
                user_bank_account.save()

                bill = Bill(user_id_id=user)
                bill.save()
                lib_of_bills, created = LibraryBills.objects.get_or_create(user_id=request.user)
                setattr(bill, 'total_money_spent', total)
                setattr(bill, 'payment_method', 'Credit card')
                setattr(bill, 'name', user_bank_account.name)
                for p in products:
                    bill.products.add(p)
                bill.save()
                lib_of_bills.bills.add(bill)
                lib_of_bills.save()
                cart.products.clear()
                cart.save()

                # Add fail_silently=True when testing
                messages.success(request,
                                 "Your payment has been processed successfully. Please check your email for "
                                 "payment details, you can also download the bill.", fail_silently=True)

                subject = 'Alejandria, Thank you for buying through our website'
                msg = 'Dear ' + request.user.username + ",\nThank you for buying through our website. \nHere you" \
                                                        " will find a copy with the details of your purchase." \
                                                        "\nRemember that you can also find all your bills in your " \
                                                        "profile on our website. " \
                                                        "\n\n Name: " + bill.name + "\n Date: " + str(bill.date) + "\n" \
                                                        " Total: " + str(total) + "€" + "\n\nAlejandria Team."

                send_mail(subject, msg, EMAIL_HOST_USER, [request.user.email], fail_silently=True)

                return HttpResponseRedirect('/')
        else:
            messages.error(request, "You can't complete the purchase, you haven't enough money!")

    return HttpResponseRedirect('/payment')


def draw_my_ruler(pdf):
    pdf.drawString(100, 810, 'x100')
    pdf.drawString(200, 810, 'x200')
    pdf.drawString(300, 810, 'x300')
    pdf.drawString(400, 810, 'x400')
    pdf.drawString(500, 810, 'x500')

    pdf.drawString(10, 100, 'y100')
    pdf.drawString(10, 200, 'y200')
    pdf.drawString(10, 300, 'y300')
    pdf.drawString(10, 400, 'y400')
    pdf.drawString(10, 500, 'y500')
    pdf.drawString(10, 600, 'y600')
    pdf.drawString(10, 700, 'y700')
    pdf.drawString(10, 800, 'y800')


def generate_pdf(request):
    user = request.user or None

    if user:

        user_bills = LibraryBills.objects.get(user_id=user)
        user_bill = user_bills.bills.filter(user_id=user).last()

        products = user_bill.products.all()

        products_titles = [p.ISBN.title for p in products]

        # Content
        filename = 'Expenses.pdf'
        document_title = 'Expenses'
        title = 'Alejanria'
        subtitle = 'Thank you for buying through our website!'

        text_lines = [
            'Username: ' + str(User.objects.filter(id=user.id).first().username),
            'Name: ' + user_bill.name,
            'Date: ' + str(user_bill.date),
            'Total: ' + str(user_bill.total_money_spent) + '€',
            'Products: ' + ', '.join(products_titles)
        ]

        # Make your response and prep to attach
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        tmp = BytesIO()

        # Create pdf
        pdf = canvas.Canvas(tmp)

        # Set title
        pdf.setFillColorRGB(0, 0, 255)
        pdf.setTitle(document_title)
        pdf.drawCentredString(300, 770, title)
        pdf.setFont('Courier-Bold', 36)
        # self.draw_my_ruler(pdf)

        # Set subtitle
        pdf.setFont('Courier', 24)
        pdf.drawCentredString(290, 720, subtitle)

        # Set line
        pdf.line(30, 710, 550, 710)

        # Set body text
        text = pdf.beginText(40, 680)
        text.setFont('Courier', 18)
        # pdf.setFillColor(colors.red)
        for line in text_lines:
            text.textLine(line)
        pdf.drawText(text)

        # Draw image
        # pdf.drawInlineImage(image, 130, 400)

        # Save changes
        pdf.showPage()
        pdf.save()

        # Get the data out and close the buffer cleanly
        pdf = tmp.getvalue()
        tmp.close()

        # Get StringIO's body and write it out to the response.
        response.write(pdf)
        return response
