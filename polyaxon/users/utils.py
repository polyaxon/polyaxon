from rest_framework.authtoken.models import Token

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


def login_user(request, response, user, login=True):
    if login:
        auth_login(request, user)

    if user.is_authenticated:
        token, _ = Token.objects.get_or_create(user=request.user)
        response.set_cookie('token', value=token)
        response.set_cookie('user', value=request.user.username)


def logout_user(request, response, logout=True):
    if logout:
        auth_logout(request)

    response.delete_cookie('token')
    response.delete_cookie('user')
