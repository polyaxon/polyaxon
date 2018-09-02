# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client import settings
from polyaxon_client.api.auth import AuthApi
from polyaxon_client.api.bookmark import BookmarkApi
from polyaxon_client.api.build_job import BuildJobApi
from polyaxon_client.api.cluster import ClusterApi
from polyaxon_client.api.experiment import ExperimentApi
from polyaxon_client.api.experiment_group import ExperimentGroupApi
from polyaxon_client.api.experiment_job import ExperimentJobApi
from polyaxon_client.api.job import JobApi
from polyaxon_client.api.project import ProjectApi
from polyaxon_client.api.user import UserApi
from polyaxon_client.api.version import VersionApi
from polyaxon_client.api_config import ApiConfig
from polyaxon_client.exceptions import PolyaxonException
from polyaxon_client.transport import Transport

DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443


class PolyaxonClient(object):
    def __init__(self,
                 host=None,
                 token=None,
                 http_port=None,
                 ws_port=None,
                 use_https=False,
                 in_cluster=settings.IN_CLUSTER,
                 authentication_type=settings.AuthenticationTypes.TOKEN,
                 api_version='v1',
                 reraise=False):
        if not all([host, token]) and not in_cluster:
            raise PolyaxonException(
                'Client requires at least a host and a token if not running in-cluster.')

        self._host = host
        self._http_port = http_port or (DEFAULT_HTTPS_PORT
                                        if use_https
                                        else DEFAULT_HTTP_PORT)
        self._ws_port = ws_port or (DEFAULT_HTTPS_PORT
                                    if use_https
                                    else DEFAULT_HTTP_PORT)
        self._use_https = use_https
        self._token = token
        self._in_cluster = in_cluster
        self._authentication_type = authentication_type
        self._api_version = api_version
        self._reraise = reraise

        self._transport = None
        self._api_config = None

        self._auth_api = None
        self._cluster_api = None
        self._version_api = None
        self._project_api = None
        self._experiment_group_api = None
        self._experiment_api = None
        self._experiment_job_api = None
        self._job_api = None
        self._build_job_api = None
        self._user_api = None
        self._bookmark_api = None

    def reset(self):
        if not all([self.host, self.token]) and not self.in_cluster:
            raise PolyaxonException(
                'Client requires at least a host and a token if not running in-cluster.')

        self._transport = None
        self._api_config = None

        self._auth_api = None
        self._cluster_api = None
        self._version_api = None
        self._project_api = None
        self._experiment_group_api = None
        self._experiment_api = None
        self._experiment_job_api = None
        self._job_api = None
        self._build_job_api = None
        self._user_api = None
        self._bookmark_api = None

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

    @property
    def authentication_type(self):
        return self._authentication_type

    @property
    def in_cluster(self):
        return self._in_cluster

    @property
    def api_version(self):
        return self._api_version

    @property
    def reraise(self):
        return self._reraise

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

    def set_in_cluster(self, in_cluster):
        self._in_cluster = in_cluster
        self.reset()

    def set_authentication_type(self, authentication_type):
        self._authentication_type = authentication_type
        self.reset()

    def set_version_api(self, version_api):
        self._api_version = version_api
        self.reset()

    def set_reraise(self, reraise):
        self._reraise = reraise
        self.reset()

    @property
    def transport(self):
        if not self._transport:
            self._transport = Transport(token=self.api_config.token,
                                        authentication_type=self.api_config.authentication_type,
                                        reraise=self.api_config.reraise)
        return self._transport

    @property
    def api_config(self):
        if not self._api_config:
            self._api_config = ApiConfig(host=self.host,
                                         http_port=self.http_port,
                                         ws_port=self.ws_port,
                                         token=self.token,
                                         authentication_type=self.authentication_type,
                                         version=self.api_version,
                                         use_https=self.use_https,
                                         reraise=self.reraise,
                                         in_cluster=self.in_cluster)
        return self._api_config

    @property
    def auth(self):
        if not self._auth_api:
            self._auth_api = AuthApi(transport=self.transport,
                                     config=self.api_config)
        return self._auth_api

    @property
    def cluster(self):
        if not self._cluster_api:
            self._cluster_api = ClusterApi(transport=self.transport,
                                           config=self.api_config)
        return self._cluster_api

    @property
    def version(self):
        if not self._version_api:
            self._version_api = VersionApi(transport=self.transport,
                                           config=self.api_config)
        return self._version_api

    @property
    def project(self):
        if not self._project_api:
            self._project_api = ProjectApi(transport=self.transport,
                                           config=self.api_config)
        return self._project_api

    @property
    def experiment_group(self):
        if not self._experiment_group_api:
            self._experiment_group_api = ExperimentGroupApi(transport=self.transport,
                                                            config=self.api_config)
        return self._experiment_group_api

    @property
    def experiment(self):
        if not self._experiment_api:
            self._experiment_api = ExperimentApi(transport=self.transport,
                                                 config=self.api_config)
        return self._experiment_api

    @property
    def experiment_job(self):
        if not self._experiment_job_api:
            self._experiment_job_api = ExperimentJobApi(transport=self.transport,
                                                        config=self.api_config)
        return self._experiment_job_api

    @property
    def job(self):
        if not self._job_api:
            self._job_api = JobApi(transport=self.transport,
                                   config=self.api_config)
        return self._job_api

    @property
    def build_job(self):
        if not self._build_job_api:
            self._build_job_api = BuildJobApi(transport=self.transport,
                                              config=self.api_config)
        return self._build_job_api

    @property
    def user(self):
        if not self._user_api:
            self._user_api = UserApi(transport=self.transport,
                                     config=self.api_config)
        return self._user_api

    @property
    def bookmark(self):
        if not self._bookmark_api:
            self._bookmark_api = BookmarkApi(transport=self.transport,
                                             config=self.api_config)
        return self._bookmark_api
