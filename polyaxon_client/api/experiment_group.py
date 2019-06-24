# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.schemas import ExperimentConfig, GroupConfig, GroupStatusConfig


class ExperimentGroupApi(BaseApiHandler):
    """
    Api handler to get experiments for a group from the server.
    """
    ENDPOINT = "/"

    def get_experiment_group(self, username, project_name, group_id):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'groups',
                                     group_id)
        try:
            response = self.transport.get(request_url)
            return self.prepare_results(response_json=response.json(), config=GroupConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving project')
            return None

    def list_experiments(self,
                         username,
                         project_name,
                         group_id,
                         metrics=None,
                         params=None,
                         query=None,
                         sort=None,
                         page=1):
        """Fetch list of experiments related to this experiment group."""
        request_url = self.build_url(self._get_http_url(), username, project_name, 'experiments')

        try:
            request_params = self.get_page(page=page)
            request_params['group'] = group_id
            if metrics:
                request_params['metrics'] = metrics
            if params:
                request_params['params'] = params
            if query:
                request_params['query'] = query
            if sort:
                request_params['sort'] = sort
            response = self.transport.get(request_url, params=request_params)
            return self.prepare_list_results(response.json(), page, ExperimentConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving experiments')
            return []

    def update_experiment_group(self,
                                username,
                                project_name,
                                group_id,
                                patch_dict,
                                background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'groups',
                                     group_id)

        if background:
            self.transport.async_patch(request_url, json_data=patch_dict)
            return None

        try:
            response = self.transport.patch(request_url, json_data=patch_dict)
            return self.prepare_results(response_json=response.json(), config=GroupConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while updating project')
            return None

    def delete_experiment_group(self, username, project_name, group_id, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'groups',
                                     group_id)

        if background:
            self.transport.async_delete(request_url)
            return None

        try:
            response = self.transport.delete(request_url)
            return response
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while deleting experiment group')
            return None

    def get_statuses(self, username, project_name, group_id, page=1):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'groups',
                                     group_id,
                                     'statuses')
        try:
            response = self.transport.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, GroupStatusConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving group statuses')
            return None

    def create_status(self,
                      username,
                      project_name,
                      group_id,
                      status,
                      message=None,
                      background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'groups',
                                     group_id,
                                     'statuses')

        json_data = {'status': status}
        if message:
            json_data['message'] = message
        if background:
            self.transport.async_post(request_url, json_data=json_data)
            return None

        try:
            response = self.transport.post(request_url, json_data=json_data)
            return self.prepare_results(response_json=response.json(),
                                        config=GroupStatusConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while creating group status.')
            return None

    def stop(self, username, project_name, group_id, pending=False, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'groups',
                                     group_id,
                                     'stop')
        json_data = None
        if pending is True:
            json_data = {'pending': pending}

        if background:
            self.transport.async_post(request_url, json_data=json_data)
            return None

        try:
            return self.transport.post(request_url, json_data=json_data)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while stopping experiments in group')
            return None

    def start_tensorboard(self,
                          username,
                          project_name,
                          group_id,
                          content=None,
                          is_managed=True,
                          background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'groups',
                                     group_id,
                                     'tensorboard',
                                     'start')

        job_config = {
            'content': self.validate_content(content=content),
            'is_managed': is_managed
        } if content else {}

        if background:
            self.transport.async_post(request_url, json_data=job_config)
            return None

        try:
            return self.transport.post(request_url, json_data=job_config)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while starting tensorboard')
            return None

    def stop_tensorboard(self, username, project_name, group_id, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'groups',
                                     group_id,
                                     'tensorboard',
                                     'stop')

        if background:
            self.transport.async_post(request_url)
            return None

        try:
            return self.transport.post(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while stopping tensorboard')
            return None

    def bookmark(self, username, project_name, group_id, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'groups',
                                     group_id,
                                     'bookmark')

        if background:
            self.transport.async_post(request_url)
            return None

        try:
            return self.transport.post(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while bookmarking group')
            return None

    def unbookmark(self, username, project_name, group_id, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'groups',
                                     group_id,
                                     'unbookmark')

        if background:
            self.transport.async_delete(request_url)
            return None

        try:
            return self.transport.delete(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while unbookmarking group')
            return None
