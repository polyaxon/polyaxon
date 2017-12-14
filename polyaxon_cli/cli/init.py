# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

import os

from polyaxon_client.exceptions import PolyaxonHTTPError
from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile

from polyaxon_cli.cli.project import get_project_or_local
from polyaxon_cli.managers.ignore import IgnoreManager
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils import constants
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.files import create_init_file
from polyaxon_cli.utils.formatting import Printer


@click.command()
@click.argument('project', type=str)
@click.option('--model', is_flag=True, default=False,
              help='Init a polyaxon file with `model` step template.')
@click.option('--run', is_flag=True, default=False,
              help='Init a polyaxon file with `exec` step template.')
def init(project, model, run):
    """Init a new polyaxonfile specification."""
    user, project_name = get_project_or_local(project)
    try:
        project_config = PolyaxonClients().project.get_project(user, project_name)
    except PolyaxonHTTPError:
        Printer.print_error('Make sure you have a project with this name `{}`'.format(project))
        Printer.print_error('You can a new project with this command: '
                            'polyaxon project create --name={} --description=...'.format(project))
        sys.exit(1)

    if not any([model, run]) and not all([model, run]):
        Printer.print_error("You must specify which an init option, "
                            "possible values: `--model` or `--run`.")
        sys.exit(1)

    result = False
    if model:
        result = create_init_file(constants.INIT_FILE_MODEL, project)

    elif run:
        result = create_init_file(constants.INIT_FILE_RUN, project)

    if result:
        ProjectManager.set_config(project_config, init=True)
        IgnoreManager.init_config()
        Printer.print_success(
            "Polyaxonfile was created successfully `{}`".format(constants.INIT_FILE))
        sys.exit(1)

    # if we are here the file was not created
    if not os.path.isfile(constants.INIT_FILE):
        Printer.print_error(
            "Something went wrong, init command did not create a file.\n"
            "Possible reasons: you don't have the write to create the file.")
        sys.exit(1)

    # file was already there, let's check if the project passed correspond to this file
    spec = PolyaxonFile.read(constants.INIT_FILE)
    print(spec.project.name)
    if project_config.api_url != spec.project.name:
        Printer.print_error(
            "Something went wrong, init command did not create a file.\n"
            "Anothor file already exist with different "
            "project name `{}`.".format(spec.project.name))
        sys.exit(1)

    # At this point we check if we need to re init configurations
    ProjectManager.set_config(project_config, init=True)
    IgnoreManager.init_config()
    Printer.print_success(
        "Polyaxonfile was created successfully `{}`".format(constants.INIT_FILE))
