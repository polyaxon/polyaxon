# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

import clint
from polyaxon_schemas.polyaxonfile.logger import logger
from polyaxon_schemas.settings import RunTypes

from polyaxon_cli.cli.check import check_polyaxonfile
from polyaxon_cli.cli.version import get_version, PROJECT_NAME


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), help='The polyaxon file to check.')
@click.option('--experiment', '-x', type=int,
              help='Run specific experiment, if nothing passed all experiments will be run.')
def run(file, experiment):
    """Command for running polyaxonfile experiments."""
    plx_file = check_polyaxonfile(file)
    if plx_file.run_type == RunTypes.LOCAL:
        # check that polyaxon is installed
        version = get_version(PROJECT_NAME)
        if version is None:
            click.echo("""In order to run locally, polyaxon must be installed.""")
            if click.confirm("Do you want to install polyaxon now?"):
                from polyaxon_cli.cli.version import pip_upgrade
                pip_upgrade(PROJECT_NAME)
            else:
                clint.textui.puts("Your can manually run:")
                with clint.textui.indent(4):
                    clint.textui.puts("pip install -U polyaxon")
                clint.textui.puts("to install to the latest version of polyaxon")
                sys.exit(0)

        logger.info('Running polyaxonfile locally')
        from polyaxon.polyaxonfile.local_runner import run, run_experiment
        if experiment:
            run_experiment(file, experiment)
        else:
            run(file)

    else:
        from polyaxon_k8s.k8s.spawner import K8SSpawner
        spawner = K8SSpawner(polyaxonfile=plx_file)
        if experiment is not None:
            logger.info('Running experiment {} polyaxonfile on {}'.format(experiment,
                                                                          plx_file.run_type))
            spawner.create_experiment(experiment)
        else:
            logger.info('Running experiment all polyaxonfile on {}'.format(plx_file.run_type))
            spawner.create_all_experiments()

