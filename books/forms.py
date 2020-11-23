"""
Contains forms.ModelForm used for ajax communication
"""

from django import forms
from books.models import Book


class BookForm(forms.ModelForm):
    """
    Defines the structure of information that a Book represents
    """
    terms = forms.BooleanField(
        error_messages={'required': 'You must accept the terms and conditions'},
        label="Terms&Conditions"
    )

    class Meta:
        """ BookFrom Meta """
        model = Book

        fields = [
            "ISBN",
            "title",
            "description",
            "saga",
            "author",
            "publication_date",
            "price",
            "language",
            "primary_genre",
            "secondary_genre",
            "publisher",
            "num_pages",
            "recommended_age",
            "thumbnail",
            "eBook"
        ]
