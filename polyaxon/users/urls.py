from django.urls import re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns

from polyaxon.config_settings import registration

from users import views

if registration.REGISTRATION_WORKFLOW == registration.REGISTRATION_SUPERUSER_VALIDATION_WORKFLOW:
    urlpatterns = [
        re_path(
            r'^register/?$',
            views.SimpleRegistrationView.as_view(),
            name='registration_simple_register'),
        re_path(
            r'^register/complete/?$',
            TemplateView.as_view(template_name='users/registration_simple_complete.html'),
            name='registration_complete'),
    ]
else:
    urlpatterns = [
        re_path(
            r'^token/$',
            login_required(views.TokenView.as_view()),
            name='token'),
        re_path(
            r'^login/$',
            auth_views.LoginView.as_view(template_name='users/login.html'),
            name='login'),
        re_path(
            r'^logout/$',
            auth_views.LogoutView.as_view(template_name='users/logout.html'),
            name='logout'),
        re_path(
            r'^password_change/$',
            auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'),
            name='password_change'),
        re_path(
            r'^password_change/done/$',
            auth_views.PasswordChangeDoneView.as_view(
                template_name='users/password_change_done.html'),
            name='password_change_done'),
        re_path(
            r'^password_reset/$',
            views.PasswordResetView.as_view(),
            name='password_reset'),
        re_path(
            r'^password_reset/done/$',
            auth_views.PasswordResetDoneView.as_view(
                template_name='users/password_reset_done.html'),
            name='password_reset_done'),
        re_path(
            r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='users/password_reset_confirm.html'),
            name='password_reset_confirm'),
        re_path(
            r'^reset/done/$',
            auth_views.PasswordResetCompleteView.as_view(
                template_name='users/password_reset_complete.html'),
            name='password_reset_complete'),
        # registration
        re_path(
            r'^activate/complete/$',
            TemplateView.as_view(template_name='users/registration_activation_complete.html'),
            name='registration_activation_complete'),
        # The activation key can make use of any character from the
        # URL-safe base64 alphabet, plus the colon as a separator.
        re_path(
            r'^activate/(?P<activation_key>[-:\w]+)/$',
            views.ActivationView.as_view(),
            name='registration_activate'),
        re_path(
            r'^register/$',
            views.RegistrationView.as_view(),
            name='registration_register'),
        re_path(
            r'^register/complete/$',
            TemplateView.as_view(template_name='users/registration_complete.html'),
            name='registration_complete'),
        re_path(
            r'^register/closed/$',
            TemplateView.as_view(template_name='users/registration_closed.html'),
            name='registration_disallowed'),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
