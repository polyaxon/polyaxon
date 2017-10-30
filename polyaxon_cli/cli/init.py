# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_cli.exceptions import PolyaxonException
from polyaxon_cli.utils import constants
from polyaxon_cli.utils.files import create_init_file


@click.command()
@click.option('--model', is_flag=True, default=False,
              help='Init a polyaxon file with `model` step template.')
@click.option('--exec', is_flag=True, default=False,
              help='Init a polyaxon file with `exec` step template.')
def init(model, exec):
    """Command for initializing a polyaxonfile."""
    if not any([model, exec]) and not all([model, exec]):
        raise PolyaxonException("You must specify which file to create, "
                                "only one option si possible: `--model` or `--exec`.")

    result = False
    if model:
        result = create_init_file(constants.INIT_FILE_MODEL)

    elif exec:
        result = create_init_file(constants.INIT_FILE_EXEC)

    if result:
        click.secho("Polyaxonfile was created successfully `{}`".format(constants.INIT_FILE),
                    fg='green')
    else:
        click.secho("Something went wrong, init command did not create a file.\n"
                    "Possible reasons: you don't have the write to create the file, "
                    "or it already exists.",
                    fg='red')
