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
from polyaxon.cli.options import OPTIONS_PROJECT
from polyaxon.client import ProjectClient
from polyaxon.env_vars.getters import get_project_or_local
from polyaxon.managers.git import GitConfigManager
from polyaxon.managers.ignore import IgnoreConfigManager
from polyaxon.managers.project import ProjectConfigManager
from polyaxon.polyaxonfile import check_polyaxonfile
from polyaxon.schemas.types import V1GitType
from polyaxon.utils import constants, indentation
from polyaxon.utils.formatting import Printer
from polyaxon.utils.path_utils import create_init_file


def create_polyaxonfile():
    if os.path.isfile(constants.INIT_FILE_PATH):
        try:
            _ = check_polyaxonfile(constants.INIT_FILE_PATH)  # noqa
            Printer.print_success(
                "A valid polyaxonfile.yaml was found in this project."
            )
        except Exception as e:
            handle_cli_error(e, message="A Polyaxonfile was found but it is not valid.")
            sys.exit(1)
    else:
        create_init_file()
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


@click.command()
@click.option(
    *OPTIONS_PROJECT["args"],
    type=str,
    help="To enable local cache in this folder, "
    "the project name to initialize, e.g. 'mnist' or 'adam/mnist'."
)
@click.option(
    "--git-connection",
    type=str,
    help="Optional git connection to use for the interactive mode and to "
    "automatically injecting code references in your operation manifests.",
)
@click.option(
    "--git-url",
    type=str,
    help="Optional git url to use for the interactive mode and for "
    "automatically injecting code references in your operation manifests. "
    "If no git-connection is passed, this url must point to a public repo,"
    "If a connection is passed and if it has a git url reference in the schema "
    "it will be patched with this url.",
)
@click.option(
    "--polyaxonfile",
    is_flag=True,
    default=False,
    show_default=False,
    help="Init a polyaxon file in this project.",
)
@click.option(
    "--polyaxonignore",
    is_flag=True,
    default=False,
    show_default=False,
    help="Init a polyaxonignore file in this project.",
)
def init(project, git_connection, git_url, polyaxonfile, polyaxonignore):
    """Initialize a new local project and cache directory.

    Note: We recommend that you add the local cache `.polyaxon`
    to your `.gitignore` and `.dockerignore` files.
    """
    if not any([project, git_connection, git_url, polyaxonfile, polyaxonignore]):
        Printer.print_warning(
            "`polyaxon init` did not receive any valid option.",
            command_help="polyaxon init",
        )
    if project:
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
        init_project = False
        if ProjectConfigManager.is_initialized():
            local_project = ProjectConfigManager.get_config()
            click.echo(
                "Warning! This project is already initialized with the following project:"
            )
            with indentation.indent(4):
                indentation.puts("Owner: {}".format(local_project.owner))
                indentation.puts("Project: {}".format(local_project.name))
            if click.confirm(
                "Would you like to override this current config?", default=False
            ):
                init_project = True
        else:
            init_project = True

        if init_project:
            ProjectConfigManager.purge(visibility=ProjectConfigManager.VISIBILITY_LOCAL)
            config = polyaxon_client.client.sanitize_for_serialization(
                polyaxon_client.project_data
            )
            ProjectConfigManager.set_config(
                config, init=True, visibility=ProjectConfigManager.VISIBILITY_LOCAL
            )
            Printer.print_success("Project was initialized")
        else:
            Printer.print_header("Project config was not changed.")

    if git_connection or git_url:
        init_git = False
        if GitConfigManager.is_initialized():
            click.echo(
                "Warning! A {} file was found.".format(
                    GitConfigManager.CONFIG_FILE_NAME
                )
            )
            if click.confirm("Would you like to override it?", default=False):
                init_git = True
        else:
            init_git = True

        if init_git:
            GitConfigManager.purge(visibility=GitConfigManager.VISIBILITY_LOCAL)
            config = GitConfigManager.CONFIG(
                connection=git_connection,
                git=V1GitType(url=git_url) if git_url else None,
            )
            GitConfigManager.set_config(config=config, init=True)
            Printer.print_success(
                "New {} file was created.".format(GitConfigManager.CONFIG_FILE_NAME)
            )
        else:
            Printer.print_header(
                "{} file was not changed.".format(GitConfigManager.CONFIG_FILE_NAME)
            )

    if polyaxonfile:
        create_polyaxonfile()

    if polyaxonignore:
        init_ignore = False
        if IgnoreConfigManager.is_initialized():
            click.echo(
                "Warning! A {} file was found.".format(
                    IgnoreConfigManager.CONFIG_FILE_NAME
                )
            )
            if click.confirm("Would you like to override it?", default=False):
                init_ignore = True
        else:
            init_ignore = True

        if init_ignore:
            IgnoreConfigManager.init_config()
            Printer.print_success(
                "New {} file was created.".format(IgnoreConfigManager.CONFIG_FILE_NAME)
            )
        else:
            Printer.print_header(
                "{} file was not changed.".format(IgnoreConfigManager.CONFIG_FILE_NAME)
            )
