# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException
from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ExperimentGroupConfig, GroupStatusConfig


class ExperimentGroupClient(PolyaxonClient):
    """Client to get experiments for a group from the server"""
    ENDPOINT = "/"

    def get_experiment_group(self, username, project_name, group_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_id)
        try:
            response = self.get(request_url)
            return ExperimentGroupConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving project')
            return None

    def list_experiments(self,
                         username,
                         project_name,
                         group_id,
                         metrics=None,
                         declarations=None,
                         query=None,
                         sort=None,
                         page=1):
        """Fetch list of experiments related to this experiment group."""
        request_url = self._build_url(self._get_http_url(), username, project_name, 'experiments')

        try:
            params = self.get_page(page=page)
            params['group'] = group_id
            if metrics:
                params['metrics'] = metrics
            if declarations:
                params['declarations'] = declarations
            if query:
                params['query'] = query
            if sort:
                params['sort'] = sort
            response = self.get(request_url, params=params)
            return self.prepare_list_results(response.json(), page, ExperimentConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiments')
            return []

    def update_experiment_group(self, username, project_name, group_id, patch_dict):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_id)

        try:
            response = self.patch(request_url, json_data=patch_dict)
            return ExperimentGroupConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating project')
            return None

    def delete_experiment_group(self, username, project_name, group_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_id)
        try:
            response = self.delete(request_url)
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting experiment group')
            return None

    def get_statuses(self, username, project_name, group_id, page=1):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_id,
                                      'statuses')
        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, GroupStatusConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving group statuses')
            return None

    def stop(self, username, project_name, group_id, pending=False):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_id,
                                      'stop')
        json_data = None
        if pending is True:
            json_data = {'pending': pending}

        try:
            return self.post(request_url, json_data=json_data)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while stopping experiments in group')
            return None

    def start_tensorboard(self, username, project_name, group_id, job_config=None):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_id,
                                      'tensorboard',
                                      'start')

        try:
            job_config = {'config': job_config} if job_config else {}
            return self.post(request_url, json_data=job_config)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while starting tensorboard')
            return None

    def stop_tensorboard(self, username, project_name, group_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_id,
                                      'tensorboard',
                                      'stop')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while stopping tensorboard')
            return None

    def bookmark(self, username, project_name, group_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_id,
                                      'bookmark')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while bookmarking group')
            return None

    def unbookmark(self, username, project_name, group_id):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'groups',
                                      group_id,
                                      'unbookmark')
        try:
            return self.delete(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while unbookmarking group')
            return None
