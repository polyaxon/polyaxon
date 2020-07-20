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

import os
import sys

import click

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.errors import handle_cli_error
from polyaxon.client import ProjectClient
from polyaxon.env_vars.getters import get_project_or_local
from polyaxon.managers.ignore import IgnoreManager
from polyaxon.managers.project import ProjectManager
from polyaxon.polyaxonfile import check_polyaxonfile
from polyaxon.utils import constants, indentation
from polyaxon.utils.formatting import Printer
from polyaxon.utils.path_utils import create_debug_file, create_init_file


def create_polyaxonfile():
    if os.path.isfile(constants.INIT_FILE_PATH):
        try:
            _ = check_polyaxonfile(constants.INIT_FILE_PATH)  # noqa
            Printer.print_success("A valid polyaxonfile.yaml was found in the project.")
        except Exception as e:
            handle_cli_error(e, message="A Polyaxonfile was found but it is not valid.")
            sys.exit(1)
    else:
        create_init_file(constants.INIT_FILE)
        # if we are here the file was not created
        if not os.path.isfile(constants.INIT_FILE_PATH):
            Printer.print_error(
                "Something went wrong, init command did not create a file.\n"
                "Possible reasons: you don't have enough rights to create the file."
            )
            sys.exit(1)

        Printer.print_success(
            "{} was created successfully.".format(constants.INIT_FILE_PATH)
        )


def create_debug_polyaxonfile():
    if os.path.isfile(constants.DEBUG_FILE_PATH):
        Printer.print_success("A polyaxonfile.debug.yaml was found in the project.")
    else:
        create_debug_file(constants.DEBUG_FILE)
        # if we are here the file was not created
        if not os.path.isfile(constants.DEBUG_FILE_PATH):
            Printer.print_error(
                "Something went wrong, init command did not create a debug file.\n"
                "Possible reasons: you don't have enough rights to create the file."
            )
            sys.exit(1)

        Printer.print_success(
            "{} was created successfully.".format(constants.DEBUG_FILE_PATH)
        )


@click.command()
@click.argument("project", type=str)
@click.option(
    "--polyaxonfile",
    is_flag=True,
    default=False,
    show_default=False,
    help="Init a polyaxon file in this project.",
)
@click.option(
    "--purge",
    is_flag=True,
    default=False,
    show_default=False,
    help="Purge previous configs before calling init.",
)
def init(project, polyaxonfile, purge):
    """Initialize a new polyaxonfile specification."""
    owner, project_name = get_project_or_local(project, is_cli=True)
    try:
        polyaxon_client = ProjectClient(owner=owner, project=project_name)
        polyaxon_client.refresh_data()
    except (ApiException, HTTPError) as e:
        Printer.print_error(
            "Make sure you have a project with this name `{}`".format(project)
        )
        handle_cli_error(
            e,
            message="You can a create new project with this command: "
            "polyaxon project create "
            "--name={} [--description=...] [--tags=...]".format(project_name),
        )
        sys.exit(1)

    if purge:
        ProjectManager.purge()
        IgnoreManager.purge()
    init_project = False
    if ProjectManager.is_initialized():
        local_project = ProjectManager.get_config()
        click.echo(
            "Warning! This project is already initialized with the following project:"
        )
        with indentation.indent(4):
            indentation.puts("User: {}".format(local_project.user))
            indentation.puts("Project: {}".format(local_project.name))
        if click.confirm(
            "Would you like to override this current config?", default=False
        ):
            init_project = True
    else:
        init_project = True

    if init_project:
        ProjectManager.purge(visibility=ProjectManager.VISIBILITY_LOCAL)
        config = polyaxon_client.client.sanitize_for_serialization(
            polyaxon_client.project_data
        )
        ProjectManager.set_config(
            config, init=True, visibility=ProjectManager.VISIBILITY_LOCAL
        )
        Printer.print_success("Project was initialized")
    else:
        Printer.print_header("Project config was not changed.")

    init_ignore = False
    if IgnoreManager.is_initialized():
        click.echo("Warning! Found a .polyaxonignore file.")
        if click.confirm("Would you like to override it?", default=False):
            init_ignore = True
    else:
        init_ignore = True

    if init_ignore:
        IgnoreManager.init_config()
        Printer.print_success("New .polyaxonignore file was created.")
    else:
        Printer.print_header(".polyaxonignore file was not changed.")

    if polyaxonfile:
        create_polyaxonfile()
        create_debug_polyaxonfile()
