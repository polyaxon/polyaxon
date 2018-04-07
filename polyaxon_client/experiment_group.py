# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException
from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ExperimentGroupConfig


class ExperimentGroupClient(PolyaxonClient):
    """Client to get experiments for a group from the server"""
    ENDPOINT = "/"

    def get_experiment_group(self, username, project_name, group_sequence):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_sequence)
        try:
            response = self.get(request_url)
            return ExperimentGroupConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving project')
            return None

    def list_experiments(self, username, project_name, group_sequence, page=1):
        """Fetch list of experiments related to this experiment group."""
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_sequence,
                                      'experiments')

        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ExperimentConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiments')
            return []

    def update_experiment_group(self, username, project_name, group_sequence, patch_dict):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_sequence)

        try:
            response = self.patch(request_url, json_data=patch_dict)
            return ExperimentGroupConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating project')
            return None

    def delete_experiment_group(self, username, project_name, group_sequence):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_sequence)
        try:
            response = self.delete(request_url)
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting experiment group')
            return None

    def stop(self, username, project_name, group_sequence, pending=False):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_sequence,
                                      'stop')
        json_data = None
        if pending is True:
            json_data = {'pending': pending}

        try:
            return self.post(request_url, json_data=json_data)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while stopping experiments in group')
            return None
