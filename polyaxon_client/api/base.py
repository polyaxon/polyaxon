# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from collections import Mapping

from polyaxon_client.exceptions import ERRORS_MAPPING, PolyaxonClientException


class BaseApiHandler(object):
    """
    Base api handler.
    """
    ENDPOINT = None
    HEARTBEAT = '_heartbeat'

    def __init__(self, transport, config):
        self.transport = transport
        self.config = config

    @staticmethod
    def build_url(*parts):
        url = ''
        for part in parts:
            part = part.rstrip('/').lstrip('/') if isinstance(part, six.string_types) else part
            if part:
                url += '{}/'.format(part)

        return url

    def _get_url(self, base_url, endpoint=None):
        endpoint = endpoint or self.ENDPOINT
        if endpoint is None:
            raise ERRORS_MAPPING['base'](
                "This function expects `ENDPOINT` attribute to be set, "
                "or an `endpoint` argument to be passed.")
        return self.build_url(base_url, endpoint)

    def _get_http_url(self, endpoint=None):
        return self._get_url(self.config.base_url, endpoint)

    def _get_ws_url(self, endpoint=None):
        return self._get_url(self.config.base_ws_url, endpoint)

    def get_page(self, page=1):
        if page <= 1:
            return {}
        return {'offset': (page - 1) * self.config.PAGE_SIZE}

    def prepare_list_results(self, response_json, current_page, config):
        list_results = {
            'count': response_json.get('count', 0),
            'next': current_page + 1 if response_json.get('next') else None,
            'previous': current_page - 1 if response_json.get('previous') else None,
        }
        if self.config.schema_response:
            list_results['results'] = [
                config.from_dict(obj) for obj in response_json.get('results', [])]
        else:
            list_results['results'] = response_json.get('results', [])

        return list_results

    def prepare_results(self, response_json, config):
        return config.from_dict(response_json) if self.config.schema_response else response_json

    @staticmethod
    def validate_config(config, config_schema):
        if isinstance(config, Mapping):
            return config_schema.from_dict(config)
        elif not isinstance(config, config_schema):
            raise PolyaxonClientException(
                'Received an invalid config. '
                'Expects a Mapping or an instance of `{}`.'.format(config_schema.__name__))

        return config
