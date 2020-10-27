from django.db import models

from django.utils import timezone

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class UserDummy(models.Model):  # TODO: Replace with the real User
    ID = models.IntegerField(primary_key=True, blank=False, null=False)


class Book(models.Model):
    ISBN = models.IntegerField(primary_key=True, blank=False, null=False)  # What about models.AutoField
    user_id = models.ForeignKey(UserDummy, on_delete=models.CASCADE)  # Reference to the User that created it #TODO: on_delete=models.CASCADE
    title = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=500, blank=True, null=True)  # Synopsis
    saga = models.CharField(max_length=30, blank=True, null=True)
    authors = models.ManyToManyField(Author, max_length=10, blank=True, null=True)  # Un llibre pot tenir més d'un autor.
    # Has to be datetime.date
    # By default it's now.
    publication_date = models.DateField(null=True, blank=True, default=timezone.now)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    language = models.CharField(max_length=15, blank=False)  # TODO: Might have choices=<<languages it can be>>
    genre = models.CharField(max_length=30, blank=False)  # TODO: choices=<<all possible genres>>, also can have multiple choices
    publisher = models.CharField(max_length=30)
    num_pages = models.IntegerField(blank=False)
    num_sold = models.IntegerField(default=0)
    recommended_age = models.CharField(max_length=30, blank=True, null=True)  #TODO: choices=<<possible range recommendation>> example: Juvenile
        # Path to thumbnail(Thubnail identified by ISBN)
    thumbnail = models.CharField(max_length=30)  # TODO:Should be blank=False in the Future

    #pub_date = publication_date  # Abreviation


class Product(models.Model):
    ID = models.IntegerField(primary_key=True)
    ISBN = models.OneToOneField(Book, on_delete=models.CASCADE, blank=False, null=False)
                                                            #TODO: What to do on_delete=?
    price = models.DecimalField(decimal_places=2, max_digits=8)
    # TODO: Could be in no.arange(0.00, 100.00, 0.01) -> To have percentages with 0.01 precision
    per_values = range(0,101)
    human_readable = [str(value) for value in per_values]
    fees = models.DecimalField(decimal_places=2, max_digits=5, choices=zip(per_values, human_readable))
    discount = models.DecimalField(decimal_places=2, max_digits=5, choices=zip(per_values, human_readable))


class Rating(models.Model):
    ID = models.IntegerField(primary_key=True, blank=False, null=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)  # TODO: on_delete
    user_id = models.ForeignKey(UserDummy, on_delete=models.CASCADE, null=False, blank=False)  # TODO: on_delete
    text = models.TextField(max_length=500,null=False, blank=True)
    per_values = range(1, 6)
    human_readable = [str(value) for value in per_values]
    score = models.IntegerField(choices=zip(per_values,human_readable), null=False, blank=False)
    date = models.DateField(null=False, blank=False, default=timezone.now)


class Bill(models.Model):
    num_factura = models.IntegerField(primary_key=True,blank=False,null=False)  #TODO: auto field
    products = models.ManyToManyField(Product)
    user_id = models.ForeignKey(UserDummy, on_delete=models.PROTECT)
    date = models.DateField(null=True, blank=True, default=timezone.now)
    seller_info = models.TextField(blank=True, null=False)  # TODO: This is provisional
    payment_method = models.CharField(max_length=30) # TODO: Define choices.


class FAQ(models.Model):
    ID = models.AutoField(primary_key=True)
    question = models.TextField(blank=False, null=False)
    answer = models.TextField(blank=False, null=False)


class Cart(models.Model):
    products = models.ManyToManyField(Product)
