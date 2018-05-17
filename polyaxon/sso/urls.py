from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from sso import views

urlpatterns = [
    re_path(r'^(?P<provider>\w{0,50})/?$',
            views.AccountCreateIdentityView.as_view(),
            name='create_identity'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
