# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import click
import sys

import os
from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile
from polyaxon_schemas.polyaxonfile.specification import PluginSpecification
from polyaxon_schemas.utils import to_list

from polyaxon_cli.utils import constants
from polyaxon_cli.utils.formatting import Printer, dict_tabulate


def check_polyaxonfile(file, log=True, is_plugin=False):
    file = to_list(file)
    exists = [os.path.isfile(f) for f in file]

    if not any(exists):
        Printer.print_error('Polyaxonfile is not present, '
                            'please run {}'.format(constants.INIT_COMMAND))
        sys.exit(1)

    try:
        plx_file = PolyaxonFile.read(file)
        if is_plugin:
            plx_file = PluginSpecification.read(plx_file._data)
        if log:
            Printer.print_success("Polyaxonfile valid")
        return plx_file
    except Exception as e:
        Printer.print_error("Polyaxonfile is not valid")
        sys.exit(1)


def get_group_experiments_info(matrix_space, n_experiments, concurrency, search_method):
    info = OrderedDict()
    info['Matrix space contains'] = '{} experiments'.format(matrix_space)
    if n_experiments:
        info['Exploring a maximum of'] = '{} experiments'.format(n_experiments)
    info['Search method'] = search_method.lower()
    info['Concurrency'] = ('{} runs'.format('sequential')
                           if concurrency == 1 else
                           '{} concurrent runs'.format(concurrency))

    dict_tabulate(info)


@click.command()
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='The polyaxon file to check.')
@click.option('--all', '-a', is_flag=True, default=False,
              help='Checks and prints the validated file.')
@click.option('--version', '-v', is_flag=True, default=False, help='Checks and prints the version.')
@click.option('--run-type', is_flag=True, default=False, help='Checks and prints the run_type.')
@click.option('--project', '-p', is_flag=True, default=False,
              help='Checks and prints the project def.')
@click.option('--log-path', is_flag=True, default=False, help='Checks and prints the log path.')
@click.option('--experiments', '-x', is_flag=True, default=False,
              help='Checks and prints the matrix space of experiments.')
@click.option('--matrix', '-m', is_flag=True, default=False,
              help='Checks and prints the matrix def.')
def check(file, all, version, run_type, project, log_path, matrix, experiments):
    """Check a polyaxonfile."""
    file = file or 'polyaxonfile.yml'
    plx_file = check_polyaxonfile(file)

    if version:
        Printer.decorate_format_value('The version is: {}',
                                      plx_file.version,
                                      'yellow')

    if run_type:
        Printer.decorate_format_value('The run-type is: {}',
                                      plx_file.run_type,
                                      'yellow')

    if project:
        Printer.decorate_format_value('The project is: {}',
                                      plx_file.project.name,
                                      'yellow')
    if log_path:
        Printer.decorate_format_value('The project logging path is: {}',
                                      plx_file.project_path,
                                      'yellow')
    if matrix:
        declarations = '\n'.join([str(d) for d in plx_file.matrix_declarations])
        if not declarations:
            click.echo('This file has one independent experiment.')
        else:
            Printer.decorate_format_value('The matrix definition is:\n{}',
                                          declarations,
                                          'yellow')

    if experiments:
        matrix_space, n_experiments, concurrency, search_method = plx_file.experiments_def
        if matrix_space == 1:
            Printer.decorate_format_value('This polyaxon specification has {}',
                                          'One experiment',
                                          'yellow')
        else:
            click.echo(
                'This polyaxon specification has experiment group with the following definition:')
            get_group_experiments_info(matrix_space, n_experiments, concurrency, search_method)

    if all:
        click.echo("Validated file:\n{}".format(plx_file.parsed_data))

    return plx_file
