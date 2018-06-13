# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.job import JobConfig, JobStatusConfig

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException


class BuildJobClient(PolyaxonClient):
    """Client to get build jobs from the server"""
    ENDPOINT = "/"

    def get_job(self, username, project_name, job_sequence):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_sequence)
        try:
            response = self.get(request_url)
            return JobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving job')
            return None

    def update_job(self, username, project_name, job_sequence, patch_dict):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_sequence)
        try:
            response = self.patch(request_url, json_data=patch_dict)
            return JobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating job')
            return None

    def delete_job(self, username, project_name, job_sequence):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_sequence)
        try:
            return self.delete(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting job')
            return None

    def get_statuses(self, username, project_name, job_sequence, page=1):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_sequence,
                                      'statuses')
        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, JobStatusConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving job status')
            return None

    def stop(self, username, project_name, job_sequence):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_sequence,
                                      'stop')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while stopping job')
            return None

    def resources(self, username, project_name, job_sequence, message_handler=None):
        """Streams builds resources using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(),
                                      username,
                                      project_name,
                                      'builds',
                                      job_sequence,
                                      'resources')
        self.socket(request_url, message_handler=message_handler)

    # pylint:disable=inconsistent-return-statements
    def logs(self, username, project_name, job_sequence, stream=True, message_handler=None):
        """Streams builds logs using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        if not stream:
            request_url = self._build_url(self._get_http_url(),
                                          username,
                                          project_name,
                                          'builds',
                                          job_sequence,
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
                                      job_sequence,
                                      'logs')
        self.socket(request_url, message_handler=message_handler)
