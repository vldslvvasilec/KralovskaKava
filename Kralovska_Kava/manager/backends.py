from django.contrib.auth.backends import ModelBackend
from manager.models import Manager

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Manager.objects.get(username=username)
            if user.check_password(password):
                return user
        except Manager.DoesNotExist:
            return None
