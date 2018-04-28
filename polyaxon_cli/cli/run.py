# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.cli.check import check_polyaxonfile, get_group_experiments_info
from polyaxon_cli.cli.upload import upload
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer
from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ExperimentGroupConfig


@click.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon files to run.')
@click.option('--description', type=str,
              help='The description to give to this run.')
@click.option('-u', is_flag=True, default=False,
              help='To upload the repo before running.')
@click.pass_context
@clean_outputs
def run(ctx, file, description, u):  # pylint:disable=redefined-builtin
    """Run polyaxonfile specification.

    Example:

    \b
    ```bash
    $ polyaxon run -f file -f file_override ...
    ```

    Example: upload before running

    \b
    ```bash
    $ polyaxon run -f file -u
    ```

    """
    file = file or 'polyaxonfile.yml'
    specification = check_polyaxonfile(file, log=False).specification

    # Check if we need to upload
    if u:
        ctx.invoke(upload, async=False)

    project = ProjectManager.get_config_or_raise()
    project_client = PolyaxonClients().project

    if specification.is_experiment:
        click.echo('Creating an independent experiment.')
        experiment = ExperimentConfig(
            description=description,
            config=specification.parsed_data)
        try:
            project_client.create_experiment(project.user,
                                             project.name,
                                             experiment)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not create experiment.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        Printer.print_success('Experiment was created')
    else:
        click.echo('Creating an experiment group with the following definition:')
        experiments_def = specification.experiments_def
        get_group_experiments_info(**experiments_def)
        experiment_group = ExperimentGroupConfig(
            description=description,
            content=specification._data)  # pylint:disable=protected-access
        try:
            project_client.create_experiment_group(project.user,
                                                   project.name,
                                                   experiment_group)
            Printer.print_success('Experiment group was created')
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not create experiment group.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
