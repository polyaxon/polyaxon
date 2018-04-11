# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys

from collections import OrderedDict

import click

from polyaxon_cli.utils import constants
from polyaxon_cli.utils.formatting import Printer, dict_tabulate
from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile
from polyaxon_schemas.utils import to_list


def check_polyaxonfile(file, log=True):  # pylint:disable=redefined-builtin
    file = to_list(file)
    exists = [os.path.isfile(f) for f in file]

    if not any(exists):
        Printer.print_error('Polyaxonfile is not present, '
                            'please run {}'.format(constants.INIT_COMMAND))
        sys.exit(1)

    try:
        plx_file = PolyaxonFile(file)
        if log:
            Printer.print_success("Polyaxonfile valid")
        return plx_file
    except Exception as e:
        Printer.print_error("Polyaxonfile is not valid ")
        Printer.print_error('Error message `{}`.'.format(e))
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
@click.option('--experiments', '-x', is_flag=True, default=False,
              help='Checks and prints the matrix space of experiments.')
def check(file,  # pylint:disable=redefined-builtin
          all,  # pylint:disable=redefined-builtin
          version,
          run_type,
          project,
          experiments):
    """Check a polyaxonfile."""
    file = file or 'polyaxonfile.yml'
    specification = check_polyaxonfile(file).specification

    if version:
        Printer.decorate_format_value('The version is: {}',
                                      specification.version,
                                      'yellow')

    if run_type:
        Printer.decorate_format_value('The run-type is: {}',
                                      specification.run_type,
                                      'yellow')

    if project:
        Printer.decorate_format_value('The project is: {}',
                                      specification.project.name,
                                      'yellow')

    if experiments:
        matrix_space, n_experiments, concurrency, search_method = specification.experiments_def
        if matrix_space == 1:
            Printer.decorate_format_value('This polyaxon specification has {}',
                                          'One experiment',
                                          'yellow')
        else:
            click.echo(
                'This polyaxon specification has experiment group with the following definition:')
            get_group_experiments_info(matrix_space, n_experiments, concurrency, search_method)

    if all:
        click.echo("Validated file:\n{}".format(specification.parsed_data))

    return specification
