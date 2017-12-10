# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.experiment import (
    ExperimentConfig,
    ExperimentJobConfig,
    ExperimentStatusConfig,
    ExperimentJobStatusConfig
)

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonException


class ExperimentClient(PolyaxonClient):
    """Client to get experiments from the server"""
    ENDPOINT = "/experiments"

    def list_experiments(self, page=1):
        """This gets all experiments visible to the user from the server."""
        try:
            response = self.get(self._get_url(), params=self.get_page(page=page))
            experiments_dict = response.json()
            return [ExperimentConfig.from_dict(experiment)
                    for experiment in experiments_dict.get("results", [])]
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiments')
            return []

    def get_experiment(self, experiment_uuid):
        request_url = self._build_url(self._get_url(), experiment_uuid)
        try:
            response = self.get(request_url)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment')
            return None

    def update_experiment(self, experiment_uuid, patch_dict):
        request_url = self._build_url(self._get_url(), experiment_uuid)
        try:
            response = self.patch(request_url, json=patch_dict)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while updating experiment')
            return None

    def delete_experiment(self, experiment_uuid):
        request_url = self._build_url(self._get_url(), experiment_uuid)
        try:
            response = self.delete(request_url)
            return response
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while deleting experiment')
            return None

    def get_status(self, experiment_uuid):
        request_url = self._build_url(self._get_url(), experiment_uuid, 'status')
        try:
            response = self.get(request_url)
            return ExperimentStatusConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving experiment status')
            return None

    def list_jobs(self, experiment_uuid, page=1):
        """Fetch list of jobs related to this experiment."""
        request_url = self._build_url(self._get_url(), experiment_uuid, 'jobs')

        try:
            response = self.get(request_url, params=self.get_page(page=page))
            jobs = response.json()
            return [ExperimentJobConfig.from_dict(job) for job in jobs.get("results", [])]
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving jobs')
            return []

    def get_job_status(self, experiment_uuid, job_uuid):
        request_url = self._build_url(self._get_url(), experiment_uuid, 'jobs', job_uuid, 'status')

        try:
            response = self.get(request_url)
            return ExperimentJobStatusConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while retrieving job status')
            return []

    def restart(self, experiment_uuid):
        """Restart an experiment."""
        request_url = self._build_url(self._get_url(), experiment_uuid, 'restart')

        try:
            response = self.post(request_url)
            return ExperimentConfig.from_dict(response.json())
        except PolyaxonException as e:
            self.handle_exception(e=e, log_message='Error while restarting experiment')
            return None
