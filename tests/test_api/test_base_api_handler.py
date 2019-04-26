# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tests.test_api.utils import TestBaseApi

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import ERRORS_MAPPING, PolyaxonClientException
from polyaxon_client.schemas import BuildJobConfig, ExperimentConfig


class DummyConfig(object):
    @staticmethod
    def from_dict(value, unknown=None):  # noqa
        return 'from_dict', value


class TestBaseApiHandler(TestBaseApi):
    # pylint:disable=protected-access
    def setUp(self):
        super(TestBaseApiHandler, self).setUp()
        self.api_handler = BaseApiHandler(transport=self.transport, config=self.api_config)

    def test_get_page(self):
        assert self.api_handler.get_page() == {}
        assert self.api_handler.get_page(page=1) == {}
        assert self.api_handler.get_page(page=2) == {'offset': self.api_config.PAGE_SIZE}
        assert self.api_handler.get_page(page=3) == {'offset': self.api_config.PAGE_SIZE * 2}

    def test_build_url(self):
        assert self.api_handler.build_url('a') == 'a/'
        assert self.api_handler.build_url('a', 'b') == 'a/b/'

    def test_get_url(self):
        with self.assertRaises(ERRORS_MAPPING['base']):
            self.api_handler._get_url('a')

        assert self.api_handler._get_url('base', 'endpoint') == 'base/endpoint/'
        assert self.api_handler._get_http_url('endpoint') == '{}/endpoint/'.format(
            self.api_config.base_url)
        assert self.api_handler._get_ws_url('endpoint') == '{}/endpoint/'.format(
            self.api_config.base_ws_url)

    def test_prepare_results(self):
        # Schema response
        results = self.api_handler.prepare_results(response_json={'foo': 'bar'},
                                                   config=DummyConfig)
        assert results == ('from_dict', {'foo': 'bar'})

        # Raw response
        self.api_config.schema_response = False
        results = self.api_handler.prepare_results(response_json={'foo': 'bar'},
                                                   config=DummyConfig)
        assert results == {'foo': 'bar'}

    def test_prepare_list_results(self):
        # Schema response
        results = self.api_handler.prepare_list_results(response_json={'results': ['bar']},
                                                        current_page=1,
                                                        config=DummyConfig)
        assert results == {'count': 0,
                           'next': None,
                           'previous': None,
                           'results': [('from_dict', 'bar')]}

        # Raw response
        self.api_config.schema_response = False
        results = self.api_handler.prepare_list_results(response_json={'results': ['bar']},
                                                        current_page=1,
                                                        config=DummyConfig)
        assert results == {'count': 0, 'next': None, 'previous': None, 'results': ['bar']}

    def test_validate_config(self):
        assert isinstance(self.api_handler.validate_config(config={}, config_schema=BuildJobConfig),
                          BuildJobConfig)

        with self.assertRaises(PolyaxonClientException):
            self.api_handler.validate_config(config=ExperimentConfig(),
                                             config_schema=BuildJobConfig)

    def test_validate_content(self):
        assert self.api_handler.validate_content(None) is None
        assert self.api_handler.validate_content({'foo': 'bar'}) == "{'foo': 'bar'}"
        assert self.api_handler.validate_content("{'foo': 'bar'}") == "{'foo': 'bar'}"
        assert self.api_handler.validate_content(BuildJobConfig()) == '{}'.format(
            BuildJobConfig().to_dict())
