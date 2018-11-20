
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from db.models.tokens import Token


def login_user(request, response, user, login=True):
    if login:
        auth_login(request, user)

    if user.is_authenticated:
        token, _ = Token.objects.get_or_create(user=request.user)
        response.set_cookie('token', value=token.key)
        response.set_cookie('user', value=request.user.username)


def logout_user(request, response, logout=True):
    if logout:
        auth_logout(request)

    response.delete_cookie('token')
    response.delete_cookie('user')
