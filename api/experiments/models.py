# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models

from libs.models import DiffModel
from projects.models import PolyaxonFile


class Experiment(DiffModel):
    """A model that represents experiments created through a polyaxonfile."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    name = models.CharField(max_length=256, blank=True, null=True,
                            help_text='Name of the experiment')
    description = models.TextField(blank=True, null=True,
                                   help_text='Description of the experiment.')
    polyaxonfile = models.ForeignKey(PolyaxonFile,
                                     help_text='The polyaxonfile that generate this experiment.')
    compiled_polyaxonfile = JSONField(help_text='The compiled polyaxon with specific values '
                                                'for this experiment.')
