from django.urls import re_path

from rest_framework.urlpatterns import format_suffix_patterns

from versions import views

urlpatterns = [
    re_path(r'^versions/cli/?$', views.CliVersionView.as_view()),
    re_path(r'^versions/platform/?$', views.PlatformVersionView.as_view()),
    re_path(r'^versions/lib/?$', views.LibVersionView.as_view()),
    re_path(r'^versions/chart/?$', views.ChartVersionView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
