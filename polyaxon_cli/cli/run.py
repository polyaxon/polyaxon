# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile
from polyaxon_schemas.polyaxonfile.logger import logger
from polyaxon_schemas.settings import RunTypes

from polyaxon_cli.cli.version import get_version, PROJECT_NAME


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), help='The polyaxon file to check.')
@click.option('--experiment', '-x', is_flag=True, default=False,
              help='Run specific experiment, if nothing passed all experiments will be run.')
def run(file, experiment):
    """Command for running a polyaxonfile."""
    plx_file = PolyaxonFile(file)
    if plx_file.run_type == RunTypes.LOCAL:
        # check that polyaxon is installed
        version = get_version(PROJECT_NAME)
        if version is None:
            click.echo("""In order to run locally, polyaxon must be installed.""")
            if click.confirm("Do you want to install polyaxon now?"):
                from polyaxon_cli.cli.version import pip_upgrade
                pip_upgrade(PROJECT_NAME)
            else:
                click.echo("""Your can manually run:
    pip install -U polyaxon
to install to the latest version of polyaxon)""")
                sys.exit(0)

        logger.info('Running polyaxonfile locally')
        from polyaxon.polyaxonfile.local_runner import run, run_experiment
        if experiment:
            run_experiment(file, experiment)
        else:
            run(file)

    else:
        from polyaxon_k8s.k8s.spawner import K8SSpawner
        manager = K8SSpawner(polyaxonfile=file)
        if experiment:
            manager.create_experiment(experiment)
        else:
            manager.create_all_experiments()

