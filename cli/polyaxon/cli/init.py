# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys

import click

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon.cli.getters.project import get_project_or_local
from polyaxon.client import PolyaxonClient
from polyaxon.logger import clean_outputs
from polyaxon.managers.ignore import IgnoreManager
from polyaxon.managers.project import ProjectManager
from polyaxon.schemas.polyaxonfile import PolyaxonFile
from polyaxon.utils import constants, indentation
from polyaxon.utils.files import create_init_file
from polyaxon.utils.formatting import Printer


def create_polyaxonfile():
    if os.path.isfile(constants.INIT_FILE):
        try:
            _ = PolyaxonFile(constants.INIT_FILE).specification  # noqa
            Printer.print_success("A valid polyaxonfile.yaml was found in the project.")
        except Exception as e:
            Printer.print_error("A Polyaxonfile was found but it is not valid.")
            Printer.print_error("Error message `{}`.".format(e))
            sys.exit(1)
    else:
        create_init_file(constants.INIT_FILE_RUN)
        # if we are here the file was not created
        if not os.path.isfile(constants.INIT_FILE):
            Printer.print_error(
                "Something went wrong, init command did not create a file.\n"
                "Possible reasons: you don't have enough rights to create the file."
            )
            sys.exit(1)

        Printer.print_success(
            "{} was created successfully.".format(constants.INIT_FILE)
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
@clean_outputs
def init(project, polyaxonfile, purge):
    """Initialize a new polyaxonfile specification."""
    owner, project_name = get_project_or_local(project)
    try:
        polyaxon_client = PolyaxonClient()
        project_config = polyaxon_client.projects_v1.get_project(owner, project_name)
    except (ApiException, HTTPError) as e:
        Printer.print_error(
            "Make sure you have a project with this name `{}`".format(project)
        )
        Printer.print_error(
            "You can a create new project with this command: "
            "polyaxon project create "
            "--name={} [--description=...] [--tags=...]".format(project_name)
        )
        Printer.print_error("Error message `{}`.".format(e))
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
        ProjectManager.purge()
        config = polyaxon_client.api_client.sanitize_for_serialization(project_config)
        ProjectManager.set_config(config, init=True)
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
