# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import sys

from polyaxon_client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError

from polyaxon_cli.managers.ignore import IgnoreManager
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.files import create_tarfile, get_files_in_current_directory
from polyaxon_cli.utils.formatting import Printer


@click.command()
@click.option('--async', is_flag=True, default=True, help='Upload synchronously.')
def upload(async):
    """Upload code of the current directory while respecting the .polyaxonignore file."""
    project = ProjectManager.get_config_or_raise()
    files = IgnoreManager.get_unignored_file_paths()
    file_path = create_tarfile(files, project.name)
    files, files_size = get_files_in_current_directory('repo', [file_path])
    try:
        PolyaxonClients().project.upload_repo(project.user, project.name, files, files_size, async)
    except (PolyaxonHTTPError, PolyaxonShouldExitError) as e:
        Printer.print_error('Could not upload code for project `{}`.'.format(project.name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
    Printer.print_success('Files uploaded.')
