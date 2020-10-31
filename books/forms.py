from django import forms
from django.contrib.auth.forms import UserCreationForm
from books.models import User
import django.contrib.auth.forms

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    # User
    country1 = forms.CharField(label="País",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}))
    city1 = forms.CharField(label="Ciudad",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}))
    street1 = forms.CharField(label="Calle",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle'}))
    zip1 = forms.CharField(label="C.P.",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CP'}))
    # Fact
    country2 = forms.CharField(label="País",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}))
    city2 = forms.CharField(label="Ciudad",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}))
    street2 = forms.CharField(label="Calle",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle'}))
    zip2 = forms.CharField(label="C.P.",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CP'}))


    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]