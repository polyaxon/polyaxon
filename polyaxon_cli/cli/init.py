# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys

import click

from polyaxon_cli.cli.getters.project import get_project_or_local
from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import (
    PolyaxonClientException,
    PolyaxonHTTPError,
    PolyaxonShouldExitError
)
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.ignore import IgnoreManager
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.schemas import PolyaxonFile
from polyaxon_cli.utils import constants, indentation
from polyaxon_cli.utils.files import create_init_file
from polyaxon_cli.utils.formatting import Printer


def create_polyaxonfile():
    if os.path.isfile(constants.INIT_FILE):
        try:
            _ = PolyaxonFile(constants.INIT_FILE).specification  # noqa
            Printer.print_success("A valid polyaxonfile.yaml was found in the project.")
        except Exception as e:
            Printer.print_error("A Polyaxonfile was found but it is not valid.")
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    else:
        create_init_file(constants.INIT_FILE_RUN)
        # if we are here the file was not created
        if not os.path.isfile(constants.INIT_FILE):
            Printer.print_error(
                "Something went wrong, init command did not create a file.\n"
                "Possible reasons: you don't have enough rights to create the file.")
            sys.exit(1)

        Printer.print_success("{} was created successfully.".format(constants.INIT_FILE))


@click.command()
@click.argument('project', type=str)
@click.option('--polyaxonfile', is_flag=True, default=False, show_default=False,
              help='Init a polyaxon file in this project.')
@clean_outputs
def init(project, polyaxonfile):
    """Initialize a new polyaxonfile specification."""
    user, project_name = get_project_or_local(project)
    try:
        project_config = PolyaxonClient().project.get_project(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Make sure you have a project with this name `{}`'.format(project))
        Printer.print_error(
            'You can a create new project with this command: '
            'polyaxon project create '
            '--name={} [--description=...] [--tags=...]'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    init_project = False
    if ProjectManager.is_initialized():
        local_project = ProjectManager.get_config()
        click.echo('Warning! This project is already initialized with the following project:')
        with indentation.indent(4):
            indentation.puts('User: {}'.format(local_project.user))
            indentation.puts('Project: {}'.format(local_project.name))
        if click.confirm('Would you like to override this current config?', default=False):
            init_project = True
    else:
        init_project = True

    if init_project:
        ProjectManager.purge()
        ProjectManager.set_config(project_config, init=True)
        Printer.print_success('Project was initialized')
    else:
        Printer.print_header('Project config was not changed.')

    init_ignore = False
    if IgnoreManager.is_initialized():
        click.echo('Warning! Found a .polyaxonignore file.')
        if click.confirm('Would you like to override it?', default=False):
            init_ignore = True
    else:
        init_ignore = True

    if init_ignore:
        IgnoreManager.init_config()
        Printer.print_success('New .polyaxonignore file was created.')
    else:
        Printer.print_header('.polyaxonignore file was not changed.')

    if polyaxonfile:
        create_polyaxonfile()
