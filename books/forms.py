from django import forms
from django.contrib.auth.forms import UserCreationForm
from books.models import User, Address, Book
import django.contrib.auth.forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Layout, Submit


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    # User
    country1 = forms.CharField(label="País", widget=forms.TextInput(
        attrs={'class': 'form-control register-text', 'placeholder': 'País'}))
    city1 = forms.CharField(label="Ciudad", widget=forms.TextInput(
        attrs={'class': 'form-control register-text', 'placeholder': 'Ciudad'}))
    street1 = forms.CharField(label="Calle", widget=forms.TextInput(
        attrs={'class': 'form-control register-text', 'placeholder': 'Calle'}))
    zip1 = forms.CharField(label="C.P.",
                           widget=forms.TextInput(attrs={'class': 'form-control register-text', 'placeholder': 'CP'}))
    # Fact
    country2 = forms.CharField(label="País", widget=forms.TextInput(
        attrs={'class': 'form-control register-text', 'placeholder': 'País'}))
    city2 = forms.CharField(label="Ciudad", widget=forms.TextInput(
        attrs={'class': 'form-control register-text', 'placeholder': 'Ciudad'}))
    street2 = forms.CharField(label="Calle", widget=forms.TextInput(
        attrs={'class': 'form-control register-text', 'placeholder': 'Calle'}))
    zip2 = forms.CharField(label="C.P.",
                           widget=forms.TextInput(attrs={'class': 'form-control register-text', 'placeholder': 'CP'}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def save(self, commit=True):
        own = Address(country=self.data["country1"], city=self.data["city1"], street=self.data["street1"],
                      zip=self.data["zip1"])
        fact = Address(country=self.data["country2"], city=self.data["city2"], street=self.data["street2"],
                       zip=self.data["zip2"])
        own.save()
        fact.save()

        user = User(email=self.data["email"], first_name=self.data["first_name"], last_name=self.data["last_name"],
                    username=self.data["username"],
                    password=self.data["password1"], user_address=own, fact_address=fact)
        user.save()

        return user

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        pwd = cleaned_data.get("password1")
        conf_pwd = cleaned_data.get("password2")
        if pwd != conf_pwd:
            raise forms.ValidationError("Not matching passwords!")


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn-primary')
            )
        )

## TODO: That is an option to load books in the paige details.htm, but by now we are using the standard django
## Model DetailView, and passing the information through the html.
# class GetBookForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ['ISBN', 'title', 'description', 'saga', 'authors',
#                   'publication_date', 'price', 'language', 'genre', 'publisher',
#                   'num_pages', 'recommended_age', 'thumbnail']
#         widgets = {
#             'thumbnail' :
#         }
