from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """A model that represents users inside Polyaxon"""

    class Meta(AbstractUser.Meta):
        app_label = 'db'
