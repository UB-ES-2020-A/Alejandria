from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

"""
IF NECESSARY INTRODUCE help_text in some characteristics.
"""
GENRE_CHOICES = [
    ('FANT', 'Fantasy'),
    ('CRIM', 'Crime & Thriller'),
    ('FICT', 'Fiction'),
    ('SCFI', 'Science Fiction'),
    ('HORR', 'Horror'),
    ('ROMA', 'Romance'),
    ('TEEN', 'Teen & Young Adult'),
    ('KIDS', "Children's Books"),
    ('ANIM', 'Anime & Manga'),
    ('OTHR', 'Others'),
    ('ARTS', 'Art'),
    ('BIOG', 'Biography'),
    ('FOOD', 'Food'),
    ('HIST', 'History'),
    ('DICT', 'Dictionary'),
    ('HEAL', 'Health'),
    ('HUMO', 'Humor'),
    ('SPOR', 'Sport'),
    ('TRAV', 'Travel'),
    ('POET', 'Poetry')
]


class Address(models.Model):
    street = models.CharField(max_length=50, null=False, blank=False)
    city = models.CharField(validators=[RegexValidator(regex=r"^[A-Z][a-z]+$", message='Invalid city name.',
                                                       code='nomatch')], max_length=50, null=False, blank=False)
    country = models.CharField(validators=[RegexValidator(regex=r"^[A-Z][a-z]+$", message='Invalid country name.',
                                                          code='nomatch')], max_length=50, null=False, blank=False)
    zip = models.CharField(validators=[RegexValidator(regex=r"^[0-9]{4-7}$", message='Invalid zip. Must have 5 digits.',
                                                      code='nomatch')], max_length=10, null=False, blank=False)


class User(AbstractUser):
    id = models.AutoField(primary_key=True, null=False, blank=True)
    # TODO: ADD USERNAME AS A PK
    role = models.CharField(max_length=10, null=False, blank=False)
    name = models.CharField(validators=[RegexValidator(regex=r"^[A-Z][a-z ,.'-]+$", message='Invalid name.',
                                                       code='nomatch')], max_length=150, null=False, blank=False, default="user")
    password = models.CharField(validators=[RegexValidator(regex=r"^[A-Za-z0-9]{6,20}$", message='Invalid password.',
                                                           code='nomatch')], max_length=150, null=False, blank=False)
    email = models.EmailField(validators=[RegexValidator(regex=r"^[A-Za-z0-9](\.?[A-Za-z0-9]){5,}@g(oogle)?mail\.com$", message='Invalid email.',
                                                         code='nomatch')], max_length=150, null=False, blank=False)
    user_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True,
                                     related_name="user_address")
    fact_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True,
                                     related_name="fact_address")
    genre_preference_1 = models.CharField(max_length=4, choices=GENRE_CHOICES, blank=True, null=True)
    genre_preference_2 = models.CharField(max_length=4, choices=GENRE_CHOICES, null=True, blank=True)
    genre_preference_3 = models.CharField(max_length=4, choices=GENRE_CHOICES, null=True, blank=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatars/")


class Guest(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=True)
    device = models.CharField(max_length=200, null=False, blank=False)


# class Author(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#
#     def __eq__(self, other):
#         if isinstance(other, self.__class__):
#             return self.__dict__ == other.__dict__
#         else:
#             return False


class Book(models.Model):
    ISBN = models.CharField(primary_key=True, max_length=13, blank=False, null=False)  # Its a Char instead of Integer
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)  # Synopsis
    saga = models.CharField(max_length=100, blank=True, null=True)
    # authors = models.ManyToManyField(Author, max_length=10, blank=True, null=True,
    #                                  default=None)  # Un llibre pot tenir més d'un autor.
    author = models.CharField(max_length=50, default="Anonymous")
    # Has to be datetime.date
    # By default it's now.
    publication_date = models.DateField(null=True, blank=True, default=timezone.now)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    language = models.CharField(max_length=30, blank=False)
    primary_genre = models.CharField(max_length=4, choices=GENRE_CHOICES, default='OTHR')
    secondary_genre = models.CharField(max_length=4, choices=GENRE_CHOICES, null=True, blank=True)
    publisher = models.CharField(max_length=50)
    num_pages = models.IntegerField(blank=False)
    num_sold = models.IntegerField(default=0)
    recommended_age = models.CharField(max_length=30, blank=True,
                                       null=True)
    # Path to thumbnail(Thubnail identified by ISBN)
    thumbnail = models.ImageField(blank=True, null=True, upload_to="thumbnails/")  # TODO:Should be blank=False in the Future
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0, blank=True, null=True)
    eBook = models.FileField(blank=True, null=True, upload_to="ebooks/", default="/media/ebooks/download.pdf")
    # pub_date = publication_date  # Abreviation


class BookProperties(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False,
                             blank=False)
    desired = models.BooleanField(default=False)
    readed = models.BooleanField(default=False)


class Rating(models.Model):
    ID = models.AutoField(primary_key=True, blank=False, null=False)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False,
                                blank=False)
    text = models.TextField(max_length=500, null=False, blank=True)
    per_values = range(1, 6)
    human_readable = [str(value) for value in per_values]
    score = models.IntegerField(choices=zip(per_values, human_readable), null=False, blank=False)
    date = models.DateField(null=True, blank=True, default=timezone.now)


class Cupon(models.Model):
    code = models.CharField(primary_key=True, max_length=10, blank=False, null=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False)
    percentage = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], null=False)
    max_limit = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99999999)], null=True)
    redeemed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99999999)], null=True)


class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE, blank=False, null=True)
    books = models.ManyToManyField(Book)


class Bill(models.Model):
    num_bill = models.AutoField(primary_key=True, blank=False, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date = models.DateField(null=True, blank=True, default=timezone.now)
    payment_method = models.CharField(max_length=50)
    books = models.ManyToManyField(Book)
    total_money_spent = models.DecimalField(decimal_places=2, max_digits=8, null=True)


class LibraryBills(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    bills = models.ManyToManyField(Bill)


class FAQ(models.Model):
    # First object = Saved on the model, second object = Human readable one
    FAQ_CHOICES = [
        ('DWL', 'About our ebooks'),
        ('REF', 'Refund'),
        ('SEL', 'Sell your ebooks'),
        ('FAC', 'About bills and payment'),
        ('CON', 'Contact us'),
    ]

    ID = models.AutoField(primary_key=True)

    question = models.TextField(blank=False, null=False)
    answer = models.TextField(blank=False, null=False)
    category = models.CharField(blank=False, null=False, choices=FAQ_CHOICES, max_length=50)

    def __str__(self):
        return "ID:{}  CAT:{}   {} --- {}".format(self.ID, self.category, self.question, self.answer)


## TODO: If we decide to give the option to the admin to add the FAQ to a new category, categories shold be saved to the database
# class FAQchoices(models.Model):


class ResetMails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    activated = models.BooleanField(default=True)


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=100)
    money = models.DecimalField(decimal_places=2, max_digits=8, default=500.00)
    card_number = models.CharField(validators=[RegexValidator(regex=r'^[0-9]{16}$', message='Length has to be 16',
                                                              code='nomatch')], max_length=16, null=True)
    month_exp = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], null=True)
    year_exp = models.IntegerField(validators=[MinValueValidator(2020)], null=True)
    cvv = models.IntegerField(validators=[MinValueValidator(000), MaxValueValidator(9999)], null=True)  # 3 or 4 digits
