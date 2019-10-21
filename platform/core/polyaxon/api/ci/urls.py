from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.ci import views
from constants.urls import OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN

urlpatterns = [
    re_path(r'^{}/{}/ci/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN),
            views.CIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
