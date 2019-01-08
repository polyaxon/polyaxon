from django.contrib.auth.admin import UserAdmin

from db.models.users import User


def register(admin_register):
    admin_register(User, UserAdmin)
