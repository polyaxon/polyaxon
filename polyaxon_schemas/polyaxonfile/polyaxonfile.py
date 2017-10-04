# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.polyaxonfile import validator
from polyaxon_schemas.polyaxonfile import reader
from polyaxon_schemas.polyaxonfile.parser import Parser
from polyaxon_schemas.polyaxonfile.specification import Specification
from polyaxon_schemas.settings import ClusterConfig, RunTypes


class PolyaxonFile(object):
    """Parses Polyaxonfiles, and validate that it respects the current file specification"""

    def __init__(self, filepath):
        self._filepath = filepath

        self._data = reader.read(self._filepath)
        self._parsed_data = Parser.parse(self._data)
        self._validated_data = validator.validate(self._parsed_data)

    @classmethod
    def read(cls, filepath):
        if isinstance(filepath, cls):
            return filepath
        return cls(filepath)

    @property
    def data(self):
        return self._data

    @property
    def parsed_data(self):
        return self._parsed_data

    @property
    def validated_data(self):
        return self._validated_data

    @property
    def project_path(self):
        project_path = None
        if self.settings:
            project_path = self.settings.logging.path

        return project_path or '/tmp/plx_logs/' + self.project.name

    @property
    def version(self):
        return self.validated_data[Specification.VERSION]

    @property
    def project(self):
        return self.validated_data[Specification.PROJECT]

    @property
    def model(self):
        return self.validated_data[Specification.MODEL]

    @property
    def settings(self):
        return self.validated_data.get(Specification.SETTINGS, None)

    @property
    def environment(self):
        return self.validated_data.get(Specification.ENVIRONMENT, None)

    @property
    def train(self):
        return self.validated_data.get(Specification.TRAIN, None)

    @property
    def eval(self):
        return self.validated_data.get(Specification.EVAL, None)

    @property
    def run_type(self):
        return self.settings.run_type if self.settings else RunTypes.LOCAL

    @property
    def cluster_def(self):
        cluster = {
            'master': 1,
        }
        is_distributed = False

        if self.environment:
            cluster['worker'] = self.environment.n_workers
            cluster['ps'] = self.environment.n_ps
            is_distributed = True

        return cluster, is_distributed

    def get_cluster(self, host='127.0.0.1', master_port=10000, worker_port=11000, ps_port=12000):
        def get_address(port):
            return '{}:{}'.format(host, port)

        cluster_def, is_distributed = self.cluster_def

        cluster_config = {
            'master': [get_address(master_port)]
        }

        workers = []
        for i in range(cluster_def.get('worker', 0)):
            workers.append(get_address(worker_port))
            worker_port += 1

        cluster_config['worker'] = workers

        ps = []
        for i in range(cluster_def.get('ps', 0)):
            ps.append(get_address(ps_port))
            ps_port += 1

        cluster_config['ps'] = ps

        return ClusterConfig.from_dict(cluster_config)
