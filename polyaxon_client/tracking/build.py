# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.handlers.conf import setup_logging
from polyaxon_client.tracking.job import BaseJob
from polyaxon_client.tracking.no_op import check_no_op
from polyaxon_client.tracking.utils.backend import OTHER_BACKEND


class BuildJob(BaseJob):
    REQUIRES_OUTPUTS = False

    @check_no_op
    def __init__(self,
                 project=None,
                 job_id=None,
                 client=None,
                 track_logs=True,
                 track_code=True):
        super(BuildJob, self).__init__(
            project=project,
            job_id=job_id,
            job_type='builds',
            client=client,
            track_logs=track_logs,
            track_code=track_code)

    @check_no_op
    def create(self,
               name=None,
               backend=None,
               tags=None,
               description=None,
               content=None):
        build_config = {}
        if name:
            build_config['name'] = name
        if tags:
            build_config['tags'] = tags
        build_config['backend'] = OTHER_BACKEND
        if backend:
            build_config['backend'] = backend
        if description:
            build_config['description'] = description
        if content:
            build_config['content'] = self.client.project.validate_content(content=content)
        build_config['is_managed'] = settings.IS_MANAGED

        build = self.client.project.create_build(
            username=self.username,
            project_name=self.project_name,
            build_config=build_config,
        )
        if not build:
            raise PolyaxonClientException('Could not create build.')
        if not settings.IS_MANAGED and self.track_logs:
            setup_logging(send_logs=self.send_logs)
        self.job_id = self._get_entity_id(build)
        self.job = build
        self.last_status = 'created'

        if self.track_code:
            self.log_code_ref()

        if not settings.IS_MANAGED:
            self._start()
            self._set_health_url()

        return self

    def _update(self, patch_dict):
        self.client.build_job.update_build(username=self.username,
                                           project_name=self.project_name,
                                           job_id=self.job_id,
                                           patch_dict=patch_dict,
                                           background=True)

    @check_no_op
    def log_dockerfile(self, dockerfile):
        self._update({'dockerfile': dockerfile})
