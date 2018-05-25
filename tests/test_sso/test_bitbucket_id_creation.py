from urllib.parse import urlparse

from django.urls import reverse

from tests.utils import BaseViewTest


class BitbucketIdentityTest(BaseViewTest):
    def test_wrong_provider_raises_404(self):
        auth_path = reverse('oauth:create_identity', kwargs={'provider': 'undefined'})
        resp = self.client.get(auth_path)
        assert resp.status_code == 404

    def test_get_redirects_to_login(self):
        auth_path = reverse('oauth:create_identity', kwargs={'provider': 'bitbucket'})
        resp = self.client.get(auth_path)
        redirect = urlparse(resp['Location'])
        assert resp.status_code == 302
        assert redirect.path == reverse('users:login')

    def test_flow(self):
        auth_path = reverse('oauth:create_identity', kwargs={'provider': 'bitbucket'})

        resp = self.client.post(auth_path)
        assert resp.status_code == 302
        redirect = urlparse(resp['Location'])
        assert redirect.scheme == 'https'
        assert redirect.netloc == 'bitbucket.org'
        assert redirect.path == '/site/oauth2/authorize'
