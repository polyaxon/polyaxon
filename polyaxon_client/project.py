# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException
from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.job import JobConfig, TensorboardJobConfig
from polyaxon_schemas.project import ExperimentGroupConfig, ProjectConfig


class ProjectClient(PolyaxonClient):
    """Client to get projects from the server"""
    ENDPOINT = "/"

    def list_projects(self, username, page=1):
        request_url = self._build_url(self._get_http_url(), username)
        try:
            response = self.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ProjectConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving projects.')
            return []

    def get_project(self, username, project_name):
        request_url = self._build_url(self._get_http_url(), username, project_name)
        try:
            response = self.get(request_url)
            return ProjectConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving project.')
            return None

    def create_project(self, project_config):
        try:
            response = self.post(self._get_http_url('/projects'),
                                 json_data=project_config.to_dict())
            return ProjectConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while creating project.')
            return None

    def update_project(self, username, project_name, patch_dict):
        request_url = self._build_url(self._get_http_url(), username, project_name)
        try:
            response = self.patch(request_url, json_data=patch_dict)
            return ProjectConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating project.')
            return None

    def delete_project(self, username, project_name):
        request_url = self._build_url(self._get_http_url(), username, project_name)
        try:
            response = self.delete(request_url)
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting project.')
            return None

    def upload_repo(self, username, project_name, files, files_size=None, upload_async=True):
        """Uploads code data related for this project from the current dir."""
        request_url = self._build_url(
            self._get_http_url(), username, project_name, 'repo', 'upload')

        json_data = None
        if upload_async is False:
            json_data = {'async': upload_async}
        try:
            response = self.upload(request_url,
                                   files=files,
                                   files_size=files_size,
                                   json_data=json_data)
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating project repo.')
            return None

    def download_repo(self, username, project_name):
        """Downloads code for this project to the current dir."""
        request_url = self._build_url(
            self._get_http_url(), username, project_name, 'repo', 'download')

        try:
            response = self.download(request_url, 'repo.tar.gz')
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while downloading project repo.')
            return None

    def list_experiment_groups(self, username, project_name, query=None, sort=None, page=1):
        """Fetch list of experiment groups related to this project."""
        request_url = self._build_url(
            self._get_http_url(), username, project_name, 'groups')

        try:
            params = self.get_page(page=page)
            if query:
                params['query'] = query
            if sort:
                params['sort'] = sort
            response = self.get(request_url, params=params)
            return self.prepare_list_results(response.json(), page, ExperimentGroupConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment groups.')
            return []

    def create_experiment_group(self, username, project_name, experiment_group_config):
        if isinstance(experiment_group_config, Mapping):
            experiment_group_config = ExperimentGroupConfig.from_dict(experiment_group_config)
        elif not isinstance(experiment_group_config, ExperimentGroupConfig):
            raise PolyaxonException('create_experiment_group received an invalid '
                                    'experiment_group_config.')

        request_url = self._build_url(
            self._get_http_url(), username, project_name, 'groups')

        try:
            response = self.post(request_url, json_data=experiment_group_config.to_dict())
            return ExperimentGroupConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while creating experiment group.')
            return None

    def list_experiments(self,
                         username,
                         project_name,
                         independent=None,
                         group=None,
                         metrics=None,
                         declarations=None,
                         query=None,
                         sort=None,
                         page=1):
        """Fetch list of experiments related to this project."""
        request_url = self._build_url(self._get_http_url(), username, project_name, 'experiments')

        try:
            params = self.get_page(page=page)
            if independent:
                params['independent'] = independent
            if group:
                params['group'] = group
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
            self.handle_exception(e=e, log_message='Error while retrieving experiments.')
            return []

    def create_experiment(self, username, project_name, experiment_config):
        if isinstance(experiment_config, Mapping):
            experiment_config = ExperimentConfig.from_dict(experiment_config)
        elif not isinstance(experiment_config, ExperimentConfig):
            raise PolyaxonException('create_experiment received an invalid experiment_config.')

        request_url = self._build_url(self._get_http_url(), username, project_name, 'experiments')

        try:
            response = self.post(request_url, json_data=experiment_config.to_dict())
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while creating experiment.')
            return None

    def list_jobs(self, username, project_name, query=None, sort=None, page=1):
        """Fetch list of jobs related to this project."""
        request_url = self._build_url(
            self._get_http_url(), username, project_name, 'jobs')

        try:
            params = self.get_page(page=page)
            if query:
                params['query'] = query
            if sort:
                params['sort'] = sort
            response = self.get(request_url, params=params)
            return self.prepare_list_results(response.json(), page, JobConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving jobs.')
            return []

    def create_job(self, username, project_name, job_config):
        if isinstance(job_config, Mapping):
            job_config = JobConfig.from_dict(job_config)
        elif not isinstance(job_config, JobConfig):
            raise PolyaxonException('create_job received an invalid job_config.')

        request_url = self._build_url(self._get_http_url(), username, project_name, 'jobs')

        try:
            response = self.post(request_url, json_data=job_config.to_dict())
            return JobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while creating job.')
            return None

    def list_builds(self, username, project_name, query=None, sort=None, page=1):
        """Fetch list of build jobs related to this project."""
        request_url = self._build_url(
            self._get_http_url(), username, project_name, 'builds')

        try:
            params = self.get_page(page=page)
            if query:
                params['query'] = query
            if sort:
                params['sort'] = sort
            response = self.get(request_url, params=params)
            return self.prepare_list_results(response.json(), page, JobConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving build jobs.')
            return []

    def create_build(self, username, project_name, build_config):
        if isinstance(build_config, Mapping):
            build_config = JobConfig.from_dict(build_config)
        elif not isinstance(build_config, JobConfig):
            raise PolyaxonException('create_build received an invalid build_config.')

        request_url = self._build_url(self._get_http_url(), username, project_name, 'builds')

        try:
            response = self.post(request_url, json_data=build_config.to_dict())
            return JobConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while creating build job.')
            return None

    def list_tensorboards(self, username, project_name, query=None, sort=None, page=1):
        """Fetch list of tensorboard jobs related to this project."""
        request_url = self._build_url(
            self._get_http_url(), username, project_name, 'tensorboards')

        try:
            params = self.get_page(page=page)
            if query:
                params['query'] = query
            if sort:
                params['sort'] = sort
            response = self.get(request_url, params=params)
            return self.prepare_list_results(response.json(), page, TensorboardJobConfig)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving tensorboard jobs.')
            return []

    def start_tensorboard(self, username, project_name, job_config=None):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'tensorboard',
                                      'start')

        try:
            job_config = {'config': job_config} if job_config else {}
            return self.post(request_url, json_data=job_config)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while starting tensorboard.')
            return None

    def stop_tensorboard(self, username, project_name):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'tensorboard',
                                      'stop')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while stopping tensorboard.')
            return None

    def start_notebook(self, username, project_name, job_config=None):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'notebook',
                                      'start')

        try:
            job_config = {'config': job_config} if job_config else {}
            return self.post(request_url, json_data=job_config)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while starting notebook.')
            return None

    def stop_notebook(self, username, project_name, commit=True):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'notebook',
                                      'stop')
        json_data = None
        if commit is False:
            json_data = {'commit': commit}
        try:
            return self.post(request_url, json_data=json_data)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while stopping notebook.')
            return None

    def bookmark(self, username, project_name):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'bookmark')
        try:
            return self.post(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while bookmarking project.')
            return None

    def unbookmark(self, username, project_name):
        request_url = self._build_url(self._get_http_url(),
                                      username,
                                      project_name,
                                      'unbookmark')
        try:
            return self.delete(request_url)
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while unbookmarking project.')
            return None
