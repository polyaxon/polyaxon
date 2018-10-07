# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

import click

from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import PolyaxonHTTPError, PolyaxonShouldExitError
from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.managers.ignore import IgnoreManager
from polyaxon_cli.managers.project import ProjectManager
from polyaxon_cli.utils.files import create_tarfile, get_files_in_current_directory
from polyaxon_cli.utils.formatting import Printer
from polyaxon_client.exceptions import PolyaxonClientException


@click.command()
@clean_outputs
def upload():  # pylint:disable=assign-to-new-keyword
    """Upload code of the current directory while respecting the .polyaxonignore file."""
    project = ProjectManager.get_config_or_raise()
    files = IgnoreManager.get_unignored_file_paths()
    with create_tarfile(files, project.name) as file_path:
        with get_files_in_current_directory('repo', [file_path]) as (files, files_size):
            try:
                PolyaxonClient().project.upload_repo(project.user,
                                                     project.name,
                                                     files,
                                                     files_size)
            except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
                Printer.print_error('Could not upload code for project `{}`.'.format(project.name))
                Printer.print_error('Error message `{}`.'.format(e))
                Printer.print_error('Check if you have access rights for this project and '
                                    'that you are not uploading large files.'
                                    'If you are running a notebook, '
                                    'you should stop it before uploading.')
                sys.exit(1)
            Printer.print_success('Files uploaded.')
