# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ExperimentGroupConfig

from polyaxon_cli.cli.check import check_polyaxonfile, get_group_experiments_info
from polyaxon_cli.cli.project import equal_projects
from polyaxon_cli.cli.upload import upload
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer


@click.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon files to run.')
@click.option('--description', type=str,
              help='The description to give to this run.')
@click.option('-u', is_flag=True, default=False,
              help='To upload the repo before running.')
@click.pass_context
def run(ctx, file, description, u):
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
    plx_file = check_polyaxonfile(file, log=False)

    # Check if we need to upload
    if u:
        ctx.invoke(upload, async=False)

    matrix_space, n_experiments, concurrency, search_method = plx_file.experiments_def
    project = ProjectManager.get_config_or_raise()
    project_client = PolyaxonClients().project
    if not equal_projects(plx_file.project.name, project.unique_name):
        Printer.print_error('Your polyaxonfile defined a different project '
                            'than the one set in this repo.')
        sys.exit(1)
    if matrix_space == 1:
        click.echo('Creating an independent experiment.')
        experiment = ExperimentConfig(description=description,
                                      content=plx_file._data,
                                      config=plx_file.experiment_specs[0].parsed_data)
        try:
            response = project_client.create_experiment(project.user,
                                                        project.name,
                                                        experiment)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not create experiment.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
        Printer.print_success('Experiment was created')
    else:
        click.echo('Creating an experiment group with the following definition:')
        get_group_experiments_info(matrix_space, n_experiments, concurrency, search_method)
        experiment_group = ExperimentGroupConfig(description=description,
                                                 content=plx_file._data)
        try:
            response = project_client.create_experiment_group(project.user,
                                                              project.name,
                                                              experiment_group)
            Printer.print_success('Experiment group was created')
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not create experiment group.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
