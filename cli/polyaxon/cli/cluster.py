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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon.cli.errors import handle_cli_error
from polyaxon.client import PolyaxonClient
from polyaxon.exceptions import (
    PolyaxonClientException,
    PolyaxonHTTPError,
    PolyaxonShouldExitError,
)
from polyaxon.logger import clean_outputs
from polyaxon.utils.formatting import Printer, dict_tabulate, list_dicts_to_tabulate


def get_cluster_info(cluster_config):
    Printer.print_header("Cluster info:")
    cluster_dict = cluster_config.to_light_dict()
    cluster_info = cluster_dict["version_api"]
    dict_tabulate(cluster_info)

    nodes = list_dicts_to_tabulate(
        [
            Printer.add_memory_unit(node.to_light_dict(), "memory")
            for node in cluster_config.nodes
        ]
    )

    if nodes:
        Printer.print_header("Cluster Nodes:")
        nodes.pop("status", None)
        nodes.pop("kernel_version", None)
        dict_tabulate(nodes, is_list_dict=True)


def get_node_info(node_config):
    if not node_config:
        Printer.print_error("No node was found.")
        sys.exit(1)
    node = node_config.to_dict()
    node.pop("gpus")
    Printer.print_header("Node info:")
    dict_tabulate(Printer.add_memory_unit(node, "memory"))

    gpus_items = list_dicts_to_tabulate(
        [
            Printer.add_memory_unit(gpu.to_light_dict(), "memory")
            for gpu in node_config.gpus
        ]
    )

    if gpus_items:
        Printer.print_header("Node GPUs:")
        dict_tabulate(gpus_items, is_list_dict=True)


@click.command()
@click.option("--node", "-n", type=int, help="Get information about a node.")
@clean_outputs
def cluster(node):
    """Get cluster and nodes info."""
    cluster_client = PolyaxonClient().cluster
    if node:
        try:
            node_config = cluster_client.get_node(node)
        except (
            PolyaxonHTTPError,
            PolyaxonShouldExitError,
            PolyaxonClientException,
        ) as e:
            handle_cli_error(e, message="Could not load node `{}` info.".format(node))
            sys.exit(1)
        get_node_info(node_config)
    else:
        try:
            cluster_config = cluster_client.get_cluster()
        except (
            PolyaxonHTTPError,
            PolyaxonShouldExitError,
            PolyaxonClientException,
        ) as e:
            handle_cli_error(e, message="Could not load cluster info.")
            sys.exit(1)
        get_cluster_info(cluster_config)
