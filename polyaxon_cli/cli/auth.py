# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import webbrowser

import sys

from polyaxon_client.auth import AuthClient
from polyaxon_schemas.authentication import AccessTokenConfig, CredentialsConfig
from polyaxon_schemas.polyaxonfile.logger import logger

from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.managers.config import GlobalConfigManager
from polyaxon_cli.utils.clients import PolyaxonClients


@click.command()
@click.option('--token', '-t', help='Polyaxon token')
@click.option('--username', '-u', help='Polyaxon username')
@click.option('--password', '-p', help='Polyaxon password')
def login(token, username, password):
    """Log into Polyaxon."""
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
        access_code = PolyaxonClients().auth.login(credentials=credentials)
        if not access_code:
            logger.info("Failed to login")
            return

    if not token:
        cli_info_url = "{}/users/token".format(GlobalConfigManager.get_value('host'))
        click.confirm('Authentication token page will now open in your browser. Continue?',
                      abort=True, default=True)

        webbrowser.open(cli_info_url)

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
    AuthConfigManager.set_config(access_token)
    logger.info("Login Successful")


@click.command()
def logout():
    """Logout of Polyaxon."""
    AuthConfigManager.purge()
    logger.info("You are logged out")
