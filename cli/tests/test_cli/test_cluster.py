#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# # coding: utf-8
# from __future__ import absolute_import, division, print_function
#
# import pytest
# from mock import patch
# from tests.test_cli.utils import BaseCommandTestCase
#
# from polyaxon.cli.cluster import cluster
#
#
# @pytest.mark.cli_mark
# class TestCliCluster(BaseCommandTestCase): TODO
#     @patch("polyaxon.client.api.cluster.ClusterApi.get_cluster")
#     @patch("polyaxon.cli.cluster.get_cluster_info")
#     def test_get_cluster(self, get_cluster_info, get_cluster):
#         self.runner.invoke(cluster)
#         get_cluster.assert_called_once()
#         get_cluster_info.assert_called_once()
#
#     @patch("polyaxon.client.api.cluster.ClusterApi.get_node")
#     @patch("polyaxon.cli.cluster.get_node_info")
#     def test_get_node(self, get_node_info, get_node):
#         self.runner.invoke(cluster, ["--node=1"])
#         get_node.assert_called_once()
#         get_node_info.assert_called_once()
