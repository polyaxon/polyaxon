# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_cli.managers.ignore import IgnoreManager
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_cli.utils.files import create_tarfile, get_files_in_current_directory
from polyaxon_cli.utils.formatting import Printer


@click.command()
def upload():
    """Upload code for current set project."""
    if not ProjectManager.is_initialized():
        Printer.print_error('Please initialize your project before uploading any code.'
                            '`polyaxon init PROJECT_NAME [--run|--model]`')
    project = ProjectManager.get_config()
    files = IgnoreManager.get_unignored_file_paths()
    filepath = create_tarfile(files, project.name)
    files, files_size = get_files_in_current_directory('repo', [filepath])
    PolyaxonClients().project.upload_repo(project.uuid.hex, files, files_size)
    Printer.print_success('Files upload.')
