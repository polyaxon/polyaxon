from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import View

from sso.wizard import IdentityWizard


class AccountCreateIdentityView(View):
    def dispatch(self, request, provider, *args, **kwargs):  # pylint:disable=arguments-differ
        if not IdentityWizard.manager.knows(provider):
            raise Http404
        wizard = IdentityWizard.get_for_request(request)

        if wizard is None or not wizard.is_valid():
            wizard = IdentityWizard(
                provider_key=provider,
                request=request,
            )

            if request.method != 'POST' and not wizard.is_valid():
                return HttpResponseRedirect(reverse('users:login'))

            wizard.initialize()

        return wizard.current_step()
