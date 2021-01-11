#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
from polyaxon.logger import clean_outputs
from polyaxon.managers.auth import AuthConfigManager
from polyaxon.managers.cli import CliConfigManager
from polyaxon.managers.client import ClientConfigManager
from polyaxon.managers.project import ProjectConfigManager
from polyaxon.managers.run import RunConfigManager
from polyaxon.managers.user import UserConfigManager
from polyaxon.utils.formatting import Printer, dict_tabulate, dict_to_tabulate


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
@click.option(
    "--list",
    "-l",
    "_list",
    is_flag=True,
    help="Deprecated, please use `polyaxon config show`.",
)
@clean_outputs
def config(_list):  # pylint:disable=redefined-builtin
    """Set and get the global configurations."""
    if _list:
        Printer.print_warning(
            "`polyaxon config -l` is deprecated, please use `polyaxon config show`!"
        )


@config.command()
@clean_outputs
def show():
    """Show the current cli, client, and user configs."""
    _config = ClientConfigManager.get_config_or_default()
    Printer.print_header("Client config:")
    dict_tabulate(_config.to_dict())
    _config = CliConfigManager.get_config_or_default()
    if _config:
        Printer.print_header("CLI config:")
        if _config.current_version:
            click.echo("Version {}".format(_config.current_version))
        else:
            Printer.print_warning("This cli is not configured.")
        if _config.installation:
            config_installation = dict_to_tabulate(
                _config.installation,
                humanize_values=True,
                exclude_attrs=["hmac", "auth", "host"],
            )
            dict_tabulate(config_installation)
        else:
            Printer.print_warning("This cli is not connected to a Polyaxon Host.")
    _config = UserConfigManager.get_config_or_default()
    if _config:
        Printer.print_header("User config:")
        config_user = dict_to_tabulate(
            _config.to_dict(),
            humanize_values=True,
            exclude_attrs=["theme"],
        )
        dict_tabulate(config_user)


@config.command()
@click.argument("keys", type=str, nargs=-1)
@clean_outputs
def get(keys):
    """Get the specific keys from the global configuration.

    Example:

    \b
    $ polyaxon config get host verify-ssl
    """
    _config = ClientConfigManager.get_config_or_default()

    if not keys:
        return

    print_values = {}
    for key in keys:
        key = key.replace("-", "_")
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
    "--disable-errors-reporting",
    type=bool,
    help="To set the disable errors reporting.",
)
@clean_outputs
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

    should_purge = False
    for key, value in kwargs.items():
        if key == "host":
            should_purge = True
        if value is not None:
            setattr(_config, key, value)

    ClientConfigManager.set_config(_config)
    Printer.print_success("Config was updated.")
    # Reset cli config
    CliConfigManager.purge()
    if should_purge:
        AuthConfigManager.purge()
        UserConfigManager.purge()


@config.command()
@click.option(
    "--cache-only",
    is_flag=True,
    help="To purge the cache only.",
)
@clean_outputs
def purge(cache_only):
    """Purge the global config values."""
    if not cache_only:
        ClientConfigManager.purge()
        CliConfigManager.purge()
        AuthConfigManager.purge()
        UserConfigManager.purge()
    ProjectConfigManager.purge()
    RunConfigManager.purge()
    Printer.print_success("Configs was removed.")
