# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.cli import CliConfigManager
from polyaxon_cli.managers.config import GlobalConfigManager
from polyaxon_cli.utils.formatting import Printer, dict_tabulate


def validate_options(ctx, param, value):
    possible_values = ['verbose', 'host']
    if value and value not in possible_values:
        raise click.BadParameter(
            "Value `{}` is not supported, must one of the value {}".format(value, possible_values))
    return value


@click.group(invoke_without_command=True)
@click.option('--list', '-l', is_flag=True, help='List all global config values.')
@clean_outputs
def config(list):  # pylint:disable=redefined-builtin
    """Set and get the global configurations."""
    if list:
        _config = GlobalConfigManager.get_config()
        Printer.print_header('Current config:')
        dict_tabulate(_config.to_dict())


@config.command()
@click.argument('keys', type=str, nargs=-1)
@clean_outputs
def get(keys):
    """Get the global config values by keys.

    Example:

    \b
    ```bash
    $ polyaxon config get host http_port
    ```
    """
    _config = GlobalConfigManager.get_config_or_default()

    if not keys:
        return

    print_values = {}
    for key in keys:
        if hasattr(_config, key):
            print_values[key] = getattr(_config, key)
        else:
            click.echo('Key `{}` is not recognised.'.format(key))

    dict_tabulate(print_values, )


@config.command()
@click.option('--verbose', type=bool, help='To set the verbosity of the client.')
@click.option('--host', type=str, help='To set the server endpoint.')
@click.option('--http_port', type=int, help='To set the http port.')
@click.option('--ws_port', type=int, help='To set the stream port.')
@click.option('--use_https', type=bool, help='To set the https.')
@clean_outputs
def set(verbose, host, http_port, ws_port, use_https):  # pylint:disable=redefined-builtin
    """Set the global config values.

    Example:

    \b
    ```bash
    $ polyaxon config set --hots=localhost http_port=80
    ```
    """
    _config = GlobalConfigManager.get_config_or_default()

    if verbose is not None:
        _config.verbose = verbose

    if host is not None:
        _config.host = host

    if http_port is not None:
        _config.http_port = http_port

    if ws_port is not None:
        _config.ws_port = ws_port

    if use_https is not None:
        _config.use_https = use_https

    GlobalConfigManager.set_config(_config)
    Printer.print_success('Config was update.')
    # Reset cli config
    CliConfigManager.purge()
