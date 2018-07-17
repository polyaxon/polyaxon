# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException
from polyaxon_schemas.job import JobConfig, JobStatusConfig


class BuildJobClient(PolyaxonClient):
    """Client to get build jobs from the server"""
    ENDPOINT = "/"

    def get_build(self, username, project_name, job_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_id)
        try:
            response = self.get(request_url)
            return JobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving build')
            return None

    def update_build(self, username, project_name, job_id, patch_dict):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_id)
        try:
            response = self.patch(request_url, json_data=patch_dict)
            return JobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating build')
            return None

    def delete_build(self, username, project_name, job_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_id)
        try:
            return self.delete(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting build')
            return None

    def get_statuses(self, username, project_name, job_id, page=1):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_id,
                                      'statuses')
        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, JobStatusConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving build statuses')
            return None

    def stop(self, username, project_name, job_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_id,
                                      'stop')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while stopping build')
            return None

    def bookmark(self, username, project_name, job_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_id,
                                      'bookmark')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while bookmarking build')
            return None

    def unbookmark(self, username, project_name, job_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_id,
                                      'unbookmark')
        try:
            return self.delete(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while unbookmarking build')
            return None

    def resources(self, username, project_name, job_id, message_handler=None):
        """Streams builds resources using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_id,
                                      'resources')
        self.socket(request_url, message_handler=message_handler)

    # pylint:disable=inconsistent-return-statements
    def logs(self, username, project_name, job_id, stream=True, message_handler=None):
        """Streams builds logs using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        if not stream:
            request_url = self._build_url(self._get_http_url(),
                                          username,
                                          project_name,
                                          'builds',
                                          job_id,
                                          'logs')

            try:
                return self.get(request_url)
            except PolyaxonException as e:
                self.handle_exception(e=e, log_message='Error while retrieving builds')
                return []

        request_url = self._build_url(self._get_ws_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_id,
                                      'logs')
        self.socket(request_url, message_handler=message_handler)
