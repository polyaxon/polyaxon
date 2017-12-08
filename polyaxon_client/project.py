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

    def list_projects(self):
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

    def get_project(self, uuid):
        request_url = self._build_url(self._get_url(), uuid)
        try:
            response = self.get(request_url)
            return ProjectConfig.from_dict(response.json())
        except NotFoundError:
            return None

    def create_project(self, config):
        try:
            response = self.post(self._get_url(), json=config.to_dict())
            return ProjectConfig.from_dict(response.json())
        except PolyaxonException as e:
            logger.info("Error while creating project: {}".format(e.message))
            if isinstance(e, AuthenticationError):
                # exit now since there is nothing we can do without login
                sys.exit(1)
            return None

    def update_project(self, uuid, config_dict):
        request_url = self._build_url(self._get_url(), uuid)
        try:
            response = self.patch(request_url, json=config_dict)
            return ProjectConfig.from_dict(response.json())
        except PolyaxonException as e:
            logger.info("Error while updating project: {}".format(e.message))
            if isinstance(e, AuthenticationError):
                # exit now since there is nothing we can do without login
                sys.exit(1)
            return None

    def delete_project(self, uuid):
        request_url = self._build_url(self._get_url(), uuid)
        try:
            self.delete(request_url)
        except PolyaxonException as e:
            logger.info("Error while updating project: {}".format(e.message))
            if isinstance(e, AuthenticationError):
                # exit now since there is nothing we can do without login
                sys.exit(1)
            return None
