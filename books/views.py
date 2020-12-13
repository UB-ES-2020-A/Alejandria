import random
import re
from datetime import datetime, timedelta, date
from io import BytesIO

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from reportlab.pdfgen import canvas

from Alejandria.settings import EMAIL_HOST_USER

from .utils import *
from .forms import BookForm, UpdateBookForm, BookPropertiesForm, CuponForm
from .models import Book, FAQ, Cart, User, Address, ResetMails, Guest, BankAccount, Bill, LibraryBills, Rating, \
    BookProperties, Cupon

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
    pk_url_kwarg = 'pk'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        relation_book = Book.objects.filter(primary_genre=self.object.primary_genre)[:20]
        context['isbn'] = str(self.object.ISBN)
        review_list = Rating.objects.filter(ISBN=self.object)
        book = get_object_or_404(Book, pk=self.kwargs['pk'])

        if self.request.user.is_authenticated:
            properties, created = BookProperties.objects.get_or_create(book=book, user=self.request.user)
            context['form'] = properties

        relation_book = Book.objects.filter(primary_genre=context['object'].primary_genre)[:20]
        context['isbn'] = str(context['object'].ISBN)
        review_list = Rating.objects.filter(ISBN=context['object'])

        if self.request.user.id:
            owned = Book.objects.filter(bill__in=Bill.objects.filter(user_id=self.request.user)).filter(ISBN=book.ISBN)#.filter(ISBN=book) # TODO: NEED TO FIX THIS
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

        if self.object.discount:
            new_price = self.object.price - (self.object.discount * self.object.price / 100)
            context['new_price'] = new_price

        return context


    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            if 'kwargs' in kwargs:
                book = get_object_or_404(Book, pk=kwargs['kwargs'])
            else:
                book = get_object_or_404(Book, pk=self.kwargs['pk'])
            properties, created = BookProperties.objects.get_or_create(book=book, user=request.user)

            pre_desired = properties.desired
            pre_readed = properties.readed

            change = None
            value = None

            if 'readed' in request.POST:
                change = 'readed'
                aux = request.POST['readed']
                if aux == 'on':
                    if pre_readed:
                        value = False
                    else:
                        value = True

            if 'desired' in request.POST:
                change = 'desired'
                aux = request.POST['desired']
                if aux == 'on':
                    if pre_desired:
                        value = False
                    else:
                        value = True

            form = BookPropertiesForm(request.POST, instance=properties)

            if form.is_valid():
                book_properties = form.save(commit=False)
                # intern fields (not showed to user)
                if change == 'desired':
                    book_properties.desired = value
                    book_properties.readed = pre_readed
                elif change == 'readed':
                    book_properties.readed = value
                    book_properties.desired = pre_desired

                book_properties.user = request.user
                if 'kwargs' in kwargs:
                    book_properties.book = get_object_or_404(Book, pk=kwargs['kwargs'])
                else:
                    book_properties.book = get_object_or_404(Book, pk=kwargs['pk'])

                if not 'kwargs' in kwargs:
                    messages.info(request, 'Your preference has been saved!')
                book_properties.save()
            else:
                if not 'kwargs' in kwargs:
                    messages.info(request, 'Oops.. something is wrong')

        context = {}
        context['book'] = book_properties.book
        context['form'] = book_properties

        if self.request.user.id is not None:
            owned = Book.objects.filter(bill__in=Bill.objects.filter(user_id=self.request.user)).filter(ISBN=context['book']).first() # TODO: NEED TO FIX THIS
            if owned:
                context['owned'] = "true"

        if 'owned' not in context.keys():
            context['owned'] = 'false'

        return render(request, "details.html", context)

    def render_to_response(self, context, **response_kwargs):
        response = super(BookView, self).render_to_response(context, **response_kwargs)
        cart = get_cart(self.request.user.id, self.request, response)
        if cart is not None:
            context['total_items'] = len(cart.books.all())
        else:
            context['total_items'] = 0
        return response



