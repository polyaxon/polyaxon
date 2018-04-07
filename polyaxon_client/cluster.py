# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException
from polyaxon_schemas.clusters import ClusterNodeConfig, PolyaxonClusterConfig


class ClusterClient(PolyaxonClient):
    """Client to get clusters from the server"""
    ENDPOINT = "/cluster"
    ENDPOINT_NODES = "/nodes"

    def get_cluster(self):
        request_url = self._build_url(self._get_http_url())
        try:
            response = self.get(request_url)
            return PolyaxonClusterConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving cluster')
            return None

    def get_node(self, node_sequence):
        request_url = self._build_url(self._get_http_url(self.ENDPOINT_NODES), node_sequence)
        try:
            response = self.get(request_url)
            return ClusterNodeConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving node')
            return None
