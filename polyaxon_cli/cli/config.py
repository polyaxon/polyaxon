# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_cli.managers.config import GlobalConfigManager


def validate_options(ctx, param, value):
    possible_values = ['verbose', 'host', 'working_directory']
    if value and value not in possible_values:
        raise click.BadParameter(
            "Value `{}` is not supported, must one of the value {}".format(value, possible_values))
    return value


@click.group(invoke_without_command=True)
@click.option('--list', '-l', is_flag=True, help='List global config values')
@click.option('--get', callback=validate_options, help='Get global config value')
def config(list, get):
    """Command for setting and getting global configurations."""
    if list:
        config = GlobalConfigManager.get_config()
        click.echo(config.to_dict())

    if get:
        v = GlobalConfigManager.get_value(get)
        click.echo(v)


@config.command()
@click.option('--verbose', type=bool, help='The verbosity of the client')
@click.option('--host', type=str, help='The server endpoint')
@click.option('--working_directory', type=click.Path(exists=True), help='The working directory')
def set(verbose, host, working_directory):
    """

    :param verbose:
    :param host:
    :param working_directory:
    :return:
    """
    config = GlobalConfigManager.get_config() or GlobalConfigManager.CONFIG()
    if verbose is not None:
        config.verbose = verbose

    if host is not None:
        config.host = host

    if working_directory is not None:
        config.working_directory = working_directory

    GlobalConfigManager.set_config(config)