def generate_id():
    temp = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    list_id = [str(random.randint(0, 16)) if character == 'x' else character for character in temp]
    id = "".join(list_id)
    return id


def get_cart(user_id, request, response=None):
    if user_id:
        cart = Cart.objects.get(user_id=user_id)
    else:
        device = request.COOKIES.get('device')
        if not device and response is not None:
            device = generate_id()
            response.set_cookie('device', device)

        user, created = Guest.objects.get_or_create(device=device)
        cart, created = Cart.objects.get_or_create(guest_id=user)

    if cart is not None:
        return cart
    return None


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

        next_day = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")

        context['recent'] = Book.objects.filter(publication_date__range=[last_day, today])[:20]
        context['comingsoon'] = Book.objects.filter(publication_date__range=[today, next_day])[:20]
        context['fantasy'] = Book.objects.filter(primary_genre__contains="FANT")[:20]
        context['crime'] = Book.objects.filter(primary_genre__contains="CRIM")[:20]
        context['anime'] = Book.objects.filter(primary_genre__contains="ANIM")[:20]
        context['fiction'] = Book.objects.filter(primary_genre__contains="FICT")[:20]
        context['romance'] = Book.objects.filter(primary_genre__contains="ROMA")[:20]
        context['horror'] = Book.objects.filter(primary_genre__contains="HORR")[:20]

        the_user = self.request.user
        if not 'AnonymousUser' in str(the_user):
            properties = BookProperties.objects.filter(user = the_user)
            print(properties)
            recently_readed = [prop.book for prop in properties if prop.readed][:10]
            print("reacently readed: ", recently_readed)
            readed_sagas = list(set([book.saga for book in recently_readed]))
            readed_genres = list(set([book.primary_genre for book in recently_readed] +  [book.secondary_genre for book in recently_readed] ))
            
            recommended_books = Book.objects.filter(
                (Q(saga__in=readed_sagas)
                 | Q(primary_genre__in=readed_genres))
                 | Q(secondary_genre__in=readed_genres)
                )

            recommended_books_list = [book for book in recommended_books if book not in recently_readed]
            print("Recommended:", recommended_books_list)
            recommended_books_list = random.sample(recommended_books_list, min(len(recommended_books_list), 20))
            context['recommended'] = recommended_books_list

        promotions_books = Book.objects.filter(~Q(discount=0))
        context['promotion_books'] = promotions_books[:20]


        context['recent'] = Book.objects.filter(publication_date__range=[last_day, today])
        context['fantasy'] = Book.objects.filter(primary_genre__contains="FANT")
        context['crime'] = Book.objects.filter(primary_genre__contains="CRIM")
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(HomeView, self).render_to_response(context, **response_kwargs)
        cart = get_cart(self.user_id, self.request, response)
        if cart is not None:
            context['total_items'] = len(cart.books.all())
        else:
            context['total_items'] = 0
        return response


class SearchView(generic.ListView):
    model = Book
    template_name = 'search.html'
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
        #self.user_id = self.request.user.id or None
        self.user_id = request.user
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
        cart = get_cart(self.user_id, self.request)
        if cart is not None:
            context['total_items'] = len(cart.books.all())
        else:
            context['total_items'] = 0

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
            promotions_books = Book.objects.filter(~Q(discount=0))
            context['promotion_books'] = promotions_books[:20]
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
                if not request.test:
                    messages.info(request, 'Your book has been created successfully!')

                book.save()
                return HttpResponseRedirect('/editor')
            else:
                if not request.test:
                    messages.info(request, 'Oops.. something is wrong')
                form = BookForm()
                return render(request, "sell.html", {"form": form})


