# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon.cli.cluster import cluster


class TestCluster(BaseCommandTestCase):
    @patch("polyaxon.client.api.cluster.ClusterApi.get_cluster")
    @patch("polyaxon.cli.cluster.get_cluster_info")
    def test_get_cluster(self, get_cluster_info, get_cluster):
        self.runner.invoke(cluster)
        get_cluster.assert_called_once()
        get_cluster_info.assert_called_once()

    @patch("polyaxon.client.api.cluster.ClusterApi.get_node")
    @patch("polyaxon.cli.cluster.get_node_info")
    def test_get_node(self, get_node_info, get_node):
        self.runner.invoke(cluster, ["--node=1"])
        get_node.assert_called_once()
        get_node_info.assert_called_once()
