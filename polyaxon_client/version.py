# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.polyaxonfile.logger import logger

from polyaxon_client.base import PolyaxonClient
from polyaxon_schemas.version import CliVersionConfig


class VersionClient(PolyaxonClient):
    """Client to get API version from the server."""
    ENDPOINT = "/cli_version"

    def get_cli_version(self):
        response = self.get(self._get_url())
        data_dict = response.json()
        logger.debug("CLI Version info :{}".format(data_dict))
        return CliVersionConfig.from_dict(data_dict)
