# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.schemas import (
    BuildJobConfig,
    ExperimentConfig,
    GroupConfig,
    JobConfig,
    ProjectConfig,
    TensorboardJobConfig
)


class ProjectApi(BaseApiHandler):
    """
    Api handler to get projects from the server.
    """
    ENDPOINT = "/"

    def list_projects(self, username, page=1):
        request_url = self.build_url(self._get_http_url(), username)
        try:
            response = self.transport.get(request_url, params=self.get_page(page=page))
            return self.prepare_list_results(response.json(), page, ProjectConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving projects.')
            return []

    def get_project(self, username, project_name):
        request_url = self.build_url(self._get_http_url(), username, project_name)
        try:
            response = self.transport.get(request_url)
            return self.prepare_results(response_json=response.json(), config=ProjectConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving project.')
            return None

    def create_project(self, project_config):
        project_config = self.validate_config(config=project_config, config_schema=ProjectConfig)
        try:
            response = self.transport.post(self._get_http_url('/projects'),
                                           json_data=project_config.to_dict())
            return self.prepare_results(response_json=response.json(), config=ProjectConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while creating project.')
            return None

    def update_project(self, username, project_name, patch_dict, background=False):
        request_url = self.build_url(self._get_http_url(), username, project_name)

        if background:
            self.transport.async_patch(request_url, json_data=patch_dict)
            return None

        try:
            response = self.transport.patch(request_url, json_data=patch_dict)
            return self.prepare_results(response_json=response.json(), config=ProjectConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while updating project.')
            return None

    def delete_project(self, username, project_name, background=False):
        request_url = self.build_url(self._get_http_url(), username, project_name)

        if background:
            self.transport.async_delete(request_url)
            return None

        try:
            response = self.transport.delete(request_url)
            return response
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while deleting project.')
            return None

    def enable_ci(self, username, project_name, config=None, background=False):
        """Enable ci on the project"""
        request_url = self.build_url(
            self._get_http_url(), username, project_name, 'ci')
        json_data = {}
        if config:
            json_data['config'] = config

        if background:
            self.transport.async_post(request_url, json_data=json_data)
            return None

        try:
            response = self.transport.post(request_url, json_data=json_data)
            return response
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while enabling ci on project.')
            return None

    def disable_ci(self, username, project_name, background=False):
        """Disable ci on the project"""
        request_url = self.build_url(
            self._get_http_url(), username, project_name, 'ci')

        if background:
            self.transport.async_delete(request_url)
            return None

        try:
            response = self.transport.delete(request_url)
            return response
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while disabling ci on project.')
            return None

    def set_repo(self, username, project_name, git_url, is_public=True, background=False):
        """Set a git url on the project to use as a code repo."""
        request_url = self.build_url(
            self._get_http_url(), username, project_name, 'repo', 'external')

        json_data = {
            'git_url': git_url,
            'is_public': is_public
        }
        if background:
            self.transport.async_post(request_url, json_data=json_data)
            return None

        try:
            response = self.transport.post(request_url, json_data=json_data)
            return response
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while setting external repo on project.')
            return None

    def sync_repo(self, username, project_name, background=False):
        """Sync the external git repo of the project."""
        request_url = self.build_url(
            self._get_http_url(), username, project_name, 'repo', 'sync')

        if background:
            self.transport.async_post(request_url)
            return None

        try:
            response = self.transport.post(request_url)
            return response
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while syncing external repo on project.')
            return None

    def upload_repo(self,
                    username,
                    project_name,
                    files,
                    files_size=None,
                    sync=False,
                    background=False):
        """Uploads code data related for this project from the current dir."""
        request_url = self.build_url(
            self._get_http_url(), username, project_name, 'repo', 'upload')

        json_data = {}
        if sync:
            json_data['sync'] = sync

        if background:
            self.transport.async_upload(request_url,
                                        files=files,
                                        files_size=files_size,
                                        json_data=json_data)
            return None

        try:
            response = self.transport.upload(request_url,
                                             files=files,
                                             files_size=files_size,
                                             json_data=json_data)
            return response
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while updating project repo.')
            return None

    def download_repo(self,
                      username,
                      project_name,
                      commit=None,
                      filename=None,
                      untar=False,
                      delete_tar=True,
                      extract_path=None):
        """Downloads code for this project to the current dir."""
        request_url = self.build_url(
            self._get_http_url(), username, project_name, 'repo', 'download')

        params = {}
        if commit:
            params['commit'] = commit

        filename = filename or 'repo.tar.gz'

        try:
            response = self.transport.download(
                request_url,
                filename=filename,
                params=params,
                untar=untar,
                delete_tar=delete_tar,
                extract_path=extract_path)
            return response
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while downloading project repo.')
            return None

    def list_experiment_groups(self, username, project_name, query=None, sort=None, page=1):
        """Fetch list of experiment groups related to this project."""
        request_url = self.build_url(
            self._get_http_url(), username, project_name, 'groups')

        try:
            params = self.get_page(page=page)
            if query:
                params['query'] = query
            if sort:
                params['sort'] = sort
            response = self.transport.get(request_url, params=params)
            return self.prepare_list_results(response.json(), page, GroupConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving experiment groups.')
            return []

    def create_experiment_group(self,
                                username,
                                project_name,
                                experiment_group_config,
                                background=False):
        experiment_group_config = self.validate_config(config=experiment_group_config,
                                                       config_schema=GroupConfig)
        request_url = self.build_url(self._get_http_url(), username, project_name, 'groups')

        if background:
            self.transport.async_post(request_url, json_data=experiment_group_config.to_dict())
            return None

        try:
            response = self.transport.post(request_url, json_data=experiment_group_config.to_dict())
            return self.prepare_results(response_json=response.json(), config=GroupConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while creating experiment group.')
            return None

    def list_experiments(self,
                         username,
                         project_name,
                         independent=None,
                         group=None,
                         metrics=None,
                         params=None,
                         query=None,
                         sort=None,
                         page=1):
        """Fetch list of experiments related to this project."""
        request_url = self.build_url(self._get_http_url(), username, project_name, 'experiments')

        try:
            request_params = self.get_page(page=page)
            if independent:
                request_params['independent'] = independent
            if group:
                request_params['group'] = group
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
            self.transport.handle_exception(e=e, log_message='Error while retrieving experiments.')
            return []

    def create_experiment(self,
                          username,
                          project_name,
                          experiment_config,
                          group=None,
                          background=False):
        experiment_config = self.validate_config(config=experiment_config,
                                                 config_schema=ExperimentConfig)
        experiment_data = experiment_config.to_dict()
        if group:
            experiment_data['experiment_group'] = group
        request_url = self.build_url(self._get_http_url(), username, project_name, 'experiments')

        if background:
            self.transport.async_post(request_url, json_data=experiment_data)
            return None

        try:
            response = self.transport.post(request_url, json_data=experiment_data)
            return self.prepare_results(response_json=response.json(), config=ExperimentConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while creating experiment.')
            return None

    def list_jobs(self, username, project_name, query=None, sort=None, page=1):
        """Fetch list of jobs related to this project."""
        request_url = self.build_url(
            self._get_http_url(), username, project_name, 'jobs')

        try:
            params = self.get_page(page=page)
            if query:
                params['query'] = query
            if sort:
                params['sort'] = sort
            response = self.transport.get(request_url, params=params)
            return self.prepare_list_results(response.json(), page, JobConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving jobs.')
            return []

    def create_job(self, username, project_name, job_config, background=False):
        job_config = self.validate_config(config=job_config, config_schema=JobConfig)
        request_url = self.build_url(self._get_http_url(), username, project_name, 'jobs')

        if background:
            self.transport.async_post(request_url, json_data=job_config.to_dict())
            return None

        try:
            response = self.transport.post(request_url, json_data=job_config.to_dict())
            return self.prepare_results(response_json=response.json(), config=JobConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while creating job.')
            return None

    def list_builds(self, username, project_name, query=None, sort=None, page=1):
        """Fetch list of build jobs related to this project."""
        request_url = self.build_url(
            self._get_http_url(), username, project_name, 'builds')

        try:
            params = self.get_page(page=page)
            if query:
                params['query'] = query
            if sort:
                params['sort'] = sort
            response = self.transport.get(request_url, params=params)
            return self.prepare_list_results(response.json(), page, JobConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while retrieving build jobs.')
            return []

    def invalidate_builds(self, username, project_name, background=False):
        """Invalidate all build jobs related to this project."""
        request_url = self.build_url(
            self._get_http_url(), username, project_name, 'builds', 'invalidate')

        if background:
            self.transport.async_post(request_url)
            return None

        try:
            return self.transport.post(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while invalidating builds.')
            return None

    def create_build(self, username, project_name, build_config, background=False):
        build_config = self.validate_config(config=build_config, config_schema=BuildJobConfig)
        request_url = self.build_url(self._get_http_url(), username, project_name, 'builds')

        if background:
            self.transport.async_post(request_url, json_data=build_config.to_dict())
            return None

        try:
            response = self.transport.post(request_url, json_data=build_config.to_dict())
            return self.prepare_results(response_json=response.json(), config=BuildJobConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while creating build job.')
            return None

    def list_tensorboards(self, username, project_name, query=None, sort=None, page=1):
        """Fetch list of tensorboard jobs related to this project."""
        request_url = self.build_url(
            self._get_http_url(), username, project_name, 'tensorboards')

        try:
            params = self.get_page(page=page)
            if query:
                params['query'] = query
            if sort:
                params['sort'] = sort
            response = self.transport.get(request_url, params=params)
            return self.prepare_list_results(response.json(), page, TensorboardJobConfig)
        except PolyaxonClientException as e:
            self.transport.handle_exception(
                e=e, log_message='Error while retrieving tensorboard jobs.')
            return []

    def start_tensorboard(self,
                          username,
                          project_name, content=None,
                          is_managed=True,
                          background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
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
            self.transport.handle_exception(e=e, log_message='Error while starting tensorboard.')
            return None

    def stop_tensorboard(self, username, project_name, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'tensorboard',
                                     'stop')

        if background:
            self.transport.async_post(request_url)
            return None

        try:
            return self.transport.post(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while stopping tensorboard.')
            return None

    def start_notebook(self,
                       username,
                       project_name,
                       content=None,
                       is_managed=True,
                       background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'notebook',
                                     'start')

        content = self.validate_content(content=content)
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
            self.transport.handle_exception(e=e, log_message='Error while starting notebook.')
            return None

    def stop_notebook(self, username, project_name, commit=True, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'notebook',
                                     'stop')
        json_data = None
        if commit is False:
            json_data = {'commit': commit}

        if background:
            self.transport.async_post(request_url, json_data=json_data)
            return None

        try:
            return self.transport.post(request_url, json_data=json_data)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while stopping notebook.')
            return None

    def bookmark(self, username, project_name, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'bookmark')

        if background:
            self.transport.async_post(request_url)
            return None

        try:
            return self.transport.post(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while bookmarking project.')
            return None

    def unbookmark(self, username, project_name, background=False):
        request_url = self.build_url(self._get_http_url(),
                                     username,
                                     project_name,
                                     'unbookmark')

        if background:
            self.transport.async_delete(request_url)
            return None

        try:
            return self.transport.delete(request_url)
        except PolyaxonClientException as e:
            self.transport.handle_exception(e=e, log_message='Error while unbookmarking project.')
            return None
