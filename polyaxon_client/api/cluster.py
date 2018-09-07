# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.schemas import ClusterNodeConfig, PolyaxonClusterConfig


class ClusterApi(BaseApiHandler):
    """
    Api handler to get clusters from the server.
    """
    ENDPOINT = "/cluster"
    ENDPOINT_NODES = "/nodes"

    def get_cluster(self):
        request_url = self.build_url(self._get_http_url())
        try:
            response = self.transport.get(request_url)
            return self.prepare_results(response_json=response.json(), config=PolyaxonClusterConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving cluster')
            return None

    def get_node(self, node_sequence):
        request_url = self.build_url(self._get_http_url(self.ENDPOINT_NODES), node_sequence)
        try:
            response = self.transport.get(request_url)
            return self.prepare_results(response_json=response.json(), config=ClusterNodeConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving node')
            return None
