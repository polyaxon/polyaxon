# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.cli.check import check_polyaxonfile, check_polyaxonfile_kind
from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import (
    PolyaxonClientException,
    PolyaxonHTTPError,
    PolyaxonShouldExitError
)
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.schemas import kinds
from polyaxon_cli.utils import indentation
from polyaxon_cli.utils.formatting import Printer


def get_tensorboard_url(user, project_name, experiment=None, group=None):
    if experiment:
        return "{}/tensorboard/{}/{}/experiments/{}/\n".format(
            PolyaxonClient().api_config.http_host,
            user,
            project_name,
            experiment)
    if group:
        return "{}/tensorboard/{}/{}/groups/{}/\n".format(
            PolyaxonClient().api_config.http_host,
            user,
            project_name,
            group)
    return "{}/tensorboard/{}/{}/\n".format(PolyaxonClient().api_config.http_host,
                                            user,
                                            project_name)


@click.group()
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'.")
@click.option('--group', '-g', type=int, help="The group id number.")
@click.option('--experiment', '-xp', type=int, help="The experiment id number.")
@click.pass_context
@clean_outputs
def tensorboard(ctx, project, group, experiment):
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['group'] = group
    ctx.obj['experiment'] = experiment


@tensorboard.command()
@click.pass_context
@clean_outputs
def url(ctx):
    """Prints the tensorboard url for project/experiment/experiment group.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples for project tensorboards:

    \b
    ```bash
    $ polyaxon tensorboard url
    ```

    \b
    ```bash
    $ polyaxon tensorboard -p mnist url
    ```

    Examples for experiment tensorboards:

    \b
    ```bash
    $ polyaxon tensorboard -xp 1 url
    ```

    Examples for experiment group tensorboards:

    \b
    ```bash
    $ polyaxon tensorboard -g 1 url
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))
    group = ctx.obj.get('group')
    experiment = ctx.obj.get('experiment')
    if experiment:
        try:
            response = PolyaxonClient().experiment.get_experiment(
                username=user,
                project_name=project_name,
                experiment_id=experiment)
            obj = 'experiment {}'.format(experiment)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get experiment `{}`.'.format(experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    elif group:
        try:
            response = PolyaxonClient().experiment_group.get_experiment_group(
                username=user,
                project_name=project_name,
                group_id=group)
            obj = 'group `{}`.'.format(group)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get group `{}`.'.format(group))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    else:
        try:
            response = PolyaxonClient().project.get_project(
                username=user,
                project_name=project_name)
            obj = 'project `{}`.'.format(project_name)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get project `{}`.'.format(project_name))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    if response.has_tensorboard:
        click.echo(get_tensorboard_url(user=user,
                                       project_name=project_name,
                                       experiment=experiment,
                                       group=group))
    else:
        Printer.print_warning('This `{}` does not have a running tensorboard'.format(obj))
        click.echo('You can start tensorboard with this command: polyaxon tensorboard start --help')


@tensorboard.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon files to run.')
@click.pass_context
@clean_outputs
def start(ctx, file):  # pylint:disable=redefined-builtin
    """Start a tensorboard deployment for project/experiment/experiment group.

    Project tensorboard will aggregate all experiments under the project.

    Experiment group tensorboard will aggregate all experiments under the group.

    Experiment tensorboard will show all metrics for an experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example: using the default tensorflow image 1.4.1.

    \b
    ```bash
    $ polyaxon tensorboard start
    ```

    Example: with custom image and resources

    \b
    ```bash
    $ polyaxon tensorboard start -f file -f file_override ...
    ```

    Example: starting a tensorboard for an experiment group

    \b
    ```bash
    $ polyaxon tensorboard -g 1 start -f file
    ```

    Example: starting a tensorboard for an experiment

    \b
    ```bash
    $ polyaxon tensorboard -xp 112 start -f file
    ```
    """
    specification = None
    job_content = None
    if file:
        specification = check_polyaxonfile(file, log=False).specification

    if specification:
        # pylint:disable=protected-access
        check_polyaxonfile_kind(specification=specification, kind=kinds.TENSORBOARD)
        job_content = specification.raw_data

    user, project_name = get_project_or_local(ctx.obj.get('project'))
    group = ctx.obj.get('group')
    experiment = ctx.obj.get('experiment')
    if experiment:
        try:
            response = PolyaxonClient().experiment.start_tensorboard(
                username=user,
                project_name=project_name,
                experiment_id=experiment,
                content=job_content,
                is_managed=True,
            )
            obj = 'experiment `{}`'.format(experiment)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not start tensorboard experiment `{}`.'.format(experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    elif group:
        try:
            response = PolyaxonClient().experiment_group.start_tensorboard(
                username=user,
                project_name=project_name,
                group_id=group,
                content=job_content,
                is_managed=True,
            )
            obj = 'group `{}`'.format(group)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not start tensorboard group `{}`.'.format(group))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    else:
        try:
            response = PolyaxonClient().project.start_tensorboard(
                username=user,
                project_name=project_name,
                content=job_content,
                is_managed=True,
            )
            obj = 'project `{}`'.format(project_name)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not start tensorboard project `{}`.'.format(project_name))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    if response.status_code == 200:
        Printer.print_header("A tensorboard for this {} is already running on:".format(obj))
        click.echo(get_tensorboard_url(user=user,
                                       project_name=project_name,
                                       experiment=experiment,
                                       group=group))
        sys.exit(0)

    if response.status_code != 201:
        Printer.print_error('Something went wrong, Tensorboard was not created.')
        sys.exit(1)

    Printer.print_success('Tensorboard is being deployed for {}'.format(obj))
    indentation.puts("It may take some time before you can access tensorboard.\n")
    indentation.puts("Your tensorboard will be available on:\n")
    with indentation.indent(4):
        indentation.puts(get_tensorboard_url(user, project_name, experiment, group))


@tensorboard.command()
@click.option('--yes', '-y', is_flag=True, default=False,
              help='Automatic yes to prompts. '
                   'Assume "yes" as answer to all prompts and run non-interactively.')
@click.pass_context
@clean_outputs
def stop(ctx, yes):
    """Stops the tensorboard deployment for project/experiment/experiment group if it exists.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples: stopping project tensorboard

    \b
    ```bash
    $ polyaxon tensorboard stop
    ```

    Examples: stopping experiment group tensorboard

    \b
    ```bash
    $ polyaxon tensorboard -g 1 stop
    ```

    Examples: stopping experiment tensorboard

    \b
    ```bash
    $ polyaxon tensorboard -xp 112 stop
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))
    group = ctx.obj.get('group')
    experiment = ctx.obj.get('experiment')

    if experiment:
        obj = 'experiment `{}`'.format(experiment)
    elif group:
        obj = 'group `{}`'.format(group)
    else:
        obj = 'project `{}/{}`'.format(user, project_name)

    if not yes and not click.confirm("Are sure you want to stop tensorboard "
                                     "for {}".format(obj)):
        click.echo('Existing without stopping tensorboard.')
        sys.exit(1)

    if experiment:
        try:
            PolyaxonClient().experiment.stop_tensorboard(
                username=user,
                project_name=project_name,
                experiment_id=experiment)
            Printer.print_success('Tensorboard is being deleted')
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not stop tensorboard {}.'.format(obj))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    elif group:
        try:
            PolyaxonClient().experiment_group.stop_tensorboard(
                username=user,
                project_name=project_name,
                group_id=group)
            Printer.print_success('Tensorboard is being deleted')
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not stop tensorboard {}.'.format(obj))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    else:
        try:
            PolyaxonClient().project.stop_tensorboard(
                username=user,
                project_name=project_name)
            Printer.print_success('Tensorboard is being deleted')
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not stop tensorboard {}.'.format(obj))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
