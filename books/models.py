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
    city = models.CharField(max_length=50, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False)
    zip = models.CharField(max_length=10, null=False, blank=False)


class User(AbstractUser):
    id = models.AutoField(primary_key=True, null=False, blank=True)
    # TODO: ADD USERNAME AS A PK
    role = models.CharField(max_length=10, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    password = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    user_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True,
                                     related_name="user_address")
    fact_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True,
                                     related_name="fact_address")
    genre_preference_1 = models.CharField(max_length=4, choices=GENRE_CHOICES, blank=True, null=True)
    genre_preference_2 = models.CharField(max_length=4, choices=GENRE_CHOICES, null=True, blank=True)
    genre_preference_3 = models.CharField(max_length=4, choices=GENRE_CHOICES, null=True, blank=True)


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
                                on_delete=models.CASCADE)  # Reference to the User that created it #TODO: on_delete=models.CASCADE
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
    language = models.CharField(max_length=30, blank=False)  # TODO: Might have choices=<<languages it can be>>
    primary_genre = models.CharField(max_length=4, choices=GENRE_CHOICES, default='OTHR')  # TODO: choices=<<all possible genres>>, also can have multiple choices
    secondary_genre = models.CharField(max_length=4, choices=GENRE_CHOICES, null=True, blank=True)
    publisher = models.CharField(max_length=50)
    num_pages = models.IntegerField(blank=False)
    num_sold = models.IntegerField(default=0)
    recommended_age = models.CharField(max_length=30, blank=True,
                                       null=True)  # TODO: choices=<<possible range recommendation>> example: Juvenile
    # Path to thumbnail(Thubnail identified by ISBN)
    thumbnail = models.ImageField(blank=True, null=True, upload_to="thumbnails/")  # TODO:Should be blank=False in the Future
    eBook = models.FileField(blank=True, null=True, upload_to="ebooks/")
    # pub_date = publication_date  # Abreviation


class Product(models.Model):
    ID = models.AutoField(primary_key=True)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE, blank=False, null=False)
    # TODO: What to do on_delete=?
    price = models.DecimalField(decimal_places=2, max_digits=8)
    # TODO: Could be in no.arange(0.00, 100.00, 0.01) -> To have percentages with 0.01 precision
    per_values = range(0, 101)
    human_readable = [str(value) for value in per_values]
    fees = models.DecimalField(decimal_places=2, max_digits=5, choices=zip(per_values, human_readable), default=21.0)
    discount = models.DecimalField(decimal_places=2, max_digits=5, choices=zip(per_values, human_readable), default=0.0)


class Rating(models.Model):
    ID = models.AutoField(primary_key=True, blank=False, null=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)  # TODO: on_delete
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False,
                                blank=False)  # TODO: on_delete
    text = models.TextField(max_length=500, null=False, blank=True)
    per_values = range(1, 6)
    human_readable = [str(value) for value in per_values]
    score = models.IntegerField(choices=zip(per_values, human_readable), null=False, blank=False)
    date = models.DateField(null=False, blank=False, default=timezone.now)


class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE, blank=False, null=True)
    products = models.ManyToManyField(Product)


class Bill(models.Model):
    num_bill = models.AutoField(primary_key=True, blank=False, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date = models.DateField(null=True, blank=True, default=timezone.now)
    payment_method = models.CharField(max_length=50)
    products = models.ManyToManyField(Product)
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
    card_number = models.CharField(validators=[RegexValidator(regex='^[0-9]{16}$', message='Length has to be 16',
                                                              code='nomatch')], max_length=16, null=True)
    month_exp = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], null=True)
    year_exp = models.IntegerField(validators=[MinValueValidator(2020)], null=True)
    cvv = models.IntegerField(validators=[MinValueValidator(000), MaxValueValidator(9999)], null=True)  # 3 or 4 digits
