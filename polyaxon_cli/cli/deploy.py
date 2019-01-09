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


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True),
              help='The polyaxon deployment config file(s) to check.')
@click.option('--check', is_flag=True, default=False,
              help='Check if deployment file and other requirements are met.')
@click.option('--upgrade', is_flag=True, default=False,
              help='Upgrade a Polyaxon deployment.')
@click.option('--teardown', is_flag=True, default=False,
              help='Upgrade a Polyaxon deployment.')
@clean_outputs
def deploy(file, check, upgrade, teardown):   # pylint:disable=redefined-builtin
    """Deploy polyaxon."""
    config = read_deployment_config(file)
    manager = DeployManager(config=config, filepath=file)
    exception = None
    if check:
        manager.check()
        Printer.print_success('Polyaxon deployment file is valid.', add_sign=True)
    elif upgrade:
        try:
            manager.upgrade()
        except Exception as e:
            Printer.print_error('Polyaxon could not upgrade the deployment.', add_sign=True)
            exception = e

    elif teardown:
        try:
            if click.confirm('Would you like to execute pre-delete hooks?', default=False):
                manager.teardown(hooks=True)
            else:
                manager.teardown(hooks=False)
        except Exception as e:
            Printer.print_error('Polyaxon could not teardown the deployment.', add_sign=True)
            exception = e
    else:
        try:
            manager.install()
        except Exception as e:
            Printer.print_error('Polyaxon could not be installed.', add_sign=True)
            exception = e

    if exception:
        Printer.print_error('Error message `{}`.'.format(exception))
