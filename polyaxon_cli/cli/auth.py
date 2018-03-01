# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

import sys

from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError

from polyaxon_schemas.authentication import AccessTokenConfig, CredentialsConfig

from polyaxon_cli.logger import logger
from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer


@click.command()
@click.option('--token', '-t', help='Polyaxon token.')
@click.option('--username', '-u', help='Polyaxon username.')
@click.option('--password', '-p', help='Polyaxon password.')
def login(token, username, password):
    """Login to Polyaxon."""
    auth_client = PolyaxonClients().auth
    if username:
        # Use username / password login
        if not password:
            password = click.prompt('Please enter your password', type=str, hide_input=True)
            password = password.strip()
            if not password:
                logger.info('You entered an empty string. '
                            'Please make sure you enter your password correctly.')
                sys.exit(1)

        credentials = CredentialsConfig(username=username, password=password)
        try:
            access_code = auth_client.login(credentials=credentials)
        except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
            Printer.print_error('Could not login.')
            Printer.print_error(e)
            sys.exit(1)

        if not access_code:
            Printer.print_error("Failed to login")
            return
    else:
        if not token:
            token_url = "{}/app/auth/login?next=/app/token".format(auth_client.http_host)
            click.confirm('Authentication token page will now open in your browser. Continue?',
                          abort=True, default=True)

            click.launch(token_url)
            logger.info("Please copy and paste the authentication token.")
            token = click.prompt('This is an invisible field. Paste token and press ENTER',
                                 type=str, hide_input=True)

        if not token:
            logger.info("Empty token received. "
                        "Make sure your shell is handling the token appropriately.")
            logger.info("See docs for help: http://docs.polyaxon.com/polyaxon_cli/commands/auth")
            return

        access_code = token.strip(" ")

    try:
        AuthConfigManager.purge()
        user = PolyaxonClients().auth.get_user(token=access_code)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not load user info.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
    access_token = AccessTokenConfig(username=user.username, token=access_code)
    AuthConfigManager.set_config(access_token)

    Printer.print_success("Login Successful")


@click.command()
def logout():
    """Logout of Polyaxon."""
    AuthConfigManager.purge()
    Printer.print_success("You are logged out")


@click.command()
def whoami():
    """Show current logged Polyaxon user."""
    user = PolyaxonClients().auth.get_user()
    click.echo("\nUsername: {username}, Email: {email}\n".format(**user.to_dict()))
