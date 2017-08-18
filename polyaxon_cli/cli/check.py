# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile

from polyaxon_cli.logging import logger


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), help='The polyaxon file to check.')
@click.option('--version', is_flag=True, default=False, help='Checks and prints the version.')
@click.option('--cluster', is_flag=True, default=False, help='Checks and prints the cluster def.')
@click.option('--run-type', is_flag=True, default=False, help='Checks and prints the run_type.')
def check(file, version, cluster, run_type):
    """Command for checking a polyaxonfile."""
    plx_file = PolyaxonFile(file)
    logger.info("Polyaxonfile valid")

    if version:
        logger.info('The version is: {}'.format(plx_file.version))

    elif cluster:
        cluster_def, is_distributed = plx_file.cluster_def
        logger.info('The cluster definition is: {}'.format(cluster_def))

    elif run_type:
        logger.info('The run_type is: {}'.format(plx_file.run_type))

    else:
        logger.info('Validated file:\n{}'.format(plx_file.parsed_data))
