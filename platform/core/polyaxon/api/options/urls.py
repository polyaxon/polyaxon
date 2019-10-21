from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.options import views
from constants.urls import OWNER_NAME_PATTERN

options_urlpatterns = [
    re_path(r'{}/options/?$'.format(
        OWNER_NAME_PATTERN),
        views.OwnerConfigOptionsViewV1.as_view()),
    re_path(r'options/?$', views.ClusterConfigOptionsViewV1.as_view()),
]

urlpatterns = format_suffix_patterns(options_urlpatterns)
