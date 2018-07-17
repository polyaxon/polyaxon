# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException
from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.job import JobConfig
from polyaxon_schemas.project import ExperimentGroupConfig, ProjectConfig


class BookmarkClient(PolyaxonClient):
    """Client to list or create bookmarks for experiment/jobs/projects/builds/groups"""
    ENDPOINT = "/bookmarks"

    @staticmethod
    def prepare_list_results(response_json, current_page, config):
        return {
            'count': response_json.get('count', 0),
            'next': current_page + 1 if response_json.get('next') else None,
            'previous': current_page - 1 if response_json.get('previous') else None,
            'results': [config.from_dict(obj.get('content_object'))
                        for obj in response_json.get("results", [])]}

    def builds(self, username, page=1):
        """This gets all bookmarked builds from the server."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      'builds')
        try:
            response = self.get(request_url,
                                params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, JobConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving bookmarked builds.')
            return []

    def jobs(self, username, page=1):
        """This gets all bookmarked jobs from the server."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      'jobs')
        try:
            response = self.get(request_url,
                                params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, JobConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving bookmarked jobs.')
            return []

    def experiments(self, username, page=1):
        """This gets all bookmarked experiments from the server."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      'experiments')
        try:
            response = self.get(request_url,
                                params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving bookmarked experiments.')
            return []

    def groups(self, username, page=1):
        """This gets all bookmarked groups from the server."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      'groups')
        try:
            response = self.get(request_url,
                                params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentGroupConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving bookmarked groups.')
            return []

    def projects(self, username, page=1):
        """This gets all bookmarked projects from the server."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      'projects')
        try:
            response = self.get(request_url,
                                params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ProjectConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving bookmarked projects.')
            return []
