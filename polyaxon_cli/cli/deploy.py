# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_cli.logger import clean_outputs
from polyaxon_cli.utils.formatting import Printer


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True),
              help='The polyaxon deployment config file(s) to check.')
@click.option('--manager_path', type=click.Path(exists=True),
              help='The path of the deployment manager, e.g. local chart.')
@click.option('--check', is_flag=True, default=False,
              help='Check if deployment file and other requirements are met.')
@click.option('--upgrade', is_flag=True, default=False,
              help='Upgrade a Polyaxon deployment.')
@clean_outputs
def deploy(file, manager_path, check, upgrade):  # pylint:disable=redefined-builtin
    if upgrade:
        Printer.print_warning('The command `polyaxon deploy [-f] --upgrade` is deprecated, '
                              'please use `polyaxon admin upgrade [-f]`.')
    elif check:
        Printer.print_warning('The command `polyaxon deploy [-f] --check` is deprecated, '
                              'please use `polyaxon admin deploy [-f] --check`.')
    else:
        Printer.print_warning('The command `polyaxon deploy [-f]` is deprecated, '
                              'please use `polyaxon admin deploy [-f]`.')


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True),
              help='The polyaxon deployment config file(s) to check.')
@clean_outputs
def teardown(file):  # pylint:disable=redefined-builtin
    Printer.print_warning('The command `polyaxon teardown [-f]` is deprecated, '
                          'please use `polyaxon admin teardown [-f]`.')
