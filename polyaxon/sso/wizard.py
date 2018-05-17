from __future__ import absolute_import, print_function

import logging

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from libs.wizards import Wizard
from sso import providers
from sso.models import SSOIdentity, SSOProvider

logger = logging.getLogger('polyaxon.identity')


class IdentityWizard(Wizard):
    logger = logger

    name = 'identity_wizard'
    manager = providers.default_manager
    model_cls = SSOProvider

    def redirect_url(self, request):
        associate_url = reverse('sso:create_identity')

        # Use configured redirect_url if specified for the pipeline if available
        associate_url = self.config.get('redirect_url', associate_url)
        return '{}://{}{}'.format(request.schema, request.get_host(), associate_url)

    def finish_wizard(self):
        identity = self.provider.build_identity(self.state.data)

        defaults = {
            'is_valid': True,
            'scopes': identity.get('scopes', []),
            'data': identity.get('data', {}),
            'last_verified': timezone.now(),
        }

        identity, created = SSOIdentity.objects.get_or_create(
            idp=self.provider_model,
            user=self.request.user,
            external_id=identity['id'],
            defaults=defaults,
        )

        if not created:
            identity.update(**defaults)

        self.state.clear()

        return HttpResponseRedirect('/')
