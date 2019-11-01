# coding: utf-8
from __future__ import absolute_import, division, print_function

from tests.test_transports.utils import BaseTestCaseTransport

from polyaxon.client.transport import Transport
from polyaxon.schemas.cli.client_configuration import ClientConfig
from polyaxon.services.auth import AuthenticationTypes


class TestTransport(BaseTestCaseTransport):
    # pylint:disable=protected-access
    def setUp(self):
        super(TestTransport, self).setUp()
        self.transport = Transport()

    def test_get_headers(self):
        assert self.transport._get_headers() == {}
        assert self.transport._get_headers({"foo": "bar"}) == {"foo": "bar"}

        self.transport.config = ClientConfig(token="token", host="host")

        assert self.transport._get_headers() == {
            "Authorization": "{} {}".format(AuthenticationTypes.TOKEN, "token")
        }
        assert self.transport._get_headers({"foo": "bar"}) == {
            "foo": "bar",
            "Authorization": "{} {}".format(AuthenticationTypes.TOKEN, "token"),
        }

        self.transport.config.authentication_type = AuthenticationTypes.INTERNAL_TOKEN
        assert self.transport._get_headers() == {
            "Authorization": "{} {}".format(AuthenticationTypes.INTERNAL_TOKEN, "token")
        }
        assert self.transport._get_headers({"foo": "bar"}) == {
            "foo": "bar",
            "Authorization": "{} {}".format(
                AuthenticationTypes.INTERNAL_TOKEN, "token"
            ),
        }
