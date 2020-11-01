from django.contrib import admin

# Register your models here.

from .models import Book, User, Address

admin.site.register(Book)
admin.site.register(User)
admin.site.register(Address)
#TODO