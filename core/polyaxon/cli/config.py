#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

import click

from polyaxon.cli.errors import handle_cli_error
from polyaxon.managers.auth import AuthConfigManager
from polyaxon.managers.cli import CliConfigManager
from polyaxon.managers.client import ClientConfigManager
from polyaxon.managers.git import GitConfigManager
from polyaxon.managers.ignore import IgnoreConfigManager
from polyaxon.managers.project import ProjectConfigManager
from polyaxon.managers.run import RunConfigManager
from polyaxon.utils.formatting import Printer, dict_tabulate


def validate_options(ctx, param, value):
    possible_values = ["verbose", "host"]
    if value and value not in possible_values:
        raise click.BadParameter(
            "Value `{}` is not supported, must one of the value {}".format(
                value, possible_values
            )
        )
    return value


@click.group(invoke_without_command=True)
@click.option("--list", "-l", is_flag=True, help="List all global config values.")
def config(list):  # pylint:disable=redefined-builtin
    """Set and get the global configurations."""
    if list:
        _config = ClientConfigManager.get_config_or_default()
        Printer.print_header("Current config:")
        dict_tabulate(_config.to_dict())


@config.command()
@click.argument("keys", type=str, nargs=-1)
def get(keys):
    """Get the global config values by keys.

    Example:

    \b
    $ polyaxon config get host port
    """
    _config = ClientConfigManager.get_config_or_default()

    if not keys:
        return

    print_values = {}
    for key in keys:
        if hasattr(_config, key):
            print_values[key] = getattr(_config, key)
        else:
            click.echo("Key `{}` is not recognised.".format(key))

    dict_tabulate(print_values)


@config.command()
@click.option("--debug", type=bool, help="To set the verbosity of the client.")
@click.option("--host", type=str, help="To set the server endpoint.")
@click.option(
    "--no-api",
    type=str,
    help="To disable using polyaxon.com or on-prem api.",
)
@click.option(
    "--verify-ssl",
    type=bool,
    help="To set whether or not to verify the SSL certificate.",
)
@click.option(
    "--compatibility-check-interval",
    type=int,
    help="To set the compatibility check interval, to disable set this flag to -1.",
)
@click.option(
    "--disable-errors-reporting",
    type=bool,
    help="To set the disable errors reporting.",
)
def set(**kwargs):  # pylint:disable=redefined-builtin
    """Set the global config values.

    Example:

    \b
    $ polyaxon config set --host=localhost
    """
    try:
        _config = ClientConfigManager.get_config_or_default()
    except Exception as e:
        handle_cli_error(e, message="Polyaxon load configuration.")
        Printer.print_header(
            "You can reset your config by running: polyaxon config purge"
        )
        sys.exit(1)

    for key, value in kwargs.items():
        if value is not None:
            setattr(_config, key, value)

    ClientConfigManager.set_config(_config)
    Printer.print_success("Config was updated.")
    # Reset cli config
    CliConfigManager.purge()


@config.command()
@click.option(
    "--cache-only",
    is_flag=True,
    help="To purge cache only.",
)
def purge(cache_only):
    """Purge the global config values."""
    if not cache_only:
        ClientConfigManager.purge()
        CliConfigManager.purge()
        AuthConfigManager.purge()
    ProjectConfigManager.purge()
    RunConfigManager.purge()
    IgnoreConfigManager.purge()
    GitConfigManager.purge()
    Printer.print_success("Configs was removed.")
