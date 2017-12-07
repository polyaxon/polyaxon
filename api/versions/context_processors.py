# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from versions.models import CliVersion


def versions(request):
    return {'cli_version': CliVersion.load()}