class EditBookView(PermissionRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'edit_book.html'
    permission_required = ('books.add_book',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # format data to suit frontend requirements
        if context.get('book').publication_date:
            context['date'] = context.get('book').publication_date.strftime("%Y-%m-%d")
        context['promos'] = Cupon.objects.filter(Q(book=context.get('book').ISBN))
        return context

    # post (update) of book
    def post(self, request, *args, **kwargs):

        if 'delete_promo' in request.POST:
            book = get_object_or_404(Book, pk=self.kwargs['pk'])
            promo = get_object_or_404(Cupon, pk=request.POST['delete_promo'])
            promo.delete()
            context = {}
            context['book'] = book
            context['date'] = context['book'].publication_date.strftime("%Y-%m-%d")
            context['promos'] = Cupon.objects.filter(Q(book=context['book'].ISBN))
            return render(request, "edit_book.html", context)

        elif "promo_form" in request.POST:
            if request.method == 'POST':
                # get the instance to modify
                book = get_object_or_404(Book, pk=self.kwargs['pk'])
                promo_form = CuponForm(request.POST)
                book_form = UpdateBookForm(request.POST, instance=book)
                if promo_form.is_valid():
                    promotion = promo_form.save(commit=False)
                    # intern field (not shown to user)
                    promotion.book = book
                    promotion.redeemed = 0

                    if not 'test' in request.POST:
                        messages.info(request, 'Promo code added successfully!')
                    promotion.save()
                else:
                    if not 'test' in request.POST:
                        messages.error(request, 'Oops.. something is wrong')
            else:
                promo_form = CuponForm()

            context = {}
            context['promo_form'] = promo_form
            context['book'] = book
            context['date'] = context['book'].publication_date.strftime("%Y-%m-%d")
            context['promos'] = Cupon.objects.filter(Q(book=context['book'].ISBN))

            return render(request, "edit_book.html", context)

        else:
            print(self.kwargs)
            print(request)
            if request.method == 'POST':
                # get the instance to modify
                s = get_object_or_404(Book, pk=self.kwargs['pk'])
                form = UpdateBookForm(request.POST, instance=s)
                if form.is_valid():
                    book = form.save(commit=False)
                    # intern field (not shown to user)
                    book.user_id = request.user

                    if not 'testing' in self.kwargs:
                        messages.info(request, 'Your book has been updated successfully!')
                    book.save()
                    return HttpResponseRedirect('/editor')
                else:
                    if not 'testing' in self.kwargs:
                        messages.info(request, 'Oops.. something is wrong')
                    book = get_object_or_404(Book, pk=self.kwargs['pk'])
                    context = {}
                    context['form'] = form
                    context['book'] = book
                    context['date'] = context['book'].publication_date.strftime("%Y-%m-%d")
                    context['promos'] = Cupon.objects.filter(Q(book=context['book'].ISBN))
                    return render(request, "edit_book.html", context)


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
        self.user_id = self.request.user.id
        cart = get_cart(self.user_id, self.request)
        if cart is not None:
            return cart.books.all()
        print("CART DON'T EXIST")
        return []

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['books_from_cart_view'] = Book.objects.all()[:6]
        context['books_from_cart_view_1'] = Book.objects.all()[:3]
        context['books_from_cart_view_2'] = Book.objects.all()[3:6]
        context['books_from_cart_view_3'] = Book.objects.all()[6:9]
        cart = get_cart(self.user_id, self.request)
        books = cart.books.all()
        total_price = 0
        for book in books:
            total_price += book.price
        context['total_price'] = total_price
        context['total_items'] = len(books)
        return context


def delete_product(request, book):
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

    print("DELETE BOOK ", book)
    cart.books.remove(book)
    cart.save()
    print("CART: ", cart.books.all())
    return HttpResponseRedirect('/cart')


def add_product(request, view, book):
    user = request.user or None
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

    print("ADD BOOK ", book)
    cart.books.add(book)
    cart.save()

    if view == 'home':
        return HttpResponseRedirect('/')
    if view == 'cart':
        return HttpResponseRedirect('/cart')
    if view == 'details':
        return HttpResponseRedirect('/book/'+book)


class FaqsView(generic.ListView):
    model = FAQ
    template_name = 'faqs.html'
    context_object_name = 'faqs'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None

    def get_queryset(self):
        self.user_id = self.request.user.id
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
        the_user = self.request.user
        if 'AnonymousUser' in str(the_user):
            context['admin'] = False
        else:
            context['admin'] = self.request.user.role in 'Admin'

        cart = get_cart(self.user_id, self.request)
        context['total_items'] = len(cart.books.all())

        return context

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

                try:
                    fact_address.clean()
                    user_address.clean()
                    user.full_clean()

                except ValidationError:
                    # Do something when validation is not passing
                    print("ERROR VALIDATION REGISTER")
                    fact_address.delete()
                    user_address.delete()
                    user.delete()
                    return JsonResponse({"error": True})

                else:
                    # Create user's cart
                    device = request.COOKIES.get('device')
                    guest, created = Guest.objects.get_or_create(device=device)
                    cart_user, created = Cart.objects.get_or_create(user_id=user)
                    if device:
                        cart_guest_query = Cart.objects.filter(guest_id=guest)
                        if cart_guest_query.count() != 0:
                            cart_guest = cart_guest_query.first()
                            for book in cart_guest.books.all():
                                cart_user.books.add(book)
                            cart_guest.books.clear()
                            cart_guest.save()
                            cart_user.save()

                    return JsonResponse({"error": False})

            else:
                return JsonResponse({"error": True})

        return JsonResponse({"error": True})


@csrf_exempt
def post_avatar(request):
    if 'trigger' in request.POST and 'avatar' in request.POST['trigger']:
        file = request.FILES.get("avatar")
        if file is not None:
            if request.user.is_authenticated:
                user = request.user
            else:
                user = request.POST["username"]
                user = User.objects.filter(username=user).first()

            user.avatar.save(file.name, file)
            return JsonResponse({"error": False})
    return JsonResponse({"error": True})


def check_data(request):
    if request.method == 'POST':
        if 'username' in request.POST:
            username = request.POST["username"]
            return JsonResponse({"exists": User.objects.filter(username=username).exists()})
        if 'email' in request.POST:
            email = request.POST["email"]
            return JsonResponse({"exists": User.objects.filter(email=email).exists()})


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
                                         "msg": "Reset mail was sent to " + recipient + " successfully. Please check your inbox.",
                                         "id": last})
                except:
                    return JsonResponse({"error": True, "msg": "Your request failed, please try it again."})

            return JsonResponse({"error": True,
                                 "msg": "Invalid mail address"})


        elif 'trigger' in request.POST and request.POST['trigger'] == 'reset':
            try:
                if 'id' in kwargs:
                    reset_id = kwargs['id']
                elif 'id' in request.POST:
                    reset_id = request.POST['id']

                new_pass = request.POST['new_pass']
                user = ResetMails.objects.filter(id=int(reset_id)).first().user
                user.password = new_pass
                user.save()
                return JsonResponse({"error": False})
            except:
                return JsonResponse({"error": True})

    elif request.method == 'GET':
        if 'id' in kwargs:
            reset_id = kwargs['id']
        elif 'id' in request.GET:
            reset_id = request.GET['id']
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
    queryset = Book.objects.all()
    context_object_name = 'cart_list'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None
        self.username = ''
        self.card_number = ''
        self.total = 0
        self.year = None
        self.month = None
        self.cvv = None
        self.gifts = []

    def get_queryset(self):
        self.user_id = self.request.user.id
        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
            if cart:
                return cart.books.all()
        return None

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        if self.user_id:
            cart = Cart.objects.get(user_id=self.user_id)
            user_bank_account = BankAccount.objects.filter(user_id=self.user_id).first() or None
            books = cart.books.all()
            total_price = 0
            for book in books:
                total_price += book.price
            context['total_price'] = total_price
            context['total_items'] = len(books)
            if user_bank_account is not None:
                context['card_owner'] = self.username
                context['card_number'] = self.card_number
                context['month'] = self.month
                context['year'] = self.year
                context['cvv'] = self.cvv
        else:
            context['total_items'] = 0

        return context

    def post(self, request, *args, **kwargs):
        for a in request.POST:
            self.gifts.append((a, request.POST[a]))

        request.session['gifts'] = self.gifts
        print(request.session['gifts'])
        return JsonResponse({'message': 'ok'})


