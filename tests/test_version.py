# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
from unittest import TestCase
import httpretty
from faker import Faker

from polyaxon_schemas.version import CliVersionConfig

from polyaxon_client.version import VersionClient

faker = Faker()


class TestVersionClient(TestCase):

    def setUp(self):
        self.client = VersionClient(host='http://localhost', version='v1')

    @httpretty.activate
    def test_get_cli_version(self):
        object = CliVersionConfig(latest_version='1.0', min_version='0.5').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            VersionClient._build_url(
                VersionClient.BASE_URL.format('http://localhost', 'v1'),
                VersionClient.ENDPOINT),
            body=json.dumps(object),
            content_type='application/json', status=200)
        result = self.client.get_cli_version()
        assert object == result.to_dict()
