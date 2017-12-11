# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.experiment import (
    ExperimentJobStatusConfig,
    ExperimentJobConfig,
)

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException


class JobClient(PolyaxonClient):
    """Client to get jobs from the server"""
    ENDPOINT = "/jobs"

    def get_job(self, job_uuid):
        request_url = self._build_url(self._get_http_url(), job_uuid)
        try:
            response = self.get(request_url)
            return ExperimentJobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving job')
            return None

    def get_job_status(self, job_uuid):
        request_url = self._build_url(self._get_http_url(), job_uuid, 'statuses')

        try:
            response = self.get(request_url)
            return ExperimentJobStatusConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving job statuses')
            return []

    def resources(self, job_uuid, message_handler=None):
        """Streams job resources using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(), job_uuid, 'resources')
        self.socket(request_url, message_handler=message_handler)

    def logs(self, job_uuid, message_handler=None):
        """Streams job logs using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(), job_uuid, 'logs')
        self.socket(request_url, message_handler=message_handler)
