# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.cli.build import logs as build_logs
from polyaxon_cli.cli.check import get_group_experiments_info
from polyaxon_cli.cli.experiment import logs as experiment_logs
from polyaxon_cli.cli.job import logs as job_logs
from polyaxon_cli.cli.upload import upload as upload_cmd
from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_cli.managers.build_job import BuildJobManager
from polyaxon_cli.managers.experiment import ExperimentManager
from polyaxon_cli.managers.experiment_group import GroupManager
from polyaxon_cli.managers.job import JobManager
from polyaxon_cli.schemas import BuildJobConfig, ExperimentConfig, GroupConfig, JobConfig
from polyaxon_cli.utils import cache
from polyaxon_cli.utils.formatting import Printer
from polyaxon_client.exceptions import PolyaxonClientException


def run(ctx,
        name,
        user,
        project_name,
        description,
        tags,
        specification,
        ttl,
        upload,
        log,
        can_upload):
    project_client = PolyaxonClient().project

    def run_experiment():
        click.echo('Creating an independent experiment.')
        experiment = ExperimentConfig(
            name=name,
            description=description,
            tags=tags,
            content=specification.raw_data,
            ttl=ttl,
            is_managed=True,
        )
        try:
            response = PolyaxonClient().project.create_experiment(user,
                                                                  project_name,
                                                                  experiment)
            cache.cache(config_manager=ExperimentManager, response=response)
            Printer.print_success('Experiment `{}` was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not create experiment.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def run_group():
        click.echo('Creating an experiment group with the following definition:')
        experiments_def = specification.experiments_def
        get_group_experiments_info(**experiments_def)
        experiment_group = GroupConfig(
            name=name,
            description=description,
            tags=tags,
            content=specification.raw_data,
            is_managed=True,
        )
        try:
            response = project_client.create_experiment_group(user,
                                                              project_name,
                                                              experiment_group)
            cache.cache(config_manager=GroupManager, response=response)
            Printer.print_success('Experiment group {} was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not create experiment group.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def run_job():
        click.echo('Creating a job.')
        job = JobConfig(
            name=name,
            description=description,
            tags=tags,
            content=specification.raw_data,
            ttl=ttl,
            is_managed=True,
        )
        try:
            response = project_client.create_job(user,
                                                 project_name,
                                                 job)
            cache.cache(config_manager=JobManager, response=response)
            Printer.print_success('Job {} was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not create job.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def run_build():
        click.echo('Creating a build.')
        job = BuildJobConfig(
            name=name,
            description=description,
            tags=tags,
            content=specification.raw_data,
            ttl=ttl,
            is_managed=True,
        )
        try:
            response = project_client.create_build(user,
                                                   project_name,
                                                   job)
            cache.cache(config_manager=BuildJobManager, response=response)
            Printer.print_success('Build {} was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not create build.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    # Check if we need to upload
    if upload:
        if can_upload:
            Printer.print_error('Uploading is not supported when switching project context!')
            click.echo('Please, either omit the `-u` option or `-p` / `--project=` option.')
            sys.exit(1)
        ctx.invoke(upload_cmd, sync=False)

    logs_cmd = None
    if specification.is_experiment:
        run_experiment()
        logs_cmd = experiment_logs
    elif specification.is_group:
        run_group()
    elif specification.is_job:
        run_job()
        logs_cmd = job_logs
    elif specification.is_build:
        run_build()
        logs_cmd = build_logs

    # Check if we need to invoke logs
    if log and logs_cmd:
        ctx.obj = {'project': '{}/{}'.format(user, project_name)}
        ctx.invoke(logs_cmd)
