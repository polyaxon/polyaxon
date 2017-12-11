# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.clusters import PolyaxonClusterConfig, ClusterNodeConfig

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException


class ClusterClient(PolyaxonClient):
    """Client to get clusters from the server"""
    ENDPOINT = "/clusters"
    ENDPOINT_NODES = "/nodes"

    def list_clusters(self, page=1):
        """Fetch list of clusters related to authenticate user."""
        request_url = self._build_url(self._get_http_url())

        try:
            response = self.get(request_url, params=self.get_page(page=page))
            clusters_dict = response.json()
            return [PolyaxonClusterConfig.from_dict(cluster)
                    for cluster in clusters_dict.get("results", [])]
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving clusters')
            return []

    def get_cluster(self, cluster_uuid='default'):
        request_url = self._build_url(self._get_http_url(), cluster_uuid)
        try:
            response = self.get(request_url)
            return PolyaxonClusterConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving cluster')
            return None

    def get_node(self, node_uuid):
        request_url = self._build_url(self._get_http_url(self.ENDPOINT_NODES), node_uuid)
        try:
            response = self.get(request_url)
            return ClusterNodeConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving node')
            return None
