# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.utils.formatting import Printer
from polyaxon_client.exceptions import PolyaxonClientException


@click.group()
@clean_outputs
def superuser():
    """Commands for superuser role management."""


@superuser.command()
@click.argument('username', type=str)
@clean_outputs
def grant(username):
    """Grant superuser role to a user.

    Example:

    \b
    ```bash
    $ polyaxon superuser grant david
    ```
    """
    try:
        PolyaxonClient().user.grant_superuser(username)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not grant superuser role to user `{}`.'.format(username))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success(
        "Superuser role was granted successfully to user `{}`.".format(username))


@superuser.command()
@click.argument('username', type=str)
@clean_outputs
def revoke(username):
    """Revoke superuser role to a user.

    Example:

    \b
    ```bash
    $ polyaxon superuser revoke david
    ```
    """
    try:
        PolyaxonClient().user.revoke_superuser(username)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not revoke superuser role from user `{}`.'.format(username))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success(
        "Superuser role was revoked successfully from user `{}`.".format(username))
