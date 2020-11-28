# backend.ModelBackends deffined in this file
from django.contrib.auth import backends
from books.models import User


class EmailAuthBackend(backends.ModelBackend):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair, then check
    a username/password pair if email failed
    """
    # Pylint: disable=arguments-differ
    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
                if user.password == password:
                    return user
            except User.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
