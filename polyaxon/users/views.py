# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from polyaxon_schemas.user import UserConfig

from rest_framework.authtoken.models import Token

from registration.backends.hmac import views as hmac_views
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from users.forms import RegistrationForm


class RegistrationView(hmac_views.RegistrationView):
    form_class = RegistrationForm
    template_name = 'users/register.html'
    email_body_template = 'users/activation_email.txt'
    email_subject_template = 'users/activation_email_subject.txt'

    def get_success_url(self, user):
        return 'users:registration_complete', (), {}


class ActivationView(hmac_views.ActivationView):
    template_name = 'users/activate.html'
    success_url = 'users:registration_activation_complete'


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'
    subject_template_name = 'users/password_reset_subject.txt'
    email_template_name = 'users/password_reset_body.txt'
    success_url = reverse_lazy('users:password_reset_done')


class TokenView(TemplateView):
    template_name = 'users/token.html'

    def get_context_data(self, **kwargs):
        context = super(TokenView, self).get_context_data(**kwargs)
        token, _ = Token.objects.get_or_create(user=self.request.user)
        context['token'] = token.key
        return context


class UserView(RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        return Response(UserConfig.obj_to_dict(user))