class EditorLibrary(PermissionRequiredMixin, generic.ListView):
    model = Book
    template_name = 'editor_library.html'
    context_object_name = 'coincident'
    permission_required = ('books.add_book',)

    # permission_required = 'Alejandria.view_book'

    def __init__(self):
        super().__init__()
        self.editorBooks = None
        self.user_id = None

    def get(self, request, *args, **kwargs):
        print(request.GET)
        self.user_id = self.request.user.id

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
                if request.POST["taste1"] and request.POST["taste1"] != "None":
                    genre_preference_1 = encode_genre(request.POST["taste1"])

                if request.POST["taste2"] and request.POST["taste2"] != "None":
                    genre_preference_2 = encode_genre(request.POST["taste2"])

                if request.POST["taste3"] and request.POST["taste3"] != "None":
                    genre_preference_3 = encode_genre(request.POST["taste3"])

                # Apply changes
                user.username = request.POST["username"]
                user.email = request.POST["email"]
                user.user_address = user_address
                user.fact_address = fact_address
                user.name = first_name
                user.first_name = first_name
                user.last_name = last_name

                if request.POST["taste1"] != "None":
                    user.genre_preference_1 = genre_preference_1
                if request.POST["taste2"] != "None":
                    user.genre_preference_2 = genre_preference_2
                if request.POST["taste3"] != "None":
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
            context = {
                'total_items': len(cart.books.all())
            }
        else:
            context = {}
        return render(request, "view_profile.html", context)


