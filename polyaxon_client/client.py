# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from datetime import datetime

from hestia.tz_utils import utc

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
from polyaxon_client.transport import Transport


class PolyaxonClient(object):
    def __init__(self,
                 api_config=None,
                 host=None,
                 token=None,
                 port=None,
                 http_port=None,
                 ws_port=None,
                 use_https=False,
                 verify_ssl=None,
                 is_managed=None,
                 authentication_type=None,
                 api_version=None,
                 reraise=False,
                 schema_response=None,
                 timeout=None):

        self._api_config = api_config or ApiConfig(host=host,
                                                   port=port,
                                                   http_port=http_port,
                                                   ws_port=ws_port,
                                                   token=token,
                                                   authentication_type=authentication_type,
                                                   version=api_version,
                                                   use_https=use_https,
                                                   verify_ssl=verify_ssl,
                                                   is_managed=is_managed,
                                                   schema_response=schema_response,
                                                   reraise=reraise,
                                                   timeout=timeout)

        self._transport = None
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
        self._transport = None
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
        return self.api_config.host

    @property
    def http_port(self):
        return self.api_config.http_port

    @property
    def ws_port(self):
        return self.api_config.ws_port

    @property
    def use_https(self):
        return self.api_config.use_https

    @property
    def verify_ssl(self):
        return self.api_config.verify_ssl

    @property
    def token(self):
        return self.api_config.token

    @property
    def authentication_type(self):
        return self.api_config.authentication_type

    @property
    def is_managed(self):
        return self.api_config.is_managed

    @property
    def api_version(self):
        return self.api_config.version

    @property
    def reraise(self):
        return self.api_config.reraise

    @property
    def timeout(self):
        return self.api_config.timeout

    def set_host(self, host):
        self.api_config.host = host
        self.reset()

    def set_http_port(self, http_port):
        self.api_config.http_port = http_port
        self.reset()

    def set_ws_port(self, ws_port):
        self.api_config.ws_port = ws_port
        self.reset()

    def set_use_https(self, use_https):
        self.api_config.use_https = use_https
        self.reset()

    def set_verify_ssl(self, verify_ssl):
        self.api_config.verify_ssl = verify_ssl
        self.reset()

    def set_token(self, token):
        self.api_config.token = token
        self.reset()

    def set_is_managed(self, is_managed):
        self.api_config.is_managed = is_managed
        self.reset()

    def set_authentication_type(self, authentication_type):
        self.api_config.authentication_type = authentication_type
        self.reset()

    def set_version_api(self, version_api):
        self.api_config.version = version_api
        self.reset()

    def set_reraise(self, reraise):
        self.api_config.reraise = reraise
        self.reset()

    def set_health_check(self, url):
        self.transport.set_health_check(url)

    def unset_health_check(self, url):
        self.transport.unset_health_check(url)

    def set_internal_health_check(self):
        if settings.INTERNAL_HEALTH_CHECK_URL:
            self.set_health_check(
                self.auth.build_url(self.api_config.base_url, settings.INTERNAL_HEALTH_CHECK_URL))

    def reconcile(self, status):
        if settings.INTERNAL_RECONCILE_URL:
            self.transport.post(
                url=self.auth.build_url(self.api_config.base_url, settings.INTERNAL_RECONCILE_URL),
                json_data={'status': status, 'created_at': str(utc.localize(datetime.utcnow()))})

    @property
    def transport(self):
        if not self._transport:
            self._transport = Transport(config=self.api_config)
        return self._transport

    @property
    def api_config(self):
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
