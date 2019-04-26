# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client import settings
from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.schemas import ExperimentConfig, GroupConfig, JobConfig, ProjectConfig


class BookmarkApi(BaseApiHandler):
    """
    Api handler to list or create bookmarks for experiment/jobs/projects/builds/groups
    """
    ENDPOINT = "/bookmarks"

    def prepare_list_results(self, response_json, current_page, config):
        list_results = {
            'count': response_json.get('count', 0),
            'next': current_page + 1 if response_json.get('next') else None,
            'previous': current_page - 1 if response_json.get('previous') else None
        }
        results = [obj.get('content_object') for obj in response_json.get("results", [])]
        if self.config.schema_response:
            list_results['results'] = [
                config.from_dict(obj, unknown=settings.RECEPTION_UNKNOWN_BEHAVIOUR)
                for obj in results]
        else:
            list_results['results'] = results

        return list_results

    def builds(self, username, page=1):
        """This gets all bookmarked builds from the server."""
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     'builds')
        try:
            response = self.transport.get(request_url,
                                          params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, JobConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving bookmarked builds.')
            return []

    def jobs(self, username, page=1):
        """This gets all bookmarked jobs from the server."""
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     'jobs')
        try:
            response = self.transport.get(request_url,
                                          params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, JobConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving bookmarked jobs.')
            return []

    def experiments(self, username, page=1):
        """This gets all bookmarked experiments from the server."""
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     'experiments')
        try:
            response = self.transport.get(request_url,
                                          params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving bookmarked experiments.')
            return []

    def groups(self, username, page=1):
        """This gets all bookmarked groups from the server."""
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     'groups')
        try:
            response = self.transport.get(request_url,
                                          params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, GroupConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving bookmarked groups.')
            return []

    def projects(self, username, page=1):
        """This gets all bookmarked projects from the server."""
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     'projects')
        try:
            response = self.transport.get(request_url,
                                          params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ProjectConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving bookmarked projects.')
            return []