def complete_purchase(request):
    print(request.POST)
    user = request.user.id or None
    if user:
        user_bank_account, created = BankAccount.objects.get_or_create(user_id=user)
        current_money = float(user_bank_account.money)
        cart = Cart.objects.get(user_id=user)
        books = cart.books.all()
        total = 0
        coupons = []

        for i in range(int(request.POST.get('redeemed_codes'))):
            coupon = Cupon.objects.filter(code=request.POST.get('code'+str(i))).first()
            if coupon:
                coupons.append(coupon)

        for book in books:
            total += book.price

            for coupon in coupons:
                if coupon.book == book:
                    total -= book.price * coupon.percentage/100


        total = float(total)

        print(total)

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
                setattr(bill, 'total_money_spent', total)
                setattr(bill, 'payment_method', 'Credit card')
                setattr(bill, 'name', user_bank_account.name)
                gifted_books = []
                if 'gifts' in request.session:
                    gifted_books = [gift[0] for gift in request.session['gifts']]
                for book in books:
                    if book.ISBN not in gifted_books:
                        print(book.ISBN)
                        print("lol")
                        book.num_sold += 1
                        book.save()
                        bill.books.add(book)
                bill.save()
                lib_of_bills, created = LibraryBills.objects.get_or_create(user_id=request.user)
                lib_of_bills.bills.add(bill)
                lib_of_bills.save()

                subject = 'Alejandria, Thank you for buying through our website'
                msg = 'Dear ' + request.user.username + ",\nThank you for buying through our website. \nHere you" \
                                                        " will find a copy with the details of your purchase." \
                                                        "\nRemember that you can also find all your bills in your " \
                                                        "profile on our website. " \
                                                        "\n\n Name: " + bill.name + "\n Date: " + str(bill.date) + "\n" \
                                                        " Total: " + str(total) + "€" + "\n\nAlejandria Team."

                send_mail(subject, msg, EMAIL_HOST_USER, [request.user.email], fail_silently=True)

                for i in range(len(gifted_books)):
                    print("Gifting book...")
                    gifted_user = User.objects.filter(username=request.session['gifts'][i][1]).first()
                    book = Book.objects.filter(ISBN=request.session['gifts'][i][0]).first()
                    new_bill = Bill(user_id_id=gifted_user.id)
                    new_bill.save()
                    book.num_sold += 1
                    book.save()
                    new_bill.books.add(book)
                    new_bill.save()
                    lib_of_bills, created = LibraryBills.objects.get_or_create(user_id=gifted_user)
                    lib_of_bills.bills.add(bill)
                    lib_of_bills.save()
                    subject = 'Alejandria, Thank you for buying through our website'
                    msg = 'Dear ' + gifted_user.username + ",\nCongratulations, you got gifted a book by " + \
                                                            request.user.username + " you for buying through our website. \nHere you" \
                                                            " will find a copy with the details of your gift." \
                                                            "\nRemember that you can also find all your bills in your " \
                                                            "profile on our website. " \
                                                            "\n\n Name: " + new_bill.name + "\n Date: " + str(
                        bill.date) + "\n" \
                                     " Total: " + str(total) + "€" + "\n\nAlejandria Team."

                    send_mail(subject, msg, EMAIL_HOST_USER, [gifted_user.email], fail_silently=True)

                cart.books.clear()
                cart.save()

                # Add fail_silently=True when testing
                messages.success(request,
                                 "Your payment has been processed successfully. Please check your email for "
                                 "payment details, you can also download the bill.", fail_silently=True)

                return HttpResponseRedirect('/')
        else:
            messages.error(request, "You can't complete the purchase, you haven't enough money!")

    return HttpResponseRedirect('/payment')


