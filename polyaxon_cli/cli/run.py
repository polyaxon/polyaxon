# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

import click
from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ExperimentGroupConfig

from polyaxon_cli.cli.check import check_polyaxonfile
from polyaxon_cli.cli.project import get_current_project
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer, dict_tabulate


@click.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon files to run.')
@click.option('--name', '-n', type=click.Path(exists=True),
              help='The name to give to this run.')
@click.option('--description', '-n', type=click.Path(exists=True),
              help='The description to give to this run.')
def run(file, name, description):
    """Command for running polyaxonfile specification.

    Example:

    ```
    polyaxon run -f file -f file_override ...
    ```
    """
    name = name or uuid.uuid4().hex
    file = file or 'polyaxonfile.yml'
    project = get_current_project()
    plx_file = check_polyaxonfile(file)
    num_experiments, concurrency = plx_file.experiments_def
    project_client = PolyaxonClients().project
    if num_experiments == 1:
        click.echo('Creating an independent experiment.')
        experiment = ExperimentConfig(name=name,
                                      description=description,
                                      content=plx_file._data,
                                      config=plx_file.experiment_specs[0].parsed_data)
        response = project_client.create_experiment(project.uuid.hex, experiment)
        Printer.print_success('Experiment was created')
    else:
        click.echo('Creating an experiment group with {} experiments.'.format(num_experiments))
        experiment_group = ExperimentGroupConfig(name=name,
                                                 description=description,
                                                 content=plx_file._data)
        response = project_client.create_experiment_group(project.uuid.hex, experiment_group)
        Printer.print_success('Experiment group was created')

    response = response.to_dict()
    dict_tabulate(response)
