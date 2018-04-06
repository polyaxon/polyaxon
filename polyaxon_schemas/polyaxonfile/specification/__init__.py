# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.polyaxonfile.specification.experiment import ExperimentSpecification
from polyaxon_schemas.polyaxonfile.specification.group import GroupSpecification
from polyaxon_schemas.polyaxonfile.specification.plugin import PluginSpecification

SPECIFICATION_BY_KIND = {
    ExperimentSpecification._SPEC_KIND: ExperimentSpecification,
    GroupSpecification._SPEC_KIND: GroupSpecification,
    PluginSpecification._SPEC_KIND: PluginSpecification
}