def generate_pdf(request):
    user = request.user or None

    if user:

        user_bills = LibraryBills.objects.get(user_id=user)
        user_bill = user_bills.bills.filter(user_id=user).last()

        books = user_bill.books.all()

        books_price = [book.price for book in books]

        # Content
        filename = 'Expenses-' + str(user.id) + str(date.today()) + '.pdf'
        document_title = 'Expenses-' + str(user.id) + str(date.today())
        title = 'BOOK SALE INVOICE'
        subtitle = 'Thank you for buying through our website!'

        server_details_lines = [
            'Address:  Gran Via de les Corts Catalanes, 585, 08007 Barcelona',
            'Email: alejandria.books.2020@gmail.com',
            'Tlf: + 01 234 567 89'
        ]

        clients_details_lines = [
            'Name: ' + user.name + ' ' + user.last_name,
            'Email: ' + user.email,
            'Address: ' + user.fact_address.city + ', ' + user.fact_address.country + ', ' + user.fact_address.street,
            'Zip: ' + str(user.fact_address.zip),
            'Date: ' + str(user_bill.date)
        ]

        books_details_lines = [book.title + ' (' + book.ISBN + ')' for book in books]


        text_lines = [
            'Username: ' + str(User.objects.filter(id=user.id).first().username),
            'Name: ' + user_bill.name,
            'Date: ' + str(user_bill.date),
            'Total: ' + str(user_bill.total_money_spent) + '€'
        ]

        # Make your response and prep to attach
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        tmp = BytesIO()

        # Create pdf
        pdf = canvas.Canvas(tmp)

        # Set title
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setTitle(document_title)
        pdf.setFont('Courier-Bold', 20)
        pdf.drawCentredString(300, 770, title)
        #draw_my_ruler(pdf)

        # Set subtitle
        pdf.setFont('Courier', 12)
        pdf.drawCentredString(300, 750, subtitle)

        # Set rect
        pdf.rect(30, 690, 535, 30, fill=1)

        # Set section: Alejandria
        pdf.setFillColorRGB(255, 255, 255)
        pdf.setFont('Courier-Bold', 14)
        pdf.drawString(40, 700, 'ALEJANDRIA')

        # Set body text
        text = pdf.beginText(40, 670)
        text.setFont('Helvetica', 12)
        pdf.setFillColorRGB(0, 0, 0)
        for line in server_details_lines:
            text.textLine(line)
        pdf.drawText(text)

        # Set rect
        pdf.rect(30, 590, 535, 30, fill=1)

        # Set section: Client
        pdf.setFillColorRGB(255, 255, 255)
        pdf.setFont('Courier-Bold', 14)
        pdf.drawString(40, 600, 'CLIENT DETAILS')

        # Set body text
        text = pdf.beginText(40, 570)
        text.setFont('Helvetica', 12)
        pdf.setFillColorRGB(0, 0, 0)
        for line in clients_details_lines:
            text.textLine(line)
        pdf.drawText(text)

        # Set rect
        pdf.rect(30, 466, 535, 30, fill=1)

        # Set section: Books
        pdf.setFillColorRGB(255, 255, 255)
        pdf.setFont('Courier-Bold', 14)
        pdf.drawString(40, 476, 'BOOKS')

        # Set body text
        text = pdf.beginText(40, 446)
        text.setFont('Helvetica', 12)
        pdf.setFillColorRGB(0, 0, 0)
        for line in books_details_lines:
            text.textLine(line)
        pdf.drawText(text)

        # Set body text
        text = pdf.beginText(520, 446)
        text.setFont('Helvetica', 12)
        pdf.setFillColorRGB(0, 0, 0)
        for line in books_price:
            text.textLine(str(line) + ' €')
        pdf.drawText(text)

        # Set Line
        pdf.line(40, 446 - 12*len(books_price) - 5, 560, 446 - 12*len(books_price) - 5)

        # Write Total
        pdf.drawString(40, 446 - 12*len(books_price) - 20, 'Total')
        pdf.drawString(520, 446 - 12*len(books_price) - 20, str(user_bill.total_money_spent) + ' €')

        # Write Copyright
        pdf.drawCentredString(330, 50, '© 2020 Copyright: Alejandria.com')

        # Save changes
        pdf.showPage()
        pdf.save()

        # Get the data out and close the buffer cleanly
        pdf = tmp.getvalue()
        tmp.close()

        # Get StringIO's body and write it out to the response.
        response.write(pdf)
        return response


