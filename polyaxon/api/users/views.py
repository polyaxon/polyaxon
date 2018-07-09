from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView

import auditor

from api.users.forms import RegistrationForm
from api.users.utils import login_user, logout_user
from api.utils.views import PostAPIView
from event_manager.events.superuser import SUPERUSER_ROLE_GRANTED, SUPERUSER_ROLE_REVOKED
from event_manager.events.user import USER_ACTIVATED, USER_DELETED
from polyaxon_schemas.user import UserConfig
from signals import users as users_signals


class AuthTokenLogin(ObtainAuthToken):
    """Login user and return user's token."""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        response = Response({'token': token.key})
        if request.data.get('login'):
            auth_login(self.request, user)
            response.set_cookie('token', value=token)
            response.set_cookie('user', value=user.username)
        return response


class AuthTokenLogout(APIView):
    throttle_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        response = Response()
        response.delete_cookie('token')
        response.delete_cookie('user')
        return response


class RefreshSessionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        auth_login(self.request, request.user)
        return Response()


class LoginView(AuthLoginView):
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return HttpResponseRedirect('/')
        response = super().dispatch(request, *args, **kwargs)
        login_user(request=request, response=response, user=request.user, login=False)
        return response


class LogoutView(AuthLogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        logout_user(request=request, response=response, logout=False)
        return response


class RegistrationView(FormView):
    """Register a new (inactive) user account, generate an activation key and email it to the user.

    This is different from the model-based activation workflow in that
    the activation key is the username, signed using Django's
    TimestampSigner, with HMAC verification on activation.
    """
    form_class = RegistrationForm
    template_name = 'users/register.html'
    email_body_template = 'users/activation_email.txt'
    email_subject_template = 'users/activation_email_subject.txt'
    success_url = 'users:registration_complete'
    key_salt = 'users.tokens.RegistrationView'

    def form_valid(self, form):
        self.register(form)
        return redirect(self.get_success_url())

    def register(self, form):
        new_user = self.create_inactive_user(form)
        users_signals.user_registered.send(
            sender=self.__class__,
            user=new_user,
            request=self.request)
        return new_user

    def create_inactive_user(self, form):
        """
        Create the inactive user account and send an email containing
        activation instructions.

        """
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()

        self.send_activation_email(new_user)

        return new_user

    def get_activation_key(self, user):
        """
        Generate the activation key which will be emailed to the user.

        """
        return signing.dumps(
            obj=getattr(user, user.USERNAME_FIELD),
            salt=self.key_salt
        )

    def get_email_context(self, activation_key):
        """
        Build the template context used for the activation email.

        """
        return {
            'activation_key': activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': get_current_site(self.request)
        }

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is the username,
        signed using TimestampSigner.

        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context.update({
            'user': user
        })
        subject = render_to_string(self.email_subject_template,
                                   context)
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = ''.join(subject.splitlines())
        message = render_to_string(self.email_body_template,
                                   context)
        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


class SimpleRegistrationView(RegistrationView):
    """Registration and validation though a superuser."""
    form_class = RegistrationForm
    template_name = 'users/register.html'

    def create_inactive_user(self, form):
        """Create the inactive user account and wait for validation from superuser"""
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()
        return new_user

    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)


class ActivationView(TemplateView):
    """
    Given a valid activation key, activate the user's
    account. Otherwise, show an error message stating the account
    couldn't be activated.

    """
    template_name = 'users/activate.html'
    success_url = 'users:registration_activation_complete'
    key_salt = 'users.tokens.RegistrationView'

    def activate(self, *args, **kwargs):
        # This is safe even if, somehow, there's no activation key,
        # because unsign() will raise BadSignature rather than
        # TypeError on a value of None.
        username = self.validate_key(kwargs.get('activation_key'))
        if username is not None:
            user = self.get_user(username)
            if user is not None:
                user.is_active = True
                user.save()
                return user
        return False

    def validate_key(self, activation_key):
        """
        Verify that the activation key is valid and within the
        permitted activation time window, returning the username if
        valid or ``None`` if not.

        """
        try:
            username = signing.loads(
                activation_key,
                salt=self.key_salt,
                max_age=settings.ACCOUNT_ACTIVATION_DAYS * 86400
            )
            return username
        # SignatureExpired is a subclass of BadSignature, so this will
        # catch either one.
        except signing.BadSignature:
            return None

    def get_user(self, username):
        """
        Given the verified username, look up and return the
        corresponding user account if it exists, or ``None`` if it
        doesn't.

        """
        User = get_user_model()  # noqa
        try:
            user = User.objects.get(**{
                User.USERNAME_FIELD: username,
                'is_active': False
            })
            return user
        except User.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        """The base activation logic; subclasses should leave this method
        alone and implement activate(), which is called from this method.
        """
        activated_user = self.activate(*args, **kwargs)
        if activated_user:
            users_signals.user_activated.send(
                sender=self.__class__,
                user=activated_user,
                request=request
            )
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'
    subject_template_name = 'users/password_reset_subject.txt'
    email_template_name = 'users/password_reset_body.txt'
    success_url = reverse_lazy('users:password_reset_done')


class TokenView(TemplateView):
    template_name = 'users/token.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token, _ = Token.objects.get_or_create(user=self.request.user)
        context['token'] = token.key
        return context


class UserView(RetrieveAPIView):
    """Get user details."""
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        return Response(UserConfig.obj_to_dict(user))


class ActivateView(PostAPIView):
    """Activate user."""
    queryset = get_user_model().objects.filter()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    lookup_field = 'username'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = True
        user.save()
        auditor.record(event_type=USER_ACTIVATED,
                       instance=user,
                       actor_id=self.request.user.id)
        return Response(status=status.HTTP_200_OK)


class DeleteView(DestroyAPIView):
    """Delete user."""
    queryset = get_user_model()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    lookup_field = 'username'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        auditor.record(event_type=USER_DELETED,
                       instance=instance,
                       actor_id=self.request.user.id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GrantSuperuserView(PostAPIView):
    """Grant a user the superuser role."""
    queryset = get_user_model()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    lookup_field = 'username'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_staff = True
        user.is_superuser = True
        user.save()
        auditor.record(event_type=SUPERUSER_ROLE_GRANTED,
                       instance=user,
                       actor_id=self.request.user.id)
        return Response(status=status.HTTP_200_OK)


class RevokeSuperuserView(PostAPIView):
    """Revoke the superuser role from user."""
    queryset = get_user_model()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    lookup_field = 'username'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_staff = False
        user.is_superuser = False
        user.save()
        auditor.record(event_type=SUPERUSER_ROLE_REVOKED,
                       instance=user,
                       actor_id=self.request.user.id)
        return Response(status=status.HTTP_200_OK)
