from __future__ import absolute_import, print_function

import logging
import uuid

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

import auditor
from libs.wizards import Wizard
from sso import providers
from sso.models import SSOIdentity
from users.utils import login_user

logger = logging.getLogger('polyaxon.identity')


class IdentityWizard(Wizard):
    logger = logger

    name = 'identity_wizard'
    manager = providers.default_manager

    def redirect_url(self, request):
        associate_url = reverse('sso:create_identity', args=[self.provider.key])

        # Use configured redirect_url if specified for the pipeline if available
        associate_url = self.config.get('redirect_url', associate_url)
        return '{}://{}{}'.format('https' if request.is_secure() else 'http',
                                  request.get_host(),
                                  associate_url)

    def get_or_create_user(self, identity):
        # Check if request has already a user
        if not self.request.user.is_anonymous:
            return self.request.user

        # Try to look for user:
        # * 1. based on the external id
        # * 2. based on an existing email
        # * 3. based on an existing username

        try:
            sso_identity = SSOIdentity.objects.get(external_id=identity['id'])
            return sso_identity.user
        except SSOIdentity.DoesNotExist:
            pass

        user_model_cls = get_user_model()
        user = user_model_cls.objects.filter(Q(email=identity['email']) |
                                             Q(username=identity['username']))
        if user.count() > 0:
            try:
                user = user_model_cls.objects.get(email=identity['email'])
            except user_model_cls.DoesNotExist:
                user = user_model_cls.objects.get(email=identity['username'])
            return user
        # Create a new user
        return user_model_cls.objects.create(
            email=identity['email'],
            username=identity['username'],
            first_name=identity['first_name'],
            last_name=identity['last_name'],
            password='{}.{}'.format(
                self.provider.key, uuid.uuid4().hex)  # Generate a random password
        )

    def finish_wizard(self):
        identity = self.provider.build_identity(self.state.data)

        defaults = {
            'valid': True,
            'scopes': identity.get('scopes', []),
            'data': identity.get('data', {}),
            'last_verified': timezone.now(),
        }

        user = self.get_or_create_user(identity=identity)
        _, created = SSOIdentity.objects.update_or_create(
            provider=self.provider.key,
            user=user,
            external_id=identity['id'],
            defaults=defaults,
        )

        if created:
            auditor.record(event_type=self.provider.event_type, instance=user)

        self.state.clear()

        response = HttpResponseRedirect('/')
        login_user(request=self.request, response=response, user=user, login=True)
        return response
