# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
from clint.textui import colored
from polyaxon_k8s.k8s.templates.pods import PodStatus

from polyaxon_schemas.polyaxonfile.logger import logger
from polyaxon_schemas.settings import RunTypes

from polyaxon_cli.cli.check import check_polyaxonfile


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), help='The polyaxon file to check.')
@click.option('--experiment', '-x', type=int, required=True,
              help='Run specific experiment, if nothing passed all experiments will be run.')
def status(file, experiment):
    """Command for stopping polyaxonfile experiments."""
    plx_file = check_polyaxonfile(file)
    if plx_file.run_type != RunTypes.LOCAL:
        from polyaxon_k8s.k8s.spawner import K8SSpawner
        spawner = K8SSpawner(polyaxonfile=plx_file)
        status = spawner.get_experiment_status(experiment)
        message = "Experiment {} polyaxonfile on {} is {}"
        if status == PodStatus.FAILED:
            message = colored.red(message)
        elif status in (PodStatus.PENDING, PodStatus.CONTAINER_CREATING):
            message = colored.yellow(message)
        elif status == PodStatus.RUNNING:
            message = colored.yellow(message)
        elif status == PodStatus.SUCCEEDED:
            message = colored.green(message)

        logger.info(message.format(experiment, plx_file.run_type, status))

