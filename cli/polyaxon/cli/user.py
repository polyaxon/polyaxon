#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon.cli.errors import handle_cli_error
from polyaxon.client import PolyaxonClient
from polyaxon.exceptions import (
    PolyaxonClientException,
    PolyaxonHTTPError,
    PolyaxonShouldExitError,
)
from polyaxon.logger import clean_outputs
from polyaxon.utils.formatting import Printer


@click.group()
@clean_outputs
def user():
    """Commands for user management."""


@user.command()
@click.argument("username", type=str)
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
        PolyaxonClient().user.activate_user(username)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        handle_cli_error(e, message="Could not activate user `{}`.".format(username))
        sys.exit(1)

    Printer.print_success("User `{}` was activated successfully.".format(username))


@user.command()
@click.argument("username", type=str)
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
        PolyaxonClient().user.delete_user(username)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        handle_cli_error(e, message="Could not delete user `{}`.".format(username))
        sys.exit(1)

    Printer.print_success("User `{}` was deleted successfully.".format(username))
