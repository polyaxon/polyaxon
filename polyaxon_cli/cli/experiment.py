# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click
import rhea

from polyaxon_cli.cli.getters.experiment import (
    get_experiment_job_or_local,
    get_project_experiment_or_local
)
from polyaxon_cli.cli.upload import upload
from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import (
    PolyaxonClientException,
    PolyaxonHTTPError,
    PolyaxonShouldExitError
)
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.experiment import ExperimentManager
from polyaxon_cli.managers.experiment_job import ExperimentJobManager
from polyaxon_cli.utils import cache
from polyaxon_cli.utils.formatting import (
    Printer,
    dict_tabulate,
    get_meta_response,
    get_resources,
    list_dicts_to_tabulate
)
from polyaxon_cli.utils.log_handler import get_logs_handler
from polyaxon_cli.utils.validation import validate_tags


def get_experiment_details(experiment):  # pylint:disable=redefined-outer-name
    if experiment.description:
        Printer.print_header("Experiment description:")
        click.echo('{}\n'.format(experiment.description))

    if experiment.resources:
        get_resources(experiment.resources.to_dict(), header="Experiment resources:")

    if experiment.params:
        Printer.print_header("Experiment params:")
        dict_tabulate(experiment.params)

    if experiment.last_metric:
        Printer.print_header("Experiment last metrics:")
        dict_tabulate(experiment.last_metric)

    response = experiment.to_light_dict(
        humanize_values=True,
        exclude_attrs=[
            'uuid', 'config', 'project', 'experiments', 'description',
            'params', 'last_metric', 'resources', 'jobs', 'run_env'
        ])

    Printer.print_header("Experiment info:")
    dict_tabulate(Printer.add_status_color(response))


