# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_schemas.settings import RunTypes

from polyaxon_cli.cli.check import check_polyaxonfile


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), help='The polyaxon file to check.')
@click.option('--experiment', '-x', type=int, required=True,
              help='Run specific experiment, if nothing passed all experiments will be run.')
def logs(file, experiment):
    """Command for stopping polyaxonfile experiments."""
    plx_file = check_polyaxonfile(file)
    if plx_file.run_type != RunTypes.LOCAL:
        from polyaxon_k8s.k8s.spawner import K8SSpawner
        spawner = K8SSpawner(polyaxonfile=plx_file)
        click.echo(spawner.get_task_log(experiment, 'master', 0))

