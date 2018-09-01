# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_client.transport import Transport


class TestTransport(TestCase):
    def setUp(self):
        self.transport = Transport()

    def test_get_headers(self):
        assert self.transport._get_headers() == {}
        assert self.transport._get_headers({'foo': 'bar'}) == {'foo': 'bar'}

        self.transport.token = 'token'

        assert self.transport._get_headers() == {
            "Authorization": "{} {}".format('token', 'token')
        }
        assert self.transport._get_headers({'foo': 'bar'}) == {
            'foo': 'bar',
            "Authorization": "{} {}".format('token', 'token')
        }

        self.transport.authentication_type = 'bearer'
        assert self.transport._get_headers() == {
            "Authorization": "{} {}".format('bearer', 'token')
        }
        assert self.transport._get_headers({'foo': 'bar'}) == {
            'foo': 'bar',
            "Authorization": "{} {}".format('bearer', 'token')
        }
