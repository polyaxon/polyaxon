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
import polyaxon_sdk

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import settings
from polyaxon.cli.dashboard import get_dashboard_url
from polyaxon.cli.errors import handle_cli_error, handle_command_not_in_ce
from polyaxon.cli.session import session_expired, set_versions_config
from polyaxon.client import PolyaxonClient
from polyaxon.logger import clean_outputs, logger
from polyaxon.managers.auth import AuthConfigManager
from polyaxon.managers.cli import CliConfigManager
from polyaxon.managers.user import UserConfigManager
from polyaxon.schemas.api.authentication import AccessTokenConfig, V1Credentials
from polyaxon.utils.formatting import Printer, dict_tabulate, dict_to_tabulate


@click.command()
@click.option("--token", "-t", help="Polyaxon token.")
@click.option("--username", "-u", help="Polyaxon username or email.")
@click.option("--password", "-p", help="Polyaxon password.")
@clean_outputs
def login(token, username, password):
    """Login to Polyaxon Cloud or Polyaxon EE."""
    if not settings.CLI_CONFIG or settings.CLI_CONFIG.is_ce:
        handle_command_not_in_ce()

    polyaxon_client = PolyaxonClient()
    if username and not token:
        # Use user or email / password login
        if not password:
            password = click.prompt(
                "Please enter your password", type=str, hide_input=True
            )
            password = password.strip()
            if not password:
                logger.info(
                    "You entered an empty string. "
                    "Please make sure you enter your password correctly."
                )
                sys.exit(1)

        try:
            body = V1Credentials(username=username, password=password)
            access_auth = polyaxon_client.auth_v1.login(body=body)
        except (ApiException, HTTPError) as e:
            AuthConfigManager.purge()
            UserConfigManager.purge()
            CliConfigManager.purge()
            handle_cli_error(e, message="Could not login.")
            sys.exit(1)

        if not access_auth.token:
            Printer.print_error("Failed to login")
            return
    else:
        if not token:
            token_url = get_dashboard_url(subpath="profile/token")
            click.confirm(
                "Authentication token page will now open in your browser. Continue?",
                abort=True,
                default=True,
            )

            click.launch(token_url)
            logger.info("Please copy and paste the authentication token.")
            token = click.prompt(
                "This is an invisible field. Paste token and press ENTER",
                type=str,
                hide_input=True,
            )

        if not token:
            logger.info(
                "Empty token received. "
                "Make sure your shell is handling the token appropriately."
            )
            logger.info(
                "See docs for help: http://polyaxon.com/docs/polyaxon_cli/commands/auth"
            )
            return

        access_auth = polyaxon_sdk.models.V1Auth(token=token.strip(" "))

    # Set user
    try:
        AuthConfigManager.purge()
        UserConfigManager.purge()
        polyaxon_client = PolyaxonClient(token=access_auth.token)
        user = polyaxon_client.users_v1.get_user()
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not load user info.")
        sys.exit(1)
    access_token = AccessTokenConfig(username=user.username, token=access_auth.token)
    AuthConfigManager.set_config(access_token)
    UserConfigManager.set_config(user)
    polyaxon_client.config.token = access_auth.token
    Printer.print_success("Login successful")

    set_versions_config(polyaxon_client=polyaxon_client, set_handler=True)


@click.command()
@clean_outputs
def logout():
    """Logout from Polyaxon Cloud or Polyaxon EE."""
    AuthConfigManager.purge()
    UserConfigManager.purge()
    CliConfigManager.purge()
    Printer.print_success("You are logged out")


@click.command()
@clean_outputs
def whoami():
    """Show current logged Polyaxon Cloud or Polyaxon EE user."""
    if not settings.CLI_CONFIG or settings.CLI_CONFIG.is_ce:
        handle_command_not_in_ce()

    try:
        polyaxon_client = PolyaxonClient()
        user = polyaxon_client.users_v1.get_user()
    except ApiException as e:
        if e.status == 403:
            session_expired()
        handle_cli_error(e, message="Could not get the user info.", sys_exit=True)
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not load user info.", sys_exit=True)

    response = dict_to_tabulate(user.to_dict(), exclude_attrs=["role", "theme"])
    Printer.print_header("User info:")
    dict_tabulate(response)
