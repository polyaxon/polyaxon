# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import requests

import mock

from tests.test_transports.utils import BaseTestCaseTransport

from polyaxon_client.transport import Transport
from polyaxon_client.transport.utils import Bar


class TestHttpTransport(BaseTestCaseTransport):
    # pylint:disable=protected-access
    def setUp(self):
        super(TestHttpTransport, self).setUp()
        self.transport = Transport()

    def test_create_progress_callback(self):
        encoder = mock.MagicMock()
        encoder.configure_mock(len=10)
        _, progress_bar = self.transport.create_progress_callback(encoder)
        assert isinstance(progress_bar, Bar)

    def test_format_sizeof(self):
        assert self.transport.format_sizeof(10) == '10.0B'
        assert self.transport.format_sizeof(10000) == '9.8KiB'
        assert self.transport.format_sizeof(100000) == '97.7KiB'
        assert self.transport.format_sizeof(10000000) == '9.5MiB'
        assert self.transport.format_sizeof(10000000000) == '9.3GiB'

    def test_session(self):
        assert hasattr(self.transport, '_session') is False
        assert isinstance(self.transport.session, requests.Session)
        assert isinstance(self.transport._session, requests.Session)
