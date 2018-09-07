# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.utils.formatting import Printer, dict_tabulate, list_dicts_to_tabulate
from polyaxon_client.exceptions import PolyaxonClientException


def get_cluster_info(cluster_config):
    Printer.print_header("Cluster info:")
    cluster_dict = cluster_config.to_light_dict()
    cluster_info = cluster_dict['version_api']
    dict_tabulate(cluster_info)

    nodes = list_dicts_to_tabulate([Printer.add_memory_unit(node.to_light_dict(), 'memory')
                                    for node in cluster_config.nodes])

    if nodes:
        Printer.print_header("Cluster Nodes:")
        nodes.pop('status', None)
        nodes.pop('kernel_version', None)
        dict_tabulate(nodes, is_list_dict=True)


def get_node_info(node_config):
    if not node_config:
        Printer.print_error('No node was found.')
        sys.exit(1)
    node = node_config.to_dict()
    node.pop('gpus')
    Printer.print_header("Node info:")
    dict_tabulate(Printer.add_memory_unit(node, 'memory'))

    gpus_items = list_dicts_to_tabulate([Printer.add_memory_unit(gpu.to_light_dict(), 'memory')
                                         for gpu in node_config.gpus])

    if gpus_items:
        Printer.print_header("Node GPUs:")
        dict_tabulate(gpus_items, is_list_dict=True)


@click.command()
@click.option('--node', '-n', type=int, help='Get information about a node.')
@clean_outputs
def cluster(node):
    """Get cluster and nodes info."""
    cluster_client = PolyaxonClient().cluster
    if node:
        try:
            node_config = cluster_client.get_node(node)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not load node `{}` info.'.format(node))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        get_node_info(node_config)
    else:
        try:
            cluster_config = cluster_client.get_cluster()
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not load cluster info.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        get_cluster_info(cluster_config)
