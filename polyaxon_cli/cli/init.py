# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys

import click

from marshmallow import ValidationError

from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.ignore import IgnoreManager
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils import constants
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.files import create_init_file
from polyaxon_cli.utils.formatting import Printer
from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile


@click.command()
@click.argument('project', type=str)
@click.option('--run', is_flag=True, default=True, show_default=True,
              help='Init a polyaxon file with `exec` step template.')
@click.option('--model', is_flag=True, default=False, show_default=True,
              help='Init a polyaxon file with `model` step template.')
@clean_outputs
def init(project, run, model):
    """Initialize a new polyaxonfile specification."""
    user, project_name = get_project_or_local(project)
    try:
        project_config = PolyaxonClients().project.get_project(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Make sure you have a project with this name `{}`'.format(project))
        Printer.print_error(
            'You can a create new project with this command: '
            'polyaxon project create '
            '--name={} [--description=...] [--tags=...]'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if not any([model, run]) and not all([model, run]):
        Printer.print_error("You must specify which init option, "
                            "possible values: `--model` or `--run`.")
        sys.exit(1)

    result = False
    if model:
        result = create_init_file(constants.INIT_FILE_MODEL)

    elif run:
        result = create_init_file(constants.INIT_FILE_RUN)

    if result:
        ProjectManager.purge()
        ProjectManager.set_config(project_config, init=True)
        IgnoreManager.init_config()
        Printer.print_success(
            "Project `{}` was initialized and Polyaxonfile was created successfully `{}`".format(
                project, constants.INIT_FILE))
        sys.exit(1)

    # if we are here the file was not created
    if not os.path.isfile(constants.INIT_FILE):
        Printer.print_error(
            "Something went wrong, init command did not create a file.\n"
            "Possible reasons: you don't have the write to create the file.")
        sys.exit(1)

    # file was already there, let's check if the project passed correspond to this file
    try:
        PolyaxonFile(constants.INIT_FILE).specification
    except (PolyaxonfileError, ValidationError) as e:
        Printer.print_error(
            "Something went wrong, init command did not create a file.\n"
            "Another file already exist with.")
        Printer.print_error('Error message: `{}`.'.format(e))
        sys.exit(1)

    # At this point we check if we need to re init configurations
    ProjectManager.purge()
    ProjectManager.set_config(project_config, init=True)
    IgnoreManager.init_config()
    Printer.print_success(
        "Project `{}` was initialized and Polyaxonfile was created successfully `{}`".format(
            project, constants.INIT_FILE))
