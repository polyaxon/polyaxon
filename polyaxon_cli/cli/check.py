# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile

from polyaxon_client.logger import logger

from polyaxon_cli.utils.formatting import Printer


def check_polyaxonfile(file):
    try:
        plx_file = PolyaxonFile.read(file)
        Printer.print_success("Polyaxonfile valid")
        return plx_file
    except Exception as e:
        Printer.print_error("Polyaxonfile is not valid")
        logger.exception(e)


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), help='The polyaxon file to check.')
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
    plx_file = check_polyaxonfile(file)

    def get_result(value):
        return click.style('{}'.format(value), fg='yellow')

    if version:
        click.echo('The version is: {}'.format(get_result(plx_file.version)))

    if run_type:
        click.echo("The run-type is: {}".format(get_result(plx_file.run_type)))

    if project:
        click.echo("The project definition is: {}".format(get_result(plx_file.project.to_dict())))

    if log_path:
        click.echo("The project logging path is: {}".format(get_result(plx_file.project_path)))

    if matrix:
        declarations = [str(d) for d in plx_file.matrix_declarations]
        declarations = get_result('\n'.join(declarations))
        click.echo("The matrix definition is:\n{}".format(declarations))

    if experiments:
        num_experiments, concurrency = plx_file.experiments_def
        if num_experiments == 1:
            result = get_result('One experiment')
            click.echo("This polyaxon specification has {}".format(result))
        elif concurrency == 1:
            num_experiments = get_result(num_experiments)
            concurrency = get_result('sequential')
            click.echo("The matrix-space has {} experiments, "
                       "with {} runs".format(num_experiments, concurrency))
        else:
            num_experiments, concurrency = get_result(num_experiments), get_result(concurrency)
            click.echo("The matrix-space has {} experiments,"
                       "with {} concurrent runs".format(num_experiments, concurrency))

    if all:
        click.echo("Validated file:\n{}".format(plx_file.parsed_data))

    return plx_file
