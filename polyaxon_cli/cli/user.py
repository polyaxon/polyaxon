# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.formatting import Printer
from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError


@click.group()
@clean_outputs
def user():
    """Commands for user management."""


@user.command()
@click.argument('username', type=str)
@clean_outputs
def activate(username):
    """Activate a user.

    Example:

    \b
    ```bash
    $ polyaxon user activate david
    ```
    """
    try:
        PolyaxonClients().user.activate_user(username)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not activate user `{}`.'.format(username))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("User `{}` was activated successfully.".format(username))


@user.command()
@click.argument('username', type=str)
@clean_outputs
def delete(username):
    """Delete a user.

    Example:

    \b
    ```bash
    $ polyaxon user delete david
    ```
    """
    try:
        PolyaxonClients().user.delete_user(username)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not delete user `{}`.'.format(username))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("User `{}` was deleted successfully.".format(username))
