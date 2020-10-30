from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Book(models.Model):
    ISBN = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    author = models.CharField(max_length=30)
    year = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    language = models.CharField(max_length=15)
    genre = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    num_pages = models.IntegerField()
    num_sold = models.IntegerField()
    recommended_age = models.IntegerField()
    thumbnail = models.CharField(max_length=30)


class Address(models.Model):
    street = models.CharField(max_length=50, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False)
    zip = models.CharField(max_length=10, null=False, blank=False)


class User(AbstractUser):
    id = models.AutoField(primary_key=True, null=False, blank=True)
    role = models.CharField(max_length=10, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    password = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    user_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=False, null=False,
                                     related_name="user_address")
    fact_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=False, null=False,
                                     related_name="fact_address")
