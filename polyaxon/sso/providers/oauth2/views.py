import uuid

from urllib.parse import parse_qsl, urlencode

from django.http import HttpResponseRedirect
from django.views import View

from libs.http import safe_urlopen
from libs.json_utils import loads


class OAuth2LoginView(View):
    authorize_url = None
    client_id = None
    scope = ''

    # pylint:disable=keyword-arg-before-vararg
    def __init__(self, authorize_url=None, client_id=None, scope=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if authorize_url is not None:
            self.authorize_url = authorize_url
        if client_id is not None:
            self.client_id = client_id
        if scope is not None:
            self.scope = scope

    def get_scope(self):
        return self.scope

    def get_authorize_url(self):
        return self.authorize_url

    def get_authorize_params(self, state, redirect_uri):
        return {
            'client_id': self.client_id,
            'response_type': "code",
            'scope': self.get_scope(),
            'state': state,
            'redirect_uri': redirect_uri,
        }

    def dispatch(self, request, wizard, *args, **kwargs):  # pylint:disable=arguments-differ
        if 'code' in request.GET:
            return wizard.next_step()

        state = uuid.uuid4().hex

        params = self.get_authorize_params(
            state=state,
            redirect_uri=wizard.redirect_url(request=request),
        )
        redirect_uri = '{}?{}'.format(self.get_authorize_url(), urlencode(params))

        wizard.bind_state('state', state)
        return self.redirect(redirect_uri)

    def redirect(self, url):
        return HttpResponseRedirect(url)


class OAuth2CallbackView(View):
    access_token_url = None
    client_id = None
    client_secret = None

    def __init__(self, access_token_url=None, client_id=None, client_secret=None, **kwargs):
        super().__init__(**kwargs)
        if access_token_url is not None:
            self.access_token_url = access_token_url
        if client_id is not None:
            self.client_id = client_id
        if client_secret is not None:
            self.client_secret = client_secret

    def get_token_params(self, code, redirect_uri):
        return {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

    def exchange_token(self, request, wizard, code):
        data = self.get_token_params(
            code=code,
            redirect_uri=wizard.redirect_url(request=request),
        )
        response = safe_urlopen(self.access_token_url, data=data)
        content = response.content.decode()
        if response.headers['Content-Type'].startswith('application/x-www-form-urlencoded'):
            return dict(parse_qsl(content))
        return loads(content)

    def dispatch(self, request, wizard, *args, **kwargs):  # pylint:disable=arguments-differ
        error = request.GET.get('error')
        state = request.GET.get('state')
        code = request.GET.get('code')

        if error:
            wizard.logger.info('identity.token-exchange-error', extra={'error': error})
            return wizard.error(error)

        if state != wizard.fetch_state('state'):
            wizard.logger.info('identity.token-exchange-error', extra={'error': 'invalid_state'})
            return wizard.error('An error occurred while validating your request.')

        data = self.exchange_token(request, wizard, code)

        if 'error_description' in data:
            error = data.get('error')
            wizard.logger.info('identity.token-exchange-error', extra={'error': error})
            return wizard.error(data['error_description'])

        if 'error' in data:
            wizard.logger.info('identity.token-exchange-error', extra={'error': data['error']})
            return wizard.error('Failed to retrieve token from the upstream service.')

        wizard.bind_state('data', data)

        return wizard.next_step()
