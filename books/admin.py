"""
Models are registered here to the admin.
"""
from django.contrib import admin

# Register your models here.
from .models import Book, User, Address # pylint: disable=relative-beyond-top-level

admin.site.register(Book)
admin.site.register(User)
admin.site.register(Address)
