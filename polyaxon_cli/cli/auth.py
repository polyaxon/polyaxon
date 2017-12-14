# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

import sys

from polyaxon_client.exceptions import PolyaxonShouldExitError
from polyaxon_schemas.authentication import AccessTokenConfig, CredentialsConfig

from polyaxon_cli.logger import logger
from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer


@click.command()
@click.option('--token', '-t', help='Polyaxon token')
@click.option('--username', '-u', help='Polyaxon username')
@click.option('--password', '-p', help='Polyaxon password')
def login(token, username, password):
    """Log into Polyaxon."""
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
        except PolyaxonShouldExitError as e:
            logger.exception(e)
            sys.exit(0)

        if not access_code:
            Printer.print_error("Failed to login")
            return
    else:
        if not token:
            cli_info_url = "{}/users/token".format(auth_client.http_host)
            click.confirm('Authentication token page will now open in your browser. Continue?',
                          abort=True, default=True)

            click.launch(cli_info_url)
        logger.info("Please copy and paste the authentication token.")
        access_code = click.prompt('This is an invisible field. Paste token and press ENTER',
                                   type=str, hide_input=True)

        if not access_code:
            logger.info("Empty token received. "
                        "Make sure your shell is handling the token appropriately.")
            logger.info("See docs for help: http://docs.polyaxon.com/faqs/authentication/")
            return

        access_code = access_code.strip(" ")

    user = PolyaxonClients().auth.get_user(token=access_code)
    access_token = AccessTokenConfig(username=user.username, token=access_code)
    try:
        AuthConfigManager.set_config(access_token)
    except PolyaxonShouldExitError as e:
        logger.exception(e)
        sys.exit(0)

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
    click.echo("Username: {username}, Email: {email}".format(**user.to_dict()))
