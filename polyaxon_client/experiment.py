# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.experiment import (
    ExperimentConfig,
    ExperimentJobConfig,
    ExperimentStatusConfig,
    ExperimentMetricConfig)

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException


class ExperimentClient(PolyaxonClient):
    """Client to get experiments from the server"""
    ENDPOINT = "/"

    def list_experiments(self, page=1):
        """This gets all experiments visible to the user from the server."""
        try:
            response = self.get(self._get_http_url('/experiments'),
                                params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiments')
            return []

    def get_experiment(self, username, project_name, experiment_sequence):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence)
        try:
            response = self.get(request_url)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment')
            return None

    def update_experiment(self, username, project_name, experiment_sequence, patch_dict):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence)
        try:
            response = self.patch(request_url, json_data=patch_dict)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating experiment')
            return None

    def delete_experiment(self, username, project_name, experiment_sequence):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence)
        try:
            return self.delete(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting experiment')
            return None

    def get_statuses(self, username, project_name, experiment_sequence, page=1):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'statuses')
        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentStatusConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment status')
            return None

    def get_metrics(self, username, project_name, experiment_sequence, page=1):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'metrics')
        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentMetricConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment status')
            return None

    def create_metric(self, username, project_name, experiment_sequence, values):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'metrics')
        try:
            response = self.post(request_url, data={'values': values})
            return ExperimentMetricConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment status')
            return None

    def list_jobs(self, username, project_name, experiment_sequence, page=1):
        """Fetch list of jobs related to this experiment."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'jobs')

        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentJobConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving jobs')
            return []

    def restart(self, username, project_name, experiment_sequence):
        """Restart an experiment."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'restart')

        try:
            response = self.post(request_url)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while restarting experiment')
            return None

    def stop(self, username, project_name, experiment_sequence):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'stop')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while stopping experiment')
            return None

    def resources(self, username, project_name, experiment_sequence, message_handler=None):
        """Streams experiments resources using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'resources')
        self.socket(request_url, message_handler=message_handler)

    def logs(self, username, project_name, experiment_sequence, message_handler=None):
        """Streams experiments logs using websockets.

        message_handler: handles the messages received from server.
            e.g. def f(x): print(x)
        """
        request_url = self._build_url(self._get_ws_url(),
                                      username,
                                      project_name,
                                      'experiments',
                                      experiment_sequence,
                                      'logs')
        self.socket(request_url, message_handler=message_handler)
