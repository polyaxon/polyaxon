from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from constants.urls import USERNAME_PATTERN
from api.users import views

urlpatterns = [
    re_path(r'^users/?$',
            views.UserView.as_view()),
    re_path(r'^users/token/?$',
            views.AuthTokenLogin.as_view()),
    re_path(r'^users/logout/?$',
            views.AuthTokenLogout.as_view()),
    re_path(r'^users/activate/{}/?$'.format(USERNAME_PATTERN),
            views.ActivateView.as_view()),
    re_path(r'^users/delete/{}/?$'.format(USERNAME_PATTERN),
            views.DeleteView.as_view()),
    re_path(r'^users/session/refresh/?$',
            views.RefreshSessionView.as_view()),
    re_path(r'^superusers/grant/{}/?$'.format(USERNAME_PATTERN),
            views.GrantSuperuserView.as_view()),
    re_path(r'^superusers/revoke/{}/?$'.format(USERNAME_PATTERN),
            views.RevokeSuperuserView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
