# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from hestia.auth import AuthenticationTypes
from tests.test_transports.utils import BaseTestCaseTransport

from polyaxon_client.api_config import ApiConfig
from polyaxon_client.transport import Transport


class TestTransport(BaseTestCaseTransport):
    # pylint:disable=protected-access
    def setUp(self):
        super(TestTransport, self).setUp()
        self.transport = Transport()

    def test_get_headers(self):
        assert self.transport._get_headers() == {}
        assert self.transport._get_headers({'foo': 'bar'}) == {'foo': 'bar'}

        self.transport.config = ApiConfig(token='token', host='host')

        assert self.transport._get_headers() == {
            'Authorization': "{} {}".format(AuthenticationTypes.TOKEN, 'token')
        }
        assert self.transport._get_headers({'foo': 'bar'}) == {
            'foo': 'bar',
            'Authorization': "{} {}".format(AuthenticationTypes.TOKEN, 'token')
        }

        self.transport.config.authentication_type = AuthenticationTypes.INTERNAL_TOKEN
        assert self.transport._get_headers() == {
            'Authorization': "{} {}".format(AuthenticationTypes.INTERNAL_TOKEN, 'token')
        }
        assert self.transport._get_headers({'foo': 'bar'}) == {
            'foo': 'bar',
            'Authorization': "{} {}".format(AuthenticationTypes.INTERNAL_TOKEN, 'token')
        }