class UserLibrary(generic.ListView): #PermissionRequiredMixin
    model = Book
    template_name = 'user_library.html'
    context_object_name = 'coincident'
    # permission_required = ('books.add_book',)

    # permission_required = 'Alejandria.view_book'

    def __init__(self):
        super().__init__()
        self.userBooks = None
        self.user_id = None

    def get(self, request, *args, **kwargs):
        self.user_id = self.request.user.id
        print(request.GET)

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
        user_books = Book.objects.filter(bill__in=Bill.objects.filter(user_id=self.request.user.id))
        context['user_prod'] = user_books

        return context


class UserBills(generic.ListView): #PermissionRequiredMixin
    model = Book
    template_name = 'user_bills.html'
    context_object_name = 'coincident'
    # permission_required = ('books.add_book',)

    # permission_required = 'Alejandria.view_book'

    def __init__(self):
        super().__init__()
        self.user_id = None

    def get(self, request, *args, **kwargs):
        print(request.GET)
        self.user_id = self.request.user.id
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):  # TODO: Test
        context = super().get_context_data(**kwargs)

        # Filtering by title or author
        user_bills = LibraryBills.objects.get(user_id=self.user_id)
        context['user_bills'] = user_bills.bills.all()
        print(user_bills.bills.all())

        return context


def check_promo_code(request, **kwargs):
    if request.method == 'GET':
        coupon = Cupon.objects.filter(code=kwargs['code']).first()
        if not coupon:
            return JsonResponse({'error': 'The coupon does not exist.'}, status=404)

        if coupon.redeemed >= coupon.max_limit:
            return JsonResponse({'error': 'The coupon has already been redeemed.'}, status=404)

        dic = {}
        books = Cart.objects.filter(user_id=request.user).first().books.all()
        for book in books:
            if coupon.book == book:
                dic[book.ISBN] = book.price - book.price * coupon.percentage / 100

        if dic == {}:
            return JsonResponse({'error': 'The coupon introduced does not apply to any book in your cart.'}, status=404)

        return JsonResponse(dic)


