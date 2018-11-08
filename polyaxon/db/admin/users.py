from django.contrib.admin import site
from django.contrib.auth.admin import UserAdmin

from db.models.users import User

site.register(User, UserAdmin)
