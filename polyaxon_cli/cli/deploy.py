# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

import click
import rhea

from hestia.list_utils import to_list

from polyaxon_cli.exceptions import PolyaxonConfigurationError, PolyaxonDeploymentConfigError
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.deploy import DeployManager
from polyaxon_cli.schemas.deployment_configuration import DeploymentConfig


def read_deployment_config(filepaths):
    filepaths = to_list(filepaths)
    for filepath in filepaths:
        if not os.path.isfile(filepath):
            raise PolyaxonDeploymentConfigError("`{}` must be a valid file".format(filepath))
    if not filepaths:
        return None

    data = rhea.read(filepaths)
    try:
        deployment_config = DeploymentConfig.from_dict(data)
    except PolyaxonConfigurationError as e:
        raise PolyaxonDeploymentConfigError(e)

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
    if check:
        manager.check()
    elif upgrade:
        manager.upgrade()
    elif teardown:
        if click.confirm('Would you like to execute pre-delete hooks?', default=False):
            manager.teardown(hooks=True)
        else:
            manager.teardown(hooks=False)
    else:
        manager.install()
