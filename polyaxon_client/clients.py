# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.auth import AuthClient
from polyaxon_client.bookmark import BookmarkClient
from polyaxon_client.build_job import BuildJobClient
from polyaxon_client.cluster import ClusterClient
from polyaxon_client.experiment import ExperimentClient
from polyaxon_client.experiment_group import ExperimentGroupClient
from polyaxon_client.experiment_job import ExperimentJobClient
from polyaxon_client.job import JobClient
from polyaxon_client.project import ProjectClient
from polyaxon_client.user import UserClient
from polyaxon_client.version import VersionClient


class PolyaxonClients(object):
    def __init__(self, host, token, http_port=80, ws_port=80, use_https=False):
        self._updated = False
        self._host = host
        self._http_port = http_port
        self._ws_port = ws_port
        self._use_https = use_https
        self._token = token
        self.params = dict(
            host=self.host,
            http_port=self.http_port,
            ws_port=self.ws_port,
            token=self.token,
            use_https=self.use_https,
            reraise=True)

        self._auth_client = None
        self._cluster_client = None
        self._version_client = None
        self._project_client = None
        self._experiment_group_client = None
        self._experiment_client = None
        self._experiment_job_client = None
        self._job_client = None
        self._build_job_client = None
        self._user_client = None
        self._bookmark_client = None

    def reset(self):
        self._auth_client = None
        self._cluster_client = None
        self._version_client = None
        self._project_client = None
        self._experiment_group_client = None
        self._experiment_client = None
        self._experiment_job_client = None
        self._job_client = None
        self._build_job_client = None
        self._user_client = None
        self._bookmark_client = None

    @property
    def host(self):
        return self._host

    @property
    def http_port(self):
        return self._http_port

    @property
    def ws_port(self):
        return self._ws_port

    @property
    def use_https(self):
        return self._use_https

    @property
    def token(self):
        return self._token

    def set_host(self, host):
        self._host = host
        self.reset()

    def set_http_port(self, http_port):
        self._http_port = http_port
        self.reset()

    def set_ws_port(self, ws_port):
        self._ws_port = ws_port
        self.reset()

    def set_use_https(self, use_https):
        self._use_https = use_https
        self.reset()

    def set_token(self, token):
        self._token = token
        self.reset()

    @property
    def auth(self):
        if not self._auth_client:
            self._auth_client = AuthClient(**self.params)
        return self._auth_client

    @property
    def cluster(self):
        if not self._cluster_client:
            self._cluster_client = ClusterClient(**self.params)
        return self._cluster_client

    @property
    def version(self):
        if not self._version_client:
            self._version_client = VersionClient(**self.params)
        return self._version_client

    @property
    def project(self):
        if not self._project_client:
            self._project_client = ProjectClient(**self.params)
        return self._project_client

    @property
    def experiment_group(self):
        if not self._experiment_group_client:
            self._experiment_group_client = ExperimentGroupClient(**self.params)
        return self._experiment_group_client

    @property
    def experiment(self):
        if not self._experiment_client:
            self._experiment_client = ExperimentClient(**self.params)
        return self._experiment_client

    @property
    def experiment_job(self):
        if not self._experiment_job_client:
            self._experiment_job_client = ExperimentJobClient(**self.params)
        return self._experiment_job_client

    @property
    def job(self):
        if not self._job_client:
            self._job_client = JobClient(**self.params)
        return self._job_client

    @property
    def build_job(self):
        if not self._build_job_client:
            self._build_job_client = BuildJobClient(**self.params)
        return self._build_job_client

    @property
    def user(self):
        if not self._user_client:
            self._user_client = UserClient(**self.params)
        return self._user_client

    @property
    def bookmark(self):
        if not self._bookmark_client:
            self._bookmark_client = BookmarkClient(**self.params)
        return self._bookmark_client
