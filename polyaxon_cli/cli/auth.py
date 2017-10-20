# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import webbrowser

from polyaxon_schemas.access_token import AccessTokenConfig
from polyaxon_schemas.polyaxonfile.logger import logger

from polyaxon_cli.client.auth import AuthClient
from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.managers.config import GlobalConfigManager


@click.command()
@click.option('--token', is_flag=True, default=False, help='Just enter token')
def login(token):
    """Log into Polyaxon via Auth0."""
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
    user = AuthClient().get_user(access_code)
    access_token = AccessTokenConfig(username=user.username, token=access_code)
    AuthConfigManager.set_config(access_token)
    logger.info("Login Successful")


@click.command()
def logout():
    """Logout of Polyaxon."""
    AuthConfigManager.purge()
    logger.info("You are logged out")
