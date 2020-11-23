from .models import User
from validate_email import validate_email
from nltk import word_tokenize
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def encode_genre(taste):
    genres = {
        'Fantasy': 'FANT',
        'Crime & Thriller': 'CRIM',
        'Fiction': 'FICT',
        'Science Fiction': 'SCFI',
        'Horror': 'HORR',
        'Romance': 'ROMA',
        'Teen & Young Adult': 'TEEN',
        "Children's Books": 'KIDS',
        'Anime & Manga': 'ANIM',
        'Others': 'OTHR',
        'Art': 'ARTS',
        'Biography': 'BIOG',
        'Food': 'FOOD',
        'History': 'HIST',
        'Dictionary': 'DICT',
        'Health': 'HEAL',
        'Humor': 'HUMO',
        'Sport': 'SPOR',
        'Travel': 'TRAV',
        'Poetry': 'POET'
    }

    return genres[taste]


def validate_register(request):
    # No Blank Data
    data = request.POST
    data_answered = all([len(data[key]) > 0 for key in data if 'taste' not in key])
    exists = User.objects.filter(email=request.POST["email"]).exists()
    validation = data_answered and not exists
    return validation


def validate_data(request):
    data = request.POST
    data_answered = all([len(data[key]) > 0 for key in data if 'taste' not in key])
    check_mail = validate_email(data["email"])
    return data_answered and check_mail


def tokenize(text):
    return word_tokenize(text)
