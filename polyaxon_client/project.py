# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ProjectConfig, ExperimentGroupConfig

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException, NotFoundError


class ProjectClient(PolyaxonClient):
    """Client to get projects from the server"""
    ENDPOINT = "/projects"

    def list_projects(self, page=1):
        try:
            response = self.get(self._get_http_url(), params=self.get_page(page=page))
            projects_dict = response.json()
            return [ProjectConfig.from_dict(project)
                    for project in projects_dict.get("results", [])]
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving projects')
            return []

    def get_project(self, project_uuid):
        request_url = self._build_url(self._get_http_url(), project_uuid)
        try:
            response = self.get(request_url)
            return ProjectConfig.from_dict(response.json())
        except NotFoundError:
            return None

    def create_project(self, project_config):
        try:
            response = self.post(self._get_http_url(), json=project_config.to_dict())
            return ProjectConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while creating project')
            return None

    def update_project(self, project_uuid, patch_dict):
        request_url = self._build_url(self._get_http_url(), project_uuid)
        try:
            response = self.patch(request_url, json=patch_dict)
            return ProjectConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating project')
            return None

    def delete_project(self, project_uuid):
        request_url = self._build_url(self._get_http_url(), project_uuid)
        try:
            response = self.delete(request_url)
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting project')
            return None

    def upload_repo(self, project_uuid, files, files_size=None):
        """Uploads code data related for this project from the current dir."""
        request_url = self._build_url(self._get_http_url(), project_uuid, 'repo', 'upload')

        try:
            response = self.upload(request_url, files=files, files_size=files_size)
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating project repo')
            return None

    def list_experiment_groups(self, project_uuid, page=1):
        """Fetch list of experiment groups related to this project."""
        request_url = self._build_url(self._get_http_url(), project_uuid, 'experiment_groups')

        try:
            response = self.get(request_url, params=self.get_page(page=page))
            experiment_group_dicts = response.json()
            return [ExperimentGroupConfig.from_dict(experiment_group)
                    for experiment_group in experiment_group_dicts.get("results", [])]
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment groups')
            return []

    def create_experiment_group(self, project_uuid, experiment_group_config):
        request_url = self._build_url(self._get_http_url(), project_uuid, 'experiment_groups')

        try:
            response = self.post(request_url, json=experiment_group_config.to_dict())
            return ExperimentGroupConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while creating experiment group')
            return None

    def update_experiment_group(self, project_uuid, experiment_group_uuid, patch_dict):
        request_url = self._build_url(self._get_http_url(),
                                      project_uuid,
                                      'experiment_groups',
                                      experiment_group_uuid)

        try:
            response = self.patch(request_url, json=patch_dict)
            return ExperimentGroupConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating project')
            return None

    def delete_experiment_group(self, project_uuid, experiment_group_uuid):
        request_url = self._build_url(self._get_http_url(),
                                      project_uuid,
                                      'experiment_groups',
                                      experiment_group_uuid)
        try:
            response = self.delete(request_url)
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting experiment group')
            return None

    def list_experiments(self, project_uuid, page=1):
        """Fetch list of experiments related to this project."""
        request_url = self._build_url(self._get_http_url(), project_uuid, 'experiments')

        try:
            response = self.get(request_url, params=self.get_page(page=page))
            experiment_dicts = response.json()
            return [ExperimentConfig.from_dict(experiment_group)
                    for experiment_group in experiment_dicts.get("results", [])]
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiments')
            return []

    def create_experiment(self, project_uuid, experiment_config):
        request_url = self._build_url(self._get_http_url(), project_uuid, 'experiments')

        try:
            response = self.post(request_url, json=experiment_config.to_dict())
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while creating experiment group')
            return None

    def add_tensorboard(self, uuid):
        # TODO
        pass
