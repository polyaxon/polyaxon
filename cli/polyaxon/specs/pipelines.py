#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8
from __future__ import absolute_import, division, print_function

from polyaxon import kinds
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.schemas.polyflow.pipeline import PipelineConfig
from polyaxon.specs.base import BaseSpecification


class ScheduleSpecificationMixin(object):
    @property
    def schedule(self):
        return self.config.schedule

    @property
    def schedule_kind(self):
        return self.schedule.kind if self.schedule else None

    @property
    def schedule_start_at(self):
        return self.schedule.start_at if self.schedule else None

    @property
    def schedule_end_at(self):
        return self.schedule.end_at if self.schedule else None

    @property
    def schedule_frequency(self):
        return self.schedule.frequency if self.schedule else None

    @property
    def schedule_cron(self):
        return self.schedule.cron if self.schedule else None

    @property
    def schedule_depends_on_past(self):
        return self.schedule.depends_on_past if self.schedule else None

    @property
    def execute_at(self):
        return self.schedule.execute_at if self.schedule else None


class PipelineSpecification(BaseSpecification, ScheduleSpecificationMixin):
    """The polyaxonfile specification for pipelines.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
    """

    _SPEC_KIND = kinds.PIPELINE

    CONFIG = PipelineConfig

    def apply_container_contexts(self, contexts=None):
        raise PolyaxonSchemaError(
            "This method is not allowed on this specification."
        )

    def apply_context(self):
        self.config.process_dag()
        self.config.validate_dag()
        self.config.process_templates()
        return self
