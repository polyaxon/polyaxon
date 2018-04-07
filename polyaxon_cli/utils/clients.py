# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.managers.config import GlobalConfigManager
from polyaxon_client.auth import AuthClient
from polyaxon_client.cluster import ClusterClient
from polyaxon_client.experiment import ExperimentClient
from polyaxon_client.experiment_group import ExperimentGroupClient
from polyaxon_client.jobs import JobClient
from polyaxon_client.project import ProjectClient
from polyaxon_client.user import UserClient
from polyaxon_client.version import VersionClient


class PolyaxonClients(object):
    def __init__(self):
        self.host = GlobalConfigManager.get_value('host')
        self.http_port = GlobalConfigManager.get_value('http_port')
        self.ws_port = GlobalConfigManager.get_value('ws_port')
        self.use_https = GlobalConfigManager.get_value('use_https')
        self.token = AuthConfigManager.get_value('token')
        self.params = dict(
            host=self.host,
            http_port=self.http_port,
            ws_port=self.ws_port,
            token=self.token,
            use_https=self.use_https,
            reraise=True)

    @property
    def auth(self):
        return AuthClient(**self.params)

    @property
    def cluster(self):
        return ClusterClient(**self.params)

    @property
    def version(self):
        return VersionClient(**self.params)

    @property
    def project(self):
        return ProjectClient(**self.params)

    @property
    def experiment_group(self):
        return ExperimentGroupClient(**self.params)

    @property
    def experiment(self):
        return ExperimentClient(**self.params)

    @property
    def job(self):
        return JobClient(**self.params)

    @property
    def user(self):
        return UserClient(**self.params)
