# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib.auth import views as auth_views, get_user_model
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from polyaxon_schemas.user import UserConfig
from rest_framework import status

from rest_framework.authtoken.models import Token

from registration.backends.hmac import views as hmac_views
from rest_framework.generics import RetrieveAPIView, GenericAPIView, get_object_or_404, \
    CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from users.forms import RegistrationForm


class SimpleRegistrationView(hmac_views.RegistrationView):
    """Registration and validation though a superuser."""
    form_class = RegistrationForm
    template_name = 'users/register.html'

    def get_success_url(self, user):
        return 'users:registration_complete', (), {}

    def create_inactive_user(self, form):
        """Create the inactive user account and wait for validation from superuser"""
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()
        return new_user


class RegistrationView(hmac_views.RegistrationView):
    """Registration and validation through email."""
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


class ActivateView(CreateAPIView):
    queryset = get_user_model().objects.filter()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    lookup_field = 'username'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)


class DeleteView(DestroyAPIView):
    queryset = get_user_model()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    lookup_field = 'username'


class GrantSuperuserView(CreateAPIView):
    queryset = get_user_model()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    lookup_field = 'username'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return Response(status=status.HTTP_200_OK)


class RevokeSuperuserView(CreateAPIView):
    queryset = get_user_model()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    lookup_field = 'username'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return Response(status=status.HTTP_200_OK)
