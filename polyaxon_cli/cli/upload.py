# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_cli.cli.project import get_current_project
from polyaxon_cli.managers.ignore import IgnoreManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.files import create_tarfile, get_files_in_current_directory
from polyaxon_cli.utils.formatting import Printer


@click.command()
def upload():
    """Upload code for current set project."""
    project = get_current_project()
    files = IgnoreManager.get_unignored_file_paths()
    filepath = create_tarfile(files, project.name)
    files, files_size = get_files_in_current_directory('repo', [filepath])
    PolyaxonClients().project.upload_repo(project.user, project.name, files, files_size)
    Printer.print_success('Files upload.')
