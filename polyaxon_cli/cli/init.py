# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

from polyaxon_client.exceptions import PolyaxonShouldExitError

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
    try:
        project_config = PolyaxonClients().project.get_project_by_name(project)
    except PolyaxonShouldExitError as e:
        Printer.print_error('Make sure you have a project with this name `{}`'.format(project))
        Printer.print_error('You can a new project with this command: '
                            'polyaxon project create --name={} --description=...'.format(project))
        sys.exit(0)

    if not any([model, run]) and not all([model, run]):
        Printer.print_error("You must specify which an init option, "
                            "possible values: `--model` or `--exec`.")
        sys.exit(0)

    result = False
    if model:
        result = create_init_file(constants.INIT_FILE_MODEL, project)

    elif run:
        result = create_init_file(constants.INIT_FILE_RUN, project)

    if result:
        ProjectManager.set_config(project_config)
        IgnoreManager.init_config()
        Printer.print_success(
            "Polyaxonfile was created successfully `{}`".format(constants.INIT_FILE))
    else:
        Printer.print_error(
            "Something went wrong, init command did not create a file.\n"
            "Possible reasons: you don't have the write to create the file, "
            "or it already exists.")
