# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import click
import six

from tabulate import tabulate

from polyaxon_cli.utils.clients import PolyaxonClients


def get_cluster_info(cluster_config):
    click.secho("Cluster info:", fg='yellow')
    cluster_info = cluster_config.version_api
    items = six.iteritems(cluster_info)
    click.echo(tabulate(items))

    nodes = OrderedDict()
    for node in cluster_config.nodes:
        node = node.to_dict()
        for k, v in six.iteritems(node):
            if k in nodes:
                nodes[k].append(v)
            else:
                nodes[k] = [v]

    if nodes:
        click.secho("Cluster Nodes:", fg='yellow')
        click.echo(tabulate(nodes, headers="keys"))


def get_node_info(node_config):
    node = node_config.to_dict()
    gpus = node.pop('gpus', [])
    click.secho("Node info:", fg='yellow')
    items = six.iteritems(node)
    click.echo(tabulate(list(items)))

    click.secho("Node GPUs:", fg='yellow')
    gpus_items = OrderedDict()
    for gpu in gpus:
        for k, v in six.iteritems(gpu):
            if k in gpus_items:
                gpus_items[k].append(v)
            else:
                gpus_items[k] = [v]

    if gpus_items:
        headers = six.iterkeys(gpu)
        # remove the cluster_node uuid
        gpus_items.pop('cluster_node')
        click.echo(tabulate(gpus_items, headers=headers))


@click.command()
@click.option('--node', type=str)
def cluster(node):
    """Get cluster and nodes info."""
    cluster_client = PolyaxonClients().cluster
    if node:
        node_config = cluster_client.get_node(node)
        get_node_info(node_config)
    else:
        cluster_config = cluster_client.get_cluster()
        get_cluster_info(cluster_config)
