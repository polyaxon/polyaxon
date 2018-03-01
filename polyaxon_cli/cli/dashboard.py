# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_cli.utils.clients import PolyaxonClients


@click.command()
@click.option('--yes', '-y', is_flag=True, default=False,
              help='Automatic yes to prompts. '
                   'Assume "yes" as answer to all prompts and run non-interactively.')
def dashboard(yes):
    """Open dashboard in browser."""
    dashboard_url = "{}".format(PolyaxonClients().auth.http_host)
    if not yes:
        click.confirm('Dashboard page will now open in your browser. Continue?',
                      abort=True, default=True)

    click.launch(dashboard_url)
