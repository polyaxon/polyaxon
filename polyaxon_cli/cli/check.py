# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import six

from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), help='The polyaxon file to check.')
@click.option('--all', '-a', type=click.Path(exists=True),
              help='Checks and prints the validated file.')
@click.option('--version', '-v', is_flag=True, default=False, help='Checks and prints the version.')
@click.option('--cluster', is_flag=True, default=False, help='Checks and prints the cluster def.')
@click.option('--run-type', is_flag=True, default=False, help='Checks and prints the run_type.')
@click.option('--project', '-p', is_flag=True, default=False,
              help='Checks and prints the project def.')
@click.option('--log-path', is_flag=True, default=False, help='Checks and prints the log path.')
@click.option('--experiments', '-x', is_flag=True, default=False,
              help='Checks and prints the matrix space of experiments.')
@click.option('--matrix', '-m', is_flag=True, default=False,
              help='Checks and prints the matrix def.')
def check(file, all, version, cluster, run_type, project, log_path, matrix, experiments):
    """Command for checking a polyaxonfile."""
    try:
        plx_file = PolyaxonFile(file)
        click.secho("Polyaxonfile valid", fg='green')
    except Exception as e:
        click.secho("Polyaxonfile is not valid", fg='red')
        raise PolyaxonFile(e)

    if version:
        click.echo('The version is: {}'.format(plx_file.version))

    if cluster:
        for xp in range(plx_file.matrix_space):
            cluster_def, is_distributed = plx_file.get_cluster_def_at(xp)
            click.echo('The cluster definition for experiment {} is: {}'.format(
                xp + 1, cluster_def))

    if run_type:
        click.echo('The run-type is: {}'.format(plx_file.run_type))

    if project:
        click.echo('The project definition is: {}'.format(plx_file.project.to_dict()))

    if log_path:
        click.echo('The project logging path is: {}'.format(plx_file.project_path))

    if matrix:
        declarations = [str(d) for d in plx_file.matrix_declarations]
        click.echo('The matrix definition is:\n{}'.format('\n'.join(declarations)))

    if experiments:
        experiments_def = plx_file.experiments_def
        if experiments_def[0] == 1:
            click.echo('One experiment')
        elif experiments_def[1] == 1:
            click.echo('The matrix-space is: {} running sequentially'.format(experiments_def[0]))
        else:
            click.echo('The matrix-space is: {} with {} concurrent runs'.format(*experiments_def))

    if all:
        click.echo('Validated file:\n{}'.format(plx_file.parsed_data))
