"""
Django settings for Alejandria project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '56&@1#k_scqs8ymk&24hm@f4z=g!*5b#%_tgk)zmny(hh__-#d'
LOGIN_URL = '/'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['alejandria-es.herokuapp.com', '127.0.0.1','localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # own apps
    'crispy_forms',
    'Alejandria',
    # 'books',
    'books.apps.BooksConfig',
    'test'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'Alejandria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Alejandria.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     'travis_ci_test',
            'USER':     'postgres',
            'PASSWORD': '',
            'HOST':     'localhost',
            'PORT':     '5432',
        }
    }
elif 'HEROKU' in os.environ:
    DATABASES = {
        'default': {
            # Se configura en el pgadmin del postgresql
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'd6ttju9kflvip9',  # Poned este nombre todos en el pgadmin al crear la db local
            'USER': 'hhcommywfpctls',  # Cread este usuario y asignadlo como owner de la db y dadle todos los permisos
            'PASSWORD': 'dcd0b919ef67e90389ee27dc77b4a75a4c2d245936f67c85cc774ee46f7dfa0a',  # usad esta constraseña
            'HOST': 'ec2-54-156-85-145.compute-1.amazonaws.com',  # como hemos dicho es una db local
            'PORT': '5432'  # a este puerto
        }

        # Despues de configurar la
    }

else:
    print("Remember, you are in the local database.")
    DATABASES = {
        'default': {
            # Se configura en el pgadmin del postgresql
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'Alejandria_DB',  # Poned este nombre todos en el pgadmin al crear la db local
            'USER': 'Alejandro',  # Cread este usuario y asignadlo como owner de la db y dadle todos los permisos
            'PASSWORD': 'Password1',  # usad esta constraseña
            'HOST': 'localhost',  # como hemos dicho es una db local
            'PORT': '5432'  # a este puerto
        }

        # Despues de configurar la
    }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'books.backend.EmailAuthBackend',

)

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# STATICFILES_DIRS = ['/static/']
AUTH_USER_MODEL = 'books.User'
CRISPY_TEMPLATE_PACK="bootstrap4"

# MAIL SETUP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'alejandria.books.2020@gmail.com'
EMAIL_HOST_PASSWORD = 'alejandriaES2020'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Alejandria Books <alejandria.books.2020@gmail.com>'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# For print in tests
# NOSE_ARGS = ['--nocapture',
#             '--nologcapture',]
