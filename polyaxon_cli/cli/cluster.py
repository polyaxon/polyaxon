# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError

from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer, list_dicts_to_tabulate, dict_tabulate


def get_cluster_info(cluster_config):
    Printer.print_header("Cluster info:")
    cluster_dict = cluster_config.to_dict()
    cluster_info = cluster_dict['version_api']
    dict_tabulate(cluster_info)

    nodes = list_dicts_to_tabulate(cluster_dict['nodes'])

    if nodes:
        Printer.print_header("Cluster Nodes:")
        dict_tabulate(nodes, is_list_dict=True)


def get_node_info(node_config):
    if not node_config:
        Printer.print_error('No node was found.')
        sys.exit(1)
    node = node_config.to_dict()
    gpus = node.pop('gpus', [])
    Printer.print_header("Node info:")
    dict_tabulate(node)

    gpus_items = list_dicts_to_tabulate(gpus)

    if gpus_items:
        Printer.print_header("Node GPUs:")
        gpus_items.pop('cluster_node')
        dict_tabulate(gpus_items, is_list_dict=True)


@click.command()
@click.option('--node', type=str)
def cluster(node):
    """Get cluster and nodes info."""
    cluster_client = PolyaxonClients().cluster
    if node:
        try:
            node_config = cluster_client.get_node(node)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not load node `{}` info.'.format(node))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        get_node_info(node_config)
    else:
        try:
            cluster_config = cluster_client.get_cluster()
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not load cluster info.'.format(node))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        get_cluster_info(cluster_config)
