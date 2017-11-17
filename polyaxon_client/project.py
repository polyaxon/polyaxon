# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_schemas.project import ProjectConfig
from polyaxon_schemas.polyaxonfile.logger import logger

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException, AuthenticationError, NotFoundError


class ProjectClient(PolyaxonClient):
    """Client to get projects from the server"""
    ENDPOINT = "/projects"

    def get_projects(self):
        try:
            response = self.get(self._get_url())
            projects_dict = response.json()
            return [ProjectConfig.from_dict(project) 
                    for project in projects_dict.get("results", [])]
        except PolyaxonException as e:
            logger.info("Error while retrieving projects: {}".format(e.message))
            if isinstance(e, AuthenticationError):
                # exit now since there is nothing we can do without login
                sys.exit(1)
            return []

    def get_by_name(self, username, projectname):
        request_url = self._build_url(self._get_url(), username, projectname)
        try:
            response = self.get(request_url)
            return ProjectConfig.from_dict(response.json())
        except NotFoundError:
            return None
