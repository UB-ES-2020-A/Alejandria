import re
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden
from django.views import generic
import random

from Alejandria.settings import EMAIL_HOST_USER

from .forms import BookForm, UpdateBookForm
from .models import Book, FAQ, Cart, Product, User, Address, Rating, ResetMails, Guest


# Create your views here.

"""
This is my custom response to get to a book by it's ISBN. The ISBN is passed by the front in an AJAX
"""

NUM_COINCIDENT = 10
NUM_RELATED = 5
MONTHS_TO_CONSIDER_TOP_SELLER = 6


#
# def book(request):  # TODO: this function is not linked to the frontend
#     if request.method == 'GET' and request['']:
#         try:
#             req_book = get_object_or_404(Book, pk=request.GET['ISBN'])  # I get ISBN set in frontend form ajax
#         except(KeyError, Book.DoesNotExist):
#             return render(request, 'search.html', {  # TODO: Provisional
#                 'error_message': 'Alejandria can not find this book.'
#             })
#         else:
#             return render(request, 'details.html', {'book': req_book})
#
#     elif request.method == 'POST':
#         """
#         Here we can treat different situations,
#             Is it an admin, who wants to add a book?
#             Is it an editor?
#             What information do we need?
#         """
#         # TODO: Treat POST methods to save new Books
#         return render(request, 'search.html', {'error_message': 'Not Implemented Yet'})  # TODO: Provisional
#
#
# # This one works in theory when using the url with the pk inside # TODO: The idea is to use something like that
# def book_pk(request, pk):
#     req_book = get_object_or_404(Book, pk=pk)
#     return render(request, 'details.html', {'book': req_book})


# This one is the same but uses a generic Model, lso should work with the primary key
class BookView(generic.DetailView):
    model = Book
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        relation_book = Book.objects.filter(primary_genre=context['object'].primary_genre)[:20]

        if relation_book:
            context['book_relation'] = relation_book
        else:
            context['book_relation'] = Book.objects.all()[:20]

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
        today = datetime.today()
        # context['new_books'] = Book.objects.filter(
        #    publication_date__range=[str(today)[:10], str(today - timedelta(days=10))[:10]])[:10]
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

    def generate_id(self):
        temp = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
        list_id = [str(random.randint(0, 16)) if character == 'x' else character for character in temp]
        id = "".join(list_id)
        print('ID', id)
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
                |  Q(secondary_genre__in=self.genres_preferences)))

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
    user_id = request.user.id or None
    print(request.GET)
    if user_id:
        cart = Cart.objects.get(user_id=user_id)
    else:
        device = request.COOKIES['device']
        user, created = Guest.objects.get_or_create(device=device)
        cart, created = Cart.objects.get_or_create(guest_id=user)

    product = cart.products.get(ID=product_id)
    print("DELETE BOOK ", product)
    cart.products.remove(product)
    cart.save()
    return HttpResponseRedirect('/cart')


def add_product(request, view, book):
    user_id = request.user.id or None
    print(request.POST)
    if user_id:
        cart = Cart.objects.get(user_id=user_id)
    else:
        device = request.COOKIES['device']
        user, created = Guest.objects.get_or_create(device=device)
        cart, created = Cart.objects.get_or_create(guest_id=user)
        print('Cart', cart)

    products = Product.objects.all()
    print(products)
    for product in products:
        print('product it: ', product.ISBN.ISBN)
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
        context['list_query'] = dict(zip(_range, [FAQ.objects.filter(category='DWLDBOOK'),
                                                  FAQ.objects.filter(category='DEVOL'),
                                                  FAQ.objects.filter(category='SELL'),
                                                  FAQ.objects.filter(category='FACTU'),
                                                  FAQ.objects.filter(category='CONTACT')]))

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
    def validate_register(data):
        # No Blank Data
        data_answered = all([len(data[key]) > 0 for key in data if 'taste' not in key])
        exists = User.objects.filter(email=request.POST["email"]).exists()
        validation = data_answered and not exists
        return validation

    def encode_genre(taste):

        genres = {
            'Fantasy': 'FANT',
            'Crime & Thriller': 'CRIM',
            'Fiction': 'FICT',
            'Science Fiction': 'SCFI',
            'Horror': 'HORR',
            'Romance': 'ROMA',
            'Teen & Young Adult': 'TEEN',
            "Children's Books": 'KIDS',
            'Anime & Manga': 'ANIM',
            'Others': 'OTHR',
            'Art': 'ARTS',
            'Biography': 'BIOG',
            'Food': 'FOOD',
            'History': 'HIST',
            'Dictionary': 'DICT',
            'Health': 'HEAL',
            'Humor': 'HUMO',
            'Sport': 'SPOR',
            'Travel': 'TRAV',
            'Poetry': 'POET'
        }

        return genres[taste]

    if request.method == 'POST':
        if 'trigger' in request.POST and 'register' in request.POST['trigger']:
            if validate_register(request.POST):
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
                device = request.COOKIES['device']
                guest = Guest.objects.get(device=device)
                cart_guest = Cart.objects.get(guest_id=guest)
                cart_user = Cart(user_id=user)
                cart_user.save()
                cart_user = Cart.objects.get(user_id=user)
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

                # Update cart
                device = request.COOKIES['device']
                guest = Guest.objects.get(device=device)
                cart_guest = Cart.objects.get(guest_id=guest)
                cart_user = Cart.objects.get(user_id=user)
                for product in cart_guest.products.all():
                    cart_user.products.add(product)
                cart_guest.products.clear()
                cart_guest.save()
                cart_user.save()

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
class PaymentView(generic.ListView):
    # model = Account
    template_name = 'payment.html'
    context_object_name = 'cart_list'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None

    def get_queryset(self):
        request = self.request
        print(request.GET)
        self.user_id = request.user.id or None
        print("GEEEET PAYMENTTTTTTT", self.user_id)
        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
            print(cart)
            if cart:
                return cart.products.all()
        return None

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
            products = cart.products.all()
            total_price = 0
            items = len(products)
            for prod in products:
                print(prod.price)
                total_price += prod.price
            print("TOTAL_PRICE PAYMENT", total_price)
            context['total_price'] = total_price
            context['total_items'] = items
        else:
            context['total_items'] = 0

        return context


class EditorLibrary(PermissionRequiredMixin, generic.ListView):
    model = Book
    template_name = 'editor_library.html'  # TODO: Provisional file
    context_object_name = 'coincident'
    permission_required = ('books.add_book',)
    #permission_required = 'Alejandria.view_book'

    def __init__(self):
        super().__init__()
        self.editorBooks = None
        self.user_id = None

    def get(self, request, *args, **kwargs):
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