@click.group()
@click.option('--project', '-p', type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'.")
@click.option('--experiment', '-xp', type=int, help="The experiment id number.")
@click.pass_context
@clean_outputs
def experiment(ctx, project, experiment):  # pylint:disable=redefined-outer-name
    """Commands for experiments."""
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['experiment'] = experiment


@experiment.command()
@click.option('--job', '-j', type=int, help="The job id.")
@click.pass_context
@clean_outputs
def get(ctx, job):
    """Get experiment or experiment job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples for getting an experiment:

    \b
    ```bash
    $ polyaxon experiment get  # if experiment is cached
    ```

    \b
    ```bash
    $ polyaxon experiment --experiment=1 get
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 --project=cats-vs-dogs get
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 -p alain/cats-vs-dogs get
    ```

    Examples for getting an experiment job:

    \b
    ```bash
    $ polyaxon experiment get -j 1  # if experiment is cached
    ```

    \b
    ```bash
    $ polyaxon experiment --experiment=1 get --job=10
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 --project=cats-vs-dogs get -j 2
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 -p alain/cats-vs-dogs get -j 2
    ```
    """

    def get_experiment():
        try:
            response = PolyaxonClient().experiment.get_experiment(user, project_name, _experiment)
            cache.cache(config_manager=ExperimentManager, response=response)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not load experiment `{}` info.'.format(_experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        get_experiment_details(response)

    def get_experiment_job():
        try:
            response = PolyaxonClient().experiment_job.get_job(user,
                                                               project_name,
                                                               _experiment,
                                                               _job)
            cache.cache(config_manager=ExperimentJobManager, response=response)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get job `{}`.'.format(_job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        if response.resources:
            get_resources(response.resources.to_dict(), header="Job resources:")

        response = Printer.add_status_color(response.to_light_dict(
            humanize_values=True,
            exclude_attrs=['uuid', 'definition', 'experiment', 'unique_name', 'resources']
        ))
        Printer.print_header("Job info:")
        dict_tabulate(response)

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job()
    else:
        get_experiment()


@experiment.command()
@click.pass_context
@clean_outputs
def delete(ctx):
    """Delete experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon experiment delete
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    if not click.confirm("Are sure you want to delete experiment `{}`".format(_experiment)):
        click.echo('Existing without deleting experiment.')
        sys.exit(1)

    try:
        response = PolyaxonClient().experiment.delete_experiment(
            user, project_name, _experiment)
        # Purge caching
        ExperimentManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not delete experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Experiment `{}` was delete successfully".format(_experiment))


@experiment.command()
@click.option('--name', type=str,
              help='Name of the experiment, must be unique within the project, could be none.')
@click.option('--description', type=str, help='Description of the experiment.')
@click.option('--tags', type=str, help='Tags of the experiment, comma separated values.')
@click.pass_context
@clean_outputs
def update(ctx, name, description, tags):
    """Update experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment -xp 2 update --description="new description for my experiments"
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 2 update --tags="foo, bar" --name="unique-name"
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    update_dict = {}

    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    tags = validate_tags(tags)
    if tags:
        update_dict['tags'] = tags

    if not update_dict:
        Printer.print_warning('No argument was provided to update the experiment.')
        sys.exit(0)

    try:
        response = PolyaxonClient().experiment.update_experiment(
            user, project_name, _experiment, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not update experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment updated.")
    get_experiment_details(response)


@experiment.command()
@click.option('--yes', '-y', is_flag=True, default=False,
              help="Automatic yes to prompts. "
                   "Assume \"yes\" as answer to all prompts and run non-interactively.")
@click.pass_context
@clean_outputs
def stop(ctx, yes):
    """Stop experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment stop
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 2 stop
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    if not yes and not click.confirm("Are sure you want to stop "
                                     "experiment `{}`".format(_experiment)):
        click.echo('Existing without stopping experiment.')
        sys.exit(0)

    try:
        PolyaxonClient().experiment.stop(user, project_name, _experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not stop experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment is being stopped.")


@experiment.command()
@click.option('--copy', '-c', is_flag=True, default=False,
              help="To copy the experiment before restarting.")
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help="The polyaxon files to update with.")
@click.option('-u', is_flag=True, default=False,
              help="To upload the repo before restarting.")
@click.pass_context
@clean_outputs
def restart(ctx, copy, file, u):  # pylint:disable=redefined-builtin
    """Restart experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment --experiment=1 restart
    ```
    """
    content = None
    update_code = None
    if file:
        content = '{}'.format(rhea.read(file))

    # Check if we need to upload
    if u:
        ctx.invoke(upload, sync=False)
        update_code = True

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    try:
        if copy:
            response = PolyaxonClient().experiment.copy(
                user, project_name, _experiment, content=content, update_code=update_code)
            Printer.print_success('Experiment was copied with id {}'.format(response.id))
        else:
            response = PolyaxonClient().experiment.restart(
                user, project_name, _experiment, content=content, update_code=update_code)
            Printer.print_success('Experiment was restarted with id {}'.format(response.id))
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not restart experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@experiment.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help="The polyaxon files to update with.")
@click.option('-u', is_flag=True, default=False,
              help="To upload the repo before resuming.")
@click.pass_context
@clean_outputs
def resume(ctx, file, u):  # pylint:disable=redefined-builtin
    """Resume experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment --experiment=1 resume
    ```
    """
    content = None
    update_code = None
    if file:
        content = '{}'.format(rhea.read(file))

    # Check if we need to upload
    if u:
        ctx.invoke(upload, sync=False)
        update_code = True

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    try:
        response = PolyaxonClient().experiment.resume(
            user, project_name, _experiment, content=content, update_code=update_code)
        Printer.print_success('Experiment was resumed with id {}'.format(response.id))
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not resume experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


@experiment.command()
@click.option('--page', type=int, help="To paginate through the list of jobs.")
@click.pass_context
@clean_outputs
def jobs(ctx, page):
    """List jobs for experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment --experiment=1 jobs
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    page = page or 1
    try:
        response = PolyaxonClient().experiment.list_jobs(
            user, project_name, _experiment, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get jobs for experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Jobs for experiment `{}`.'.format(_experiment))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No jobs found for experiment `{}`.'.format(_experiment))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Jobs:")
        objects.pop('experiment', None)
        dict_tabulate(objects, is_list_dict=True)


@experiment.command()
@click.option('--job', '-j', type=int, help="The job id.")
@click.option('--page', type=int, help="To paginate through the list of statuses.")
@click.pass_context
@clean_outputs
def statuses(ctx, job, page):
    """Get experiment or experiment job statuses.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples getting experiment statuses:

    \b
    ```bash
    $ polyaxon experiment statuses
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 statuses
    ```

    Examples getting experiment job statuses:

    \b
    ```bash
    $ polyaxon experiment statuses -j 3
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 statuses --job 1
    ```
    """

    def get_experiment_statuses():
        try:
            response = PolyaxonClient().experiment.get_statuses(
                user, project_name, _experiment, page=page)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could get status for experiment `{}`.'.format(_experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        meta = get_meta_response(response)
        if meta:
            Printer.print_header('Statuses for experiment `{}`.'.format(_experiment))
            Printer.print_header('Navigation:')
            dict_tabulate(meta)
        else:
            Printer.print_header('No statuses found for experiment `{}`.'.format(_experiment))

        objects = list_dicts_to_tabulate(
            [Printer.add_status_color(o.to_light_dict(humanize_values=True), status_key='status')
             for o in response['results']])
        if objects:
            Printer.print_header("Statuses:")
            objects.pop('experiment', None)
            dict_tabulate(objects, is_list_dict=True)

    def get_experiment_job_statuses():
        try:
            response = PolyaxonClient().experiment_job.get_statuses(user,
                                                                    project_name,
                                                                    _experiment,
                                                                    _job,
                                                                    page=page)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get status for job `{}`.'.format(job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        meta = get_meta_response(response)
        if meta:
            Printer.print_header('Statuses for Job `{}`.'.format(_job))
            Printer.print_header('Navigation:')
            dict_tabulate(meta)
        else:
            Printer.print_header('No statuses found for job `{}`.'.format(_job))

        objects = list_dicts_to_tabulate(
            [Printer.add_status_color(o.to_light_dict(humanize_values=True), status_key='status')
             for o in response['results']])
        if objects:
            Printer.print_header("Statuses:")
            objects.pop('job', None)
            dict_tabulate(objects, is_list_dict=True)

    page = page or 1

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job_statuses()
    else:
        get_experiment_statuses()


@experiment.command()
@click.option('--job', '-j', type=int, help="The job id.")
@click.option('--gpu', '-g', is_flag=True, help="List experiment GPU resources.")
@click.pass_context
@clean_outputs
def resources(ctx, job, gpu):
    """Get experiment or experiment job resources.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples for getting experiment resources:

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources --gpu
    ```

    Examples for getting experiment job resources:

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources -j 1
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources -j 1 --gpu
    ```
    """

    def get_experiment_resources():
        try:
            message_handler = Printer.gpu_resources if gpu else Printer.resources
            PolyaxonClient().experiment.resources(
                user, project_name, _experiment, message_handler=message_handler)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get resources for experiment `{}`.'.format(_experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def get_experiment_job_resources():
        try:
            message_handler = Printer.gpu_resources if gpu else Printer.resources
            PolyaxonClient().experiment_job.resources(user,
                                                      project_name,
                                                      _experiment,
                                                      _job,
                                                      message_handler=message_handler)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get resources for job `{}`.'.format(_job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job_resources()
    else:
        get_experiment_resources()


@experiment.command()
@click.option('--job', '-j', type=int, help="The job id.")
@click.option('--past', '-p', is_flag=True, help="Show the past logs.")
@click.option('--follow', '-f', is_flag=True, default=False,
              help="Stream logs after showing past logs.")
@click.option('--hide_time', is_flag=True, default=False,
              help="Whether or not to hide timestamps from the log stream.")
@click.pass_context
@clean_outputs
def logs(ctx, job, past, follow, hide_time):
    """Get experiment or experiment job logs.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples for getting experiment logs:

    \b
    ```bash
    $ polyaxon experiment logs
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 10 -p mnist logs
    ```

    Examples for getting experiment job logs:

    \b
    ```bash
    $ polyaxon experiment -xp 1 -j 1 logs
    ```
    """

    def get_experiment_logs():
        if past:
            try:
                response = PolyaxonClient().experiment.logs(
                    user, project_name, _experiment, stream=False)
                get_logs_handler(handle_job_info=True,
                                 show_timestamp=not hide_time,
                                 stream=False)(response.content.decode().split('\n'))
                print()

                if not follow:
                    return
            except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
                if not follow:
                    Printer.print_error(
                        'Could not get logs for experiment `{}`.'.format(_experiment))
                    Printer.print_error(
                        'Error message `{}`.'.format(e))
                    sys.exit(1)

        try:
            PolyaxonClient().experiment.logs(
                user,
                project_name,
                _experiment,
                message_handler=get_logs_handler(handle_job_info=True,
                                                 show_timestamp=not hide_time))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get logs for experiment `{}`.'.format(_experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def get_experiment_job_logs():
        if past:
            try:
                response = PolyaxonClient().experiment_job.logs(
                    user,
                    project_name,
                    _experiment,
                    _job,
                    stream=False)
                get_logs_handler(handle_job_info=True,
                                 show_timestamp=not hide_time,
                                 stream=False)(response.content.decode().split('\n'))
                print()

                if not follow:
                    return
            except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
                if not follow:
                    Printer.print_error(
                        'Could not get logs for experiment `{}`.'.format(_experiment))
                    Printer.print_error(
                        'Error message `{}`.'.format(e))
                    sys.exit(1)

        try:
            PolyaxonClient().experiment_job.logs(
                user,
                project_name,
                _experiment,
                _job,
                message_handler=get_logs_handler(handle_job_info=True,
                                                 show_timestamp=not hide_time))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get logs for job `{}`.'.format(_job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job_logs()
    else:
        get_experiment_logs()


@experiment.command()
@click.pass_context
@clean_outputs
def outputs(ctx):
    """Download outputs for experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment -xp 1 outputs
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    try:
        PolyaxonClient().experiment.download_outputs(user, project_name, _experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not download outputs for experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
    Printer.print_success('Files downloaded.')


@experiment.command()
@click.pass_context
@clean_outputs
def bookmark(ctx):
    """Bookmark experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment bookmark
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 2 bookmark
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    try:
        PolyaxonClient().experiment.bookmark(user, project_name, _experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not bookmark experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment is bookmarked.")


@experiment.command()
@click.pass_context
@clean_outputs
def unbookmark(ctx):
    """Unbookmark experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment unbookmark
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 2 unbookmark
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    try:
        PolyaxonClient().experiment.unbookmark(user, project_name, _experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not unbookmark experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment is unbookmarked.")