def addfaq(request):
    the_user = request.user
    response = HttpResponse()
    if 'AnonymousUser' in str(the_user):
        return HttpResponseForbidden('You have to be an admin to do that')
    else:
        admin = request.user.role in 'Admin'
        if admin:
            category = request.POST.get('category')
            question = request.POST.get('question')
            answer = request.POST.get('answer')

            try:
                category = [cat[0] for cat in FAQ.FAQ_CHOICES if category in cat][0]
            except:
                return HttpResponseForbidden('Select a valid category')

            try:
                faq = FAQ(category=category, question=question, answer=answer)
                faq.save()
            except:
                return HttpResponseForbidden('Something went wrong')
        else:
            return HttpResponseForbidden('You have to be an admin to do that')
    return response

def modifyfaq(request):
    the_user = request.user
    response = HttpResponse()
    if 'AnonymousUser' in str(the_user):
        return HttpResponseForbidden('You have to be an admin to do that')
    else:
        admin = request.user.role in 'Admin'
        if admin:
            original = request.POST.get('original')
            category = request.POST.get('category')
            question = request.POST.get('question')
            answer = request.POST.get('answer')

            try:
                category = [cat[0] for cat in FAQ.FAQ_CHOICES if category in cat][0]
            except:
                return HttpResponseForbidden('Select a valid category')

            original_faq = FAQ.objects.filter(question=original)

            if original_faq:
                try:
                    original_faq.update(category=category, question=question, answer=answer)
                except:
                    return HttpResponseForbidden('Something went wrong')
            else:
                return HttpResponseForbidden('This FAQ does not exist')
        else:
            return HttpResponseForbidden('You have to be an admin to do that')
    return response


def deletefaq(request):
    the_user = request.user
    response = HttpResponse()
    if 'AnonymousUser' in str(the_user):
        return HttpResponseForbidden('You have to be an admin to do that')
    else:
        admin = request.user.role in 'Admin'
        if admin:
            original = request.POST.get('original')

            original_faq = FAQ.objects.filter(question=original)

            if original_faq:
                try:
                    original_faq.delete()
                except:
                    return HttpResponseForbidden('Something went wrong')
            else:
                return HttpResponseNotFound('This FAQ does not exist')
        else:
            return HttpResponseForbidden('You have to be an admin to do that')
    return response


class DesiredLibrary(generic.ListView): #PermissionRequiredMixin
    model = Book
    template_name = 'desired_library.html'

    def __init__(self):
        super().__init__()
        self.user = None

    def get(self, request, *args, **kwargs):
        #self.user_id = self.request.user.id
        self.user = request.user
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):  # TODO: Test
        context = super().get_context_data(**kwargs)

        desired_books = BookProperties.objects.filter(Q(user=self.user) & (Q(desired=True)))
        desired_list = []
        for desired in desired_books:
            new_price = desired.book.price - (desired.book.discount * desired.book.price / 100)
            desired_list.append((desired.book,new_price))

        context['desired_books'] = desired_list

        return context


def checkUsernameGift(request, **kwargs):
    if request.method == 'GET':
        user = User.objects.filter(username=kwargs['username']).first()
        book = Book.objects.filter(ISBN=request.GET['isbn']).first()
        owned = Book.objects.filter(bill__in=Bill.objects.filter(user_id=user)).filter(ISBN=book.ISBN)
        if user:
            if user == request.user:
                return JsonResponse({'error': "You can't gift a book to yourself."}, status=403)

            if owned:
                return JsonResponse({'error': 'The user already owns the book.'}, status=404)

            return JsonResponse({'message': 'The user is eligible to receive this gift.'})

        return JsonResponse({'error': "The user doesn't exist."}, status=404)

def about_us(request):
    return render(request, "about_us.html")
