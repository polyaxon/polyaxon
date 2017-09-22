# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from polyaxon.estimators.estimator_spec import EstimatorSpec
from polyaxon.estimators.run_config import RunConfig
from polyaxon.estimators.estimator import Estimator
from polyaxon.estimators.agents import BaseAgent, Agent, PGAgent, TRPOAgent
from polyaxon.estimators.hooks import HOOKS


ESTIMATORS = OrderedDict([
    ('Estimator', Estimator),
])

AGENTS = OrderedDict([
    ('Agent', Agent),
    ('PGAgent', PGAgent),
    ('TRPOAgent', TRPOAgent)
])
