# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import rhea

from polyaxon_deploy.schemas.deployment import DeploymentConfig


def read(filepaths):
    data = rhea.read(filepaths)
    return DeploymentConfig.from_dict(data)
