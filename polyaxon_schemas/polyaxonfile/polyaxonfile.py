# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.polyaxonfile import validator
from polyaxon_schemas.polyaxonfile import reader
from polyaxon_schemas.polyaxonfile.parser import Parser


class PolyaxonFile(object):
    """Parses Polyaxonfiles, and validate that it respects the current file specification"""

    def __init__(self, filepath):
        self._filepath = filepath

        self._data = reader.read(self._filepath)
        self._parsed_data = Parser.parse(self._data)
        self._validated_data = validator.validate(self._parsed_data)

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
        return self.validated_data['version']

    @property
    def project(self):
        return self.validated_data['project']

    @property
    def model(self):
        return self.validated_data['model']

    @property
    def settings(self):
        return self.validated_data.get('settings', None)

    @property
    def train(self):
        return self.validated_data.get('train', None)

    @property
    def eval(self):
        return self.validated_data.get('eval', None)
