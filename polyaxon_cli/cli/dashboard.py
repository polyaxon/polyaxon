# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_cli.utils.clients import PolyaxonClients


@click.command()
def dashboard():
    """Open dashboard in browser."""
    dashboard_url = "{}/app/token".format(PolyaxonClients().auth.http_host)
    click.confirm('Dashboard page will now open in your browser. Continue?',
                  abort=True, default=True)

    click.launch(dashboard_url)
