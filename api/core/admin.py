# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from core.models import (
    Agent,
    AgentMemory,
    Bridge,
    Decoder,
    Encoder,
    Environment,
    Estimator,
    Experiment,
    InputData,
    Loss,
    Metric,
    Optimizer,
    Pipeline,
    PolyaxonModel,
    RunConfig,
    SubGraph,
)

admin.site.register(Agent)
admin.site.register(AgentMemory)
admin.site.register(Environment)
admin.site.register(Loss)
admin.site.register(Metric)
admin.site.register(Optimizer)
admin.site.register(Bridge)
admin.site.register(Encoder)
admin.site.register(Decoder)
admin.site.register(SubGraph)
admin.site.register(PolyaxonModel)
admin.site.register(Estimator)
admin.site.register(Pipeline)
admin.site.register(InputData)
admin.site.register(RunConfig)
admin.site.register(Experiment)
