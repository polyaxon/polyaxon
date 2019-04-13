# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys

import click

from hestia.list_utils import to_list
from polyaxon_deploy import reader

from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.deploy import DeployManager
from polyaxon_cli.utils.formatting import Printer


def read_deployment_config(filepaths):
    if not filepaths:
        return None

    filepaths = to_list(filepaths)
    for filepath in filepaths:
        if not os.path.isfile(filepath):
            Printer.print_error("`{}` must be a valid file".format(filepath))
            sys.exit(1)
    try:
        deployment_config = reader.read(filepaths)
    except Exception as e:
        Printer.print_error("Polyaxon deployment file is not valid ")
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    return deployment_config


@click.group()
@clean_outputs
def admin():
    """Commands for admin management."""


@admin.command()
@click.option('--file', '-f', type=click.Path(exists=True),
              help='The polyaxon deployment config file(s) to check.')
@click.option('--manager_path', type=click.Path(exists=True),
              help='The path of the deployment manager, e.g. local chart.')
@click.option('--check', is_flag=True, default=False,
              help='Check if deployment file and other requirements are met.')
@click.option('--dry_run', is_flag=True, default=False,
              help='Dry run the configuration and generate a debuggable output.')
@clean_outputs
def deploy(file, manager_path, check, dry_run):  # pylint:disable=redefined-builtin
    """Deploy polyaxon."""
    config = read_deployment_config(file)
    manager = DeployManager(config=config,
                            filepath=file,
                            manager_path=manager_path,
                            dry_run=dry_run)
    exception = None
    if check:
        manager.check()
        Printer.print_success('Polyaxon deployment file is valid.')
    else:
        try:
            manager.install()
        except Exception as e:
            Printer.print_error('Polyaxon could not be installed.')
            exception = e

    if exception:
        Printer.print_error('Error message `{}`.'.format(exception))


@admin.command()
@click.option('--file', '-f', type=click.Path(exists=True),
              help='The polyaxon deployment config file(s) to check.')
@click.option('--manager_path', type=click.Path(exists=True),
              help='The path of the deployment manager, e.g. local chart.')
@click.option('--check', is_flag=True, default=False,
              help='Check if deployment file and other requirements are met.')
@click.option('--dry_run', is_flag=True, default=False,
              help='Dry run the configuration and generate a debuggable output.')
@clean_outputs
def upgrade(file, manager_path, check, dry_run):  # pylint:disable=redefined-builtin
    """Upgrade a Polyaxon deployment."""
    config = read_deployment_config(file)
    manager = DeployManager(config=config,
                            filepath=file,
                            manager_path=manager_path,
                            dry_run=dry_run)
    exception = None
    if check:
        manager.check()
        Printer.print_success('Polyaxon deployment file is valid.')
    else:
        try:
            manager.upgrade()
        except Exception as e:
            Printer.print_error('Polyaxon could not upgrade the deployment.')
            exception = e

    if exception:
        Printer.print_error('Error message `{}`.'.format(exception))


@admin.command()
@click.option('--file', '-f', type=click.Path(exists=True),
              help='The polyaxon deployment config file(s) to check.')
@clean_outputs
def teardown(file):  # pylint:disable=redefined-builtin
    """Teardown a polyaxon deployment given a config file."""
    config = read_deployment_config(file)
    manager = DeployManager(config=config, filepath=file)
    exception = None
    try:
        if click.confirm('Would you like to execute pre-delete hooks?', default=True):
            manager.teardown(hooks=True)
        else:
            manager.teardown(hooks=False)
    except Exception as e:
        Printer.print_error('Polyaxon could not teardown the deployment.')
        exception = e

    if exception:
        Printer.print_error('Error message `{}`.'.format(exception))
