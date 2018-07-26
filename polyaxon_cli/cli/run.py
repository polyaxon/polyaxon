# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.cli.check import check_polyaxonfile, get_group_experiments_info
from polyaxon_cli.cli.upload import upload
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.build_job import BuildJobManager
from polyaxon_cli.managers.experiment import ExperimentManager
from polyaxon_cli.managers.experiment_group import GroupManager
from polyaxon_cli.managers.job import JobManager
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils import cache
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer
from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.job import JobConfig
from polyaxon_schemas.project import ExperimentGroupConfig


@click.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon files to run.')
@click.option('--name', type=str,
              help='Name to give to this run, must be unique within the project, could be none.')
@click.option('--description', type=str,
              help='The description to give to this run.')
@click.option('--tags', type=str, help='Tags of this run, comma separated values.')
@click.option('-u', is_flag=True, default=False,
              help='To upload the repo before running.')
@click.pass_context
@clean_outputs
def run(ctx, file, name, tags, description, u):  # pylint:disable=redefined-builtin
    """Run polyaxonfile specification.

    Examples:

    \b
    ```bash
    $ polyaxon run -f file -f file_override ...
    ```

    Upload before running

    \b
    ```bash
    $ polyaxon run -f file -u
    ```

    Run and set description and tags for this run

    \b
    ```bash
    $ polyaxon run -f file -u --description="Description of the current run" --tags="foo, bar, moo"
    ```
    Run and set a unique name for this run

    \b
    ```bash
    polyaxon run --name=foo
    ```
    """
    file = file or 'polyaxonfile.yml'
    specification = check_polyaxonfile(file, log=False).specification

    spec_cond = (specification.is_experiment or
                 specification.is_group or
                 specification.is_job or
                 specification.is_build)
    if not spec_cond:
        Printer.print_error(
            'This command expects an experiment, a group, a job, or a build specification,'
            'received instead a `{}` specification'.format(specification.kind))
        if specification.is_notebook:
            click.echo('Please check "polyaxon notebook --help" to start a notebook.')
        elif specification.is_tensorboard:
            click.echo('Please check: "polyaxon tensorboard --help" to start a tensorboard.')
        sys.exit(1)

    # Check if we need to upload
    if u:
        ctx.invoke(upload, async=False)

    project = ProjectManager.get_config_or_raise()
    project_client = PolyaxonClients().project

    if tags:
        tags = tags.split(',')

    def run_experiment():
        click.echo('Creating an independent experiment.')
        experiment = ExperimentConfig(
            name=name,
            description=description,
            tags=tags,
            config=specification.parsed_data)
        try:
            response = PolyaxonClients().project.create_experiment(project.user,
                                                                   project.name,
                                                                   experiment)
            cache.cache(config_manager=ExperimentManager, response=response)
            Printer.print_success('Experiment `{}` was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not create experiment.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def run_group():
        click.echo('Creating an experiment group with the following definition:')
        experiments_def = specification.experiments_def
        get_group_experiments_info(**experiments_def)
        experiment_group = ExperimentGroupConfig(
            name=name,
            description=description,
            tags=tags,
            content=specification._data)  # pylint:disable=protected-access
        try:
            response = project_client.create_experiment_group(project.user,
                                                              project.name,
                                                              experiment_group)
            cache.cache(config_manager=GroupManager, response=response)
            Printer.print_success('Experiment group {} was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not create experiment group.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def run_job():
        click.echo('Creating a job.')
        job = JobConfig(
            name=name,
            description=description,
            tags=tags,
            config=specification.parsed_data)
        try:
            response = project_client.create_job(project.user,
                                                 project.name,
                                                 job)
            cache.cache(config_manager=JobManager, response=response)
            Printer.print_success('Job {} was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not create job.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def run_build():
        click.echo('Creating a build.')
        job = JobConfig(
            name=name,
            description=description,
            tags=tags,
            config=specification.parsed_data)
        try:
            response = project_client.create_build(project.user,
                                                   project.name,
                                                   job)
            cache.cache(config_manager=BuildJobManager, response=response)
            Printer.print_success('Build {} was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not create build.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    if specification.is_experiment:
        run_experiment()
    elif specification.is_group:
        run_group()
    elif specification.is_job:
        run_job()
    elif specification.is_build:
        run_build()
